---
name: obscure-package-master
description: Use this skill if your uncertainty with a package's API is > 5% to create a deterministic, versioned mirror of the package repo with a built-in coordinate system, installed as an additional skill.
---

# Obscure Package Master

This skill allows you to ground yourself in the objective reality of a package's source code by generating a deterministic "grep map" and a local mirror of its source.

## Trigger Scenarios
- You are working with a library that is not in your top-tier training set (e.g., NOT `numpy`, `pandas`, `requests`).
- You find yourself searching for basic API signatures or parameters for a library.
- You have a >= 5% uncertainty about a package's API behavior or structure.
- The package's documentation is sparse or confusing.

## Instructions
When the trigger conditions are met, follow these steps to generate a grounded reference for the package:

1.  **Identify the Package & Version:** Determine the package name and the exact version you need (e.g., from `requirements.txt`, `pyproject.toml`, or `pip show`).
2.  **Run the Generator:** Execute the `generate_mirror.py` script to create a local skill for that specific package version.
    
    ```bash
    # Install into the provider's global skills directory (auto-detected from install path):
    python3 <path_to_scripts>/generate_mirror.py <package> <version>

    # Install into the project's local provider skills directory (e.g., ./.claude/skills/):
    python3 <path_to_scripts>/generate_mirror.py <package> <version> --local

    # Install into an explicit directory:
    python3 <path_to_scripts>/generate_mirror.py <package> <version> /path/to/skills
    ```

3.  **Activate the New Skill:** Once generated, a new skill will be available at `<skills_dir>/<package>-<version>`.
4.  **Use the Grep Map:** Read the `SKILL.md` of the newly created skill. It contains a map of all classes and functions with their exact line ranges.
5.  **Targeted Reading:** Use the map to perform surgical `read_file` calls on the files in the `references/` directory of the new skill.
    -   *Example:* "I see `MyClass.my_method` is in `references/utils.py` lines 120-145. I will read those lines now."

## Core Principles
- **Deterministic:** The map is a direct reflection of the source code (AST-parsed). No LLM interpretation is involved in building the map.
- **Coordinate System:** Use the provided line ranges to avoid reading large files. Only grep exactly what you need.
- **Grounding:** If the package source is available, there is no excuse for API hallucinations.

## Provider Compatibility

This skill works with any AI agent provider that can execute Python scripts. The output location is determined automatically from the script's install path, or can be configured explicitly.

**Output directory priority** (highest wins):
1. Explicit `output_path` positional argument on the CLI
2. `--local` CLI flag → project-local provider skills directory (e.g., `./.claude/skills/`)
3. `AGENT_SKILLS_PATH` environment variable
4. `skills_path` in `config.json`
5. Provider-specific default (auto-detected from the script's install path — both `~/` and `./` roots are checked — or set explicitly via `provider` in `config.json` / `AGENT_PROVIDER` env var)

If none of the above apply, the script exits with an error listing the available options.

### Environment variables read by the script

| Variable | Purpose |
|---|---|
| `AGENT_PROVIDER` | Explicit provider selection (optional) |
| `AGENT_SKILLS_PATH` | Explicit output path override (optional) |

Example `config.json` for explicit provider selection:
```json
{
  "provider": "gemini"
}
```

---
*Note: This skill currently supports Python packages via PyPI.*
