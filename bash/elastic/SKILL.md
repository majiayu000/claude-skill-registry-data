---
name: elastic
description: >-
  Elasticsearch cluster via a Python CLI (basic auth). Ping, cluster health,
  list indices, manage Kibana dashboards, visualizations, data views, and cases, and Elastic
  Security detection rules. Use when the user mentions Elasticsearch, Elastic,
  Kibana, an ES cluster, security rules, alerts, cases, or invokes /elastic_*.
disable-model-invocation: true
---

### TO COPY

# elastic

Per-workspace registration slice. Credentials live in `{SKILL_PATH}/.env`.

## Working directory

Placeholders changed by `/meta-skills` at copy time (NAME => {PLACEHOLDER}):

IS_GLOBAL => {IS_GLOBAL}
TYPE_OF_AI_TOOLS => {TYPE_OF_AI_TOOLS}
SKILL_PATH => {SKILL_PATH}

```bash
export CURRENT_SKILL_DIRECTORY="{SKILL_PATH}"
~/.meta-skills/.venv/bin/python ~/.meta-skills/skills/db/elastic/scripts/cli.py env
```

##### END TO COPY

# elastic

Elasticsearch REST API via the official Python client ([docs](https://www.elastic.co/docs/api/doc/elasticsearch)). Auth: HTTP basic (`USERNAME` / `PASSWORD`) against `URL`.

## When to use

Trigger phrases: "Elasticsearch", "Elastic cluster", "Kibana dashboards", "data view", "list ES indices", "cluster health", "security rule", "detection rule", "Kibana case", `/elastic_*`.

`skill_env.py` loads `.env` via SkillCred — do not `source` it in the shell. `CURRENT_SKILL_DIRECTORY` is the only required export.

Prefer `~/.meta-skills/.venv/bin/python` from `~/.meta-skills/skills/db/elastic/`.

## Credentials — SkillCred `.env`

`.env` is next to the **registered** skill, resolved by `SkillCred("elastic", [".env"])`.

| Variable | Notes |
|----------|--------|
| `URL` | Cluster URL (`https://localhost:9200` or Elastic Cloud endpoint) |
| `USERNAME` | Basic-auth user |
| `PASSWORD` | Basic-auth password |

```bash
cp ~/.meta-skills/skills/db/elastic/.env.example "{SKILL_PATH}/.env"
# edit URL / USERNAME / PASSWORD
python scripts/cli.py env
```

First deps: `cd ~/.meta-skills/skills/db/elastic && ~/.meta-skills/install.sh pip init .`

Local self-signed certs (localhost / 127.0.0.1) skip TLS verify. Elastic Cloud keeps verify on.

## Command sections

Map `/elastic_<…>` → `python scripts/cli.py …`; return JSON. Slash/CLI tables live in `command.md/` under the shared library.

## elastic-cluster

`.env` validation, cluster ping, and cluster health.
Open the command file for `/elastic_env`, `/elastic_ping`, or `/elastic_health`.

Commands → `~/.meta-skills/skills/db/elastic/command.md/elastic-cluster.command.md`

---

## elastic-indices

Index inventory, field mappings, and document search.
Open the command file to list indices, inspect `{INDEX}` fields, or run `--esquery`.

Commands → `~/.meta-skills/skills/db/elastic/command.md/elastic-indices.command.md`

---

## elastic-dashboard

Kibana dashboards — list, get, create, replace.
Open the command file for dashboard JSON (`{TITLE}`, `{VIS_ID}`, `{DASH_ID}`). `update` is a full replace.

Commands → `~/.meta-skills/skills/db/elastic/command.md/elastic-dashboard.command.md`

---

## elastic-visualization

Kibana visualizations library — list, get, create, replace, delete.
Open the command file for visualization JSON (`{TITLE}`, `{INDEX_PATTERN}`, `{TIME_FIELD}`, `{VIS_ID}`). `update` is a full replace.

Commands → `~/.meta-skills/skills/db/elastic/command.md/elastic-visualization.command.md`

---

## elastic-data-view

Kibana data views — get, create, patch, delete.
Open the command file for `{DATA_VIEW_ID}`, `{INDEX}*`, `{NAME}`, `{TIME_FIELD}`. `update` is a partial POST.

Commands → `~/.meta-skills/skills/db/elastic/command.md/elastic-data-view.command.md`

---

## elastic-alert

Elastic Security detection alerts (get / delete) and rules (create, get, update, delete).
Open the command file for `{ALERT_ID}`, `{RULE_ID}` / `{JSON}`. Confirm before writes. Rule `update` is a full replace.

Commands → `~/.meta-skills/skills/db/elastic/command.md/elastic-alert.command.md`

---

## elastic-case

Kibana cases — get, create from an alert, attach an alert, delete the case and its alerts.
Open the command file for `{CASE_ID}`, `{ALERT_ID}` / `{JSON}`. Confirm before writes. `delete` also removes attached alerts.

Commands → `~/.meta-skills/skills/db/elastic/command.md/elastic-case.command.md`

---

## How to run

1. `export CURRENT_SKILL_DIRECTORY="{SKILL_PATH}"` then `cd ~/.meta-skills/skills/db/elastic`.
2. Ensure `.env` exists next to the registered skill; `/elastic_env`.
3. Map `/elastic_<…>` → `~/.meta-skills/.venv/bin/python scripts/cli.py …`; return JSON.

## Notes

- Confirm with the user before destructive index/document writes, `kibana visualization delete`, `kibana data-view` create / update / delete, dashboard/visualization `update` (PUT is a full replace), `kibana case` create-from-alert / add-alert / delete, `alert delete`, and `alert security-rule` create / update / delete.
- Never commit `.env` or echo `PASSWORD`.
- Docs: [Elasticsearch Python client](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html).
