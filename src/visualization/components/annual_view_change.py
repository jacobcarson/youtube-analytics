import pandas as pd
import plotly.graph_objects as go
from src.visualization.base import VisualizationResult

# Chart 5 Quarterly income of top 5 YouTube channels  
class YearlyViewAnalyzer:
    """Analyzer for Yearly Views of Top 5 YouTube Channels"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def create_visualization(self) -> VisualizationResult:
        """Create bar chart for average yearly views"""
        if 'Year' not in self.df.columns:
            return VisualizationResult()
        
        # Top 5 Channels by Total Views
        df_views = pd.melt(self.df, id_vars=['Year'], var_name='Channel', value_name='Views')
        df_views['Views'] = df_views['Views'] / 1000000
        df_views_sorted = df_views.sort_values(by=['Year', 'Views'], ascending=[True, False])

        # Create Plotly line chart
        fig = go.Figure()
        channels = df_views_sorted['Channel'].unique()
        max_views = df_views['Views'].max()
        y_range = [0, max_views * 1.1]

        for channel in channels:
            channel_data = df_views_sorted[df_views_sorted['Channel'] == channel]
            fig.add_trace(go.Scatter(
                x=channel_data['Year'],
                y=channel_data['Views'],
                mode='lines+markers',
                name=channel,
                line=dict(width=2),
            ))

        fig.update_layout(
            title={
                'text': '👀 Annual Views of Top 5 YouTube Channels',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
            },
            xaxis=dict(title='Year', tickangle=45),
            yaxis=dict(title='Annual Views (M)', range=y_range, showgrid=True),
            template='plotly_white',
            font=dict(family="Arial", size=12),
            plot_bgcolor='rgba(0,0,0,0)',
            width=1200,
            height=800
        )

        top_channels_per_year = df_views.loc[df_views_sorted.groupby('Year')['Views'].idxmax()]

        top_channels_text = []
        for index, row in top_channels_per_year.iterrows():
            top_channels_text.append(f"In {row['Year']}, the top channel was {row['Channel']} with {round(row['Views'],1)}M views.")

        # Join all the formatted strings and print
        top_channels_summary = ' \n'.join(top_channels_text)

        # Metrics and insights
        metrics = {
            'Top Viewed Channel in a Year': f"{str(df_views.loc[df_views['Views'].idxmax()]['Channel'])}, with {str(round(df_views.loc[df_views['Views'].idxmax()]['Views'], 1))}M views in {str(df_views.loc[df_views['Views'].idxmax()]['Year'])}.",
            'Top Total Viewed Channel': f"{str(df_views.loc[df_views['Views'].idxmax()]['Channel'])}, with {round(df_views.loc[df_views['Channel'] == df_views.loc[df_views['Views'].idxmax()]['Channel']]['Views'].sum(),1)}M total views.",
            'Highest Viewership Growth': f"{df_views.groupby('Channel')['Views'].agg(['first', 'last']).apply(lambda x: (x['last'] - x['first']) / x['first'] * 100, axis=1).idxmax()}, who grew {round(df_views.groupby('Channel')['Views'].agg(['first', 'last']).apply(lambda x: (x['last'] - x['first']) / x['first'] * 100, axis=1).max(),2)}% from {df_views['Year'].min()} to {df_views['Year'].max()}." 
        }
        insights = [
            f"{top_channels_summary}",
            "The coloured lines represent the channels and their average viewership per year.",
            "The chart uses clear annotations to make data interpretation easier."
        ]

        return VisualizationResult(figure=fig, metrics=metrics, insights=insights)