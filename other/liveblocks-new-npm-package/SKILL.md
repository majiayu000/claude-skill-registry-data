---
name: liveblocks-new-npm-package
description: >
  Publish a new placeholder package to NPM under the @liveblocks/* org.
  Creates a minimal package.json + index.js in a temp dir and gives the
  user exact commands to run. Use when publishing a brand-new @liveblocks/*
  package for the first time (version 0.0.0 placeholder to claim the name).
---

# Publish a new @liveblocks/\* NPM placeholder

The goal is to claim a new package name on NPM by publishing a minimal `0.0.0`
placeholder. The user then fills it in for real later.

## Template

The minimal package has exactly two files:

**`package.json`**

```json
{
  "name": "@liveblocks/<PACKAGE>",
  "version": "0.0.0",
  "license": "Apache-2.0",
  "main": "index.js"
}
```

**`index.js`**

```js
// Placeholder
```

No `README.md`, no `description`, no extra fields.

## Process

1. **Ask the user for the package name** if not already provided (e.g. `foobar`
   → full name becomes `@liveblocks/foobar`).

2. **Create the temp dir and files yourself** using Bash:

```sh
DIR=$(mktemp -d)
mkdir -p "$DIR"
```

Then write `package.json` (with the correct package name) and `index.js`
(`// Placeholder`) into `$DIR` using the Write tool.

3. **Tell the user the single command to run:**

```
cd <DIR> && npm publish --access public
```

Substitute `<DIR>` with the actual temp path that was created.

4. **Remind the user:**

   - They must be logged in to npm with an account that has publish rights to the
     `@liveblocks` org (`npm whoami` to check, `npm login` if not).
   - After publishing, the temp dir can be deleted.
   - The `--access public` flag is required for scoped packages on the free tier.

5. **Do not** run `npm publish` yourself — the user runs that final step.
