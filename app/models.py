from sklearn.linear_model import LinearRegression
import numpy as np

# Dummy data
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])

# Train a simple linear regression model
model = LinearRegression()
model.fit(X, y)

def predict(value: float):
    return model.predict(np.array([[value]]))[0]
