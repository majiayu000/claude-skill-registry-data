---
name: Query Grafana Tempo
description: Query and explore distributed traces in Grafana Tempo. Use when a user asks to pull tracing data for analysis.
allowed-tools: Bash(curl --get:*)
---

# Read from Grafana Tempo

## Instructions

When a user refers to a date or a range of dates, use the "unix epoch seconds" format. Always assume
the time is UTC unless specified explicitly.

Prefer storing the output in a temporal text file to run any analysis on the fetched data offline.

## Examples

Retrieve a trace:

```
curl --get -g 'https://tempo-ops-01-ops-eu-south-0.grafana-ops.net/tempo/api/v2/traces/<trace>' \
-u 1:`cat $HOME/.config/gcom/gcom-ops.token` \
--data-urlencode 'start=<unixts>' --data-urlencode 'end=<unixts>'
```

The user "1" is the well-known "ops tenant". The API password for the tenant is stored in the mentioned file.

Use the "ops" instance to pull logs for *all non-dev* workloads.

Run the query against the **dev Tempo instance** (note user "3"):

```
curl --get -g 'https://tempo-dev-01-dev-us-central-0.grafana.net/tempo/api/v2/traces/<trace>' \
  -u 3:`cat $HOME/.config/gcom/gcom-dev.token` \
  --data-urlencode 'start=<unixts>' --data-urlencode 'end=<unixts>'
```

Retrieve the trace `ee309726a47bd91c00d48037ef0eacb4` from a time range from 2025/12/09 10:55 until 2025/12/09 11:05 (time is in UTC):

```
curl --get -g "https://tempo-ops-01-ops-eu-south-0.grafana-ops.net/tempo/api/v2/traces/ee309726a47bd91c00d48037ef0eacb4" \
  -u 1:`cat ~/.config/gcom/gcom-ops.token` \
  --data-urlencode 'start=1765277700' --data-urlencode 'end=1765278300'
```

## Reference

The complete online reference for Grafana Tempo API is available at https://grafana.com/docs/tempo/latest/api_docs/
