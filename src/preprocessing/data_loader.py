import pandas as pd
from typing import Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    """Handle data loading and basic preprocessing"""
    
    @staticmethod
    def load_data() -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
        """Load and preprocess YouTube data from CSV files"""
        try:
            df_top = pd.read_csv('./data/top_100_youtubers.csv')
            df_view = pd.read_csv('./data/avg_view_every_year.csv')
            
            # Basic preprocessing
            df_top = df_top.drop_duplicates()
            df_view = df_view.drop_duplicates()
            
            logger.info("Data loaded successfully")
            return df_top, df_view
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return None, None