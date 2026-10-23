---
name: jmeter-load-testing
description: "Authors Apache JMeter `.jmx` test plans (Thread Groups + HTTP samplers + assertions + listeners) in the JMeter GUI, runs them headlessly via `jmeter -n -t plan.jmx -l results.jtl`, generates an HTML dashboard with `-e -o`, and gates CI on JTL parsing. Use when the project has an existing JMeter investment, needs JVM-native load tooling, or works in domains with strong JMeter community support (banking, telecom, enterprise)."
---

# jmeter-load-testing

## Overview

Apache JMeter is the long-running JVM-native load-testing tool. Tests
are XML `.jmx` files authored in JMeter's GUI; CI runs them headless
via the `jmeter` CLI ([jmeter-getstarted][getstarted]).

[getstarted]: https://jmeter.apache.org/usermanual/get-started.html

The official guidance is explicit:

> "GUI mode should only be used for creating the test script, CLI mode
> (NON GUI) must be used for load testing." ([jmeter-getstarted][getstarted])

This skill covers the CLI / CI side. Authoring is GUI-driven and out
of scope here - see the JMeter user manual for the Thread Group /
HTTP Sampler / Assertion authoring flow.

## When to use

- The project already has `.jmx` test plans.
- The team is on the JVM and prefers JMeter's mature ecosystem
  (BlazeMeter, Taurus, plugin manager, distributed mode).
- A specific protocol is needed that JMeter has first-class support
  for: JDBC, JMS, MQTT, FTP, LDAP, SOAP - k6's plugin landscape is
  weaker for niche protocols.

If the team is starting fresh, evaluate
`k6-load-testing` (developer-friendly JS) or the Gatling (JVM DSL) and
Locust (Python) references in `load-testing-overview` before adopting
JMeter - XML authoring has a steep learning curve.

## Install

JMeter requires **Java 8 or higher** with `JAVA_HOME` set. Download
the latest release from
[jmeter.apache.org](https://jmeter.apache.org/) and extract - there
is no installer ([jmeter-getstarted][getstarted]).

For Docker-based CI, official images are at `apache/jmeter`. Pin to
a specific tag rather than `latest`.

## Running

### Canonical CLI invocation

Per [jmeter-getstarted][getstarted]:

```bash
jmeter -n -t test.jmx -l results.jtl
```

| Flag | Purpose                                                 |
|------|---------------------------------------------------------|
| `-n` | Non-GUI mode. **Required for load tests.**              |
| `-t` | Path to the `.jmx` test plan.                            |
| `-l` | Output file for raw sample results (JTL - CSV-shaped).  |

### With HTML dashboard

Per [jmeter-getstarted][getstarted]:

```bash
jmeter -n -t test.jmx -l results.jtl -e -o report_folder
```

| Flag | Purpose                                                  |
|------|----------------------------------------------------------|
| `-e` | Generate the HTML dashboard report automatically.        |
| `-o` | Output folder (must be empty or non-existent).           |

The dashboard shows percentiles, throughput, error rates, response-
time graphs, and per-sampler breakdowns - the canonical JMeter
output for human review.

### Other useful flags

| Flag                              | Purpose                                                 |
|-----------------------------------|---------------------------------------------------------|
| `-J<property>=<value>`            | Override a JMeter property at the JVM level.            |
| `-G<property>=<value>`            | Override a property in distributed (remote) mode.       |
| `-Jjmeter.save.saveservice.output_format=csv` | Force CSV JTL (vs. XML).               |
| `-q <props-file>`                 | Additional properties file.                              |
| `-r`                              | Start the test on remote slaves (distributed mode).      |
| `-X`                              | Exit JMeter when the test finishes.                      |

For multi-environment runs, parameterize the test plan with
`${__P(api.base.url, default)}` and override at the CLI:

```bash
jmeter -n -t orders.jmx -l results.jtl \
  -Japi.base.url=https://staging.example.com \
  -Japi.token=$API_TOKEN
```

## Parsing results

The JTL file is the structured artifact for CI gating. Default JTL
columns (CSV): `timeStamp`, `elapsed`, `label`, `responseCode`,
`responseMessage`, `threadName`, `dataType`, `success`, `failureMessage`,
`bytes`, `sentBytes`, `grpThreads`, `allThreads`, `URL`, `Latency`,
`IdleTime`, `Connect`.

Quick-and-dirty pass/fail with `awk`:

```bash
# Count errors
awk -F',' 'NR>1 && $8=="false"' results.jtl | wc -l

# Compute mean response time
awk -F',' 'NR>1 { sum+=$2; n++ } END { print sum/n }' results.jtl
```

For richer parsing, use the JMeter HTML report's
`statistics.json` under the report folder - it contains the
percentiles per sampler in JSON form.

## CI integration

```yaml
# .github/workflows/jmeter.yml
name: load-test

on:
  pull_request:
    paths: ['tests/load/**.jmx']
  schedule:
    - cron: '0 4 * * *'

jobs:
  jmeter:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Run JMeter via Docker
        env:
          API_TOKEN: ${{ secrets.STAGING_API_TOKEN }}
        run: |
          docker run --rm \
            -v "$PWD:/work" \
            -w /work \
            apache/jmeter \
              -n -t tests/load/orders.jmx \
              -l results.jtl \
              -e -o report \
              -Japi.token=$API_TOKEN \
              -Japi.base.url=https://staging.example.com

      - name: Pass/fail gate
        run: |
          ERRORS=$(awk -F',' 'NR>1 && $8=="false"' results.jtl | wc -l)
          if [ "$ERRORS" -gt 10 ]; then
            echo "::error::Got $ERRORS errors (>10 threshold)"
            exit 1
          fi

      - name: Upload report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: jmeter-report
          path: |
            report/
            results.jtl
          retention-days: 14
```

The Docker invocation pattern keeps the CI runner clean - no Java /
JMeter install on the runner.

## Anti-patterns

| Anti-pattern                                              | Why it fails                                                         | Fix |
|-----------------------------------------------------------|----------------------------------------------------------------------|-----|
| Running tests in GUI mode "just for this one quick run"   | GUI runner adds overhead; metrics are skewed; per [jmeter-getstarted][getstarted] this is explicitly forbidden for load tests. | Always `-n`. GUI is for authoring only. |
| Hard-coding URLs / tokens in the `.jmx` XML                | Test plan binds to one environment.                                  | Parameterize: `${__P(api.base.url, ...)}`; override with `-J`. |
| Saving JTL in XML format                                  | XML JTL files are 5-10x larger than CSV; slow to parse.            | Force CSV with `-Jjmeter.save.saveservice.output_format=csv`. |
| Listeners enabled in CI runs                              | UI listeners (View Results Tree, Aggregate Report) consume RAM proportional to sample count; OOMs at scale. | Disable all listeners in `.jmx`; emit JTL only; generate HTML report post-run via `-e -o`. |
| One mega-test-plan with 100 samplers                      | Failure attribution is hard; runtime dominated by one slow endpoint. | Split into per-domain `.jmx` files; run as separate CI jobs. |
| Threshold gates only on error rate                         | A 30-second response that succeeds passes the rate gate but breaks UX. | Pair error-rate with percentile gates parsed from `statistics.json`. |

## Limitations

- **XML authoring.** `.jmx` files are not human-friendly; reviews of
  test-plan changes are awkward.
- **Memory hungry.** JMeter's per-sample memory overhead is high
  vs. k6 / Gatling.
- **Single-machine VU limits.** ~1000 threads per machine before JVM
  contention; for higher loads, use distributed mode (master +
  remote slaves) or move to a tool with a smaller per-VU footprint.
- **Plugin ecosystem fragmentation.** Many JMeter plugins are
  abandoned; vet plugin maintenance status before depending on one.

## References

- [jmeter-getstarted][getstarted] - canonical CLI flags, GUI-vs-CLI
  guidance, dashboard generation.
- Apache JMeter user manual - https://jmeter.apache.org/usermanual/
- `k6-load-testing` and the Gatling / Locust references in
  `load-testing-overview` - alternatives by stack.
- `perf-budget-gate` - downstream
  gate aggregating multiple runner verdicts.
