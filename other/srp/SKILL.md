---
name: srp
description: Refactor a class toward the Single Responsibility Principle by identifying responsibilities, grouping cohesive behavior, and extracting focused classes. Use when the user says `/srp`, asks for SRP refactoring, or runs `/refactor:srp`.
metadata:
  legacy-name: refactor:srp
---

Refactor the class provided in $ARGUMENTS to adhere to the Single Responsibility Principle by extracting classes and simplifying the design.

## Instructions:
1. Identify all responsibilities within the given class
2. Group related methods and properties by their cohesive purpose
3. Extract each responsibility into its own focused class
4. Consider alternative, simpler designs that make future changes easier
5. Ensure each resulting class has only one reason to change

## Analysis approach:
- **Identify responsibilities by**:
    - Methods that serve different actors/users
    - Distinct areas of functionality
    - Different reasons for change
    - Unrelated data and behavior groupings
    - Infrastructure vs domain logic separation
    - I/O operations vs business logic

## Common responsibility patterns to separate:
- Data persistence/storage from business logic
- Validation logic from core behavior
- Formatting/presentation from domain logic
- External service communication from internal logic
- Configuration from implementation
- Factory/creation logic from usage
- Orchestration/coordination from execution
- Logging/metrics from business operations

## Output format:
1. **Current responsibilities**: List each identified responsibility with supporting methods/properties
2. **Proposed class structure**:
    - Name and purpose of each extracted class
    - Methods and properties it would contain
    - Clear single responsibility statement
3. **Refactored design**: Show the transformed code structure
4. **Alternative designs**: Present 1-2 simpler alternatives if applicable
5. **Benefits**: Explain how each extraction improves:
    - Testability
    - Maintainability
    - Flexibility for change
    - Code clarity

## Design principles to apply:
- Prefer composition over inheritance
- Keep classes small and focused
- High cohesion within classes
- Low coupling between classes
- Clear, single purpose for each class
- Consider using interfaces for flexibility
