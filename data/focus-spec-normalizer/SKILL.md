---
name: focus-spec-normalizer
description: Normalize vendor-specific billing rows (AWS CUR, Azure Cost Management, GCP Billing Export, OCI) into FOCUS v1.2 columns from user-pasted CSV or JSON input. Refuses to invent column values not derivable from the input. No credentials accepted; operates on user-supplied data only.
allowed-tools: Read Grep Glob
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.1"
  updated: "2026-05-13"
  category: finops
  lifecycle: experimental
---

# FOCUS Spec Normalizer

## Purpose

Map vendor-specific billing row data (pasted as CSV or JSON snippet) to FOCUS v1.2 columns. The output is a FOCUS-normalized row or set of rows that can be ingested by any FinOps tool that accepts FOCUS-formatted data.

No network access. No credentials. All input is user-supplied billing data.

## When to use

Use this skill when:

- The user has pasted one or more billing rows from AWS CUR, Azure Cost Management export, GCP Billing Export, or OCI billing and wants them mapped to FOCUS v1.2 columns
- The user wants to understand which FOCUS columns can and cannot be populated from a given vendor's billing format
- The user is building a multi-cloud cost normalization pipeline and needs the column-level mapping documented

## Operating rules

- **No credential accepted.** No cloud credentials, billing account IDs, tenant IDs, or service principal data are accepted. The user pastes de-identified or sample billing data; no live API connection is made.
- **No invented values.** If a FOCUS column cannot be populated from the data in the input row, the output cell is set to `null` and the reason is stated. Do not infer, default, or fabricate values for required FOCUS columns that are absent from the input.
- **Input format.** Accept CSV (with header row) or JSON object/array. State the detected format before mapping.
- **Provenance labels.** Every mapped FOCUS column value must carry one label:
  - `mapped` — value is directly present in the input row under a different column name
  - `derived` — value is computed from one or more input columns using a documented transformation (state the transformation)
  - `null` — column cannot be populated from the available input (state why)
- **FOCUS version.** This skill targets FOCUS v1.2. State the FOCUS version in every output.
- **Load references only when needed.**

## Mapping behavior

### Step 1: detect vendor

Identify the billing format from the column names present in the input header:
- AWS CUR: columns include `lineItem/UsageType`, `lineItem/ProductCode`, `lineItem/BlendedCost`, `lineItem/UnblendedCost`
- Azure Cost Management: columns include `CostInBillingCurrency`, `ResourceType`, `SubscriptionId`, `MeterName`
- GCP Billing Export: columns include `service.description`, `sku.description`, `cost`, `usage.amount`, `project.id`
- OCI: columns include `currency/currencyCode`, `cost/myCost`, `service/serviceName`, `product/resourceName`

If the vendor cannot be identified from column names, ask one clarifying question.

### Step 2: apply vendor-specific mapping

Load the relevant mapping section from references/vendor-mapping.md for the detected vendor, then produce FOCUS v1.2 output columns.

### Step 3: flag gaps

For any required FOCUS v1.2 column that cannot be populated, include a gap note:

```
<FocusColumn>: null
  Reason: <why this column cannot be populated from <vendor> billing data>
  Resolution: <where in the vendor's billing config this data can be enabled, if known>
```

## Response shape

Return:

1. Detected vendor and input format.
2. FOCUS v1.2 normalized row(s) in JSON object format.
3. Provenance label for each column value.
4. Gap summary table listing columns set to null and resolution notes.
5. FOCUS version declared: `1.2`.

Example output structure:

```json
{
  "FocusVersion": "1.2",
  "ProviderName": "Amazon Web Services",
  "PublisherName": "Amazon Web Services",
  "ServiceCategory": "Compute",
  "ServiceName": "Amazon EC2",
  "ChargeCategory": "Usage",
  "ChargeDescription": "...",
  "ChargeFrequency": "Usage-based",
  "BillingPeriodStart": "2026-04-01T00:00:00Z",
  "BillingPeriodEnd": "2026-05-01T00:00:00Z",
  "BilledCost": 42.50,
  "BilledCurrency": "USD",
  "EffectiveCost": null,
  "ListCost": null,
  "ContractedCost": null,
  "ResourceId": "i-0abc1234def567890",
  "ResourceName": null,
  "SkuId": "RunInstances:0014",
  "SkuPriceId": null,
  "Region": "us-east-1",
  "AvailabilityZone": "us-east-1a",
  "Tags": {}
}
```

Each field in the output is annotated with its provenance label in the gap summary.

## References

Load these only when needed:

- [FOCUS v1.2 column definitions](references/focus-columns.md) — every required column with type and example.
- [Vendor mapping tables](references/vendor-mapping.md) — AWS CUR, Azure Cost Management, GCP Billing Export, and OCI to FOCUS mapping.
