---
name: pywf-oss-write-doc
description: "Write or update a user-facing Sphinx documentation page of a pywf open-source Python library, as reStructuredText or as a Jupyter notebook with raw reStructuredText cells for cross-references, then build and check it. Use when the user asks to document a feature for its users, write a guide or tutorial page, add a notebook example, or fix the docs. Maintainer knowledge goes to pywf-oss-write-maintain-skill instead."
---

Write or update one docs page under `docs/source/` that builds cleanly, appears in the sidebar, and links correctly to the API reference and other pages.

Read ../pywf-oss-base/SKILL.md, then:
- ../pywf-oss-base/references/13-sphinx.md
- ../pywf-oss-base/references/14-docfly.md
- ../pywf-oss-base/references/15-furo.md (only when changing the look or the theme)
- ../pywf-oss-base/references/16-sphinx-design.md (only when the page needs layout or widgets: cards, tabs, dropdowns, badges, buttons)
- ../pywf-oss-base/references/17-nbsphinx.md (only for notebook pages)
- ../pywf-oss-base/references/18-knowledge-channels.md

Templates: ../pywf-oss-base/assets/notebook-page-template.ipynb and ../pywf-oss-base/assets/raw-rst-cell.json.

## Steps

1. **Pick the channel, the format, and the place.**
   - Check the fact belongs in user docs (`18-knowledge-channels.md` section 2). How to maintain this repo goes to `pywf-oss-write-maintain-skill`; say so, and stop.
   - A notebook for runnable usage guides, `.rst` for concepts and design notes. If the user did not say, choose, and state the choice.
   - List the existing page folders, then choose the `NN-Title` folder that puts the page at the right sidebar position.
2. **Gather facts** from `api.py` and the docstrings of what you document. Examples import from `<package_name>.api`, as users would.
3. **Write.**
   - Give the page a unique label and a title (in a notebook, both in a raw reStructuredText cell).
   - Use cross-reference roles for API names, and `:ref:` for other pages.
   - Edit notebooks with `NotebookEdit` or `nbformat`.
4. **Run notebooks** with the `nbconvert` command in `17-nbsphinx.md` section 5. Every cell must succeed; the outputs are committed.
5. **Build and check** as in `13-sphinx.md` section 4: no new warnings, 0 unresolved cross-references (`check_doc_xrefs.py`, `13-sphinx.md` section 2.2), and the page in the sidebar with the right title. For layout work, also run the visual check.

## Boundaries

- Never edit `docs/source/api/`. To improve the API pages, improve the docstrings, and say so.
- Keep `README.rst` short; long material goes in a docs page the README links to.

Next step: `pywf-oss-changelog`.
