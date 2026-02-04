---
name: test-scaffolder
description: Generate test boilerplate from code or specs. Use for creating new tests, setting up test files, pytest fixtures, page objects, and E2E test scaffolding.
---

# Test Scaffolder Skill

**Activation:** create test, new test file, test boilerplate, scaffold test, generate test, page object

## Overview

Generate test boilerplate for pytest (backend) and Playwright E2E tests. Follows project patterns from the `testing` skill.

**Note:** Frontend component testing (vitest) is not currently used. Testing is done via E2E tests (pytest + Playwright) with database verification.

> **CRITICAL: Container-First Execution**
>
> Backend test commands run in Docker, E2E runs on host:
> ```bash
> docker compose exec backend pytest /tests/unit/backend/
> pytest -m e2e tests/e2e/python/
> ```

## Pytest Unit Test Template

```python
# tests/unit/backend/services/test_{module}.py
"""Unit tests for {Module}Service."""
import pytest
from unittest.mock import Mock, AsyncMock

from app.services.{module} import {Module}Service


class Test{Module}Service:
    """Test cases for {Module}Service."""

    @pytest.fixture
    def service(self) -> {Module}Service:
        """Create service instance with mocked dependencies."""
        mock_repo = Mock()
        return {Module}Service(repository=mock_repo)

    def test_validate_input_success(self, service: {Module}Service) -> None:
        """Test input validation with valid data."""
        result = service.validate({"name": "test", "value": 42})
        assert result.is_valid is True

    def test_validate_input_failure(self, service: {Module}Service) -> None:
        """Test input validation with invalid data."""
        with pytest.raises(ValueError, match="Name cannot be empty"):
            service.validate({"name": "", "value": 42})

    @pytest.mark.parametrize("platform,expected", [
        ("nam", True),
        ("aida_x", True),
        ("invalid", False),
    ])
    def test_platform_validation(
        self,
        service: {Module}Service,
        platform: str,
        expected: bool,
    ) -> None:
        """Test platform validation against allowed values."""
        result = service.is_valid_platform(platform)
        assert result is expected
```

## Pytest Integration Test Template

```python
# tests/integration/backend/api/test_{endpoint}.py
"""Integration tests for {Endpoint} API."""
import pytest
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
@pytest.mark.integration
class Test{Endpoint}API:
    """Integration tests for {endpoint} endpoints."""

    async def test_create_success(
        self,
        client: AsyncClient,
        auth_headers: dict[str, str],
        test_user,
    ) -> None:
        """Test successful creation via POST."""
        response = await client.post(
            "/api/v1/{endpoint}",
            json={"name": "Test Item", "description": "Test"},
            headers=auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["id"] is not None
        assert data["name"] == "Test Item"
        assert data["user_id"] == str(test_user.id)

    async def test_get_by_id(
        self,
        client: AsyncClient,
        auth_headers: dict[str, str],
        make_{entity},
    ) -> None:
        """Test GET by ID returns correct entity."""
        entity = await make_{entity}(name="Existing Item")

        response = await client.get(
            f"/api/v1/{endpoint}/{entity.id}",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Existing Item"

    async def test_get_not_found(
        self,
        client: AsyncClient,
        auth_headers: dict[str, str],
    ) -> None:
        """Test GET with non-existent ID returns 404."""
        response = await client.get(
            f"/api/v1/{endpoint}/{uuid4()}",
            headers=auth_headers,
        )

        assert response.status_code == 404

    async def test_list_with_pagination(
        self,
        client: AsyncClient,
        auth_headers: dict[str, str],
        make_{entity},
    ) -> None:
        """Test list endpoint with pagination."""
        for i in range(5):
            await make_{entity}(name=f"Item {i}")

        response = await client.get(
            "/api/v1/{endpoint}?limit=2&offset=0",
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["{entities}"]) == 2
        assert data["total"] >= 5

    async def test_unauthorized_access(
        self,
        client: AsyncClient,
    ) -> None:
        """Test endpoint returns 401 without auth."""
        response = await client.get("/api/v1/{endpoint}")
        assert response.status_code == 401
```

## Pytest Factory Fixture Template

```python
# tests/integration/backend/conftest.py (add to existing)
@pytest.fixture(scope="function")
def make_{entity}(db_session: AsyncSession, test_user):
    """Factory fixture for creating {Entity} instances."""
    from app.models.{entity} import {Entity}

    async def _make_{entity}(
        name: str = "Test {Entity}",
        user=None,
        **kwargs,
    ) -> {Entity}:
        entity = {Entity}(
            id=uuid4(),
            user_id=(user or test_user).id,
            name=name,
            **kwargs,
        )
        db_session.add(entity)
        await db_session.flush()
        await db_session.refresh(entity)
        return entity

    return _make_{entity}
```

## Playwright Page Object Template (Python)

```python
# tests/e2e/python/pages/{page}_page.py
"""Page Object for {Page} page."""
from playwright.async_api import Page, expect


class {Page}Page:
    """Page Object for {Page} functionality."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

        # Locators
        self.heading = page.locator('[data-testid="{page}-heading"]')
        self.name_input = page.locator('[data-testid="form-name-input"]')
        self.submit_button = page.locator('[data-testid="submit-btn"]')
        self.error_message = page.locator('[data-testid="error-message"]')
        self.success_message = page.locator('[data-testid="success-message"]')
        self.item_list = page.locator('[data-testid="{entity}-list"]')

    async def goto(self) -> None:
        """Navigate to the page."""
        await self.page.goto(f"{self.base_url}/{path}")
        await expect(self.heading).to_be_visible()

    async def fill_form(self, name: str) -> None:
        """Fill the form with data."""
        await self.name_input.fill(name)

    async def submit(self) -> None:
        """Submit the form."""
        await self.submit_button.click()

    async def create_item(self, name: str) -> None:
        """Create a new item."""
        await self.fill_form(name)
        await self.submit()
        await expect(self.success_message).to_be_visible()

    async def expect_error(self, message: str) -> None:
        """Assert an error message is displayed."""
        await expect(self.error_message).to_be_visible()
        await expect(self.error_message).to_contain_text(message)

    async def expect_item_visible(self, name: str) -> None:
        """Assert an item is visible in the list."""
        await expect(self.item_list.get_by_text(name)).to_be_visible()
```

## Playwright E2E Test Template (Python)

```python
# tests/e2e/python/tests/test_{feature}.py
"""E2E tests for {Feature}."""
import pytest
from playwright.async_api import Page, expect
from sqlalchemy import text

from tests.e2e.python.pages.{page}_page import {Page}Page


@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.e2e_quick
class Test{Feature}E2E:
    """E2E tests for {Feature} functionality."""

    async def test_displays_page_correctly(
        self,
        page: Page,
        frontend_url: str,
    ) -> None:
        """Test page loads correctly."""
        {page}_page = {Page}Page(page, frontend_url)
        await {page}_page.goto()

        await expect({page}_page.heading).to_be_visible()
        await expect({page}_page.submit_button).to_be_enabled()

    async def test_creates_item_successfully(
        self,
        page: Page,
        db_session,
        frontend_url: str,
    ) -> None:
        """Test creating an item via UI and verifying in database."""
        {page}_page = {Page}Page(page, frontend_url)
        await {page}_page.goto()

        item_name = f"E2E-Test-{pytest.helpers.timestamp()}"
        await {page}_page.create_item(item_name)

        # LAYER 3: Verify database state
        result = await db_session.execute(
            text("SELECT id FROM {entities} WHERE name = :name"),
            {"name": item_name}
        )
        assert result.fetchone() is not None

    async def test_shows_validation_error(
        self,
        page: Page,
        frontend_url: str,
    ) -> None:
        """Test validation error for empty name."""
        {page}_page = {Page}Page(page, frontend_url)
        await {page}_page.goto()

        await {page}_page.fill_form("")
        await {page}_page.submit()
        await {page}_page.expect_error("Name is required")
```

## Quick Reference

| Test Type | Location | Template |
|-----------|----------|----------|
| Unit (backend) | `tests/unit/backend/` | Pytest class with fixtures |
| Integration (backend) | `tests/integration/backend/` | Pytest with real DB |
| E2E (Playwright) | `tests/e2e/python/tests/` | Python pytest specs |
| Page Objects | `tests/e2e/python/pages/` | Python page class pattern |

## Example Invocations

### Create Unit Test for Service
```
"Create unit tests for the AudioProcessingService"
-> Use Pytest Unit Test Template
-> Place in tests/unit/backend/services/test_audio_processing.py
```

### Create Integration Tests for API
```
"Scaffold integration tests for the /api/v1/shootouts endpoint"
-> Use Pytest Integration Test Template
-> Create factory fixture for shootout
-> Place in tests/integration/backend/api/test_shootouts.py
```

### Create Page Object for E2E
```
"Create a page object for the Signal Chain Builder page"
-> Use Page Object Template
-> Place in tests/e2e/python/pages/builder_page.py
-> Create matching test in tests/e2e/python/tests/test_builder.py
```

## Test Naming Conventions

| Convention | Example |
|------------|---------|
| Test file | `test_{module}.py` |
| Test class | `Test{Feature}` |
| Test method | `test_{action}_{expected_result}` |
| Page object | `{page}_page.py` |
| E2E test | `test_{feature}.py` |
