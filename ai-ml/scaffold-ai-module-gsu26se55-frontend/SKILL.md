---
name: scaffold-ai-module
description: Bootstrap toàn bộ AI module từ đầu — tạo folder structure, requirements.txt, pytest.ini, .gitignore, rồi chạy lần lượt scaffold-model × 2, scaffold-preprocessing, scaffold-training × 2, scaffold-fastapi-endpoint, scaffold-unit-tests. Dùng khi module chưa có gì.
argument-hint: []
allowed-tools: Write, Read, Bash
---

# Scaffold AI Module (Bootstrap)

Usage: `/scaffold-ai-module`

Chạy lệnh này **một lần duy nhất** khi khởi tạo repo AI module từ đầu.
Sau lệnh này: module đã có đủ cấu trúc, templates, và tests — sẵn sàng để implement.

---

## Bước 0 — Xác nhận repo trống

```bash
ls -la
git status
```

Nếu repo đã có source code → **DỪNG**, hỏi user có muốn tiếp tục không.
Skill này thiết kế để chạy trên module chưa có gì.

---

## Bước 1 — Tạo folder structure

```bash
mkdir -p \
  api/routers \
  api/schemas \
  data \
  models/weights \
  train \
  tests \
  data/raw

touch \
  api/__init__.py \
  api/routers/__init__.py \
  api/schemas/__init__.py \
  data/__init__.py \
  models/__init__.py \
  train/__init__.py \
  tests/__init__.py
```

Kết quả:
```
ai-module/
├── api/
│   ├── __init__.py
│   ├── main.py              ← tạo ở Bước 4
│   ├── routers/
│   │   └── predict.py       ← tạo ở Bước 4
│   └── schemas/
│       └── predict.py       ← tạo ở Bước 4
├── data/
│   ├── __init__.py
│   ├── raw/                 ← dataset CSV đặt ở đây (không commit)
│   └── preprocess.py        ← tạo ở Bước 5
├── models/
│   ├── __init__.py
│   ├── soh_predictor.py     ← tạo ở Bước 3
│   ├── anomaly_detector.py  ← tạo ở Bước 3
│   └── weights/             ← artifacts commit vào Git (< 50MB)
├── train/
│   ├── __init__.py
│   ├── train_soh.py         ← tạo ở Bước 6
│   └── train_anomaly.py     ← tạo ở Bước 6
├── tests/
│   ├── __init__.py
│   ├── conftest.py          ← tạo ở Bước 7
│   ├── test_preprocess.py
│   ├── test_model.py
│   ├── test_inference.py
│   └── test_api.py
├── requirements.txt         ← tạo ở Bước 2
├── pytest.ini               ← tạo ở Bước 2
└── .gitignore               ← cập nhật ở Bước 2
```

---

## Bước 2 — Tạo config files

### `requirements.txt`

```
torch==2.3.0
scikit-learn==1.4.2
fastapi==0.111.0
uvicorn[standard]==0.30.1
pydantic==2.7.1
numpy==1.26.4
pandas==2.2.2
joblib==1.4.2
httpx==0.27.0
pytest==8.2.0
pytest-cov==5.0.0
```

> Pin toàn bộ version — reproducibility. Khi cần update: đổi version + retest.

### `pytest.ini`

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --tb=short
```

### `.gitignore` — thêm vào cuối file (tạo mới nếu chưa có)

```gitignore
# Python
__pycache__/
*.py[cod]
.venv/
*.egg-info/
.pytest_cache/
.coverage
htmlcov/

# Dataset — không commit raw data
data/raw/

# Model artifacts lớn — chỉ commit nếu < 50MB
# models/weights/*.pth
# models/weights/*.pkl
# Nếu > 50MB: dùng Git LFS (xem rules/tech/ai.md)

# Môi trường
.env
```

---

## Bước 3 — Scaffold models

Chạy `/scaffold-model SOHPredictor` → tạo `models/soh_predictor.py`

Chạy `/scaffold-model AnomalyDetector` → tạo `models/anomaly_detector.py`

> Xem chi tiết templates tại `.claude/skills/dev/ai/scaffold-model/SKILL.md`

---

## Bước 4 — Scaffold FastAPI endpoint

Chạy `/scaffold-fastapi-endpoint predict` → tạo:
- `api/main.py`
- `api/routers/predict.py`
- `api/schemas/predict.py`

Sau khi tạo xong, **bắt buộc cập nhật** `api/schemas/predict.py` để enforce 30 timestep:

```python
from pydantic import BaseModel, Field, field_validator
from typing import Literal

WINDOW_SIZE = 30

class PredictRequest(BaseModel):
    voltage:     list[float] = Field(..., min_length=WINDOW_SIZE,
                                     description=f"Đúng {WINDOW_SIZE} voltage readings (V)")
    current:     list[float] = Field(..., min_length=WINDOW_SIZE,
                                     description=f"Đúng {WINDOW_SIZE} current readings (A)")
    temperature: list[float] = Field(..., min_length=WINDOW_SIZE,
                                     description=f"Đúng {WINDOW_SIZE} temperature readings (°C)")

    @field_validator("voltage", "current", "temperature")
    @classmethod
    def check_length(cls, v: list[float], info) -> list[float]:
        if len(v) < WINDOW_SIZE:
            raise ValueError(f"{info.field_name} cần ít nhất {WINDOW_SIZE} giá trị, nhận {len(v)}")
        return v[-WINDOW_SIZE:]   # lấy 30 timestep cuối nếu gửi nhiều hơn


class PredictResponse(BaseModel):
    status:      Literal["Normal", "Degrading", "Failed"]
    soh_percent: float = Field(..., ge=0.0, le=100.0)
    confidence:  float = Field(..., ge=0.0, le=1.0)
```

Cập nhật `api/main.py` để load đủ 3 artifacts khi startup:

```python
import os, random
import numpy as np
import torch
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import predict as predict_router
from data.preprocess import load_scaler
from models.soh_predictor   import SOHPredictor
from models.anomaly_detector import AnomalyDetector

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

MODEL_VERSION    = "1.0"
LSTM_PATH        = f"models/weights/soh_lstm_v{MODEL_VERSION}.pth"
ISO_FOREST_PATH  = f"models/weights/isolation_forest_v{MODEL_VERSION}.pkl"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── kiểm tra file tồn tại trước khi load ──────────────────────
    for path, label in [
        (LSTM_PATH,       "LSTM model"),
        (ISO_FOREST_PATH, "Isolation Forest"),
        ("models/weights/scaler.pkl", "MinMaxScaler"),
    ]:
        assert os.path.exists(path), (
            f"[STARTUP] {label} không tìm thấy tại '{path}'. "
            "Chạy training scripts trước khi start server."
        )

    app.state.scaler     = load_scaler()
    app.state.lstm_model = SOHPredictor.load(LSTM_PATH, expected_version=MODEL_VERSION)
    app.state.iso_model  = AnomalyDetector.load(ISO_FOREST_PATH, expected_version=MODEL_VERSION)
    yield


app = FastAPI(title="AI Module — GSU26SE55", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_router.router)


@app.get("/health")
def health():
    return {
        "status":                   "ok",
        "model_version":            MODEL_VERSION,
        "scaler_loaded":            hasattr(app.state, "scaler"),
        "lstm_loaded":              hasattr(app.state, "lstm_model"),
        "isolation_forest_loaded":  hasattr(app.state, "iso_model"),
    }
```

Cập nhật `api/routers/predict.py` để dùng đúng state:

```python
from fastapi import APIRouter, HTTPException, Request
from api.schemas.predict import PredictRequest, PredictResponse
import numpy as np
import torch

router = APIRouter(prefix="", tags=["predict"])


@router.post("/predict", response_model=PredictResponse)
async def predict(body: PredictRequest, request: Request) -> PredictResponse:
    scaler     = request.app.state.scaler
    lstm_model = request.app.state.lstm_model
    iso_model  = request.app.state.iso_model

    try:
        # ── preprocess ─────────────────────────────────────────────
        window = np.array([body.voltage, body.current, body.temperature],
                          dtype=np.float32).T             # (30, 3)
        window_scaled = scaler.transform(window)          # (30, 3)
        x = torch.tensor(window_scaled).unsqueeze(0)      # (1, 30, 3)

        # ── SOH prediction ─────────────────────────────────────────
        with torch.no_grad():
            soh = float(lstm_model(x).item())
        soh = max(0.0, min(100.0, soh))

        # ── anomaly detection ──────────────────────────────────────
        x_flat    = window_scaled.reshape(1, -1)           # (1, 90)
        score     = float(iso_model.score(x_flat)[0])
        status    = iso_model.classify(score, soh)

        # ── confidence: normalize score về [0, 1] ──────────────────
        confidence = float(np.clip((score + 0.5) / 0.5, 0.0, 1.0))

        return PredictResponse(
            status=status,
            soh_percent=round(soh, 2),
            confidence=round(confidence, 4),
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Prediction failed")
```

---

## Bước 5 — Scaffold preprocessing

Chạy `/scaffold-preprocessing nasa` → tạo `data/preprocess.py`

> Xem chi tiết tại `.claude/skills/dev/ai/scaffold-preprocessing/SKILL.md`

---

## Bước 6 — Scaffold training scripts

Chạy `/scaffold-training SOHPredictor`   → tạo `train/train_soh.py`

Chạy `/scaffold-training AnomalyDetector` → tạo `train/train_anomaly.py`

> Xem chi tiết tại `.claude/skills/dev/ai/scaffold-training/SKILL.md`

---

## Bước 7 — Scaffold unit tests

Chạy `/scaffold-unit-tests all` → tạo `tests/conftest.py` + 4 test files

> Xem chi tiết tại `.claude/skills/dev/ai/scaffold-unit-tests/SKILL.md`

---

## Bước 8 — Verify cấu trúc

```bash
find . -name "*.py" | grep -v __pycache__ | sort
cat requirements.txt
```

Expected output (tối thiểu):
```
./api/__init__.py
./api/main.py
./api/routers/__init__.py
./api/routers/predict.py
./api/schemas/__init__.py
./api/schemas/predict.py
./data/__init__.py
./data/preprocess.py
./models/__init__.py
./models/anomaly_detector.py
./models/soh_predictor.py
./train/__init__.py
./train/train_anomaly.py
./train/train_soh.py
./tests/__init__.py
./tests/conftest.py
./tests/test_api.py
./tests/test_inference.py
./tests/test_model.py
./tests/test_preprocess.py
```

---

## Bước 9 — Cài dependencies và kiểm tra import

```bash
pip install -r requirements.txt

# Kiểm tra import không bị lỗi syntax
python -c "from models.soh_predictor import SOHPredictor; print('SOHPredictor OK')"
python -c "from models.anomaly_detector import AnomalyDetector; print('AnomalyDetector OK')"
python -c "from data.preprocess import build_windows; print('preprocess OK')"
python -c "from api.main import app; print('FastAPI app OK')"
```

Nếu import lỗi → sửa trước khi tiếp tục.

---

## Bước 10 — Chạy tests (trừ test_api vì chưa có artifacts)

```bash
pytest tests/test_preprocess.py tests/test_model.py -v
# Expected: tất cả PASS (không cần artifacts)

# test_inference.py và test_api.py cần artifacts → skip tự động
pytest tests/ -v --cov=api --cov=data --cov=models --cov=train --cov-report=term-missing
```

---

## Checklist cuối

- [ ] Tất cả thư mục và `__init__.py` đã tạo?
- [ ] `requirements.txt` pin version đầy đủ?
- [ ] `models/soh_predictor.py` và `models/anomaly_detector.py` đã tạo?
- [ ] `data/preprocess.py` có `SEED=42`, `TRAIN_IDS`, `load_scaler()`?
- [ ] `api/main.py` load 3 artifacts khi startup, có `/health` endpoint?
- [ ] `api/schemas/predict.py` enforce `min_length=30`?
- [ ] `train/train_soh.py` có early stopping và in MAE/RMSE?
- [ ] `tests/conftest.py` có `autouse=True` seed fixture?
- [ ] `python -c "from api.main import app"` không lỗi syntax?
- [ ] `data/raw/` trong `.gitignore`?

---

## Workflow tiếp theo sau scaffold-ai-module

```
1. Đặt NASA dataset CSV vào data/raw/
2. python -m train.train_soh      ← tạo scaler.pkl + soh_lstm_v1.0.pth
3. python -m train.train_anomaly  ← tạo isolation_forest_v1.0.pkl
4. pytest tests/ -v               ← tất cả test phải PASS kể cả test_api
5. uvicorn api.main:app --reload   ← test thủ công
6. /kltn-reviewcode               ← review trước khi ship
```
