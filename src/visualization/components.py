import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
    
# Chart 5 Quarterly income of top 5 YouTube channels  
class QuarterlyIncomeAnalyzer:
    """Analyzer for Quarterly Income of Top 5 YouTube Channels"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def create_visualization(self) -> VisualizationResult:
        """Create bar chart for average quarterly income"""
        if 'ChannelName' not in self.df.columns or not all(
            col in self.df.columns for col in ['Income q1', 'Income q2', 'Income q3', 'Income q4']
        ):
            return VisualizationResult()
        
        # Top 5 Channels by Total Views
        top5_channels = self.df.groupby('ChannelName')['Views'].sum().nlargest(5).index
        top5_df = self.df[self.df['ChannelName'].isin(top5_channels)]
        
        # Calculate total and average income
        top5_df['Total Income'] = top5_df[['Income q1', 'Income q2', 'Income q3', 'Income q4']].sum(axis=1)
        income_avg = top5_df.groupby('ChannelName')['Total Income'].mean().reset_index()
        income_avg.columns = ['ChannelName', 'Average Income']
        
        # Format income values for display
        income_avg['Formatted Income'] = income_avg['Average Income'].apply(lambda x: f"${x / 1_000_000:.1f}M")
        
        # Highlight top channel
        top_channel = income_avg.iloc[0]
        colors = ['#636EFA' if channel != top_channel['ChannelName'] else '#EF553B' 
                  for channel in income_avg['ChannelName']]

        # Create Plotly bar chart
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=income_avg['ChannelName'],
            y=income_avg['Average Income'],
            text=income_avg['Formatted Income'],
            textposition='outside',
            marker=dict(color=colors, line=dict(color='black', width=1)),
        ))

        # Calculate y-axis range
        max_income = income_avg['Average Income'].max()
        y_range = [0, max_income * 1.1]  # For better visualization

        fig.update_layout(
            title={
                'text': '💰 Average Quarterly Income of Top 5 YouTube Channels',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis=dict(title='Channel Name', tickangle=45),
            yaxis=dict(title='Average Income ($M)', range=y_range, showgrid=True),
            template='plotly_white',
            font=dict(family="Arial", size=12),
            plot_bgcolor='rgba(0,0,0,0)',
        )
        
        # Metrics and insights
        metrics = {
            'top_channel': top_channel['ChannelName'],
            'top_income': f"${top_channel['Average Income'] / 1_000_000:.1f}M"
        }
        insights = [
            f"The top channel is {metrics['top_channel']} with an average income of {metrics['top_income']} per quarter.",
            "The highlighted bar represents the channel with the highest average income.",
            "The chart uses clear annotations to make data interpretation easier."
        ]
        
        return VisualizationResult(figure=fig, metrics=metrics, insights=insights)