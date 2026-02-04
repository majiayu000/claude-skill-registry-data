---
name: integration-helpers
description: Integration templates for FastAPI endpoints, Next.js UI components, and Supabase schemas for ML model deployment. Use when deploying ML models, creating inference APIs, building ML prediction UIs, designing ML database schemas, integrating trained models with applications, or when user mentions FastAPI ML endpoints, prediction forms, model serving, ML API deployment, inference integration, or production ML deployment.
allowed-tools: Bash, Read, Write, Edit, WebFetch
---

# integration-helpers

## Instructions

This skill provides production-ready integration templates for deploying machine learning models into full-stack applications. It covers FastAPI inference endpoints, Next.js prediction interfaces, and Supabase schemas for ML metadata storage.

### 1. FastAPI Inference Endpoints

Create production-ready ML inference APIs with proper error handling and validation:

```bash
# Generate FastAPI ML router
bash ./skills/integration-helpers/scripts/add-fastapi-endpoint.sh <model-type> <endpoint-name>

# Model types: classification, regression, text-generation, image-classification, embeddings
```

**What This Creates:**
- Pydantic models for request/response validation
- Inference endpoint with proper error handling
- Model loading and caching logic
- Health check endpoint
- Batch prediction support
- Async request handling

**Router Structure:**
```python
from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import BaseModel, Field
import numpy as np

router = APIRouter(
    prefix="/ml",
    tags=["machine-learning"],
    responses={500: {"description": "Model inference error"}},
)
```

**Example Usage:**
```bash
# Create text classification endpoint
bash ./skills/integration-helpers/scripts/add-fastapi-endpoint.sh classification sentiment-analysis

# Creates: app/routers/ml_sentiment_analysis.py
```

### 2. Request/Response Models

Define type-safe ML inference contracts:

**Classification Model:**
```python
class ClassificationRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)
    model_version: str | None = None
    return_probabilities: bool = False

class ClassificationResponse(BaseModel):
    prediction: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    probabilities: dict[str, float] | None = None
    model_version: str
    inference_time_ms: float
```

**Regression Model:**
```python
class RegressionRequest(BaseModel):
    features: list[float] = Field(..., min_items=1)
    feature_names: list[str] | None = None

class RegressionResponse(BaseModel):
    prediction: float
    feature_importance: dict[str, float] | None = None
    model_version: str
```

**Image Classification:**
```python
class ImageClassificationResponse(BaseModel):
    predictions: list[dict[str, Any]]
    top_prediction: str
    confidence: float
    processing_time_ms: float
```

### 3. Model Loading and Caching

Implement efficient model loading with caching:

```python
from functools import lru_cache
import joblib
import torch

# Singleton model loader
class ModelLoader:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load_model(self, model_path: str):
        if self._model is None:
            # Load based on framework
            if model_path.endswith('.pkl'):
                self._model = joblib.load(model_path)
            elif model_path.endswith('.pt'):
                self._model = torch.load(model_path)
            # Add TensorFlow, ONNX, etc.
        return self._model

# Dependency for endpoints
async def get_model():
    loader = ModelLoader()
    return loader.load_model("models/latest.pkl")
```

### 4. Inference Endpoints with Error Handling

Implement robust inference with proper error handling:

```python
@router.post("/predict", response_model=ClassificationResponse)
async def predict(
    request: ClassificationRequest,
    model = Depends(get_model)
):
    try:
        start_time = time.time()

        # Preprocess input
        processed_input = preprocess_text(request.text)

        # Run inference
        prediction = model.predict([processed_input])[0]
        probabilities = None

        if request.return_probabilities:
            probs = model.predict_proba([processed_input])[0]
            probabilities = {
                label: float(prob)
                for label, prob in zip(model.classes_, probs)
            }

        inference_time = (time.time() - start_time) * 1000

        return ClassificationResponse(
            prediction=str(prediction),
            confidence=float(max(probs)) if probabilities else 0.0,
            probabilities=probabilities,
            model_version=MODEL_VERSION,
            inference_time_ms=inference_time
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Model inference failed: {str(e)}"
        )
```

### 5. Batch Prediction Support

Enable efficient batch inference:

```python
class BatchClassificationRequest(BaseModel):
    texts: list[str] = Field(..., min_items=1, max_items=100)
    model_version: str | None = None

class BatchClassificationResponse(BaseModel):
    predictions: list[ClassificationResponse]
    total_inference_time_ms: float

@router.post("/predict/batch", response_model=BatchClassificationResponse)
async def predict_batch(
    request: BatchClassificationRequest,
    model = Depends(get_model)
):
    start_time = time.time()
    predictions = []

    # Process in batches for efficiency
    for text in request.texts:
        pred = await predict(
            ClassificationRequest(text=text),
            model=model
        )
        predictions.append(pred)

    total_time = (time.time() - start_time) * 1000

    return BatchClassificationResponse(
        predictions=predictions,
        total_inference_time_ms=total_time
    )
```

### 6. Next.js Prediction Forms

Create React components for ML model interaction:

```bash
# Generate Next.js prediction form
bash ./skills/integration-helpers/scripts/add-nextjs-component.sh <component-type> <component-name>

# Component types: classification-form, regression-form, image-upload, chat-interface
```

**What This Creates:**
- TypeScript React component with shadcn/ui
- Form validation with react-hook-form and zod
- Loading states and error handling
- Result visualization components
- API integration with fetch/axios

**Example Component:**
```typescript
// components/ml/sentiment-form.tsx
'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Card } from '@/components/ui/card'

const formSchema = z.object({
  text: z.string().min(1).max(10000),
})

export function SentimentForm() {
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
  })

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setLoading(true)
    try {
      const response = await fetch('/api/ml/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(values),
      })
      const data = await response.json()
      setResult(data)
    } catch (error) {
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card className="p-6">
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <Textarea {...form.register('text')} />
        <Button type="submit" disabled={loading}>
          {loading ? 'Analyzing...' : 'Analyze Sentiment'}
        </Button>
      </form>
      {result && <ResultDisplay result={result} />}
    </Card>
  )
}
```

### 7. Result Visualization Components

Display ML predictions with visual feedback:

```typescript
// Classification result with confidence
function ClassificationResult({ prediction, confidence, probabilities }) {
  return (
    <div className="space-y-4">
      <div className="text-2xl font-bold">{prediction}</div>
      <div className="text-muted-foreground">
        Confidence: {(confidence * 100).toFixed(1)}%
      </div>
      {probabilities && (
        <div className="space-y-2">
          {Object.entries(probabilities).map(([label, prob]) => (
            <div key={label} className="flex items-center gap-2">
              <span className="w-24">{label}</span>
              <div className="flex-1 bg-secondary rounded-full h-2">
                <div
                  className="bg-primary h-2 rounded-full"
                  style={{ width: `${prob * 100}%` }}
                />
              </div>
              <span className="w-12 text-right">{(prob * 100).toFixed(1)}%</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
```

### 8. Supabase ML Metadata Schemas

Create database schemas for ML model tracking and results:

```bash
# Generate Supabase schema for ML metadata
bash ./skills/integration-helpers/scripts/create-supabase-schema.sh <schema-type>

# Schema types: ml-models, predictions, training-runs, model-versions
```

**ML Models Table:**
```sql
create table ml_models (
  id uuid default gen_random_uuid() primary key,
  name text not null,
  model_type text not null, -- classification, regression, etc.
  framework text not null, -- scikit-learn, pytorch, tensorflow
  version text not null,
  artifact_url text, -- Cloud storage URL
  metrics jsonb, -- Accuracy, F1, RMSE, etc.
  hyperparameters jsonb,
  feature_names text[],
  target_classes text[],
  is_active boolean default true,
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  created_by uuid references auth.users(id)
);

create index idx_ml_models_active on ml_models(is_active, created_at desc);
create index idx_ml_models_type on ml_models(model_type);
```

**Predictions Log Table:**
```sql
create table predictions (
  id uuid default gen_random_uuid() primary key,
  model_id uuid references ml_models(id),
  model_version text not null,
  input_data jsonb not null,
  prediction jsonb not null,
  confidence float,
  inference_time_ms float,
  user_id uuid references auth.users(id),
  session_id text,
  created_at timestamptz default now()
);

create index idx_predictions_model on predictions(model_id, created_at desc);
create index idx_predictions_user on predictions(user_id, created_at desc);
create index idx_predictions_session on predictions(session_id);
```

**Training Runs Table:**
```sql
create table training_runs (
  id uuid default gen_random_uuid() primary key,
  model_id uuid references ml_models(id),
  dataset_name text not null,
  dataset_size integer,
  train_test_split jsonb, -- {train: 0.8, test: 0.2}
  hyperparameters jsonb,
  training_metrics jsonb, -- Loss curves, accuracy per epoch
  validation_metrics jsonb,
  test_metrics jsonb,
  training_duration_seconds integer,
  status text default 'running', -- running, completed, failed
  error_message text,
  artifact_url text,
  created_at timestamptz default now(),
  completed_at timestamptz,
  created_by uuid references auth.users(id)
);

create index idx_training_runs_model on training_runs(model_id, created_at desc);
create index idx_training_runs_status on training_runs(status);
```

**Model Versions Table:**
```sql
create table model_versions (
  id uuid default gen_random_uuid() primary key,
  model_id uuid references ml_models(id),
  version text not null,
  changelog text,
  metrics_comparison jsonb, -- Compare with previous version
  is_deployed boolean default false,
  deployment_url text,
  created_at timestamptz default now(),
  deployed_at timestamptz,
  created_by uuid references auth.users(id),
  unique(model_id, version)
);

create index idx_model_versions_deployed on model_versions(model_id, is_deployed);
```

### 9. API Route Handlers for Next.js

Create Next.js API routes that call FastAPI backend:

```typescript
// app/api/ml/predict/route.ts
import { NextRequest, NextResponse } from 'next/server'

const FASTAPI_URL = process.env.FASTAPI_URL || 'http://localhost:8000'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()

    const response = await fetch(`${FASTAPI_URL}/ml/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    })

    if (!response.ok) {
      const error = await response.json()
      return NextResponse.json(
        { error: error.detail },
        { status: response.status }
      )
    }

    const data = await response.json()
    return NextResponse.json(data)

  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to connect to ML service' },
      { status: 500 }
    )
  }
}
```

## Examples

### Example 1: Complete Sentiment Analysis Integration

```bash
# 1. Create FastAPI endpoint
cd /path/to/fastapi-backend
bash plugins/ml-training/skills/integration-helpers/scripts/add-fastapi-endpoint.sh classification sentiment-analysis

# 2. Create Next.js form component
cd /path/to/nextjs-frontend
bash plugins/ml-training/skills/integration-helpers/scripts/add-nextjs-component.sh classification-form sentiment-form

# 3. Create Supabase schema for logging
bash plugins/ml-training/skills/integration-helpers/scripts/create-supabase-schema.sh ml-models
bash plugins/ml-training/skills/integration-helpers/scripts/create-supabase-schema.sh predictions
```

**Result:** End-to-end sentiment analysis system with API, UI, and data logging

### Example 2: Image Classification Service

```bash
# 1. Create image classification endpoint
bash plugins/ml-training/skills/integration-helpers/scripts/add-fastapi-endpoint.sh image-classification image-classifier

# 2. Create image upload component
bash plugins/ml-training/skills/integration-helpers/scripts/add-nextjs-component.sh image-upload image-classifier-form

# 3. Setup model versioning schema
bash plugins/ml-training/skills/integration-helpers/scripts/create-supabase-schema.sh model-versions
```

**Result:** Complete image classification service with upload UI and version tracking

## Requirements

**FastAPI Dependencies:**
- FastAPI 0.100+
- Pydantic 2.0+
- scikit-learn, PyTorch, or TensorFlow (based on your model)
- python-multipart (for file uploads)
- joblib or pickle (for model serialization)

**Next.js Dependencies:**
- Next.js 14+
- React 18+
- shadcn/ui components
- react-hook-form
- zod
- TypeScript

**Supabase:**
- PostgreSQL 15+
- Row Level Security enabled
- UUID extension enabled

## Best Practices

**API Design:**
- Use proper HTTP status codes (200, 400, 500)
- Implement request validation with Pydantic
- Add rate limiting for production
- Log all predictions for monitoring
- Version your models in URLs or headers

**Performance:**
- Cache models in memory (singleton pattern)
- Use async endpoints for I/O operations
- Implement batch prediction for efficiency
- Consider model quantization for speed
- Use background tasks for heavy operations

**Security:**
- Validate all inputs strictly
- Implement authentication for API endpoints
- Use CORS properly in production
- Don't expose model internals in errors
- Rate limit inference endpoints

**Monitoring:**
- Log inference times
- Track prediction distributions
- Monitor error rates
- Store predictions for retraining
- Set up alerts for degraded performance

**Error Handling:**
- Return structured error responses
- Differentiate input errors from model errors
- Provide helpful error messages
- Log errors for debugging
- Implement graceful degradation

---

**Plugin:** ml-training
**Version:** 1.0.0
**Category:** ML Integration
**Skill Type:** Integration Templates
