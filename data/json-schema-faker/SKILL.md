---
name: json-schema-faker
description: Generate realistic fake data from JSON schemas, producing 1-50 valid records that conform exactly to the schema. Use when creating sample datasets from schema definitions, populating test databases, or generating example API responses. Returns only valid JSON that passes schema validation.
---

# JSON Schema Faker Skill

Generate realistic fake data from JSON schemas with guaranteed validity.

## Quick Start

When you have a JSON schema and need realistic sample data:

```bash
node scripts/generate-fake-data.mjs /path/to/schema.json 25
```

This generates 25 valid records conforming to your schema.

## Requirements

Install dependencies first:

```bash
npm install @json-schema-faker/core ajv
```

## How It Works

1. **Parse schema** - Loads and validates your JSON schema
2. **Configure faker** - Sets up realistic data generation with custom rules
3. **Generate records** - Creates 1-50 records using faker
4. **Validate output** - Validates each record against the schema
5. **Return JSON** - Outputs only valid records as pretty-printed JSON

## Features

**Schema Compliance**: All generated records are validated against the schema—only valid JSON is returned.

**Realistic Data**: Uses faker.js with domain-specific extensions (currency codes, country codes, time windows) to produce realistic data beyond simple random strings.

**Customizable**: Specify 1-50 records. Script auto-caps at 50.

**Error Handling**: Handles generation failures gracefully; reports warnings for records that couldn't be generated after multiple attempts.

## Usage

### Basic Generation

```bash
node scripts/generate-fake-data.mjs schema.json 10
```

Generates 10 records from `schema.json`, outputs JSON to stdout.

### Specify Record Count

```bash
node scripts/generate-fake-data.mjs schema.json 50
```

Records are capped at 50 maximum. If omitted, defaults to 10.

### Save to File

```bash
node scripts/generate-fake-data.mjs schema.json 30 > output.json
```

## Improving Data Quality

The faker library generates realistic data based on schema hints. To improve data quality:

1. **Add format hints**: Use `"format": "email"`, `"format": "date"`, `"format": "uri"`
2. **Add faker directives**: Use `"faker": "name.firstName"` to guide generation
3. **Use enums**: For constrained fields, provide valid options
4. **Set constraints**: Use `minimum`, `maximum`, `minLength`, `maxLength` appropriately
5. **Avoid overly restrictive patterns**: Very complex regex patterns may cause generation to fail

See `references/faker-customization.md` for detailed customization options and available faker methods.

## Example: Accommodation Listings

Given a schema for accommodation listings (with faker hints for currency and country), the skill generates realistic data like:

```json
[
  {
    "id": "listing_ashdod_001",
    "title": "Beachfront Apartment",
    "type": "apartment",
    "location": {
      "city": "Ashdod",
      "countryCode": "IL",
      "distanceToBeachMinutes": 5,
      "coordinates": { "lat": 31.8, "lng": 34.65 }
    },
    "rating": { "score": 8.5, "count": 45 },
    "pricePreview": {
      "currency": "USD",
      "nightly": 180,
      "total": 540,
      "nights": 3
    },
    ...
  }
]
```

## Troubleshooting

**"Could not generate valid record"**: The schema may have constraints that conflict (e.g., minLength > maxLength). Review your schema constraints.

**"Failed to parse schema"**: Ensure the schema file is valid JSON.

**Too few records generated**: Some schemas have tight constraints. Increase attempts or relax schema constraints.

## Advanced Customization

To add custom faker methods beyond the built-in ones (currencyCode, countryCode, timeWindow), edit the `setupFaker()` function in `scripts/generate-fake-data.mjs`.

Example: Add a custom "accommodationType" method:

```javascript
faker.accommodationType = () => {
  const types = ['apartment', 'house', 'hotel', 'bnb']
  return faker.random.arrayElement(types)
}
```

Then use in your schema:

```json
{
  "type": "string",
  "faker": "accommodationType"
}
```
