from src.visualization.components import (
    CategoryDistributionAnalyzer, 
    LikesSubscribersAnalyzer, 
    YoutubersByCountryDist, 
    QuarterlyIncomeAnalyzer,
    FollowersByCategoryAnalyzer,
    YearlyViewAnalyzer,
    MostSubscribersAnalyzer,
)

TOP_100_YOUTUBERS_PATH = './data/top_100_youtubers.csv'
AVG_VIEW_EVERY_YEAR_PATH = './data/avg_view_every_year.csv'

ANALYZERS_CONFIG = {
    "Category Distribution": { # Chart 1
        "analyzer_class": CategoryDistributionAnalyzer,
        "title": "Category Distribution of YouTube Channels",
    },
    "Likes vs Subscribers": { # Chart 2
        "analyzer_class": LikesSubscribersAnalyzer,
        "title": "Likes vs Subscribers Analysis",
        "prediction": True
    },
    "Global Distribution": { # Chart 3
        "analyzer_class": YoutubersByCountryDist,
        "title": "Global Distribution of Top YouTubers",
    },
    "Annual Views for Top Channels": { # Chart 4
        "analyzer_class": YearlyViewAnalyzer,
        "title": "Annual Views for Top Channels"
    },
    "Income Analysis": { # Chart 5
        "analyzer_class": QuarterlyIncomeAnalyzer,
        "title": "Average Quarterly Income of Top 5 YouTube Channels",
    },
    "Followers by Category": { # Chart 7
        "analyzer_class": FollowersByCategoryAnalyzer,
        "title": "Followers by Category",
    },
    "Most Subscribers Analysis": { # Chart 8
        "analyzer_class": MostSubscribersAnalyzer,
        "title": "Top Channel Analysis"
    }
}
