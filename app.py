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

def main() -> None:
    st.set_page_config(page_title="YouTube Analytics", page_icon="📊", layout="wide")
    st.title("📊 YouTube Channel Analytics")
    
    # Sidebar
    analysis = st.sidebar.selectbox(
        "Choose Analysis",
        list(ANALYZERS_CONFIG.keys())
    )
    
    # Load data
    df_top, df_view = DataLoader.load_data()
    
    if df_top is not None and df_view is not None:
        # data preview
        st.subheader("Data Preview")
        st.dataframe(df_top.head())
        
        # analysis based on selection
        analyzer_config = ANALYZERS_CONFIG.get(analysis)
        if analyzer_config:
            render(analyzer_config["title"], analyzer_config["analyzer_class"], df_top, analyzer_config.get("prediction", False))

if __name__ == "__main__":
    main()