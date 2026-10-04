---
name: run-the-tests
description: Run the test suites (all of them or one workspace) — TypeScript services, infra synth, web unit + Playwright, Flink, iOS — and know which need Docker or exiftool.
---
# Run the tests

About 85 test files across TypeScript workspaces, the Flink job (Java), and the iOS
app (Swift). Suites needing Docker or exiftool detect the dependency and
self-skip, so the root command always completes on a bare laptop. TDD is the
rule for `services/`, `flink/`, and `web/src/lib`: failing test first.

## Read first
- docs/TESTING.md — the 12-stop guided tour, per-suite "Needs" lines, coverage gates, and Known issues.

## Commands
```bash
npm test --workspaces --if-present -- --coverage   # everything CI's backend job runs
npm test --workspace services/<name>               # one service (shared, api, graph-writer, mcp, publisher, ...)
npm test --workspace infra                         # CDK synth assertions (FinOps, tags, secrets)
npm test --workspace web                           # web units
npm run test:e2e --workspace web                   # Playwright (once: cd web && npx playwright install --with-deps chromium)
./gradlew -p flink test                            # Flink MiniCluster (Java 17, no Docker)
xcodebuild test -project app/BasicEventProducer.xcodeproj -scheme BasicEventProducer \
  -destination 'platform=iOS Simulator,name=iPhone 17 Pro'   # iOS (Mac + Xcode)
```

## Gotchas
- Docker is needed by the integration files in services/shared (Redpanda + Neo4j), graph-writer, mcp, and publisher's golden test — they start testcontainers and self-skip when `docker info` fails. Set `WOS_GRAPH_URI`/`_USER`/`_PASSWORD` to use an external Neo4j instead (trip ids prefixed `test-`, torn down).
- `services/publisher/test/assets.exif.test.ts` needs `exiftool` on PATH (`brew install exiftool`); it self-skips otherwise — including in CI, where no workflow installs it (known gap).
- Coverage thresholds live in each workspace's vitest.config.ts and only fail the build when `--coverage` is passed — that flag is what makes CI enforcing.
- First testcontainer run pulls images; hook timeouts allow up to 8 minutes.
- 100%-branch-gated files: shared/envelope.ts, mcp/scrub.ts, publisher/scrub.ts, graph-writer/labels.ts.
