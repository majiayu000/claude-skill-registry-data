---
name: data-science
description: Skills for data science workflows — interactive exploration, Jupyter notebooks, data analysis, SQLite storage, and visualization.
version: 2.0.0
metadata:
  hermes:
    tags: [data]
    related_skills: [jupyter-live-kernel]
---

# Data Science

## Overview

Skills for data science workflows — interactive Python exploration via live Jupyter kernels, data analysis and aggregation with SQLite, and visualization with matplotlib.

## Sub-skills

- **jupyter-live-kernel**: Iterative Python via live Jupyter kernel (hamelnb)

## Labeled Sections

### SQLite Data Storage

For Hermes Agent's lightweight structured data storage using SQLite — news aggregates, trends, task state, user preferences — see `references/sqlite-data.md`. Covers table creation, queries, upsert patterns, FTS, and performance optimization.

## Usage

Load individual skills from this category using:
```
skill_view(name="data-science/{sub_skill}")
```
