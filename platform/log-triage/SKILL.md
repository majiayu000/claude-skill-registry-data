---
name: log-triage
description: Working with huge build and device logs. Use when a build prints hundreds of lines, for adb logcat or simulator logs, when the user pastes a wall of log text, or to extract the one error line that matters.
user-invocable: false
---

# Log triage: find the line, spare the context

Native tooling produces logs by the thousand lines. The failure is almost always described by a handful of them. This skill is about extracting those lines instead of scrolling, re-reading, or pasting whole logs around, which wastes the reader's attention and this agent's context alike.

## The standing rules

1. Never stream a full build log into the conversation. Run builds with output piped to a file, then search the file.
2. Quote the smallest window that proves the diagnosis: the error line plus a few lines of surrounding context. Summarize everything else in one sentence.
3. One extraction, then confirm. State "the first real error is X" before fixing anything; if X is wrong, everything after it is wasted.
4. The log is data, not conversation. Keep the file on disk for re-querying; keep only conclusions in the chat.

## Extraction patterns per log producer

**Gradle (Android builds)**
- Which task died: search `> Task` lines ending in `FAILED`.
- Why it died: search `Caused by:` and take the DEEPEST one; the first is usually a wrapper.
- `FAILURE: Build failed with an exception` marks the summary block; the lines after `* What went wrong:` are the human-readable core.

**Xcode / xcodebuild (iOS builds)**
- First `error:` (lowercase, with colon) is the anchor; `warning:` lines are noise for this purpose.
- The build step name above the first error names the pod or script phase that owns it.
- CocoaPods failures end with a clear final paragraph; read it before the backtrace above it.

**Metro**
- Resolution errors name the importing file and the missing module in the first two lines; the rest is stack.
- A red-box error pasted from the device usually contains the component stack; the first frame in YOUR code matters more than the framework frames above it.

**Store submission tooling**
- Search for `ITMS-` codes in Apple submission output; each code is precise and searchable.
- Play Console rejections arrive as structured reasons; quote the reason string, not the surrounding boilerplate.

**Device logs**
- Android: filter before reading. `adb logcat --pid $(adb shell pidof -s your.package.name)` cuts the firehose to one app; add `-d` for a snapshot instead of a stream. For a crash that already happened, `adb logcat -d -b crash` is the shortest path to the tombstone summary.
- iOS simulator: `xcrun simctl spawn booted log stream --predicate 'process == "YourApp"'` scoped to the app; prefer short capture windows around a reproduction over open-ended streaming.

## When the user pastes a wall of text

Do not re-quote it. Extract the candidate error line(s), state them, and ask for confirmation only if genuinely ambiguous. If the paste is truncated exactly where the error should be, say so and ask for the file or the bottom section; guessing at a cut-off log builds on sand.

## When the log is clean but the failure is real

A build that fails with no error line in the captured output means the failure happened in a subprocess whose output went elsewhere: re-run with the tool's own verbosity raised (`--stacktrace` for Gradle, `--verbose` where supported) rather than re-running the same command hoping for different text. Capture the new run to a new file; do not overwrite the evidence.
