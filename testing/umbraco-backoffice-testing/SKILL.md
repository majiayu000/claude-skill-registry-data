---
name: umbraco-backoffice-testing
description: >-
  Testing an Umbraco package in a browser: component tests of backoffice elements built on
  `@umbraco-cms/backoffice` (a controller host, the package's translations, fake contexts),
  and Playwright end-to-end tests on Umbraco's helpers (the package name, the environment
  variables the helpers read, login and run settings). Use when setting up, writing or
  reviewing a backoffice element test or a Playwright test for an Umbraco package. For test
  patterns beyond these (API mocking with MSW, trees, entity actions, test data builders),
  see the official Backoffice Testing Skills plugin.
---

# Testing an Umbraco package in a browser

`project-init` creates the test setups (its frontend tests and end-to-end tests steps). How to
shape a test is `bdd-specs`'s job. C# tests on Umbraco's integration test package are
`umbraco-dotnet-testing`'s.

The official Umbraco Backoffice Testing Skills plugin, if installed, has more patterns: element and context
tests (`umbraco-unit-testing`), mocked API responses (`umbraco-msw-testing`), and backoffice
journeys (`umbraco-e2e-testing`, `umbraco-playwright-testhelpers`, `umbraco-test-builders`).
Where it differs from this skill on package names, environment variables or setup, this skill
wins: it was checked against the published helpers.

The backoffice section was run against `@umbraco-cms/backoffice` 17.7.1 in Web Test Runner, and
the end-to-end snippets type-checked against `@umbraco-cms/acceptance-test-helpers` 17.7.1. The
environment variable names were checked at `release-17.7.1` and `release-18.2.1`.

## Backoffice element tests: a controller host and loaded translations

A test of an element built on `@umbraco-cms/backoffice` needs no import map. With Web Test
Runner's `nodeResolve: true`, the imports resolve from `node_modules` (`@umbraco-cms/backoffice`
as a dev dependency at the project's CMS version). The esbuild plugin needs the project's
`tsconfig.json`, or the decorators reach the browser untransformed and the test file fails
with a `SyntaxError`. Two things a plain Lit test doesn't need:

- **An Umbraco controller host.** Contexts and controllers (`UmbContextBase`,
  `consumeContext`, `observe`) attach to a host. Create the context on a test element that
  extends `UmbLitElement`, and put the element under test inside it. On a plain `<div>` the
  context's constructor throws `addUmbController is not a function`.
- **The package's translations, registered and loaded.** `this.localize.term(...)` renders
  the key (`readingTime_minutes`) until both are done: register the package's `localization`
  manifests with `umbExtensionsRegistry`, then call `umbLocalizationRegistry.loadLanguage`.
  The registry comes from `@umbraco-cms/backoffice/localization`, not
  `@umbraco-cms/backoffice/localization-api`.
  The strings load asynchronously, so wait for the text.

```ts
import { expect, fixture, html, waitUntil } from '@open-wc/testing';
import { customElement } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import { umbExtensionsRegistry } from '@umbraco-cms/backoffice/extension-registry';
import { umbLocalizationRegistry } from '@umbraco-cms/backoffice/localization';
import { manifests } from '../manifests.js';
import { ReadingTimeContext } from './reading-time.context.js';
import './reading-time-badge.element.js';

@customElement('test-host')
class TestHostElement extends UmbLitElement {}

describe('reading-time-badge', () => {
	before(() => {
		umbExtensionsRegistry.registerMany(manifests.filter((m) => m.type === 'localization'));
		umbLocalizationRegistry.loadLanguage('en');
	});

	it('shows the minutes from the context', async () => {
		const host = await fixture<TestHostElement>(html`<test-host></test-host>`);
		new ReadingTimeContext(host).setMinutes(3);
		const badge = document.createElement('reading-time-badge');
		host.appendChild(badge);

		await waitUntil(() => badge.shadowRoot?.textContent?.includes('3 min read'));
		expect(badge.shadowRoot!.textContent).to.contain('3 min read');
	});
});
```

To stand in for a context, write a fake that extends `UmbContextBase` with the same token
and create it on the host. A plain object passed to `provideContext` throws
`getHostElement is not a function`.

The CMS's own test utilities (`@umbraco-cms/internal/test-utils`) aren't published, so don't
import them.

## End-to-end tests: Umbraco's Playwright helpers

Umbraco's Playwright helpers (login, `umbracoApi` for test data, `umbracoUi` for the
backoffice, JSON builders) are published as **`@umbraco-cms/acceptance-test-helpers`**,
versioned with the CMS from 17.3. Install the version matching the site.

- **Not the old names.** `@umbraco/playwright-testhelpers` and `@umbraco/json-models-builders`
  are deprecated. The package's own README examples import from
  `@umbraco/acceptance-test-helpers`, which doesn't exist on npm. Import from
  `@umbraco-cms/acceptance-test-helpers`.
- **Configure through environment variables**, never committed: `URL` (the site's address;
  the helpers use it, not Playwright's `baseURL`, and it defaults to
  `https://localhost:44339`, the CMS repo's own port), `UMBRACO_USER_LOGIN`,
  `UMBRACO_USER_PASSWORD`, and `STORAGE_STATE_PATH`. The API helpers read their tokens from
  the storage state file, so `STORAGE_STATE_PATH` names the same file the setup saves.
  The helpers read no other names: `UMBRACO_URL` or `STORAGE_STAGE_PATH` is ignored, and the
  helpers fall back to the default address and no tokens.
- **Log in once**, in a setup project, and give the tests that state.
- **Run one test at a time** (`workers: 1`). Every test shares one site and database.
  Umbraco's own suite runs this way, and asks for SQL Server or LocalDb because SQLite can't
  keep up even then. On a SQLite demo site, keep runs serial.

```ts
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';
import 'dotenv/config';

export const STORAGE_STATE = process.env.STORAGE_STATE_PATH ?? 'playwright/.auth/user.json';

export default defineConfig({
	testDir: './tests',
	workers: 1,
	use: { baseURL: process.env.URL, ignoreHTTPSErrors: true, testIdAttribute: 'data-mark' },
	projects: [
		{ name: 'setup', testMatch: '**/*.setup.ts' },
		{
			name: 'e2e',
			testMatch: '**/*.spec.ts',
			dependencies: ['setup'],
			use: { ...devices['Desktop Chrome'], storageState: STORAGE_STATE },
		},
	],
});
```

```ts
// tests/auth.setup.ts
import { test as setup } from '@playwright/test';
import { UiHelpers } from '@umbraco-cms/acceptance-test-helpers';
import { STORAGE_STATE } from '../playwright.config';

setup('authenticate', async ({ page }) => {
	const umbracoUi = new UiHelpers(page);
	await umbracoUi.goToBackOffice();
	await umbracoUi.login.enterEmail(process.env.UMBRACO_USER_LOGIN!);
	await umbracoUi.login.enterPassword(process.env.UMBRACO_USER_PASSWORD!);
	await umbracoUi.login.clickLoginButtonAndWaitForBackOffice();
	await page.context().storageState({ path: STORAGE_STATE });
});
```

Tests then import `test` from the package and get `umbracoApi` and `umbracoUi` as fixtures.
The config loads `.env` with `dotenv` (a dev dependency). Keep `.env` and
`playwright/.auth/` out of git.

Source: `tests/Umbraco.Tests.AcceptanceTest/` in the CMS repo (`playwright.config.ts`,
`tests/auth.setup.ts`, `README.md`) and the package's `dist/umbraco.config.js` and
`dist/helpers/`.
