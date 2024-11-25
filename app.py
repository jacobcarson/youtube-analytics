import streamlit as st
import pandas as pd
from src.preprocessing.data_loader import DataLoader
from src.constants import ANALYZERS_CONFIG

def render(title: str, analyzer_class: any, df: pd.DataFrame, prediction: False):
    """Generic function to render analysis"""
    st.subheader(title)
    analyzer = analyzer_class(df)
    result = analyzer.create_visualization()
    
    if result.figure:
        st.plotly_chart(result.figure, use_container_width=True)
        
        # Display metrics if available
        if result.metrics:
            st.markdown("### Metrics")
            for metric_name, metric_value in result.metrics.items():
                st.metric(metric_name, metric_value)
        
        # Display insights
        if result.insights:
            st.markdown("### Key Insights")
            for insight in result.insights:
                st.info(f"- {insight}")

        # Optional: Render prediction analysis
        if prediction:
            # Add separator and extra spacing
            st.markdown("---")  # Separator line
            st.markdown("")  # Blank markdown for minimal spacing
            st.empty()  # Spacer for extra padding

            st.markdown("### Prediction Analysis")
            prediction_result = analyzer.create_prediction()
            
            if prediction_result.figure:
                st.plotly_chart(prediction_result.figure, use_container_width=True)
            
            if prediction_result.metrics:
                st.markdown("### Model Metrics")
                for metric_name, metric_value in prediction_result.metrics.items():
                    st.metric(metric_name, metric_value)
            
            if prediction_result.insights:
                st.markdown("### Insights")
                for insight in prediction_result.insights:
                    st.info(f"- {insight}")

            if hasattr(prediction_result, "extra_data"):
                st.markdown("### R² Scores for Other Models")
                st.dataframe(prediction_result.extra_data)

def render_dashboard(df_top: pd.DataFrame, df_view: pd.DataFrame):
    """Render all graphs together in a custom dashboard view"""

    # number of columns in each row
    custom_column_layout = [2, 1, 2, 1, 1, 1]  # Example: 2 graphs in first row, 1 in the second, etc.

    graphs = []

    analyzers_sorted = { # for better visualization
        "Category Distribution": ANALYZERS_CONFIG.get("Category Distribution"),
        "Most Subscribers Analysis": ANALYZERS_CONFIG.get("Most Subscribers Analysis"),
        "Likes vs Subscribers": ANALYZERS_CONFIG.get("Likes vs Subscribers"),
        "Global Distribution": ANALYZERS_CONFIG.get("Global Distribution"),
        "Followers by Category": ANALYZERS_CONFIG.get("Followers by Category"),
        "Annual Views for Top Channels": ANALYZERS_CONFIG.get("Annual Views for Top Channels"),
        "Income Analysis": ANALYZERS_CONFIG.get("Income Analysis"),
        "Clustering Channels": ANALYZERS_CONFIG.get("Clustering Channels")
    }
    
    # Generate results for each analyzer
    for _, config in analyzers_sorted.items():
        analyzer_class = config["analyzer_class"]

        # Select the correct DataFrame (df_view or df_top)
        df = df_view if config["title"] == "Annual Views for Top Channels" else df_top
        analyzer = analyzer_class(df)
        result = analyzer.create_visualization() # Replace this function for a custom one if you want a different visualization
        graphs.append(result.figure)

    # Render the graphs in a custom grid layout
    graph_idx = 0
    for row_columns in custom_column_layout:
        cols = st.columns(row_columns)  # Create a row with the specified number of columns
        for col in cols:
            if graph_idx < len(graphs):
                figure = graphs[graph_idx]
                with col:
                    st.plotly_chart(figure, use_container_width=True)
                graph_idx += 1

def main() -> None:
    st.set_page_config(page_title="YouTube Analytics", page_icon="📊", layout="wide")
    st.title("📊 YouTube Channel Analytics")
    
    # Sidebar
    dashboard_mode = st.sidebar.button("Dashboard", use_container_width= True)
    analysis = st.sidebar.selectbox(
        "Choose Analysis",
        list(ANALYZERS_CONFIG.keys())
    )
    
    # Load data
    df_top, df_view = DataLoader.load_data()
    
    if df_top is not None and df_view is not None:
        if dashboard_mode:
            # Render the dashboard with all graphs
            render_dashboard(df_top, df_view)
            return 
        
        # data preview
        st.subheader("Data Preview")
        analyzer_config = ANALYZERS_CONFIG.get(analysis)

        if analyzer_config["title"] == "Annual Views for Top Channels":
            st.dataframe(df_view.head())
            render(analyzer_config["title"], analyzer_config["analyzer_class"], df_view, analyzer_config.get("prediction", False))
        else:
            st.dataframe(df_top.head())
            render(analyzer_config["title"], analyzer_config["analyzer_class"], df_top, analyzer_config.get("prediction", False))

if __name__ == "__main__":
    main()