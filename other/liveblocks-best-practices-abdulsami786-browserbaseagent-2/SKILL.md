---
name: "liveblocks-best-practices"
description: "Use this skill when building, debugging, or answering questions
  about Liveblocks. Liveblocks gives you the building blocks and infrastructure
  to enable people and AI to work together inside your app, powering realtime
  collaboration.

  Liveblocks features include collaboration, rooms, organizations, workspaces,
  comments, composer, threads, notifications, multiplayer, conflict resolution,
  realtime presence, avatar stacks, AI collaborators, AI agents, text editors,
  Tiptap, BlockNote, Lexical, React Flow, Chat SDK.

  Common components include AiChat, Thread, InboxNotification, Composer, Toolbar
  (for Lexical Tiptap), FloatingToolbar, FloatingComposer, FloatingThreads,
  AnchoredThreads.

  Common hooks include useThreads, useStorage, useMutation, useOthers,
  useInboxNotifications, useAiChats.

  Common issues are related to authentication (ID tokens vs access tokens),
  permissions, room limits, connection errors, user info."
license: "Apache License 2.0"
metadata:
  author: "liveblocks"
  version: "1.0.0"
---

# Liveblocks best practices

## When to use this skill

Use this skill when implementing features using any Liveblocks packages, for
example [`@liveblocks/react`](https://www.npmjs.com/package/@liveblocks/react)
or [`@liveblocks/node`](https://www.npmjs.com/package/@liveblocks/node). This
could be related to features like realtime multiplayer, commenting,
notifications, cursors, avatar stacks, AI, and more. This also includes
technologies like Liveblocks Storage, Yjs, Tiptap, BlockNote, Lexical, React
Flow, tldraw, and more.

## Quick reference

A number of reference files are available in the `references/` directory. You
must read the list below, and load relevant files as needed. For example,
`add-user-information` is available in the `references/add-user-information.md`
file.

## References

- `add-user-information`: Add user information to your application, such as
  name, avatar, color, and more. Users will no longer be anonymous. Useful for
  displaying user info in comments, comments mention suggestions, notifications,
  cursors, avatar stacks.
- `ai-as-a-collaborator`: Use agentic workflows to allow AI to collaborate like
  a human inside your Liveblocks application.
- `ai-chats-with-tools-knowledge-components`: Set up and troubleshoot chats with
  RAG, knowledge, custom components, tool calling, custom models. Different to
  AI as a collaborator, as it is NOT workflow based.
- `auth-endpoint-callback`: Use a callback function to authenticate users,
  instead of passing a string to `authEndpoint`. Useful for passing custom
  headers to your back end, and for preventing automatic reconnection when the
  token is invalid.
- `authenticating-with-access-tokens`: Alternative method for authenticating
  users with their ID and info, best for very simple permissions.
- `authenticating-with-id-tokens`: Recommended method for authenticating users
  with their ID and info, best for complex permissions.
- `avoid-hitting-user-limit-in-rooms`: How to avoid rooms filling up with users.
- `compartmentalize-resources-with-organizations`: Use organizations to create
  workspaces/tenants and compartmentalize resources, such as rooms,
  notifications, comment threads, and more. You can filter by organization when
  listing rooms and more.
- `create-custom-comment-composer`: Build your own commenting composer (advanced
  use cases only).
- `create-custom-realtime-multiplayer`: Use Liveblocks Storage to build fully
  custom conflict-resolved multiplayer apps, like Figma, Pitch, Spline. Helpful
  for one-off realtime features too, like simple properties in a document.
- `create-custom-text-editor-toolbar`: Set up a styled toolbar, static or
  floating next to your selection, in Tiptap and Lexical.
- `create-rooms-manually`: Always create rooms yourself in production
  applications, setting permissions, organization, metadata.
- `customize-thread-components`: Use slots to customize comments inside of
  threads, and their different parts.
- `dark-mode-styles`: You can import CSS styling for dark mode themes.
- `develop-and-test-locally`: Set up a local dev server, and use it for
  Continuous Integration (CI) and End-to-End (E2E) testing. Connect to your app
  not online.
- `devtools-extension`: Inspect Liveblocks Storage, Yjs, presence, events, and
  connected users with DevTools extensions for Chrome, Firefox, Edge.
- `edit-component-text-strings`: Override strings in default components, such as
  button values, tooltip text, error text, more. Also helpful for setting other
  languages.
- `exhaustive-deps-with-usemutation`: Prevent and fix stale-closure bugs with
  `useMutation` by configuring the `react-hooks/exhaustive-deps` ESLint rule.
- `handling-connection-errors`: Handle problems joining rooms because of
  permissions, authentication, changed room IDs.
- `handling-full-rooms`: Handle problems caused by joining full rooms.
- `handling-hook-and-component-errors`: Handle errors caused by hooks and
  pre-built components.
- `handling-unstable-connections`: Implement fallbacks and error messages when
  users have poor network conditions.
- `log-out-of-liveblocks`: Rarely useful, but helpful in specific SPA situations
  where you cannot navigate the page to log out.
- `multiplayer-react-flow`: Use the Liveblocks React Flow package to create
  multiplayer diagrams with cursors and more.
- `multiple-text-editors`: Add multiple Tiptap or BlockNote editors to the same
  page. Optionally use Storage to hold their field IDs.
- `offline-support-in-text-editors`: Give your text editors the illusion of a
  quicker load time.
- `override-css-variables`: Add custom styles to the default components by
  overriding Liveblocks CSS variables.
- `performant-others-and-presence`: Prevent unnecessary presence renders by
  using `useOtherConnectionIds`, `useOthersMapped`, `useOther`, and `shallow` to
  update components only when necessary.
- `performant-storage-with-selectors`: Prevent unnecessary storage renders by
  using `useStorage` selectors and `shallow`.
- `prevent-unsaved-changes-being-lost`: Stop losing unsynched or unsaved
  changes.
- `primitive-component-parts`: Use primitives to create custom components or to
  merge components from your design system into Liveblocks UI.
- `remove-liveblocks-branding`: A Liveblocks logo badge appears in the bottom
  right of the screen, this is how to remove it.
- `rendering-error-components`: Use `ErrorBoundary` to structure your app with
  error fallbacks.
- `rendering-loading-components`: Use `ClientSideSuspense` to performantly
  structure your app with loading skeletons and spinners.
- `send-comment-notification-emails`: Send email notifications to users when
  they have unread comments. These comments are sent via webhooks, and are
  triggered when a user is mentioned, or has participated in a thread.
- `smoother-realtime-updates`: Make presence and storage run at a higher frame
  rate, appearing more smooth. Using this option, updates can be received more
  frequently.
- `suspense-vs-regular-hooks`: You must read this when using any Liveblocks
  hooks. React suspense uses `ErrorBoundary` and `ClientSideSuspense`
  components. Regular hooks use `{ error, isLoading }` values.
- `tiptap-best-practices`: Server-side rendering, starter kit extensions,
  initial content, unsaved changes, more.
- `trigger-custom-notifications`: Trigger any kind of notification in your
  inbox, even those unrelated to commenting.
- `type-liveblocks-correctly`: Always use TypeScript to type Liveblocks where
  available. Presence, others, user info, storage, metadata, room info,
  notifications activities, can all be automatically typed.
- `url-params-in-room-id`: Use URL params in room IDs to create rooms, and
  incorporate document titles in the URL.
- `utility-components`: Import a ready-made emoji picker, or human-readable
  timestamps, durations, file sizes.
- `yjs-best-practices`: YKeyValue, subdocuments, V2 encoding, double imports,
  getYjsProviderForRoom. NOT relevant if you're using Tiptap, BlockNote, or
  Lexical.
- `z-index-issues`: Fix z-index problems by targeting portaled elements.

## Note

Some files link to markdown files in the Liveblocks docs, for example:

```
https://liveblocks.io/docs/concepts.md
```

When linking users to these pages, remove `.md` from the link, so they can view
the full content:

```
https://liveblocks.io/docs/concepts
```

## Liveblocks packages

Always check if we provide a package for your technology. For example, if you're
using React Flow, you should use **`@liveblocks/react-flow`**.

- **`@liveblocks/client`**: JavaScript client. Can use with any framework, e.g.
  Vue, Svelte, vanilla JS.
- **`@liveblocks/react`**: React client. Contains hooks and components..
- **`@liveblocks/react-ui`**: Pre-built React UI components and primitives.
  `@liveblocks/react` for data and hooks.
- **`@liveblocks/react-tiptap`**: Collaborative Tiptap integration for React.
- **`@liveblocks/react-blocknote`**: Collaborative BlockNote integration for
  React.
- **`@liveblocks/react-lexical`**: Collaborative Lexical integration for React.
- **`@liveblocks/node-lexical`**: Server-side Lexical utilities for Node.js.
- **`@liveblocks/node-prosemirror`**: Server-side ProseMirror utilities For
  Node.js. Also works with Tiptap and BlockNote.
- **`@liveblocks/react-flow`**: Multiplayer React Flow.
- **`@liveblocks/yjs`**: Yjs provider backed by Liveblocks rooms.
- **`@liveblocks/redux`**: Sync Liveblocks room state with a Redux store.
- **`@liveblocks/zustand`**: Sync Liveblocks room state with Zustand.
- **`@liveblocks/node`**: Node.js server SDK. Use for auth and lots more.
- **`@liveblocks/emails`**: Build notification emails more easily.
- **`@liveblocks/chat-sdk-adapter`**: Make multi-platform (Liveblocks, Slack,
  Discord, etc.) chat bots.
- **Python SDK**: Python server SDK. Use for auth and lots more.
- **REST API**: HTTP API. Use for auth and lots more.

### If a technology is not listed here

If the users want to set up a new technology, first check the following
resources to see if a package exists:

- [llms.txt](https://liveblocks.io/llms.txt)
- [Documentation](https://liveblocks.io/docs)
- [Examples](https://liveblocks.io/examples)

## Learn more

Learn more in [Liveblocks docs](https://liveblocks.io/docs).
