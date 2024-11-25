from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

class LinearRegressionModel:
    """Linear Regression Model for Predicting Subscribers from Likes"""

    def __init__(self, X, y, test_size=0.2, random_state=42):
        self.X = X.reshape(-1, 1)
        self.y = y
        self.test_size = test_size
        self.random_state = random_state
        self.model = LinearRegression()
        self.r2_score = None
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None

    def train(self):
        """Train the linear regression model"""
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=self.test_size, random_state=self.random_state
        )
        self.model.fit(self.X_train, self.y_train)

    def predict(self):
        """Predict using the linear regression model"""
        return self.model.predict(self.X_test)

    def evaluate(self):
        """Evaluate the model using R2 score"""
        y_pred = self.predict()
        self.r2_score = r2_score(self.y_test, y_pred)
        return self.r2_score
