---
name: poc-tier
description: Classify PoC file quality as Tier 1-4. Run after exploiter completes, before triager-sim. Matches "PoC tier", "PoC quality", "poc quality", "exploit verify"
user-invocable: true
argument-hint: <poc-file-path>
allowed-tools: [Read, Bash, Grep]
---

# PoC Quality Tier Classification

## CRITICAL RULES (NEVER VIOLATE)
1. **Tier 3-4 = submission FORBIDDEN** — PoC without execution evidence is 100% Informative
2. **No real network call + response capture = cannot be Tier 1** — local mock = Bronze at best

Automatically classifies PoC quality as Tier 1-4.
Prevents Tier 3-4 submission failures (Veda, Katana, etc. — 4 failures).

## Input
- `$ARGUMENTS`: PoC file path (e.g., `evidence/ssrf/poc.py`, `poc/foundry-test/test/Exploit.t.sol`)

## Tier Definitions

| Tier | Name | Requirements | Outcome |
|------|------|-------------|---------|
| **1** | Gold | Runtime verified + integration test + evidence capture + UA fingerprint | ACCEPT (high confidence) |
| **2** | Silver | Executable script + output capture, no integration test | ACCEPT (moderate confidence) |
| **3** | Bronze | Script exists but output is theoretical/mock | **DROPPED — submission forbidden** |
| **4** | Reject | No PoC, pseudocode only, "left as exercise" | **DROPPED — submission forbidden** |

## Few-Shot Examples

### Tier 1 (Gold) — Real API call + response capture + assertion
```python
resp = requests.get(f"{BASE}/api/users/2", headers={"Authorization": f"Bearer {token_user1}"})
assert resp.status_code == 200
data = resp.json()
assert "email" in data  # user1 can read user2's PII
print(f"[VULN] Cross-user data: {data['email']}")  # captured in output.txt
```

### Tier 3 (Bronze) — Script exists but mock output
```python
# This should work against the production API
url = "https://example.com/api/admin"  # placeholder
# TODO: replace with actual target URL
resp = requests.get(url)  # hypothetical response would contain admin data
print("Exploitation successful")  # no actual evidence
```

## Procedure

### Step 1: Read PoC File
```
Read $ARGUMENTS
```

### Step 2: Positive Signal Detection (+1 tier each)

**Network calls present**:
!`grep -cE "requests\.|fetch\(|curl |remote\(|cast send|cast call|axios\.|http\.|urllib" "$ARGUMENTS" 2>/dev/null || echo "0"`

**Real response capture present**:
!`grep -cE "response\.|status_code|\.json\(\)|recvline|recvuntil|interactive|200 OK|HTTP/" "$ARGUMENTS" 2>/dev/null || echo "0"`

**Test framework usage**:
!`grep -cE "forge test|npm test|pytest|unittest|assert|vm\.expect|console\.log" "$ARGUMENTS" 2>/dev/null || echo "0"`

### Step 3: Negative Signal Detection (-1 tier each)

**Incomplete markers**:
!`grep -ciE "TODO|FIXME|theoretical|hypothetical|would work|should work|left as exercise|mock|placeholder" "$ARGUMENTS" 2>/dev/null || echo "0"`

**Hardcoded mock data**:
!`grep -cE "fake_|mock_|dummy_|example\.com|0xdead|placeholder" "$ARGUMENTS" 2>/dev/null || echo "0"`

**Commented-out core logic**:
!`grep -cE "^#.*exploit|^#.*send|^#.*remote|^//.*attack" "$ARGUMENTS" 2>/dev/null || echo "0"`

### Step 4: Tier Calculation
```
base_tier = 2  (Silver default)

# Positive signals
if network_calls == 0: tier += 1  (Silver→Bronze)
if response_capture > 0: tier -= 1  (can upgrade)
if test_framework > 0: tier -= 0.5

# Negative signals
if incomplete_markers > 0: tier += 1
if mock_data > 2: tier += 1
if commented_out > 0: tier += 1

tier = clamp(tier, 1, 4)
```

### Step 5: Output
```
[POC-TIER] File: <path>
[POC-TIER] Positive signals: network_calls=N, response_capture=N, test_framework=N
[POC-TIER] Negative signals: incomplete=N, mock_data=N, commented_out=N
[POC-TIER] Tier: N (<name>)
[POC-TIER] Result: PASS (Tier 1-2) / BLOCK (Tier 3-4, submission forbidden)
```

### BLOCK Actions
- **Tier 3**: "Script exists but no execution evidence. Run it and capture output.txt"
- **Tier 4**: "No PoC. Write exploit code first. Theoretical descriptions are 100% Informative"

## DeFi PoC Extra Checks
- `vm.deal()` used + no honest disclosure → downgrade to Tier 3
- `fork-url` + real block number → Tier 1 signal
- `assert` proving profit → Tier 1 signal

> **REMINDER**: Tier 3-4 = NEVER submit. Only Tier 1-2 pass to triager-sim.
