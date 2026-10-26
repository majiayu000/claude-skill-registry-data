---
name: duo-intelligence
description: "Adds Foundation Models to an iPhone Duo app: the on-device model (SystemLanguageModel) and the Private Cloud Compute server model (PrivateCloudComputeLanguageModel) behind one LanguageModelSession API, an AI side pane beside the content when the phone is open or in book pose (split ArrangementView) and a one-line summary when it is closed or in tabletop, streaming (streamResponse with @Generable partial snapshots) into a pane that keeps going through fold and unfold, availability checks and non-AI fallbacks, quota and error handling (LanguageModelError), tool calling, image prompts (Attachment), reasoning levels (ContextOptions) and privacy. Use when someone adds summaries, an assistant, chat, tagging or image understanding to an app that runs on iPhone Duo, or when an AI feature restarts on a fold, sits in the fold or doesn't fit the outer display."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# duo-intelligence

The Foundation Models framework gives an app Apple's on-device language model and, from iOS 27, the larger Private Cloud Compute model, through the same Swift API ([Foundation Models](https://developer.apple.com/documentation/foundationmodels)). On iPhone Duo the question is where the result goes and what happens when the phone folds mid-answer. This skill answers both.

Load neighbours when the task needs them: `duo-continuity` (state that survives a fold), `duo-layout` (size classes, the fold, `ArrangementView`), `duo-postures` (book and tabletop layouts), `duo-app-intents` (let Siri and Shortcuts run the same feature).

Labels: *measured* means we ran it on the iPhone Duo simulator (iOS 27.1) on 20 October 2026; see [references/evidence.md](references/evidence.md). *Unverified* means we could not confirm it. Everything else comes from Apple's pages, linked inline. Full source list: [reference/sources.md](https://github.com/Kimeur/duology/blob/main/reference/sources.md).

## What Apple says, and what it doesn't

Apple's iPhone Duo pages and the six Duo Tech Talks say nothing about Foundation Models (we searched the transcripts, the HIG page and the developer overview). The Duo advice below applies Apple's general Duo rules to AI features: keep the same features on both displays, let the open phone add one level of detail, keep controls out of the fold ([HIG: Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo)). An AI pane is a supporting pane, like the Podcasts transcript Apple puts beside Now Playing with a split `ArrangementView` ([talk 111463](https://developer.apple.com/videos/play/tech-talks/111463/?time=560)). The model facts come from the Foundation Models docs and WWDC26 sessions [241](https://developer.apple.com/videos/play/wwdc2026/241/) and [319](https://developer.apple.com/videos/play/wwdc2026/319/).

| | On device: `SystemLanguageModel` | Server: `PrivateCloudComputeLanguageModel` |
|---|---|---|
| Since | iOS 26.0 | iOS 27.0, plus a managed entitlement |
| Network | Not needed | Needed |
| Context | 4,096 tokens | 32K tokens |
| Limits | None | A daily limit per person; iCloud+ raises it |
| Reasoning | No | `light`, `moderate`, `deep` |
| Images | Yes, iOS 27 (`.vision` capability) | Yes |

Sources: [Adding server-side intelligence with Private Cloud Compute](https://developer.apple.com/documentation/foundationmodels/adding-server-side-intelligence-with-private-cloud-compute), [Managing the context window](https://developer.apple.com/documentation/foundationmodels/managing-the-context-window), [Analyzing images with multimodal prompting](https://developer.apple.com/documentation/foundationmodels/analyzing-images-with-multimodal-prompting). Both models conform to the iOS 27 `LanguageModel` protocol, so `LanguageModelSession(model:instructions:)` takes either one and the rest of your code stays the same.

## Rules

1. **Start on device.** Use Private Cloud Compute only when evaluation (Apple's Evaluations framework, new in Xcode 27) shows the on-device model can't do the job, the app has the entitlement, and the person knows the text leaves the phone ([PCC guide](https://developer.apple.com/documentation/foundationmodels/adding-server-side-intelligence-with-private-cloud-compute), [HIG: Generative AI](https://developer.apple.com/design/human-interface-guidelines/generative-ai)).
2. **Check availability, then still expect failure.** *Measured:* the simulator reported both models `.available`, yet every on-device request failed. Every request needs a non-AI fallback.
3. **One feature, two sizes.** Open and wide: the result in a pane beside the content. Closed, or any window that can't fit the pane beside: one line, with a way to the full pane. Same feature, same data.
4. **Own the request in a model, not a view.** One `AssistantModel` per window, created in the window root. A fold resizes the window; the stream must not notice ([duo-continuity](https://github.com/Kimeur/duology/blob/main/plugins/duology/skills/duo-continuity/SKILL.md)).
5. **Ask for structure.** A `@Generable` type with a short headline first feeds the closed phone early and the open pane fully, from one request.
6. **Let the arrangement keep the pane off the fold.** A split `ArrangementView` puts the note and the pane one on each side. Text in a scroll view may cross the fold; Stop, Retry and text fields may not.
7. **Say where AI is used and keep people in control.** Label the pane, say what the model is doing, and let people dismiss or retry the result ([HIG: Generative AI](https://developer.apple.com/design/human-interface-guidelines/generative-ai)). Add Stop too: a request can hang (*measured*).
8. **Gate the APIs.** `SystemLanguageModel` and sessions are iOS 26.0. `PrivateCloudComputeLanguageModel`, `LanguageModel`, `Attachment`, `ContextOptions` and `LanguageModelError` are iOS 27.0. `ArrangementView` is iOS 27.1. iPhone Duo ships with iOS 27.1, so `#available` only matters for other iPhones.

## 1. Pick the model

```swift
import FoundationModels

/// Picks the model for one request. Start on device; move to Private Cloud Compute
/// only when the task needs it, the app has the entitlement and the person agreed.
@available(iOS 27.0, *)
enum AssistantModels {
    static func choose(needsLargeContext: Bool, cloudAllowed: Bool) -> (any LanguageModel)? {
        if needsLargeContext && cloudAllowed {
            let cloud = PrivateCloudComputeLanguageModel()
            if cloud.isAvailable && !cloud.quotaUsage.isLimitReached { return cloud }
        }
        let onDevice = SystemLanguageModel.default
        return onDevice.isAvailable ? onDevice : nil   // nil: show the non-AI fallback
    }

    /// Words for the fallback when the on-device model can't run.
    static var unavailableReason: String? {
        switch SystemLanguageModel.default.availability {
        case .available: nil
        case .unavailable(.deviceNotEligible): "This iPhone can't run Apple Intelligence."
        case .unavailable(.appleIntelligenceNotEnabled): "Turn on Apple Intelligence in Settings to get summaries."
        case .unavailable(.modelNotReady): "Summaries will work once the model finishes downloading."
        case .unavailable: "Summaries aren't available right now."
        }
    }
}
```

- `SystemLanguageModel` is `Observable` in the SDK, so a view that reads `availability` can follow it as the model downloads (unverified on a device).
- Private Cloud Compute needs the `com.apple.developer.private-cloud-compute` entitlement, which Apple grants to eligible apps on request ([entitlement](https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.developer.private-cloud-compute), [Accessing Private Cloud Compute](https://developer.apple.com/private-cloud-compute/)). *Measured:* without it, the simulator still reported `.available`, and a request never returned in 9 minutes. Keep Stop on screen for every request.
- Network failure on Private Cloud Compute: Apple says to retry on device. Quota: show a quiet, persistent note, not an alert. Code for both: [references/models-and-availability.md](references/models-and-availability.md).

## 2. Stream into a model the window owns

```swift
import FoundationModels
import Observation

@available(iOS 26.0, *)
@Generable
struct NoteDigest {
    @Guide(description: "One line of at most eight words, shown on the closed phone")
    var headline: String
    @Guide(description: "The key points, shown in the side pane", .count(3))
    var points: [String]
}

/// One per window, created in the window's root view. The stream lives here,
/// not in a view, so closing or opening the phone never restarts it.
@available(iOS 27.0, *)
@MainActor @Observable
final class AssistantModel {
    enum Phase: Equatable { case idle, working, done, failed(String) }

    private(set) var digest: NoteDigest.PartiallyGenerated?
    private(set) var phase = Phase.idle
    private var task: Task<Void, Never>?
    @ObservationIgnored private var lastRequest: (note: String, model: any LanguageModel)?

    func summarize(_ note: String, with model: any LanguageModel) {
        task?.cancel()                       // one summary at a time; a new one replaces the old
        lastRequest = (note, model)
        digest = nil
        phase = .working
        task = Task {
            let session = LanguageModelSession(model: model, instructions: "Summarize the note for a busy reader.")
            do {
                for try await snapshot in session.streamResponse(to: note, generating: NoteDigest.self) {
                    if Task.isCancelled { return }   // stop() or a newer request owns the state now
                    digest = snapshot.content        // partial: fields fill in as they arrive
                }
                if !Task.isCancelled { phase = .done }
            } catch {
                // Keep the note usable without AI. A cancelled task must not overwrite a newer one.
                if !Task.isCancelled { phase = .failed(error.localizedDescription) }
            }
        }
    }

    func retry() {
        if let lastRequest { summarize(lastRequest.note, with: lastRequest.model) }
    }

    func stop() {
        task?.cancel()
        task = nil
        if phase == .working { phase = .idle }
    }
}
```

- The model generates `@Generable` properties in the order you declare them ([guided generation](https://developer.apple.com/documentation/foundationmodels/generating-swift-data-structures-with-guided-generation)). Put the closed-phone headline first: it shows before the points are done.
- A session handles one request at a time; a second call while one runs is an error ([Generating content](https://developer.apple.com/documentation/foundationmodels/generating-content-and-performing-tasks-with-foundation-models)). Cancel the old task or check `isResponding`.
- *Measured* (stand-in stream, because the simulator's model failed): a task held by a window-owned model kept appending through close, open, book and tabletop. The note view kept its identity and the selection survived. The stream fell up to 1.4 s behind its pace around a fold, then went on as before ([evidence](references/evidence.md)).
- Never start a request in `onAppear` or `.task` below a layout switch. A fold can run it again ([duo-continuity](https://github.com/Kimeur/duology/blob/main/plugins/duology/skills/duo-continuity/SKILL.md)).

## 3. Pane when open, one line when closed

```swift
import SwiftUI

// requires: Note, NoteBody (your types); AssistantPane, AssistantSummaryBar (references/assistant-pane.md)

/// Wide (open, book): the note leading, the assistant pane trailing, one on each side of the fold.
/// Otherwise (closed, tabletop, a narrow window): the note with a one-line digest at the bottom;
/// Details shows the same pane in a sheet.
@available(iOS 27.1, *)
struct NoteScreen: View {
    let note: Note
    let assistant: AssistantModel                 // owned by the window root
    @Environment(\.horizontalSizeClass) private var widthClass
    @State private var paneIsBeside = false
    @State private var showsPaneSheet = false

    var body: some View {
        ArrangementView {
            NoteBody(note: note)                  // primary: shown in every pose
        } secondary: {
            AssistantPane(model: assistant)       // shown only when it fits beside
        }
        .arrangementViewStyle(.split.axes(.horizontal))   // beside, never below
        .safeAreaInset(edge: .bottom) {
            if !paneIsBeside {
                AssistantSummaryBar(model: assistant) { showsPaneSheet = true }
            }
        }
        .onGeometryChange(for: CGSize.self) { $0.size } action: { size in
            // The split rule duo-patterns measured: side by side needs regular width and a wide view.
            paneIsBeside = widthClass == .regular && size.width > size.height
        }
        .sheet(isPresented: $showsPaneSheet) { AssistantPane(model: assistant) }
        .onChange(of: paneIsBeside) { _, beside in
            if beside { showsPaneSheet = false }  // the pane is on screen now
        }
    }
}
```

- Put it inside the window's `NavigationStack`, never inside a `List`, `ScrollView` or `NavigationSplitView` ([HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Arrangement-views)).
- No API says "the secondary is hidden", so `paneIsBeside` mirrors the split rule (`duo-patterns`, supporting pane). Measure it after the inset, so the bar's height can't flip the result.
- `AssistantPane`, `AssistantSummaryBar`, the window root and a UIKit version: [references/assistant-pane.md](references/assistant-pane.md).

What each pose gets (layout by size class and shape, never by pose; see `duo-postures`):

| Phone | Window | The AI feature |
|---|---|---|
| Closed, portrait or sideways | 466 × 678 or 678 × 466 pt, compact width | The note, and one line at the bottom: the headline, or what the model is doing. Details opens the full pane in a sheet. |
| Open, flat, held wide | 951 × 669 pt | Note leading, pane trailing, half each. |
| Book (partly folded, held wide) | 951 × 669 pt | The same, one on each side of the fold. The pane sits in the trailing region, where controls stay once the phone closes (`duo-postures`). |
| Tabletop (partly folded, held tall) | 669 × 951 pt | The note, with the one-line bar in the bottom region, near the hands. Details opens the sheet. |
| Split View on the inner display | Half the display | Whatever its width class and shape allow; *unverified*. |

Window sizes come from [device facts](https://github.com/Kimeur/duology/blob/main/reference/device-facts.md#displays). What our probe showed in each pose: [references/evidence.md](references/evidence.md#the-pane-in-each-pose).

Apple lets the open phone add one level of hierarchy, as Mail adds the message beside the list ([HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo#Best-practices)). The pane is that level. The closed phone keeps the feature; it only shows less of it.

## 4. Errors and fallbacks

- Catch `LanguageModelError` (iOS 27) for guardrail violations, refusals, context overflow, rate limits and time-outs. iOS 26's `LanguageModelSession.GenerationError` is deprecated in iOS 27. Its missing-assets case moved to `SystemLanguageModel.Error.assetsUnavailable`; treat that like `.modelNotReady`.
- *Measured:* the simulator's failure arrived as a plain `NSError` (domain `FoundationModels.LanguageModelError`, code -1), so typed `catch` clauses missed it. Always end with a plain `catch` that shows the fallback.
- A refusal or guardrail error on text the person typed: say the feature can't handle that input and let them try again ([Improving the safety of generative model output](https://developer.apple.com/documentation/foundationmodels/improving-the-safety-of-generative-model-output)).
- Context overflow: trim the transcript, or split the text into chunks with one session each ([Managing the context window](https://developer.apple.com/documentation/foundationmodels/managing-the-context-window)).
- Code: [references/models-and-availability.md](references/models-and-availability.md#errors-and-fallbacks).

## 5. Privacy

- On-device requests stay on the phone. Private Cloud Compute sends the prompt to Apple's servers; Apple says it stores nothing and lets researchers check that ([WWDC26 session 319](https://developer.apple.com/videos/play/wwdc2026/319/)). Still tell people before their text leaves the phone, and let them say no ([HIG: Generative AI](https://developer.apple.com/design/human-interface-guidelines/generative-ai)).
- Never put text from the person or a web page in `instructions`. The model trusts instructions more than prompts, so that opens the door to prompt injection ([safety guide](https://developer.apple.com/documentation/foundationmodels/improving-the-safety-of-generative-model-output)).
- A third-party model behind the `LanguageModel` protocol: fetch its access token securely (Apple suggests OAuth) and keep it in the Keychain ([WWDC26 session 241](https://developer.apple.com/videos/play/wwdc2026/241/)). Its privacy terms are not Apple's; say so.

## 6. Tools, images and reasoning

- A `Tool` lets the model ask your app for data. Keep tools small and read-only unless the person confirms an action.
- `Attachment(cgImage)` in a prompt sends an image (iOS 27). Check `capabilities.contains(.vision)` first; the on-device model reported it (*measured*).
- `ContextOptions(reasoningLevel:)` works with Private Cloud Compute; the on-device model reported no reasoning capability (*measured*).
- Code for all three: [references/tools-images-reasoning.md](references/tools-images-reasoning.md).

## Test it

1. Test the quota note without using up a quota: in the scheme's Run options, "Simulated Apple Foundation Models Availability" has "Approaching Quota Usage Limit" and "Quota Usage Limit Reached" ([PCC guide](https://developer.apple.com/documentation/foundationmodels/adding-server-side-intelligence-with-private-cloud-compute); the WWDC26 video shows slightly different labels).
2. Start a summary on the closed phone, then press Open in Device Hub while it streams, and Closed again. The text must keep growing, with no restart and no second request.
3. Check book and tabletop (`duo-pose set book`, `duo-pose set tabletop` from `duo-pose-matrix`, or Device Hub's buttons): no button of the pane in the fold, and the bar sits in the bottom region in tabletop.
4. Profile token use with the Foundation Models instrument (Product > Profile) ([Managing the context window](https://developer.apple.com/documentation/foundationmodels/managing-the-context-window)).
5. Judge output quality on a device with Apple Intelligence. *Measured:* on our Mac the simulator's model failed every request, and `contextSize` read 0.

## Checklist

- [ ] On-device model first; Private Cloud Compute only with the entitlement, a reason, and the person's consent.
- [ ] Availability checked before showing the feature; every request also has a fallback for failure.
- [ ] The final `catch` is untyped and shows the non-AI path.
- [ ] One `AssistantModel` per window, owned by the window root; no request starts in `onAppear` or `.task` below a layout switch.
- [ ] A `@Generable` result with the closed-phone headline as its first property.
- [ ] Open and book: pane beside the content in a split `ArrangementView`. Closed and tabletop: one line plus a way to the full pane. Same feature on both displays.
- [ ] Sheet closes when the pane fits beside; the pane shows the same text in place.
- [ ] No Stop, Retry or text field in the fold in book or tabletop.
- [ ] The pane says it is AI, says what the model is doing, and has Stop and Retry.
- [ ] No user or web text in `instructions`; people told before text goes to Private Cloud Compute.
- [ ] iOS 26 and iOS 27 APIs behind `@available` when the app deploys lower.
- [ ] Tested through close and open while streaming, and on a device with Apple Intelligence.
