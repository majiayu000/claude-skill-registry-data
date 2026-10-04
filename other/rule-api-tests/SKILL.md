---
name: rule-api-tests
description: MANDATORY when editing files matching ["api/tests/**/*.py"]. When writing or modifying API tests in api/tests/
---

# API Testing Rules

## Factory Patterns

ALWAYS request the `enable_factory_create` fixture in any test that calls `Factory.create()`. NEVER call `Factory.create()` without it.

ALWAYS use `Factory.build()` when the test does not need persisted database records. NEVER use `.create()` for in-memory-only logic.

```python
# From api/tests/src/services/test_validation.py
def make_application(attachments=None, forms=None):
    app = ApplicationFactory.build()
    app.application_attachments = attachments or []
    return app
```

NEVER call `db_session.commit()` after `Factory.create()`. The factory already commits internally.

NEVER hardcode values the factory generates. ALWAYS reference the factory object attribute instead.

## Test Structure

ALWAYS write tests as standalone `def test_*()` functions. NEVER wrap in a class unless sharing `scope="class"` fixtures or inheriting `BaseTestClass`.

ALWAYS structure route tests as: (1) create data via factories, (2) HTTP request, (3) assert status code first, (4) assert body. ALWAYS convert UUIDs to strings when comparing with JSON.

```python
# From api/tests/src/api/opportunities/test_opportunity_routes.py
def test_opportunity_get_200(client, enable_factory_create, user_auth_token):
    opportunity = OpportunityFactory.create()
    response = client.get(
        f"/v1/opportunities/{opportunity.opportunity_id}",
        headers={"X-SGG-Token": user_auth_token},
    )
    assert response.status_code == 200
    assert response.get_json()["data"]["opportunity_id"] == str(
        opportunity.opportunity_id
    )
```

ALWAYS separate service-layer tests from route tests into dedicated files. Service tests MUST call the Python function directly and use `pytest.raises`. Route tests MUST use the `client` fixture.

## Auth in Tests

ALWAYS use `headers={"X-API-Key": user_api_key_id}` for general access or `headers={"X-SGG-Token": user_auth_token}` for user-authenticated endpoints. NEVER use the legacy `headers={"X-Auth": api_auth_token}` in new tests.

## Framework and Query Style

ALWAYS use pytest conventions. NEVER use `unittest.TestCase` or `setUp()`/`tearDown()`.

ALWAYS use SQLAlchemy 2.0 `select()` style. NEVER use `db_session.query()`.

```python
# From api/tests/src/api/users/test_user_routes.py
user_profile = db_session.execute(
    select(UserProfile).where(UserProfile.user_id == user_id)
).scalar_one_or_none()
```

## Error Testing

ALWAYS test both success (200/201) and error paths (401, 403, 404, 422). Each error scenario MUST have its own test function.

ALWAYS check APIFlask errors via `exc_info.value.status_code` and `exc_info.value.message`. NEVER use the `match` parameter of `pytest.raises` for APIFlask `HTTPError`.

```python
# From api/tests/src/services/workflows/test_ingest_workflow_event.py
with pytest.raises(apiflask.exceptions.HTTPError) as exc_info:
    ingest_workflow_event(db_session, payload)
assert exc_info.value.status_code == 404
assert exc_info.value.message == "The specified resource was not found"
```

## Test Data and Cleanup

NEVER add `cascade_delete_from_db_table` unless the test requires a clean-slate table. ALWAYS rely on transaction isolation.

ALWAYS use `@pytest.mark.parametrize` for testing the same logic with multiple inputs. NEVER duplicate test functions for input variations.

```python
# From api/tests/src/api/applications/test_application_forms.py
@pytest.mark.parametrize(
    "application_response,expected_warnings",
    [
        ({}, [{"field": "$", "message": "'name' is a required property"}]),
        ({"name": "bob", "age": 500}, [{"field": "$.age"}]),
        ({"name": "bob", "age": 50, "extra": ""}, []),
    ],
)
def test_form_update_warnings(
    client, enable_factory_create, application_response, expected_warnings
):
    ...
```

## Naming and Organization

ALWAYS name route tests as `test_<resource>_<action>_<scenario>_<status_code>`. ALWAYS name service tests as `test_<action>_<scenario>`.

ALWAYS define helpers, constants, and module-level factory builds at the top of the file. NEVER interleave helper definitions between test functions.

ALWAYS use comment banners to group related tests in files with 10+ test functions.

```python
# ========================================
# Start Workflow Validation Tests
# ========================================
```

## Fixtures and Resources

ALWAYS use `scope="session"` for expensive resources (search clients, index aliases, RSA keys). ALWAYS use `monkeypatch_session` for session-scoped env vars.

```python
# From api/tests/conftest.py
@pytest.fixture(scope="session")
def agency_index_alias(search_client, monkeypatch_session):
    alias = f"test-agency-index-alias-{uuid.uuid4().int}"
    monkeypatch_session.setenv("AGENCY_SEARCH_INDEX_ALIAS", alias)
    return alias
```

## Infrastructure and Mocking

ALWAYS test against real infrastructure (Postgres, OpenSearch, LocalStack). NEVER mock database or search operations. ONLY mock external third-party services (login.gov, AWS Pinpoint).

## Task Testing

ALWAYS assert task metrics via `task.metrics[task.Metrics.METRIC_NAME]` after running background tasks. NEVER verify task behavior only by querying the database.

```python
# From api/tests/src/task/test_build_opportunities.py
task = BuildAutomaticOpportunities(db_session, form_ids)
task.run()
assert task.metrics[task.Metrics.OPPORTUNITY_CREATED_COUNT] == 20
assert task.metrics[task.Metrics.OPPORTUNITY_ALREADY_EXIST_COUNT] == 0
```

## Shared Utilities

ALWAYS extract complex setup logic used across multiple test files into `tests/lib/` modules. ALWAYS add a docstring explaining the utility's purpose.

---

## Context Enrichment

When generating significant test code (new test suite, complex test fixtures, multi-file test changes), enrich your context:
- Call `get_rules_for_file("[file being tested]")` from the `simpler-grants-context` MCP server to understand the conventions the code under test should follow
- Call `get_rule_detail("api-routes")` or `get_rule_detail("api-services")` for the patterns being tested
- Consult **Compound Knowledge** for indexed documentation on test patterns, factory usage, and fixture conventions

## Related Rules

When writing API tests, also consult these related rules:
- **`api-routes.mdc`** — understand decorator stack and response patterns for route tests
- **`api-services.mdc`** — understand service signatures and query patterns for service tests
- **`api-database.mdc`** — understand model conventions for factory definitions
- **`api-error-handling.mdc`** — understand error patterns for error path tests
- **`cross-domain.mdc`** — factory `.build()` vs `.create()` decision, structured logging assertions

**Debugging:** Invoke the debugging agent (or use `/debug`) to diagnose failing tests — it will trace through the code under test and identify root causes.

## Specialist Validation

When generating or significantly modifying API tests:

**For simple changes (adding a single test function):**
No specialist invocation needed — the directives in this rule file are sufficient.

**For moderate changes (new test suite, new fixture pattern):**
Invoke `codebase-conventions-reviewer` to validate against test conventions.

**For complex changes (new test infrastructure, shared utility modules, complex parametrize):**
Invoke the following specialists (run in parallel where possible):
- `performance-oracle` — validate test efficiency (unnecessary `.create()`, fixture scoping, DB overhead)
- `codebase-conventions-reviewer` — validate test structure and naming conventions
- `kieran-python-reviewer` — Python-specific quality review for test patterns

<!-- Hook enforcement: test-pattern-checker validates testing conventions -->
