---
name: license-impl
description: Use when implementing any part of the Cortex Notes license/KeyGen system. Loads full plan context, phase checklist, and implementation rules specific to the license feature.
---

# License Implementation Skill

**Always read `docs/LICENSE_PLAN.md` before writing any code.** It is the authoritative source for schemas, IPC contracts, phase scope, and security decisions.

---

## Quick Reference

### New files for this feature
| File | Layer | Purpose |
|------|-------|---------|
| `cortex-keygen/keygen.js` | CLI tool (separate) | Generate Ed25519 keypair, sign + issue licenses |
| `main/machine-id.js` | Main process | SHA-256 hardware fingerprint |
| `main/license-validator.js` | Main process | Verify signature, check expiry, grace period |
| `renderer/index.html` | HTML | `#license-modal`, `#trial-banner`, license settings tab content |
| `renderer/app.js` | Renderer | `state.license`, `licenseGate()`, activation flow, trial banner render |
| `renderer/styles.css` | Styles | License modal, trial banner, feature-lock overlay |

### IPC channels to add in `main/main.js` and `main/preload.js`
```js
'license:status'     // → { status, tier, daysLeft, features, customerName, expiresAt }
'license:activate'   // payload: { key } → { success, data: licenseState }
'license:deactivate' // → { success }
'license:openPortal' // → opens shell.openExternal to purchase URL
```

### `state.license` shape (init in state object)
```js
license: {
  status: 'trial',        // 'trial'|'licensed'|'expired'|'invalid'|'grace'
  tier: 'trial',          // 'trial'|'personal'|'pro'|'team'
  daysLeft: 14,
  features: [],           // ['ai','backup','encryption','unlimited']
  customerName: '',
  expiresAt: null,
  licenseId: null,
}
```

### Feature gate pattern
```js
function licenseGate(feature) {
  return state.license.features.includes(feature);
}
// Usage: if (!licenseGate('ai')) { showUpgradePrompt('ai'); return; }
```

### Dependency
```
npm install @noble/ed25519
```
`@noble/ed25519` — audited pure-JS Ed25519 implementation. Works in Node (main process) and browser (renderer for client-side pre-validation). No native bindings needed.

---

## Phase Checklist

### Phase 1 — Offline skeleton
- [ ] `cortex-keygen/keygen.js` — `generate-keypair` and `issue` commands
- [ ] `main/machine-id.js` — fingerprint function exported
- [ ] `main/license-validator.js` — `validateLicense()`, `getTrialState()`, `loadLicenseFile()`
- [ ] `main/main.js` — add `license:status`, `license:activate` handlers
- [ ] `main/preload.js` — expose `window.noteflow.license.*`
- [ ] `renderer/app.js` — `state.license` init, load on startup, `openActivationModal()`
- [ ] `renderer/index.html` — `#license-modal`, `#trial-banner`
- [ ] `renderer/styles.css` — modal + banner styles
- [ ] Settings tab: License section

### Phase 2 — Feature gating
- [ ] `licenseGate(feature)` in renderer
- [ ] AI Chat gated behind `ai`
- [ ] Backup gated behind `backup`
- [ ] Encryption (note lock) gated behind `encryption`
- [ ] 50-note cap on Trial (gate `unlimited`)
- [ ] Feature-lock overlay component

### Phase 3 — Online activation
- [ ] Activation server deployed (Cloudflare Workers / Vercel)
- [ ] `license:activate` wired to `POST /api/v1/activate`
- [ ] Background heartbeat (non-blocking, `setInterval` in main process)
- [ ] `license:deactivate` wired to `POST /api/v1/deactivate`
- [ ] Grace period countdown written to `license.json`

### Phase 4 — Polish
- [ ] Key input auto-format (dashes + uppercase)
- [ ] Windows URI handler `cortex://activate?key=...`
- [ ] In-app purchase link
- [ ] Deep-link handler in `main/main.js`

---

## Security Rules (Non-Negotiable)

1. **Private key never leaves the keygen tool.** Never embed it in the app.
2. **`license.json` is AES-256-GCM encrypted** using `machineId` as the key — never plaintext.
3. **Always verify the Ed25519 signature before trusting any payload field.**
4. **Never trust `status` from renderer state alone** for security decisions — re-read from validator in main process.
5. **Atomic write** for `license.json` — `.tmp` → `fs.renameSync` pattern (same as all other data files).

---

## Key Format

```
CORTEX-A1B2C-D3E4F-G5H6I-J7K8L
```

Decodes to: `base64url(payload_json) + '.' + base64url(ed25519_signature)`

Payload required fields: `id`, `product`, `version`, `type`, `seats`, `issued_at`, `features[]`, `customer.email`

---

## Machine Fingerprint

```js
// main/machine-id.js
const inputs = [
  os.hostname(),
  os.cpus()[0]?.model ?? '',
  firstNonLoopbackMAC(),  // os.networkInterfaces()
  process.env.USERPROFILE ?? process.env.HOME ?? '',
].join('|');
return crypto.createHash('sha256').update(inputs).digest('hex');
```

Hamming-distance tolerance of 1 character handles minor hardware changes (RAM upgrade, NIC change) without requiring re-activation.

---

## Trial State

Stored in `settings.json` under `trial` key (backward-compatible addition):

```json
{
  "trial": {
    "startedAt": "ISO8601",
    "notesCreated": 0
  }
}
```

Trial expires 14 days after `startedAt`. Note cap is 50 (`notesCreated >= 50` blocks new note creation with upgrade prompt).
