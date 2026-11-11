---
description: Keep the Docker container aligned with the template and install Python packages directly in the notebook
model: haiku
---

# Goal

- When creating Docker images for projects and tutorials, we want to
  - Always use the same Docker template image from `class_project` to avoid
    replicating Docker containers
  - Install the needed packages in the notebooks to customize the container

## Inputs

- The user passes:
  - A target dir `<TARGET_DIR>` (e.g.,
    `msml610/tutorials/L03_knowledge_representation`) cloned from
    `class_project/project_template`
  - (Optional) pointers to Jupyter notebooks

# Workflow

## Use the Docker Container From the Project Teamplate

- In the project dir (e.g., `msml610/tutorials/L03_knowledge_representation`),
  use the same `Dockerfile` and `requirements.txt` as the matching files in
  `class_project/project_template`, so the project container matches the class
  project template
- If the image needs something that `pip` cannot install, add it to `Dockerfile`
  with a clear comment on why it is needed

## Discover All Packages Needed by the Notebook

- A notebook's own `import` lines are not the full picture. Each notebook pairs with
  a `*_utils.py` file (e.g., `L03_06_logic_solvers.ipynb` ->
  `L03_06_logic_solvers_utils.py`), imported with a line like:

  ```
  import L03_06_logic_solvers_utils as utils
  ```

- Read the `*_utils.py` file and any local module it imports (transitively). Collect
  every third-party `import` / `from ... import` statement, not just those in the
  notebook
- Map import names to pip names where they differ (e.g., `cv2` -> `opencv-python`,
  `sklearn` -> `scikit-learn`, `PIL` -> `Pillow`, `yaml` -> `PyYAML`)
- Diff this full list against `requirements.txt` and `Dockerfile`. A package used by
  the notebook or its utils that is missing from both is a bug, even if it is
  already installed in the container used to author the notebook
- Add every missing package to `requirements.txt`, and to `Dockerfile` only if it
  cannot be installed with `pip` (per `## Use the Docker Container from the Project
  Teamplate` above)

## Add Packages to Notebooks

- Add a `pip install` cell for the packages needed in each notebook, including every
  package from `## Discover All Packages Needed by the Notebook` above. Install and
  pin the versions
- For each notebook, add after the first call with

  ```
  %load_ext autoreload
  %autoreload 2

  import logging
  ```

  a cell with content like:

  ```
  !pip install -q python-sat==1.9.dev15 sympy==1.14.0 z3-solver==5.1.0.0

  import pysat
  print("pysat version: ", pysat.__version__)
  import sympy
  print("sympy version: ", sympy.__version__)
  import z3
  print("z3 version: ", z3.get_version_string())
  ```

## Sync Notebook

- At the end, sync the paired `.py` file with Jupytext following the conventions in
  `# Code Architecture and Responsibility` ->
  `## Utilities vs. Notebook Responsibilities` in `.claude/skills/notebook.rules.md`

# Verification

- [ ] Every third-party import in the notebook and its paired `*_utils.py` file
      has a matching entry in `requirements.txt` and in the notebook's
      `pip install` cell
- [ ] Build the docker container with `docker_build.sh` inside the target dir
      `<TARGET_DIR>`
- [ ] Make sure the container builds correctly and it's the same as the Docker
      container for the project, if possible
- [ ] Run each notebook inside the docker container with `docker_cmd.sh` and
      `nbconvert` to make sure they run correctly end-to-end

# Conventions

- Always follow the conventions and guidelines in `.claude/skills/notebook.rules.md`
