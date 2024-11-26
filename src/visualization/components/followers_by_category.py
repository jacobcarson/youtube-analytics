import pandas as pd
import plotly.express as px
from src.visualization.base import VisualizationResult

class FollowersByCategoryAnalyzer:
    """Analyzer for Followers by Category"""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def create_visualization(self) -> VisualizationResult:
        """Create bar chart for followers by category"""
        if 'Category' not in self.df.columns or 'followers' not in self.df.columns:
            return VisualizationResult()
        
        # Aggregate followers by category
        cat_followers = self.df.groupby('Category')['followers'].sum().sort_values(ascending=True)
        df_chart = cat_followers.reset_index()
        df_chart.columns = ['Category', 'Followers']
        
        # Convert followers to billions for better readability
        df_chart['Followers'] = df_chart['Followers'] / 1_000_000_000
        
        # Create Plotly bar chart
        fig = px.bar(
            df_chart,
            x='Category',
            y='Followers',
            title='Followers by Category',
            labels={'Category': 'Category', 'Followers': 'Followers (billion)'},
            template='plotly_white',
            width=1200,
            height=800
        )
        
        # Adjust layout with expanded y-axis range
        max_followers = df_chart['Followers'].max()
        y_margin = max_followers * 0.2  # Add 20% margin
        fig.update_layout(
            xaxis_tickangle=45,
            yaxis=dict(range=[0, max_followers + y_margin]),
            font=dict(family="Arial", size=12),
        )

        # Insights
        insights = [
            f"The category with the most followers is {df_chart.iloc[-1]['Category']} with {df_chart.iloc[-1]['Followers']:.2f} billion followers.",
            "This chart highlights the total number of followers for each category."
        ]
        
        return VisualizationResult(figure=fig, metrics=None, insights=insights)
