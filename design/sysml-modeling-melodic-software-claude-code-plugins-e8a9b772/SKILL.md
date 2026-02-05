---
name: sysml-modeling
description: Systems Modeling Language (SysML) for systems engineering and complex system design
allowed-tools: Read, Glob, Grep, Write, Edit
---

# SysML Modeling Skill

## When to Use This Skill

Use this skill when:

- **Sysml Modeling tasks** - Working on systems modeling language (sysml) for systems engineering and complex system design
- **Planning or design** - Need guidance on Sysml Modeling approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Systems Modeling Language (SysML) for Model-Based Systems Engineering (MBSE) and complex system design.

## MANDATORY: Documentation-First Approach

Before creating SysML models:

1. **Invoke `docs-management` skill** for systems engineering patterns
2. **Verify SysML 2.0 syntax** via MCP servers
3. **Base all guidance on OMG SysML specification**

## SysML vs UML

| Aspect | UML | SysML |
|--------|-----|-------|
| Focus | Software systems | Systems of all types |
| Requirements | Not included | First-class diagrams |
| Structure | Classes, Components | Blocks, Parts |
| Parametrics | Not included | Constraint blocks |
| Allocation | Not included | Allocation relationships |
| Domain | Software engineering | Systems engineering |

## SysML Diagram Types

### Behavior Diagrams

| Diagram | Purpose | From UML |
|---------|---------|----------|
| Activity | Flow of actions and data | Extended |
| Sequence | Object interactions over time | Same |
| State Machine | Lifecycle behavior | Same |
| Use Case | System-actor interactions | Same |

### Structure Diagrams

| Diagram | Purpose | SysML Specific |
|---------|---------|----------------|
| Block Definition (BDD) | System structure hierarchy | Yes |
| Internal Block (IBD) | Internal component connections | Yes |
| Package | Model organization | Extended |

### Requirements Diagrams

| Diagram | Purpose | SysML Specific |
|---------|---------|----------------|
| Requirements | Requirements and relationships | Yes |
| Parametric | Constraint equations | Yes |

## Requirements Diagram

### PlantUML Syntax

```plantuml
@startuml
skinparam rectangle {
  BackgroundColor<<requirement>> LightBlue
  BackgroundColor<<testCase>> LightGreen
}

rectangle "<<requirement>>\nREQ-001: System Performance" as REQ001 {
  id = "REQ-001"
  text = "System shall process 1000 requests/second"
  risk = "High"
  verifyMethod = "Test"
}

rectangle "<<requirement>>\nREQ-002: Response Time" as REQ002 {
  id = "REQ-002"
  text = "System shall respond within 100ms (p95)"
  risk = "Medium"
  verifyMethod = "Test"
}

rectangle "<<requirement>>\nREQ-003: Availability" as REQ003 {
  id = "REQ-003"
  text = "System shall achieve 99.9% uptime"
  risk = "High"
  verifyMethod = "Analysis"
}

rectangle "<<testCase>>\nTC-001: Load Test" as TC001 {
  id = "TC-001"
  verifies = "REQ-001, REQ-002"
}

REQ001 <-- REQ002 : <<deriveReqt>>
REQ001 <-- REQ003 : <<deriveReqt>>
REQ002 <.. TC001 : <<verify>>
REQ001 <.. TC001 : <<verify>>

@enduml
```

### Requirements Relationships

```text
<<deriveReqt>>    Derived requirement (child from parent)
<<refine>>        Element refines requirement
<<satisfy>>       Design element satisfies requirement
<<verify>>        Test case verifies requirement
<<trace>>         General traceability
<<copy>>          Requirement copied (reuse)
<<containment>>   Nested requirement
```

## Block Definition Diagram (BDD)

### PlantUML Syntax

```plantuml
@startuml
skinparam class {
  BackgroundColor<<block>> LightYellow
  BackgroundColor<<valueType>> LightGreen
}

class "<<block>>\nVehicleSystem" as Vehicle {
  values
  --
  + maxSpeed: Speed
  + weight: Mass
  + range: Distance
  operations
  --
  + start()
  + stop()
  + accelerate(targetSpeed: Speed)
}

class "<<block>>\nPowertrainSubsystem" as Powertrain {
  values
  --
  + power: Power
  + efficiency: Real
  parts
  --
  + engine: Engine[1]
  + transmission: Transmission[1]
}

class "<<block>>\nEngine" as Engine {
  values
  --
  + displacement: Volume
  + cylinders: Integer
  + fuelType: FuelType
  operations
  --
  + ignite()
  + shutoff()
}

class "<<block>>\nTransmission" as Transmission {
  values
  --
  + gearRatios: Real[6]
  + currentGear: Integer
  operations
  --
  + shiftUp()
  + shiftDown()
}

class "<<block>>\nChassisSubsystem" as Chassis {
  parts
  --
  + wheels: Wheel[4]
  + suspension: Suspension[4]
  + brakes: BrakeSystem[1]
}

class "<<valueType>>\nSpeed" as Speed {
  unit = km/h
}

class "<<valueType>>\nMass" as Mass {
  unit = kg
}

class "<<enumeration>>\nFuelType" as FuelType {
  Gasoline
  Diesel
  Electric
  Hybrid
}

Vehicle *-- Powertrain : <<block>>
Vehicle *-- Chassis : <<block>>
Powertrain *-- Engine
Powertrain *-- Transmission
Engine --> FuelType

@enduml
```

### Block Stereotypes

```text
<<block>>           System element (hardware, software, human)
<<constraintBlock>> Parametric constraint
<<valueType>>       Type with unit
<<flowPort>>        Flow of matter/energy/data
<<proxy>>           Proxy for external element
<<full>>            Full internal access
```

## Internal Block Diagram (IBD)

### PlantUML Syntax

```plantuml
@startuml
skinparam component {
  BackgroundColor<<part>> LightYellow
}

package "VehicleSystem [IBD]" {
  component "powertrain : PowertrainSubsystem" as powertrain <<part>> {
    portin "fuelIn" as p_fuel
    portout "torqueOut" as p_torque
    portout "heatOut" as p_heat
  }

  component "chassis : ChassisSubsystem" as chassis <<part>> {
    portin "torqueIn" as c_torque
    portout "motionOut" as c_motion
  }

  component "cooling : CoolingSubsystem" as cooling <<part>> {
    portin "heatIn" as cool_heat
    portout "coolantOut" as cool_out
  }

  component "fuelSystem : FuelSubsystem" as fuel <<part>> {
    portout "fuelOut" as f_out
  }

  ' Connections (item flows)
  f_out --> p_fuel : <<itemFlow>>\nfuel: Fuel
  p_torque --> c_torque : <<itemFlow>>\ntorque: Torque
  p_heat --> cool_heat : <<itemFlow>>\nheat: ThermalEnergy
}

@enduml
```

## Parametric Diagram

### Constraint Blocks

```plantuml
@startuml
skinparam class {
  BackgroundColor<<constraintBlock>> LightCoral
}

class "<<constraintBlock>>\nNewtonSecondLaw" as Newton {
  constraints
  --
  { F = m * a }
  parameters
  --
  F: Force
  m: Mass
  a: Acceleration
}

class "<<constraintBlock>>\nKineticEnergy" as KE {
  constraints
  --
  { E = 0.5 * m * v^2 }
  parameters
  --
  E: Energy
  m: Mass
  v: Velocity
}

class "<<constraintBlock>>\nRangeEquation" as Range {
  constraints
  --
  { R = (fuelCapacity * efficiency) / consumption }
  parameters
  --
  R: Distance
  fuelCapacity: Volume
  efficiency: Real
  consumption: VolumePerDistance
}

@enduml
```

### Parametric Usage

```plantuml
@startuml
package "VehiclePerformance [Parametric]" {
  object "newton : NewtonSecondLaw" as n {
    F = thrustForce
    m = vehicleMass
    a = acceleration
  }

  object "energy : KineticEnergy" as e {
    E = kineticEnergy
    m = vehicleMass
    v = velocity
  }

  object "vehicle : Vehicle" as v {
    mass = 1500 kg
    thrust = 5000 N
  }

  n::m --> v::mass
  n::F --> v::thrust
  e::m --> v::mass
}

@enduml
```

## Activity Diagram (Enhanced)

### SysML Extensions

```plantuml
@startuml
title Vehicle Start Sequence [Activity]

start

:Receive Start Command;
note right: <<objectFlow>>\nStartRequest

fork
  :Validate Key Fob;
fork again
  :Check Safety Interlocks;
end fork

if (Valid?) then (yes)
  :Power On ECU;

  fork
    :Initialize Engine;
    :<<allocate>>\nEngine ECU;
  fork again
    :Initialize Transmission;
    :<<allocate>>\nTransmission ECU;
  fork again
    :Initialize Dashboard;
    :<<allocate>>\nBody Control Module;
  end fork

  :Start Engine;
  :<<objectFlow>>\nEngineStatus = Running;

  :Report Ready;
else (no)
  :Report Error;
  :<<objectFlow>>\nErrorCode;
endif

stop

@enduml
```

### Object Flow and Control Flow

```text
Control Flow: Sequence of actions (solid arrow)
Object Flow: Data/material flow (dashed arrow with <<objectFlow>>)
Rate: Flow rate specification { rate = 100/sec }
Probability: Branch probability { probability = 0.8 }
Streaming: Continuous flow { streaming }
```

## Allocation

### Allocation Relationships

```plantuml
@startuml
skinparam rectangle {
  BackgroundColor<<requirement>> LightBlue
  BackgroundColor<<block>> LightYellow
  BackgroundColor<<activity>> LightGreen
}

rectangle "<<requirement>>\nREQ-001: Process Orders" as R1

rectangle "<<activity>>\nProcessOrder" as A1

rectangle "<<block>>\nOrderProcessor" as B1

R1 <.. A1 : <<satisfy>>
A1 <.. B1 : <<allocate>>

note bottom of B1
  Function ProcessOrder
  is allocated to block
  OrderProcessor
end note

@enduml
```

### Allocation Matrix

```text
| Function/Behavior | Allocated To (Block) |
|-------------------|----------------------|
| ProcessOrder      | OrderProcessor       |
| ValidatePayment   | PaymentGateway       |
| ShipOrder         | FulfillmentSystem    |
| NotifyCustomer    | NotificationService  |
```

## C# Model Representation

```csharp
// SysML Block as C# class
public abstract class Block
{
    public string Name { get; init; }
    public IReadOnlyDictionary<string, object> Values { get; init; }
    public IReadOnlyList<Block> Parts { get; init; }
    public IReadOnlyList<Port> Ports { get; init; }
}

public sealed class VehicleSystem : Block
{
    // Value properties
    public Speed MaxSpeed { get; init; }
    public Mass Weight { get; init; }
    public Distance Range { get; init; }

    // Parts
    public PowertrainSubsystem Powertrain { get; init; }
    public ChassisSubsystem Chassis { get; init; }
    public CoolingSubsystem Cooling { get; init; }

    // Operations
    public void Start() { /* ... */ }
    public void Stop() { /* ... */ }
    public void Accelerate(Speed targetSpeed) { /* ... */ }
}

// Value Types with Units
public readonly record struct Speed(double Value, SpeedUnit Unit = SpeedUnit.KmPerHour)
{
    public static Speed FromKmPerHour(double value) => new(value, SpeedUnit.KmPerHour);
    public static Speed FromMilesPerHour(double value) =>
        new(value * 1.60934, SpeedUnit.KmPerHour);
}

public readonly record struct Mass(double Value, MassUnit Unit = MassUnit.Kilogram);
public readonly record struct Distance(double Value, DistanceUnit Unit = DistanceUnit.Kilometer);

// Constraint Block
public sealed class NewtonSecondLaw : IConstraint
{
    public Force CalculateForce(Mass mass, Acceleration acceleration)
        => new(mass.Value * acceleration.Value);

    public Acceleration CalculateAcceleration(Force force, Mass mass)
        => new(force.Value / mass.Value);
}

// Requirement
public sealed record Requirement(
    string Id,
    string Text,
    RiskLevel Risk,
    VerificationMethod VerifyMethod,
    IReadOnlyList<string> DerivedFrom,
    IReadOnlyList<string> SatisfiedBy,
    IReadOnlyList<string> VerifiedBy);

public enum RiskLevel { Low, Medium, High }
public enum VerificationMethod { Analysis, Inspection, Demonstration, Test }
```

## MBSE Workflow

When creating SysML models:

1. **Define Requirements**: Capture stakeholder needs in requirements diagrams
2. **Model Structure**: Create BDD for system decomposition
3. **Define Interfaces**: Use IBD for part connections and flows
4. **Specify Behavior**: Activity, sequence, and state diagrams
5. **Add Constraints**: Parametric diagrams for physics/math
6. **Allocate Functions**: Map behaviors to structural elements
7. **Trace & Verify**: Link requirements through to verification

## Best Practices

### Model Organization

```text
Model
├── 1_Requirements/
│   ├── StakeholderNeeds.req
│   ├── SystemRequirements.req
│   └── DerivedRequirements.req
├── 2_Structure/
│   ├── SystemContext.bdd
│   ├── SystemArchitecture.bdd
│   └── Subsystems/
│       ├── PowertrainStructure.bdd
│       └── PowertrainInternal.ibd
├── 3_Behavior/
│   ├── UseCases.uc
│   ├── SystemSequences.seq
│   └── StateMachines/
│       └── VehicleStates.stm
├── 4_Parametrics/
│   └── PerformanceConstraints.par
└── 5_Allocation/
    └── FunctionAllocation.alloc
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Block | PascalCase noun | VehicleSystem |
| Part | camelCase noun | powertrain |
| Port | camelCase + In/Out | fuelIn, torqueOut |
| Requirement | REQ-### | REQ-001 |
| Constraint | PascalCase equation | NewtonSecondLaw |

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
