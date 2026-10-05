---
name: adb-karrot
description: Karrot app automation - bypass Play Integrity detection, login, and interaction workflows
version: 1.0.0
modularized: true
scripts_enabled: true
tier: 3
category: adb-app-automation
last_updated: 2025-12-01
compliance_score: 100
dependencies:
  - adb-screen-detection
  - adb-navigation-base
  - adb-workflow-orchestrator
  - adb-magisk
auto_trigger_keywords:
  - karrot
  - play-integrity
  - api-hooking
  - bypass
  - login
scripts:
  - name: adb-karrot-launch.py
    purpose: Launch Karrot app
    type: python
    command: uv run .claude/skills/adb-karrot/scripts/adb-karrot-launch.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-12-01

  - name: adb-karrot-check-detection.py
    purpose: Check if app detects emulator/spoofed environment
    type: python
    command: uv run .claude/skills/adb-karrot/scripts/adb-karrot-check-detection.py
    zero_context: false
    version: 1.0.0
    last_updated: 2025-12-01

  - name: adb-karrot-test-login.py
    purpose: Test login with bypass, verify successful authentication
    type: python
    command: uv run .claude/skills/adb-karrot/scripts/adb-karrot-test-login.py
    zero_context: false
    version: 1.0.0
    last_updated: 2025-12-01

color: cyan
---

---

## Quick Reference (30 seconds)

**Karrot App Automation & Play Integrity Bypass**

**What It Does**: Automates Karrot app interactions. Enables Play Integrity API bypass via Magisk hooks to allow app usage on unsupported environments.

**Core Capabilities**:
- 🚀 **App Launching**: Open Karrot with auto-detection
- 🔍 **Detection Checking**: Verify if app detects emulator
- 🔐 **Login Automation**: Automated login with verification
- ✅ **Bypass Validation**: Confirm Play Integrity bypass success

**When to Use**:
- Testing Karrot app on emulator
- Implementing Play Integrity bypass
- Automating login and basic navigation
- Validating bypass effectiveness

---

## Scripts

### adb-karrot-launch.py

Launch Karrot application.

```bash
# Launch on default device
uv run .claude/skills/adb-karrot/scripts/adb-karrot-launch.py

# Specify device
uv run .claude/skills/adb-karrot/scripts/adb-karrot-launch.py --device 127.0.0.1:5555

# Wait for login screen
uv run .claude/skills/adb-karrot/scripts/adb-karrot-launch.py \
    --wait-text "Login" \
    --timeout 10

# JSON output
uv run .claude/skills/adb-karrot/scripts/adb-karrot-launch.py --json
```

---

### adb-karrot-check-detection.py

Check if Karrot detects emulator or spoofed environment.

```bash
# Quick detection check
uv run .claude/skills/adb-karrot/scripts/adb-karrot-check-detection.py \
    --device 127.0.0.1:5555

# Detailed check (launch and monitor)
uv run .claude/skills/adb-karrot/scripts/adb-karrot-check-detection.py \
    --device 127.0.0.1:5555 \
    --launch \
    --detailed

# Check for error-18 (PlayIntegrity CLIENT_TRANSIENT_ERROR)
uv run .claude/skills/adb-karrot/scripts/adb-karrot-check-detection.py \
    --device 127.0.0.1:5555 \
    --check-logcat

# JSON output
uv run .claude/skills/adb-karrot/scripts/adb-karrot-check-detection.py --json
```

---

### adb-karrot-test-login.py

Test login functionality with bypass enabled.

```bash
# Basic login test
uv run .claude/skills/adb-karrot/scripts/adb-karrot-test-login.py \
    --device 127.0.0.1:5555 \
    --email test@example.com \
    --password testpass123

# Login with verification
uv run .claude/skills/adb-karrot/scripts/adb-karrot-test-login.py \
    --device 127.0.0.1:5555 \
    --email test@example.com \
    --password testpass123 \
    --verify-success \
    --timeout 30

# Test bypass effectiveness (should NOT get error-18)
uv run .claude/skills/adb-karrot/scripts/adb-karrot-test-login.py \
    --device 127.0.0.1:5555 \
    --email test@example.com \
    --password testpass123 \
    --check-bypass

# JSON output
uv run .claude/skills/adb-karrot/scripts/adb-karrot-test-login.py --json
```

---

## Workflows

### karrot-bypass-playintegrity.toon

**COMPLETE PLAY INTEGRITY BYPASS WORKFLOW** - Master workflow coordinating all steps from Magisk setup through Karrot login verification.

```yaml
name: Karrot Play Integrity Bypass - Complete Workflow
description: Full end-to-end bypass setup and validation
version: 1.0.0

parameters:
  device: "127.0.0.1:5555"
  module_path: "/sdcard/PlayIntegrityFork.zip"
  test_email: "test@karrot.example.com"
  test_password: "bypasstest123"
  timeout: 30

phases:
  # PHASE 1: Setup Magisk with Zygisk
  - id: phase1_magisk_setup
    name: "Phase 1: Setup Magisk with Zygisk"
    steps:
      - id: launch_magisk
        action: adb-magisk-launch
        params:
          device: "{{ device }}"
          wait_text: "Modules"
          timeout: 10

      - id: navigate_settings
        action: adb-tap
        params:
          x: 100
          y: 200
          device: "{{ device }}"

      - id: enable_zygisk
        action: adb-magisk-enable-zygisk
        params:
          device: "{{ device }}"
          auto_reboot: false

  # PHASE 2: Install PlayIntegrityFork Module
  - id: phase2_install_module
    name: "Phase 2: Install PlayIntegrityFork Module"
    steps:
      - id: launch_magisk_again
        action: adb-magisk-launch
        params:
          device: "{{ device }}"

      - id: navigate_modules
        action: adb-tap
        params:
          x: 100
          y: 100
          device: "{{ device }}"

      - id: tap_install_fab
        action: adb-tap
        params:
          x: 400
          y: 800
          device: "{{ device }}"

      - id: wait_file_picker
        action: adb-wait-for
        params:
          method: text
          target: "Select"
          timeout: 5

      - id: select_module_file
        action: adb-file-select
        params:
          path: "{{ module_path }}"

      - id: wait_install_complete
        action: adb-wait-for
        params:
          method: text
          target: "Installation complete"
          timeout: "{{ timeout }}"

  # PHASE 3: Verify Magisk Module
  - id: phase3_verify_module
    name: "Phase 3: Verify Module Installation"
    steps:
      - id: check_module_list
        action: adb-magisk-launch
        params:
          device: "{{ device }}"
          wait_text: "PlayIntegrityFork"
          timeout: 10

      - id: verify_module_enabled
        action: adb-screenshot-capture
        params:
          device: "{{ device }}"

  # PHASE 4: Launch Karrot and Check Pre-Bypass
  - id: phase4_check_prebypas
    name: "Phase 4: Check Detection Pre-Bypass"
    steps:
      - id: launch_karrot
        action: adb-karrot-launch
        params:
          device: "{{ device }}"
          timeout: 10

      - id: check_detection_initial
        action: adb-karrot-check-detection
        params:
          device: "{{ device }}"
          detailed: true

  # PHASE 5: Configure PlayIntegrityFork
  - id: phase5_configure_module
    name: "Phase 5: Configure PlayIntegrityFork Module"
    steps:
      - id: wait_karrot_ready
        action: adb-wait-for
        params:
          method: text
          target: "Login"
          timeout: 10

      - id: note_configuration_needed
        action: adb-screenshot-capture
        params:
          device: "{{ device }}"

  # PHASE 6: Test Login with Bypass
  - id: phase6_test_bypass
    name: "Phase 6: Test Login with Bypass Active"
    steps:
      - id: test_login
        action: adb-karrot-test-login
        params:
          device: "{{ device }}"
          email: "{{ test_email }}"
          password: "{{ test_password }}"
          verify_success: true
          check_bypass: true
          timeout: "{{ timeout }}"

  # PHASE 7: Verify Bypass Success
  - id: phase7_final_verification
    name: "Phase 7: Final Verification"
    steps:
      - id: check_detection_after
        action: adb-karrot-check-detection
        params:
          device: "{{ device }}"
          check_logcat: true

      - id: wait_profile_screen
        action: adb-wait-for
        params:
          method: text
          target: "Profile"
          timeout: 5

recovery:
  # Retry on module installation failure
  - on_error: phase2_install_module
    action: retry
    max_attempts: 2
    delay: 3

  # Fallback for detection check
  - on_error: phase4_check_prebypas
    action: adb-screenshot-capture
    then: continue

  # Retry login test
  - on_error: phase6_test_bypass
    action: retry
    max_attempts: 2
    delay: 2
```

### karrot-login.toon

Simplified login workflow (faster, for repeated testing).

```yaml
name: Karrot Login Test
description: Quick login workflow for bypass validation

parameters:
  device: "127.0.0.1:5555"
  email: "test@karrot.example.com"
  password: "testpass123"

phases:
  - id: launch_and_login
    name: "Launch and Login"
    steps:
      - id: launch
        action: adb-karrot-launch
        params: {device: "{{ device }}"}

      - id: wait_login_screen
        action: adb-wait-for
        params: {method: text, target: "Email", timeout: 5}

      - id: test_login
        action: adb-karrot-test-login
        params:
          device: "{{ device }}"
          email: "{{ email }}"
          password: "{{ password }}"
          verify_success: true
```

---

## Usage Patterns

### Pattern 1: Complete Bypass Setup

```bash
# Full end-to-end bypass implementation
uv run .claude/skills/adb-workflow-orchestrator/scripts/adb-run-workflow.py \
    --workflow .claude/skills/adb-karrot/workflows/karrot-bypass-playintegrity.toon \
    --param device=127.0.0.1:5555 \
    --param module_path=/sdcard/PlayIntegrityFork.zip \
    --verbose
```

### Pattern 2: Quick Login Test

```bash
# Fast login test for bypass validation
uv run .claude/skills/adb-workflow-orchestrator/scripts/adb-run-workflow.py \
    --workflow .claude/skills/adb-karrot/workflows/karrot-login.toon \
    --param device=127.0.0.1:5555 \
    --param email=test@example.com
```

### Pattern 3: Detection Monitoring

```bash
# Monitor detection status during testing
watch -n 5 "uv run .claude/skills/adb-karrot/scripts/adb-karrot-check-detection.py \
    --device 127.0.0.1:5555 \
    --check-logcat"
```

---

## Analysis Files (From Previous Research)

Located in `./analysis/`:
- `detection-report.md` - Detailed detection mechanism analysis
- `bypass-strategy.md` - Bypass approach and reasoning
- `playintegrity-findings.md` - Play Integrity API research

---

## Integration Points

**Depends On**:
- `adb-magisk` (Magisk setup and module installation)
- `adb-screen-detection` (screenshot and OCR verification)
- `adb-navigation-base` (gesture automation)
- `adb-workflow-orchestrator` (workflow coordination)

**Used By**:
- Custom app testing and automation
- Play Integrity bypass validation

---

## Karrot App Detection Mechanism

```
Google Play Integrity API
  ├─ deviceIntegrity()
  ├─ serverIntegrity() (hardcoded token)
  ├─ 1000ms timeout
  └─ Error -18: CLIENT_TRANSIENT_ERROR (emulator)

Persona SDK Wrapper
  └─ Calls integrity verification

PlayIntegrityFork Bypass
  └─ Hooks Play Services
      └─ Returns spoofed device signature
```

---

**Version**: 1.0.0
**Status**: ✅ App-Specific Tier
**Scripts**: 3
**Workflows**: 2
**Last Updated**: 2025-12-01
**Tier**: 3 (App-Specific)

