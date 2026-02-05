---
name: page
description: Guide for creating page components. This skill should be used when users want to create a new page component (or update an existing page component)
---

## File structure

Each page lives in its own folder under `src/pages/[name]/` and typically includes:

- `[name]-page.ts` - page component
- `[name]-page.stories.ts` - Storybook story (imports `./[name]-page.js`)

It can also include other assets like styles, sub-components, etc.

The page name and custom element tag should be kebab-case (e.g., `user-profile`).

## Page component

- Extend `LitElement` (or `withStore(LitElement)` when using store bindings) and register via `customElements.define('my-page', MyPage)`.
- Define styles in `static styles` and always include `BSHelpersCSS` in the array.
- Define reactive properties with `static properties: PropertyDeclarations`, then `declare` each field.
  - Use `attribute: false` for non-primitive or store-backed properties.
  - Initialize defaults in the constructor when needed.

## Linking properties to app state

- Use the `store` property inside `PropertyDeclarations` to link to a Reatom `Atom`.
- Wrap the class with `withStore` from `lit-reatom`.
- Keep state props typed (e.g., `declare appSession: ReturnType<typeof appSessionAtom>`).

## Tasks (DOM events)

- Use DOM events to trigger service logic via `helpers/domTask.ts`.
- Declare task params/returns in `src/setup/tasks.ts` (`TaskEventRegistry`).
- Register handlers in `src/setup/services.ts` using `registerTaskHandler`.
- Dispatch tasks from components via `dispatchTask(this, 'task-name', params)`

## Configure routing

- Register the page route in `src/main.ts` as a children of the app route.
- Add a `ui5-side-navigation-item` in `src/pages/app-shell/app-shell-page.ts` for navigation.

Example:

```ts
import { LitElement, html, css, PropertyDeclarations } from 'lit'
import { withStore } from 'lit-reatom'
import { BSHelpersCSS } from 'helpers/bootstrapCSS'
import { dispatchTask } from 'helpers/domTask'
import { myDataAtom, MyData } from 'stores/myData'

export class MyComponent extends withStore(LitElement) {
  static properties: PropertyDeclarations = {
    title: {},
    myData: { attribute: false, store: myDataAtom },
  }

  declare title?: string
  declare myData: MyData

  constructor() {
    super()
    this.title = 'My Component'
  }

  loadData() {
    dispatchTask(this, 'load-data', { id: 1 })
  }

  render() {
    return html`<div class="container">
      ${this.title ? html`<p>${this.title}</p>` : ''}
      <div>
        <p>Data ID: ${this.myData?.id}</p>
        <p>Data Name: ${this.myData?.name}</p>
      </div>
      <button class="btn btn-primary" @click=${this.loadData}>Load data</button>
    </div> `
  }

  static styles = [
    BSHelpersCSS,
    css`
      /* component styles */
    `,
  ]
}

customElements.define('my-component', MyComponent)
```

## Storybook story

Keep stories simple and use the `Components/<PageName>` naming pattern from existing pages.

Example:

```ts
import './my-page.js'

export default {
  title: 'Components/MyPage',
  component: 'my-page',
  parameters: {
    actions: {
      handles: [],
    },
  },
  args: {},
}

export const Default = { args: {} }
```
