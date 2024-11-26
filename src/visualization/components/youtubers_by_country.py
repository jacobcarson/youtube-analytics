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
            title= 'Global Distribution of Top YouTubers',   
            labels={'Count': 'Number of YouTubers'},
            template='plotly_white',
            width=1200,
            height=800
        )

        fig.update_layout(
            title={
                    'text': '🌐 Global Distribution of Top Youtube Channels',
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
            },
            font=dict(family="Arial", size=12),
            uniformtext_minsize=16,
            uniformtext_mode='hide'
        )
        
        # metrics
        metrics = {
            'Top Country': country_counts.iloc[0]['Country'],
            'Most "Top 100" Channels in a Country': country_counts.iloc[0]['Count'],
            'Total Countries in the Top 100': len(country_counts)
        }
        
        # insights
        insights = [
            f"The highest population of \"Top 100\" YouTubers are from {metrics['Top Country']} ({metrics['Most "Top 100" Channels in a Country']} channels)",
            f"The \"Top 100\" creators are spread across {metrics['Total Countries in the Top 100']} countries"
        ]
        
        return VisualizationResult(figure=fig, metrics=metrics, insights=insights)
    