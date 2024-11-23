import pandas as pd
import plotly.graph_objects as go
from src.visualization.base import VisualizationResult

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