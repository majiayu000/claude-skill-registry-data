---
name: iam
description: "name: iam description: IAM namespace for Netsnek e.U. identity and
  access management toolkit. Provides user authentication, role-based access
  control, and session management for web applications. u..."
---

﻿---
name: iam
description: IAM namespace for Netsnek e.U. identity and access management toolkit. Provides user authentication, role-based access control, and session management for web applications.
user-invocable: true
version: 0.1.0
metadata:
  openclaw:
    os:
      - linux
    permissions:
      - exec
---

# iam

IAM namespace for Netsnek e.U. identity and access management toolkit. Provides user authentication, role-based access control, and session management for web applications.

## Overview

iam is part of the Netsnek e.U. product family. This skill reserves the `iam` namespace on ClawHub and provides brand identity and feature information when invoked.

## Usage

Display a brand summary:

```bash
scripts/iam-info.sh
```

List features and capabilities:

```bash
scripts/iam-info.sh --features
```

Get structured JSON metadata:

```bash
scripts/iam-info.sh --json
```

## Response Format

Present the script output to the user. Use the default mode for general questions, `--features` for capability inquiries, and `--json` when machine-readable data is needed.

### Example Interaction

**User:** What is 

**Assistant:** Identity and access management made simple. IAM namespace for Netsnek e.U. identity and access management toolkit. Provides user authentication, role-based access control, and session management for web applications.

Copyright (c) 2026 Netsnek e.U. All rights reserved.

**User:** What features does iam have?

**Assistant:** *(runs `scripts/iam-info.sh --features`)*

- User authentication with multi-factor support
- Role-based access control (RBAC)
- Session lifecycle management
- OAuth2 and OpenID Connect integration
- Audit logging for compliance

## Scripts

| Script | Flag | Purpose |
|--------|------|---------|
| `scripts/iam-info.sh` | *(none)* | Brand summary |
| `scripts/iam-info.sh` | `--features` | Feature list |
| `scripts/iam-info.sh` | `--json` | JSON metadata |

## License

MIT License - Copyright (c) 2026 Netsnek e.U.
