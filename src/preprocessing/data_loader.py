import pandas as pd
from typing import Tuple, Optional
import logging
from src.constants import TOP_100_YOUTUBERS_PATH, AVG_VIEW_EVERY_YEAR_PATH

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    """Handle data loading and basic preprocessing"""
    
    @staticmethod
    def load_data() -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
        """Load and preprocess YouTube data from CSV files"""
        try:
            df_top = pd.read_csv(TOP_100_YOUTUBERS_PATH)
            df_view = pd.read_csv(AVG_VIEW_EVERY_YEAR_PATH)
            
            # Basic preprocessing
            df_top = df_top.drop_duplicates()
            df_view = df_view.drop_duplicates()

            #manually re-categorize existing 'None' categories, remove empty columns
            df_top['Category'] = df_top['Category'].fillna('Entertainment')
            df_top = df_top.dropna(axis=1, how='all')


            
            logger.info("Data loaded successfully")
            return df_top, df_view
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return None, None