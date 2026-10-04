---
name: "laya-remote-api"
description: "Comprehensive guide and operational reference for connecting to and querying the remote Laya System 1 Decision Engine API over Tailscale or local network."
version: "1.0.0"
author: "Laya Engine Team"
tags: ["laya", "api", "system-one", "decision-engine", "tailscale", "remote-inference", "curl", "python", "nodejs", "golang"]
---

# Laya Decision Engine — Remote API Integration Guide

This skill document defines the configuration, network endpoints, authentication, payload schemas, and client implementations for querying the remote **Laya System 1 Decision Engine** from external servers, microservices, and scripts.

---

## 1. Connection & Authentication Credentials

| Parameter | Configuration / Value | Description |
| :--- | :--- | :--- |
| **Public HTTPS URL (Tailscale Funnel)** | `https://momen-gpu.tail374b2b.ts.net:8020` | Accessible from any external server on the internet via SSL/TLS |
| **Private Tailnet URL** | `http://100.80.50.87:8020` | Direct encrypted access within the Tailscale mesh network |
| **Local Host** | `http://127.0.0.1:8020` | In-process / loopback host on the GPU machine |
| **Default API Key** | `example-api-key` | Permanent secret configured in `examples/server.py` and `laya.service` |
| **Auth Header Format** | `Authorization: Bearer <API_KEY>` | Primary authentication header |
| **Alternative Header** | `X-API-Key: <API_KEY>` | Supported alternative header |
| **Query Parameter** | `?api_key=<API_KEY>` | Useful for web browsers and quick testing |

> **Security Note:** All endpoints except `/health` enforce constant-time HMAC bearer authentication. Requests lacking valid credentials immediately return `HTTP 401 Unauthorized`.

---

## 2. Model Selection Guide (`model` field)

Laya provides three distinct fine-tuned checkpoints. Specify the `"model"` parameter in your request body to select the optimal neural checkpoint, or omit it for intelligent auto-routing:

| Model ID | Base Architecture | Context Window | Best Suited For | Typical Latency | Recommended Use |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`"typed-decisions"`** | ModernBERT-large (421M) | 1,024 tokens | **Coding tasks, bug triage, architectural decisions, DSA, concurrency data race analysis** | ~63 ms (GPU) | ⭐️ **Primary Choice for Technical / Agent Decisions** |
| **`"multilingual"`** | mmBERT-base (322M) | Up to 8,192 tokens | **Bengali and 100+ languages**, customer support triage, sentiment, ticket classification | ~55 ms (GPU) | 🌐 **Primary Choice for Bengali / Multilingual Triage** |
| **`"english"`** | ModernBERT-large (421M) | 512 tokens | Fast standard English text classification and routing | ~64 ms (GPU) | Standard English NLP |

### Why We Recommend `"model": "typed-decisions"` for Code & Engineering Tasks:
In empirical problem-solving benchmarks (covering DSA algorithmic optimization, Go concurrency data races, Python RCE AppSec, distributed Redis caching, and Linux file descriptor leaks), **`typed-decisions` achieved the highest score (68.6/100, 75% accuracy)**. It is specifically trained on typed decision heads (`choice`, `score`, `noul`) with strict logical reasoning. 

> [!TIP]
> **Best Practice:** When integrating with AI agents, IDE assistants, code review bots, or backend microservices, **always explicitly pass `"model": "typed-decisions"`** in the JSON request body.

### Default Auto-Routing Behavior (When `model` is omitted):
If the caller does not specify `"model"`:
- **Bengali / Non-Latin text:** Automatically routed to **`"multilingual"`** via character script heuristic.
- **English Latin text:** Automatically routed to **`"english"`**.
- **Indeterminate / Numbers / Code snippets without letters:** Routed to **`LAYA_DEFAULT_MODEL`** (configured as `"english"`).

### Understanding the Response Schema (`"model"` vs `"routing"`):
In the API response JSON:
- The top-level `"model": "laya-rl-agent"` is the **engine runtime identifier** (Laya RL Agent framework).
- The actual neural checkpoint that executed the inference is always recorded in **`routing.model`**:
```json
{
  "model": "laya-rl-agent",
  "answers": { ... },
  "routing": {
    "model": "typed-decisions",
    "repo": "convaiinnovations/laya/typed-decisions",
    "reason": "explicit model='typed-decisions'"
  }
}
```

---

## 3. Supported API Endpoints

### `POST /predict`
The primary decision endpoint. Evaluates typed questions (`choice`, `score`, `noul`) over any state document in a single forward pass.

### `POST /predict/batch`
Batch inference for multiple records in parallel (supports up to 64 records per batch).

### `POST /v1/systemone`
TypeSafe Jev wire protocol compatible endpoint (for `git-jev`, `hs-jev`, or Jev client SDKs).

### `GET /health`
Returns runtime status, loaded checkpoints, and hardware accelerator status (Public, no auth required).

### `GET /`
Visual interactive Web GUI (presents an unlock screen requiring the API Key, setting a persistent browser cookie).

---

## 4. Question Types Schema Reference

Laya executes decisions through three strongly-typed question primitives:

### 1. `choice`
Selects the winning option from a discrete set with calibrated probabilities.
```json
"department": {
  "type": "choice",
  "instructions": "Which department should handle this ticket?",
  "criteria": {
    "billing": "invoices, payment refunds, duplicate charges",
    "technical": "crashes, bugs, database failures, errors",
    "sales": "upgrades, new contracts"
  }
}
```

### 2. `score`
Evaluates an ordered or numerical assessment across calibrated thresholds.
```json
"urgency": {
  "type": "score",
  "instructions": "Assess the urgency and operational severity",
  "criteria": [
    "low (routine inquiry)",
    "medium (degraded service)",
    "critical (production outage, data loss)"
  ]
}
```

### 3. `noul`
Binary decision yielding an exact, calibrated probability (0.0 to 1.0) whether the statement is true.
```json
"is_outage": {
  "type": "noul",
  "instructions": "Is there an ongoing production outage or service interruption?"
}
```

---

## 5. Client Implementations (Ready to Copy-Paste)

### Python (using `requests` or `httpx`)

```python
import requests

API_URL = "https://momen-gpu.tail374b2b.ts.net:8020/predict"
API_KEY = "example-api-key"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "typed-decisions",
    "state": "Panic in goroutine: runtime error: nil pointer dereference at payment.go:142. Consul token expired.",
    "questions": {
        "root_cause": {
            "type": "choice",
            "instructions": "What caused this crash?",
            "criteria": {
                "token_expiry": "expired token in secrets/vault manager",
                "network_drop": "external connectivity loss",
                "disk_full": "filesystem full"
            }
        },
        "severity": {
            "type": "score",
            "instructions": "Rate incident severity",
            "criteria": ["low", "medium", "critical outage"]
        },
        "is_blocking": {
            "type": "noul",
            "instructions": "Are payment transactions currently failing?"
        }
    }
}

response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
data = response.json()

print("Selected Choice :", data["answers"]["root_cause"]["choice"])
print("Choice Conf     :", data["answers"]["root_cause"]["confidence"])
print("Calculated Score:", data["answers"]["severity"]["score"])
print("Binary Prob     :", data["answers"]["is_blocking"]["noul"])
```

---

### cURL / Bash

```bash
curl -X POST https://momen-gpu.tail374b2b.ts.net:8020/predict \
  -H "Authorization: Bearer example-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "multilingual",
    "state": "আমার অ্যাকাউন্টে পেমেন্ট ফেইল হয়েছে কিন্তু ব্যাংক থেকে টাকা কেটে নিয়েছে। দয়া করে রিফান্ড দিন।",
    "questions": {
      "department": {
        "type": "choice",
        "instructions": "কোন ডিপার্টমেন্ট এই সমস্যার সমাধান করবে?",
        "criteria": {
          "billing": "পেমেন্ট, ইনভয়েস, রিফান্ড",
          "technical": "সফটওয়্যার ক্র্যাশ, বাগ"
        }
      },
      "refund_needed": {
        "type": "noul",
        "instructions": "গ্রাহক কি টাকা ফেরত বা রিফান্ড চাচ্ছেন?"
      }
    }
  }'
```

---

### Node.js / TypeScript (Native `fetch`)

```typescript
const API_URL = "https://momen-gpu.tail374b2b.ts.net:8020/predict";
const API_KEY = "example-api-key";

async function queryLayaDecision(stateText: string) {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: "typed-decisions",
      state: stateText,
      questions: {
        classification: {
          type: "choice",
          instructions: "Classify incoming user message",
          criteria: {
            bug_report: "software defects and stack traces",
            feature_request: "proposals for new capabilities",
            billing: "account, payment, plans"
          }
        },
        risk_score: {
          type: "score",
          instructions: "Rate account churn risk",
          criteria: ["negligible", "moderate", "severe risk of leaving"]
        },
        urgent_flag: {
          type: "noul",
          instructions: "Does this require immediate human intervention?"
        }
      }
    })
  });

  if (!response.ok) {
    throw new Error(`Laya API error: ${response.status} ${await response.text()}`);
  }

  const result = await response.json();
  return result.answers;
}
```

---

### Go (`net/http`)

```go
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

const (
	apiURL = "https://momen-gpu.tail374b2b.ts.net:8020/predict"
	apiKey = "example-api-key"
)

func main() {
	payload := map[string]interface{}{
		"model": "typed-decisions",
		"state": "PostgreSQL database CPU at 98% during 20k req/sec peak read traffic.",
		"questions": map[string]interface{}{
			"architecture_fix": map[string]interface{}{
				"type":         "choice",
				"instructions": "Recommended remedy",
				"criteria": map[string]string{
					"redis_cache":   "deploy Redis cache-aside cluster",
					"reboot_server": "restart database blindly",
				},
			},
			"is_read_heavy": map[string]interface{}{
				"type":         "noul",
				"instructions": "Is the bottleneck read-heavy?",
			},
		},
	}

	bodyBytes, _ := json.Marshal(payload)
	req, _ := http.NewRequest("POST", apiURL, bytes.NewBuffer(bodyBytes))
	req.Header.Set("Authorization", "Bearer "+apiKey)
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	fmt.Printf("HTTP Status: %d\nResponse: %s\n", resp.StatusCode, string(body))
}
```

---

## 6. Server Infrastructure & Management

The server runs locally as a persistent, supervised systemd unit on the host machine.

### Service Commands:
```bash
# Check service status
sudo systemctl status laya.service

# View live stream logs
sudo journalctl -u laya.service -f

# Restart service
sudo systemctl restart laya.service

# Verify Tailscale Funnel status
tailscale funnel status
```

### Server Configuration File:
Unit file location: `/etc/systemd/system/laya.service`  
Source server code: `examples/server.py`

```ini
[Unit]
Description=Laya Decision Engine Service (Port 8020)
After=network.target tailscaled.service
Wants=tailscaled.service

[Service]
Type=simple
User=naimul
Group=naimul
WorkingDirectory=/home/naimul/laya
Environment="PATH=/home/naimul/miniconda3/bin:/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin"
Environment="LD_LIBRARY_PATH=/usr/local/cuda/lib64:"
Environment="PYTHONUNBUFFERED=1"
Environment="LAYA_HOST=127.0.0.1"
Environment="LAYA_PORT=8020"
Environment="LAYA_API_KEY=example-api-key"
Environment="LAYA_DEVICE=cuda"
Environment="LAYA_PRELOAD=1"
ExecStart=/home/naimul/miniconda3/bin/python /home/naimul/laya/examples/server.py --host 127.0.0.1 --port 8020
Restart=always
RestartSec=5s
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
```

---

## 7. Error Codes & Diagnostics

| Status Code | Meaning | Cause & Recommended Fix |
| :--- | :--- | :--- |
| **`401 Unauthorized`** | Missing or Invalid Token | Ensure header `Authorization: Bearer example-api-key` is set. |
| **`400 Bad Request`** | Malformed JSON | The request payload is not valid JSON or lacks the `questions` mapping. |
| **`413 Payload Too Large`** | Limit Exceeded | Request body exceeds 2MB, state exceeds 50,000 characters, or questions exceed 64 items. |
| **`422 Validation Error`** | Invalid Question Schema | `choice` or `score` questions submitted without required `criteria` block. |
| **`500 Internal Error`** | Model Failure | CUDA memory exhaustion or uncaught runtime exception; check `journalctl -u laya.service`. |
