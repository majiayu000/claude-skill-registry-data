---
name: project-structure
description: Use when adding or moving code in envd-rs — new endpoint, Connect RPC, middleware, helper, module or test. Says which file/folder it belongs in and the code style rules (crates.io-style layout, no mod.rs, no comments, KISS, Go-compatible API).
---

# envd-rs project structure

Layout follows rust-lang/crates.io: `foo.rs` declares submodules that live in `foo/`. Never create `mod.rs`.

```
Cargo.toml             workspace only: members = ["crates/*"], release profile
crates/orchestrator/   orchestrator crate (same layout rules as envd below)
  src/storage/         object_store backends (backend.rs: Storage::open per provider, signed UploadUrl;
                       backend/providers.rs: S3, GCS, Azure builders; backend/gcs/ ADC, credential flows, external
                       accounts; backend/azure/ DefaultAzureCredential chain, AAD, WS-Trust, SAS; backend/aws.rs + aws/sse.rs S3 server-side encryption headers), object_path.rs (validate_object_path), spec.rs (StorageSpec, upstream storage URL
                       parsing), local_upload.rs (HMAC UploadSigner), build paths, header V3
  src/go_url.rs        Go net/url parse and String (go_url/escape.rs, go_url/query.rs url.Values)
  src/go_exec.rs       commands with Go exec error texts (exit status N, signal: killed, not found in $PATH);
                       go_humanize.rs (humanize.Bytes)
  src/builder/         template builder: config.rs (BuilderConfig env), template_files.rs (+ render.rs Go template
                       subset, layers.rs files/symlink tars, hash.rs filesHash/provision version; assets/template/),
                       ext4.rs (+ stats.rs debugfs parsing), oci/ (reference.rs go-containerregistry names, registry.rs
                       distribution client, auth.rs, ecr.rs SigV4, pull.rs GetPublicImage, untar.rs moby untar with
                       whiteouts, export.rs layers top-first, overlay_mount.rs new mount API, copy.rs rsync),
                       rootfs.rs (+ unpack.rs CreateExt4Filesystem), provision.rs (console marker scan),
                       phases.rs (BuildEnv) + phases/base.rs (+ build.rs), pipeline.rs (PhasePipeline)
  src/go_strconv.rs    strconv.ParseBool, strconv.Quote, caarlos0/env bool errors; go_os.rs (Go PathError text);
                       go_path.rs (path.Clean, Join, Dir, Base)
  src/go_gzip.rs       Go compress/gzip + flate BestSpeed port (layer digests byte for byte); go_tar.rs (Go archive/tar
                       writer: USTAR prefix split, PAX records); go_time.rs + go_time/parse.rs (time.ParseDuration)
  src/featureflags.rs  LaunchDarkly client (featureflags/client.rs: offline fallbacks, overrides), contexts.rs (sandbox,
                       team, service, kind contexts), flags.rs (every upstream flag with its fallback), prefetch.rs
  src/telemetry.rs     OpenTelemetry: metrics.rs, traces.rs, logs.rs (tracing bridge with target/level filters),
                       endpoint.rs (OTEL_COLLECTOR_GRPC_ENDPOINT), fc.rs (vcpu_limit counter), identity.rs (resource), grpc.rs (otelgrpc server
                       spans, traceparent, rpc.server.duration with sandbox.resume and team.id from metadata), report.rs (span errors), server/ (upstream instruments; network.rs slot return duration)
  src/block/           sparse cache + tracker, chunker (storage-backed or local), build file (DiffStore: TTL, pins,
                       disk-pressure eviction), overlay
  src/exposure/nbd/    NBD server (concurrent dispatch over the BlockDevice trait), ioctls, device.rs (attach),
                       pool.rs (DevicePool: process-wide ready devices on std threads, NBD_POOL_SIZE)
  src/network/         slot.rs (slot addressing), slot/host.rs (Linux: netns, veth, tap via rtnetlink/tun,
                       iptables REDIRECTs; HostSlots), pool.rs (NetworkPool: 32 new, 100 reused, 3s return delay, configure/reset egress), storage.rs (SlotStorage: index allocation,
                       leaked namespaces), firewall.rs (nftables slot-firewall: sets, DSCP, EgressRules),
                       settings.rs (SANDBOX_* network env), prerequisites.rs (NETWORK_VERSION=2 checks)
  src/tcpfirewall/     egress TCP proxy on 5016/5017/5018: rules.rs (domain/CIDR allow-deny), sniff.rs (HTTP Host,
                       TLS SNI), proxy.rs (SO_ORIGINAL_DST, 30s dial)
  src/hyperloop/       hyperloop server on 5010 for the guest: server.rs (/me, /logs), logs.rs (SourceSandbox)
  src/proxy.rs         sandbox HTTP proxy on PROXY_PORT 5007 (upstream shared/pkg/proxy + orchestrator/pkg/proxy): server.rs
                       (ProxyServer: h1/h2c accept loop, graceful shutdown, forced close), handler.rs (resolve, refuse with cors/pages,
                       connection limit, forward), forward.rs (hop-by-hop, Host mask, upgrade tunnel), host.rs (sandbox id and port
                       from Host or E2b-Sandbox-* headers), refusal.rs (Refusal), pages.rs + pages/template.rs (JSON/HTML error pages
                       from assets/proxy/*.html, Go template subset), cors.rs, limit.rs + limiter.rs (per-lifecycle connection
                       limit), pool.rs + pool/ (client per lifecycle, retrying dialer, TLS skip-verify), tracking.rs (counted,
                       abortable connections), stream_abort.rs (Connect end-stream frame), destination.rs, body.rs;
                       sandbox.rs (SandboxProxy: ingress token, mask_request_host, https_ports, envd internal routes in
                       sandbox/internal_routes.rs, metrics in sandbox/metrics.rs, node.rs registry lookup)
  src/routing/         publisher.rs (RoutingPublisher: sandbox:routing:{id} on insert/stopping, tombstones),
                       redis.rs (fred client: Redis::connect, RoutingCatalog, EventStream, RedisSettings)
  src/peer.rs          peer chunk sharing between orchestrators (ChunkService): switch.rs (PeerSwitch: installed registry + resolver,
                       flag peer-to-peer-chunk-transfer, register/finish around a snapshot upload, uploaded builds for 1 h),
                       registry.rs (PeerRegistry, key peer:{build}, Redis impl in routing/redis.rs), resolver.rs (Resolver: lazy
                       channels, per-build "switched to storage" flag), handle.rs (PeerHandle, try_peer), stream.rs (PeerChunks,
                       first message decides availability), blob.rs (PeerBlob), seekable.rs (PeerSeekable, SeekableError::Transitioned),
                       parents.rs (PeerParents: a parent that a peer still uploads is waited for in storage), availability.rs, server.rs (ChunkServer: the four RPCs) + server/ (resolve.rs PeerCache lookups, blob.rs and
                       seekable.rs sources, chunk.rs 1 MiB message bound, source.rs SourceError to gRPC status); testing.rs (FakeChunks
                       gRPC server). storage/backend/peered.rs routes Storage reads through the peer for the six served files
  src/events.rs        SandboxEvent, EventsService fan-out to EventSinks (Redis stream gated by wh:{team})
  src/clickhouse/      batcher.rs (1000 rows / 1000 queue / 1s), endpoint.rs (DSN, native writer with TLS),
                       rows.rs (sandbox_events, sandbox_host_stats), sinks.rs
  src/hoststats.rs     per-sandbox host stats sampler (StatsIdentity, cgroup CPU/memory)
  src/oom.rs           OOM kill watermark from envd /metrics
  src/sandbox_observer.rs  per-sandbox envd /metrics poll every 5 s: metrics.rs (SandboxMetrics), poll.rs (clock drift,
                       thresholds, CPU hotplug stuck warning), gauges.rs (e2b.sandbox.* gauges on the 5 s sandbox meter),
                       sandboxes.rs (registry adapter)
  src/volumes.rs       VolumeService (upstream pkg/volumes): service.rs (VolumeServer, volume and path confinement, gRPC
                       trait), one file per RPC (volume.rs, dir_create.rs, dir_list.rs, file_create.rs FileUpload,
                       file_get.rs FileDownload, path_delete.rs, path_stat.rs, path_update.rs), parents.rs (ensure_dirs),
                       entry.rs (EntryInfo, symlinks resolved inside the volume), failure.rs (processError mapping),
                       api_error.rs (UserError status details), spans.rs, test_support.rs;
                       chrooted.rs + chrooted/ (upstream pkg/chrooted: Chrooted confined by openat2 RESOLVE_IN_ROOT
                       through rustix; resolve.rs symlink walk, remove.rs, names.rs, info.rs, file.rs, metrics.rs);
                       the PERSISTENT_VOLUME_MOUNTS config is server/config/volume_mounts.rs
  src/builder/         template-manager role: service.rs (TemplateService RPCs, TemplateBuilder trait), builds.rs
                       (BuildCache, 10 min TTL), logs.rs (BuildLog), phase.rs (Phase trait, run_phases, BuildError),
                       pipeline.rs (PhasePipeline), hash.rs (HashKeys), index.rs (LayerIndex), uploads.rs
                       (LayerUploads: background layer uploads, index written after landing), layer.rs
                       (LayerExecutor: resume or cold boot, update_envd, pause and upload), sandbox_command.rs
                       (logStream adapter), commands.rs + commands/ (RUN, ENV, WORKDIR, USER, COPY; script.rs
                       renders the embedded assets/template/commands/*.sh), phases/ (base, steps: steps and default user,
                       finalize: configure.sh, start/ready, CA bundle from assets/template/finalize/, optimize: prefetch,
                       ensure_free_disk: build-ensure-free-disk-space flag, rootfs grow over NBD, with sizing.rs, measure.rs,
                       resize.rs, offline.rs (NBD device guard), grow.rs; layer/filesystem.rs persists its VM-less layer)
  src/template.rs      Template: snapfile, headers and metadata fetched once per build (OnceCell); template/cache.rs
                       (TemplateCache: 25h sliding TTL, Arc pins, 1 min grace, add_snapshot), metadata.rs
                       (metadata.json with upstream keys, V1 fallback), optimize.rs (collect_prefetch: 2-run trace)
  src/phases.rs        PhaseTimer: resume phase durations and notes
  src/cgroup.rs        cgroup v2 per sandbox, named sbx-<id>-<random>; CgroupStats with memory.peak reset;
                       cgroup/cpu_limit.rs (cpu.max quota, threaded vcpu child holding the fc_vcpu threads), removal.rs
                       (rmdir, cgroup.kill fallback and retry)
  src/firecracker/     config (VmConfig builder), kernel_args.rs (Go buildKernelArgs), console.rs (FC output to tracing with a
                       2000-byte tail and the FlushMetrics filter), client (API over unix socket), launch.rs (unshare -m script, /fc-vm paths),
                       memory_info.rs (GET /memory, /memory/mappings), mmds.rs, vcpus.rs (MAX_VCPUS, machine sizes, fc_vcpu
                       thread count, snapshot capacity refusal), process
  src/memory/          userfaultfd: region.rs (handshake regions, address <-> memfile offset), uffd.rs (safe uffd fd),
                       handshake.rs (SCM_RIGHTS listener, uffd + optional memfd), server.rs (page-fault loop, installed
                       pages, Prefaulter), snapshot.rs (memfile export from the memfd or process_vm_readv),
                       trace.rs (PrefetchTracker, Trace intersection), prefetch.rs + prefetch/ (source.rs init/last-cycle/both,
                       last_cycle.rs, plan.rs, flags.rs worker settings)
  src/envd/upgrade/    resume-time envd live upgrade: target.rs (flag target, candidate, resolve), rollout.rs (EnvdUpgrades: node-local
                       binary cache at <base>/envdbin, startup warm, plan: flag, old_envd gate, resolve, exec-context gate, cached copy),
                       gate.rs (decline reasons), phase.rs (phase labels), deliver.rs (POST /upgrade to envd); envd/report.rs
                       (X-Envd-Version, -Handover, -Defaults headers of /init); sandbox/upgrade.rs (Sandbox keeps the report, compares
                       defaults, call_envd_upgrade); server/node/upgrade.rs (Node::maybe_upgrade_envd: deliver, wait ready, confirm,
                       handover metrics, called by start_with); telemetry/envd_defaults.rs (orchestrator.envd.defaults.* counters)
  src/envd.rs          envd POST /init client (upstream retry semantics); envd/version.rs (Go semver, snapshot >= 0.5.0);
                       envd/process.rs (Connect process.Start client, bash -l -c as a user), body.rs (bounded reads of
                       guest responses), cpus.rs (X-Envd-Cpus check),
                       quiesce.rs + quiesce/guest.rs (GuestQuiesce: fsfreeze, fsthaw, exec fallback, guest sync before a
                       filesystem-only snapshot; GuestEnvd posts and shell commands)
  src/storage/build.rs Build: memfile + rootfs headers of a snapshot
  src/sandbox.rs       Sandbox lifecycle: cold_boot, stop; sandbox/config.rs builder, resources.rs (teardown, Drop),
                       vcpu_limit.rs (resume VM size, boot quota, confine vCPU threads), reboot.rs (filesystem boot gate,
                       CPU template pick and check, VM size),
                       snapshot.rs (Snapshot, LocalSnapshot, snapshot_into/pause_into/pause: dirty pages via /memory/dirty or resident-empty, rootfs diff, upload;
                       snapshot/filesystem.rs: FilesystemSnapshot, a VM-less layer of header, metadata and optional rootfs diff;
                       snapshot/in_place.rs: filesystem-only checkpoint of the running VM: quiesce, pause, snapshot,
                       rootfs export, resume in place, thaw, with rollback and the lost-sandbox failures),
                       resume.rs (snapshot load over uffd),
                       harvest.rs + harvest/ (pause harvest: throwaway deny-egress resume recording a fresh trace)
  src/server/          gRPC node: config.rs (env; config/storage.rs: TEMPLATE_/BUILD_CACHE_ storage resolution,
                       config/binaries.rs: kernel and Firecracker per version), vcpus.rs (Create vcpu validation, cold boot
                       size, filesystem boot dispatch), node/reboot.rs (Node::reboot, the filesystem boot),
                       upload.rs (local HMAC PUT /upload), node.rs (Node: storage, store, registry, network pool, template cache),
                       node/checkpoint.rs (Checkpoint: route decision, resume-fresh; checkpoint/route.rs gates and balloon mode,
                       checkpoint/in_place.rs filesystem-only in-place checkpoint, cache, upload, killed event), lifecycle.rs (task per sandbox: commands, end_time
                       expiry, death watch), service.rs (SandboxService), registry.rs (Go map semantics: reserve,
                       lifecycle-aware stop, stop_reserved), services.rs (ORCHESTRATOR_SERVICES roles),
                       scheduling.rs (SchedulingMetadata from headers), user_error.rs (UserError status details),
                       host_stats.rs and oom_monitor.rs (per-sandbox collectors), status.rs (NodeStatus, override rules, outstanding work), metrics.rs (host
                       metrics poller, /proc parsers), info.rs (InfoService), health.rs (/health on the tonic router),
                       admission.rs (max sandboxes from flags; admission/semaphore.rs resizable starting semaphore), pause_disk.rs (BuildDisk, PauseDiskReservation: refuse a pause the build filesystem cannot hold; node/pause_disk.rs admits it), shutdown.rs (drain), app.rs (App: one axum
                       router for SandboxService, InfoService, grpc health and /health), retry.rs (upload retry
                       policy), uploads.rs (Uploads: background snapshot uploads, parents land first)
  src/proto.rs         tonic::include_proto!("_") of proto/orchestrator/*.proto (no package upstream)
  src/main.rs          orchestrator binary: NodeConfig::from_env, App served by axum on GRPC_PORT (5008), upstream shutdown order
  src/bin/resume-build.rs  dev tool binary (upstream cmd/resume-build); the logic lives in src/resume_build.rs + resume_build/
                       (options: Go-style flags via go_flag.rs, env: setupEnv, runner: resume/cmd/pause/benchmark over an in-process
                       SandboxServer, guest: envd commands and pause signals, shell: PTY via envd/pty.rs, optimize, fph_bench, gdb)
  examples/sandbox.rs  dev runner: cold or (E2B_RESUME=1) resumed sandbox, 127.0.0.1:49983 forwarded to envd
  tests/*_contract.rs  Linux-only (root, KVM, nbd) integration tests, run in CI; proxy_contract.rs and sandbox_proxy_contract.rs
                       run anywhere (tests/proxy_contract/support.rs: backends, TLS fixtures in tests/fixtures/proxy)
docker/guest.Dockerfile + envd.service  test microVM rootfs (Debian, envd under systemd)
scripts/ci/            CI helpers: vm-assets.sh, guest-rootfs.sh, vm-sdk-tests.sh, s3.sh, kvm-spike.sh
scripts/clippy-linux.sh clippy of the whole workspace in Docker (rust:1.98) to catch Linux-only compile errors on a Mac
proto/envd/            envd .proto copied from upstream E2B (never edit)
proto/orchestrator/    orchestrator, info, template-manager and volume .proto copied from upstream E2B (never edit), UPSTREAM_COMMIT
website/               Fumadocs (Next.js, static export) docs: content/docs/**/*.mdx in English, *.cs.mdx and
                       meta.cs.json in Czech; lib/i18n.ts (en default, cs), components/mermaid.tsx; npm run build
crates/envd/build.rs   codegen from ../../proto/envd
crates/envd/reference/ upstream envd OpenAPI + pinned commit
crates/envd/src/
  main.rs              parse config, init tracing, bind, serve. Nothing else.
  lib.rs               pub mod list only
  config.rs            CLI flags (Go `flag` compatible)
  app.rs               AppState (shared state, Arc), Defaults
  router.rs            build_router: every REST route + Connect services + layers, in one place
  auth.rs              who is calling: basic_username, request_user, URL signing
  middleware.rs        pub mod list
  middleware/          one file per tower middleware (access_token.rs, basic_auth.rs)
  controllers.rs       pub mod list
  controllers/         one file per area: health.rs, envs.rs, init.rs, filesystem.rs, ...
  controllers/<area>/  helpers of a big area (filesystem/entry.rs, ops.rs, watch.rs; files/download.rs, upload.rs, compose.rs, encoding.rs; process/spawn.rs, output.rs, events.rs, registry.rs)
  host.rs + host/      things done to the VM (clock, /etc/hosts, MMDS)
  user.rs              Linux users/groups
  envvars.rs           env vars for spawned processes
  util.rs + util/      small shared helpers (error_response.rs; fs.rs: OS error text, eval_symlinks; paths.rs; keepalive.rs; metadata.rs: user.e2b.* xattrs)
  proto.rs             include_generated!() only
crates/envd/tests/     HTTP contract tests against a real server (tests/common: spawn_server_with_state)
```

## Where does new code go

| Adding | Put it in |
|---|---|
| REST endpoint | handler fn in `controllers/<area>.rs`, route line in `router.rs` |
| Connect service | `controllers/<service>.rs` with `impl <Trait> for <Service>`, register in `router.rs` |
| Logic of a big controller | `controllers/<area>/<topic>.rs`, plain `pub fn` |
| Middleware for every request | `middleware/<name>.rs`, `.layer(...)` in `router.rs` |
| Shared state | field on `AppState` in `app.rs` |
| Helper used by 2+ areas | `util/<topic>.rs` |
| New top-level concern (processes, cgroups) | `<concern>.rs` + `<concern>/` at the crate `src/` root |

Handler names: verb + thing (`get_envs`, `post_init`). Connect methods keep the generated names.

## Code rules

- **No comments at all** — no `//`, `///`, `//!`. Names carry the meaning.
- **KISS**: no traits, newtypes, error enums or wrapper/delegating methods unless the compiler forces them. Free functions, `match`, `?`, iterator chains.
- **Chaining**: write code as method chains — `Option`/`Result`/iterator combinators (`map`, `and_then`, `filter`, `map_or`, `is_none_or`, `try_for_each`) rather than `if let`/`let else` with early returns, e.g. `headers.get(..).and_then(..).filter(..).map_or(DEFAULT, ..)`.
- **Builders**: build values with builder chains, e.g. `ErrorResponse::builder().status(StatusCode::NOT_FOUND).message(text).build()`. A struct created in several places gets its own `builder()`; use library builders (`OpenOptions`, `Response::builder`).
- **Named fields always**: no tuple structs (`struct Foo(Bar)`), no `.0`/`.1` field access.
- Errors are `String`, `io::Error`, `ConnectError` or `util::error_response::ErrorResponse` (REST JSON/plain error like Go `jsonError`) carrying the exact text the client sees.
- **API = upstream Go envd**: paths, status codes, JSON shapes, header names and error texts must match byte for byte. Check the Go source before writing; internals are plain Rust.
- Unit tests live in `#[cfg(test)] mod tests` at the bottom of the same file; HTTP behaviour goes in `crates/<crate>/tests/*_contract.rs`.
- `rustfmt.toml` sets `max_width = 120`; run `cargo fmt` and `cargo clippy --all-targets` before committing.

## Request flow

```
CORS -> require_token (middleware/access_token.rs)
     -> authenticate_user (middleware/basic_auth.rs, puts User into extensions)
     -> REST route from router.rs, or fallback to Connect router
     -> controller fn
```
