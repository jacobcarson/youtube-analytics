import pandas as pd
import plotly.express as px
from src.visualization.base import VisualizationResult

# Chart 3 Distribution of youtubers by country    
class YoutubersByCountryDist:
    """Analyzer for Global Distribution of YouTubers"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def create_visualization(self) -> VisualizationResult:
        """Create bar chart for global distribution of YouTubers"""
        if 'Country' not in self.df.columns:
            return VisualizationResult()
            
        # YouTubers by country
        country_counts = self.df['Country'].value_counts().reset_index()
        country_counts.columns = ['Country', 'Count']
        
        # bar chart
        fig = px.bar(
            country_counts,
            x='Country',
            y='Count',
            title='Global Distribution of Top YouTubers',
            labels={'Count': 'Number of YouTubers'},
            template='plotly_white'
        )
        
        # metrics
        metrics = {
            'top_country': country_counts.iloc[0]['Country'],
            'top_count': country_counts.iloc[0]['Count'],
            'total_countries': len(country_counts)
        }
        
        # insights
        insights = [
            f"Most YouTubers are from {metrics['top_country']} ({metrics['top_count']} channels)",
            f"Top creators spread across {metrics['total_countries']} countries"
        ]
        
        return VisualizationResult(figure=fig, metrics=metrics, insights=insights)
    