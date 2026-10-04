---

name: skill-creator

description: |

  Guide for creating, updating, validating, and packaging Claude skills. Trigger when requested to design a new skill, initialize a skill directory, write a SKILL.md file, run skill utility scripts (init_skill.py, package_skill.py, quick_validate.py), validate skill formats, or package them into ZIP files. Keywords: SKILL.md, init_skill.py, package_skill.py, quick_validate.py, create skill, update skill, package skill, zip skill, skill metadata, progressive disclosure.



  Guide for creating, updating, validating, and packaging Claude skills. Trigger when requested to design a new skill, initialize a skill directory, write a SKILL.md file, run skill utility scripts (init_skill.py, package_skill.py, quick_validate.py), validate skill formats, or package them into ZIP files. Keywords: SKILL.md, init_skill.py, package_skill.py, quick_validate.py, create skill, update skill, package skill, zip skill, skill metadata, progressive disclosure.



license: Complete terms in LICENSE.txt

---



# Skill Creator - Expert Workflow & Guidelines



Provides professional-grade guidelines and workflows for creating, refining, validating, and packaging skills that extend Claude's capabilities. 



## Progressive Disclosure & Resource Loading Triggers



This skill relies on utility scripts located in the `scripts/` subdirectory. Rather than reading the scripts' source code fully, trigger their usage as black boxes using the following command-line executions:



- **Initialize a new skill**: Run `python scripts/init_skill.py --help` to view configuration arguments.

- **Quick validation**: Run `python scripts/quick_validate.py <path/to/skill>` to check local compliance without packaging.

- **Validate and package**: Run `python scripts/package_skill.py <path/to/skill> <output-dir>` to perform schema validation and bundle resources.



## Freedom Calibration & Constraints

- **Constraint Level: Medium-High**

  - **High Rigidity**: Directory structure, YAML frontmatter keys (`name`, `description`), script execution protocols, and validation schemas must be strictly followed.

  - **High Freedom**: Actual content design, domain-specific procedures, visual styles, and asset/script selections are customized based on the target domain.



## Decision Tree: Resource Separation Trade-Offs



Use this tree to determine where specific types of content should live. Keeping `SKILL.md` slim (~5k words max) ensures high context efficiency and prevents LLM distraction.



```

Is the content a code/script, a static reference, or a template/asset?

 ├─ Executable Code or Tool CLI

 │   └─ Is it a short snippet or a reusable utility?

 │       ├─ Short snippet (<=10 lines) → In-line code block in SKILL.md

 │       └─ Reusable/complex utility → Save in scripts/ (e.g., scripts/rotate_pdf.py)

 ├─ Domain Information, Schemas, Policies, APIs, or Documentation

 │   └─ Is it core to the execution loop or auxiliary reference?

 │       ├─ Core execution loop & rules → Directly in SKILL.md

 │       └─ Auxiliary schemas/detailed docs → Save in references/ (e.g., references/api_docs.md)

 └─ Boilerplate, Images, Fonts, or Project Templates

     └─ Save in assets/ (e.g., assets/boilerplate-html/)

```



## Professional Mindset & Design Framework



When creating or modifying a skill, run through this mental checklist:



1. **Who is the user?** (Usually another Claude instance). Design instructions in **imperative/infinitive form** (e.g., "To run validation, execute..." instead of "You should execute...").

2. **What is the minimal context needed?** Keep `SKILL.md` under 5,000 words. Move large schemas, data tables, and extensive lists to `references/`.

3. **What are the fragility points?** Define exactly where Claude or the user might fail (e.g., path resolution, missing dependencies, rate limits) and provide explicit fallbacks.

4. **Is it testable?** Ensure the validation scripts can run cleanly and verify the structure before final delivery.



## Step-by-Step Skill Engineering Procedure



### Step 1: Requirements Gathering & Scoping

- Define the target domain and specific triggers.

- Identify the input formats and output requirements.

- Map the tool dependencies and necessary Python/binary packages.



### Step 2: Directory Initialization

- Run `python scripts/init_skill.py <skill-name> --path <output-directory>` to create the compliant layout.

- Review the generated folders: `scripts/`, `references/`, `assets/`, and `SKILL.md`.



### Step 3: Resource Engineering

- **Create Scripts**: Place Python/Bash scripts in `scripts/`. Keep them modular and self-contained.

- **Populate References**: Put large schemas, markdown tables, or static docs in `references/`.

- **Collect Assets**: Put boilerplate files, templates, or media in `assets/`.



### Step 4: Write the SKILL.md instructions

- Use **imperative/infinitive form** for all procedures (e.g., "Analyze the input data", "Execute the package script").

- Include a robust YAML frontmatter containing `name` and `description` (with clear WHAT, WHEN, and trigger KEYWORDS).

- Add the `NEVER` Anti-Patterns table, decision trees, and error resolution scenarios.



### Step 5: Validation & Verification

- Execute `python scripts/quick_validate.py <path/to/skill-folder>`.

- Fix any issues identified by the validator (e.g., invalid YAML formatting, broken file references).



### Step 6: Packaging

- Package the validated skill using:

  ```bash

  python scripts/package_skill.py <path/to/skill-folder> [optional/output/dir]

  ```

- Deliver the resulting `.zip` artifact to the user.



## Critical Anti-Patterns (NEVER List)



| Anti-Pattern | Description | Alternative / Solution |

| :--- | :--- | :--- |

| **NEVER** duplicate information | Duplicating contents between `SKILL.md` and reference files creates maintenance overhead and validation failures. | Make `SKILL.md` a single source of truth for procedures; keep reference files for data. |

| **NEVER** use second-person text | Using "You should do X" or "We need to Y" degrades parsing efficiency by LLMs. | Write in imperative: "Execute command X", "Verify file exists". |

| **NEVER** write massive inline files | Embedding large code blocks (>50 lines) or database schemas directly in `SKILL.md` bloats context. | Move code blocks to `scripts/` and schemas/tables to `references/`. |

| **NEVER** write absolute local paths | Hardcoding paths like `/home/user/...` breaks compatibility across environments. | Use relative paths from the skill root or environment variables. |

| **NEVER** ignore validation errors | Bypassing validation failures when packaging results in broken skill loading downstream. | Treat all script warnings and validation failures as blocking issues. |

| **NEVER** package without a description | Creating a skill with a blank or placeholder frontmatter prevents Claude from matching/triggering it. | Provide a robust description specifying WHAT, WHEN, and KEYWORDS. |



## Common Error Scenarios & Fallbacks



### Scenario 1: `init_skill.py` fails due to target directory permissions or existing directory

- **Root Cause**: Directory already exists or permissions are read-only.

- **Fallback**: 

  1. Specify a different output path using `--path`.

  2. If the directory exists and must be updated, manually create the files or rename the target directory.



### Scenario 2: Validation fails on metadata schema

- **Root Cause**: The YAML frontmatter is malformed (e.g., missing name/description, missing dashes `---`, invalid characters).

- **Fallback**: Ensure the first lines of the file are exactly:

  ```yaml

  ---

  name: your-skill-name

  description: Robust text here.

  ---

  ```

  Ensure description does not contain unquoted colons `:` which break YAML parsers.



### Scenario 3: Validation fails with "Unreferenced resource files"

- **Root Cause**: A script, reference, or asset exists in the folders but is never mentioned or linked inside the `SKILL.md` text.

- **Fallback**: Edit `SKILL.md` to explain how and when to use that resource, or delete the unused file from the skill directory.


