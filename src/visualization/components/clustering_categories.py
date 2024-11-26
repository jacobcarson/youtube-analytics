import pandas as pd
import numpy as np
import plotly.express as px
import umap
from umap import UMAP
import hdbscan
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from src.visualization.base import VisualizationResult
from scipy.stats import entropy

class ClusteringDistributionAnalyzer:
    """Analyzer for Category Distribution"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def create_visualization(self) -> VisualizationResult:

        #create lists of the different feature types
        numerical_features = self.df.select_dtypes(include=['number']).columns.tolist()
        categorical_features = self.df.select_dtypes(include=['object', 'category']).columns.tolist()

        """Perform clustering on the dataset using UMAP and HDBSCAN."""
        if not (numerical_features or categorical_features):
            return VisualizationResult(insights=["No features selected for clustering."])


        #scale and encode the Data
        preprocess_steps = []
        if numerical_features:
            preprocess_steps.append(('num', StandardScaler(), numerical_features))
        elif categorical_features:
            preprocess_steps.append(('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features))
        
        #create the column transformer, ignore any other column
        preprocessor = ColumnTransformer(preprocess_steps, remainder='drop')
        
        #perform the transformations
        processed_data = preprocessor.fit_transform(self.df)

        #UMAP Dimensionality Reduction
        umap_params = {'n_neighbors': 10, 'min_dist': 0.1, 'n_components': 3, 'random_state': 42}
        umap_model = UMAP(**umap_params)
        umap_embeddings = umap_model.fit_transform(processed_data)

        #HDBSCAN Clustering
        hdbscan_params = {'min_cluster_size': 2}
        hdbscan_model = hdbscan.HDBSCAN(**hdbscan_params)
        cluster_labels = hdbscan_model.fit_predict(umap_embeddings)

        #Add cluster labels to the DataFrame
        self.df['Cluster'] = cluster_labels

        #Calculate cluster centers
        cluster_centers = self.df.groupby('Cluster')[numerical_features].mean()

        # Generate concise cluster names focusing on the top 3 most important numerical trends and the top categorical trend
        cluster_names = {}
        for cluster_idx in cluster_centers.index:
            # Start with the cluster label
            cluster_name = f"Cluster {cluster_idx} - "

            # Normalize the data (StandardScaler)
            scaler = StandardScaler()
            normalized_data = scaler.fit_transform(self.df[numerical_features])

            # Create a DataFrame for normalized features
            normalized_df = pd.DataFrame(normalized_data, columns=numerical_features)

            # Calculate the variance of the normalized features
            feature_importance = {}
            for feature in numerical_features:
                # Get the normalized values for the current feature in the cluster
                feature_values = normalized_df.loc[self.df['Cluster'] == cluster_idx, feature]
                
                # Calculate the variance of the normalized feature
                feature_variance = feature_values.var()
                feature_importance[feature] = feature_variance

            # Sort features by variance
            sorted_features = sorted(feature_importance.items(), key=lambda item: item[1], reverse=True)

            # Focus on the top 3 most important features
            num_desc = []
            for feature, _ in sorted_features[:3]:
                # Get the feature's values for the current cluster
                feature_values = self.df[self.df['Cluster'] == cluster_idx][feature]

                # Calculate quartiles (Q1, Q3)
                Q1 = feature_values.quantile(0.25)
                Q3 = feature_values.quantile(0.75)

                # Classify based on the quartiles
                if feature_values.mean() > Q3:  # High
                    num_desc.append(f"High {feature}")
                elif feature_values.mean() < Q1:  # Low
                    num_desc.append(f"Low {feature}")
                else:
                    num_desc.append(f"Moderate {feature}")

            if num_desc:
                cluster_name += " & ".join(num_desc)

            # Evaluate the most important categorical feature based on mode and entropy
            cat_feature_importance = {}
            for cat_feature in categorical_features:
                # Get the categorical values for the current feature in the cluster
                cat_values = self.df[self.df['Cluster'] == cluster_idx][cat_feature]
                
                # Calculate the mode (most frequent value) and its frequency
                mode_category = cat_values.mode()
                mode_frequency = cat_values.value_counts().iloc[0] if not mode_category.empty else 0
                
                # Calculate the entropy of the categorical feature values (higher entropy = more uniform distribution)
                value_counts = cat_values.value_counts(normalize=True)
                cat_entropy = entropy(value_counts)

                # Assign importance based on mode frequency (dominance) and entropy
                # A higher mode_frequency and lower entropy indicates higher importance
                cat_feature_importance[cat_feature] = (mode_frequency, -cat_entropy)

            # Sort categorical features by a combination of mode dominance and entropy
            sorted_cat_features = sorted(cat_feature_importance.items(), key=lambda item: item[1], reverse=True)
            
            # Take the most important categorical feature
            if sorted_cat_features:
                top_cat_feature = sorted_cat_features[0][0]
                mode_category = self.df[self.df['Cluster'] == cluster_idx][top_cat_feature].mode()
                if not mode_category.empty:
                    cluster_name += f" - {top_cat_feature}: {mode_category[0]}"

            # Store the concise name in the cluster_names dictionary
            cluster_names[cluster_idx] = cluster_name

        # Map cluster names to DataFrame
        self.df['Cluster_Name'] = self.df['Cluster'].map(cluster_names)

        # Visualization
        if umap_params.get('n_components', 2) == 2:
            fig = px.scatter(
                self.df,
                x=umap_embeddings[:, 0],
                y=umap_embeddings[:, 1],
                color=self.df['Cluster_Name'].astype(str),
                hover_data=self.df[numerical_features + categorical_features],
                title="2D UMAP Clusters",
                labels={'color': 'Cluster Name'}
            )
        else:
            fig = px.scatter_3d(
                self.df,
                x=umap_embeddings[:, 0],
                y=umap_embeddings[:, 1],
                z=umap_embeddings[:, 2],
                color=self.df['Cluster_Name'].astype(str),
                hover_data=self.df[numerical_features + categorical_features],
                title="3D UMAP Clusters",
                labels={'color': 'Cluster Name'},
                height=800,
                width=1200
            )
        
        fig.update_layout(
        title={
                'text': '✨ Category Clustering of Top Youtube Channels',
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
            'Number of Clusters': len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0),
            'Number of Outliers': sum(cluster_labels == -1),
        }

        insights = [
            f"Number of clusters identified: {metrics['Number of Clusters']}",
            f"Number of outliers detected: {metrics['Number of Outliers']}",
        ]
        
        return VisualizationResult(figure=fig, metrics=metrics, insights=insights)
