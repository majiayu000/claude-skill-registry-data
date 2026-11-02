---
name: background-execution
description: Use when scheduling deferred work, finishing work after the app backgrounds, transferring files in the background, waking the app via push, or debugging background tasks that never run. Writes and reviews Swift code for background execution on Apple platforms - BGTaskScheduler (app refresh…
license: MIT
metadata:
  author: Anton Novoselov
  version: '1.0'
---

Write and review Swift code that runs work while the app is backgrounded or suspended, choosing the right API for the job and respecting the system's constraints so the work actually runs and the app is not terminated.

Review process:

1. Establish the background execution model (lifecycle, budgets, force-quit, the five principles) using `references/fundamentals.md`.
1. Confirm the chosen API matches the work using the decision tree below; reroute if it does not.
1. Validate `BGTaskScheduler` usage (registration timing, Info.plist, expiration, `setTaskCompleted`) using `references/bg-task-scheduler.md`.
1. Validate task assertions (`beginBackgroundTask`/`endBackgroundTask`, `performExpiringActivity`) using `references/task-assertions.md`.
1. Validate background `URLSession` config and the relaunch flow using `references/background-url-session.md`.
1. Validate silent/VoIP push payloads, headers, and handlers using `references/background-push.md`.
1. Validate `UIBackgroundModes` declarations and location specifics using `references/background-modes.md`.
1. Validate background audio (session category, recording while locked, interruptions, route changes, mic permission) using `references/background-audio.md`.
1. Validate SwiftUI `ScenePhase` / `.backgroundTask` usage using `references/swiftui-background-tasks.md`.
1. Validate macOS schedulers (`NSBackgroundActivityScheduler`, `beginActivity`, `SMAppService`) using `references/macos-background.md`.
1. Check testing/debugging and constraint handling using `references/testing-and-debugging.md`.
1. Catch common mistakes using `references/anti-patterns.md`.

If doing partial work, load only the relevant reference files.


## Task-based routing

Match the user's goal to the read order. Load only what you need.

### "Refresh my app's content in the background"
1. `references/bg-task-scheduler.md` - `BGAppRefreshTask`, register/submit/expiration
2. `references/testing-and-debugging.md` - simulate the launch, handle `backgroundRefreshStatus`

### "Run long maintenance / ML / cleanup in the background"
1. `references/bg-task-scheduler.md` - `BGProcessingTask`, power/network requirements
2. `references/testing-and-debugging.md` - simulate launch and expiration

### "Let a user-started export keep running after they leave (iOS 26)"
1. `references/bg-task-scheduler.md` - `BGContinuedProcessingTask`, progress, submission strategy, GPU
2. `references/fundamentals.md` - the consent / user-initiated principle

### "Finish an in-flight upload / save when the app backgrounds"
1. `references/task-assertions.md` - `beginBackgroundTask`/`endBackgroundTask`, `performExpiringActivity`

### "Download or upload a large file that survives suspension"
1. `references/background-url-session.md` - background config, delegate, the relaunch flow
2. `references/testing-and-debugging.md` - force-quit and constraint caveats

### "Wake my app from the server"
1. `references/background-push.md` - silent push payload/headers/handler, or PushKit for calls
2. `references/background-modes.md` - the `remote-notification` mode

### "Keep playing audio in the background"
1. `references/background-audio.md` - the `audio` mode + active session, category/mode/options, interruptions, route changes

### "Record / dictate / transcribe with the screen locked"
1. `references/background-audio.md` - `.playAndRecord`, recording while locked, mic permission, AVAudioEngine taps, the production gotchas

### "Track location in the background"
1. `references/background-modes.md` - the `location` mode, significant-change and region monitoring

### "Do this the SwiftUI way"
1. `references/swiftui-background-tasks.md` - `ScenePhase`, `.backgroundTask(.appRefresh/.urlSession)`
2. `references/bg-task-scheduler.md` - you still schedule with `BGTaskScheduler`

### "Background work on macOS"
1. `references/macos-background.md` - `NSBackgroundActivityScheduler`, `beginActivity`, `SMAppService`

### "My background task never runs / how do I test it"
1. `references/testing-and-debugging.md` - lldb simulate commands, the states that gate execution
2. `references/anti-patterns.md` - the usual causes

### "I'm hitting bugs or App Review issues"
1. `references/anti-patterns.md` - catches with before/after fixes


## Decision tree

### Which background API should I use?

```
Does the work require user consent or input mid-flight?
  -> Background runtime is wrong. Bring it to the foreground.

Is work already running and you just need to finish it as the app backgrounds?
  -> beginBackgroundTask / endBackgroundTask (apps)
  -> ProcessInfo.performExpiringActivity (app extensions, watchOS)

Is it a user-initiated long task that should continue with visible progress? (iOS/iPadOS 26)
  -> BGContinuedProcessingTask

Is it a large/long file download or upload that must survive suspension/termination?
  -> background URLSession

Does the server need to tell the app new content exists?
  -> background (silent) push  (apns-push-type: background, content-available: 1)

Is it an incoming call invitation?
  -> PushKit + CallKit (report the call on every push)

Is it periodic content refresh before the user opens the app?
  -> BGAppRefreshTask

Is it long, deferrable maintenance / ML / cleanup?
  -> BGProcessingTask (optionally requiresExternalPower / requiresNetworkConnectivity)

Does the app need to keep playing audio or recording the mic (incl. while locked)?
  -> audio UIBackgroundMode + active AVAudioSession (.playback or .playAndRecord)  [background-audio.md]

Does the app need to keep running for location / BLE / VoIP?
  -> declare the matching UIBackgroundModes capability  [background-modes.md]

macOS, deferrable repeating maintenance?
  -> NSBackgroundActivityScheduler

macOS, keep critical non-UI work from being napped?
  -> ProcessInfo.beginActivity / performActivity
```

### Which BGTask type?

```
Short content refresh, system picks the time around app usage?
  -> BGAppRefreshTask          (UIBackgroundModes: fetch)

Long maintenance, ideally on charger + network?
  -> BGProcessingTask          (UIBackgroundModes: processing; requiresExternalPower / requiresNetworkConnectivity)

User-tapped long work with progress UI, continues after backgrounding? (iOS 26)
  -> BGContinuedProcessingTask (title/subtitle, progress, submission strategy, optional .gpu)

Long processing of health-research-study data? (iOS 17)
  -> BGHealthResearchTask
```


## Core Instructions

- **Never** treat background execution as guaranteed. It is opportunistic and discretionary; design every feature with a foreground reconciliation path and never put correctness-critical logic solely in a background task.
- **Never** register a `BGTaskScheduler` handler lazily, in view code, or after launch finishes. Register all handlers in `App.init()` / `application(_:didFinishLaunchingWithOptions:)`, because the system may launch the app directly into the background. (`BGContinuedProcessingTask` is the one exception - it registers dynamically on user intent.)
- **Never** register the same task identifier twice - it crashes the app.
- **Never** omit the expiration handler on a `BGTask`; without one the system silently marks the task complete-and-unsuccessful. Set it, have it cancel work fast, and call `setTaskCompleted(success:)` exactly once.
- **Never** forget to reschedule. `BGTaskScheduler` requests are one-shot; submit the next request as the first line of the launch handler.
- Put `requiresExternalPower` / `requiresNetworkConnectivity` only on `BGProcessingTaskRequest`, never on app-refresh. Treat `earliestBeginDate` as a floor, not a schedule.
- **Never** leave a `beginBackgroundTask` unbalanced. Call `endBackgroundTask` on both the success path and inside the expiration handler, idempotently (guard on `.invalid`); an unbalanced assertion kills the app. Call `beginBackgroundTask` before starting the work, not at the end of the background-transition delegate.
- **Never** trust `backgroundTimeRemaining` as a real budget - it is `DBL_MAX` in the foreground and advisory in the background. Plan for ~30 s and rely on the expiration handler.
- Use `beginBackgroundTask` (apps) or `performExpiringActivity` (extensions, watchOS) only to **finish work already running**, never to start fresh long work or schedule future work.
- **Never** use completion-handler convenience methods or `dataTask` on a background `URLSession`; background sessions require a delegate. Create one session per identifier, store it, and recreate it at relaunch with the identical identifier and config.
- Implement the full relaunch flow for background `URLSession`: store the handler from `handleEventsForBackgroundURLSession`, recreate the session, and call the stored handler from `urlSessionDidFinishEvents(forBackgroundURLSession:)` on the main thread. Move the file from `didFinishDownloadingTo`'s `location` synchronously inside the callback.
- For background uploads, use file-backed `uploadTask(with:fromFile:)` - data and stream uploads fail after the app exits.
- **Never** send a silent push without `apns-push-type: background` (and `apns-priority: 5`), and keep the `aps` dictionary to `content-available` only. Call the fetch completion handler within ~30 s. Treat silent push as throttled and coalesced, not reliable.
- On iOS 13+, report an incoming call to CallKit on **every** VoIP push, or the system terminates the app and revokes VoIP-push privileges. Never use VoIP pushes for non-call data.
- **Never** set `allowsBackgroundLocationUpdates = true` without the `location` background mode - it is a fatal error. Prefer significant-change / region monitoring over the continuous `location` mode.
- Background audio needs **both** the `audio` mode and an active `AVAudioSession` with a background-capable category (`.playback` for playback, `.playAndRecord` / `.record` for recording-while-locked); the mode alone does nothing. Activate the session when audio begins (not at launch) and deactivate with `.notifyOthersOnDeactivation`. Always handle `interruptionNotification` (check `.shouldResume` before resuming) and `routeChangeNotification` (pause on `.oldDeviceUnavailable`).
- For mic capture, require permission with `AVAudioApplication.requestRecordPermission()` (iOS 17+) and declare `NSMicrophoneUsageDescription` - without the key the app crashes, and without permission capture returns silent zeroed samples, not an error. Install `AVAudioEngine` taps off the main actor (the closure runs on a realtime thread) and match `AVAudioFile` settings to the input node's format.
- Declare `UIBackgroundModes` sparingly; App Review rejects unjustified modes. Prefer the lighter alternative.
- Account for the user: a force-quit suppresses `BGTaskScheduler`, silent push, and background `URLSession` relaunch until the next manual launch. Read `backgroundRefreshStatus` (degrade on `.denied`, stay silent on `.restricted`) and back off under Low Power Mode and elevated thermal state.
- Do background-relevant setup (task registration, session recreation, dependency wiring) on a path that runs on every launch, not in `.onAppear` / `.task` - a background launch may never build the UI.
- With scenes enabled, use `sceneDidEnterBackground(_:)` (not the deprecated `applicationDidEnterBackground(_:)`); it has ~5 s to return.
- On macOS use `NSBackgroundActivityScheduler` for deferrable maintenance and `ProcessInfo.beginActivity`/`endActivity` (balanced, or `performActivity`) to control App Nap; `performExpiringActivity` does not exist on macOS.
- Test background tasks on a real device with the lldb `_simulateLaunchForTaskWithIdentifier:` / `_simulateExpirationForTaskWithIdentifier:` commands - never ship a reference to them. Always test the expiration path.


## Output Format

If the user asks for a review, organize findings by file. For each issue:

1. State the file and relevant line(s).
2. Name the anti-pattern being replaced.
3. Show a brief before/after code fix.

Skip files with no issues. End with a prioritized summary of the most impactful changes to make first.

If the user asks you to write or fix background-execution code, make the changes directly instead of returning a findings report.

Example output:

### SyncManager.swift

**Line 22: `BGTaskScheduler` handler registered in `.onAppear` - never runs on a background launch.**

```swift
// Before
.onAppear {
    BGTaskScheduler.shared.register(forTaskWithIdentifier: id, using: nil) { ... }
}

// After - register in App.init() / didFinishLaunching
init() {
    BGTaskScheduler.shared.register(forTaskWithIdentifier: id, using: nil) { task in
        self.handleRefresh(task: task as! BGAppRefreshTask)
    }
}
```

**Line 48: missing expiration handler and `setTaskCompleted` - the app is killed at expiry.**

```swift
// Before
func handleRefresh(task: BGAppRefreshTask) { refresh() }

// After
func handleRefresh(task: BGAppRefreshTask) {
    scheduleNext()
    let op = RefreshOperation()
    task.expirationHandler = { op.cancel() }
    op.completionBlock = { task.setTaskCompleted(success: !op.isCancelled) }
    queue.addOperation(op)
}
```

### Summary

1. **Registration timing (high):** move the handler to `App.init()` or it never fires on background launch.
2. **Completion contract (high):** add the expiration handler and call `setTaskCompleted` exactly once.

End of example.


## References

- `references/fundamentals.md` - the execution model: foreground/background/suspended, system budgets, force-quit, user toggles, the five principles, the lifecycle and scene states, the "which API" map.
- `references/bg-task-scheduler.md` - `BackgroundTasks`: `BGAppRefreshTask`, `BGProcessingTask`, `BGContinuedProcessingTask` (iOS 26), `BGHealthResearchTask`, registration, Info.plist keys, submit, expiration, errors.
- `references/task-assertions.md` - `beginBackgroundTask`/`endBackgroundTask`, `backgroundTimeRemaining`, `ProcessInfo.performExpiringActivity`, assertions vs `BGTaskScheduler`.
- `references/background-url-session.md` - background `URLSession` config, mandatory delegate, the relaunch / `handleEventsForBackgroundURLSession` flow, knobs, resume data.
- `references/background-push.md` - silent/background push (payload, headers, handler, throttling), PushKit/VoIP + the CallKit requirement.
- `references/background-modes.md` - the `UIBackgroundModes` matrix, background location, BLE/accessory/PTT, deprecated background fetch.
- `references/background-audio.md` - background playback and recording: `AVAudioSession` categories/modes/options, recording while locked, mic permission, interruptions, route changes, `AVAudioEngine` taps and production gotchas.
- `references/swiftui-background-tasks.md` - `ScenePhase`, the `.backgroundTask` scene modifier, async cancellation, scheduling vs handling.
- `references/macos-background.md` - `NSBackgroundActivityScheduler`, `ProcessInfo.beginActivity`/App Nap, `SMAppService`, cross-platform map.
- `references/testing-and-debugging.md` - lldb simulate-launch/expiration, `backgroundRefreshStatus`, Low Power Mode, thermal state, what gates execution.
- `references/anti-patterns.md` - common mistakes LLMs make when generating background-execution code.
