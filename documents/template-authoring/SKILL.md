---
name: template-authoring
description: How the dotnet new template is defined and packaged - .template.config/template.json and its two host files, sourceName replacement, symbols such as authorName and the include toggles, code that's left out when a toggle is off, short flags, the restore post action, what template/template.csproj packs, and how to test an install. Use when changing template options, the package contents or anything that affects generated solutions.
metadata:
  scope: maintainer
---

# Template authoring

## The rule

The repository is both a working solution and a `dotnet new` template. `.template.config/template.json` defines the template; `template/template.csproj` packs it into a NuGet package of type `Template`. When someone runs `dotnet new`, every occurrence of the `sourceName` (the template's own name, such as `CleanMinimalApi`) in file names and contents is replaced with their project name, including `CleanMinimalApi.slnx`.

| Symbol | Option | Replaces |
| --- | --- | --- |
| `authorName` | `--authorName`<br>`-an` | `Stephen Walsh` (`--author` is reserved by `dotnet new`) |
| `includeAuth` | `--include-auth` | Nothing. A toggle, off by default. Off, every line of authentication code is left out; on, `authority` and `audience` switch on through `isEnabled` and `authority` becomes required through `isRequired` (web templates) |
| `authority` | `--authority`<br>`-iss` | The empty `Authentication:Authority` setting in `appsettings.json`, only with `--include-auth`. Passed without it, it's ignored without a word (web templates) |
| `audience` | `--audience`<br>`-aud` | The empty `Authentication:Audience` setting in `appsettings.json`, only with `--include-auth`. Passed without it, it's ignored without a word (web templates) |
| `skipRestore` | `--no-restore` | Nothing; it turns the restore post action off |

Three files in `.template.config` make up the template, and every symbol appears in each one that applies:

| File | Used by | Holds |
| --- | --- | --- |
| `template.json` | Every host | Identity, `groupIdentity`, `precedence` and `generatorVersions`, `tags.type` of `solution`, the standard classifications, `defaultName`, an SDK `constraints` entry matching `global.json`, the symbols with a `displayName` and a `description`, a `HostIdentifier` bind, `primaryOutputs` (the `.slnx`, and `docs/RUN.md` for IDEs only) and three post actions: restore, open `docs/RUN.md` in the IDE, and a next-steps line in the terminal |
| `dotnetcli.host.json` | `dotnet new` | Each symbol's `longName` and short flag, and `usageExamples` (kept for hosts that show them; the .NET 10 `--help` doesn't) |
| `ide.host.json` | Visual Studio, Rider | The icon (`.template.config/icon.png`, a copy of the root `icon.png`), platform and project type `tags`, and the label, description, visibility and choice labels of each symbol. The author name has a `shared` `persistenceScope` named `LeanMeanCleanApps`, so Visual Studio remembers it across all five templates |

The words in those files are the first thing people read, in a terminal or a dialog. Write them in our voice (`docs-and-voice`): plain first, then one dry line if it earns its place. The `defaultName` is `WorksOnMyMachine.Movies` (`WorksOnMyMachine.Reviews` in the Lambda function). Visual Studio and Rider suggest it as the project name, and `dotnet new` uses the folder name instead.

## Feature toggles

Every optional feature is a toggle, and every toggle has the same shape, so people learn it once:

- A `bool` symbol named `include<Feature>` in `template.json`, such as `includeAuth`, with a `displayName` of "Include <feature>". Its description doesn't state the default, because `dotnet new --help` prints that under every option.
- A `longName` of `include-<feature>` in `dotnetcli.host.json`, so it's `--include-auth` on the command line. No short flag.
- A checkbox labelled "Include <feature>" in `ide.host.json`, whose description ends with its default, such as "Default: off.", because the IDE dialogs don't show defaults.
- One row in the options table of the README, `NUGET.md` and the docs site's template options page, which list every toggle with a Default column.

Off means absent, not switched off. Files that only exist for a toggle go in a `(!include<Feature>)` exclude list under `sources` in `template.json`, and code inside shared files is wrapped so `dotnet new` can leave it out. In C#, `#if includeAuth` and `#endif` start at the beginning of the line, with no brackets (the build fails IDE0047 and IDE0055 otherwise). In project files it's `<!--#if (includeAuth) -->` and `<!--#endif -->`, and in `appsettings.json` it's `//#if (includeAuth)` and `//#endif`. A file type the template engine doesn't know, such as the GraphQL schema snapshot, gets `#if (includeAuth)` and `#endif` lines through `SpecialCustomOperations` in `template.json`.

The repository itself stays all on. The Presentation project and the presentation integration tests define each toggle's constant, such as `includeAuth`, inside `<!--#if (false) -->`, which `dotnet new` always removes. The template's skills and `AGENTS.md` ship either way.

A toggle's inputs, such as `authority` and `audience`, are separate symbols, enabled with `isEnabled` and made required with `isRequired` only when the toggle is on. Only `dotnet new` honours those two. Visual Studio and Rider show every input whatever the toggle says ([dotnet/templating#7860](https://github.com/dotnet/templating/issues/7860)), and Rider lists checkboxes first, then text fields in alphabetical order by label. So an input's label starts with its feature, such as "Authentication authority", to sit right under its checkbox, and its IDE description says it's only used when that box is ticked. A toggle that needs another one says so in its conditions, such as `(includeTests && includeArchitectureTests)`. Verify Template checks the defaults, everything on, everything off, and each toggle flipped on its own.

The package includes `src/`, `tests/`, `docs/RUN.md`, the root build files, `AGENTS.md`, `CLAUDE.md`, the persona and the engineering skills. It also packs `template/README.md` as the generated solution's `README.md` and `template/ci.yml` as `.github/workflows/ci.yml`, while leaving the template repository's own `README.md`, the rest of `.github/`, the community files and the repository and maintainer skills out. Those skills are listed in `RepositorySkills` in `template/template.csproj`; a new one is added there. The pipeline fails a package over 1 MB.

## Getting found

`dotnet new search` and `dotnet new list` match any part of the template `name` or of any short name, and nothing else. `--tag` matches a whole classification, and nuget.org and `dotnet package search` read the package's `PackageTags`. So every template puts its search words in all three:

- `shortName` is a list. The first entry is the template's own name in lower case, such as `cleanminimalapi`, and never changes. After it come one or two shorter aliases, such as `cleanminimal` or `cleanmcp`, then `lmca-<key>` and `leanmeancleanapps-<key>`, where the key is the docs site's (`minimalapi`, `mcp`, `graphql`, `webapi`, `lambda`). Those two make searches for clean, lmc, lmca, lean, mean and leanmeanclean find every template. Never a bare short name such as `mcp`, which clashes with other people's templates.
- The `name` and the package `Title` match, and carry the words people search for that the name lacks, such as "(MCP)", "(Hot Chocolate)", "(Controllers)" or "AWS".
- Every template has the `Lean Mean Clean Apps` classification, so `dotnet new list --tag "Lean Mean Clean Apps"` shows the family.
- `PackageTags` carry the tags all five share, brand words included (`clean`, `cleanarchitecture`, `lmc`, `lmca`, `leanmeanclean`, `leanmeancleanapps`), then the template's own.

The README and `NUGET.md` name the aliases under the install commands, and the docs site's template options page lists them. The pipeline's Verify Template step uses the first short name.

## Steps

1. Change `template.json` or `template.csproj`. `template.csproj` references `Microsoft.TemplateEngine.Authoring.Tasks`, Microsoft's template validator, which checks `.template.config` on every build and pack; keep its output free of messages, not just errors. A new option also goes in `dotnetcli.host.json` with a short flag that doesn't clash with `dotnet new`'s own (`-n`, `-o`, `-lang`, `-h`), and in `ide.host.json` with `isVisible` set, or Visual Studio hides it.
2. Keep the `sourceName` out of identifiers. A class called `CleanMinimalApiApplication` becomes invalid when the name is replaced with something like `My.Api`.
3. Test the install from the repository root:

   ``` bash
   dotnet new install ./ --force
   dotnet new <shortName> --help
   dotnet new <shortName> --name Sample --output ../Sample
   dotnet build ../Sample && dotnet test ../Sample
   dotnet new uninstall ./
   ```

   With `--include-auth`, also create one with `--include-auth --authority https://login.example.com --output ../Secured` and test that. Leave the authority out and `dotnet new` should stop with exit code 102.

   `--help` shows the short flags and descriptions. Creating the solution should end with `Restoring .../Sample.slnx` and `Restore succeeded`, which is the post action at work; `--no-restore` should skip it.

4. For package contents, also pack and look inside:

   ``` bash
   dotnet pack template/template.csproj --output packages
   unzip -l packages/*.nupkg
   ```

5. A new option goes in the README and `NUGET.md` options tables, and on the docs site's template options page.

## Don't

- Change `identity` or the first `shortName`; existing installs and docs depend on them. Adding aliases after it is fine (see Getting found).
- Make a primary output that isn't a project visible to the CLI. The restore post action restores every primary output it can see, so `docs/RUN.md` carries the same `HostIdentifier` condition as the action that opens it.
- Add a `.sln`. The solution is `.slnx` only, and `primaryOutputs`, the Dockerfile and the package all point at it.
- Reuse a short flag across options, or give one to `--no-restore`; the `dotnet new` templates from Microsoft leave it long, and so do we.
- Pack with a wildcard over the whole repository; it pulls in build output and pipeline files.
- Add an option without testing the generated solution with it on and off.

## Check

The Test job's Verify Template step installs the packed template, generates a solution and checks that nothing of the template leaked into it (no `includeAuth` markers, no trace of the template's own name, no `icon.png`) and that it has `README.md` and `.github/workflows/ci.yml`, then checks its format and runs its tests. Where the template has `--include-auth` it does it again with the toggle on, and checks that `--include-auth` without `--authority` is refused with exit code 102.
