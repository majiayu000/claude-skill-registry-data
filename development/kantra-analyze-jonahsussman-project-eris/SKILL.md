---
name: kantra-analyze
description: Utilize Kantra, a CLI that unifies analysis and transformation capabilities of Konveyor, to analyze the source code of an application for violations.
allowed-tools: Bash(kantra:*), Bash(yq:*)
---

Utilize the command `/kantra-analyze` to perform analysis on application source code for violations using Kantra. Be sure to ask the user what directory to analyze, as well as suggest target technologies.

IMPORTANT: If the user makes changes to what you suggest, be sure to confirm the final results before continuing.

Then, filter the `output.yaml` (using the schema in `reference.md`) using the scripts provided to extract all the violations found.

IMPORTANT: If making a decision about the input directory, be sure to scope the input directory to only the relevant application code to avoid unnecessary processing of unrelated files.

## Kantra Analyze Command

To show help for the Kantra analyze command, run:

```sh
kantra analyze --help
```


To run analysis on application source code, run:

```sh
kantra analyze --input=<path/to/source/code> --output=<path/to/output/report> --skip-static-report
```

If the output directory already exists, Kantra will fail. To overwrite the directory, supply the `--overwrite` flag.

> [!IMPORTANT]
> `--skip-static-report` is used to avoid generating a static HTML report, which may not be needed in all contexts.


To list all sources and targets, use:

```sh
kantra analyze --list-sources
kantra analyze --list-targets
```

Add targets to the analyze command using multiple `--target=<target>` flags.

> [!IMPORTANT]
> Try to limit the sources and targets to only those relevant to your application to avoid unnecessary processing of unrelated rules.


To list all providers, use:

```sh
kantra analyze --list-providers
```