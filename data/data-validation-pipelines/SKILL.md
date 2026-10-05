---
name: data-validation-pipelines
description: "A validation *boundary* is any point where data crosses from a system you do not"
---

# Data Validation Pipelines (Verbose)

## Core Patterns

### Validate at the Boundary

A validation *boundary* is any point where data crosses from a system you do not
control into one you do: an HTTP response, an S3 drop, a Kafka topic, a partner
SFTP file, a form submission. Put one gate at each boundary that parses raw input
into a typed domain object. Everything downstream of the gate may assume validity.

```python
from datetime import datetime, timezone
from pydantic import BaseModel, Field, ValidationError, field_validator

class OrderEvent(BaseModel):
    order_id: str = Field(pattern=r"^ORD-[0-9A-F]{12}$")
    customer_id: int = Field(gt=0)
    total_cents: int = Field(ge=0, le=1_000_000)   # >$10k routes to manual review
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    placed_at: datetime

    @field_validator("placed_at")
    @classmethod
    def sane_timestamp(cls, v: datetime) -> datetime:
        now = datetime.now(tz=timezone.utc)
        if v > now:
            raise ValueError("placed_at in the future")
        if (now - v).days > 365:
            raise ValueError("placed_at older than retention window")
        return v
```

The alternative — validating defensively wherever data is *used* — fails for three
reasons. The checks are never complete, because nobody knows the full set of call
sites. They drift apart, so one module treats `currency=""` as USD and another
raises. And they lose provenance: by the time a `NoneType` error surfaces in a
report, the file that produced it is four hops upstream and two days old.

Parse, don't validate: the gate's output type should make invalid states
unrepresentable. If an `OrderEvent` exists, its `currency` is three uppercase
letters — no downstream code needs to re-check.

### Schema Validation vs Data Quality

These are different jobs, and teams routinely ship only the first.

| | Schema validation | Data quality validation |
|---|---|---|
| Question | Is it shaped right? | Is it *true*? |
| Catches | Missing column, wrong type, bad enum | Impossible values, stale loads, broken joins |
| Fails when | Producer changes structure | Producer changes meaning |
| Tooling | Pydantic, Avro/Protobuf + registry, dbt contracts | Great Expectations, dbt tests, Soda, custom SQL |
| Cost | Per-row, cheap | Aggregate scan, expensive |

The dangerous class of bug lives entirely in the second column. An upstream team
renames a field, backfills the old one with zeros for compatibility, and every type
check passes while `revenue_usd` is `0.0` for a month. Or a currency column silently
switches from USD to local currency: still `float64`, still positive, still
non-null, and every regional total is now nonsense.

Semantic checks that repeatedly earn their keep:

```python
import great_expectations as gx

batch.expect_column_values_to_be_between("age", min_value=0, max_value=120)
batch.expect_column_values_to_be_in_set("country_code", VALID_ISO_3166)
batch.expect_column_values_to_be_unique("order_id")
batch.expect_column_pair_values_A_to_be_greater_than_B("shipped_at", "placed_at")
batch.expect_table_row_count_to_be_between(min_value=3_500_000, max_value=5_000_000)
batch.expect_column_mean_to_be_between("total_cents", min_value=1500, max_value=9000)
```

That last one — asserting on a *distribution statistic* rather than a row
predicate — is what catches the unit change, the silent backfill, and the
deduplication regression. No per-row rule can see any of those.

### Volume, Freshness, and Referential Integrity

Missing data is more common than malformed data and far quieter. Three assertions
cover most of it:

```sql
-- 1. Freshness: has anything landed recently?
select max(loaded_at) as last_load,
       datediff('minute', max(loaded_at), current_timestamp) as staleness_min
from analytics.orders
having staleness_min > 90

-- 2. Volume: is today's partition in family with recent history?
with daily as (
  select load_date, count(*) as n
  from analytics.orders
  where load_date >= dateadd('day', -28, current_date)
  group by 1
),
baseline as (select median(n) as med from daily where load_date < current_date)
select d.load_date, d.n, b.med
from daily d cross join baseline b
where d.load_date = current_date
  and (d.n < 0.7 * b.med or d.n > 1.5 * b.med)

-- 3. Referential integrity: orphaned foreign keys
select o.customer_id
from analytics.orders o
left join analytics.customers c on o.customer_id = c.customer_id
where c.customer_id is null
```

In dbt these map to `dbt_utils.recency`, a custom volume test, and the built-in
`relationships` test — worth using the packaged versions so results land in the
manifest and show up in the docs graph rather than only in a job log.

Express bounds relative to a trailing window, not as constants. A threshold of
`row_count > 1000000` written when the table was young becomes meaningless once the
table does ten million a day, and it will not fire on a 60% drop.

### Quarantine Instead of Halting

A pipeline that fails the whole batch on the first bad row gets disabled by the
third page. Split the stream:

```python
valid, rejected = [], []
for raw in incoming:
    try:
        valid.append(OrderEvent.model_validate(raw))
    except ValidationError as exc:
        rejected.append({
            "raw": raw,
            "errors": exc.errors(),          # field, rule, and offending value
            "batch_id": batch_id,
            "rejected_at": datetime.now(tz=timezone.utc),
        })

write_rejects(rejected)
reject_rate = len(rejected) / max(len(incoming), 1)
if reject_rate > 0.01:
    raise PipelineError(f"reject rate {reject_rate:.2%} exceeds 1% threshold")
load(valid)
```

Keeping the raw payload is the part people skip and later regret — without it you
can neither reproduce the failure nor replay the rows once the upstream bug is
fixed. The reject table also doubles as the best data-quality dashboard you will
get for free: rules ranked by fire count tell you which producer to go talk to.

### Severity Tiers and Write-Audit-Publish

| Severity | Behavior | Example |
|---|---|---|
| `error` | Block publication; readers keep the last good version | Primary key not unique; row count −80% |
| `warn` | Publish, open a ticket, annotate the table | New unseen category; null rate up 3pp |
| `info` | Record a metric only | Distribution shift inside tolerance |

Pair `error` with **write-audit-publish**: load into a staging table, run the checks
there, and swap the production pointer only if they pass. Readers never observe a
partially-validated table, and rollback is a pointer move rather than a restore.

### Contracts at the Producer

Runtime validation is a net; a contract is a fence. Where the producer is inside
your organization, register the schema and make incompatible changes fail *their*
CI rather than your 3am job.

```yaml
# dbt: enforce the shape at build time
models:
  - name: dim_customer
    config:
      contract:
        enforced: true
    columns:
      - name: customer_id
        data_type: bigint
        constraints:
          - type: not_null
          - type: primary_key
```

Avro or Protobuf behind a schema registry set to `BACKWARD` compatibility does the
same for streams: a producer that drops a required field cannot deploy at all.

For validation of the *transformations* between tables rather than the data
entering them, see `sql-optimization` for query-level concerns and
`dimensional-modeling` for grain and key integrity.

## Common Anti-Patterns

❌ **Null checks scattered through transformation code** — incomplete, mutually
inconsistent, and the error surfaces far from its source.
✅ One validation gate per boundary that parses into a typed object.

❌ **Treating schema conformance as data quality** — types pass while the values
are nonsense.
✅ Add range, set, uniqueness, referential, freshness, and distribution checks.

❌ **Failing the entire load on one bad row.**
✅ Quarantine rows with their raw payload; fail on reject *rate*.

❌ **Every check severity set to `error`** — on-call learns to rerun with checks
skipped, and validation stops existing in practice.
✅ Tier checks; reserve blocking for correctness-critical invariants.

❌ **Validating only in the warehouse** — the bad data is already six hours old and
has fanned out to three downstream marts.
✅ Validate at ingest too; warehouse tests are the second line, not the first.

❌ **Hard-coded thresholds nobody revisits.**
✅ Bound against a trailing window so limits track real growth.

❌ **Validation results that go nowhere but the job log.**
✅ Persist outcomes as a table; alert on trends, not only the latest run.

❌ **Checking only for nulls in a column that is never null** — a rule that has
never fired is telling you something, usually that it tests the wrong thing.
✅ Periodically review fire rates and retire or retarget dead rules.

## Data Validation Checklist

- [ ] Every external input has exactly one validation gate
- [ ] Gate output is a typed object downstream code can trust
- [ ] Schema checks cover types, required fields, enums, patterns
- [ ] Semantic checks cover ranges, sets, uniqueness, cross-field consistency
- [ ] Referential integrity tested on every foreign key
- [ ] Freshness assertion with an explicit staleness SLA
- [ ] Row-count check bounded against a trailing window, not a constant
- [ ] At least one distribution statistic asserted per critical numeric column
- [ ] Invalid rows quarantined with raw payload, failing rule, and batch id
- [ ] Job fails on reject rate rather than on a single rejected row
- [ ] Checks tiered into error / warn / info
- [ ] Write-audit-publish so readers never see unvalidated data
- [ ] Schema contract enforced at the producer where the producer is internal
- [ ] Check results persisted and trended over time
- [ ] Rule fire rates reviewed; dead rules retired
