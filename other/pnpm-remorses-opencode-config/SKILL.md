---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: pnpm
description: Use to debug why a specific package has duplicate dependencies in a pnpm project's node_modules, which can cause type-checking and bundler errors or duplicate singleton instances such as React contexts. Also use for pnpm workspace dependency updates, and when a just-published package version will not install or update (minimumReleaseAge blocks it). NEVER use package.json overrides to update or align versions; use `pnpm update -r <package>` instead.
---

# package manager: pnpm with workspace

this project uses pnpm workspaces to manage dependencies. important scripts are in the root package.json or various packages' package.json

try to run commands inside the package folder that you are working on. for example you should never run `pnpm test` from the root

if you need to install packages always use pnpm

always invoke package scripts explicitly with `pnpm run <script>`. this is
especially important for `deploy`: `pnpm deploy` is pnpm's built-in deployment
command, while `pnpm run deploy` executes the project's `"deploy"` script.

instead of adding packages directly in package.json use `pnpm install package` inside the right workspace folder. NEVER manually add a package by updating package.json

## updating a package

when i ask you to update a package always run `pnpm update -r packagename`. to update to latest also add --latest

Do not do `pnpm add packagename` to update a package. only to add a missing one. otherwise other packages versions will get out of sync.

NEVER add `pnpm.overrides` or any other package.json override to update, pin, or align a dependency version. update every workspace consumer together with `pnpm update -r packagename` instead. use `pnpm update -r --latest packagename` when the latest release is required.

## newly published package will not install (minimum release age)

pnpm delays newly published versions by 1 day (`minimumReleaseAge: 1440`), a supply chain security feature. If a package does not update even though a new version was just published, this config is blocking it.

Add the package to the exclude list with the global script:

```bash
bun ~/.config/pnpm/update-minimum-release-age-exclude.ts package-name @some-scope/pkg
```

The script fetches all packages maintained by npm user `xmorse`, collapses scoped packages into `@scope/*` globs, and merges the extra packages passed as args. It writes both `~/.config/pnpm/config.yaml` (pnpm 11) and `~/.npmrc` (pnpm 10). `~/.config/pnpm/` is a git repo.

## fixing duplicate pnpm dependencies

sometimes typescript will fail if there are 2 duplicate packages in the workspace node_modules. this can happen in pnpm if a package is used in 2 different places (even if inside a node_module package, transitive dependency) with a different set of versions for a peer dependency

for example if better-auth depends on zod peer dep and zod is in different versions in 2 dependency subtrees

to identify if a pnpm package is duplicated, search for the string " packagename@" inside `pnpm-lock.yaml`, notice the space in the search string. then if the result returns multiple instances with a different set of peer deps inside the round brackets, it means that this package is being duplicated. here is an example of a package getting duplicated:

```

  better-auth@1.3.6(react-dom@19.1.1(react@19.1.1))(react@19.1.1)(zod@3.25.76):
    dependencies:
      '@better-auth/utils': 0.2.6
      '@better-fetch/fetch': 1.1.18
      '@noble/ciphers': 0.6.0
      '@noble/hashes': 1.8.0
      '@simplewebauthn/browser': 13.1.2
      '@simplewebauthn/server': 13.1.2
      better-call: 1.0.13
      defu: 6.1.4
      jose: 5.10.0
      kysely: 0.28.5
      nanostores: 0.11.4
      zod: 3.25.76
    optionalDependencies:
      react: 19.1.1
      react-dom: 19.1.1(react@19.1.1)

  better-auth@1.3.6(react-dom@19.1.1(react@19.1.1))(react@19.1.1)(zod@4.0.17):
    dependencies:
      '@better-auth/utils': 0.2.6
      '@better-fetch/fetch': 1.1.18
      '@noble/ciphers': 0.6.0
      '@noble/hashes': 1.8.0
      '@simplewebauthn/browser': 13.1.2
      '@simplewebauthn/server': 13.1.2
      better-call: 1.0.13
      defu: 6.1.4
      jose: 5.10.0
      kysely: 0.28.5
      nanostores: 0.11.4
      zod: 4.0.17
    optionalDependencies:
      react: 19.1.1
      react-dom: 19.1.1(react@19.1.1)

```

as you can see, better-auth is listed twice with different sets of peer deps. in this case it's because of zod being in version 3 and 4 in two subtrees of our workspace dependencies.

as a first step, try running `pnpm dedupe better-auth` with your package name and see if there is still the problem.

below i will describe how to generally deduplicate a package. i will use zod as an example. it works with any dependency found in the previous step.

to deduplicate the package, we have to make sure we only have 1 version of zod installed in your workspace. DO NOT use overrides for this. instead, fix the problem by manually updating the dependencies that are forcing the older version of zod in the dependency tree.

to do so, we first have to run the command `pnpm -r why zod@3.25.76` to see the reason the older zod version is installed. in this case, the result is something like this:

```

website /Users/morse/Documents/GitHub/holocron/website (PRIVATE)

dependencies:
@better-auth/stripe 1.2.10
├─┬ better-auth 1.3.6
│ └── zod 3.25.76 peer
└── zod 3.25.76
db link:../db
└─┬ docs-website link:../docs-website
  ├─┬ fumadocs-docgen 2.0.1
  │ └── zod 3.25.76
  ├─┬ fumadocs-openapi link:../fumadocs/packages/openapi
  │ └─┬ @modelcontextprotocol/sdk 1.17.3
  │   ├── zod 3.25.76
  │   └─┬ zod-to-json-schema 3.24.6
  │     └── zod 3.25.76 peer
  └─┬ searchapi link:../searchapi
    └─┬ agents 0.0.109
      ├─┬ @modelcontextprotocol/sdk 1.17.3
      │ ├── zod 3.25.76
      │ └─┬ zod-to-json-schema 3.24.6
      │   └── zod 3.25.76 peer
      └─┬ ai 4.3.19
        ├─┬ @ai-sdk/provider-utils 2.2.8
        │ └── zod 3.25.76 peer
        └─┬ @ai-sdk/react 1.2.12
          ├─┬ @ai-sdk/provider-utils 2.2.8
          │ └── zod 3.25.76 peer
          └─┬ @ai-sdk/ui-utils 1.2.11
            └─┬ @ai-sdk/provider-utils 2.2.8
              └── zod 3.25.76 peer
```

here we can see zod 3 is installed because of @modelcontextprotocol/sdk, @better-auth/stripe and agents packages. to fix the problem, we can run

```
pnpm update -r --latest  @modelcontextprotocol/sdk @better-auth/stripe agents
```

this way, if these packages include the newer version of the dependency, zod will be deduplicated automatically.

in this case, we could have only updated @better-auth/stripe to fix the issue too, that's because @better-auth/stripe is the one that has better-auth as a peer dep. but finding what is the exact problematic package is difficult, so it is easier to just update all packages you notice that we depend on directly in our workspace package.json files.

if after doing this we still have duplicate packages, you will have to ask the user for help. you can try deleting the node_modules and restarting the approach, but it rarely helps.
