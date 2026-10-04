---
name: obsidian-livesync
description: "Community implementation of self-hosted livesync. Reflect your vault changes to some other devices immediately. Please make sure to disable other synchronize solutions to avoid content corruption or duplication."
source: obsidian-livesync
---

# Self-hosted LiveSync

## Plugin metadata

- **id:** `obsidian-livesync`
- **source:** vault-native
- **plugin-type:** community
- **status:** enabled
- **class:** FULL
- **has-settings:** true

### Commands

- `obsidian-livesync:p2p-establish-connection` -- Self-hosted LiveSync: P2P Sync : Connect to the Signalling Server
- `obsidian-livesync:p2p-close-connection` -- Self-hosted LiveSync: P2P Sync : Disconnect from the Signalling Server
- `obsidian-livesync:livesync-switch-remote` -- Self-hosted LiveSync: Switch active connection
- `obsidian-livesync:livesync-replicate-with-specific` -- Self-hosted LiveSync: Sync with a saved connection
- `obsidian-livesync:livesync-review-compatibility-pause` -- Self-hosted LiveSync: Review why synchronisation is paused
- `obsidian-livesync:open-p2p-server-status` -- Self-hosted LiveSync: P2P Sync : Open P2P Status
- `obsidian-livesync:replicate-now-by-p2p-default-peer` -- Self-hosted LiveSync: Replicate P2P to default peer
- `obsidian-livesync:replicate-now-by-p2p` -- Self-hosted LiveSync: Replicate now by P2P
- `obsidian-livesync:p2p-sync-targets` -- Self-hosted LiveSync: P2P: Sync with targets
- `obsidian-livesync:livesync-reset-remote-size-threshold-and-check` -- Self-hosted LiveSync: Reset notification threshold and check the remote database usage
- `obsidian-livesync:livesync-replicate` -- Self-hosted LiveSync: Sync now
- `obsidian-livesync:livesync-dump` -- Self-hosted LiveSync: Copy database information for the active file
- `obsidian-livesync:livesync-toggle` -- Self-hosted LiveSync: Toggle LiveSync
- `obsidian-livesync:livesync-suspendall` -- Self-hosted LiveSync: Toggle All Sync.
- `obsidian-livesync:livesync-scan-files` -- Self-hosted LiveSync: Scan storage and database again
- `obsidian-livesync:livesync-runbatch` -- Self-hosted LiveSync: Apply pending changes now
- `obsidian-livesync:livesync-abortsync` -- Self-hosted LiveSync: Abort synchronization immediately
- `obsidian-livesync:livesync-export-config` -- Self-hosted LiveSync: Write setting markdown manually
- `obsidian-livesync:livesync-import-config` -- Self-hosted LiveSync: Parse setting file
- `obsidian-livesync:view-log` -- Self-hosted LiveSync: Show log
- `obsidian-livesync:dump-debug-info` -- Self-hosted LiveSync: Generate full report for opening the issue with debug info
- `obsidian-livesync:livesync-history` -- Self-hosted LiveSync: Show history
- `obsidian-livesync:livesync-filehistory` -- Self-hosted LiveSync: Pick a file to show history
- `obsidian-livesync:livesync-checkdoc-conflicted` -- Self-hosted LiveSync: Resolve if conflicted.
- `obsidian-livesync:livesync-conflictcheck` -- Self-hosted LiveSync: Pick a file to resolve conflict
- `obsidian-livesync:livesync-all-conflictcheck` -- Self-hosted LiveSync: Resolve all conflicted files
- `obsidian-livesync:livesync-global-history` -- Self-hosted LiveSync: Show vault history
- `obsidian-livesync:livesync-setting-qr` -- Self-hosted LiveSync: Show settings as a QR code
- `obsidian-livesync:livesync-copysetupuri` -- Self-hosted LiveSync: Copy settings as a new setup URI
- `obsidian-livesync:livesync-copysetupuri-short` -- Self-hosted LiveSync: Copy settings as a new setup URI (With customization sync)
- `obsidian-livesync:livesync-copysetupurifull` -- Self-hosted LiveSync: Copy settings as a new setup URI (Full)
- `obsidian-livesync:livesync-opensetupuri` -- Self-hosted LiveSync: Use the copied setup URI (Formerly Open setup URI)
- `obsidian-livesync:livesync-plugin-dialog-ex` -- Self-hosted LiveSync: Show customization sync dialog
- `obsidian-livesync:livesync-sync-internal` -- Self-hosted LiveSync: (re)initialise hidden files between storage and database
- `obsidian-livesync:livesync-scaninternal-storage` -- Self-hosted LiveSync: Scan hidden file changes on the storage
- `obsidian-livesync:livesync-scaninternal-database` -- Self-hosted LiveSync: Scan hidden file changes on the local database
- `obsidian-livesync:livesync-internal-scan-offline-changes` -- Self-hosted LiveSync: Scan and apply all offline hidden-file changes
- `obsidian-livesync:analyse-database` -- Self-hosted LiveSync: Analyse Database Usage (advanced)
- `obsidian-livesync:gc-v3` -- Self-hosted LiveSync: Garbage Collection V3 (advanced, beta)

# Self-hosted LiveSync

**Description:** Community implementation of self-hosted livesync. Reflect your vault changes to some other devices immediately. Please make sure to disable other synchronize solutions to avoid content corruption or duplication.
**Status:** Enabled
**Plugin ID:** obsidian-livesync

## Available Commands

Available command IDs (use execute_command for Obsidian-native commands):
- `obsidian-livesync:p2p-establish-connection` -- Self-hosted LiveSync: P2P Sync : Connect to the Signalling Server
- `obsidian-livesync:p2p-close-connection` -- Self-hosted LiveSync: P2P Sync : Disconnect from the Signalling Server
- `obsidian-livesync:livesync-switch-remote` -- Self-hosted LiveSync: Switch active connection
- `obsidian-livesync:livesync-replicate-with-specific` -- Self-hosted LiveSync: Sync with a saved connection
- `obsidian-livesync:livesync-review-compatibility-pause` -- Self-hosted LiveSync: Review why synchronisation is paused
- `obsidian-livesync:open-p2p-server-status` -- Self-hosted LiveSync: P2P Sync : Open P2P Status
- `obsidian-livesync:replicate-now-by-p2p-default-peer` -- Self-hosted LiveSync: Replicate P2P to default peer
- `obsidian-livesync:replicate-now-by-p2p` -- Self-hosted LiveSync: Replicate now by P2P
- `obsidian-livesync:p2p-sync-targets` -- Self-hosted LiveSync: P2P: Sync with targets
- `obsidian-livesync:livesync-reset-remote-size-threshold-and-check` -- Self-hosted LiveSync: Reset notification threshold and check the remote database usage
- `obsidian-livesync:livesync-replicate` -- Self-hosted LiveSync: Sync now
- `obsidian-livesync:livesync-dump` -- Self-hosted LiveSync: Copy database information for the active file
- `obsidian-livesync:livesync-toggle` -- Self-hosted LiveSync: Toggle LiveSync
- `obsidian-livesync:livesync-suspendall` -- Self-hosted LiveSync: Toggle All Sync.
- `obsidian-livesync:livesync-scan-files` -- Self-hosted LiveSync: Scan storage and database again
- `obsidian-livesync:livesync-runbatch` -- Self-hosted LiveSync: Apply pending changes now
- `obsidian-livesync:livesync-abortsync` -- Self-hosted LiveSync: Abort synchronization immediately
- `obsidian-livesync:livesync-export-config` -- Self-hosted LiveSync: Write setting markdown manually
- `obsidian-livesync:livesync-import-config` -- Self-hosted LiveSync: Parse setting file
- `obsidian-livesync:view-log` -- Self-hosted LiveSync: Show log
- `obsidian-livesync:dump-debug-info` -- Self-hosted LiveSync: Generate full report for opening the issue with debug info
- `obsidian-livesync:livesync-history` -- Self-hosted LiveSync: Show history
- `obsidian-livesync:livesync-filehistory` -- Self-hosted LiveSync: Pick a file to show history
- `obsidian-livesync:livesync-checkdoc-conflicted` -- Self-hosted LiveSync: Resolve if conflicted.
- `obsidian-livesync:livesync-conflictcheck` -- Self-hosted LiveSync: Pick a file to resolve conflict
- `obsidian-livesync:livesync-all-conflictcheck` -- Self-hosted LiveSync: Resolve all conflicted files
- `obsidian-livesync:livesync-global-history` -- Self-hosted LiveSync: Show vault history
- `obsidian-livesync:livesync-setting-qr` -- Self-hosted LiveSync: Show settings as a QR code
- `obsidian-livesync:livesync-copysetupuri` -- Self-hosted LiveSync: Copy settings as a new setup URI
- `obsidian-livesync:livesync-copysetupuri-short` -- Self-hosted LiveSync: Copy settings as a new setup URI (With customization sync)
- `obsidian-livesync:livesync-copysetupurifull` -- Self-hosted LiveSync: Copy settings as a new setup URI (Full)
- `obsidian-livesync:livesync-opensetupuri` -- Self-hosted LiveSync: Use the copied setup URI (Formerly Open setup URI)
- `obsidian-livesync:livesync-plugin-dialog-ex` -- Self-hosted LiveSync: Show customization sync dialog
- `obsidian-livesync:livesync-sync-internal` -- Self-hosted LiveSync: (re)initialise hidden files between storage and database
- `obsidian-livesync:livesync-scaninternal-storage` -- Self-hosted LiveSync: Scan hidden file changes on the storage
- `obsidian-livesync:livesync-scaninternal-database` -- Self-hosted LiveSync: Scan hidden file changes on the local database
- `obsidian-livesync:livesync-internal-scan-offline-changes` -- Self-hosted LiveSync: Scan and apply all offline hidden-file changes
- `obsidian-livesync:analyse-database` -- Self-hosted LiveSync: Analyse Database Usage (advanced)
- `obsidian-livesync:gc-v3` -- Self-hosted LiveSync: Garbage Collection V3 (advanced, beta)

## Configuration File

Settings path: `.obsidian/plugins/obsidian-livesync/data.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/plugins/obsidian-livesync/data.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/plugins/obsidian-livesync/data.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify data.json directly.

## Current Configuration

These are the plugin's current settings (sensitive values redacted):

```
useCustomRequestHandler: false
liveSync: false
syncOnSave: false
syncOnStart: false
savingDelay: 200
lessInformationInLog: false
gcDelay: 0
minimumChunkSize: 20
longLineThreshold: 250
showVerboseLog: false
suspendFileWatching: false
trashInsteadDelete: true
periodicReplication: false
periodicReplicationInterval: 60
syncOnFileOpen: false
encrypt: false
usePathObfuscation: false
doNotDeleteFolder: false
resolveConflictsByNewerFile: false
batchSave: false
batchSaveMinimumDelay: 5
batchSaveMaximumDelay: 60
usePluginSettings: false
showOwnPlugins: false
showStatusOnEditor: true
showStatusOnStatusbar: true
showOnlyIconsOnEditor: false
hideFileWarningNotice: false
usePluginSync: false
autoSweepPlugins: false
autoSweepPluginsPeriodic: false
notifyPluginOrSettingUpdated: false
checkIntegrityOnSave: false
batch_size: 25
batches_limit: 25
useHistory: true
disableRequestURI: true
skipOlderFilesOnSync: true
checkConflictOnlyOnOpen: false
showMergeDialogOnlyOnActive: false
syncInternalFiles: false
syncInternalFilesBeforeReplication: false
syncInternalFilesIgnorePatterns: \/node_modules\/, \/\.git\/, \/obsidian-livesync\/
syncInternalFilesInterval: 60
additionalSuffixOfDatabaseName: f97346b88ea75b65
ignoreVersionCheck: false
lastReadUpdates: 0
deleteMetadataOfDeletedFiles: false
customChunkSize: 0
readChunksOnline: true
watchInternalFileChanges: true
automaticallyDeleteMetadataOfDeletedFiles: 0
disableMarkdownAutoMerge: false
writeDocumentsIfConflicted: false
useDynamicIterationCount: false
syncAfterMerge: false
permitEmptyPassphrase: false
useIndexedDBAdapter: false
useTimeouts: false
writeLogToTheFile: false
doNotPaceReplication: false
hashCacheMaxCount: 300
hashCacheMaxAmount: 50
concurrencyOfReadChunksOnline: 40
minimumIntervalOfReadChunksOnline: 50
hashAlg: xxhash64
suspendParseReplicationResult: false
doNotSuspendOnFetching: false
useIgnoreFiles: false
ignoreFiles: .gitignore
syncOnEditorSave: false
keepReplicationActiveInBackground: false
allowSleepDuringSynchronisation: false
allowSleepDuringSynchronisationOnDesktop: true
syncMaxSizeInMB: 50
notifyAllSettingSyncFile: false
isConfigured: false
settingVersion: 10
enableCompression: false
region: auto
useEden: false
maxChunksInEden: 10
maxTotalLengthInEden: 1024
maxAgeInEden: 10
disableCheckingConfigMismatch: false
displayLanguage: def
enableChunkSplitterV2: false
disableWorkerForGeneratingChunks: false
processSmallFilesInUIThread: false
notifyThresholdOfRemoteStorageSize: -1
usePluginSyncV2: true
usePluginEtc: false
handleFilenameCaseSensitive: false
doNotUseFixedRevisionForChunks: true
showLongerLogInsideEditor: false
sendChunksBulk: false
sendChunksBulkMaxSize: 1
useSegmenter: false
useAdvancedMode: false
usePowerUserMode: false
useEdgeCaseMode: false
enableDebugTools: false
suppressNotifyHiddenFilesChange: false
syncMinimumInterval: 2000
P2P_Enabled: false
P2P_AutoAccepting: 0
P2P_AppID: self-hosted-livesync
P2P_relays: wss://exp-relay.vrtmrz.net/
P2P_AutoBroadcast: false
P2P_AutoStart: false
P2P_IsHeadless: false
P2P_maxWirePayloadBytes: 15360
P2P_connectionPath: automatic
P2P_useDiagRTC: false
useJWT: false
jwtExpDuration: 5
useRequestAPI: false
chunkSplitterVersion: v3-rabin-karp
E2EEAlgorithm: v2
processSizeMismatchedFiles: false
forcePathStyle: true
useOnlyLocalChunk: false
maxMTimeForReflectEvents: 0
```
(5 sensitive field(s) redacted)

For full settings, read: `.obsidian/plugins/obsidian-livesync/data.json`

## Documentation

For detailed plugin documentation (commands, options, dependencies):
read_file(".vault-operator/data/skills/obsidian-livesync.readme.md")

## Usage

When the user asks for functionality related to Self-hosted LiveSync:
1. Read the plugin documentation (.readme.md) to understand capabilities and dependencies
2. Read the config file (.obsidian/plugins/obsidian-livesync/data.json). If it does not exist, that is normal -- create it with the required settings
3. Configure the plugin by writing data.json with the values needed for the task
4. Execute the task using the appropriate tool:
   - For Obsidian-native commands (including file export): use execute_command
   - For CLI-based conversion needing Pandoc/LaTeX: use execute_recipe
   - For data queries: use call_plugin_api
5. If a command opens a UI dialog, tell the user what to click.

CRITICAL RULES:
- Prefer native Obsidian commands over external tools when both can accomplish the task.
- NEVER create fake output files. If the user asks for a PDF/DOCX/image export, use execute_recipe -- do NOT write content to a .pdf file yourself.
- If a dependency is missing (e.g. Pandoc), tell the user what to install.
IMPORTANT: After reading this file, ALWAYS take action or respond. Never end silently.
