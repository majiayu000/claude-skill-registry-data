---
name: value-objects
description: Analyze code for primitive obsession and plan value object extractions around domain concepts, validation, and grouped primitive fields. Use when the user says `/value-objects`, asks for value object refactoring, or runs `/refactor:value-objects`.
metadata:
  legacy-name: refactor:value-objects
---

Analyze the class provided in $ARGUMENTS for instances of primitive obsession and suggest value object extractions.

## Instructions:
1. Examine the given class for primitive types that represent domain concepts
2. Identify groups of related primitives that could be encapsulated into value objects
3. Look for common patterns that indicate primitive obsession:
    - Multiple string/number parameters representing a single concept (e.g., street, city, state, zip for an address)
    - Validation logic scattered throughout the class for primitive values
    - Methods that operate on groups of related primitives
    - Repeated primitive type combinations across methods
    - Business rules applied to primitive values

## Patterns to detect:
- **Money/Currency**: Variables like price, cost, amount, fee, salary with currency
- **Email**: String fields for email addresses lacking validation
- **Phone Numbers**: Strings or numbers representing phone data
- **Addresses**: Multiple fields like street, city, state, zipCode
- **Date Ranges**: Separate startDate/endDate fields
- **Coordinates**: Latitude/longitude pairs
- **Percentages**: Numeric values representing percentages
- **Identifiers**: Strings or numbers used as IDs
- **URLs**: String representations of URLs
- **Names**: Multiple fields like firstName, lastName, middleName

## Output format:
1. List each identified primitive obsession case
2. Suggest a value object name and structure
3. Provide a brief implementation example with:
    - Constructor with validation
    - Relevant methods (equality, toString, etc.)
    - Any domain-specific behavior
4. Show how to refactor the original class to use the value object
5. Explain the benefits of each extraction

Focus on improving code expressiveness, encapsulation, and type safety while reducing duplication and scattering of domain logic.
