---
name: add-inventory-device
description: Add physical equipment to one or more YAML files referenced by inventory/stands.yaml. Use when asked to register a DUT, analyzer, generator, or other supported device, create a new device inventory source, reorganize equipment files, or diagnose duplicate and missing device IDs.
---

# Add Inventory Device

Register physical equipment without leaking secrets or coupling tests to physical identifiers.

## Inspect

1. Read `AGENTS.md` completely and follow its approval and verification rules.
2. Read `inventory/stands.yaml` and every path in `device_files`.
3. Read `src/hardware_test/factory/devices.py` to discover supported inventory `type` values.
4. Read inventory models and existing device entries to follow the current schema and naming.
5. Determine the device ID, supported type, example-safe model, transport data, and credential
   reference. Ask for missing required values.

## Choose the inventory source

1. Add the device to the closest existing equipment file when its grouping is clear.
2. Propose a new explicit YAML file when a category or location has enough devices to justify it.
3. Add a new file to `device_files`; never use glob discovery.
4. Resolve paths relative to `inventory/stands.yaml`.
5. Check device IDs globally across all listed files and reject duplicates.

## Design and review

1. Use only types already supported by `_DEVICE_TYPES`.
2. Treat support for a new device class or type as a separate architectural change; do not extend
   `_DEVICE_TYPES` implicitly.
3. Store host, port, model, transport type, and credential reference in device inventory.
4. Never store a password, private key, token, or real organization secret in YAML.
5. Use documentation-only address ranges for template examples.
6. Show the complete proposed device YAML, any `device_files` change, and all affected files.
7. Request explicit approval before modifying files.

Example:

```yaml
version: 1

devices:
  analyzer_02:
    type: analyzer
    model: example-analyzer-b
    transport:
      type: ssh
      ssh:
        host: 192.0.2.23
        port: 22
        credentials: analyzer-default
```

## Implement and verify

1. Modify only the approved inventory sources and documentation.
2. Preserve unrelated equipment and stand definitions.
3. Load the combined inventory and verify the new ID is present.
4. Verify all stand references remain valid and duplicate IDs fail clearly.
5. Add or update tests only after production changes are approved, as required by `AGENTS.md`.
6. Do not connect to equipment or run hardware tests unless explicitly requested.
7. Stage the intended changes and run `./scripts/ci.sh`.
8. Report the source file, device ID, supported type, and verification results.
