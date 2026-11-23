---
name: family-sync
description: How a shared change is carried to all five Lean Mean Clean Apps templates - which folders are shared, the namespace swap, opening the same branch everywhere, keeping repository and maintainer skills out of the package, and proving the copies match. Use when you have changed the Application or Infrastructure layers, their tests, shared skills, AGENTS.md, the pipeline or repository setup.
metadata:
  scope: maintainer
---

# Family sync

## The rule

The five templates share everything except the Presentation layer. A shared change is made and reviewed in CleanMinimalApi first, then the same branch is opened in the other four with the same title, in this order: MCP, GraphQL, Web API, Lambda Function.

| Shared, copied as is (with the name swapped) | Per template |
| --- | --- |
| `src/Application`, `src/Infrastructure` | `src/Presentation` |
| `tests/Application.Tests.Unit`, `tests/Infrastructure.Tests.Integration` | `tests/Presentation.Tests.*` |
| `.agents/agents/jacques.md` and every skill whose `scope` is `shared`, `repository` or `maintainer` | Skills whose `scope` is `presentation` |
| `AGENTS.md`, except the Presentation rows and the presentation skills | Those rows |
| `.github/workflows`, `.github/actions`, community files, `Directory.Build.props`, `.editorconfig` | `.template.config/`, `README.md`, `NUGET.md` |

| Template | Repository and namespace |
| --- | --- |
| Minimal API | `CleanMinimalApi` |
| MCP | `CleanModelContextProtocol` |
| GraphQL | `CleanGraphQLApi` |
| Web API | `CleanWebApi` |
| Lambda Function | `CleanLambdaFunction` |

## Steps

1. Merge-ready in CleanMinimalApi first.
2. For each other template, on the same branch name, copy the shared folders over and swap the name (no rsync needed):

   ``` bash
   SRC=../CleanMinimalApi; NAME=CleanWebApi
   for d in src/Application src/Infrastructure tests/Application.Tests.Unit tests/Infrastructure.Tests.Integration; do
     rm -rf "$d" && (cd "$SRC" && tar cf - "$d") | tar xf -
   done
   grep -rl CleanMinimalApi src/Application src/Infrastructure tests/Application.Tests.Unit tests/Infrastructure.Tests.Integration \
     | xargs sed -i "s/CleanMinimalApi/$NAME/g"
   ```

3. Copy the shared skills and the persona the same way, then edit the Presentation rows of `AGENTS.md` by hand. A new `repository` or `maintainer` skill also goes in the `RepositorySkills` list in `template/template.csproj`, so it stays out of the package.
   A presentation skill with the same name in every template (`expose-a-use-case`, `json-serialization`, `presentation-integration-tests`) is written for each template's own code, never copied.
4. Prove they match with the commands under Check. There should be no differences.
5. Build and test every template. Open the pull requests with the same title and description.

## Don't

- Change a shared file in one template only.
- Merge the copies before the CleanMinimalApi pull request is approved.
- Copy `bin/` or `obj/` folders.

## Check

Run in each copy, after the build:

``` bash
SRC=../CleanMinimalApi; NAME=CleanWebApi; SHARED="src/Application src/Infrastructure tests/Application.Tests.Unit tests/Infrastructure.Tests.Integration"
tmp=$(mktemp -d); tar cf - --exclude=bin --exclude=obj $SHARED | (cd "$tmp" && tar xf -)
grep -rl "$NAME" "$tmp" | xargs sed -i "s/$NAME/CleanMinimalApi/g"
for d in $SHARED; do diff -r --exclude=bin --exclude=obj "$SRC/$d" "$tmp/$d"; done   # expect no output
dotnet build && dotnet test
```
