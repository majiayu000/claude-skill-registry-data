---
name: karabiner
description: Configure and manage Karabiner-Elements key remapping. Use when modifying karabiner.json, adding key remappings, creating complex modifications, managing profiles, setting variables, or troubleshooting keybinding issues.
allowed-tools: [Read, Edit, Bash]
---

# Karabiner-Elements configuration skill

## Overview

Manage Karabiner-Elements configuration for macOS keyboard customization including key remapping, complex modifications, and profile management.

## Configuration locations

- Config file: `~/.config/karabiner/karabiner.json`
- CLI tool: `/Library/Application Support/org.pqrs/Karabiner-Elements/bin/karabiner_cli`
- Assets: `~/.config/karabiner/assets/complex_modifications/`

## Current configuration

### Complex modifications (internal keyboard only)

- **caps lock → left control**: Caps lock acts as control
- **right command → hyper**: Right command acts as cmd+shift+ctrl+opt
- **right option → meh**: Right option acts as shift+ctrl+opt

All modifications are limited to the internal MacBook keyboard using `device_if` conditions with `is_built_in_keyboard: true`.

## CLI operations

### Profile management

```bash
karabiner_cli --select-profile 'Default profile'
karabiner_cli --show-current-profile-name
karabiner_cli --list-profile-names
```

### Device inspection

**List connected devices:**
```bash
karabiner_cli --list-connected-devices
```

Returns JSON with device information:
- `device_id`: unique device identifier
- `device_identifiers`: keyboard/pointing device flags, vendor/product IDs
- `is_built_in_keyboard`/`is_built_in_pointing_device`: built-in device flags
- `manufacturer`, `product`: device name and manufacturer
- `transport`: connection type (USB, Bluetooth, FIFO, Audio)

Useful for finding `vendor_id` and `product_id` for device-specific mappings.

**List system variables:**
```bash
karabiner_cli --list-system-variables
```

Shows current system state variables:
- `system.now.milliseconds`: current timestamp
- `system.scroll_direction_is_natural`: natural scrolling enabled
- `system.use_fkeys_as_standard_function_keys`: function key behavior
- `system.temporarily_ignore_all_devices`: temporary disable flag

### Variable management

Set variables for complex modifications:

```bash
karabiner_cli --set-variables '{"cli_flag1":1, "cli_flag2":2}'
```

Use `--silent` flag to suppress output.

### Development tools

**Run JavaScript files:**
```bash
karabiner_cli --eval-js path/to/script.js
```

Executes JavaScript using Duktape engine. Useful for generating or manipulating complex modifications programmatically.



**Lint configuration:**
```bash
karabiner_cli --lint-complex-modifications ~/.config/karabiner/karabiner.json
```

**Format JSON:**
```bash
karabiner_cli --format-json ~/.config/karabiner/karabiner.json
```

### System operations

**Copy profile to system default (requires admin):**
```bash
sudo karabiner_cli --copy-current-profile-to-system-default-profile
```

**Remove system default profile:**
```bash
sudo karabiner_cli --remove-system-default-profile
```

### Version info

```bash
karabiner_cli --version
karabiner_cli --version-number
```

## Configuration structure

### Profile format

```json
{
  "profiles": [
    {
      "name": "Default profile",
      "selected": true,
      "complex_modifications": { "rules": [...] },
      "devices": [...],
      "simple_modifications": [...],
      "virtual_hid_keyboard": { "keyboard_type_v2": "ansi" }
    }
  ]
}
```

### Complex modification rule

```json
{
  "description": "Description of the rule",
  "manipulators": [
    {
      "type": "basic",
      "from": {
        "key_code": "h",
        "modifiers": { "mandatory": ["left_option"] }
      },
      "to": { "key_code": "left_arrow" }
    }
  ]
}
```

### Advanced manipulator features

**Tap vs hold:**
```json
{
  "from": { "key_code": "return_or_enter" },
  "to_if_alone": [{ "key_code": "return_or_enter" }],
  "to_if_held_down": [{
    "key_code": "left_shift",
    "modifiers": ["right_shift", "left_control", "left_option"]
  }],
  "parameters": {
    "basic.to_if_held_down_threshold_milliseconds": 200
  }
}
```

**Delayed actions:**
```json
{
  "to_delayed_action": {
    "to_if_canceled": [{ "key_code": "return_or_enter" }]
  },
  "parameters": {
    "basic.to_delayed_action_delay_milliseconds": 200
  }
}
```

### Device-specific mappings

```json
{
  "identifiers": {
    "is_keyboard": true,
    "product_id": 834,
    "vendor_id": 1452
  },
  "simple_modifications": [
    {
      "from": { "key_code": "fn" },
      "to": [{ "key_code": "escape" }]
    }
  ]
}
```

**Special device options:**
- `ignore: true` - ignore this device
- `disable_built_in_keyboard_if_exists: true` - disable built-in when this device connected
- `treat_as_built_in_keyboard: true` - treat as built-in keyboard
- `manipulate_caps_lock_led: false` - don't manipulate caps lock LED

## Common key codes

### Modifiers

- `left_command`, `right_command`
- `left_control`, `right_control`
- `left_shift`, `right_shift`
- `left_option`, `right_option`
- `caps_lock`, `fn`

### Special keys

- `return_or_enter`, `escape`, `delete_or_backspace`
- `tab`, `spacebar`
- `up_arrow`, `down_arrow`, `left_arrow`, `right_arrow`
- `page_up`, `page_down`, `home`, `end`

### Modifier specifications

```json
{
  "modifiers": {
    "mandatory": ["left_option"],
    "optional": ["caps_lock", "any"]
  }
}
```

## Common patterns

### Simple key remap

```json
{
  "description": "caps lock to escape",
  "manipulators": [{
    "type": "basic",
    "from": { "key_code": "caps_lock" },
    "to": [{ "key_code": "escape" }]
  }]
}
```

### Modifier + key to key

```json
{
  "description": "opt+h to left arrow",
  "manipulators": [{
    "type": "basic",
    "from": {
      "key_code": "h",
      "modifiers": { "mandatory": ["left_option"] }
    },
    "to": [{ "key_code": "left_arrow" }]
  }]
}
```

### Hyper key (tap for key, hold for modifier)

```json
{
  "description": "return to hyper when held",
  "manipulators": [{
    "type": "basic",
    "from": { "key_code": "return_or_enter" },
    "to_if_alone": [{ "key_code": "return_or_enter" }],
    "to_if_held_down": [{
      "key_code": "left_shift",
      "modifiers": ["right_shift", "left_control", "left_option"],
      "repeat": false
    }],
    "parameters": {
      "basic.to_if_held_down_threshold_milliseconds": 200
    }
  }]
}
```

## Working with configuration

### Validate changes

After editing karabiner.json:

1. Karabiner-Elements automatically reloads on file change
2. Check EventViewer to verify key mappings work
3. Use `karabiner_cli --lint-complex-modifications` to validate

### Adding new rules

1. Edit `~/.config/karabiner/karabiner.json`
2. Add new rule to `profiles[0].complex_modifications.rules`
3. Save file (auto-reload triggers)
4. Test in EventViewer

### Testing key codes

1. Open Karabiner-Elements > Misc > Launch EventViewer
2. Press keys to see their key codes
3. Use codes in configuration

## Device condition patterns

### Limiting rules to built-in keyboard

```json
{
  "conditions": [
    {
      "identifiers": [
        {
          "is_built_in_keyboard": true
        }
      ],
      "type": "device_if"
    }
  ]
}
```

Use `device_if` conditions to limit modifications to specific devices. The `is_built_in_keyboard` flag targets only the internal MacBook keyboard, ignoring all external keyboards.

### Other device condition options

- `is_built_in_keyboard`: Internal MacBook keyboard
- `is_pointing_device`: Trackpads and mice
- `vendor_id` + `product_id`: Specific device by identifiers
- `device_unless`: Inverse condition (apply to all except specified devices)

## Integration with other tools

### Hammerspoon relationship

- Karabiner: Low-level key remapping at OS level
- Hammerspoon: High-level automation and app control
- Use Karabiner for modifier/key remaps, Hammerspoon for actions

Current setup:
- Karabiner creates hyper and meh modifiers from right command/option
- Hammerspoon can bind hyper/meh keys to app launches and window management

## Troubleshooting

### Changes not taking effect

1. Check JSON syntax is valid
2. Ensure Karabiner-Elements is running
3. Check Security & Privacy settings allow Karabiner
4. Restart Karabiner-Elements: `killall Karabiner-Elements && open -a Karabiner-Elements`

### Device not recognized

1. Check `identifiers` match in EventViewer
2. Verify `is_keyboard: true` is set
3. Try unplugging and reconnecting device

### Complex modification not working

1. Test key codes in EventViewer
2. Check modifier combinations are correct
3. Verify no conflicting rules exist
4. Check rule order (first matching rule wins)

### Profile issues

```bash
karabiner_cli --list-profile-names
karabiner_cli --show-current-profile-name
karabiner_cli --select-profile 'ProfileName'
```

## Resources

- Karabiner-Elements docs: https://karabiner-elements.pqrs.org/docs/
- Complex modifications gallery: https://ke-complex-modifications.pqrs.org/
- EventViewer: Karabiner-Elements > Misc > Launch EventViewer
