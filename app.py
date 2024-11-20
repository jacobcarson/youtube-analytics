import streamlit as st
from src.preprocessing.data_loader import DataLoader
from src.visualization.components import CategoryDistributionAnalyzer, LikesSubscribersAnalyzer, YoutubersByCountryDist

def main() -> None:
    st.set_page_config(page_title="YouTube Analytics", page_icon="📊", layout="wide")
    st.title("📊 YouTube Channel Analytics")
    
    # Sidebar
    analysis = st.sidebar.selectbox(
        "Choose Analysis",
        ["Category Distribution", "Likes vs Subscribers", "Global Distribution",
         "View Trends", "Income Analysis", "Channel Clusters"]
    )
    
    # Load data
    df_top, df_view = DataLoader.load_data()
    
    if df_top is not None and df_view is not None:
        # data preview
        st.subheader("Data Preview")
        st.dataframe(df_top.head())
        
        # analysis based on selection
        if analysis == "Category Distribution":
            analyzer = CategoryDistributionAnalyzer(df_top)
            result = analyzer.create_visualization()
            
            if result.figure:
                st.plotly_chart(result.figure, use_container_width=True)
                for insight in result.insights:
                    st.info(insight)
                    
        elif analysis == "Likes vs Subscribers":
            st.subheader("Likes vs Subscribers Analysis")
            
            analyzer = LikesSubscribersAnalyzer(df_top)
            result = analyzer.create_visualization()
            
            if result.figure:
                st.plotly_chart(result.figure, use_container_width=True)
                
                # Display metrics
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Correlation Coefficient", 
                             f"{result.metrics['correlation']:.2f}")
                with col2:
                    st.metric("Correlation Strength", 
                             result.metrics['correlation_strength'])
                
                # Display insights
                st.markdown("### Key Insights")
                for insight in result.insights:
                    st.write(f"- {insight}")
                    
        elif analysis == "Global Distribution":
            st.subheader("Global Distribution of Top YouTubers")
            
            analyzer = YoutubersByCountryDist(df_top)
            result = analyzer.create_visualization()
            
            if result.figure:
                st.plotly_chart(result.figure, use_container_width=True)
                
                # Display insights
                for insight in result.insights:
                    st.info(insight)

if __name__ == "__main__":
    main()