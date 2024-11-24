import pandas as pd
import plotly.express as px
from src.visualization.base import VisualizationResult
from src.models.linear_regression_model import LinearRegressionModel
import plotly.graph_objects as go

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
    
    def create_prediction(self) -> VisualizationResult:
        """Create predictive model and analysis"""
        if 'Likes' not in self.df.columns or 'followers' not in self.df.columns:
            return VisualizationResult()

        df_clean = self.prepare_data()
        if df_clean.empty:
            return VisualizationResult()
        
        # Prepare data
        X = df_clean["Likes"].values.reshape(-1, 1)
        y = df_clean["followers"].values

        # Train and evaluate the model
        model = LinearRegressionModel(X, y)
        model.train()
        r2 = model.evaluate()
        y_pred = model.predict()
        intercept = model.model.intercept_
        slope = model.model.coef_[0]

        # Create Plotly figure
        fig = go.Figure()

        # Scatter plot of actual data
        fig.add_trace(go.Scatter(
            x=model.X_test.flatten(),
            y=model.y_test,
            mode='markers',
            name='Actual Data',
            marker=dict(color='blue', opacity=0.6, size=8),
        ))

        # Regression line
        fig.add_trace(go.Scatter(
            x=model.X_test.flatten(),
            y=y_pred,
            mode='lines',
            name='Regression Line',
            line=dict(color='red', width=2),
        ))

        fig.update_layout(
            title="Predictive Relationship between Likes and Subscribers",
            xaxis_title="Likes",
            yaxis_title="Subscribers",
            template="plotly_white",
            legend=dict(x=0.02, y=0.98),
            height=400,
            margin=dict(l=20, r=20, t=50, b=50),
        )

        # Add subtitle
        fig.add_annotation(
            xref="paper", yref="paper",
            x=0.5, y=1.15,
            showarrow=False,
            text=f"R² Score: {r2:.2f}, Intercept: {intercept:.2f}, Slope: {slope:.2f}",
            font=dict(size=12, color="black")
        )

        # Table of R2 scores for other models
        r2_results = pd.DataFrame({
            "Model": [
                "Linear Regression (Linear)", 
                "Linear Regression (Log Transformation)", 
                "Linear Regression (Square Root Transformation)", 
                "Linear Regression (Outlier Removal)", 
                "Polynomial Regression (degree 2)", 
                "Polynomial Regression (degree 3)", 
                "Random Forest", 
                "Gradient Boosting"
            ],
            "R² Score": [
                0.2326, 0.1515, 0.2168, 0.0749, 
                0.2346, 0.1740, 0.0709, 0.0096
            ]
        })

        # Insights
        insights = [
                f"The R² score of the original linear regression model is {r2:.4f}.",
                f"The intercept is {intercept:.2f}, which suggests that a channel with 0 likes is predicted to have approximately {intercept:,.0f} subscribers.",
                f"The slope is {slope:.2f}, indicating that for every additional like, the number of subscribers increases by {slope:.2f} (or roughly 1 subscriber per 50 likes).",
                "Other models were tested, as shown in the table below, with varying results.",
                "Polynomial Regression (degree 2) performed slightly better than Linear Regression, while advanced models like Random Forest and Gradient Boosting had lower R² scores.",
                "To improve the R² score, a multivariate regression model incorporating additional features (e.g., video views, uploads, engagement metrics) should be considered.",
        ]

        return VisualizationResult(
            figure=fig, 
            metrics={"R² Score": f"{r2:.4f}", "Intercept": f"{intercept:.2f}", "Slope": f"{slope:.2f}"}, 
            insights=insights, 
            extra_data=r2_results  # Include additional data for rendering
        )