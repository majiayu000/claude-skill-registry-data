---
name: etl
description: Extract Transform Load processes
license: MIT
compatibility: opencode
metadata:
  audience: data-engineers
  category: data-science
---

## What I do

- Design ETL pipelines for data integration
- Extract data from various sources
- Transform data for analytics
- Load data into data warehouses
- Handle data quality in pipelines
- Optimize pipeline performance

## When to use me

Use me when:
- Building data integration pipelines
- Moving data between systems
- Preparing data for analytics/ML
- Implementing data warehouse loading

## Key Concepts

### ETL Pipeline Architecture
```
┌─────────┐    ┌──────────┐    ┌─────────┐    ┌────────────┐
│ Source  │───▶│ Extract  │───▶│ Transform│───▶│    Load    │
│ Systems │    │  (Raw)   │    │ (Logic)  │    │ (Warehouse)│
└─────────┘    └──────────┘    └─────────┘    └────────────┘
     │                                           │
     │            Staging Area                   │
     └─────────────(Temp Storage)────────────────┘
```

### Python ETL Example
```python
import pandas as pd
from sqlalchemy import create_engine
import psycopg2

# Extract
def extract():
    users = pd.read_sql("SELECT * FROM users", db_conn)
    events = pd.read_json("s3://data/events.json")
    transactions = pd.read_csv("s3://data/transactions.csv")
    return users, events, transactions

# Transform
def transform(users, events, transactions):
    # Clean data
    users = users.dropna(subset=["email"])
    users["created_at"] = pd.to_datetime(users["created_at"])
    
    # Join and aggregate
    merged = events.merge(users, on="user_id")
    agg = merged.groupby("date").agg({
        "event_id": "count",
        "revenue": "sum"
    }).reset_index()
    
    return agg

# Load
def load(data):
    engine = create_engine("postgresql://warehouse")
    data.to_sql("daily_metrics", engine, 
                if_exists="append", index=False)

# Pipeline orchestration
users, events, transactions = extract()
data = transform(users, events, transactions)
load(data)
```

### ETL vs ELT
- **ETL**: Transform before load, structured targets
- **ELT**: Load raw, transform in warehouse, flexible
