---
name: scaffold-preprocessing
description: Scaffold data preprocessing pipeline — sliding window 30 timestep, MinMaxScaler fit trên train, train/val/test split theo battery ID chuẩn NASA, seed=42
argument-hint: [dataset-name]
allowed-tools: Write, Read, Bash
---

# Scaffold Preprocessing `$ARGUMENTS`

Usage: `/scaffold-preprocessing [dataset-name]`
Default: `nasa` nếu không truyền argument

---

## Bước 0 — Xác định dataset

Từ `$ARGUMENTS`:
- `nasa` / không có argument → **NASA Ames** (B0005–B0007 train, B0018 val/test)
- `calce` → CALCE — hỏi battery IDs trước khi tạo file
- Khác → hỏi user về battery IDs và split ratio

---

## Bước 1 — Tạo thư mục

```bash
mkdir -p data models/weights
touch data/__init__.py
```

---

## Bước 2 — Template: `data/preprocess.py`

```python
"""
Preprocessing pipeline cho NASA Battery Dataset.

Split chuẩn (CỐ ĐỊNH — không thay đổi nếu không có leader approval):
  Train : B0005, B0006, B0007
  Val   : B0018 — 70% đầu theo thứ tự timestep
  Test  : B0018 — 30% cuối theo thứ tự timestep
"""
import random
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

SEED        = 42
WINDOW_SIZE = 30
FEATURES    = ["voltage", "current", "temperature"]
SOH_NOMINAL = 2.0           # NASA nominal capacity (Ah)

TRAIN_IDS   = ["B0005", "B0006", "B0007"]
VAL_TEST_ID = "B0018"
VAL_RATIO   = 0.70

SCALER_PATH = Path("models/weights/scaler.pkl")
SCALER_VERSION = "1.0"

random.seed(SEED)
np.random.seed(SEED)


# ─────────────────────────── public API ────────────────────────────

def load_dataset(data_dir: str | Path) -> dict[str, pd.DataFrame]:
    """
    Đọc CSV từ data_dir → dict {battery_id: DataFrame}.
    Mỗi CSV phải có cột: cycle, voltage, current, temperature, capacity.
    """
    data_dir  = Path(data_dir)
    batteries: dict[str, pd.DataFrame] = {}
    for csv_file in sorted(data_dir.glob("*.csv")):
        bid = csv_file.stem
        df  = pd.read_csv(csv_file)
        _validate_columns(df, bid)
        df["soh"] = (df["capacity"] / SOH_NOMINAL * 100).clip(0, 100)
        batteries[bid] = df
    if not batteries:
        raise FileNotFoundError(f"Không tìm thấy CSV nào trong {data_dir}")
    return batteries


def build_windows(
    df: pd.DataFrame,
    window_size: int = WINDOW_SIZE,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Tạo sliding windows từ DataFrame.

    Returns:
        X: (N, window_size, 3) — [voltage, current, temperature]
        y: (N,)               — SOH% tại timestep cuối window
    """
    data   = df[FEATURES].values.astype(np.float32)
    labels = df["soh"].values.astype(np.float32)
    X, y   = [], []
    for i in range(len(data) - window_size):
        X.append(data[i : i + window_size])
        y.append(labels[i + window_size])
    return np.array(X), np.array(y)


def prepare_splits(
    batteries: dict[str, pd.DataFrame],
) -> tuple[
    np.ndarray, np.ndarray,   # X_train, y_train
    np.ndarray, np.ndarray,   # X_val,   y_val
    np.ndarray, np.ndarray,   # X_test,  y_test
]:
    """
    Tách train/val/test theo battery ID (NASA spec).
    Fit MinMaxScaler trên train set → lưu vào SCALER_PATH.
    """
    # ── train ──────────────────────────────────────────────────────
    X_trains, y_trains = [], []
    for bid in TRAIN_IDS:
        if bid not in batteries:
            raise KeyError(f"Battery {bid} không có trong dataset")
        X, y = build_windows(batteries[bid])
        X_trains.append(X)
        y_trains.append(y)
    X_train = np.concatenate(X_trains)
    y_train = np.concatenate(y_trains)

    # ── val / test (B0018) ─────────────────────────────────────────
    if VAL_TEST_ID not in batteries:
        raise KeyError(f"Battery {VAL_TEST_ID} không có trong dataset")
    df_vt     = batteries[VAL_TEST_ID]
    split_idx = int(len(df_vt) * VAL_RATIO)
    X_val,  y_val  = build_windows(df_vt.iloc[:split_idx])
    X_test, y_test = build_windows(df_vt.iloc[split_idx:])

    # ── fit scaler trên train — KHÔNG fit trên val/test ─────────────
    scaler  = MinMaxScaler(feature_range=(0, 1))
    n, w, f = X_train.shape
    scaler.fit(X_train.reshape(-1, f))

    X_train = _apply_scaler(X_train, scaler)
    X_val   = _apply_scaler(X_val,   scaler)
    X_test  = _apply_scaler(X_test,  scaler)

    _save_scaler(scaler)
    return X_train, y_train, X_val, y_val, X_test, y_test


def load_scaler() -> MinMaxScaler:
    """Load scaler đã lưu. Dùng trong inference — KHÔNG fit lại."""
    assert SCALER_PATH.exists(), (
        f"Scaler không tìm thấy tại '{SCALER_PATH}'. "
        "Chạy prepare_splits() để tạo scaler trước."
    )
    artifact = joblib.load(SCALER_PATH)
    assert artifact["version"] == SCALER_VERSION, (
        f"Scaler version mismatch: expected {SCALER_VERSION}, "
        f"got {artifact['version']}"
    )
    return artifact["scaler"]


# ────────────────────────── helpers ────────────────────────────────

def _apply_scaler(X: np.ndarray, scaler: MinMaxScaler) -> np.ndarray:
    n, w, f = X.shape
    return scaler.transform(X.reshape(-1, f)).reshape(n, w, f).astype(np.float32)


def _save_scaler(scaler: MinMaxScaler) -> None:
    SCALER_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({
        "scaler":     scaler,
        "version":    SCALER_VERSION,
        "trained_on": TRAIN_IDS,
        "features":   FEATURES,
    }, SCALER_PATH)
    print(f"Scaler saved → {SCALER_PATH}")


def _validate_columns(df: pd.DataFrame, battery_id: str) -> None:
    required = set(FEATURES) | {"capacity"}
    missing  = required - set(df.columns)
    if missing:
        raise ValueError(f"[{battery_id}] Thiếu cột: {missing}")
```

---

## Checklist sau scaffold

- [ ] `SEED = 42` đặt đầu file, `random.seed` + `np.random.seed` được gọi?
- [ ] `TRAIN_IDS = ["B0005", "B0006", "B0007"]` và `VAL_TEST_ID = "B0018"`?
- [ ] Scaler chỉ `.fit()` trên `X_train` — không fit trên val/test?
- [ ] Scaler được lưu tại `models/weights/scaler.pkl` kèm `version`, `trained_on`, `features`?
- [ ] `load_scaler()` có version assertion?
- [ ] `build_windows()` tạo shape `(N, 30, 3)` đúng không?

---

## Không được
- Fit scaler trên val/test set — data leakage trực tiếp
- Shuffle toàn bộ data rồi mới split — phải split theo battery ID trước
- Thay đổi `TRAIN_IDS` / `VAL_TEST_ID` không có leader approval
- Dùng random seed khác 42
