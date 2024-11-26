import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
            hole=0.5,
            width=1200,
            height=800
        )

        fig.update_traces(hoverinfo='label+percent', textinfo='percent', textfont_size=20, textposition='inside')

        fig.update_layout(
        title={
                'text': '📊 Category Distribution of Top Youtube Channels',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
        },
        font=dict(family="Arial", size=12),
        uniformtext_minsize=16,
        uniformtext_mode='hide'
        )

        metrics = {
            'Top Category': category_counts.index[0],
            'Number of Categories': len(category_counts)
        }
        
        insights = [
            f"Most common category: {metrics['Top Category']}",
            f"Total number of categories: {metrics['Number of Categories']}"
        ]
        
        return VisualizationResult(figure=fig, metrics=metrics, insights=insights)
