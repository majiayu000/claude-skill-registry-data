---
name: core/boolean-preference
description: >-
  Use createBooleanPreference when adding boolean preferences with paired
  set/toggle actions and reducer registration.
type: sub-skill
library: themis
requires:
  - core
  - core/reducers
sources:
  - "@themislib/themis/utils/store/boolean-preference"
  - ../SKILL.md
triggers:
  - boolean preference
  - toggle action
  - setAction toggleAction
  - register builder
---
# Boolean Preference — `createBooleanPreference`

Use this helper instead of hand-rolled set/toggle pairs. One factory owns the
namespaced actions and registers both reducer cases together.

## API

Public import: `@themislib/themis/utils/store/boolean-preference`.
`createBooleanPreference<S, Field>(options)` takes `sliceName`, `field`,
`setActionName`, and `toggleActionName`; `Field` defaults to the boolean keys of `S`.

- `field` must be a string key whose value type is strictly `boolean`.
- `setAction(value: boolean)` has tuple payload `[value]`.
- `toggleAction()` takes no arguments and flips the current value.
- Action types are `${sliceName}/${setActionName}` and
  `${sliceName}/${toggleActionName}`.
- `register(builder: BooleanPreferenceReducerBuilder<S>)` adds both handlers and
  returns the chainable builder, preserving `initialState`.
- Handlers update immutably. `createReducer` shallow-compares their result, so
  setting an already-equal flag preserves the incoming state reference.

## 2. Setup — minimum working slice

```typescript
import { createBooleanPreference } from "@themislib/themis/utils/store/boolean-preference";
import { createReducer } from "@themislib/themis/utils/store/create-reducer";

type SettingsState = { enabled: boolean; label: string };
const initialState: SettingsState = { enabled: false, label: "beta" };
```

```typescript
const enabledPreference = createBooleanPreference<SettingsState>({
  sliceName: "settings",
  field: "enabled",
  setActionName: "setEnabled",
  toggleActionName: "toggleEnabled",
});

export const settingsReducer = enabledPreference.register(createReducer(initialState));
export const { setAction: setEnabled, toggleAction: toggleEnabled } = enabledPreference;
```

Dispatch like any other action:

```typescript
store.dispatch(setEnabled(true));
store.dispatch(toggleEnabled());
```

## 3. Core patterns

### 3.2 Chaining multiple preferences

Each `.register(builder)` returns the same builder with two cases added, so you can compose any number of preferences:

```typescript
import { createBooleanPreference } from "@themislib/themis/utils/store/boolean-preference";
import { createReducer } from "@themislib/themis/utils/store/create-reducer";

type SettingsState = { darkMode: boolean; compactMode: boolean };
const initialState: SettingsState = { darkMode: false, compactMode: false };
const darkMode = createBooleanPreference<SettingsState>({
  sliceName: "settings", field: "darkMode", setActionName: "setDarkMode", toggleActionName: "toggleDarkMode",
});
const compactMode = createBooleanPreference<SettingsState>({
  sliceName: "settings", field: "compactMode", setActionName: "setCompactMode", toggleActionName: "toggleCompactMode",
});

export const settingsReducer = darkMode.register(
  compactMode.register(createReducer(initialState))
);
```

`.register` preserves the reducer's `initialState` field, so stores and tests can access `settingsReducer.initialState`.

### 3.3 Persistence saga

Pair the action with an app-local safe-storage helper, following `core/local-storage`, to persist the flag:

```typescript
import { call, takeEvery } from "typed-redux-saga";
import { setLocalStorageItem } from "../utils/safe-local-storage-saga";
import { setEnabled, toggleEnabled } from "./settings-actions";
import { selectEnabled } from "./settings-selectors";

const ENABLED_KEY = "settings/enabled";

function* persistEnabled() {
  const enabled = yield* selectEnabled.effect();
  yield* call(setLocalStorageItem, ENABLED_KEY, JSON.stringify(enabled));
}

export function* settingsPersistenceSaga() {
  yield* takeEvery([setEnabled, toggleEnabled], persistEnabled);
}
```

## 4. Common Mistakes

- Do not hand-roll a second set/toggle pair; it can drift from the factory's
  namespacing and handlers. See [API](#api).
- Register the preference before giving the reducer to the Store. Creating the
  actions alone installs no handlers, so dispatch would silently do nothing.
- Do not bypass the boolean-key constraint with `as any`; the handler would
  overwrite a non-boolean field with a boolean.
- Test set, toggle, unchanged-field preservation, and same-reference no-op sets
  through the registered reducer; see `core/testing`.

## 5. See also

- `core/reducers` — `createReducer` builder and the `same-reference on no-op` rule.
- `core/actions` — `createAction<[Params]>` tuple payloads.
- `core/local-storage` — persistence saga for preference fields.