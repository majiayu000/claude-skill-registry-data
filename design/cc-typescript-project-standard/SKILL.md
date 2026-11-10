---
name: cc-typescript-project-standard
description: Use when TypeScript configuration, module resolution, public API types, declarations, package exports, narrowing or generic contracts need design or review in applications, SDKs, CLI tools, desktop processes or libraries.
---

# TypeScript project specifications

Apply to libraries, CLI tools, desktop cores and services. Determine the application role from the actual project; a frontend/backend product name does not constrain the language.

## Purpose

Unify project configuration, type boundaries, and release product rules for the TypeScript layer. Works with front-end applications, component libraries, SDKs, CLIs, monorepo packages, and pure TypeScript tool libraries, but does not take over the framework architecture responsibilities of React, Vue, Next.js, Nuxt, or Vite.

## Procedure

1. Identify TypeScript context
   - Application projects: Prioritize checking of `tsconfig` layering, strictness, path aliases, type checking scripts and framework generation types.
   - Component library or SDK: Prioritize checking public API, declaration files, package exports, peer dependencies type boundaries and pre-release pack verification.
   - CLI or Node tools: Prioritize checking Node target versions, ESM/CJS policies, `moduleResolution`, shebang artifacts, and `process.env` type boundaries.
   - Monorepo package: Prioritize checking whether project references, composite builds, inter-package import boundaries, and workspace path aliases leak into release products.
   - The component architecture, routing organization, and state management of frameworks such as React, Vue, Next.js, and Nuxt belong to the corresponding framework skills; this process only deals with cross-framework TypeScript contracts and project boundaries.

2. Convergence `tsconfig`
   - Prefer `strict` for new code and preserve existing checks; do not disable `noImplicitAny` or `strictNullChecks` merely to hide a defect. `exactOptionalPropertyTypes` is a separate option; introduce stricter settings through a scoped, compatible migration when justified.
   - Select `target`, `lib`, `module` and `moduleResolution` according to the running environment; browser applications, Node scripts, and library packages should not share an ambiguous configuration.
   - Separate basic configuration, application configuration, test configuration and build declaration configuration to avoid testing global types from polluting production code.
   - Path aliases must be understood by TypeScript, bundler, test runner, and published products at the same time; library packages must not publish source code aliases that cannot be resolved.

3. Design type boundaries
   - Hierarchical naming of external input, DTO, domain model, UI view model, component props and tool function API.
   - The parameters and return values of the public API are explicitly marked, and internal local variables are inferred first.
   - External data is received as `unknown` first, and then narrowed by schema or type guard.
   - Complex generics, discriminative unions, DTO mappings, type guards and type tests are loaded [Type Safety Reference](references/type-safety.md); [Type Safety Patterns](references/type-safety-patterns.md) is loaded when advanced patterns are required.

4. Fixed release and announcement of products
   - The library package must confirm that the `exports`, `types`, and `files` of `package.json` are consistent with the actual build product.
   - Do not default to dual-package publishing; only produce ESM/CJS at the same time when the consumer clearly needs it, and verify that the type entry does not fork.
   - Produce `.d.ts` through `tsc --emitDeclarationOnly`, build tool declaration plug-in or API extractor, and check that the declaration file can be parsed by the consumer before publishing.
   - Do not expose tests, fixtures, internal tools, unstable types, or private paths to package exports.

5. Verify TypeScript quality
   - Prioritize the use of existing scripts in the repository, such as `typecheck`, `build`, `test`, `lint` and package pack dry-run.
   - Vite, Next, Nuxt, etc. builds do not equal full type checking; CI must have standalone typecheck or equivalent verification.
   - Type changes affect public API time-filling type tests, compile-time assertions, or consumer fixtures.

## Constraints

- Do not use `any`, unguarded non-null assertions or broad `as` to conceal an unverified boundary. A justified `skipLibCheck` dependency policy is separate from checking your own public API; record its limits.
- Do not rely on release package private deep paths in application code.
- Do not put framework directory structure, component layering, routing organization or state management decisions into this process; these are left to the corresponding framework or dedicated process.
- Don't pollute browser running code with generated, test, or Node-only types.
- Do not publish path aliases, ambient declarations, or implicit global types that can only be resolved within the source code repository.

## Expected Output

The output should include TypeScript context determinations, key `tsconfig`/package type entry suggestions, type boundary schemes, declaration file or public API risks, and verification commands. After completion, the project should be able to independently typecheck, public types can be parsed by consumers, and type safety issues should have clear narrowing or modeling solutions.

## Engineering practices

Read the [local engineering decisions](references/engineering-practices.md) for this task and follow their links to relevant shared principles. Apply levels and exceptions against actual project contracts; product frontend/backend labels do not constrain language or role.
