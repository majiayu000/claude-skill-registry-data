---
name: notepad-new-api-endpoint
description: "Reference doc: New API Endpoint Checklist"
---

# New API Endpoint Checklist

Use this notepad when creating a new API endpoint in simpler-grants-gov.

## Files to Create/Modify

For a new domain `<domain>`:

| # | File | Purpose |
|---|------|---------|
| 1 | `api/src/api/<domain>_v1/<domain>_blueprint.py` | Blueprint registration |
| 2 | `api/src/api/<domain>_v1/<domain>_routes.py` | Route handlers |
| 3 | `api/src/api/<domain>_v1/<domain>_schemas.py` | Marshmallow schemas |
| 4 | `api/src/services/<domain>_v1/<domain>_<action>.py` | Business logic |
| 5 | `api/tests/src/api/<domain>/test_<domain>_routes.py` | Route tests |
| 6 | `api/tests/src/db/models/factories.py` | Factory (if new model) |
| 7 | `api/src/app.py` | Register blueprint |

## Decorator Stack Order (immutable)

```python
@blueprint.post("/path")                    # 1. HTTP method
@blueprint.input(RequestSchema)             # 2. Input schema
@blueprint.output(ResponseSchema)           # 3. Output schema
@blueprint.doc(responses=[...], security=...) # 4. Documentation
@jwt_or_api_user_key_multi_auth.login_required # 5. Auth
@flask_db.with_db_session()                 # 6. DB session
def handler(db_session, ...):
```

## Route Handler (keep it thin)

```python
def my_endpoint(db_session: db.Session, entity_id: UUID, json_data: dict) -> response.ApiResponse:
    result = my_service.do_action(db_session, entity_id, json_data)
    return response.ApiResponse(message="Success", data=result)
```

## Service Function

```python
def do_action(db_session: db.Session, entity_id: uuid.UUID, data: dict) -> MyModel:
    entity = db_session.execute(
        select(MyModel).where(MyModel.entity_id == entity_id)
    ).scalar_one_or_none()
    if entity is None:
        raise_flask_error(404, message="Entity not found")
    # Business logic here
    return entity
```

## Test Structure

```python
def test_endpoint_200(client, enable_factory_create, user_auth_token):
    entity = EntityFactory.create()
    resp = client.get(f"/v1/domain/{entity.entity_id}", headers={"X-SGG-Token": user_auth_token})
    assert resp.status_code == 200

def test_endpoint_404(client, user_auth_token):
    resp = client.get(f"/v1/domain/{uuid.uuid4()}", headers={"X-SGG-Token": user_auth_token})
    assert resp.status_code == 404
```

## Don't Forget

- [ ] Structured logging: static messages + `extra={"entity_id": str(entity_id)}`
- [ ] Error handling via `raise_flask_error()` with `ValidationErrorDetail`
- [ ] No PII in logs (use UUIDs)
- [ ] Boolean fields: `is_*`, `has_*` prefixes
- [ ] `db_session.begin()` at route layer, not in service
