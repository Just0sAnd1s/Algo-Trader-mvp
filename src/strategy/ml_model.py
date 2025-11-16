import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os
from .indicators import rsi, macd

MODEL_PATH = 'models/rf_model.pkl'

class MLSignalModel:
    def __init__(self):
        self.model = None
        self.is_trained = False
        if os.path.exists(MODEL_PATH):
            try:
                self.model = joblib.load(MODEL_PATH)
                self.is_trained = True
            except:
                self.is_trained = False

    def prepare_features(self, df):
        df = df.copy().dropna()
        df['rsi'] = rsi(df['close'], 14)
        macd_line, signal_line, hist = macd(df['close'])
        df['macd'] = macd_line
        df['signal'] = signal_line
        df['ret1'] = df['close'].pct_change()
        df = df.dropna()
        X = df[['rsi','macd','signal','ret1']]
        y = (df['close'].shift(-1) > df['close']).astype(int).dropna()
        # align X and y
        X = X.iloc[:-1]
        return X, y

    def train(self, df):
        X, y = self.prepare_features(df)
        if len(X) < 50:
            return False
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        joblib.dump(model, MODEL_PATH)
        self.model = model
        self.is_trained = True
        return True

    def predict(self, df):
        if not self.is_trained:
            return 'HOLD'
        X, _ = self.prepare_features(df)
        if len(X) == 0:
            return 'HOLD'
        pred = self.model.predict(X.iloc[[-1]])[0]
        return 'BUY' if pred==1 else 'SELL'
