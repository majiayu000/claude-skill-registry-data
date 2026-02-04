---
name: homeassistant
description: Expert HomeAssistant development skill for creating custom sensors (template, REST, command line, Python components), building Lovelace dashboards with custom cards and layouts, and developing custom integrations with config flows, coordinators, and multiple platforms. Use this skill when working with HomeAssistant YAML configuration, Python integration development, or dashboard customization.
---

# HomeAssistant Development

## Overview

This skill provides comprehensive guidance for HomeAssistant development across three core areas: custom sensors, dashboards (Lovelace UI), and custom integrations. Use this skill when creating or modifying HomeAssistant configurations, developing custom Python components, or building user interfaces.

## When to Use This Skill

Activate this skill when:
- Creating or modifying sensors (template, REST, command line, or Python-based)
- Building or customizing Lovelace dashboards and cards
- Developing custom integrations with Python
- Working with HomeAssistant YAML configuration files
- Implementing automations that require custom sensors or components
- Setting up device integrations or API connections

## Core Capabilities

### 1. Custom Sensors

#### Template Sensors
Use template sensors for calculations, unit conversions, or combining multiple sensor values. Templates use Jinja2 syntax and are defined in YAML configuration.

**When to use:**
- Converting units (e.g., Celsius to Fahrenheit)
- Combining multiple sensor values (e.g., total power consumption)
- Creating derived values (e.g., "feels like" temperature)
- Status indicators based on other entity states

**Implementation approach:**
1. Determine the source entities needed
2. Write the Jinja2 template with proper fallback values using `| float(0)` or `| default()`
3. Set appropriate `device_class`, `state_class`, and `unit_of_measurement`
4. Add `unique_id` for UI customization capability
5. Test the template in Developer Tools → Template

**Reference:** See `references/sensors.md` for comprehensive template sensor examples and patterns.

#### RESTful Sensors
Use REST sensors to pull data from external APIs or web services.

**When to use:**
- Fetching data from external APIs
- Integrating web services without custom components
- Polling HTTP endpoints for status updates

**Implementation approach:**
1. Identify the API endpoint and authentication method
2. Configure the REST sensor with proper headers and authentication
3. Use `value_template` to extract the desired value from JSON responses
4. Use `json_attributes` or `json_attributes_path` for additional data
5. Set appropriate `scan_interval` to balance freshness and API limits

**Reference:** See `references/sensors.md` for REST sensor configuration patterns.

#### Command Line Sensors
Use command line sensors to execute shell commands and use their output as sensor values.

**When to use:**
- Reading system information not available through standard integrations
- Executing custom scripts or binaries
- Processing file contents or system resources

**Reference:** See `references/sensors.md` for command line sensor examples.

#### Python Custom Component Sensors
Use custom Python components when sensor logic is too complex for templates or requires external libraries.

**When to use:**
- Complex calculations or data processing
- Integration with Python libraries
- Stateful sensors that need to maintain data between updates
- Performance-critical operations

**Implementation approach:**
1. Create directory structure: `custom_components/<domain>/`
2. Start with the integration template in `assets/integration_template/`
3. Implement `sensor.py` with proper entity classes
4. Use `DataUpdateCoordinator` for efficient data fetching
5. Implement proper error handling and logging

**Reference:** See `references/sensors.md` for Python sensor implementation details.

### 2. Lovelace Dashboards

Create intuitive, responsive user interfaces using Lovelace cards and custom layouts.

#### Planning a Dashboard
**Approach:**
1. Identify the entities to display (lights, sensors, switches, etc.)
2. Group related entities by room or function
3. Choose appropriate card types for each entity type
4. Consider mobile vs desktop layout
5. Plan views (tabs) for different areas or purposes

#### Core Card Types

**Entities Card** - List multiple entities with controls:
- Best for control panels and grouped controls
- Supports sections, dividers, and custom icons
- Can show secondary information (last-changed, entity-id)

**Button Card** - Single entity with large tap target:
- Best for frequently-used controls
- Customizable icons and colors
- Supports tap, hold, and double-tap actions

**Gauge Card** - Visual representation of numeric values:
- Best for monitoring metrics (CPU, temperature, battery)
- Configure min/max and severity thresholds
- Visual feedback at a glance

**Picture Elements Card** - Interactive image with overlays:
- Best for floor plans or device diagrams
- Position controls and labels on images
- Create custom visual interfaces

**Conditional Card** - Show/hide based on conditions:
- Display cards only when relevant
- Reduce clutter by hiding inactive elements
- Stack multiple conditions for complex logic

#### Layout Strategies

**Grid Layout** - Responsive grid of cards:
- Automatically adjusts columns based on screen width
- Consistent sizing with `square: false` for flexible heights
- Best for collections of similar items

**Vertical/Horizontal Stack** - Group cards together:
- Stack cards to create logical groupings
- Combine with conditional cards for dynamic layouts
- Control card order and spacing

#### Custom Cards (HACS)
Install custom cards via HACS for enhanced functionality:
- **Mini Graph Card** - Compact sensor history graphs
- **Button Card (Custom)** - Advanced button customization
- **Mushroom Cards** - Modern, minimalist card designs
- **ApexCharts Card** - Powerful charting and graphing

**Installation steps:**
1. Install HACS if not already installed
2. Go to HACS → Frontend
3. Search for the desired card
4. Install and add resource reference
5. Use in dashboard with `type: custom:<card-name>`

**Reference:** See `references/dashboards.md` for comprehensive card examples, custom card configurations, and layout patterns.

### 3. Custom Integrations

Develop full-featured integrations with Python for complex device or service integrations.

#### When to Create a Custom Integration
- Integrating a device or service not supported by existing integrations
- Complex logic that can't be handled by REST sensors or templates
- Multiple related entities (sensors, switches, lights) from one source
- Need for device registry integration
- Requiring coordinator-based efficient data fetching

#### Integration Structure

**Required files:**
- `manifest.json` - Integration metadata, dependencies, and requirements
- `__init__.py` - Integration setup and platform loading
- `config_flow.py` - UI-based configuration (recommended)
- Platform files (`sensor.py`, `switch.py`, etc.) - Entity implementations

**Optional but recommended:**
- `coordinator.py` - Centralized data fetching
- `const.py` - Constants and configuration keys
- `strings.json` - UI text and translations

#### Development Workflow

**Step 1: Plan the Integration**
- Identify the device/service API or protocol
- List the entity types needed (sensors, switches, lights, etc.)
- Determine authentication and connection requirements
- Plan data update strategy (polling vs push)

**Step 2: Start with Template**
Copy the integration template from `assets/integration_template/` to `custom_components/<your_domain>/`:
```bash
cp -r assets/integration_template custom_components/my_device
```

**Step 3: Customize Manifest**
Update `manifest.json`:
- Set unique `domain` (lowercase, underscores)
- Update `name`, `documentation`, `codeowners`
- Add Python package dependencies to `requirements`
- Set appropriate `iot_class` (local_polling, cloud_polling, etc.)

**Step 4: Implement Config Flow**
In `config_flow.py`:
- Define configuration schema (host, port, API key, etc.)
- Implement connection validation in `_test_connection`
- Handle errors appropriately (cannot_connect, invalid_auth, etc.)
- Support discovery if applicable (SSDP, Zeroconf)

**Step 5: Implement Coordinator**
In `coordinator.py`:
- Create API client or device communication class
- Implement `_async_update_data` to fetch device data
- Handle errors and raise `UpdateFailed` on failures
- Set appropriate `update_interval`

**Step 6: Implement Platforms**
For each platform (sensor.py, switch.py, etc.):
- Create entity classes inheriting from `CoordinatorEntity` and platform base
- Set proper device classes, state classes, and units
- Implement `native_value` property to return current state
- Add `DeviceInfo` to group entities under one device
- Set `unique_id` for each entity

**Step 7: Test and Iterate**
- Copy to HomeAssistant's `custom_components/` directory
- Restart HomeAssistant
- Add integration via UI (Settings → Devices & Services)
- Monitor logs for errors
- Test all entity states and controls
- Verify device registry entry

#### Best Practices

**Data Fetching:**
- Always use `DataUpdateCoordinator` to centralize API calls
- This prevents multiple entities from making duplicate requests
- Coordinator automatically handles retries and error states

**Error Handling:**
- Use try/except blocks around all I/O operations
- Log errors with appropriate severity levels
- Raise `UpdateFailed` in coordinator when data fetch fails
- Return `None` or fallback values for unavailable data

**Entity Design:**
- Always set `unique_id` to enable UI customization
- Use appropriate `device_class` for proper icon and unit handling
- Set `state_class` for sensors that should appear in statistics
- Group related entities using `DeviceInfo`

**Code Quality:**
- Use type hints throughout (`-> bool`, `: str`, etc.)
- Follow HomeAssistant code style (use pylint)
- Use async/await for all I/O operations
- Import only necessary modules

**Configuration:**
- Prefer `config_flow.py` over YAML configuration
- Validate user input before accepting
- Provide clear error messages
- Support reloading configuration when possible

**Reference:** See `references/integrations.md` for complete integration development guide with detailed code examples.

## Resources

### references/
Detailed documentation loaded into context as needed:

- `sensors.md` - Comprehensive sensor implementation guide covering all sensor types, device classes, state classes, and best practices
- `dashboards.md` - Complete Lovelace dashboard reference with card types, custom cards, layouts, and design patterns
- `integrations.md` - In-depth custom integration development guide with file structure, coordinator patterns, and platform implementation

**When to read references:**
- Read `sensors.md` when implementing any type of sensor
- Read `dashboards.md` when building or modifying dashboards
- Read `integrations.md` when developing custom Python integrations

### assets/
Template files used in development output:

- `integration_template/` - Complete, working integration boilerplate with:
  - `manifest.json` - Integration metadata template
  - `__init__.py` - Integration setup with coordinator
  - `config_flow.py` - UI configuration flow
  - `coordinator.py` - Data update coordinator
  - `sensor.py` - Example sensor platform with multiple sensors
  - `const.py` - Constants file
  - `strings.json` - UI translations
  - `README.md` - Customization guide

**When to use assets:**
- Copy `integration_template/` as starting point for new integrations
- Customize the template by replacing "my_integration" with actual domain
- Follow the README.md for step-by-step customization instructions

## Development Tips

### Testing Templates
Use Developer Tools → Template in HomeAssistant to test Jinja2 templates before adding to configuration.

### Checking Configuration
Run Configuration → Check Configuration before restarting HomeAssistant to catch YAML errors.

### Viewing Logs
Monitor logs at Settings → System → Logs or via command line:
```bash
tail -f /config/home-assistant.log
```

### Reloading Without Restart
Many components support reload without full restart:
- Developer Tools → YAML → Reload Template Entities
- Developer Tools → YAML → Reload Automations
- Developer Tools → YAML → Reload Scripts

### Debugging Custom Integrations
Add debug logging to `configuration.yaml`:
```yaml
logger:
  default: info
  logs:
    custom_components.my_integration: debug
```

### Version Compatibility
Always check HomeAssistant version compatibility:
- Template syntax may change between versions
- Entity platform APIs evolve with releases
- Test integrations on target HomeAssistant version
- Review breaking changes in release notes
