---
name: 08-appkit-feedback
description: >
  Add user feedback (thumbs up/down) to an AppKit chat application, linked to
  MLflow assessments via the Databricks Assessments REST API. Covers the Vote
  table, feedback API routes (with AppKit-native auth via
  `getExecutionContext().client.config.authenticate()`), MLflow trace integration,
  and feedback UI components. Use when asked to add feedback, thumbs up/down,
  ratings, or link user judgments to MLflow traces. Triggers on "feedback",
  "thumbs up", "thumbs down", "rate response", "MLflow assessment", "user rating",
  "vote on message".
license: Apache-2.0
compatibility: Requires 07-appkit-chat-history complete (Vote table + traceId column), Node.js v22+, Databricks CLI >= 0.295.0
allowed-tools: Bash(databricks:*) Bash(npm:*) Bash(curl:*) Bash(node:*) Read
clients: [ide_cli, genie_code]
bundle_resource: apps
deploy_verb: apps_deploy
deploy_note: >
  Feedback wiring is source editing (feedback routes, MLflow REST calls via
  `config.authenticate()`, UI buttons) — client-agnostic. There is **no own DDL**: the `Vote` table is created
  by `07-appkit-chat-history` Step 1 (server-side startup, SP-owned, RULE_10), and the feedback `INSERT`/`UPSERT`
  is runtime data, not schema. MLflow assessments POST/PATCH over OAuth from the SP execution context — same on
  both clients. IDE: `databricks experiments create --profile $PROFILE`, local `npm`/`curl` checks, then deploy
  per `03-appkit-deploy`. Genie Code: `experiments create` via `runDatabricksCli` (omit `--profile`); local `npm`
  gates are an IDE convenience (server-side build on deploy); exercise feedback routes on the deployed app
  (browser / OAuth-session), not localhost. Verify assessments in the MLflow experiment UI.
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "1.1.0"
  domain: apps
  role: feedback
  standalone: false
  last_verified: "2026-06-02"
  volatility: medium
  upstream_sources:
    - name: "databricks-agent-skills/databricks-apps"
      repo: "databricks/databricks-agent-skills"
      paths:
        - "skills/databricks-apps/SKILL.md"
      relationship: "extended"
      last_synced: "2026-04-27"
      sync_commit: "manifest-v2-2026-04-22"
---

# Add User Feedback to an AppKit Chat Application

Add thumbs up/down feedback on assistant responses, persisted in Lakebase and linked
to MLflow traces via the Assessments REST API — all AppKit-native. Authentication
uses `getExecutionContext().client.config.authenticate()` (the same pattern as
[06-appkit-serving-wiring/references/custom-proxy-fallback.md](../06-appkit-serving-wiring/references/custom-proxy-fallback.md)),
so there's no dependency on `process.env.DATABRICKS_TOKEN` or manual header parsing.

> **Companion Python skill:** the canonical end-user feedback contract — what
> `mlflow.log_feedback(...)` expects, trace-id vs `client_request_id`,
> streaming, ratings, update/delete, and the negative-feedback → eval-dataset
> loop — lives in
> [`genai-agents/sdlc/04c-end-user-feedback`](../../../genai-agents/sdlc/04c-end-user-feedback/SKILL.md).
> This AppKit skill is the **frontend / Node sidecar** wire-up; 04c is the
> **Python / agent-side** contract. Naming, source format, and trace-id flow
> here intentionally match 04c so dashboards aggregate cleanly.

## When to Use

- Adding user feedback to an existing AppKit chat interface built from
  [07-appkit-chat-history](../07-appkit-chat-history/SKILL.md)
- Connecting feedback to MLflow experiment traces for model evaluation
- Building a feedback loop for agent quality monitoring

**Prerequisites:**
- Chat streaming + persistence from [07-appkit-chat-history](../07-appkit-chat-history/SKILL.md)
  (the `Vote` table, the `traceId` column on `chat.Message`, and the `messageMetaStore`
  ephemeral fallback are all produced there)
- An MLflow experiment configured (optional — feedback still works without it, it just
  doesn't log to MLflow)
- MLflow tracing enabled on the deployed agent endpoint (see Gotchas at end)

### Working in Genie Code (client routing)

This skill is **source editing + server-side code** (feedback routes, MLflow assessment calls, UI). There is **no own DDL** — the `Vote` table comes from `07-appkit-chat-history` (server-side startup, SP-owned). The MLflow REST calls authenticate from the SP execution context, so they run identically on both clients. Only the CLI/local checks differ:

| IDE/CLI (as written) | Genie Code substitution |
|----------------------|--------------------------|
| `databricks experiments create --name … --profile <PROFILE>` (Step 1) | run via `runDatabricksCli` (**omit `--profile`** — Genie Code injects the workspace + OAuth) |
| `npm run build` gates | **IDE-only** convenience — no local Node toolchain; the platform builds **server-side** on deploy. Errors surface in `databricks apps logs <name>` |
| local `curl http://localhost:8000/api/feedback …` tests (Step 4) | no local dev server — POST/GET the feedback routes on the **deployed** app via browser or the OAuth-session `requests.Session()` test in `03-appkit-deploy` |
| `rg -n '(DATABRICKS_TOKEN\|…)' server/` (Step 4) | runs on both — Grep/`rg` over the cloned repo, no client difference |
| `app.yaml` / `databricks.yml` `MLFLOW_EXPERIMENT_ID` edits (Step 1) | source edits — identical on both clients |
| `databricks apps deploy …` | see the `03-appkit-deploy` deploy-routing contract (`runDatabricksCli`, else SDK `w.apps.deploy(... SNAPSHOT)`) |

Paths are relative to `apps_lakebase/$APP_NAME` — inside your git-cloned workshop project (`artifact_root`) on Genie Code, never the read-only `.assistant/skills` copy and never `/tmp`. See `skills/genie-code-environment` for the full manifest.

---

## Header Contract (Canonical)

The feedback handler reads `req.session.userId` (set by [07-appkit-chat-history](../07-appkit-chat-history/SKILL.md) Step 2 from the canonical Databricks Apps user headers) and submits it as `AssessmentSource.source_id`.

Databricks Apps canonical user headers (inbound to AppKit):

- `x-forwarded-email`
- `x-forwarded-preferred-username`
- `x-forwarded-user`
- `x-forwarded-access-token`

`x-forwarded-user-info` is **not** a canonical Databricks Apps header and must not be used.

When this AppKit instance is the frontend half of a 2-Apps deployment (Pathway-C / Variant 4) and the agent runs in a separate Databricks App, the AppKit proxy must additionally set `x-app-user-email` on the outbound request to the Agent App so the agent can attribute its MLflow `log_feedback` calls to the originating user. The app-to-app `Authorization: Bearer` token represents the AppKit App service principal hop and **must not** be treated as the user identity. See [06d-appkit-agent-app-proxy](../06d-appkit-agent-app-proxy/SKILL.md) for the proxy-side contract.

---

## Architecture

```
User clicks 👍/👎
  │
  ├──► POST /api/feedback { chatId, messageId, isUpvoted }
  │     │
  │     ├──► UPSERT to Lakebase chat.Vote table (always)
  │     │
  │     ├──► Look up traceId from chat.Message (DB) or messageMetaStore (in-memory)
  │     │
  │     └──► POST/PATCH Databricks MLflow Assessments REST API (if traceId available)
  │           /api/3.0/mlflow/traces/{traceId}/assessments
  │           Auth: AppKit getExecutionContext().client.config.authenticate()
  │           Logs: assessment_name="user_feedback", source={ HUMAN, userId }, feedback={ value }
  │
  └──► UI updates thumbs button state
```

---

## Step 1: Configure MLflow Experiment

### Environment Variables

Add to `.env` for local development:

```env
MLFLOW_EXPERIMENT_ID=your-experiment-id
```

Add to `app.yaml` for deployed apps:

```yaml
env:
  - name: MLFLOW_EXPERIMENT_ID
    value: ${var.mlflow_experiment_id}
```

Add to `databricks.yml`:

```yaml
variables:
  mlflow_experiment_id:
    description: "MLflow experiment ID for feedback tracking"
```

### Creating an MLflow Experiment

The feedback experiment MUST be pinned to the same user-and-use-case identity that backs `APP_NAME` so concurrent workshop attendees on a shared workspace never collide on a single experiment, and the MLflow UI never lists a generic `Default` / `Tracing` / `my-app-feedback` entry.

**Naming rule (REQUIRED):** `/Users/<user_email>/mlflow/<APP_NAME>-feedback` — e.g. `/Users/jane.doe@example.com/mlflow/jane-d-stayfinder-feedback`. The leaf carries the same `${FIRSTNAME}-${LASTINITIAL}-${use_case_slug}` shape that derives `APP_NAME` (see `apps_lakebase/Instructions.md`). When running on top of `vibecoding-state`, this value is already pinned at `state://Resources.mlflow_feedback_experiment_path` by [`vibecoding-state.migrate_canonical`](../../../skills/vibecoding-state/SKILL.md#operation-migrate_canonical) — read it from state instead of inventing a new path.

If you don't have an experiment yet, create one:

```bash
# Replace <user_email> and <APP_NAME> with your actual values
# (or pull mlflow_feedback_experiment_path directly from .vibecoding-state.md).
databricks experiments create \
  --name "/Users/<user_email>/mlflow/<APP_NAME>-feedback" \
  --profile <PROFILE>
```

> **Client note — Genie Code:** run this through `runDatabricksCli` and **omit `--profile`** (the workspace + OAuth are injected). Capture the `experiment_id` from the JSON output the same way.

Note the `experiment_id` from the output and set it in your environment.

### Enabling MLflow Tracing on the Agent Endpoint

This is **not** an AppKit concern — it happens at agent deployment time. Without it,
the endpoint won't return `trace_id` in its streaming chunks and feedback will report
`mlflowStatus: "no_trace_id"`.

For Databricks Agent Framework deployments:

```python
import databricks.agents

databricks.agents.deploy(
    model_name="catalog.schema.agent_model",
    model_version=1,
    enable_trace=True,   # emits trace_id in databricks_output
)
```

If you're using a Mosaic AI Agent Evaluation endpoint, tracing is enabled by default.

For more on the trace ID shape returned in each streaming chunk, see
[references/trace-extraction.md](references/trace-extraction.md).

---

## Step 2: Add Feedback API Routes (AppKit-Native Auth)

This is the only file that touches the MLflow REST API directly. The trick is to
use AppKit's execution context for OAuth — no `process.env.DATABRICKS_TOKEN`
fallback, no manual `x-forwarded-access-token` parsing.

```typescript
import { getExecutionContext, AppKit } from "@databricks/appkit";

// Reuse or import the messageMetaStore created in 07-appkit-chat-history (Step 4b).
// If you stored it on globalThis as __appkitMessageMetaStore:
const messageMetaStore =
  (globalThis as { __appkitMessageMetaStore?: Map<string, { chatId: string; traceId: string | null }> })
    .__appkitMessageMetaStore ?? new Map();

// Dedup: one assessment per (messageId, userId) — subsequent clicks PATCH
const assessmentStore = new Map<string, string>(); // "messageId:userId" -> assessmentId

// Cached AppKit-authenticated MLflow request helper.
// Uses the app's Service Principal token by default. See the "User vs SP Auth"
// note at the end of this step if you need user OBO for MLflow calls.
async function mlflowRequest(
  path: string,
  init: { method: "POST" | "PATCH" | "GET"; body?: unknown },
): Promise<Response> {
  const ctx = getExecutionContext();
  const config = ctx.client.config;
  await config.ensureResolved();

  const host = (config.host ?? "").replace(/\/$/, "");
  if (!host) throw new Error("Databricks host not resolved from execution context");

  const headers = new Headers();
  await config.authenticate(headers);
  headers.set("Content-Type", "application/json");
  headers.set("Accept", "application/json");

  return fetch(`${host}${path}`, {
    method: init.method,
    headers,
    body: init.body ? JSON.stringify(init.body) : undefined,
  });
}

AppKit.server.extend((app) => {
  // POST /api/feedback — submit or update feedback
  app.post("/api/feedback", async (req, res) => {
    const { chatId, messageId, isUpvoted } = req.body;
    const forwardedEmail = req.headers["x-forwarded-email"];
    const userId =
      typeof forwardedEmail === "string" && forwardedEmail.length > 0
        ? forwardedEmail
        : req.session!.userId;

    if (!chatId || !messageId || typeof isUpvoted !== "boolean") {
      return res
        .status(400)
        .json({ error: "chatId, messageId, and isUpvoted (boolean) required" });
    }

    // 1. Persist vote in Lakebase
    try {
      await AppKit.lakebase.query(
        `INSERT INTO chat."Vote" ("chatId", "messageId", "isUpvoted")
         VALUES ($1, $2, $3)
         ON CONFLICT ("chatId", "messageId")
         DO UPDATE SET "isUpvoted" = $3`,
        [chatId, messageId, isUpvoted],
      );
    } catch (err) {
      console.error("[Feedback] Failed to save vote:", err);
      return res.status(500).json({ error: "Failed to save feedback" });
    }

    // 2. Resolve traceId (DB first, fall back to in-memory meta store)
    let traceId: string | null = null;
    try {
      const result = await AppKit.lakebase.query(
        `SELECT "traceId" FROM chat."Message" WHERE id = $1`,
        [messageId],
      );
      traceId = result.rows[0]?.traceId ?? null;
    } catch (err) {
      console.warn("[Feedback] DB lookup failed, checking meta store:", err);
    }
    if (!traceId) {
      const meta = messageMetaStore.get(messageId);
      if (meta?.traceId) traceId = meta.traceId;
    }

    // 3. Log to MLflow Assessments API (if trace ID + experiment available)
    let mlflowStatus: string = "skipped";
    let mlflowError: string | undefined;
    const experimentId = process.env.MLFLOW_EXPERIMENT_ID;

    if (traceId && experimentId) {
      try {
        const dedupeKey = `${messageId}:${userId}`;
        const existingAssessmentId = assessmentStore.get(dedupeKey);

        if (existingAssessmentId) {
          // Update existing assessment via PATCH
          const mlflowResponse = await mlflowRequest(
            `/api/3.0/mlflow/traces/${traceId}/assessments/${existingAssessmentId}`,
            {
              method: "PATCH",
              body: { feedback: { value: isUpvoted } },
            },
          );

          if (mlflowResponse.ok) {
            mlflowStatus = "updated";
          } else {
            const errBody = await mlflowResponse.text();
            console.warn(
              "[Feedback] MLflow PATCH error:",
              mlflowResponse.status,
              errBody,
            );
            mlflowStatus = "mlflow_error";
            mlflowError = `${mlflowResponse.status}: ${errBody.slice(0, 200)}`;
          }
        } else {
          // Create new assessment via POST
          const mlflowResponse = await mlflowRequest(
            `/api/3.0/mlflow/traces/${traceId}/assessments`,
            {
              method: "POST",
              body: {
                assessment_name: "user_feedback",
                source: { source_type: "HUMAN", source_id: userId },
                feedback: { value: isUpvoted },
              },
            },
          );

          if (mlflowResponse.ok) {
            const body = await mlflowResponse.json();
            const assessmentId = body?.assessment?.assessment_id;
            if (assessmentId) assessmentStore.set(dedupeKey, assessmentId);
            mlflowStatus = "logged";
          } else {
            const errBody = await mlflowResponse.text();
            console.warn(
              "[Feedback] MLflow POST error:",
              mlflowResponse.status,
              errBody,
            );
            mlflowStatus = "mlflow_error";
            mlflowError = `${mlflowResponse.status}: ${errBody.slice(0, 200)}`;
          }
        }
      } catch (err) {
        console.warn("[Feedback] MLflow API call failed:", err);
        mlflowStatus = "mlflow_error";
        mlflowError = String(err);
      }
    } else if (!traceId) {
      mlflowStatus = "no_trace_id";
    } else if (!experimentId) {
      mlflowStatus = "no_experiment_id";
    }

    res.json({
      success: true,
      mlflowStatus,
      ...(mlflowError && { mlflowError }),
      isUpvoted,
    });
  });

  // GET /api/feedback/:chatId — get all votes for a conversation
  app.get("/api/feedback/:chatId", async (req, res) => {
    try {
      const result = await AppKit.lakebase.query(
        `SELECT "messageId", "isUpvoted" FROM chat."Vote" WHERE "chatId" = $1`,
        [req.params.chatId],
      );
      const votes: Record<string, boolean> = {};
      for (const row of result.rows) {
        votes[row.messageId] = row.isUpvoted;
      }
      res.json({ votes });
    } catch (err) {
      console.warn("[Feedback] Failed to load votes:", err);
      res.json({ votes: {} });
    }
  });
});
```

See [references/mlflow-assessments.md](references/mlflow-assessments.md) for the
full REST API reference and AppKit auth rationale.
See [references/trace-extraction.md](references/trace-extraction.md) for
trace ID extraction patterns (already wired into
[07-appkit-chat-history](../07-appkit-chat-history/SKILL.md) Step 4a).

For 2-Apps Pathway-C, `source_id` must be the originating user's email. The app-to-app bearer identifies the AppKit SP, so do not derive MLflow `AssessmentSource.source_id` from that bearer.

### User vs. Service Principal Auth for MLflow

The `mlflowRequest` helper above uses `getExecutionContext()` **without** `.asUser(req)`,
which means the app's Service Principal creates the MLflow assessments. This is usually
what you want: the SP needs `CAN_EDIT` on the MLflow experiment, and you don't have
to grant every end user that permission. The `source.source_id: userId` in the POST
body records which user submitted the feedback.

If you need the request to go out as the actual user (e.g., you want the MLflow audit
log to attribute the call to the user), construct the fetch inside the route handler
using the request-scoped context instead:

```typescript
// User-scoped (requires each user to have CAN_EDIT on the experiment)
// Placeholder — AppKit's typed API for user-scoped custom fetch varies by SDK version.
// Prefer the SP pattern above for most cases.
```

**Gate:** `POST /api/feedback` returns `{ success: true, mlflowStatus: "logged" | "no_trace_id" | "no_experiment_id" }`. The `Vote` row is visible via `GET /api/feedback/:chatId`.

### Populating the Message Meta Store

Step 4b of [07-appkit-chat-history](../07-appkit-chat-history/SKILL.md) already writes
to `messageMetaStore` after every successful stream:

```typescript
// In /api/chat, after accumulating and persisting the assistant message
messageMetaStore.set(assistantMsgId, { chatId, traceId });
```

This is what makes feedback survive ephemeral mode: when Lakebase is down, the DB lookup
returns no rows, but `messageMetaStore.get(messageId)` still has the `traceId` from the
just-ended stream, so the MLflow assessment still logs.

---

## Step 3: Build Feedback UI Components

### FeedbackButtons Component

Create `client/src/components/FeedbackButtons.tsx`:

```tsx
import { useState } from "react";

interface FeedbackButtonsProps {
  chatId: string;
  messageId: string;
  initialVote?: boolean | null;
}

export function FeedbackButtons({ chatId, messageId, initialVote }: FeedbackButtonsProps) {
  const [vote, setVote] = useState<boolean | null>(initialVote ?? null);
  const [submitting, setSubmitting] = useState(false);

  const submitFeedback = async (isUpvoted: boolean) => {
    if (submitting) return;

    const newVote = vote === isUpvoted ? null : isUpvoted;
    setVote(newVote);

    if (newVote === null) return;

    setSubmitting(true);
    try {
      await fetch("/api/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chatId, messageId, isUpvoted: newVote }),
      });
    } catch (err) {
      console.error("Failed to submit feedback:", err);
      setVote(vote);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="flex items-center gap-1 mt-1">
      <button
        onClick={() => submitFeedback(true)}
        disabled={submitting}
        className={`rounded p-1 text-xs transition-colors ${
          vote === true
            ? "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400"
            : "text-muted-foreground hover:text-foreground hover:bg-muted"
        }`}
        title="Helpful"
      >
        👍
      </button>
      <button
        onClick={() => submitFeedback(false)}
        disabled={submitting}
        className={`rounded p-1 text-xs transition-colors ${
          vote === false
            ? "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400"
            : "text-muted-foreground hover:text-foreground hover:bg-muted"
        }`}
        title="Not helpful"
      >
        👎
      </button>
    </div>
  );
}
```

### Integrate into MessageBubble

Update the `MessageBubble` component from
[06-appkit-serving-wiring/references/chat-ui-patterns.md](../06-appkit-serving-wiring/references/chat-ui-patterns.md):

```tsx
import { FeedbackButtons } from "./FeedbackButtons";

function MessageBubble({
  message,
  chatId,
  votes,
}: {
  message: { id?: string; role: "user" | "assistant"; content: string };
  chatId: string;
  votes: Record<string, boolean>;
}) {
  return (
    <div className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[80%] rounded-lg px-4 py-3 ${
          message.role === "user"
            ? "bg-primary text-primary-foreground"
            : "bg-muted text-foreground"
        }`}
      >
        <p className="whitespace-pre-wrap text-sm">{message.content}</p>
        {message.role === "assistant" && chatId && message.id && (
          <FeedbackButtons
            chatId={chatId}
            messageId={message.id}
            initialVote={votes[message.id] ?? null}
          />
        )}
      </div>
    </div>
  );
}
```

Feedback buttons only render when the assistant message has an `id` — which is set from
the `meta` SSE event emitted in
[07-appkit-chat-history Step 4b](../07-appkit-chat-history/SKILL.md#step-4-stream--persist-assistant-message-appkit-native).

### Load Existing Votes on Chat Open

```tsx
const [votes, setVotes] = useState<Record<string, boolean>>({});

useEffect(() => {
  if (!chatId) return;
  fetch(`/api/feedback/${chatId}`)
    .then((res) => res.json())
    .then((data) => setVotes(data.votes ?? {}))
    .catch(() => {});
}, [chatId]);
```

---

## Step 4: Test the Feedback Flow

### Manual API Test

```bash
# Submit feedback
curl -s http://localhost:8000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{"chatId":"<UUID>","messageId":"<UUID>","isUpvoted":true}' | jq .

# Expected response:
# { "success": true, "mlflowStatus": "logged", "isUpvoted": true }

# Get votes for a chat
curl -s http://localhost:8000/api/feedback/<chatId> | jq .
```

### Verify MLflow Integration

If `MLFLOW_EXPERIMENT_ID` is set and the endpoint returned `traceId`:

1. Open the MLflow experiment in the Databricks workspace
2. Find the trace by ID
3. Verify the `user_feedback` assessment appears under the trace

If `mlflowStatus` is `"no_trace_id"`, the serving endpoint isn't emitting trace info.
See [references/trace-extraction.md](references/trace-extraction.md) and confirm the
endpoint was deployed with tracing enabled (Step 1).

### Verify Auth Is AppKit-Native

```bash
rg -n '(DATABRICKS_TOKEN|x-forwarded-access-token|createDatabricks|ai-sdk-provider)' server/
```

Should return **zero** matches inside the feedback code. The only Authorization header
set anywhere is via `config.authenticate(headers)`.

---

## Validation Gate

All must pass before declaring the feedback feature complete:

- [ ] `POST /api/feedback` saves to `chat."Vote"` table
- [ ] `GET /api/feedback/:chatId` returns the vote map
- [ ] Thumbs up/down buttons render on assistant messages (only when `message.id` is set)
- [ ] Clicking a button updates the UI state immediately
- [ ] Vote persists across page reloads
- [ ] MLflow assessment logged when `traceId` and `MLFLOW_EXPERIMENT_ID` are available (`mlflowStatus: "logged"`)
- [ ] PATCH path works: clicking the same button a second time updates the existing assessment (`mlflowStatus: "updated"`)
- [ ] Graceful degradation when MLflow experiment is not configured (`mlflowStatus: "no_experiment_id"`, vote still saved)
- [ ] Graceful degradation when agent endpoint lacks tracing (`mlflowStatus: "no_trace_id"`, vote still saved)
- [ ] Zero imports of `ai` or `@databricks/ai-sdk-provider` in `server/`
- [ ] Zero references to `process.env.DATABRICKS_TOKEN` in the feedback handler (auth goes through `config.authenticate`)

---

## Gotchas

| Gotcha | Fix | Step |
|--------|-----|------|
| `mlflowStatus: "no_trace_id"` for every message | Agent endpoint was deployed without tracing. Redeploy with `databricks.agents.deploy(..., enable_trace=True)` | 1 |
| `mlflowStatus: "mlflow_error"` with HTTP 403 | Service Principal lacks `CAN_EDIT` on the MLflow experiment. Grant it in the experiment permissions UI | 2 |
| `mlflowStatus: "mlflow_error"` with HTTP 404 | `traceId` is malformed or from a different experiment than `MLFLOW_EXPERIMENT_ID`. Verify `extractTraceId` is picking the right field (see [trace-extraction.md](references/trace-extraction.md)) | 2 |
| `config.host` is empty | Execution context not fully resolved. Ensure `await config.ensureResolved()` runs before `config.authenticate` | 2 |
| `messageMetaStore` is undefined in the feedback route | Stored on a different module's closure. Use the `globalThis.__appkitMessageMetaStore` pattern from [07-appkit-chat-history Step 4b](../07-appkit-chat-history/SKILL.md) | 2 |
| Feedback buttons never appear | Assistant message is missing `id`. Verify the client-side reducer in Step 4c of 07-appkit-chat-history is setting `assistantMessageId` from the `meta` SSE event | 3 |
| Same user clicks thumbs twice and two assessments appear in MLflow | `assessmentStore` lost its entry (e.g., server restarted). Rebuild by indexing assessments on message load, or tolerate duplicates — the first-clicked value is still authoritative via the DB upsert | 2 |

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [07-appkit-chat-history](../07-appkit-chat-history/SKILL.md) | Prerequisite — Vote table, `traceId` column, `messageMetaStore` |
| [06-appkit-serving-wiring](../06-appkit-serving-wiring/SKILL.md) | Reference — `custom-proxy-fallback.md` for the `config.authenticate` pattern |
| [05-appkit-lakebase-wiring](../05-appkit-lakebase-wiring/SKILL.md) | Reference — `AppKit.lakebase.query` |
| [04-appkit-plugin-add](../04-appkit-plugin-add/SKILL.md) | Reference — plugin configuration |

---

## See Also

- Upstream platform skill: [databricks-agent-skills / `databricks-apps`](https://github.com/databricks/databricks-agent-skills/tree/main/skills/databricks-apps) (tracked in `upstream_sources`).
- AppKit Serving plugin docs: [databricks.github.io/appkit/docs/plugins/serving](https://databricks.github.io/appkit/docs/plugins/serving)
- MLflow Traces API: [docs.databricks.com/api/workspace/mlflowtraces](https://docs.databricks.com/api/workspace/mlflowtraces), [MLflow tracing index](https://mlflow.org/docs/latest/llms/tracing/index.html)

