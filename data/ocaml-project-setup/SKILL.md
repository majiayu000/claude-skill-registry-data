---
name: ocaml-project-setup
description: Standards for OCaml project metadata files. Use when initializing a new OCaml library/module, preparing for opam release, setting up CI, or discussing project structure. Not for normal code edits.
license: ISC
---

# OCaml Project Setup Standards

## When to Use This Skill

Invoke this skill when:

1. **Initializing a new OCaml project** - Setting up dune-project, LICENSE, README, CI, etc.
2. **Preparing for opam release** - Ensuring all metadata is correct for publication
3. **Setting up CI/CD** - Configuring GitHub Actions, Tangled, or GitLab CI
4. **Discussing project structure** - Best practices for directory layout

**Do not use for:**
- Regular code edits or bug fixes
- Simple function additions
- Refactoring existing code

## User Configuration

Read configuration from `~/.claude/ocaml-config.json`:

```json
{
  "author": {
    "name": "Author Name",
    "email": "author@example.com"
  },
  "license": "ISC",
  "copyright_year_start": 2025,
  "ci_platform": "github",
  "git_hosting": {
    "type": "github",
    "org": "username"
  },
  "opam_overlay": {
    "enabled": false,
    "path": null,
    "name": null
  },
  "ocaml_version": "5.2.0"
}
```

If config file doesn't exist, prompt user for values and offer to save.

## License Header

Every OCaml source file should start with a license header. Use the configured license.

**ISC License:**
```ocaml
(*---------------------------------------------------------------------------
  Copyright (c) {{YEAR}} {{AUTHOR_NAME}} <{{AUTHOR_EMAIL}}>. All rights reserved.
  SPDX-License-Identifier: ISC
 ---------------------------------------------------------------------------*)
```

**MIT License:**
```ocaml
(*---------------------------------------------------------------------------
  Copyright (c) {{YEAR}} {{AUTHOR_NAME}} <{{AUTHOR_EMAIL}}>

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
  SPDX-License-Identifier: MIT
 ---------------------------------------------------------------------------*)
```

## Build System (Dune)

Use Dune for builds with automatic opam file generation.

### dune-project

See `templates/dune-project.template` for the full template.

Key points:
- Always set `(generate_opam_files true)`
- Use `(maintenance_intent "(latest)")` for actively maintained projects
- **Do not add a `(version ...)` field** - added at release time
- For Tangled projects, use appropriate URL schema

### Root dune file

See `templates/dune-root.template`.

Include `(data_only_dirs third_party)` to ignore fetched dependency sources.

## Version Control

### .gitignore

See `templates/gitignore` for the standard template.

Always include:
- `_build/`
- `third_party/`
- `*.install`
- Editor and OS files

## Code Formatting

Use OCamlFormat with default styling.

See `templates/ocamlformat` - current version 0.28.1.

## Continuous Integration

Templates available for:
- GitHub Actions: `templates/ci-github.yml`
- Tangled: `templates/ci-tangled.yml`
- GitLab CI: `templates/ci-gitlab.yml`

Select based on user's `ci_platform` configuration.

## Documentation

### README.md

See `templates/README.template.md` for structure.

Include:
- Project title and brief description
- Key features
- Installation instructions
- Usage examples
- License

## File Checklist for New Projects

Essential files:
- [ ] `README.md`
- [ ] `dune-project`
- [ ] `dune` (root)
- [ ] `.ocamlformat`
- [ ] `.gitignore`
- [ ] `LICENSE.md`
- [ ] CI configuration (based on platform)
- [ ] Source files with license headers

Test files:
- [ ] `test/dune`
- [ ] `test/test_*.ml`

## Template Variables

When using templates, replace:
- `{{PROJECT_NAME}}` - snake_case project name
- `{{PROJECT_NAME_KEBAB}}` - kebab-case project name
- `{{AUTHOR_NAME}}` - from config
- `{{AUTHOR_EMAIL}}` - from config
- `{{YEAR}}` - current year
- `{{LICENSE}}` - license identifier (ISC, MIT, etc.)
- `{{OCAML_VERSION}}` - minimum OCaml version
- `{{GIT_URL}}` - full git URL
- `{{GIT_HOSTING_TYPE}}` - github, tangled, or gitlab
