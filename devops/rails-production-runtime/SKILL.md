---
name: rails-production-runtime
description: Use when designing, reviewing, debugging, or validating Rails production process architecture, Puma sizing, worker/thread concurrency, graceful shutdown, release ordering, health/readiness, runtime configuration, secrets, or container/process lifecycle.
license: MIT
---

# Rails Production Runtime

## Purpose
Treat production as a coordinated runtime system across release artifacts, Puma, Active Job/Solid Queue, database capacity, health/readiness, shutdown/restart, observability, and rollback.

Primary references:
- https://guides.rubyonrails.org/getting_started.html
- https://guides.rubyonrails.org/configuring.html
- https://guides.rubyonrails.org/security.html
- https://puma.io/puma/file.deployment.html
- https://puma.io/puma/file.restart.html
- https://github.com/rails/solid_queue

## Activate when
- changing config/puma.rb or Puma worker/thread settings
- changing WEB_CONCURRENCY or RAILS_MAX_THREADS
- changing graceful shutdown or restart behavior
- changing Solid Queue process configuration
- combining Puma and Solid Queue in one process model
- changing Docker/container/process-manager startup
- defining readiness/liveness for deploys
- changing release/migration ordering
- debugging boot loops, OOM, DB connection exhaustion, or shutdown failures
- changing production secrets/runtime configuration
- planning application rollback around schema changes

## Repository inspection
Inspect Ruby/Rails/Puma/Solid Queue versions, Gemfile.lock, config/puma.rb, queue/recurring configuration, Dockerfile/entrypoint, deployment tooling, CI/CD, health endpoints, DB pools, process concurrency, CPU/memory limits, release migration commands, asset/build commands, required environment variables, signal/shutdown timeouts, and rollback procedures.

Never choose worker/thread counts or restart modes from generic defaults before inspecting the actual deployment topology.

## Runtime topology
Make process roles explicit:

web -> Puma workers/threads
jobs -> Solid Queue supervisor -> dispatchers/workers
scheduler -> recurring tasks

Roles may share or separate resources. Calculate aggregate CPU, memory, and DB connection demand.

## Puma capacity
Puma concurrency is a capacity decision.

Evaluate:
- workers;
- threads per worker;
- CPU budget;
- memory per worker;
- database connection pool;
- downstream API limits;
- request latency and queueing.

Do not increase threads merely because CPU is underutilized. More threads can increase database and downstream pressure.

Do not increase workers without checking aggregate memory.

Use rails-database-engineering for detailed connection-pool analysis and ruby-performance for measured capacity work.

## Restart semantics
Distinguish hot restart from phased restart.

Puma's current deployment/restart documentation treats these as different mechanisms with different constraints. Phased restart replaces workers progressively in cluster mode and requires compatible preload/application behavior; hot restart replaces the process through exec. Verify the installed Puma version before relying on exact semantics.

Never claim zero downtime solely because a restart command completed. Verify schema compatibility, readiness, load-balancer behavior, process health, and deployment artifact compatibility.

## Graceful shutdown
Use an explicit shutdown budget:

signal -> stop accepting work -> finish safe in-flight work -> release resources -> exit before hard-kill deadline

For web and job processes, ensure the application/process manager forwards signals and the graceful timeout is lower than the orchestrator's forced termination deadline.

Solid Queue's supervisor has its own graceful termination behavior and shutdown timeout. Verify the installed version and queue deployment configuration.

## Solid Queue runtime
Separate supervisor, worker, dispatcher, and scheduler configuration.

Do not treat one concurrency number as controlling the entire queue system.

When using the Solid Queue Puma plugin, inspect preload and restart strategy together. The plugin couples process lifecycle and has restart-mode implications documented by Solid Queue.

## Connection capacity
Aggregate:

web DB demand + job DB demand + maintenance demand <= database connection budget

Account for process count, thread count, job worker concurrency, replicas/roles, and multiple databases.

Use rails-database-engineering for detailed pool analysis.

## Containers and PID 1
Verify the actual process receives TERM/INT and that child processes are handled correctly.

Do not use a shell wrapper that swallows signals or leaves orphaned children.

Test both graceful and forced termination behavior where the platform supports it.

## Health/readiness
Keep these concepts separate:

boot health != readiness != dependency health

Use rails-observability for endpoint semantics. Readiness must reflect the deployment contract but should avoid expensive business operations.

Do not make liveness depend on every third-party service unless that restart policy is intentional.

## Release ordering
A rolling release may have old and new processes running simultaneously:

build artifact
-> schema expand
-> compatible application deploy
-> readiness
-> traffic
-> worker compatibility
-> backfill
-> schema contract later

Never deploy code that requires a schema state older workers or web processes cannot tolerate.

## Background-job compatibility
Queued jobs can outlive the web process that enqueued them.

Before deployment verify:
- old jobs still deserialize;
- old job code remains executable against the new schema when required;
- arguments remain compatible;
- removed constants are not referenced by queued jobs;
- queue draining/pause strategy is intentional;
- retries remain safe.

Use rails-active-job for detailed job semantics.

## Runtime configuration
Separate build-time from runtime configuration.

Build-time -> dependencies/assets/code compilation
Runtime -> secrets/endpoints/database credentials/concurrency

Validate required configuration without printing secret values.

Rails supports encrypted credentials and RAILS_MASTER_KEY when the application requires the master key. Keep credentials out of images and logs.

## Memory/CPU
Budget:

Puma master + web workers + job processes + runtime overhead + proxy/sidecars

When diagnosing OOM, correlate process role, workers, threads, workload, Ruby GC/heap behavior, job payloads, and recent releases.

## Migration release gate
Treat db:migrate as a release operation with compatibility and recovery semantics.

Verify lock impact, old/new application compatibility, backfill duration, health impact, rollback feasibility, and queued-job compatibility.

Application rollback is not automatically database rollback.

Use rails-database-engineering for migration safety.

## Process managers
For Docker/Kubernetes/Kamal/systemd or another manager, verify:
- signal forwarding;
- restart policy;
- readiness checks;
- startup/termination timeouts;
- resource limits;
- dependency ordering;
- child process management;
- log collection.

Use the repository's actual deployment system; do not invent platform configuration.

## Verification
Verify actual runtime artifacts:
- production configuration syntax;
- production boot;
- Puma startup;
- job/queue startup;
- readiness endpoint;
- required configuration presence;
- shutdown/restart behavior;
- migration state;
- resource/concurrency calculations;
- deploy and rollback procedure.

Local unit tests alone cannot prove deployment safety.

## Reference example

Production runtime configuration: forced TLS, stdout structured logging, and the standard /up health endpoint left unauthenticated.

```ruby
# config/environments/production.rb
Rails.application.configure do
  config.force_ssl = true                       # HSTS + secure cookies + redirects
  config.assume_ssl = true                      # trust the proxy's X-Forwarded-*
  config.public_file_server.enabled = ENV["RAILS_SERVE_STATIC_FILES"].present?

  config.logger = ActiveSupport::Logger.new($stdout)
    .tap { |logger| logger.formatter = ActiveSupport::Logger::SimpleFormatter.new }

  config.active_record.dump_schema_after_migration = false
end

# The health endpoint must stay cheap and unauthenticated:
#   get "/up", to: proc { [200, {}, ["ok"]] }
# Liveness checks must not touch the database; readiness checks may.
```

## Agent review checklist
- [ ] runtime/framework versions resolved
- [ ] actual deployment/process manager identified
- [ ] Puma worker/thread capacity justified
- [ ] aggregate database connection demand checked
- [ ] memory/CPU budget checked
- [ ] Solid Queue topology checked
- [ ] restart mode compatible with preload/plugin configuration
- [ ] graceful shutdown budget fits platform deadline
- [ ] readiness contract verified
- [ ] release/migration ordering verified
- [ ] queued-job compatibility checked
- [ ] secrets/runtime configuration protected
- [ ] rollback limitations documented
- [ ] focused runtime checks performed
- [ ] final deployment diff reviewed

## Anti-patterns
- increasing Puma threads without DB/downstream analysis
- increasing workers without memory analysis
- enabling Solid Queue in Puma without checking restart semantics
- claiming zero downtime from a restart command alone
- putting secrets in container images or logs
- destructive migration in the same release as incompatible code
- relying on queues being empty during deployment
- swallowing TERM in PID 1
- making readiness expensive
- treating application rollback as database rollback
- using generic production defaults without capacity evidence

## Source foundation
Primary Puma references:
- https://puma.io/puma/file.deployment.html
- https://puma.io/puma/file.restart.html

Primary Rails references:
- https://guides.rubyonrails.org/getting_started.html
- https://guides.rubyonrails.org/configuring.html
- https://guides.rubyonrails.org/security.html

Primary Solid Queue reference:
- https://github.com/rails/solid_queue

Use the installed Rails, Puma, Solid Queue, Ruby, container, and process-manager versions as the compatibility authority.

## Rails production runtime changes

For deployment/runtime changes:
- resolve Rails, Ruby, Puma, Solid Queue, and platform/process-manager versions first;
- inspect actual Puma, container, process-manager, queue, health, and release configuration;
- size web/job concurrency against memory, CPU, database pools, and downstream capacity;
- verify restart mode against preload/plugin configuration;
- align graceful shutdown with the platform hard-kill deadline;
- preserve old/new schema and queued-job compatibility during rolling releases;
- protect runtime secrets and validate required configuration without printing values;
- distinguish application rollback from database/data rollback;
- verify boot, readiness, process lifecycle, and release ordering at the owning boundary.
