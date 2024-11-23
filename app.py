import streamlit as st
import pandas as pd
from src.preprocessing.data_loader import DataLoader
from src.visualization.components import CategoryDistributionAnalyzer, LikesSubscribersAnalyzer, YoutubersByCountryDist, QuarterlyIncomeAnalyzer

ANALYZERS_CONFIG = {
    "Category Distribution": {
        "analyzer_class": CategoryDistributionAnalyzer,
        "title": "Category Distribution of YouTube Channels",
    },
    "Likes vs Subscribers": {
        "analyzer_class": LikesSubscribersAnalyzer,
        "title": "Likes vs Subscribers Analysis",
    },
    "Global Distribution": {
        "analyzer_class": YoutubersByCountryDist,
        "title": "Global Distribution of Top YouTubers",
    },
    "Income Analysis": {
        "analyzer_class": QuarterlyIncomeAnalyzer,
        "title": "Average Quarterly Income of Top 5 YouTube Channels",
    },
}

def render(title: str, analyzer_class: any, df: pd.DataFrame):
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
            render(analyzer_config["title"], analyzer_config["analyzer_class"], df_top)

if __name__ == "__main__":
    main()