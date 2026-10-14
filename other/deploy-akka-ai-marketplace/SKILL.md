---
name: deploy
description: "Build a container image, push it, and deploy the service to the Akka platform. This is the transition from local development to development on the AAO platform."
---

## User Input

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

This command transitions the service from **local development** to the
**Akka platform**. It builds a container image, pushes it to a registry,
deploys it, and configures routing. Only run this when the service works
locally (via `/akka:build`) and you're ready to ship.

## Outline

1. **Pre-flight checks**:
   - Run `mvn compile` and `mvn test` — do not deploy if tests fail
   - **Ensure platform context**:
     1. Read `akka://context` resource to check current org/project
     2. If organization is empty:
        a. Call `akka_organizations_list` to get available orgs
        b. Present the list to the user and ask which to use
        c. Remember the chosen org for subsequent tool calls
     3. If project is empty:
        a. Call `akka_projects_list` (pass `organization` parameter if known)
        b. If projects exist: present list and ask user to pick
        c. If none: ask if they want to create one via `akka_projects_create`
        d. Remember the chosen project for subsequent tool calls
     4. Read `akka://regions` to confirm target region
     5. **IMPORTANT**: Pass the chosen project as the `project` parameter on
        every platform tool call. Do NOT call `akka config set` — that
        modifies the user's persistent CLI configuration.
   - **Check the service name**: Read `pom.xml` and check the `<artifactId>`.
     If it is a scaffold default (e.g. `empty-service`, `my-service`,
     `example-service`), ask the user what service name they want to deploy
     as. Use the user's chosen name as the `service` parameter in
     `akka_services_deploy` — do NOT rename the artifactId in pom.xml.
   - **Check Docker image store**: Docker Desktop may have the containerd
     image store enabled, which is incompatible with the Akka container
     registry push flow. Check `docker info` output for `containerd` as the
     storage driver or image store. If detected, warn the user:
     _"Docker Desktop appears to be using the containerd image store, which
     is incompatible with the Akka container registry push flow. Please:_
     1. _Open Docker Desktop → Settings → General_
     2. _Uncheck 'Use containerd for pulling and storing images'_
     3. _Apply & Restart Docker Desktop_

     _Then let me know and I'll continue the deploy."_
     Do NOT proceed with the build until the user confirms this is resolved.

   - **Check for reliability testing artifacts**: Look for
     `.akka/reliability.manifest` or an `AdminEndpoint.java` file in the
     project's api package. If found, warn the user:
     _"Reliability testing admin endpoint detected. This endpoint provides
     full cluster control and proxied access to business endpoints — it
     must not be deployed to production. Run `/akka:reliability remove`
     to clean up before deploying."_
     Ask the user whether to proceed anyway (for development/staging
     deployments) or stop and run the remove command first.

   - Confirm with the user that they want to deploy to the platform

2. **Stop local services**: Before building the container image, call
   `akka_local_stop_service` to stop any locally running instance of the
   service. Running services hold file locks on build artifacts that prevent
   `mvn clean install` from packaging the image. Then call `akka_local_stop`
   to shut down the local runtime environment. If nothing is running, these
   calls are safe no-ops — proceed to the next step.

3. **Build container image**: Use `akka_build_image` MCP tool to run
   `mvn clean install -DskipTests`. This creates a local Docker image.
   Note the image name and tag from the output.

4. **Deploy to platform**: Choose the appropriate method:

   **Option A — Direct deploy** (quick iteration):
   - Use `akka_services_deploy` MCP tool with the image:tag and `push=true`
   - The `--push` flag pushes the image to the Akka container registry
     and deploys it in one step
   - Docker registry credentials are configured automatically if the user
     is logged in via `akka auth login` — no separate credential setup needed
   - Use `secret_env` to inject secrets (e.g. `{"MY_VAR": "secret-name/key"}`)
   - Suitable for development and testing

   **Option B — Descriptor-based deploy** (production):
   - Use `akka_push_image` to build and push the image first
   - Use `akka_project_export` to capture current state
   - Modify or create a project descriptor YAML with the new service
   - Use `akka_project_validate` to check the descriptor
   - Use `akka_project_apply` with `dry_run=true` first
   - Use `akka_project_apply` to apply

5. **Verify deployment**:
   - Use `akka_services_get` to check service status
   - Use `akka_services_logs` to verify the service started correctly
   - Check for errors in the logs

6. **Inspect deployed service** (optional): Use backoffice tools to inspect the
   deployed service's runtime state. These are read-only and safe for production.
   - `akka_backoffice_list_components` to verify all expected components
     (entities, views, workflows, agents) are registered and active
   - `akka_backoffice_get_entity_state` or `akka_backoffice_list_events` to
     spot-check entity state if test traffic has been sent
   - `akka_backoffice_get_workflow` to verify workflow execution
   - `akka_backoffice_query_view` to confirm view projections are working
   - `akka_backoffice_list_timers` to check timer registrations
   - Do NOT pass `local=true` — these calls target the deployed service

7. **Configure routing** (if needed):
   - Use `akka_routes_list` to check existing routes
   - If routes already exist for this service, no action needed
   - If no routes exist and the user wants external access:
     - Use `akka_hostnames_list` to check if the project has a hostname
     - If no hostnames exist, use `akka_hostnames_add` (without a hostname
       parameter) to get an auto-generated hostname — this is the easiest
       option for development
     - Once a hostname exists, use `akka_routes_create` with a path
       mapping (e.g. path `/` → service name)
   - If the user doesn't need external access yet, skip routing

8. **Report**: Summarize deployment:
   - Image URI pushed
   - Service name and version
   - Region deployed to
   - Route URL (if configured)
   - Service status
   - Component health (if backoffice inspection was performed)

## Key Rules

- ALWAYS run tests before deploying — do not deploy broken code
- ALWAYS confirm with the user before deploying to the platform
- Always validate descriptors before applying
- Always use dry_run before real apply
- Check logs after deployment to verify health
- Prefer descriptor-based deployment for production
- **NEVER modify pom.xml for image building or deployment** — do not add Jib,
  docker-maven-plugin, buildx configuration, or any other image-related plugins.
  The Akka SDK parent POM already configures docker-maven-plugin with the correct
  platform (`linux/amd64`) and base image. Running `mvn clean install -DskipTests`
  (via `akka_build_image`) is all that's needed to produce a deployable image.
  If the build fails with architecture errors, check that Docker/Colima is running
  and supports buildx — do NOT attempt to fix it by editing pom.xml.

## Done When

- [ ] `mvn compile` and `mvn test` succeeded — no deploy was attempted with failing tests.
- [ ] Platform context is confirmed: `akka://context` was read; an organization and project were selected (from `akka_organizations_list` / `akka_projects_list` if empty) and passed as the `project` parameter on every subsequent platform call — `akka config set` was NOT invoked.
- [ ] The target region was confirmed via `akka://regions`.
- [ ] The `pom.xml` `<artifactId>` was checked; if it was a scaffold default, the user supplied the deploy service name and it was passed as the `service` parameter to `akka_services_deploy` — `<artifactId>` was NOT renamed.
- [ ] Docker Desktop was checked for the containerd image store; if detected, the deploy paused until the user disabled it and confirmed.
- [ ] The user explicitly confirmed the deploy.
- [ ] `akka_local_stop_service` and `akka_local_stop` were called to release file locks before building the image.
- [ ] `akka_build_image` produced a local Docker image and the image name/tag are known.
- [ ] Either Option A (`akka_services_deploy` with `push=true`) or Option B (`akka_push_image` → `akka_project_export` → `akka_project_validate` → `akka_project_apply` with `dry_run=true` then real apply) completed successfully — production deploys used the descriptor-based flow.
- [ ] `akka_services_get` and `akka_services_logs` confirm the deployed service is healthy with no startup errors.
- [ ] Routing was configured only if requested; when configured, a hostname exists (`akka_hostnames_list` / `akka_hostnames_add`) and a route maps to the service (`akka_routes_create`).
- [ ] NO changes were made to `pom.xml` for image building or deployment — no Jib, docker-maven-plugin, or buildx plugins were added.
- [ ] The report includes image URI, service name and version, region, route URL (if configured), and current service status.
