import pandas as pd
import plotly.graph_objects as go
from src.visualization.base import VisualizationResult

class MostSubscribersAnalyzer:
    """Analyzer to identify and display the channel with the most subscribers"""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def create_visualization(self) -> VisualizationResult:
        """Find and visualize the channel with the most subscribers"""
        if 'ChannelName' not in self.df.columns or 'followers' not in self.df.columns:
            return VisualizationResult()

        # Find the top channel
        top_channel = self.df.nlargest(1, 'followers').iloc[0]
        channel_name = top_channel['ChannelName']
        follower_count = int(top_channel['followers'])

        # Create a figure for the top channel info
        fig = go.Figure()

        fig.add_annotation(
            text=f"<b>{channel_name}</b>",
            x=0.5,
            y=0.7,
            showarrow=False,
            font=dict(size=24, color="red"),
            xref="paper",
            yref="paper",
        )
        fig.add_annotation(
            text=f"<b>Subscribers: {follower_count:,}</b>",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=20, color="red"),
            xref="paper",
            yref="paper",
        )

        fig.update_layout(
            title="🌟 Channel with the Most Subscribers 🌟",
            title_font_size=20,
            title_font_color="green",
            height=400,
            paper_bgcolor="lightgray",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
        )

        # Add insights and metrics
        insights = [
            f"The channel with the most subscribers is **{channel_name}**, with **{follower_count:,}** subscribers.",
            "This visualization highlights the top-performing channel.",
                            ]
        metrics = {
            "Top Channel": channel_name,
            "Subscribers": follower_count,
        }

        return VisualizationResult(figure=fig, metrics=metrics, insights=insights)
