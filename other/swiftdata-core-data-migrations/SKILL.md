---
name: swiftdata-core-data-migrations
description: Design, implement, diagnose, and test production schema migrations for SwiftData and Core Data, including VersionedSchema snapshots, SchemaMigrationPlan stages, lightweight and custom Core Data mappings, gradual adoption, CloudKit constraints, and forward-recovery planning. Use when a persistent model changes, an existing store must upgrade without data loss, a team is choosing between SwiftData and Core Data for migration requirements, or copied production stores need validation. Do not use for ordinary fetch/query code, transient in-memory model transformations, unrelated file-format migrations, or advice that assumes Core Data should be replaced merely because SwiftData exists.
---

# SwiftData and Core Data Migrations

Protect the user's existing store first. Select the persistence and migration mechanism from requirements and the installed base, not from framework novelty.

## Inspect before designing

Identify every supported source version, store configuration, target, and sync mode before editing models.

```bash
xcodebuild -version
xcrun swiftc --version
xcodebuild -showBuildSettings -project App.xcodeproj -target App \
  | rg 'IPHONEOS_DEPLOYMENT_TARGET|MACOSX_DEPLOYMENT_TARGET|SWIFT_VERSION'
rg --files | rg '\.(xcdatamodel|xcdatamodeld|mom|momd)$|\.entitlements$|\.storekit$'
rg -n 'VersionedSchema|SchemaMigrationPlan|MigrationStage|ModelContainer|NSPersistent(Container|CloudKitContainer)|NSMigrationManager'
```

Record:

- Current and historical SwiftData schemas or `.xcdatamodel` versions.
- Persistent-store URLs, configurations, App Group use, and SQLite sidecars.
- Minimum OS for the app, extensions, tests, and packages.
- CloudKit container/environment and whether production schema is deployed.
- Store size, relationship cardinality, uniqueness rules, and required invariants.
- All released app versions that users can upgrade from.
- Whether rollback means app-binary rollback, store restoration, or forward repair.

Read [the requirements and planning framework](references/decision-framework.md) before choosing a mechanism.

## Choose from requirements

| Requirement | Prefer | Why |
|---|---|---|
| Existing healthy SwiftData store, iOS 17+ | SwiftData migration | Avoid unnecessary persistence replacement |
| Existing Core Data install base | Core Data migration | Mature versioned models, mapping models, and controlled migration |
| Deployment below SwiftData availability | Core Data | SwiftData is unavailable |
| New, straightforward Swift-native model on supported OS versions | SwiftData | Concise model and migration APIs |
| Complex entity splitting/merging or established custom policies | Core Data | Explicit mapping models and migration policies |
| Gradual adoption alongside an existing stack | Separate stores plus a deliberate boundary | Avoid two frameworks implicitly owning one file |
| CloudKit-backed production data | Keep the proven stack unless requirements justify change | Local and cloud schema evolution both constrain rollout |

Core Data is not obsolete. It remains appropriate for existing applications, older deployment targets, advanced mappings, multiple configurations, and teams that need its controls. Do not propose a SwiftData rewrite without a measured product benefit and an explicit store-conversion plan.

## Classify the change

Create a source-to-destination field and relationship map. For each change, decide whether it is:

- additive and inferable;
- a rename with persistent identity preserved;
- a transform requiring old values;
- a relationship or entity reshape;
- a constraint change requiring cleanup first;
- incompatible with an older binary or CloudKit schema.

Never assume a change is lightweight because it looks small in Swift. Prove compatibility using the framework's model/schema metadata and an on-disk upgrade test.

## Implement SwiftData migrations

Treat every `VersionedSchema` as a complete immutable snapshot, not a diff. Include every persistent model and its historical property types, relationships, attributes, and defaults. Do not edit a schema version after releasing it.

List versions in order in one `SchemaMigrationPlan`, and provide an explicit stage for every supported hop:

```swift
enum AppMigrationPlan: SchemaMigrationPlan {
    static var schemas: [any VersionedSchema.Type] {
        [SchemaV1.self, SchemaV2.self]
    }

    static var stages: [MigrationStage] {
        [.lightweight(fromVersion: SchemaV1.self, toVersion: SchemaV2.self)]
    }
}
```

Use `@Attribute(originalName:)` when a compatible rename should retain persistent identity. Use a custom stage only when data preparation or post-migration work is required.

The custom-stage contexts expose different schemas:

- `willMigrate` operates on the source/old schema.
- `didMigrate` operates on the destination/new schema.

Do not cast or fetch the other version in either closure. If a transform needs facts from both shapes, add an intermediate schema containing temporary transport fields, populate them while the old shape exists, then consume/remove them in a later hop. Batch large transforms and save checkpoints only when the framework's migration semantics make that safe.

Use [the compile-checked SwiftData example](examples/SwiftDataMigration.swift) as syntax guidance, not as a substitute for an on-disk test.

## Implement Core Data migrations

Keep versioned `.xcdatamodel` snapshots and set the intended current version. Prefer inferred lightweight migration only when Core Data can infer a valid mapping. Preserve rename identity with the model editor's renaming identifier.

For type conversion, entity split/merge, relationship reshape, or value synthesis, create a source-to-destination mapping model and use `NSEntityMigrationPolicy` where expressions are insufficient. Test every progressive hop; do not assume one inferred jump covers skipped releases.

`shouldMigrateStoreAutomatically` and `shouldInferMappingModelAutomatically` opt into automatic/inferred behavior. They do not turn an incompatible change into a lightweight migration. See [the Core Data configuration example](examples/CoreDataMigrationConfiguration.swift).

For explicit migration, migrate to a new destination URL, validate it, and replace the original store using a coordinated, recoverable procedure. Never copy a live SQLite main file while its `-wal` contains uncheckpointed data.

## Coexist or adopt gradually

Keep ownership unambiguous:

- Prefer separate stores when adding a SwiftData feature beside an existing Core Data application.
- Exchange stable IDs and Sendable value snapshots, not `NSManagedObject` or live SwiftData model instances.
- Choose one writer for duplicated data and make synchronization idempotent.
- Do not point both frameworks at the same SQLite file merely because SwiftData uses Core Data internally.
- Define how deletion, ordering, conflicts, and partial conversion behave before dual-running.
- Retire the old path only after upgrade telemetry and copied-store tests show conversion is safe.

## Treat CloudKit and rollback as separate constraints

A local store migration does not automatically migrate the CloudKit production schema. Keep cloud changes additive and compatible with old clients during staged rollout. Validate supported model shapes and migration behavior for `NSPersistentCloudKitContainer` or SwiftData CloudKit in a development container, then test the production environment before release.

Assume an older binary may be unable to open a newly migrated local store. Cloud records already uploaded under a new schema also cannot be made old-client-compatible by restoring one local file. Plan forward recovery, feature flags, export/backup where appropriate, and a minimum-supported-client policy. Read [CloudKit, rollback, and migration testing](references/testing-cloudkit-rollback.md).

## Verify with real stores

Maintain three mandatory test lanes:

1. Fresh-store creation directly at the newest schema.
2. On-disk upgrades from every supported released schema.
3. Sanitized copies of production-representative stores at realistic size.

Assert row counts, stable IDs, required values, relationships, uniqueness, ordering, and application-level invariants. Reopen the migrated store in a new container/process. Test low disk space and an injected migration failure where feasible. Never delete a failed user store as automatic recovery.

## OS 27 beta boundary

Use stable Xcode 26 APIs for the primary plan and compiled examples. If an OS 27-cycle beta introduces a migration API, label it beta, isolate it in a beta-only source path, compile it with that beta SDK, and preserve the stable SwiftData/Core Data path. Runtime `#available` cannot make symbols from an unavailable SDK compile.

## Resources

- [Requirements and planning framework](references/decision-framework.md)
- [CloudKit, rollback, and migration testing](references/testing-cloudkit-rollback.md)
- [SwiftData versioned-schema example](examples/SwiftDataMigration.swift)
- [Core Data migration configuration example](examples/CoreDataMigrationConfiguration.swift)
- [Positive and negative prompt scenarios](examples/prompts.md)
