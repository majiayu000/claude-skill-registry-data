---
name: create-grafana-dashboards
description: "Use when creating, reviewing, or extending a Grafana dashboard for a service, cloud resource, database, queue, or runtime: choosing metrics from the vendor's official monitoring page, laying out rows by RED or USE, trading paid metrics for log-derived panels, writing the dashboard README, or collecting screenshots. Also use when the user mentions CloudWatch, Prometheus, Loki, OpenTelemetry metrics, dashboard JSON, panel rows, RED method, or USE method."
---
# Grafana dashboard

## When to use
- User asks for a dashboard for a service, a cloud resource, a database, a queue, or a runtime
- User asks which metrics belong on a dashboard, or how to organise panels and rows
- A dashboard JSON needs a review, a new row, or a README with screenshots
- A metric family is billed or opt-in and the user asks whether logs can replace it

## Overview

A dashboard is a selection, not a collection. Start from the vendor's official
monitoring page for the service, keep the metrics that answer a RED question, USE
when nothing is requested,
and link that page from the README and the dashboard. Claude writes the JSON and the
README; the human runs it against live data and takes the screenshots.

Reference: [checklist.md](checklist.md). Walk it top to bottom before handing over.
Reference: [readme-template.md](readme-template.md). Copy it for the README.
Claims about an application's own instrumentation follow the
[`evidence-based-analysis`](../evidence-based-analysis/SKILL.md) skill.

## Workflow

1. Find the reference. Locate the vendor's official metrics page for the service:
   an AWS "Monitoring with CloudWatch" page, an OpenTelemetry semantic convention, a
   library's metrics document. Record its URL. No reference page, no dashboard: ask.
2. Read the infrastructure as code before the metrics. Find the Terraform,
   CloudFormation, CDK, Helm, or Kustomize that deploys the service and read the
   resource and the module it calls: engine and version, instance class, serverless
   or provisioned, replica count, log exports, parameter groups, monitoring
   features switched on or off, and their defaults in the module. That is the
   deployed variant. Module defaults you cannot read are unknowns, named as such.
   Then scope the metrics: read every metric on the page, keep the ones that apply
   to that variant, drop the rest and name the dropped families in one README line.
   Then read the service's quotas page and keep every limit that throttles or stops
   the service, with the metric that consumes it and the one that counts rejections
   (see Quotas and limits).
3. Pick the method. RED (rate, errors, duration) whenever the service has a request
   stream, and most do: HTTP servers, APIs, consumers, functions, databases (commits
   and I/O are requests), queues (messages). Saturation and limits follow as a fourth
   group. USE (utilization, saturation, errors) only for resources with no request
   metric at all: storage volumes, nodes, billing. Map every kept metric to one
   signal; a metric with no signal leaves the dashboard.
4. Organise rows. Rows mirror the sections of the reference page, in the page's
   order; a section with more than twelve panels splits into sub-rows that carry
   the section name. Inside a row, panels go rate, errors, duration, then
   saturation and limits. A paid or opt-in source gets its own collapsed row with
   its own reference link.
5. Add logs when the source has them: a Logs row driven by a log group or stream
   variable and a text filter, plus an error-log panel next to the error metric.
6. Price the paid families and ask. When a family is billed or needs an agent (Lambda
   Insights, S3 request metrics, RDS Performance Insights, Enhanced Monitoring),
   fetch the vendor's pricing page, estimate the monthly cost for the user's resource
   count and period, and put it next to the log-derived alternative with what that
   alternative loses. Show the preview and ask which way to go; never decide alone.
   Whatever the answer, the log-derived panels go in the main rows and the paid
   family in a collapsed row, so one dashboard serves both choices. The AWS Lambda
   dashboard is the worked example: REPORT lines in the function log group give
   duration, billed duration, init duration, memory size, and max memory used for
   free, and Lambda Insights stays collapsed for the users who pay for it.
7. Build the variables and panels from [checklist.md](checklist.md). Generate the
   JSON from a script kept out of the repository, and lint the output: unique panel
   ids, no grid overlap, every target bound to the period and region variables, no
   datasource uid. A hand-edited 4000-line JSON drifts; a generator does not.
8. Write the README from [readme-template.md](readme-template.md).
9. Review the first live view with the human before any screenshot. Read the
   legends for resources that do not belong to the selection, check that math
   expressions and threshold lines render, and open an empty log panel over a week
   before blaming the query. Fix the JSON, re-import, then ask for screenshots: one
   header image and one image per row, two for a long row, named by row order.
   Claude cannot render Grafana, but it edits the images: anonymise them before
   they enter the repository, then link them in the README. Never skip an image or
   describe one that does not exist.
10. Ship a template, not an instance. The JSON is the "export for sharing externally"
    form: id null, no datasource uid, the datasource reached through a datasource
    variable or an input, requirements listed. Publishing is two commits because the
    grafana.com id exists only after the first publish: commit and publish, then add
    the grafana.com link to the links array and commit again. Commits go through the
    [`git-conventions`](../git-conventions/SKILL.md) skill.

## Metric selection per signal

| Signal | Keep | Statistic |
|---|---|---|
| Rate | Request, invocation, commit, message counts; throughput | Sum per period, or a rate over the rate interval |
| Errors | Error counts, throttles, deadlocks, 4xx and 5xx, failed logins, shutdown reasons | Sum, drawn as red bars |
| Duration | Latency averages, percentiles, histograms, replica lag | Average plus p95 or p99; histogram quantile on buckets |
| Utilization | CPU, memory, connections, IOPS, network, storage used | Average or Maximum |
| Saturation | Queue depth, concurrency against a limit, credit balance, free memory, free storage, in-flight requests | Maximum, with the limit as a second series when known |

Not: "Add every metric of the AWS/RDS namespace."
Yes: "Aurora PostgreSQL on db.t4g: keep CPUCreditBalance, drop ACUUtilization, serverless only."

## Quotas and limits

A quota that is hit is an outage or a throttle, so every one the service documents
gets three things on the dashboard: the consumption metric, the limit on the same
panel as a second series or a threshold line, and the rejection counter as red bars.

| Limit lives in | Draw it as | Example |
|---|---|---|
| A metric of its own | Second series on the consumption panel | Lambda UnreservedConcurrentExecutions beside ConcurrentExecutions; DynamoDB AccountMaxReads beside the account utilization |
| A service quota | Metric math on the usage metric, percent of quota | CloudWatch SERVICE_QUOTA on an AWS/Usage ResourceCount |
| A parameter or an instance class | Text box variable drawn as a constant series, default from the vendor's formula | Aurora max_connections beside DatabaseConnections |
| A hard engine constant | Threshold line | PostgreSQL transaction ID wraparound at 2,146,483,648 |
| Billing or fair-use tiers | Ratio of usage to included amount, discards by reason | Grafana Cloud discarded samples per reason, query fair-usage ratio |

Rejection counters: Throttles, ThrottledRequests, ReadThrottleEvents, discarded
samples, rejected connections. They sit in the errors position of their row.

## Pricing preview

One table, shown to the user before any paid family is kept or dropped. Figures come
from the vendor's pricing page fetched that day, scaled to the user's resource count
and query volume; a figure Claude cannot source is marked unknown, never guessed.

| Paid or opt-in source | Monthly estimate | Free substitute | Lost with the substitute |
|---|---|---|---|
| Lambda Insights | per function, from the pricing page | REPORT lines parsed from the function log group | Network bytes, CPU time |
| S3 request metrics | per metric, from the pricing page | Server access logs or CloudTrail data events | One-minute granularity |
| RDS Performance Insights | per vCPU beyond the free tier | Slow query log, engine log export | Wait-event breakdown |
| Enhanced Monitoring | log ingestion at the chosen granularity | CloudWatch instance metrics at one-minute period | Per-process OS view |

Log queries cost too: Logs Insights bills scanned bytes, so the preview carries the
substitute's scan estimate for the dashboard's default time range. Keep the paid
row collapsed and labelled optional. A dashboard with no data in a collapsed row
still works for the user who did not enable the feature.

Not: "Lambda Insights is paid, so I replaced it with log panels."
Yes: "Lambda Insights: about 12 USD a month for 20 functions; REPORT lines give the same durations and memory for free but no network or CPU time. Keep it, or go with logs?"

## Scoping a panel to the selected resource

A multi-value variable on All reaches CloudWatch as a wildcard, and a wildcard on a
child dimension spans the whole account: instance panels then show every instance
of every cluster. Scope with the dimension pair the vendor publishes for the parent,
such as DBClusterIdentifier plus Role for Aurora, and keep the child dimension for
single-select drill-down only. The first live view tells: a legend naming a foreign
resource is a scoping bug, not a quota.

## Anonymising screenshots

Screenshots leave the organisation with the dashboard. Before a file enters the
repository, paint over and rewrite: resource identifiers, account ids, folder paths
in the breadcrumb, data source names, log group names, people and avatars. Keep
metric names, statistics, units, and values: they are what the image documents.
Sample the background colour under each patch, redraw the text in the same size,
and view the result before saving. Without an image library, ffmpeg's drawbox and
drawtext filters do the job.

Not: "aurora-prod-eu-1-20240606140220573600000002 CPUUtilization Average"
Yes: "WRITER CPUUtilization Average" or "aurora-db VolumeBytesUsed Average"

## Boundaries

This skill never invents a metric: a name absent from the reference page or the
exporter's output stays off the dashboard. It never renders a screenshot and never
writes a README image link without the file. Alerting rules, SLOs, and datasource
provisioning are out of scope.
