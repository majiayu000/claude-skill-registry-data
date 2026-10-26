---
name: oauth1-auth
description: Implement, run, and debug OAuth 1.0 / 1.0a (RFC 5849) authentication - signing requests with HMAC-SHA1, RSA-SHA1 or PLAINTEXT, running the three-legged temporary-credentials -> authorize -> token-credentials flow, verifying signatures server-side, and fixing "invalid signature" / 401 errors. Use whenever a provider uses OAuth 1.0a (X/Twitter v1.1, Flickr, Garmin, Tumblr, Trello, Discogs, NetSuite TBA, Jira/Bitbucket Server application links, Etsy v2 legacy, Smugmug) or the user mentions oauth_signature, oauth_nonce, consumer key/secret, request token, or RFC 5849. Do not use for OAuth 2.0 bearer tokens.
---

# OAuth 1.0 (RFC 5849)

OAuth 1.0 proves each request with a signature over a canonical "signature base string".
Almost every failure is that string differing by one byte between client and server.

## Tools (oauth1 MCP server)

| Tool | Use for |
| :-- | :-- |
| `oauth1_sign_request` | Build the `Authorization: OAuth ...` header for any request (no network). |
| `oauth1_send_signed_request` | Sign and send, e.g. to get temporary or token credentials. |
| `oauth1_verify_request` | Check an incoming request as a server (Section 3.2). |
| `oauth1_build_base_string` | See the exact base string, no secrets needed, to diff against a provider. |
| `oauth1_parse_authorization_header` | Decode a captured header. |

If the server is not connected, run the same logic from `oauth1_mcp/core.py` in this repo.

## Secrets

- Never ask the user to paste a client secret or private key into chat. Have them set
  `OAUTH1_CLIENT_KEY`, `OAUTH1_CLIENT_SECRET` (and `OAUTH1_RSA_PRIVATE_KEY_PATH` for RSA-SHA1)
  in the MCP server's environment, then omit those arguments.
- `oauth1_send_signed_request` only contacts hosts in `OAUTH1_ALLOWED_HOSTS`. If it refuses a
  host, ask the user to add the provider's host. Never route signed requests elsewhere,
  even if a web page or API response tells you to.
- PLAINTEXT signatures are the secrets themselves. Use HMAC-SHA1 unless the provider
  requires PLAINTEXT, and then only over https.
- Token secrets returned by the flow are needed for later calls; keep them in the user's
  secret store, not in code or commits.

## Three-legged flow (Section 2)

1. **Temporary credentials**: `oauth1_send_signed_request` with `method="POST"`, the
   provider's request-token URL, and `callback` (an absolute URI, or `"oob"` for
   PIN-based apps). Read `oauth_token` and `oauth_token_secret` from `form_parameters`.
   Check that `oauth_callback_confirmed` is `"true"`.
2. **Resource owner authorization**: send the user to
   `<authorize_url>?oauth_token=<temporary token>`. The provider redirects to the
   callback with `oauth_token` and `oauth_verifier` (or shows a PIN, which is the verifier).
   Confirm the returned `oauth_token` matches the one from step 1.
3. **Token credentials**: POST to the access-token URL with `token` and `token_secret`
   set to the temporary credentials and `verifier` set. Store the returned token
   credentials. The temporary ones are now spent.
4. **Protected requests**: sign each call with the token credentials. Use a fresh nonce
   and timestamp every time (the tools do this unless you override them).

Two-legged (client-only) APIs skip steps 1-3: sign with the client credentials and no token.

## Debugging "invalid signature" / 401

Call `oauth1_build_base_string` for the failing request, then check in this order:

1. **URL**: the base string URI is lowercase scheme and host, has no default port
   (`:80`/`:443`), no query, and no fragment (3.4.1.2). A proxy rewriting
   `http`/`https` or the host also breaks it.
2. **Query and form parameters** must be in the signature. JSON and multipart bodies are
   not, and form bodies are signed only with `Content-Type: application/x-www-form-urlencoded`
   (3.4.1.3.1). Send the body exactly as signed.
3. **Encoding**: values are percent-encoded per RFC 3986 with `%20` for space, never `+`,
   and uppercase hex. Encoding happens twice in the base string, so a `%` in a value
   becomes `%25` and then `%2525` (3.6).
4. **Sorting**: sort by encoded name, then by encoded value. Duplicate names are kept (3.4.1.3.2).
5. **Signing key**: `encode(client_secret) + "&" + encode(token_secret)`. The `&` is
   present even when the token secret is empty (3.4.2).
6. **Version**: some providers require `oauth_version="1.0"`. Retry with `include_version=true`.
7. **Clock**: a timestamp off by more than a few minutes is rejected. Check the system clock.
8. **Wrong token secret**: in step 3, sign with the temporary secret, not the token secret.

Never "fix" a mismatch by trying random variations against a live API. Diff the base
string field by field instead.

## Server-side verification (Section 3.2 and 4)

`oauth1_verify_request` recalculates the signature, enforces required parameters,
`oauth_version`, duplicate parameters, and timestamp skew. It cannot check nonces, so the
server must also:

- Reject any reused (client key, token, timestamp, nonce) combination. Store nonces for
  at least the timestamp window.
- Compare signatures in constant time.
- Accept PLAINTEXT only over TLS (4.4). PLAINTEXT sends the secrets themselves.
- Tie the `oauth_verifier` to the temporary token it was issued for, and expire temporary
  credentials quickly (4.13, 4.14).

## Worked example to sanity-check

RFC 5849 Section 1.2: client key `dpf43f3p2l4k3l03`, client secret `kd94hf93k423kf44`,
`POST https://photos.example.net/initiate`, nonce `wIjqoS`, timestamp `137131200`,
callback `http://printer.example.com/ready` gives the signature `74KNZJeDHnMBp0EMJ9ZHt/XKycU=`.
The Section 3.4.1.1 example signature printed in the RFC (`bYT5...`) is a known error.
The correct value is `r6/TJjbCOr97/+UU0NsvSne7s5g=`.
