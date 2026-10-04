---
name: icaire-educate-publish-zoom-recording
description: Recover, safely identify, publish, and attach a completed Zoom cloud recording to the correct ICAIRE Educate live session. Use when a recording link is missing or wrong, a Zoom session recording needs public no-passcode playback, an automatic recording webhook failed, or an administrator asks to publish or repair a Zoom recording on an Educate lesson or live session.
---

# ICAIRE Educate: Publish Zoom Recording

Publish one completed Zoom cloud recording to one ICAIRE Educate live session.
Treat this as a manual recovery path: identify both records, change only the
recording's access settings, update Educate through its supported write path,
and verify both systems.

## Required Context

- Identify the target Educate programme, cohort, and live session. If the user
  did not give an unambiguous session, list plausible sessions and ask them to
  choose before changing either system.
- Read the current live-session record and its recording field before writing.
  Prefer ICAIRE Educate MCP tools. If the expected tools are missing or only
  partly loaded, use `find-missing-tools` before concluding they are
  unavailable.
- Discover Zoom MCP tools for listing and reading cloud recordings. Expected
  tools include `recordings_list` and `get_recording_resource`. If the Zoom
  surface is absent or partial, use `find-missing-tools` before concluding it
  is unavailable.
- Discover ICAIRE Educate MCP tools for reading live sessions and the protected
  `publish_zoom_recording` operation. That protected operation owns the Zoom
  sharing-setting mutation and Educate update; do not work around it with raw
  credentials or direct production database writes.

## Match the Correct Occurrence

Do not construct or predict a recording URL. Zoom recording URLs and recurring
meeting occurrence UUIDs are opaque.

1. Read the session's scheduled start, end or expected duration, timezone,
   title, Zoom meeting ID, and occurrence UUID when stored.
2. List completed Zoom cloud recordings in a narrow window around the scheduled
   session.
3. Match in this priority order:
   - exact Zoom occurrence UUID
   - exact meeting ID plus a single occurrence whose start time overlaps the
     Educate session
   - exact meeting ID plus uniquely matching date, start time, and title
4. Use duration only as corroboration, never as the sole match. Allow for an
   early start, overrun, and recording processing delay.
5. Reject deleted, processing, failed, or zero-duration recordings.
6. Stop without writing if multiple occurrences remain plausible, the stored
   identifiers conflict, or the date/time evidence does not uniquely identify
   one occurrence. Show the candidates without exposing private playback data.

## Choose the Playback Target

Prefer the occurrence's meeting-level cloud-recording share/playback URL. This
keeps multiple valid segments together when recording was paused or restarted.

If the available integration exposes only recording files, select a file only
when exactly one completed MP4 satisfies all of these:

- belongs to the matched occurrence UUID
- has non-zero size and duration
- is a normal session view, preferring shared-screen-with-speaker when present
- is not an audio-only, transcript, chat, or timeline artifact

If several completed MP4 segments are part of the occurrence, do not publish
the longest file by guesswork. Use the meeting-level share URL or stop and ask
for a choice.

## Publish Through ICAIRE Educate

Pass the unambiguous Educate session identifier and matched Zoom occurrence
identifier to the protected `publish_zoom_recording` MCP tool. Use only fields
declared by its live schema. The operation must make the minimum changes needed
for a learner to open the recording without signing into Zoom or entering a
passcode:

- enable sharing for the matched recording
- disable viewer authentication
- disable on-demand registration
- disable the share passcode when the integration supports that setting
- keep viewer downloads disabled unless the user explicitly asks to enable them

Do not send Zoom credentials, recording tokens, or passcodes as tool arguments.
Do not change the original meeting's join settings, unrelated recordings, or
account-wide defaults. If the protected tool is unavailable after missing-tool
discovery, stop and report the missing capability; do not fall back to raw Zoom
API calls.

Open or inspect the resulting learner-facing URL without privileged query
parameters when a safe read-only check is available. Confirm that it resolves
to the matched occurrence and does not prompt for authentication, registration,
or a passcode. Never paste an access token or passcode into Educate.

## Update ICAIRE Educate

1. Have `publish_zoom_recording` write the verified Zoom share/playback URL to
   the target live session's supported recording URL field (currently commonly
   named `recorded_session_url`; discover the live schema instead of assuming
   it).
2. Do not separately update the database unless the protected tool explicitly
   returns a safe retry instruction for an atomicity failure.
3. Preserve unrelated session fields. If replacing a non-empty different URL,
   report the old host and target session and obtain confirmation unless the
   user explicitly asked to correct that link.
4. Read the session back from Educate and confirm the stored URL exactly matches
   the verified Zoom URL.

## Verification and Output

Return a compact report containing:

- programme, cohort, and live-session name/date
- Zoom meeting ID in masked form and occurrence match basis
- selected target type: meeting share page or single MP4
- public access checks: sharing, authentication, registration, passcode, and
  download status
- Educate write path and read-back result
- any ambiguity, missing capability, or manual action still required

Do not claim success unless Zoom settings and Educate read-back were both
verified. If Zoom was changed but the Educate write fails, report the partial
state clearly so the operation can be retried safely.

## Guardrails

- Do not expose tokens, passcodes, privileged query parameters, private email
  addresses, or raw MCP/API responses containing secrets.
- Do not infer an occurrence from duration alone or attach a recording based
  only on a similar title.
- Do not make a recording public until the target occurrence is unambiguous.
- Do not overwrite a different existing recording silently.
- Do not download, re-upload, delete, trim, or edit the recording unless the
  user explicitly requests that separate action.
