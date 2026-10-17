---
name: rails-active-storage
description: "Use when designing, implementing, reviewing, testing, or operating Rails Active Storage attachments, uploads, direct uploads, storage services, file serving, variants, previews, analysis, purge lifecycle, mirrors, or file-access security."
license: MIT
---

# Rails Active Storage Engineering

## Purpose

Treat uploaded files as a durable external-data boundary, not merely as another Active Record attribute.

Active Storage spans:

- database attachment metadata;
- object storage;
- browser-to-storage uploads;
- file serving/downloads;
- authorization and tenant isolation;
- content analysis;
- transformations and previews;
- background processing;
- cleanup/purge;
- storage migration and replication;
- testing.

Core flow:

```text
define file ownership
-> define allowed file contract
-> choose storage service
-> attach/persist relationship
-> authorize upload/access
-> upload/analyze/transform
-> serve safely
-> observe failures
-> purge/reconcile
```

The Rails Active Storage guide documents attachment macros, storage services, private/public access, direct uploads, analysis, variants/previews, testing, mirrors, and purging unattached uploads. See the source foundation below.

## Activate when

- adding `has_one_attached` or `has_many_attached`;
- changing file upload or attachment flows;
- configuring `config/storage.yml` or environment-specific storage;
- adding S3/GCS/Azure/S3-compatible object storage;
- implementing direct uploads;
- serving or downloading private files;
- adding public file access;
- adding authenticated file controllers;
- adding image/video/PDF variants or previews;
- changing analyzers or content metadata;
- adding file validation;
- implementing attachment cleanup or purge;
- migrating storage providers;
- introducing storage mirrors;
- diagnosing missing, inaccessible, duplicated, orphaned, or slow file operations;
- reviewing upload security or tenant isolation.

Do not activate merely because a model has a normal database attachment URL unrelated to Active Storage. Use the smallest relevant Rails/view/API/security skill when Active Storage is not actually involved.

## Repository inspection

Inspect before changing file behavior:

1. Ruby/Rails version and Active Storage APIs available in that version;
2. existing `has_one_attached` / `has_many_attached` declarations;
3. `config/storage.yml` and environment-specific storage configuration;
4. active storage migrations/schema;
5. object storage provider gems and credentials;
6. direct-upload JavaScript and CORS configuration;
7. routes and Active Storage route configuration;
8. authentication and authorization around file access;
9. tenant/resource ownership rules;
10. upload parameters and strong-parameter conventions;
11. file validations and content-type/size policy;
12. analyzers, variants, previews, and processing jobs;
13. purge jobs or cleanup schedules;
14. CDN/proxy/redirect behavior;
15. logging, metrics, error reporting, and provider telemetry;
16. tests using the Active Storage test service and fixtures;
17. deployment/runtime permissions, buckets, lifecycle policies, and secret configuration.

Do not introduce a second storage abstraction when repository conventions already define one.

## Decision rules

1. Classify the change: attachment/schema contract, upload authorization or tenancy, storage service and provider, direct upload and validation, serving and downloads, processing, replacement/purge lifecycle, or observability and testing.
2. Load the matching reference below before changing behavior; a direct-upload change usually needs both the upload and the authorization reference.
3. Treat the uploaded file as untrusted data and every blob identifier as an object reference that still needs authorization at the owning resource.

## Critical invariants

- Never interpret possession of a signed blob ID as proof that the caller owns the target resource.
- Never switch private storage to public as a debugging shortcut.
- Do not retry every storage error blindly.
- Never claim storage durability, complete replication, or successful migration without provider/runtime evidence.

## References

Load only the reference for the boundary being changed, before changing behavior there. Each reference is self-contained and one level deep; none links to another. Consult a listed pattern from the pattern catalog only when the change needs its implementation shape.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| a change declares or alters attachments, cardinality, Active Storage tables, or the accepted file contract | [references/attachments-and-file-contract.md](references/attachments-and-file-contract.md) | Attachment boundary; Active Storage schema ownership; File contract | `active-storage-boundary` |
| a change decides who may upload, attach, or read a blob, or crosses tenants | [references/authorization-and-tenancy.md](references/authorization-and-tenancy.md) | Upload authorization; Tenant isolation | `active-storage-upload-security` |
| a change alters storage services, environments, provider credentials, failure handling, mirrors, or CDN/proxy delivery | [references/storage-services.md](references/storage-services.md) | Storage service selection; Environment separation; Provider boundary; Storage failure semantics; Storage migration and mirrors; CDN and proxy | none |
| a change adds or alters direct uploads, CORS, file validation, filenames, or metadata | [references/uploads-and-validation.md](references/uploads-and-validation.md) | Direct uploads; Direct-upload lifecycle; CORS; File validation; Filenames and metadata | `active-storage-direct-upload`, `active-storage-upload-security` |
| a change serves private or public files, adds file controllers, or downloads blobs into memory | [references/serving-and-downloads.md](references/serving-and-downloads.md) | Serving private files; Public files; Authenticated file controllers; Download and memory usage | `active-storage-serving` |
| a change alters analysis, variants, previews, processing dependencies, or processing jobs | [references/processing.md](references/processing.md) | Analysis; Variants and previews; Processing dependencies; Background processing | `active-storage-processing` |
| a change replaces, detaches, deletes, or purges attachments or cleans up unattached blobs | [references/replacement-and-purge.md](references/replacement-and-purge.md) | Replacement and deletion semantics; Purge lifecycle; Unattached and orphaned uploads | `active-storage-purge` |
| adding storage instrumentation or choosing and writing Active Storage tests | [references/observability-and-testing.md](references/observability-and-testing.md) | Observability; Testing | `active-storage-testing` |

## Reference example

One attachment with an explicit, validated file contract, served only after authorization.

```ruby
class Document < ApplicationRecord
  has_one_attached :file

  ALLOWED_TYPES = %w[application/pdf image/png].freeze
  MAX_BYTES = 25.megabytes

  validate :enforce_file_contract

  private

  def enforce_file_contract
    return unless file.attached?

    errors.add(:file, "exceeds 25 MB") if file.byte_size > MAX_BYTES
    errors.add(:file, "must be PDF or PNG") unless file.content_type.in?(ALLOWED_TYPES)
  end
end

class DocumentsController < ApplicationController
  def show
    document = current_account.documents.find(params[:id]) # authorize before serving bytes
    redirect_to document.file.url(disposition: :attachment)
  end
end

# Variants are processed on demand and cached; never inline-transform in a request:
#   document.file.variant(resize_to_limit: [800, 800]).processed.url
```

## Agent review checklist

- [ ] Active Storage/version semantics resolved
- [ ] attachment ownership/cardinality explicit
- [ ] upload authorization explicit
- [ ] tenant isolation reviewed
- [ ] file size/type/content policy explicit
- [ ] storage service/environment separation verified
- [ ] provider credentials protected
- [ ] direct-upload lifecycle reviewed
- [ ] CORS reviewed when applicable
- [ ] private/public access decision explicit
- [ ] authenticated download boundary verified when required
- [ ] signed URL exposure understood
- [ ] download memory/capacity reviewed
- [ ] analyzer/variant dependencies verified
- [ ] background processing semantics reviewed
- [ ] replacement/delete/purge semantics explicit
- [ ] unattached-upload cleanup bounded
- [ ] mirror/migration reconciliation verified when applicable
- [ ] CDN/proxy caching reviewed when applicable
- [ ] observability excludes secret/blob data
- [ ] focused Active Storage tests exist
- [ ] live provider dependency avoided in ordinary CI

## Anti-patterns / failure modes

- using a blob ID as authorization;
- exposing Active Storage default routes for tenant-private files;
- switching private storage to public to simplify access;
- trusting browser MIME type as a security control;
- executing or serving uploaded files as application code;
- loading huge files fully into Ruby memory;
- unbounded user-controlled transformations;
- synchronous cloud deletion on critical request paths without need;
- assuming analysis is complete immediately after upload;
- assuming attachment delete means physical object delete is already complete;
- blindly purging every unattached blob;
- treating mirror replication as atomic;
- leaking signed URLs into logs;
- granting storage credentials broader permissions than required;
- testing ordinary application behavior against a real cloud bucket;
- duplicating Active Storage provider SDK logic in domain models/controllers.

## Verification

For an upload feature:

```text
attachment contract
-> validation
-> authorization
-> storage configuration
-> focused attachment tests
-> direct-upload/serving tests where applicable
-> processing/background tests
-> security checks
-> regression suite
```

For storage migration:

```text
inventory
-> copy
-> reconcile
-> mirror/dual-read evidence when used
-> cutover
-> verify reads/writes
-> verify gaps
-> retire old provider
```

Never claim storage durability, complete replication, or successful migration without provider/runtime evidence.

## Source foundation

Primary Rails source:

- https://guides.rubyonrails.org/active_storage_overview.html
- https://api.rubyonrails.org/classes/ActiveStorage.html

Composed repository skills:

- `rails-security` skill
- `rails-security-engineering` skill
- `rails-active-job` skill
- `rails-api-integration` skill
- `rails-performance` skill
- `rails-caching` skill
- `rails-observability` skill
- `rails-production-runtime` skill
- `rails-test-engineering` skill
- `rails-test-engineering` skill

## Rails Active Storage changes

For Active Storage changes:
- inspect attachment declarations, domain ownership, tenant rules, storage configuration, routes, direct-upload code, processing jobs, purge behavior, and tests before implementation;
- treat the uploaded file as untrusted data and the blob identifier as an object reference, not as authorization;
- define attachment cardinality, replacement/additive semantics, validation, retention, and purge behavior explicitly;
- keep production storage services and credentials environment-isolated and least-privileged;
- treat browser direct uploads as a staged lifecycle: upload, attach to an authorized resource, process/analyze, then clean up unattached blobs;
- review CORS, file-size/content policy, signed URLs, default Active Storage routes, proxy/redirect mode, and authenticated access for private files;
- bound download memory, transformation CPU/memory, processing concurrency, and background retry behavior;
- distinguish logical attachment removal from physical object purge;
- reconcile storage migrations/mirrors rather than assuming replication is atomic;
- use the Active Storage test service and deterministic fixtures for ordinary CI; avoid live cloud-provider dependence;
- never claim storage durability, complete migration, replication completeness, or file delivery success without provider/runtime evidence.
