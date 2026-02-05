---
name: energyplus-builder
description: "Generate EnergyPlus building simulations from natural language descriptions or building images. Use when user asks to 'create building simulation', 'generate IDF', 'simulate X-story building', provides building floor plans, 3D models, or describes buildings like 'a 3-story office building in Shenzhen'."
---

# EnergyPlus Building Simulation Skill

This skill automates the complete workflow from building description to EnergyPlus simulation results.

## Capabilities

1. Parse natural language building descriptions (Chinese/English)
2. Analyze building images (floor plans, 3D models) for geometry extraction
3. Generate compliant YAML configuration files
4. Execute YAML-to-IDF conversion with Pydantic validation
5. Run EnergyPlus simulations
6. Detect and auto-fix common errors
7. Output clean, validated YAML files

## Input Types

### Natural Language Examples
- "一栋三层的办公楼，复杂度：complex，地点位于深圳"
- "A 2-story residential building in Beijing, simple layout"
- "Create a medium complexity commercial building, 5 floors, 1000 m²"

### Image Types Supported
- Floor plans (2D layout drawings)
- 3D building models/renderings
- CAD exports

---

## Parameter Extraction Rules

When parsing user input, extract the following parameters:

| User Input Pattern | Parameter | Default Value |
|-------------------|-----------|---------------|
| "X层/楼/story/floor/level" | num_floors | 1 |
| "在[城市]/in [city]" | location | Shenzhen |
| "办公/住宅/商业/office/residential/commercial" | building_type | office |
| "complex/medium/simple" | complexity | medium |
| "X平方米/X m²/X sqm" | total_area | 500 m² |
| "朝北/朝南/facing north/south" | north_axis | 0 degrees |

---

## Complexity Levels

### Simple (每层最多3个热区)
- Zones per floor: 1-3
- Layout: Single zone or linear divisions
- Windows per exterior wall: 0-1
- Default zone area: 100 m²
- Ceiling height: 3.0 m
- No interior walls between zones

### Medium (每层最多8个热区和8个门窗)
- Zones per floor: 4-8
- Layout: Grid pattern (2x2, 2x3, 2x4)
- Windows per exterior wall: 1-2
- Default zone area: 50 m²
- Ceiling height: 3.2 m
- Interior walls between zones

### Complex (多热区及多门窗)
- Zones per floor: 9+
- Layout: Perimeter + core pattern
- Windows per exterior wall: 2-3
- Default zone area: 30 m²
- Ceiling height: 3.5 m
- Interior walls and doors

---

## City Location Database

```yaml
Shenzhen/深圳:
  Name: Shenzhen_GD_CHN Design_Conditions
  Latitude: 22.54
  Longitude: 114.00
  Time Zone: 8.00
  Elevation: 4.00

Beijing/北京:
  Name: Beijing_CHN Design_Conditions
  Latitude: 39.92
  Longitude: 116.46
  Time Zone: 8.00
  Elevation: 55.00

Shanghai/上海:
  Name: Shanghai_CHN Design_Conditions
  Latitude: 31.17
  Longitude: 121.43
  Time Zone: 8.00
  Elevation: 4.00

Guangzhou/广州:
  Name: Guangzhou_GD_CHN Design_Conditions
  Latitude: 23.13
  Longitude: 113.32
  Time Zone: 8.00
  Elevation: 11.00
```

---

## Workflow Instructions

### Step 1: Parse User Input

1. Extract building parameters from natural language or image
2. Determine complexity level (simple/medium/complex)
3. Set defaults for missing parameters

### Step 2: Calculate Building Geometry

Use the geometry rules from `./docs/geometry-rules.md`:

1. Calculate building footprint based on total area and number of floors
2. Subdivide into zones based on complexity level
3. Generate surface vertices for each zone (floor, ceiling/roof, walls)
4. Calculate window positions for exterior walls

### Step 3: Generate YAML File

Generate YAML following the structure in `./docs/yaml-schema-reference.md`:

```yaml
# Required sections in order:
SimulationControl:
Building:
Timestep:
Site:Location:
RunPeriod:
Material:
Construction:
GlobalGeometryRules:
Zone:
BuildingSurface:Detailed:
FenestrationSurface:Detailed:  # if windows exist
Schedule:
HVAC:
Output:VariableDictionary:
Output:Diagnostics:
Output:Table:SummaryReports:
OutputControl:Table:Style:
Output:Variable:
```

Save to: `schemas/generated_building_YYYYMMDD_HHMMSS.yaml`

### Step 4: Execute Pipeline

```bash
# Run the conversion and simulation pipeline
python main.py schemas/generated_building_XXXXXX.yaml dependencies/Shenzhen.epw
```

### Step 5: Check for Errors

1. **Pydantic Validation Errors**: Check console output for validation failures
2. **EnergyPlus Errors**: Check `.err` files in `output/results/energyplus_runs_*/`

Common error patterns and fixes are documented in `./docs/error-handling.md`.

### Step 6: Auto-Fix and Retry

If errors occur:
1. Parse error message to identify issue
2. Apply appropriate fix from error handling guide
3. Regenerate YAML with corrections
4. Re-run pipeline (maximum 3 retries)

### Step 7: Output Results

After successful simulation:
1. Report simulation success and output location
2. Clean the final YAML file (remove comments, format consistently)
3. Present the validated YAML to user

---

## YAML Generation Template

Use this template structure for generating YAML files:

```yaml
# ==================================================================
# Simulation Control
# ==================================================================
SimulationControl:
    Do Zone Sizing Calculation: No
    Do System Sizing Calculation: No
    Do Plant Sizing Calculation: No
    Run Simulation for Sizing Periods: No
    Run Simulation for Weather File Run Periods: Yes
    Do HVAC Sizing Simulation for Sizing Periods: Yes
    Maximum Number of HVAC Sizing Simulation Passes: 1

# ==================================================================
# Building
# ==================================================================
Building:
    Name: {building_name}
    North Axis: {north_axis}
    Terrain: {terrain}
    Loads Convergence Tolerance Value: 0.04
    Temperature Convergence Tolerance Value: 0.40
    Solar Distribution: FullInteriorAndExterior
    Maximum Number of Warmup Days: 25
    Minimum Number of Warmup Days: 6

# ==================================================================
# Timestep
# ==================================================================
Timestep:
    Number of Timesteps per Hour: 4

# ==================================================================
# Site Location
# ==================================================================
Site:Location:
    Name: {location_name}
    Latitude: {latitude}
    Longitude: {longitude}
    Time Zone: {time_zone}
    Elevation: {elevation}

# ==================================================================
# Run Period
# ==================================================================
RunPeriod:
    Name: Run Period 1
    Begin Month: 1
    Begin Day of Month: 1
    Begin Year: 2040
    End Month: 12
    End Day of Month: 31
    End Year: 2040
    Day of Week for Start Day: Tuesday
    Use Weather File Holidays and Special Days: Yes
    Use Weather File Daylight Saving Period: Yes
    Apply Weekend Holiday Rule: No
    Use Weather File Rain Indicators: Yes
    Use Weather File Snow Indicators: Yes

# ==================================================================
# Materials
# ==================================================================
Material:
  - Name: Concrete_20cm
    Type: Standard
    Roughness: MediumRough
    Thickness: 0.2
    Conductivity: 1.729
    Density: 2240
    Specific_Heat: 837

  - Name: Gypsum_1.3cm
    Type: Standard
    Roughness: Smooth
    Thickness: 0.0127
    Conductivity: 0.16
    Density: 785
    Specific_Heat: 830

  - Name: Interior_Insulation
    Type: NoMass
    Roughness: MediumRough
    Thermal_Resistance: 2.5

  - Name: SimpleGlazingSystem
    Type: Glazing
    U-Factor: 5.8
    Solar_Heat_Gain_Coefficient: 0.8
    Visible_Transmittance: 0.9

# ==================================================================
# Constructions
# ==================================================================
Construction:
  - Name: Exterior_Wall_Const
    Layers:
      - Concrete_20cm
  - Name: Interior_Wall_Const
    Layers:
      - Gypsum_1.3cm
      - Gypsum_1.3cm
  - Name: Roof_Const
    Layers:
      - Concrete_20cm
  - Name: Floor_Const
    Layers:
      - Concrete_20cm
  - Name: Ceiling_Const
    Layers:
      - Concrete_20cm
  - Name: Window_Const
    Layers:
      - SimpleGlazingSystem

# ==================================================================
# Global Geometry Rules
# ==================================================================
GlobalGeometryRules:
    Starting Vertex Position: UpperLeftCorner
    Vertex Entry Direction: Counterclockwise
    Coordinate System: World

# ==================================================================
# Zones (generate based on complexity)
# ==================================================================
Zone:
  # Generate zone entries based on complexity level

# ==================================================================
# Building Surfaces (generate for each zone)
# ==================================================================
BuildingSurface:Detailed:
  # Generate surfaces: Floor, Roof/Ceiling, 4 Walls per zone

# ==================================================================
# Fenestration Surfaces (if applicable)
# ==================================================================
FenestrationSurface:Detailed:
  # Generate windows on exterior walls

# ==================================================================
# Schedules
# ==================================================================
Schedule:
  ScheduleTypeLimits:
    - Name: On/Off
      Lower Limit Value: 0
      Upper Limit Value: 1
      Numeric Type: DISCRETE
      Unit Type: Dimensionless
    - Name: Temperature
      Numeric Type: CONTINUOUS
      Unit Type: Temperature
  Schedule:Compact:
    - Name: Always On
      Schedule Type Limits Name: On/Off
      Data:
        - Through: "12/31"
          Days:
          - For: "AllDays"
            Times:
            - Until:
                Time: "24:00"
                Value: 1
    - Name: Heating_Setpoint_Schedule
      Schedule Type Limits Name: Temperature
      Data:
        - Through: "12/31"
          Days:
          - For: "AllDays"
            Times:
            - Until:
                Time: "24:00"
                Value: 20
    - Name: Cooling_Setpoint_Schedule
      Schedule Type Limits Name: Temperature
      Data:
        - Through: "12/31"
          Days:
          - For: "AllDays"
            Times:
            - Until:
                Time: "24:00"
                Value: 26

# ==================================================================
# HVAC
# ==================================================================
HVAC:
  HVACTemplate:Thermostat:
    - Name: Ideal Loads Thermostat
      Heating Setpoint Schedule Name: Heating_Setpoint_Schedule
      Cooling Setpoint Schedule Name: Cooling_Setpoint_Schedule
  HVACTemplate:Zone:IdealLoadsAirSystem:
    # One entry per zone
    - Zone Name: {zone_name}
      Template Thermostat Name: Ideal Loads Thermostat
      System Availability Schedule Name: Always On

# ==================================================================
# Output Settings
# ==================================================================
Output:VariableDictionary:
    Key Field: regular
Output:Diagnostics:
    Key 1: DisplayExtraWarnings
Output:Table:SummaryReports:
    Report 1 Name: AllSummary
OutputControl:Table:Style:
    Column Separator: HTML
Output:Variable:
  - Key Value: "*"
    Variable Name: Zone Mean Air Temperature
    Reporting Frequency: Hourly
  - Key Value: "*"
    Variable Name: Surface Inside Face Temperature
    Reporting Frequency: Hourly
```

---

## Important Validation Rules

### Surface Vertices
- Each surface must have exactly 4 vertices (rectangular surfaces)
- Vertices must be specified counterclockwise when viewed from outside
- Minimum distance between vertices: 1e-10
- All surfaces in a zone must form a closed volume

### Interior Walls
- Interior walls connecting two zones must have paired surfaces
- Use `Outside Boundary Condition: Surface`
- Specify `Outside Boundary Condition Object` with paired surface name

### Boundary Conditions
| Surface Type | Typical Boundary Condition |
|-------------|---------------------------|
| Floor (ground level) | Ground |
| Floor (upper levels) | Surface (to ceiling below) |
| Roof | Outdoors |
| Ceiling | Surface (to floor above) |
| Exterior Wall | Outdoors |
| Interior Wall | Surface |

---

## Reference Files

For detailed specifications, refer to:
- `docs/yaml-schema-reference.md` - Complete field reference
- `docs/complexity-presets.md` - Complexity level configurations
- `docs/geometry-rules.md` - Vertex calculation formulas
- `docs/error-handling.md` - Error patterns and fixes
- `examples/` - Working YAML examples for each complexity level
