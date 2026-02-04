---
name: new-tool
description: A set of resources to help agents create new tools and integrate them into the site build process for successful deployment
---
# Creating a new tool

For guidance on what a tool is and design guidelines for tools in this repository, please refer to the `Tool Design Guidelines` section of [Tools Repository Instructions](../../../AGENTS.md#tool-design-guidelines).

## When to use this skill

Use this skill when you need to:

- Create the scaffolding and metadata for a new tool
- Integrate the new tool into the site build process

## Overview

Each "tool" is a Hugo [page bundle](https://gohugo.io/content-management/page-bundles/) within the `content/tools/` directory.
The bundle contains a file (usually HTML/JS) that performs a specific function or task and the supporting metadata and documentation to make it easy to find, use, and understand.

The entire process of creating a new tool and getting it integrated into the site can be summarized in the following phases/steps:

### Prep

1. **Clarify requirements**
   - Confirm the tool’s purpose, inputs/outputs, and expected behavior.
   - If not already instructed, decide the primary language (`html` or `python` or other; strong bias towards HTML/JS).

2. **Create the tool bundle**

  If the `hugo` binary is available, the steps below can be automated with the command:

  ```bash
  # This assumes that this will be a HTML tool; adjust `html` to `python` or other as needed
  ❯ hugo new tools/html/new-tool-slug-here
  Content dir "$repoRoot/content/tools/html/new-tool-slug-here" created
  ```

  Else, follow these manual steps:

- Create folder: `content/tools/<language>/<new-tool-slug-here>/`.
- Add `index.md` with front matter (title/description/tags/resources). See existing tools for examples.
  - The `date` field only needs `YYYY-MM-DD` (time is not required).
  - Hugo skips future-dated pages, so use the `date` command to confirm the current date before setting it.

  Regardless of method used to create the bundle, ensure the front matter includes:

- Add tool file as a page resource:
  - `resources: - name: tool-file src: tool.html` (or `tool.py`).
- Add icon as a page resource if instructed to create one or one was provided:
  - `resources: - name: tool-icon src: images/tool-icon.png`.

### Implement the tool

1. **Build the tool file**
   - For HTML/JS tools, create `tool.html` with inline JS/CSS as per design guidelines.
   - Include the local tracking snippet: add `<script src="/analytics.js"></script>` before `</body>` so usage is tracked.
   - For Python tools, create `tool.py` with necessary functionality and PEP-723 header.

2. **Test the tool**
   - For HTML tools, open `tool.html` in a browser to verify functionality.
     - `playwright` can be used for this if automated testing is needed.
   - Run Python tools locally to ensure correct behavior.
     - `pytest` can be used for automated testing if needed.
     - If tests are written for the tool, they should be included in the main tool file for maximum portability.

3. **Add documentation**
   - Write a brief description in `index.md`.
   - Include usage instructions, examples, and any relevant details.

4. **Add icon/image**
   - If an icon/image was provided or created, add it to `images/` within the tool bundle.
   - Reference it in front matter as `tool-icon`.

### Integrate the tool into the site

1. **Add page content**
   - Use `{{< tool-link >}}` for links.
   - Use `{{< tool-image >}}` to render the icon.
   - For Python tools, use `{{< py-usage >}}` inside a fenced code block.

2. **Test locally**
   - Run `hugo server` and verify the tool page renders.
   - Confirm the tool file loads and functions per spec.

3. **Generate data**
   - Run the [`ci/build_tools_data.py`](../../../ci/build_tools_data.py) to refresh [`data/tools.yaml`](../../../data/tools.yaml).
   - Confirm new entry is present and correct.

4. **Verify landing page**
   - Check that `hugo server -D` does not return any errors.
