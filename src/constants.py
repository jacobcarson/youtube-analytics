from src.visualization.components import (
    CategoryDistributionAnalyzer, 
    LikesSubscribersAnalyzer, 
    YoutubersByCountryDist, 
    QuarterlyIncomeAnalyzer,
    FollowersByCategoryAnalyzer
)

TOP_100_YOUTUBERS_PATH = './data/top_100_youtubers.csv'
AVG_VIEW_EVERY_YEAR_PATH = './data/avg_view_every_year.csv'

ANALYZERS_CONFIG = {
    "Category Distribution": {
        "analyzer_class": CategoryDistributionAnalyzer,
        "title": "Category Distribution of YouTube Channels",
    },
    "Likes vs Subscribers": {
        "analyzer_class": LikesSubscribersAnalyzer,
        "title": "Likes vs Subscribers Analysis",
        "prediction": True
    },
    "Global Distribution": {
        "analyzer_class": YoutubersByCountryDist,
        "title": "Global Distribution of Top YouTubers",
    },
    "Income Analysis": {
        "analyzer_class": QuarterlyIncomeAnalyzer,
        "title": "Average Quarterly Income of Top 5 YouTube Channels",
    },
    "Followers by Category": {
        "analyzer_class": FollowersByCategoryAnalyzer,
        "title": "Followers by Category",
    },
}
