---
name: rseng-reproducible-environments
description: >-
  Covers making research software environments reproducible: pinning a
  language version and its dependencies in a per-project virtual environment,
  choosing a package/environment manager, and packaging code and its full
  stack into a container. Use when the user asks how to set up
  venv/conda/poetry/uv/renv, lock or pin dependencies, share a runnable
  environment, escape "dependency hell" or "works on my machine", write a
  Dockerfile, build an Apptainer/Singularity image for HPC, or decide between
  a virtual environment and a container. For regenerating a project's results
  end to end see rseng-reproducibility; for environments of multi-step pipelines
  see rseng-workflows.
license: CC-BY-4.0
metadata:
  version: 0.2.0
---

# Reproducible software environments

Use this skill when software must behave the same on another machine, a
cluster, a CI runner, or a reviewer's laptop as it does on the author's.
Two complementary tools deliver this: a per-project virtual environment
that isolates the language interpreter and its libraries, and a container
that packages the code together with its entire dependency stack. Reach
for the virtual environment when developing or modifying code in one
language; reach for the container when the environment must travel across
machines, platforms, or pipelines unchanged.

## Pick the right level of isolation

Match the tool to how far the software has to travel and what it depends on:

- Language-specific virtual environment - isolates one interpreter/compiler
  version plus library versions for a single project. Default choice while
  developing, running, or modifying someone's code in one language.
- Container (Docker, Apptainer/Singularity, Docker Compose) - packages the
  whole environment, including non-language system libraries and OS-level
  config. Choose when the code must run unchanged across collaborators'
  machines, clusters, or cloud, or plug into CI/CD.
- System-level tools (Vagrant, NixOS, Packer) - reproduce a whole machine
  image or OS configuration as code. Use when the OS itself is part of what
  must be reproduced.
- Workflow environments (Nextflow, Snakemake, Galaxy, CWL/WDL) - manage
  reproducible environments for multi-step, multi-tool analysis pipelines;
  hand off to the workflows skill for these.

Decision rule: developing in one language -> virtual environment; must run
identically elsewhere, has system-level dependencies, or feeds CI/CD ->
container; the OS is part of the artifact -> system-level tool; a
multi-step pipeline -> workflow manager.

## Always work inside a per-project virtual environment

A virtual environment gives each project its own interpreter version and
its own library versions, so projects with clashing requirements coexist
without interference:

- Create one environment per project, never one global environment shared
  across everything - global installs cause silent version clashes and the
  "spaghetti setup" where nobody knows which dependency is actually in use.
- Keep environments small and scoped; add libraries to a project's own
  environment as the project needs them.
- Use separate environments to run legacy and current code side by side
  (e.g. a Python 2 project alongside a new Python 3 one), and to test a
  dependency upgrade on a branch without disturbing the working version.
- Sharing a description of the environment is what makes work portable,
  reusable, and reproducible - it lets others recreate the same setup and
  run or extend the software.

## Choose one package and environment manager, then commit to it

You need a package manager (install/update/remove libraries) and an
environment manager (create/isolate environments); some tools do both. Pick
per language and stick with it - mixing ad-hoc tools is a common source of
breakage:

- Python, pure-Python dependencies: `venv` + `pip`, or a combined tool like
  Poetry or uv (uv is a fast single tool that replaces pip and venv).
- Python with non-Python (e.g. C/C++) dependencies or multi-platform
  scientific stacks: Conda, which distributes non-Python packages and
  manages its own environments.
- R: renv. Julia: Pkg.jl. C++: Conan. Java: Maven. Ruby: Bundler.
- Cross-language / HPC generic managers: Spack, Nix/NixOS, Guix.

Tie-breakers when several tools fit: prefer what the project, team, or
community already uses so help is available, then personal preference.
State the chosen tool explicitly so contributors do not each reach for a
different one.

## Pin dependencies for reproducibility

Sharing a runnable description of the environment is the deliverable, not
just the code:

- Record the exact interpreter/compiler version and library versions the
  software is known to work with, and commit that manifest with the code:
  `pyproject.toml` + a native lockfile from a modern manager such as uv,
  `environment.yml`, `renv.lock`, `Manifest.toml`. A bare
  `requirements.txt` is an export format, not a project definition.
- One-off scripts count too: give them PEP 723 inline script metadata and
  run them with `uv run script.py`, which resolves and pins the declared
  dependencies on the fly and replaces the loose
  requirements.txt-next-to-a-script pattern entirely.
- Prefer a lockfile that pins transitive dependencies exactly when
  bit-for-bit reproducibility matters; a loosely pinned manifest that
  floats to the latest compatible version is fine for actively developed
  code that must track upstream.
- Pin tightly (exact versions) for released, cited, or result-producing
  software; pin loosely (compatible ranges) for libraries meant to stay
  current - and say which policy the project follows.
- When a project is locked to an older dependency, isolate the upgrade
  attempt in its own environment/branch rather than upgrading in place.

## Containerize when the environment must travel

Containers bundle code plus every dependency and configuration so
developers, collaborators, and reviewers run the identical setup, ending
dependency hell and "works on my machine" failures. Reach for a container when:

- the software needs specific libraries, versions, or system configuration;
- it must run across different machines, clusters, or cloud environments;
- it has to slot into automated workflows or CI/CD;
- long-term reproducibility and scalability matter.

Benefits to explain when recommending one: reproducibility and portability,
fast onboarding (collaborators just pull and run), version control (tag
images to code versions), automation-friendliness (build images in CI/CD),
and lower overhead than full virtual machines.

### Build a Docker image (general-purpose, cloud, networked services)

Standard recipe for a Python project:

- Start from a minimal, explicit base image, e.g. `python:3.10-slim`, or
  `ubuntu:22.04` for a general Linux base - pin the tag, never rely on
  `latest`.
- Copy in the project, install dependencies from the committed manifest,
  and declare the entry point.
- Use multi-stage builds to keep the final image small when build tools are
  not needed at runtime.

```
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "script.py"]
```

- Run, mounting data instead of baking it in:
  `docker run --rm -v /path/to/data:/data my-image:1.0.0 python /data/experiment.py`
- Expose ports for interactive/networked services:
  `docker run -p 8080:80 my-image:1.0.0`
- Distribute via a registry with a version tag, then push/pull:
  `docker tag my-image:1.0.0 user/my-image:1.0.0 && docker push user/my-image:1.0.0`
- Tag images to match code versions so an image is traceable to a commit or
  release.

### Build an Apptainer/Singularity image (HPC, no root)

Prefer Apptainer (formerly Singularity) on clusters where users lack root
access; it is built for reproducible science and large-scale workloads:

- Build a `.sif` file, reusing an existing Docker image when convenient:
  `apptainer build my_container.sif docker://python:3.10-slim`
- Run: `apptainer exec my-container.sif python /data/experiment.py`
- Version by naming the file, e.g. `my-container-v1.0.0.sif`, and store it
  in institutional or shared storage.
- Apptainer generally does not support Docker-style port mapping; for
  networked services prefer Docker.

### Wire containers into CI/CD

Run tests inside the same image the software ships in, so CI reproduces the
production environment. Reference the custom
image as the job image and run the test suite against it; install only
extra dependencies not already baked in. This keeps test and deployment
steps consistent and lets image builds themselves be automated.

## Working with this skill

The generated references.md beside this file lists the source
material and pointers:

- references.md - verified Learn more pointers


Learn more (verified):
  - https://docs.conda.io - conda package and environment manager
  - https://docs.astral.sh/uv/ - uv Python package manager
  - https://rstudio.github.io/renv/ - renv reproducible R environments
  - https://apptainer.org/documentation/ - Apptainer container
    documentation
  - https://book.the-turing-way.org/reproducible-research/renv -
    Turing Way reproducible environments chapter


## Parity between dev and the shipped runtime

When a project runs both bare (dev) and containerized (compose,
production), the two environments drift: an env var set in the
shell but absent from compose, a dependency in the image but not
the lockfile, different service hostnames. Declare shared
configuration ONCE (.env.example consumed by both), derive the
image from the same lockfile the dev environment uses, and treat
"works locally, fails in compose" as an environment diff to be
found (rseng-debugging reads the startup logs; rseng-testing's
entry-point check catches it before handoff).

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-dependency-management - pinning policy and update cadence
- rseng-hpc-computing - Apptainer on clusters without root
- rseng-legacy-code - running old code in isolated environments
- rseng-notebooks - kernel environments belong in lockfiles
- rseng-security - scanning images and pinned dependencies
- rseng-workflows - per-step environments in pipelines

<!-- related-skills:end -->
