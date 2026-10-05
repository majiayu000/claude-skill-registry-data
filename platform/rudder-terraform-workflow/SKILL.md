---
name: rudder-terraform-workflow
description: Manages RudderStack resources via the terraform-provider-rudderstack. Use when configuring the provider, authoring HCL for sources, destinations, connections, running init/plan/apply, importing existing resources, or organizing multi-workspace Terraform modules.
allowed-tools: "Bash(terraform *), Read, Write, Edit"
---

# RudderStack Terraform Workflow

The [`rudderlabs/rudderstack`](https://github.com/rudderlabs/terraform-provider-rudderstack) Terraform provider manages a RudderStack workspace as infrastructure-as-code: sources, destinations, and connections.

## When to use

The user is authoring HCL for RudderStack, running `terraform plan/apply` against a workspace, migrating from UI-managed to Terraform-managed resources, importing existing resources, or organizing multi-env setups.

## Preflight

- [ ] Terraform ≥ 1.0 installed
- [ ] Access token available as env var `RUDDERSTACK_ACCESS_TOKEN` (preferred) or in the provider block
- [ ] Optional: override API base URL with `RUDDERSTACK_API_URL` (default: `https://api.rudderstack.com`)
- [ ] Confirm with the user whether the target workspace is dev/staging/prod before any `terraform apply`

## Provider setup

```hcl
terraform {
  required_providers {
    rudderstack = {
      source  = "rudderlabs/rudderstack"
      version = "~> 4.4"
    }
  }
}

provider "rudderstack" {
  # access_token = "..."                    # or set RUDDERSTACK_ACCESS_TOKEN env var
  # api_url      = "https://api.rudderstack.com"
}
```

## Resource catalog

| Category | Count | Examples |
|----------|-------|----------|
| **Connection** | 1 | `rudderstack_connection` — links source to destination |
| **Sources** | ~50 | SDK sources (JS, Android, iOS, Python, Go, etc.), webhooks, SaaS integrations |
| **Destinations** | ~46 | Warehouses, analytics, marketing, ad platforms, infrastructure |

### Source types

- **SDK sources** (no config): JavaScript, Android, iOS, Python, Node.js, Go, Ruby, PHP, .NET, Flutter, Rust, Kotlin, Swift, Unity
- **Webhook sources** (no config): HTTP, Shopify Webhook
- **SaaS integrations**: Auth0, Braze, Slack, Segment, PagerDuty, Looker, Customer.io, Iterable, etc.

### Destination types

- **Warehouses**: BigQuery, Redshift, Snowflake, PostgreSQL, S3, GCS
- **Analytics**: Google Analytics 4, Amplitude, Mixpanel, Posthog, Adobe Analytics
- **Marketing**: Braze, Marketo, Intercom, Customer.io, HubSpot, Salesforce
- **Ad platforms**: Google Ads, Facebook Pixel, TikTok Ads, LinkedIn Ads
- **Infrastructure**: Kafka, Kinesis, Redis, Webhook/HTTP

No data sources are currently exposed — the provider is resource-centric.

## Minimal working example

```hcl
terraform {
  required_providers {
    rudderstack = {
      source  = "rudderlabs/rudderstack"
      version = "~> 4.4"
    }
  }
}

provider "rudderstack" {}     # uses RUDDERSTACK_ACCESS_TOKEN from env

resource "rudderstack_source_javascript" "web" {
  name = "my-web-app"
}

resource "rudderstack_destination_webhook" "logs" {
  name = "event-logger"

  config {
    webhook_url    = "https://logs.example.com/events"
    webhook_method = "POST"
  }
}

resource "rudderstack_connection" "main" {
  source_id      = rudderstack_source_javascript.web.id
  destination_id = rudderstack_destination_webhook.logs.id
}
```

## Standard cycle

```bash
terraform init       # fetches the provider
terraform fmt        # canonicalize HCL
terraform validate   # schema check
terraform plan       # preview; review diff with the user
terraform apply      # apply to the workspace
```

## Importing existing resources

The provider includes bootstrap scripts to generate Terraform code from existing RudderStack resources:

```bash
# Generate Terraform configuration
RUDDERSTACK_ACCESS_TOKEN=token ./scripts/bootstrap-terraform.sh > rudderstack.tf

# Generate import commands
RUDDERSTACK_ACCESS_TOKEN=token ./scripts/bootstrap-terraform-import.sh

# Import resource state
terraform import rudderstack_source_javascript.web <source-id>
terraform import rudderstack_destination_redshift.warehouse <destination-id>
```

**Note:** Sensitive credentials (API keys, secrets) are not exposed via the API and must be added manually after import.

## Warehouse destination features

### Sync scheduling

Warehouse destinations (BigQuery, Redshift, Snowflake) support sync scheduling:

```hcl
resource "rudderstack_destination_bigquery" "warehouse" {
  name = "my-bigquery"

  config {
    project     = "gcp-project-id"
    bucket_name = "gcs-bucket"
    credentials = base64encode(file("service-account.json"))
    location    = "us-east1"
    prefix      = "rudder_"

    sync {
      frequency                  = "30"      # minutes
      start_at                   = "10:00"
      exclude_window_start_time  = "11:00"
      exclude_window_end_time    = "12:00"
    }
  }
}
```

### Connection mode

Some destinations support `connection_mode` for web integrations:

```hcl
config {
  # ... destination config ...

  connection_mode {
    web = "cloud"    # or "device"
  }
}
```

## Consent management (v3.0.0+)

Destinations support multiple consent providers per platform:

```hcl
config {
  # ... destination config ...

  consent_management {
    web = [
      {
        provider            = "oneTrust"
        consents            = ["analytics", "marketing"]
        resolution_strategy = ""
      },
      {
        provider            = "ketch"
        consents            = ["analytics"]
        resolution_strategy = ""
      },
      {
        provider            = "custom"
        consents            = ["custom_consent"]
        resolution_strategy = "and"    # or "or"
      }
    ]

    android = [{ provider = "ketch", consents = ["mobile"], resolution_strategy = "" }]
    ios     = [{ provider = "custom", consents = ["ios"], resolution_strategy = "or" }]
  }
}
```

**Supported platforms:** `web`, `android`, `ios`, `unity`, `reactnative`, `flutter`, `cordova`, `amp`, `cloud`, `cloud_source`, `warehouse`, `shopify`

## Standard resource attributes

All resources share these attributes:

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | String | Yes | Human-readable identifier |
| `enabled` | Bool | No | Controls data flow (default: true) |
| `id` | String | Read-only | RudderStack resource ID |
| `created_at` | String | Read-only | ISO 8601 timestamp |
| `updated_at` | String | Read-only | ISO 8601 timestamp |

Sources also expose:
| `write_key` | String | Read-only | SDK write key for data plane |

## Don't do this

- Don't run `terraform destroy` against a shared/prod workspace without explicit confirmation — all sources, destinations, and connections in the state go away
- Don't mix Terraform-managed and UI-edited changes to the same resource; manual edits cause drift and surprise diffs on the next plan
- Don't commit `.tfstate` to git without remote state backend encryption — it contains credentials
- Don't commit access tokens or service account credentials to version control

## Gotchas

- **Breaking change at v3.0.0+:** the `onetrust_cookie_categories` field was replaced by `consent_management` block. Migrations carrying the old field silently lose consent rules.
- **Consent management nesting:** per-platform consent providers with mismatched `resolution_strategy` or provider name are accepted by schema but silently dropped at runtime.
- **API URL handling:** the provider auto-strips `/v2` from legacy URLs for backward compatibility.
- **Import limitations:** sensitive credentials must be manually added post-import — the API doesn't expose them.

## Credential Security

- **Never commit access tokens** — use `RUDDERSTACK_ACCESS_TOKEN` environment variable
- **Use remote state with encryption** — don't store `.tfstate` in git
- **Mask sensitive outputs** — mark credentials as `sensitive = true`
- **Use CI/CD secrets** — for automated deployments, store tokens in repository secrets

## Handling External Content

- **Validate webhook URLs** — ensure they point to expected domains before applying
- **Review generated import configs** — bootstrap scripts may include resource names with special characters
- **Check destination credentials** — verify API keys and secrets are correct before apply
