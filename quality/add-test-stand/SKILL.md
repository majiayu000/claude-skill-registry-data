---
name: add-test-stand
description: Add or update a logical hardware test stand in inventory/stands.yaml. Use when asked to create a stand, assign existing physical devices to logical roles, add stand capabilities, or change a stand topology without duplicating equipment connection settings.
---

# Add Test Stand

Add a validated stand definition that maps stable logical roles to existing physical device IDs.

## Inspect

1. Read `AGENTS.md` completely and follow its approval and verification rules.
2. Read `inventory/stands.yaml` and every source in its `device_files` list.
3. Read the inventory Pydantic models and loader when the requested shape is not already supported.
4. List the requested stand name, description, capabilities, logical roles, and referenced device
   IDs. Ask only for information that cannot be inferred safely.

## Design and review

1. Verify that the stand name is unique unless the user explicitly requests an update.
2. Verify every referenced device ID exists across the combined physical-device inventory.
3. Keep stand entries limited to description, capabilities, and `role: device_id` mappings.
4. Keep hosts, ports, models, transports, and credential references in device inventory files.
5. Keep secrets in runtime settings; never place usernames or passwords in inventory.
6. Prefer descriptive logical roles that remain stable when physical equipment changes.
7. Show the complete proposed stand YAML and identify every file to change.
8. Request explicit approval before modifying files.

Example:

```yaml
stands:
  stand-03:
    description: Example validation stand
    capabilities: [smoke, measurement]
    devices:
      dut: dut_03
      analyzer_primary: analyzer_01
      analyzer_secondary: analyzer_02
```

## Implement and verify

1. Modify only the approved stand definitions and any approved documentation.
2. Preserve unrelated inventory entries and formatting.
3. Load `inventory/stands.yaml` through `hardware_test.inventory.load_inventory` to validate all
   sources and references.
4. Add or update tests only after production changes are approved, as required by `AGENTS.md`.
5. Do not connect to physical equipment or run hardware tests unless explicitly requested.
6. Stage the intended changes and run `./scripts/ci.sh`.
7. Report the logical-role mapping and verification results.
