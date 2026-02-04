---
name: docker-testing
description: Guidance for running and debugging tests in Docker environments for FastAPI + Vue/Tailwind projects.
---

# Docker Testing Skill

Use this skill whenever you need to run the project’s test suite or
diagnose issues inside Docker containers.  It provides a summary of
common commands and troubleshooting steps.

## Running the test suite

- **Build and start services:** Use `docker compose -f docker/docker-compose.yaml up --build` to build all images and start the services in development mode.
- **Run backend tests:** Execute `docker compose -f docker/docker-compose.yaml exec backend python -m pytest` to run the backend test suite.
- **Run frontend tests:** For frontend unit tests, run `docker compose -f docker/docker-compose.yaml exec frontend npm run test` or use the appropriate Vitest command.
- **Check logs:** View logs for all services with `docker compose -f docker/docker-compose.yaml logs -f` or for a specific service with `docker compose -f docker/docker-compose.yaml logs -f backend` or `frontend`.
- **Stop services:** Shut down all running containers with `docker compose -f docker/docker-compose.yaml down`.  Include the `-v` flag to remove volumes for a clean start.

## Troubleshooting tips

- **Port conflicts:** If services fail to start, check that the default ports (backend 8000, frontend 8080) are free.  Modify port mappings in the compose file if necessary.
- **Database issues:** Ensure that the database service is healthy by running `docker compose -f docker/docker-compose.yaml ps` and looking for the “(healthy)” status.  Check `docker compose -f docker/docker-compose.yaml logs db` for errors.
- **API connection errors:** Test the backend directly with `curl http://localhost:8000/docs` to confirm it’s running.  Verify the Nginx configuration in `client/nginx.conf` if the frontend cannot reach `/api/*` endpoints.

## Best practices

- Run tests in a clean environment.  Stop containers and remove volumes if you suspect stale state.
- Use relative paths and environment variables.  Avoid hard‑coded host dependencies so your setup is portable.
- When debugging, read container logs before rerunning tests.  This saves time and surfaces issues like missing migrations or syntax errors.
