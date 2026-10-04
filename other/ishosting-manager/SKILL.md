---
name: ishosting-manager
description: Complete is*hosting infrastructure management via API. Order and configure VPS, Dedicated, Storage, VPN servers with custom hardware. Install OS, control panels, deploy apps and websites. Manage SSH keys, billing, invoices, DNS, and service lifecycle.
---

# [H1][ishosting-manager]
>**Dictum:** *Unified interface reduces API complexity.*

<br>

Complete is*hosting infrastructure management through Python API wrapper.

## Credentials

The script automatically searches for `.env` files in:
1. Current directory
2. Parent directory
3. `~/.config/ishosting/`

**Required environment variables:**
- `ISHOSTING_TOKEN` - Your API token
- `ISHOSTING_BASE_URL` - API base URL (**must use `https://`** — the script rejects `http://` to protect credentials)

**Optional environment variables:**
- `ISHOSTING_API_LANGUAGE` - API language (auto-detected, see below)
- `ISHOSTING_BASE_AUTH` - Basic auth credentials if needed

### [CRITICAL] Pre-flight credential check

**BEFORE running ANY ishosting command**, you MUST verify credentials exist. Follow this order:

**Step 1: Check for `.env` file in the project directory:**
```bash
cat .env 2>/dev/null || echo "NO_ENV_FILE"
```

**If `.env` exists and contains `ISHOSTING_TOKEN` and `ISHOSTING_BASE_URL`** → credentials are OK, proceed. The Python script loads `.env` automatically. Do NOT check shell environment variables — they are NOT set; the script reads `.env` directly.

**Step 2: If NO `.env` file found** → ASK the user to provide:
- `ISHOSTING_TOKEN` — API token
- `ISHOSTING_BASE_URL` — API base URL
- `ISHOSTING_BASE_AUTH` — Basic auth (optional)

**Step 3: When user provides credentials** → save them to `.env` in the project root:
```bash
cat > .env << 'EOF'
ISHOSTING_TOKEN=<token>
ISHOSTING_BASE_URL=<url>
ISHOSTING_BASE_AUTH=<auth>
EOF
chmod 600 .env
```

**Step 4: Ensure `.env` is in `.gitignore`** (prevents accidental credential commits):
```bash
grep -qxF '.env' .gitignore 2>/dev/null || echo '.env' >> .gitignore
```

This ensures credentials persist across sessions. Do NOT guess or invent credential values. Do NOT save `ISHOSTING_API_LANGUAGE` to `.env` — language is auto-detected from the user's messages via the `--lang` flag.

### Language auto-detection

The `--lang` flag controls the API response language. **Detect it automatically from the user's messages:**
- If the user writes in Russian (Cyrillic text), add `--lang ru` to every command
- Otherwise, omit it (defaults to `en`)

Example:
```bash
# User wrote in Russian
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-list --lang ru

# User wrote in English (or any other language)
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-list
```

Do NOT ask the user about language. Just detect it from their messages.

## Command defaults

[IMPORTANT] Zero-arg commands default to `page=1`, `limit=30`.

```bash
# Zero-arg commands
uv run .claude/skills/ishosting-manager/scripts/ishosting.py profile-view
uv run .claude/skills/ishosting-manager/scripts/ishosting.py services-list
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-list
```

## Python execution

**[CRITICAL]** Always use `uv run` for executing Python scripts, never plain `python3` or `python`.

```bash
# Correct - use uv run
uv run script.py

# Wrong - don't use plain python
python3 script.py  #
python script.py   #
```

---
## [0][INTERACTION MODEL]

**[CRITICAL]** This skill operates in a **step-by-step confirmation model**. Every user-facing question is a hard pause — the agent MUST stop and wait for an answer before doing anything else.

### STOP GATE — mandatory rule

Wherever you see **[STOP GATE]** in these instructions, you MUST:

1. Output your question or summary to the user
2. **Immediately end your response** — no further tool calls, no "proceeding...", no pre-emptive actions
3. **Wait for the user's next message** before continuing

**Why this matters:** Running multiple steps without confirmation can create orders, charges, or server deployments the user did not explicitly approve. Each STOP GATE protects the user from unintended actions.

**[FORBIDDEN]** After a STOP GATE, you MUST NOT:
- Call any tools (Bash, Read, etc.)
- Assume a default answer and proceed
- Say "I'll proceed with the default" or similar
- Combine the question with the next action in the same message

---
## [1][PROFILE]

```bash
uv run .claude/skills/ishosting-manager/scripts/ishosting.py profile-view
```

---
## [2][SETTINGS]

```bash
uv run .claude/skills/ishosting-manager/scripts/ishosting.py profile-settings-view
uv run .claude/skills/ishosting-manager/scripts/ishosting.py profile-settings-edit --firstname "John" --lastname "Doe" --phone "+1234567890"
uv run .claude/skills/ishosting-manager/scripts/ishosting.py ssh-key-view
uv run .claude/skills/ishosting-manager/scripts/ishosting.py ssh-key-create --title "SshKeyName" --public "PublicKey"
uv run .claude/skills/ishosting-manager/scripts/ishosting.py ssh-key-delete --id 1196440
```

---
## [3][SERVICES]

```bash
uv run .claude/skills/ishosting-manager/scripts/ishosting.py services-stats
uv run .claude/skills/ishosting-manager/scripts/ishosting.py services-list
```

---
## [4][VPS]

**Valid actions for `vps-status-change`:** `start`, `stop`, `reboot`, `force`, `cancel`

```bash
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-list
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-view --id 12345
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-edit --id 12345
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-status --id 12345
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-status-change --id 12345 --action start
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-status-change --id 12345 --action stop
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-status-change --id 12345 --action reboot
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-status-change --id 12345 --action force
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-status-change --id 12345 --action cancel
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-locations
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-plans --locations NL
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-plan-view --code vps-basic
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-configs --code vps-basic
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-ssh --id 12345
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-rdns-edit --id 12345 --protocol ipv4 --ip 1.2.3.4
```

---
## [5][STORAGE]

**Valid actions for `storage-status-change`:** `cancel`

```bash
uv run .claude/skills/ishosting-manager/scripts/ishosting.py storage-list
uv run .claude/skills/ishosting-manager/scripts/ishosting.py storage-view --id 12345
uv run .claude/skills/ishosting-manager/scripts/ishosting.py storage-edit --id 12345
uv run .claude/skills/ishosting-manager/scripts/ishosting.py storage-status --id 12345
uv run .claude/skills/ishosting-manager/scripts/ishosting.py storage-status-change --id 12345 --action cancel
uv run .claude/skills/ishosting-manager/scripts/ishosting.py storage-locations
uv run .claude/skills/ishosting-manager/scripts/ishosting.py storage-plans --locations US
uv run .claude/skills/ishosting-manager/scripts/ishosting.py storage-plan-view --code storage-basic
uv run .claude/skills/ishosting-manager/scripts/ishosting.py storage-configs --code storage-basic
uv run .claude/skills/ishosting-manager/scripts/ishosting.py storage-ssh --id 12345
```

---
## [6][DEDICATED]

**Valid actions for `dedicated-status-change`:** `start`, `stop`, `reboot`, `cancel`

```bash
uv run .claude/skills/ishosting-manager/scripts/ishosting.py dedicated-list
uv run .claude/skills/ishosting-manager/scripts/ishosting.py dedicated-view --id 12345
uv run .claude/skills/ishosting-manager/scripts/ishosting.py dedicated-edit --id 12345
uv run .claude/skills/ishosting-manager/scripts/ishosting.py dedicated-status --id 12345
uv run .claude/skills/ishosting-manager/scripts/ishosting.py dedicated-status-change --id 12345 --action start
uv run .claude/skills/ishosting-manager/scripts/ishosting.py dedicated-status-change --id 12345 --action stop
uv run .claude/skills/ishosting-manager/scripts/ishosting.py dedicated-status-change --id 12345 --action reboot
uv run .claude/skills/ishosting-manager/scripts/ishosting.py dedicated-status-change --id 12345 --action cancel
uv run .claude/skills/ishosting-manager/scripts/ishosting.py dedicated-locations
uv run .claude/skills/ishosting-manager/scripts/ishosting.py dedicated-plans --locations FI
uv run .claude/skills/ishosting-manager/scripts/ishosting.py dedicated-plans --locations FI --gpu true
uv run .claude/skills/ishosting-manager/scripts/ishosting.py dedicated-plan-view --code dedicated-basic
uv run .claude/skills/ishosting-manager/scripts/ishosting.py dedicated-configs --code dedicated-basic
uv run .claude/skills/ishosting-manager/scripts/ishosting.py dedicated-ssh --id 12345
uv run .claude/skills/ishosting-manager/scripts/ishosting.py dedicated-rdns-edit --id 12345 --protocol ipv4 --ip 1.2.3.4
```

---
## [7][VPN]

**Valid actions for `vpn-status-change`:** `start`, `stop`, `reboot`, `force`, `cancel`

```bash
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vpn-list
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vpn-view --id 12345
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vpn-edit --id 12345
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vpn-status --id 12345
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vpn-status-change --id 12345 --action start
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vpn-status-change --id 12345 --action stop
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vpn-status-change --id 12345 --action reboot
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vpn-status-change --id 12345 --action force
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vpn-status-change --id 12345 --action cancel
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vpn-locations
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vpn-plans
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vpn-plan-view --code vpn-basic
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vpn-configs --code vpn-basic
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vpn-rdns-edit --id 12345 --protocol ipv4 --ip 1.2.3.4
```

---
## [7.5][PRE-VALIDATION]

**Before calling `billing-order-validate` or `billing-order-create`**, run the local pre-validator to catch incompatible hardware/software combinations without an API round-trip.

```bash
# Full order pre-validation
uv run .claude/skills/ishosting-manager/scripts/validators.py validate-order \
  --type dedicated --os "linux/ubuntu.24.x#64" --panel fastpanel --location FI

# OS/panel compatibility only
uv run .claude/skills/ishosting-manager/scripts/validators.py validate-os-panel \
  --type vps --os "linux/alma9#64" --panel cpanel

# Show full compatibility matrix
uv run .claude/skills/ishosting-manager/scripts/validators.py check-matrix --type vps
```

Output: `{"valid": true/false, "errors": [...], "warnings": [...]}`

**Rules encoded:** OS/Panel compat matrix (VPS + Dedicated), Windows restrictions (no panels/admin/monitoring), panel↔admin dependency, VPS disk>100GB↔backup, Dedicated RAID needs 2+ same drives, DDoS only in NL.

**If `valid: false`** → do NOT proceed with the API order. Show the errors to the user and suggest corrections.
**If warnings present** → inform the user (e.g., "ticket-install" means support must install the panel manually).

---
## [8][BILLING]

```bash
uv run .claude/skills/ishosting-manager/scripts/ishosting.py billing-configs
uv run .claude/skills/ishosting-manager/scripts/ishosting.py billing-promo --code PROMO2024
uv run .claude/skills/ishosting-manager/scripts/ishosting.py billing-order-validate --plan PLAN_CODE --location ber --payment balance --type vps
uv run .claude/skills/ishosting-manager/scripts/ishosting.py billing-order-create --plan PLAN_CODE --location ber --payment balance --type dedicated
uv run .claude/skills/ishosting-manager/scripts/ishosting.py billing-invoices
uv run .claude/skills/ishosting-manager/scripts/ishosting.py billing-invoice-view --id 12345
uv run .claude/skills/ishosting-manager/scripts/ishosting.py billing-invoice-status --id 12345
uv run .claude/skills/ishosting-manager/scripts/ishosting.py billing-invoice-pay --id 12345
uv run .claude/skills/ishosting-manager/scripts/ishosting.py billing-invoice-cancel --id 12345
uv run .claude/skills/ishosting-manager/scripts/ishosting.py billing-balance-add --amount 100
uv run .claude/skills/ishosting-manager/scripts/ishosting.py billing-balance-invoices
uv run .claude/skills/ishosting-manager/scripts/ishosting.py billing-balance-invoice-view --id 12345
```

### Ordering with hardware/software options (VPS and Dedicated)

**[IMPORTANT]** VPS and Dedicated servers support additional hardware/software options beyond the base plan. Use the `--additions` parameter with JSON array.

**Step 1: Get available options from configs:**
```bash
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-configs --code PLAN_CODE
uv run .claude/skills/ishosting-manager/scripts/ishosting.py dedicated-configs --code PLAN_CODE
```

**Step 2: Extract option codes and category codes from configs:**

Each option in the response includes both `code` and `category.code`:
```json
{
  "name": "Nvidia 310",
  "code": "GPU_NVIDIA_310",
  "category": {"code": "PLATFORM_GPU"}
}
```

**Step 3: Build additions array:**

```json
[
  {"code": "GPU_NVIDIA_310", "category": "PLATFORM_GPU"},
  {"code": "DDOS_BASIC_CODE", "category": "ADDITIONS_DDOS"},
  {"code": "DRIVE_SSD_100GB_CODE", "category": "ADDITIONS_PLATFORM_FIXED_DRIVE_SLOT_1"}
]
```

**Step 4: Pass additions to order command:**

```bash
# Dedicated server with GPU + DDoS
uv run .claude/skills/ishosting-manager/scripts/ishosting.py billing-order-create \
  --plan DEDICATED_PLAN \
  --location ber \
  --payment balance \
  --type dedicated \
  --additions '[{"code":"GPU_NVIDIA_310","category":"PLATFORM_GPU"},{"code":"DDOS_BASIC_CODE","category":"ADDITIONS_DDOS"}]'

# VPS with extra RAM + backup
uv run .claude/skills/ishosting-manager/scripts/ishosting.py billing-order-create \
  --plan VPS_PLAN \
  --location ams \
  --payment balance \
  --type vps \
  --additions '[{"code":"RAM_DDR4_2GB_CODE","category":"ADDITIONS_PLATFORM_FIXED_RAM"},{"code":"BACKUP_DAILY_CODE","category":"ADDITIONS_BACKUP"}]'
```

**[CRITICAL]** Always get `category` codes from the API response, never hardcode them!

---
## [9][RECIPES]

### Recipe A: Create and pay for a service order (VPS/VPN/Storage/Dedicated)

**[CRITICAL]** This is a multi-step process that REQUIRES user confirmation at key points.

#### Step 1: Determine service type

**[IMPORTANT]** Identify the service type from the user's request:
- "VPS", "virtual server", "cloud server" → VPS
- "VPN", "private network" → VPN
- "dedicated server", "bare metal" → Dedicated
- "storage", "file server" → Storage

#### Step 2: Determine location and plan

**[CRITICAL]** The flow differs by service type because of how plans and locations relate:

##### Flow A — VPS / Dedicated / Storage (location-first approach)

**[IMPORTANT]** Determine location FIRST to filter plans. This reduces API response from 2MB to ~200KB.

**How locations work:** For these service types, locations are embedded in the plans themselves (each plan has a location field). The `*-locations` commands fetch all plans and extract unique locations from them. Then you can filter plans by location using the `--locations` parameter.

**Flow:** Determine location → show filtered plans → user picks plan

1. **If user specified a location** (e.g., "create VPS in Finland", "dedicated in NL"):
   - Extract location code from request
   - Skip to step 3 with that location

2. **If user did NOT specify a location:**
   - Fetch locations:
   ```bash
   uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-locations
   uv run .claude/skills/ishosting-manager/scripts/ishosting.py dedicated-locations
   uv run .claude/skills/ishosting-manager/scripts/ishosting.py storage-locations
   ```
   - Present as aligned columns with location name and code
   - Ask user: "Which location? (enter the number or code)"
   - **[STOP GATE]** End your response here. Do NOT fetch plans. Do NOT assume a default location. Wait for user input.

3. Fetch plans filtered by location:
```bash
# Use --locations parameter to filter
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-plans --locations FI
uv run .claude/skills/ishosting-manager/scripts/ishosting.py dedicated-plans --locations NL
uv run .claude/skills/ishosting-manager/scripts/ishosting.py storage-plans --locations US
```

For dedicated, can also filter by GPU/DDoS:
```bash
uv run .claude/skills/ishosting-manager/scripts/ishosting.py dedicated-plans --locations FI --gpu true
uv run .claude/skills/ishosting-manager/scripts/ishosting.py dedicated-plans --locations US --ddos DDOS_BASIC
```

4. Present filtered plans (much smaller response).

5. Ask user: "Which plan would you like? (enter the number or code)"
   **[STOP GATE]** End your response here. Do NOT fetch configs, OS options, or SSH keys. Wait for user to pick a plan.

##### Flow B — VPN (all plans share the same specs, location is chosen separately)

All VPN plans show a single default location (USA) but actually support 40+ locations via configs. So location must be determined first.

**Flow:** Show locations → user picks → show plans → user picks

1. **If user specified a location** (e.g., "create VPN in NL"):
   - Use it, confirm: "I'll use Netherlands (NL). OK?"
   - Skip to showing plans

2. **If user did NOT specify a location:**
   - Fetch locations:
   ```bash
   uv run .claude/skills/ishosting-manager/scripts/ishosting.py vpn-locations
   ```
   - Present as aligned columns:
   ```
   #   Location           Code   Extra cost
   1   USA, Chicago       US     -
   2   Netherlands        NL     -
   3   Germany            DE     -
   ```
   - Ask user: "Which location? (enter the number or code)"
   - **[STOP GATE]** End your response here. Do NOT fetch VPN plans. Do NOT assume a default location. Wait for user input.

3. Then show VPN plans:
   ```bash
   uv run .claude/skills/ishosting-manager/scripts/ishosting.py vpn-plans
   ```
4. Ask user: "Which plan would you like? (enter the number or code)"
   **[STOP GATE]** End your response here. Wait for user to pick a plan.

**Important notes:**
- Extract plan code (e.g., `29_1m`) from user choice
- For VPS/Dedicated/Storage: location comes from the chosen plan
- For VPN: location was determined in Step 2
- **Remember the service type** — you'll need `--type` in validate and create steps!

#### Step 3: Get and show OS options and hardware additions (VPS and Dedicated only)

**Skip this step for VPN and Storage** — OS is preinstalled and cannot be changed; no hardware options available.

For VPS and Dedicated, fetch available configs:

```bash
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-configs --code 29_1m
uv run .claude/skills/ishosting-manager/scripts/ishosting.py dedicated-configs --code dedicated-basic
```

Show available OS from configs. Ask user: "Which OS would you like to use?"
**[STOP GATE]** End your response here. Do NOT ask about SSH keys or proceed to validation. Wait for user to choose an OS.

After the user picks OS — ask about hardware/software additions if applicable:
"Would you like to add any hardware options (extra RAM, disk, DDoS protection, etc.)? If yes, I'll show you the available options. If no, we'll continue."
**[STOP GATE]** End your response here. Wait for user answer about additions.

If user wants hardware/software options, extract the `code` and `category.code` from the configs response and build an additions array (see Section [8] for details).

#### Step 4: Setup SSH key (CRITICAL - do this BEFORE order creation)

**[IMPORTANT]** Always ask about SSH keys BEFORE creating the order so the key can be attached during provisioning.

**Ask user**: "Would you like to add an SSH key for secure access to your server? Options: A) use existing key from your machine, B) paste a new key, C) generate a new key pair, D) skip (you'll get root password by email)."
**[STOP GATE]** End your response here. Do NOT check local SSH keys or query the API. Wait for user to choose an option.

**Option A: Use existing SSH key from OS**

Check if user has SSH keys locally:
```bash
cat ~/.ssh/id_ed25519.pub || cat ~/.ssh/id_rsa.pub
```

If found, show the public key and ask: "Use this SSH key?"

If user agrees:
1. First, get their existing SSH keys from is*hosting profile:
```bash
uv run .claude/skills/ishosting-manager/scripts/ishosting.py ssh-key-view
```

2. Check if this key already exists (compare public key). If not, add it:
```bash
uv run .claude/skills/ishosting-manager/scripts/ishosting.py ssh-key-create --title "My SSH Key" --public "ssh-ed25519 AAAA..."
```

3. Note the key ID from the response or the existing keys list. You'll use this in the order.

**Option B: User provides new key**

Ask user to paste their public SSH key, then add it to their profile (same as Option A, step 2-3).

**Option C: Generate new key pair**

```bash
ssh-keygen -t ed25519 -C "ishosting-vps" -f ~/.ssh/ishosting_key -N ""
cat ~/.ssh/ishosting_key.pub
```

Show user the generated keys, then add public key to profile (same as Option A, step 2-3).

**Option D: Skip SSH key**

User can skip this step, but warn them: "You'll receive a root password via email, but SSH key authentication is more secure."

#### Step 5: Validate order and GET USER CONFIRMATION

**[CRITICAL]** Run validation and show the user a complete order summary.

**[IMPORTANT]** ALWAYS specify `--type` parameter matching the service type:
- Use `--type vps` for VPS plans
- Use `--type vpn` for VPN plans
- Use `--type storage` for Storage plans
- Use `--type dedicated` for Dedicated plans

**Omitting `--type` will default to "vps" and cause "Wrong plan type" error if the plan is for a different service!**

```bash
# VPS with SSH key
uv run .claude/skills/ishosting-manager/scripts/ishosting.py billing-order-validate --plan 29_1m --location NL --payment balance --type vps --os "linux/ubuntu24#64" --ssh-keys "1196440"

# With hardware options
uv run .claude/skills/ishosting-manager/scripts/ishosting.py billing-order-validate --plan 29_1m --location NL --payment balance --type vps --os "linux/ubuntu24#64" --ssh-keys "1196440" --additions '[{"code":"RAM_CODE","category":"RAM_CATEGORY"}]'

# Without SSH key
uv run .claude/skills/ishosting-manager/scripts/ishosting.py billing-order-validate --plan 29_1m --location NL --payment balance --type vps --os "linux/ubuntu24#64"
```

**Present order summary as key-value lines (NOT a markdown table):**

```
Service:     VPS
Plan:        Lite (29_1m)
Location:    Netherlands
OS:          Ubuntu 24.04 LTS
CPU:         1 core
RAM:         1 GB
Disk:        25 GB
SSH Key:     Attached (My SSH Key)
Auto-renew:  Enabled
Price:       $5.00/month
```

**[IMPORTANT]** Auto-renew is enabled by default. Show it in the order summary so the user can see it.

**[CRITICAL]** Auto-renew is controlled ONLY at payment time via `--renew false` on `billing-invoice-pay`. Do NOT try to disable it via `*-edit --auto_renew false` during order creation — the `--renew` flag on the payment command is the correct and only way to set it for new orders. If the user asks to disable auto-renew, remember this and apply `--renew false` when paying the invoice (Step 7).

**Then explicitly ask**: "Ready to create this order? (yes/no)"

**[STOP GATE]** End your response here. Do NOT call `billing-order-create` or any other command. Do NOT assume "yes". Wait for the user to explicitly type "yes" or "no".

#### Step 6: Create order (only after confirmation)

**[IMPORTANT]** ALWAYS include `--type` parameter matching the service type (vps/vpn/storage/dedicated).

Same arguments as validation, but use `billing-order-create` instead of `billing-order-validate`.

This returns `{"order": {"invoice": {"id": 15718}, "services": [{"id": 12540}]}}`.

Extract invoice ID and service ID. Inform user: "Order created! Invoice #15718, Service ID: 12540"

If SSH key was attached: "[OK] SSH key attached. You can connect with: `ssh root@<server-ip>`"

#### Step 7: Handle payment

**[CRITICAL]** After order creation, ALWAYS ask the user how they want to pay. Do NOT automatically pay from balance.

##### Step 7.1: Check current balance and invoice amount

```bash
uv run .claude/skills/ishosting-manager/scripts/ishosting.py billing-invoice-view --id 15718
uv run .claude/skills/ishosting-manager/scripts/ishosting.py profile-view
```

##### Step 7.2: Present payment options to user

**Show the user:**
- Invoice amount: e.g., "$6.99"
- Current balance: e.g., "$1,000,925.06"

**Ask user to choose ONE of these payment options:**

```
#  Option       Description
1  Balance      Pay the full amount from account balance
2  Method       Pay the full amount via payment gateway (crypto, card, etc.)
3  Partly       Use balance first, pay the remainder via payment gateway
4  Pay later    Skip payment for now, invoice remains pending
```

**[STOP GATE]** End your response here. Do NOT pay the invoice. Do NOT assume the user wants to pay from balance. Wait for the user to choose one of the 4 options above.

---

##### Option 1: Balance (balance only)

```bash
uv run .claude/skills/ishosting-manager/scripts/ishosting.py billing-invoice-pay --id 15718 --balance true
```

**Check response**:
- If `paid: true` → "Payment successful! Invoice fully paid from balance."
- If `paid: false` → "Insufficient balance. Choose a payment method for the remaining amount."

---

##### Option 2: Method (payment gateway only)

1. Get available payment methods:
```bash
uv run .claude/skills/ishosting-manager/scripts/ishosting.py billing-configs
```

2. Show payment methods as a table (same format as Recipe C — balance top-up). Ask user to choose.

3. Pay with chosen method — `--method` flag only, no `--balance`:
```bash
uv run .claude/skills/ishosting-manager/scripts/ishosting.py billing-invoice-pay --id 15718 --method b_cryptomus
```

**Check response**:
- If `paid: true` → "Payment successful!"
- If `payment_link` exists → "Complete payment here: [link]"

---

##### Option 3: Partly (balance + payment gateway)

**[IMPORTANT]** This is a SINGLE API call with BOTH `--balance` and `--method` flags.

1. Get available payment methods (same as Option 2, step 1-2).

2. Pay with both balance and method in one call:
```bash
uv run .claude/skills/ishosting-manager/scripts/ishosting.py billing-invoice-pay --id 15718 --balance true --method b_cryptomus
```

The API will deduct available balance first, then generate a payment link for the remainder.

**Check response**:
- If `paid: true` → "Payment successful! Fully covered by balance."
- If `paid: false` + `payment_link` → Show: "Balance applied. Complete the remaining amount here: [link]"

---

##### Option 4: Pay later

**No command needed.** Simply inform user:

"Invoice #15718 ($6.99) is pending. You can pay it later."

---

### Recipe B: Attach SSH key to existing service

**When to use**: To add or update SSH keys on an already-provisioned VPS/Storage/Dedicated server.

#### Step 1: Ask user for SSH key preference

"Would you like to attach an SSH key?"
- **Use existing SSH key from your OS**
- **Enter a new SSH key**
- **Create a new SSH key pair**
- **Skip**

#### Step 2: Get or create the key

Same flow as Recipe A, Step 4 (Options A/B/C).

#### Step 3: Add key to is*hosting profile

```bash
uv run .claude/skills/ishosting-manager/scripts/ishosting.py ssh-key-create --title "My SSH Key" --public "ssh-ed25519 AAAA..."
```

#### Step 4: Attach key to service

```bash
# For VPS
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-ssh --id 12540

# For Storage
uv run .claude/skills/ishosting-manager/scripts/ishosting.py storage-ssh --id 12540

# For Dedicated
uv run .claude/skills/ishosting-manager/scripts/ishosting.py dedicated-ssh --id 12540
```

Inform user: "[OK] SSH key attached to service."

---

### Recipe C: Top up account balance

**[CRITICAL]** ALWAYS follow these steps when user asks to top up balance:

#### Step 1: Get and show available payment methods

**ALWAYS run this command first:**
```bash
uv run .claude/skills/ishosting-manager/scripts/ishosting.py billing-configs
```

**Present payment methods as a formatted table:**

```
#  Payment Method               Code           Min   Max       Fees       KYC
1  Crypto (Cryptomus)           b_cryptomus    $1    $10,000   None       No
2  Visa/Mastercard (Revolut)    b_revolut      $5    $10,000   +19% VAT   No
3  Visa/Mastercard (Overpay)    b_overpay      $5    $2,000    +4.5%      No
```

Show any VAT or fees, min/max limits, KYC requirements.

#### Step 2: Ask user to choose method and amount

"Please choose a payment method (enter the number or code) and specify the amount you'd like to add."

Validate amount is within the chosen method's min/max limits.

#### Step 3: Create top-up invoice

```bash
uv run .claude/skills/ishosting-manager/scripts/ishosting.py billing-balance-add --amount 50 --method b_cryptomus
```

#### Step 4: Provide payment link

**Check response**:
- If `paid: true` → "[OK] Balance added successfully!"
- If `payment_link` exists → "Complete payment here: [link]"

---

### Recipe D: Manage service status

**When to use**: User wants to start, stop, restart, or perform other actions on a service.

#### Step 1: Get current status

```bash
# For VPS
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-status --id 12540

# For VPN
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vpn-status --id 12540

# For Storage
uv run .claude/skills/ishosting-manager/scripts/ishosting.py storage-status --id 12540

# For Dedicated
uv run .claude/skills/ishosting-manager/scripts/ishosting.py dedicated-status --id 12540
```

Show user current status.

#### Step 2: Execute action

```bash
uv run .claude/skills/ishosting-manager/scripts/ishosting.py {svc}-status-change --id 12540 --action start
```

**[CRITICAL]** Check the API response. Only confirm success if the response confirms the action was applied. If error → report actual error.

---

### Recipe E: Cancel a service

**When to use**: User wants to cancel a VPS, VPN, Storage, or Dedicated service.

**[CRITICAL]** Cancellation is a **destructive and irreversible** operation. You MUST get explicit user confirmation before proceeding.

#### Step 1: Show current service info

Fetch the service details first so the user sees what they're cancelling:
```bash
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-view --id 12345
```

Show the user: service name, plan, location, IP, expiration date.

#### Step 2: Request explicit confirmation

Ask the user clearly:
"Are you sure you want to cancel service **[name]** (ID: [id])? This action is **irreversible** — the service will be terminated. (yes/no)"

**[STOP GATE]** End your response here. Do NOT run the cancel command. Do NOT assume yes. Wait for the user to explicitly type "yes" before proceeding.

#### Step 3: Execute cancellation (only after confirmation)

```bash
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-status-change --id 12345 --action cancel
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vpn-status-change --id 12345 --action cancel
uv run .claude/skills/ishosting-manager/scripts/ishosting.py storage-status-change --id 12345 --action cancel
uv run .claude/skills/ishosting-manager/scripts/ishosting.py dedicated-status-change --id 12345 --action cancel
```

Check response. Report only: "Service (ID: 12345) has been cancelled." or "Failed to cancel service: [actual error message]". Nothing else.

---

### Recipe F: Change auto-renew setting

**When to use**: User wants to enable or disable auto-renew on an **already active** service.

**[CRITICAL]** For NEW orders, auto-renew is set at payment time via `--renew false` on `billing-invoice-pay` (see Step 7 in Recipe A). Do NOT use `*-edit` to change auto-renew during order creation — it may fail on unpaid/pending services.

```bash
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-edit --id 12345 --auto_renew false
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vpn-edit --id 12345 --auto_renew false
uv run .claude/skills/ishosting-manager/scripts/ishosting.py storage-edit --id 12345 --auto_renew false
uv run .claude/skills/ishosting-manager/scripts/ishosting.py dedicated-edit --id 12345 --auto_renew false
```

**[CRITICAL]** After executing the edit command, you MUST verify the change was applied:
1. Check the API response — it must confirm `updated: true`
2. Then fetch the service details to verify the new auto_renew value:
```bash
uv run .claude/skills/ishosting-manager/scripts/ishosting.py vps-view --id 12345
```
3. Only report success if the `auto_renew` field in the response matches what was requested.
4. If the response shows the old value, report: "The change was not applied. Current auto-renew status: [value]"

---

### Recipe G: SSH safety when connecting to user's servers

**[CRITICAL]** Before executing ANY commands on a user's server via SSH, the agent MUST warn the user and obtain explicit confirmation. Never connect and run commands without the user's approval.

**When to use**: The agent is about to SSH into a user's VPS, Dedicated, or Storage server to perform operations.

#### Step 1: Display safety warning

**Before connecting**, always warn about risks: misconfiguration, service disruption, data loss, security exposure.

#### Step 2: Present the action plan

Show the user a numbered list of exactly what the agent intends to do on their server. Be specific about each step.

**[IMPORTANT]** The plan must list every command or operation the agent will perform. Do not hide steps or combine multiple actions into a single vague item.

#### Step 3: Request explicit user confirmation

**Ask the user clearly:** "Do you approve this plan? I will only proceed if you confirm. (yes/no)"

**[STOP GATE]** End your response here. Do NOT connect to the server or run any commands. Wait for the user's explicit approval.

If user says NO → ask what to change, revise plan. If any step fails → stop immediately and inform user.

---
## [10][RESPONSE VERIFICATION]

**[CRITICAL]** You MUST check every API response before reporting results to the user. NEVER assume success. NEVER say "done" without verifying the response.

**Rules:**
1. **Always read the full API response** — check `status`, `error`, and the actual data fields
2. **For action commands** (`*-edit`, `*-status-change`, `ssh-key-create`, etc.) — verify the response contains confirmation (e.g., `updated: true`, `changed: true`, `created: true`)
3. **For edit commands** — after a successful edit, fetch the resource again to confirm the change was actually applied (e.g., after `vps-edit --auto_renew false`, run `vps-view` and check that `auto_renew` is now `false`)
4. **If the API returns an error** — report the actual error to the user, do not say the action succeeded
5. **If the response is empty or ambiguous** — report that the result is unclear and suggest the user verify manually
6. **NEVER fabricate results** — only report what the API actually returned

---
## [11][OUTPUT]

Commands return: `{"status": "success|error", ...}`.

```
INDEX  PATTERN            RESPONSE
[1]    List commands       {items: object[]}
[2]    View commands       {id: int, item: object}
[3]    Action commands     {id: int, action: bool}
[4]    Create commands     {id: int, created: bool}
[5]    Payment commands    {id: int, paid: bool, payment_link?: string}
```

---
## [12][FORMATTING]

**[IMPORTANT]** Never show raw JSON to the user.

**[CRITICAL]** Do NOT use markdown tables (pipes `|` and dashes `---`). Many terminals and agents render them as ugly raw text. Use plain-text aligned columns instead.

**Profile / Service details** — use key: value lines:
```
Name:    Daniil
Email:   user@example.com
Balance: $56.50
```

**Lists** (VPS list, invoices, plans, SSH keys) — use space-aligned columns:
```
ID      Name                  Location    Plan    IP          Status
12345   My VPS                Netherlands Lite    1.2.3.4     Running
12346   Staging               Germany     Start   5.6.7.8     Stopped
```

**Payment results** — check the response:
- If `paid: true` → "Payment successful! Invoice #15718 is paid."
- If `paid: false` and `payment_link` exists - "Payment required. Complete payment here: [payment_link]"
- If `paid: false` and no link - "Payment pending. You can pay later from your profile."

**General rules:**
- Flatten nested JSON into readable fields (e.g. `platform.config.cpu.name` → CPU)
- Omit empty, null, or irrelevant fields
- Format prices with `$` symbol
- Format dates as human-readable (e.g. "Jan 16, 2026")
- For long lists, show the most relevant columns only

**[CRITICAL] Clean output — no internal leaks:**
- **NEVER** output TODO, TO_DO, FIXME, HACK, or any developer markers in user-facing text
- **NEVER** expose raw JSON field names to the user (e.g., do NOT write "paid_at есть" or "auto_renew: true"). Translate them to human-readable labels (e.g., "Paid: Yes", "Auto-renew: enabled")
- **NEVER** mix languages in a single phrase (e.g., "Оплачено: да (paid_at есть)"). Pick one language — match the user's language
- **NEVER** show internal implementation details, placeholder text, or debugging notes
- If a field value is unclear, either translate it to plain language or omit it entirely
