---
name: api-patterns
description: Use when creating or modifying API endpoints. Provides REST conventions and error handling patterns for this project.
---

# API Patterns for Pet Adoption Center

## Endpoint Conventions
- GET /pets - List all pets
- GET /pets/{id} - Get single pet
- POST /pets - Create pet
- PUT /pets/{id} - Update pet
- DELETE /pets/{id} - Delete pet

## Response Format
Always return JSON with this structure:
```python
{
    "success": True,
    "data": {...},
    "error": None
}
```

## Error Handling
Use HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad request
- 404: Not found
- 500: Server error

## Example Endpoint
```python
@app.route('/pets', methods=['GET'])
def list_pets():
    try:
        pets = Pet.query.all()
        return jsonify(success=True, data=[p.to_dict() for p in pets])
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500
```
