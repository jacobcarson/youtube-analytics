import pandas as pd
import plotly.express as px
from src.visualization.base import VisualizationResult

class CategoryDistributionAnalyzer:
    """Analyzer for Category Distribution"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def create_visualization(self) -> VisualizationResult:
        """Create pie chart for category distribution"""
        if 'Category' not in self.df.columns:
            return VisualizationResult()
            
        df_clean = self.df.dropna(subset=['Category'])
        category_counts = df_clean['Category'].value_counts()
        
        fig = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            title='YouTube Channels by Category',
            hole=0.3
        )
        
        metrics = {
            'top_category': category_counts.index[0],
            'category_count': len(category_counts)
        }
        
        insights = [
            f"Most common category: {metrics['top_category']}",
            f"Total number of categories: {metrics['category_count']}"
        ]
        
        return VisualizationResult(figure=fig, metrics=metrics, insights=insights)
