---
name: cx-voice-qa
description: Use to set up or fix quality assurance for voice/phone support, including transcript-based and AI-graded call QA. Trigger for "QA our calls", "score phone conversations", call transcription accuracy for QA, diarisation or speaker attribution problems, word error rate, grading calls from transcripts, or adapting a chat/email QA scorecard to voice.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Voice QA: grading calls you cannot read

Voice QA looks like text QA with an extra step. It is not. **You are grading a
transcript, not a call**, and the transcription pipeline introduces errors that
become grading errors — errors that are not randomly distributed.

## The problem that makes voice QA different

Automatic speech recognition and speaker diarisation fail **systematically**, not
randomly. Word error rate is consistently worse for:

- Accented and non-native speech
- Regional dialects and code-switching
- Poor audio: mobile handoffs, low-bandwidth codecs, background noise
- Overlapping speech and interruptions
- Domain vocabulary, product names, alphanumerics

Every one of those correlates with **who** is speaking. So a QA programme grading
transcripts without measuring transcription quality produces scores that are
systematically lower for agents with certain accents and for calls with certain
customers. That is a fairness problem and a validity problem at once, and it is
invisible unless you go looking.

**Measure word error rate on your own audio before you trust transcript-based
grading.** Not the vendor's benchmark — yours, segmented by accent, channel, and
audio condition.

## Step 1: validate the pipeline before writing any criteria

Build a gold set of **30–50 calls with human transcription**, deliberately spanning
your real conditions: accents, languages, mobile and landline, quiet and noisy,
short and long, and at least a few with heavy crosstalk.

Then measure:

**Word error rate.** `WER = (substitutions + insertions + deletions) / reference words`.
Report it **by segment**, not just overall. An aggregate WER of 12% that is 6% for
one group and 25% for another is not a 12% problem.

**Diarisation error.** What share of utterances are attributed to the wrong
speaker? This matters more than WER for compliance work: a disclosure attributed
to the customer instead of the agent inverts the finding.

**Entity accuracy.** Names, amounts, reference numbers, dates. General WER can look
fine while every account number is wrong, which breaks exactly the criteria that
depend on specifics.

Use the result to decide which criteria are gradeable at all. This is the step that
gets skipped, and skipping it means you never learn which of your scores are
noise.

## Step 2: choose criteria the transcript can actually support

| Criterion type | Transcript-gradeable? |
| --- | --- |
| Was information correct | Yes, if entity accuracy is good |
| Was the resolution complete | Yes |
| Was an explanation clear | Yes |
| Required disclosure given | **Only with human confirmation** |
| Identity verification completed | **Only with human confirmation** |
| Agent interrupted the customer | Poorly — needs timing, and crosstalk is where diarisation fails |
| Dead air / hold handling | No — needs audio timing, not text |
| Tone, pace, warmth | No — prosody is absent from a transcript |
| Talk-over ratio | No — needs the audio or a diarisation timeline |

**Anything that can end in an auto-fail must be confirmed against the audio by a
human.** A "missing" disclosure is at least as likely to be an ASR miss as a real
one, and the consequence of getting it wrong is disciplinary or regulatory.

For prosodic and timing criteria you need **audio features**, not transcript text:
silence duration, overlap ratio, speech rate, hold events. Many platforms expose
these separately from the transcript. If you do not have them, drop those criteria
rather than approximating them from words.

## Step 3: adapt the scorecard rather than reusing it

An email or chat scorecard does not transfer. Follow the general design procedure
in `cx-qa-scorecard-design` and then change these:

**Add** voice-specific criteria that have no text equivalent: hold handling and
warm-transfer quality, call opening and identity verification, dead-air
management, closing and next-step confirmation.

**Remove or rewrite** criteria that depend on written form: spelling and grammar,
formatting, link and attachment usage.

**Reinterpret** several that look transferable:

- **"First-contact completeness"** in voice means gathering everything in one call,
  not one message — a stronger and more measurable expectation.
- **"Acknowledgement before action"** happens in seconds on a call rather than
  paragraphs. Anchor it to the opening exchange.
- **Response time** does not exist within a call. Do not port it.

**Adjust sampling.** Call duration correlates with complexity, so a random sample
skews toward simple calls. Stratify by duration band, and deliberately include the
long tail — that is where compliance failures live.

## Step 4: expect AI grading to be worse on voice, and quantify it

If you grade transcripts with a model, the errors compound: transcription error
feeds grading error. Follow the AI-grading practice from
`cx-qa-scorecard-design` — evidence quotes, blinding to outcomes, per-criterion
agreement — with three voice-specific additions:

1. **Report agreement per audio condition**, not just per criterion. Model
   agreement with humans will be materially worse on accented and noisy calls,
   and that gradient is the fairness risk.
2. **Require the evidence quote to exist in the transcript**, and remember the
   transcript may itself be wrong. A verified quote proves the model did not
   hallucinate; it does not prove the words were said.
3. **Never auto-fail on transcript evidence alone.**

A practical guard: when a call's estimated WER (or the vendor's confidence score)
falls below a threshold, route it to human grading instead of scoring it. Grading a
bad transcript produces a number that looks like the others and is not comparable
to them.

## Step 5: handle the data properly, because voice is worse

Call recordings carry obligations that text does not.

- **Consent and recording law varies by jurisdiction** — some require all-party
  consent. Confirm before recording, and before moving recordings across borders.
- **Voice may be biometric data** in some jurisdictions, with stricter processing
  and retention rules than ordinary PII. Voiceprint analysis in particular.
- **Card data spoken aloud.** PCI DSS applies to recordings. DTMF suppression and
  pause-and-resume exist for this; verify they work rather than assuming.
- **Redact before transcripts leave your infrastructure**, including to a
  transcription or LLM vendor. That transfer is a processing decision that needs a
  basis.
- **Retention.** Recordings are large and sensitive; keep them only as long as the
  purpose requires, and make sure QA retention matches the stated policy.

Get the consent, retention, and cross-border position confirmed by compliance
before building the pipeline, not after.

## Step 6: report the measurement quality alongside the scores

Every voice QA report should carry:

- **WER overall and by segment**, so the reader knows the precision of the
  instrument.
- **The share of calls excluded** for poor transcript quality.
- **Which criteria are transcript-graded vs human-confirmed.**
- **Agreement by audio condition**, if AI-graded.

A voice QA score without transcription quality context is a number of unknown
accuracy presented as a measurement.

## Present results to the user

1. **Transcription quality first.** WER overall and by segment, and diarisation
   error. If WER differs materially across accent or audio groups, say plainly
   that transcript-based scores are not comparable across those groups — before
   presenting any score.
2. **Which criteria you excluded** as not transcript-gradeable, and why. This is
   usually the most useful part of the analysis.
3. **Scores**, with the excluded-call share stated.
4. **Auto-fails as a queue, not findings** — every one pending human confirmation
   against audio.
5. **The fairness check.** State explicitly whether scores correlate with audio
   condition or accent group. If they do, that is the headline finding and it is a
   measurement problem, not a performance one.
6. **Compliance posture** — consent, retention, redaction, and anything unresolved.

Do not paste transcript content into chat. Reference call IDs.

## Troubleshooting

**Some agents consistently score lower** — check WER by agent before concluding
anything about performance. Accent-correlated WER produces exactly this pattern.

**Compliance criteria fail at a surprising rate** — sample and listen. ASR misses
of scripted disclosures are common, because disclosures are read quickly and
often clipped.

**"Who said that" is wrong** — diarisation error. Measure it directly; it is a
different failure from WER and needs a different fix, usually better channel
separation in the recording.

**Interruption criteria produce nonsense** — crosstalk is precisely where
diarisation breaks. Either use audio overlap features or drop the criterion.

**Scores are not comparable to last quarter** — check whether the ASR model was
upgraded. Transcription changes shift scores with no change in agent behaviour;
pin and record the version.

**Short calls score better** — a sampling artifact. Stratify by duration.
