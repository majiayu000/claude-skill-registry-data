---
name: site-phase-1
description: >-
  Phase 1 — Load briefing from vendedor.db by ID. Returns lead metadata
  and all data_points for subsequent phases.
allowed-tools: Read, Bash
model: sonnet
effort: low
context: fork
user-invocable: false
---

# Phase 1 — Load Briefing

## Objective

Load the client briefing from the database and extract all data needed for the pipeline. This is a simple data retrieval phase.

## Step 1 — Query the database

Replace ID_HERE with the briefing ID provided by the orchestrator:

```bash
cd /Users/felipemoreiralanna/Documents/GitHub/vendedor-de-sites-v2
.venv/bin/python3 -c "
import sqlite3, json, sys
db = sqlite3.connect('data/vendedor.db')
row = db.execute('SELECT id, lead_source, lead_id, lead_name, lead_city, detected_niche, briefing_json FROM briefings WHERE id = ? OR lead_id = ?', ('ID_HERE', 'ID_HERE')).fetchone()
if not row: print('ERROR: Briefing not found'); sys.exit(1)
b = json.loads(row[6])
print(json.dumps({'db_id':row[0],'source':row[1],'lead_id':row[2],'name':row[3],'city':row[4],'niche':row[5],'data_points':len(b.get('data_points',[])), 'briefing':b}, ensure_ascii=False, indent=2))
db.close()
"
```

Save the full returned JSON — ALL data_points are needed in subsequent phases.

## Step 2 — Save state

```bash
cd /Users/felipemoreiralanna/Documents/GitHub/vendedor-de-sites-v2
mkdir -p sites/_state
echo '{"current_phase":1,"lead_id":"LEAD_ID_HERE","phases":{"phase_1":{"status":"complete"}}}' > sites/_state/progress.json
```

## Step 3 — Show summary to user

Display: name, city, niche, total data_points, total images.

## Exit Criteria

- [ ] Briefing loaded successfully (no errors)
- [ ] lead_id saved in state file
- [ ] User saw the summary
