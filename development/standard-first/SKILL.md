---
name: standard-first
description: >
  Guides technical implementation to always prefer the standard, officially-documented solution over
  custom or AI-generated code. Use when you are about to write new code for a feature, suggest or add
  a library or package, scaffold a new project, or configure a framework, in any language, including
  .NET and C#, Node.js and npm, Python, Go, Java, and the rest. Use it above all when the problem
  sounds like something that a built-in framework feature or a package registry already solves, such
  as logging enrichment, auth, serialization, retries, health checks, or migrations. Do not skip this
  skill because the answer feels obvious from training data.
argument-hint: "[task description]"
allowed-tools: [WebSearch, WebFetch, Read, Glob, Write, Bash]
---

# Standard-First

Before you implement anything, find what already exists: a built-in framework feature, a well-maintained package, or an official pattern. Steps 1 to 3 find the candidates, and Step 4 ranks them.

## Step 1: Understand the stack

Use `Glob` and then `Read` on the dependency and configuration manifests of the project. Those are `*.csproj`, `*.sln`, and `global.json`, plus `package.json`, `go.mod`, `requirements.txt`, `pyproject.toml`, `pom.xml`, `build.gradle`, `Cargo.toml`, and their lockfiles. Pin the exact framework version and what is already installed. That is what stops you from reading ASP.NET Core 9 docs for a project that targets .NET 6. It also stops you from proposing a package that the project already has under a different name.

When you find no project files, ask the user for the tech stack before you proceed.

## Step 2: Check for a technology-specific skill

Before you go to the web, scan the skills available in this session for one that covers the stack from Step 1. An ecosystem skill carries curated and current knowledge for that stack, and it beats a web search. When one matches, invoke it and follow its guidance, and skip Step 3 wherever that skill covers the task. Otherwise continue to Step 3.

## Step 3: Search before you implement

For every implementation task, search the official sources before you write any code.

### 3a. Find out whether a package already solves it

The first question is always this: does the solution already exist? Search the package registry of the stack with `WebSearch`. Naming the registry in the query is what surfaces its listing, as in `serilog log masking nuget` or `[problem description] npm`.

A well-maintained package is almost always better than custom code. Well-maintained means actively updated, with thousands of downloads and clear docs. Such a package gets security patches, bug fixes, and compatibility updates automatically.

Here are examples of packages that replace custom code:

- To mask sensitive values in Serilog logs, use `Serilog.Enrichers.Sensitive`, and not a custom `IDestructuringPolicy`.
- For retry logic in HTTP calls, use `Polly`, and not a hand-rolled retry loop.
- For strongly-typed configuration in ASP.NET Core, use the built-in `IOptions<T>`, and not manual configuration reads.
- For health checks, use the built-in `Microsoft.AspNetCore.Diagnostics.HealthChecks`, and not a custom endpoint.

### 3b. Fetch and read the official documentation

Once you identify a candidate package or framework feature, fetch its current documentation. Never rely on training data alone, because official docs change and package APIs evolve.

**Preferred path, the `find-docs` skill or the `ctx7` CLI**: when a `find-docs` skill is available, invoke it. Otherwise fetch the current docs with the `ctx7` CLI. Run `npx ctx7@latest library "<name>"` to resolve the library, then `npx ctx7@latest docs <id> "<focused question matching the task>"`. Both return curated and versioned docs directly.

**Fallback, `WebFetch`**: when neither is available, use `WebFetch` to retrieve the official documentation page directly.

Take the documentation from the domain of the vendor, and not from a blog or an aggregator. Use `learn.microsoft.com` for .NET and ASP.NET Core, `nodejs.org`, `docs.python.org`, `pkg.go.dev`, `docs.docker.com`, and `kubernetes.io`. For a package, start at its registry listing, and follow the docs site that it links to.

Whatever the source, read the section that is relevant to the task. Also look for sections titled "Best practices", "Recommendations", "Security considerations", "Performance", or "Production". Those sections differ from the getting-started example. They often carry configuration options, ordering constraints, and caveats that the minimal snippet omits and that matter in a real application.

The docs sometimes recommend a specific registration order, configuration pattern, or combination of options for the case at hand. Follow that recommendation, and do not stop at the minimal snippet.

### 3c. For new project scaffolding

When you create a project from scratch, find and follow the official "Getting Started" guide for the chosen framework. Do not generate boilerplate from memory. Fetch the current guide.

Search for `[framework name] getting started official documentation site:[official-domain]`.

Follow the structure, the naming conventions, and the project layout of the guide exactly as it shows them. The official guide reflects the current recommended approach, and it avoids patterns that something newer has superseded.

## Step 4: Choose the simplest solution

After you finish searching, apply Occam's Razor. Prefer the solution with the fewest moving parts that fully solves the stated problem.

**Decision hierarchy:**
1. **A built-in framework feature**, which adds no dependency. Always prefer it when it covers the need.
2. **An official or well-maintained package**, which beats custom code when it solves the problem cleanly.
3. **Custom code**, only when no package and no built-in feature handles the problem adequately.

## Step 5: Implement

Implement from the official docs, and not from training-data patterns. "Simplest" means the fewest invented parts, and it does not mean ignoring official guidance. Following official best practices is simpler over time, because it prevents you from rediscovering the pitfalls that the docs already record.

Every solution must include three things:
1. **The installation command**, such as `dotnet add package`, `npm install`, or `pip install`.
2. **Working code that follows the official recommendations.** That is the minimal code needed, structured according to the official best-practice pattern rather than copied from the getting-started snippet.
3. **A note on any deviation from a best practice.** When the existing code of the project diverges from an official recommendation, call that out instead of matching the deviation in silence.

Keep the implementation concise. Show the minimum that solves the problem correctly, and do not write a comprehensive tutorial.
