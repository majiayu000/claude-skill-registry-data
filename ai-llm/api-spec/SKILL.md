---
name: api_spec
description: API SPEC
---

# API SPEC

This skill defines the autonomous behavior, system prompt, and capabilities for the agent **API SPEC**.

## Source Location
Originally discovered in Rick's Downloads at: `/Users/kalivibecoding/Downloads/_RECENT-PROJECTS/ai-systems/cloudflare-system-main/docs/API_SPEC.md`

## 🧠 Master Agent Prompt & Capabilities

# API Specification - RJ Business Solutions Cloudflare System

## 1. Business Factory Platform API
- **Base URL**: `https://factory.rickjeffersonsolutions.com`
- **Auth**: Bearer JWT (RS256)

### POST `/api/v1/business/onboard`
- **Purpose**: Initiate business onboarding.
- **Payload**:
  ```json
  { "name": "Company Name", "email": "owner@example.com" }
  ```

### GET `/api/v1/business/status`
- **Purpose**: Retrieve setup progress.

## 2. Docs Master Agent API
- **Base URL**: `https://api-docs.rickjeffersonsolutions.com`
- **Auth**: Bearer JWT (RS256)

### POST `/api/v1/query`
- **Purpose**: Ask the AI agent a technical question.
- **Payload**:
  ```json
  { "question": "How to deploy a Worker?" }
  ```

## 3. Funnel Builder Internal API
- **Note**: Predominantly uses Next.js Server Actions.
- **Standard**: All Server Actions must verify authorization before execution.

