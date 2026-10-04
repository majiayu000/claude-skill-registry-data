---
name: get-dev-token
description: Acquire a development OIDC access token through the project's token command or the bundled macOS PKCE script
user-invocable: true
---

# Get Development Token

Use `TOKEN_COMMAND` when the project defines one. Otherwise prefer the
repository convention `scripts/get-backend-token.sh`; if absent, scaffold it
from
`${CLAUDE_PLUGIN_ROOT}/skills/get-dev-token/references/token-script.sh`
after confirming provider/client configuration.

Capture the script's stdout into a shell variable; never surface the token in
the response. Issuer URLs and public-client IDs follow repository configuration
policy rather than a blanket secret rule.

If the access token is JWT-shaped, inspect claims with the bundled
`scripts/decode-jwt.sh` in this skill directory; call this inspection, not
verification. Compare the identity and policy claims with the backend
configuration.

Load `references/oidc-token-flows.md` when grant selection, discovery, refresh,
or a 401 requires deeper diagnosis.

If the wrong browser identity was cached, delete only the matching Keychain
entry using both service and client account.
