---
name: rails-encryption-credentials-engineering
description: Design and review Rails credentials, secret storage, key management, application-level encryption, rotation, migration, and secret-safe operational boundaries.
license: MIT
---
# Rails Encryption and Credentials Engineering

## Purpose
Use this skill when a Rails application stores, retrieves, encrypts, rotates, migrates, or operationalizes secrets or sensitive persisted data. Treat credentials, cryptographic keys, encrypted database attributes, cookies, logs, and deployment configuration as distinct security boundaries.

## Activate when
Activate for config/credentials.yml.enc, environment-specific credentials files, config/master.key, RAILS_MASTER_KEY, bin/rails credentials:edit, bin/rails credentials:show, rails credentials:fetch, secret_key_base, Active Record Encryption, encrypts, deterministic encryption, encrypted migrations, key rotation, encrypted fixtures, parameter filtering, secret rotation, or production secret injection.

## Core contract
Keep secret material out of source code and ordinary logs. Separate credential storage from runtime secret delivery, and separate application configuration secrets from data-at-rest encryption keys. Use the repository's actual Rails/Ruby version before choosing APIs. Prefer Rails-supported credential and encryption mechanisms when they fit the threat model. Do not claim encryption provides authorization, deletion, or compliance by itself.

## Repository inspection
Resolve Ruby, Rails, Active Record, and deployment versions. Inspect credential files and key paths, environment-specific credential conventions, config.require_master_key, secret_key_base ownership, deployment secret injection, logging/filtering configuration, models using encrypted attributes, migrations, fixtures, background jobs, data exports, and backup/restore procedures. Inspect whether the application supports key rotation and how incidents revoke or replace compromised secrets.

## Credential stores and environment selection
Rails supports encrypted credentials and can select environment-specific credentials paths. Current Rails configuration defaults to config/credentials/#{Rails.env}.yml.enc when present, otherwise config/credentials.yml.enc; key selection similarly prefers config/credentials/#{Rails.env}.key and otherwise config/master.key. Make the chosen environment and key path explicit when customizing them. [Rails Configuring Applications guide](https://guides.rubyonrails.org/configuring.html)

## Master-key boundary
The encrypted credentials file may be version-controlled because it is encrypted, but the decryption key must remain outside the repository's ordinary source distribution. Rails accepts the configured key path and can use RAILS_MASTER_KEY. Production boot requirements must be explicit; config.require_master_key can fail closed when credentials are required. 

## Secret lifecycle
Treat generation, distribution, consumption, rotation, revocation, and destruction as separate operations. Document who/what can read a secret, where it is injected, how rotation overlaps old/new values, and how dependent services observe the change. Never print secret material while debugging.

## Application-level encryption
Active Record Encryption encrypts declared model attributes transparently and supports non-deterministic and deterministic schemes. Non-deterministic encryption is the default and is preferable unless equality querying requires deterministic encryption. Deterministic encryption trades some security properties for queryability.

## Key management
Rails Active Record Encryption can be initialized with generated keys stored in credentials or another secure runtime source. Keep primary, deterministic, and key-derivation-salt material in the intended secret store. Custom key providers and envelope-encryption designs require explicit threat-model and lifecycle review.

## Storage and query implications
Encrypted attributes have storage overhead and can change indexing/query semantics. Review column sizing, deterministic query requirements, unique validations/indexes, ordering, search behavior, exports, and data repair procedures before encrypting an existing field. Rails documents that encrypted payloads carry metadata and Base64 encoding overhead.

## Migration and rotation
For existing plaintext data, use an expand/transform/verify/cutover strategy. Never irreversibly encrypt data without a verified recovery path and backup/restore evidence. When changing encryption schemes or keys, support old data during transition when the Rails capability and threat model justify it, then retire old material deliberately.

## Secret-safe observability
Use parameter and attribute filtering for secrets and encrypted values. Review structured logs, exceptions, tracing, SQL logs, job arguments, admin consoles, metrics labels, exports, and support tooling. Rails documents filtering of sensitive parameters and encrypted Active Record values.

## Testing strategy
Test credential loading without exposing values, missing-key failure behavior, environment selection, encrypted attribute round trips, deterministic query behavior where required, migrations, rotation compatibility, parameter filtering, and production-like boot. Use fixtures and test secrets that cannot be mistaken for production material.

## Anti-patterns / failure modes
Avoid plaintext secrets in Git, credentials committed with key files, secret values in logs, one global key for unrelated security domains, deterministic encryption by default when querying is unnecessary, encrypted columns with unreviewed size/index behavior, irreversible bulk encryption without recovery evidence, environment ambiguity, hard-coded secret fallbacks, and tests that assert or print real secret material.

## Reference example

Reading encrypted credentials through a narrow accessor, never scattering Rails.application.credentials through the codebase.

```ruby
# config/credentials.yml.enc (edited via: bin/rails credentials:edit)
#   billing:
#     api_key: ...
#     endpoint: https://api.example.com

class Billing
  def self.api_key
    Rails.application.credentials.dig(:billing, :api_key) or
      raise MissingCredentialError, "billing.api_key not configured for #{Rails.env}"
  end
end

# Per-environment key selection is automatic (config/credentials/#{Rails.env}.yml.enc
# when present), and the decryption key never enters the repository.
# Local development without a key must fail loudly, not silently fall back.
```

## Agent review checklist
- [ ] Rails/Ruby version resolved
- [ ] credential store and key path explicit
- [ ] environment selection explicit
- [ ] master-key delivery reviewed
- [ ] secret_key_base ownership reviewed
- [ ] runtime secret source reviewed
- [ ] encrypted attributes and query requirements reviewed
- [ ] key lifecycle/rotation plan explicit
- [ ] migration and recovery path verified
- [ ] logs/traces/SQL/jobs filtered
- [ ] tests avoid real secrets
- [ ] production-like boot or integration evidence exists

## Verification
Resolve versions -> identify secret/encryption boundary -> inspect storage and runtime delivery -> select Rails-supported mechanism -> define lifecycle and rotation semantics -> test failure and recovery paths -> verify filtering -> run repository validation -> inspect CI evidence. Do not claim a secret is secure merely because it is encrypted at rest.

## Rails 8.1 current framework considerations

- Rails 8.1 supports command-line credential fetching, such as `rails credentials:fetch`, for deploy-time integrations.
- Keep credential lookup within the encrypted credentials boundary and verify that command output, shell environment handling, and logging do not expose secret values.

## Source foundation
- https://guides.rubyonrails.org/active_record_encryption.html
- https://guides.rubyonrails.org/security.html
- https://guides.rubyonrails.org/configuring.html
- https://api.rubyonrails.org/classes/ActiveRecord/Encryption.html

## Rails encryption/credentials changes

For credentials, secret, cryptographic key, or Active Record Encryption changes:
- resolve Ruby/Rails/Active Record versions first;
- identify whether the value is application configuration, a deployment secret, a Rails master key, a cryptographic data-encryption key, or persisted sensitive data;
- choose an explicit approved secret store and separate ciphertext from decryption keys;
- inspect config.credentials.content_path and config.credentials.key_path when environment-specific credentials are involved;
- keep config/master.key and equivalent key material outside ordinary source distribution;
- make RAILS_MASTER_KEY or the repository's runtime secret injection mechanism explicit and verify production boot behavior;
- treat secret_key_base as a foundational cryptographic secret and review session/cookie/Active Storage impact before rotation;
- use Active Record Encryption only with explicit attribute, key, query, storage, and migration contracts;
- use deterministic encryption only when equality querying/uniqueness requires it and document the security tradeoff;
- review encrypted column sizing, indexes, validations, exports, backups, and operational tooling;
- design data migrations and key rotations as resumable, observable, recoverable transitions;
- filter parameters, model inspection, SQL, job arguments, traces, and exception output that can expose sensitive values;
- use synthetic secrets in tests and never print real credentials;
- verify missing-key and failure-closed behavior in production-like environments;
- do not claim security from encryption alone: access control, key custody, logging, backup, rotation, and recovery remain separate contracts.
