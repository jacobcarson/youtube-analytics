import pandas as pd
import plotly.express as px
from dataclasses import dataclass
from typing import Optional

@dataclass
class VisualizationResult:
    """Class to hold visualization results and metrics"""
    figure: Optional[object] = None
    metrics: dict = None
    insights: list[str] = None

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

class LikesSubscribersAnalyzer:
    """Analyzer for Likes vs Subscribers relationship"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        
    def prepare_data(self) -> pd.DataFrame:
        """Prepare data for analysis"""
        return self.df.dropna(subset=['Likes', 'followers'])
    
    def calculate_metrics(self, df_clean: pd.DataFrame) -> dict:
        """Calculate analysis metrics"""
        correlation = df_clean['Likes'].corr(df_clean['followers'])
        return {
            'correlation': correlation,
            'correlation_strength': self._get_correlation_strength(correlation)
        }
    
    @staticmethod 
    def _get_correlation_strength(correlation: float) -> str:
        """Determine correlation strength"""
        if correlation > 0.7:
            return "Strong positive"
        elif correlation > 0.4:
            return "Moderate positive"
        elif correlation > 0:
            return "Weak positive"
        elif correlation < -0.7:
            return "Strong negative"
        elif correlation < -0.4:
            return "Moderate negative"
        else:
            return "Weak negative"
    
    def create_visualization(self) -> VisualizationResult:
        """Create the likes vs subscribers visualization"""
        if 'Likes' not in self.df.columns or 'followers' not in self.df.columns:
            return VisualizationResult()
        
        df_clean = self.prepare_data()
        if df_clean.empty:
            return VisualizationResult()
        
        metrics = self.calculate_metrics(df_clean)
        
        # scatter plot (log scale) - bc it looks better
        fig = px.scatter(
            df_clean,
            x='Likes',
            y='followers',
            title='Relationship between Likes and Subscribers',
            labels={'Likes': 'Total Likes (log scale)', 'followers': 'Number of Subscribers (log scale)'},
            hover_data=['ChannelName'],
            trendline="ols",
            template='plotly_white',
            log_x=True,
            log_y=True
        )
        
        fig.update_traces(
            marker=dict(size=10, opacity=0.7),
            selector=dict(mode='markers')
        )
        
        # insights
        insights = [
            f"There is a {metrics['correlation_strength'].lower()} correlation (r={metrics['correlation']:.2f}) between likes and subscribers",
            "Channels are plotted on logarithmic scales to better show the relationship across different sizes",
            "The trend line shows the general relationship direction",
            "Outliers may represent channels with unusual engagement patterns",
            "Hover over points to see specific channel details"
        ]
        
        return VisualizationResult(figure=fig, metrics=metrics, insights=insights)