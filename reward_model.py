import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import joblib
import warnings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REWARD_LOG = os.path.join(BASE_DIR, '..', 'logs', 'rewards.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'reward_model.pkl')
PLOT_PATH = os.path.join(BASE_DIR, '..', 'logs', 'reward_trend.png')

def load_reward_data():
    df = pd.read_csv(REWARD_LOG)
    df['version_num'] = df['version'].str.extract(r'v(\d+)').astype(int)
    return df[['version_num', 'rating']]

def train_reward_model(X, y):
    model = LinearRegression()
    model.fit(X, y)
    return model

def predict_next_reward(model, next_version_num):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return model.predict(pd.DataFrame([[next_version_num]], columns=['version_num']))[0]

def plot_reward_trend(X, y, model):
    plt.figure(figsize=(8, 4))
    plt.scatter(X, y, color='blue', label='Actual Ratings')
    plt.plot(X, model.predict(X), color='green', label='Regression Line')
    plt.xlabel('Version Number')
    plt.ylabel('Rating')
    plt.title('Reward Trend Across Versions')
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOT_PATH)
    print(f' Saved plot to: {PLOT_PATH}')
    plt.close()


if __name__ == "__main__":
    if not os.path.exists(REWARD_LOG):
        print("⚠️ No rewards.csv file found.")
        exit(1)

    data = load_reward_data()
    X = data[['version_num']]
    y = data['rating']

    model = train_reward_model(X, y)
    joblib.dump(model, MODEL_PATH)
    print(f" Model trained and saved to: {MODEL_PATH}")

    next_version_num = data['version_num'].max() + 1
    predicted_rating = predict_next_reward(model, next_version_num)
    print(f" Predicted rating for next version (v{next_version_num}): {predicted_rating:.2f}")
    
    new_entry = pd.DataFrame({
        'version': [f'v{next_version_num}'],
        'rating': [round(predicted_rating, 2)]
    })
    new_entry.to_csv(REWARD_LOG, mode='a', header=False, index=False)
    print(f" Logged predicted rating to rewards.csv")

    plot_reward_trend(X, y, model)
