---
name: freqai-integration
description: FreqAI self-adaptive ML retraining framework. Auto-retrains models on fresh data, prevents overfitting, adapts to regime changes. Built on FreqTrade.
---

# FreqAI Integration - Self-Adaptive ML

**Location:** `/Volumes/LegacySafe/SS_III/core/ml/freqai/`

**Impact:** Self-adaptive ML retraining (active development 2025)

**Sources:**
- [FreqTrade 2025.3 Docs](https://docs.freqtrade.io/en/2025.3/freqai/): Latest release v2025.11.1 (Dec 14, 2025)
- [GitHub robcaulk/freqai](https://github.com/robcaulk/freqai): Original implementation

## What It Does

FreqAI provides automated ML model retraining:

```
┌─────────────────────────────────────────────────────────────┐
│                    FREQAI PIPELINE                          │
│                                                             │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌─────────┐ │
│  │  Market  │──►│ Feature  │──►│   ML     │──►│ Signal  │ │
│  │   Data   │   │ Engineer │   │  Model   │   │ Output  │ │
│  └──────────┘   └──────────┘   └──────────┘   └─────────┘ │
│       │                             │                       │
│       │         ┌──────────┐        │                       │
│       └────────►│ Retrain  │◄───────┘                       │
│                 │ Scheduler│                                │
│                 │ (daily)  │                                │
│                 └──────────┘                                │
│                                                             │
│  Key Features:                                              │
│  - Auto-retrain on fresh data (daily/weekly)               │
│  - Feature importance tracking                              │
│  - Model drift detection                                    │
│  - Multiple model support (XGBoost, LightGBM, CatBoost)    │
└─────────────────────────────────────────────────────────────┘
```

## Why FreqAI

| Problem | FreqAI Solution |
|---------|-----------------|
| Models go stale | Auto-retrain on schedule |
| Overfitting to old data | Rolling training window |
| Feature drift | Feature importance monitoring |
| Regime changes | Regime-aware training |

## Core Implementation

```python
# core/ml/freqai/adaptive_model.py
from freqtrade.freqai.base_models.FreqaiMultiOutputClassifier import FreqaiMultiOutputClassifier
from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd
import numpy as np

class AdaptiveSignalModel(FreqaiMultiOutputClassifier):
    """Self-adaptive trading signal model."""

    def __init__(self, config: dict):
        super().__init__(config)
        self.model_type = config.get('model_type', 'xgboost')
        self.retrain_period = config.get('retrain_period', '1d')
        self.lookback_periods = config.get('lookback_periods', 1000)

    def fit(self, data_dictionary: dict, dk) -> None:
        """Train model on prepared features."""
        X = data_dictionary['train_features']
        y = data_dictionary['train_labels']

        # Select model type
        if self.model_type == 'xgboost':
            from xgboost import XGBClassifier
            self.model = XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                objective='multi:softmax'
            )
        elif self.model_type == 'lightgbm':
            from lightgbm import LGBMClassifier
            self.model = LGBMClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1
            )

        self.model.fit(X, y)

        # Store feature importances
        self.feature_importances = dict(zip(
            data_dictionary['train_features'].columns,
            self.model.feature_importances_
        ))

    def predict(self, data_dictionary: dict, dk) -> np.ndarray:
        """Generate predictions with confidence."""
        X = data_dictionary['prediction_features']

        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)

        return predictions, probabilities.max(axis=1)


class FeatureEngineer:
    """Feature engineering for FreqAI models."""

    @staticmethod
    def create_features(df: pd.DataFrame) -> pd.DataFrame:
        """Generate trading features from OHLCV data."""
        features = pd.DataFrame(index=df.index)

        # Price-based
        features['returns_1'] = df['close'].pct_change(1)
        features['returns_5'] = df['close'].pct_change(5)
        features['returns_20'] = df['close'].pct_change(20)

        # Volatility
        features['volatility_20'] = features['returns_1'].rolling(20).std()
        features['volatility_ratio'] = (
            features['returns_1'].rolling(5).std() /
            features['returns_1'].rolling(20).std()
        )

        # Trend
        features['sma_ratio'] = df['close'] / df['close'].rolling(20).mean()
        features['ema_ratio'] = df['close'] / df['close'].ewm(span=20).mean()

        # Volume
        features['volume_sma_ratio'] = df['volume'] / df['volume'].rolling(20).mean()

        # RSI
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        features['rsi'] = 100 - (100 / (1 + gain / loss))

        # MACD
        ema12 = df['close'].ewm(span=12).mean()
        ema26 = df['close'].ewm(span=26).mean()
        features['macd'] = ema12 - ema26
        features['macd_signal'] = features['macd'].ewm(span=9).mean()

        # Bollinger Band position
        sma20 = df['close'].rolling(20).mean()
        std20 = df['close'].rolling(20).std()
        features['bb_position'] = (df['close'] - sma20) / (2 * std20)

        return features.dropna()

    @staticmethod
    def create_labels(df: pd.DataFrame, horizon: int = 5) -> pd.Series:
        """Create target labels based on future returns."""
        future_return = df['close'].shift(-horizon) / df['close'] - 1

        labels = pd.Series(index=df.index, dtype=int)
        labels[future_return > 0.02] = 2   # Strong buy
        labels[future_return > 0.005] = 1  # Buy
        labels[future_return < -0.02] = -2 # Strong sell
        labels[future_return < -0.005] = -1 # Sell
        labels.fillna(0, inplace=True)     # Hold

        return labels


class RetrainScheduler:
    """Manages automatic model retraining."""

    def __init__(self, model: AdaptiveSignalModel, config: dict):
        self.model = model
        self.retrain_frequency = config.get('retrain_frequency', 'daily')
        self.last_retrain = None
        self.performance_threshold = config.get('performance_threshold', 0.55)

    async def check_and_retrain(self, new_data: pd.DataFrame) -> bool:
        """Check if retraining is needed and execute."""
        should_retrain = (
            self._time_based_trigger() or
            self._performance_based_trigger() or
            self._drift_based_trigger(new_data)
        )

        if should_retrain:
            await self._execute_retrain(new_data)
            return True

        return False

    def _time_based_trigger(self) -> bool:
        """Check if enough time has passed since last retrain."""
        if self.last_retrain is None:
            return True

        from datetime import datetime, timedelta
        thresholds = {
            'daily': timedelta(days=1),
            'weekly': timedelta(weeks=1),
            'monthly': timedelta(days=30)
        }
        return datetime.now() - self.last_retrain > thresholds[self.retrain_frequency]

    def _performance_based_trigger(self) -> bool:
        """Check if model performance has degraded."""
        recent_accuracy = self._calculate_recent_accuracy()
        return recent_accuracy < self.performance_threshold

    def _drift_based_trigger(self, new_data: pd.DataFrame) -> bool:
        """Detect feature distribution drift."""
        # Compare recent feature distributions to training distributions
        # Return True if significant drift detected
        pass

    async def _execute_retrain(self, data: pd.DataFrame):
        """Execute model retraining."""
        features = FeatureEngineer.create_features(data)
        labels = FeatureEngineer.create_labels(data)

        data_dict = {
            'train_features': features,
            'train_labels': labels
        }

        self.model.fit(data_dict, dk=None)
        self.last_retrain = datetime.now()
```

## Integration with ECO_SYSTEM_4

```python
# In ECO_SYSTEM_4/stages/signal_stage.py
from core.ml.freqai.adaptive_model import AdaptiveSignalModel, RetrainScheduler

class FreqAISignalGenerator:
    def __init__(self):
        self.model = AdaptiveSignalModel(config={
            'model_type': 'xgboost',
            'retrain_period': '1d',
            'lookback_periods': 1000
        })
        self.scheduler = RetrainScheduler(self.model, {
            'retrain_frequency': 'daily',
            'performance_threshold': 0.55
        })

    async def generate_signal(self, market_data: pd.DataFrame) -> dict:
        # Check if retrain needed
        await self.scheduler.check_and_retrain(market_data)

        # Generate prediction
        features = FeatureEngineer.create_features(market_data)
        prediction, confidence = self.model.predict({'prediction_features': features})

        return {
            'action': self._map_prediction(prediction[-1]),
            'confidence': float(confidence[-1]),
            'model_age_hours': self._get_model_age(),
            'feature_importances': self.model.feature_importances
        }
```

## Configuration

Add to BRAIN.json:
```json
{
  "freqai": {
    "enabled": true,
    "model_type": "xgboost",
    "retrain_frequency": "daily",
    "lookback_periods": 1000,
    "prediction_horizon": 5,
    "features": {
      "technical": ["rsi", "macd", "bb_position", "sma_ratio"],
      "volume": ["volume_sma_ratio"],
      "volatility": ["volatility_20", "volatility_ratio"],
      "returns": ["returns_1", "returns_5", "returns_20"]
    },
    "model_params": {
      "n_estimators": 100,
      "max_depth": 6,
      "learning_rate": 0.1
    },
    "performance_threshold": 0.55,
    "drift_threshold": 0.1
  }
}
```

## Required Dependencies

```bash
pip install freqtrade xgboost lightgbm catboost scikit-learn pandas numpy
```

## Testing

```bash
cd /Volumes/LegacySafe/SS_III/core/ml/freqai

python -c "
from adaptive_model import AdaptiveSignalModel, FeatureEngineer
import pandas as pd

# Load sample data
df = pd.read_csv('sample_btc_1h.csv')
features = FeatureEngineer.create_features(df)
labels = FeatureEngineer.create_labels(df)

model = AdaptiveSignalModel({'model_type': 'xgboost'})
model.fit({'train_features': features[:-100], 'train_labels': labels[:-100]}, None)

pred, conf = model.predict({'prediction_features': features[-100:]})
print(f'Predictions: {pred[-5:]}')
print(f'Confidences: {conf[-5:]}')
"
```

## Research Sources (Verified 2025)

| Source | Status | Date |
|--------|--------|------|
| [FreqTrade Docs](https://docs.freqtrade.io/en/2025.3/freqai/) | Active development | Dec 2025 |
| [PyPI freqtrade](https://pypi.org/project/freqtrade/) | v2025.11.1 | Dec 14, 2025 |

**Confidence:** HIGH for framework. Performance depends on strategy implementation.

**Note:** No published performance benchmarks. Results depend on your features/model choices.

## Status

- Implementation: NOT STARTED
- Priority: MEDIUM (requires data pipeline first)
- Dependencies: freqtrade, xgboost, data feeds
- Prerequisite: Need reliable OHLCV data pipeline
