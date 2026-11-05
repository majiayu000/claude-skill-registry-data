---
name: record-video
description: use when recording browser workflows in our app, external sites, dashboards or prototypes for PRs, evidence, explanations or bug repros
---

record the real browser workflow and show the main flow first, followed by useful additional scenarios. choose the length and pacing to suit what the video needs to explain

## when useful

use video when the sequence or interaction helps explain the task. examples beyond our app:

- external integration flows: show an OAuth redirect through a provider and the return to our app
- provider consoles: show a sandbox webhook delivery and its response, or a deployment reaching a healthy state
- observability dashboards: trace an error in posthog or axiom to the relevant event or request
- storybook and prototypes: demonstrate keyboard navigation, responsive behaviour or hard-to-reach component states
- external bug repros and design references: reproduce a third-party browser issue or show the interaction behind a proposed UI change

## plan

identify the audience, the outcome to demonstrate, and the actions and expected results. reuse the task's known URL and any relevant checkout or test setup

keep the scenario, raw footage and editing source in `playground/videos/<slug>/` so later wording/layout changes can reuse valid footage

## delegate when video is a subtask

when video supports a larger task, delegate capture, editing and initial verification to a sub-agent. when recording is the main task, work directly unless parallel work has a clear benefit

give the recorder this skill, the URL, the scenario, permitted actions and the artifact directory. keep the shared source unchanged during capture or use an isolated snapshot. the recorder returns the local video and a compact verification summary without uploading or delegating again

the parent checks the main outcome and section boundary, then handles publication

## capture

follow `/agent-browser` for browser operation and `/runbooks` when starting this app. use a named background session and prepare login/test state off camera

CLI pattern, with the task's session, URL and output path:

```sh
agent-browser --session <session> open <url>
agent-browser --session <session> record start <output.mp4> --cursor
agent-browser --session <session> click <target> --human
agent-browser --session <session> record stop
agent-browser --session <session> close
```

use per-action `--human` for clicks and drags, with targets from the browser snapshot. it clicks on arrival. for hover, double-clicks or a pause before clicking, first move smoothly to the target using integer coordinates, then pause if needed and perform the action:

```sh
agent-browser --session <session> mouse move <x> <y> --duration 1000 --steps 60
```

the duration above is an example, not a pacing requirement. check installed `--help` when a command or flag differs

check a short take first. if viewport changes stretch the recording, capture each viewport separately and preserve its proportions during composition. initialise the visible cursor off take if it resets to the origin, and preserve its position across cuts and navigation

## presentation

user preferences override these defaults:

| element | default |
| --- | --- |
| background/text | black background, white text, original UI proportions |
| orientation | useful URL path at top left; include the hostname when moving between sites |
| additional scenarios | white "additional scenarios" label at top right, appearing when the main flow ends; omit when there are none |
| captions | short action/outcome captions outside the UI |
| audio | silent unless narration is requested |
| highlights | red arrows, circles, outlines or other shapes; combine highlights when useful |
| focus | zoom only when needed for readability, then return wide |

keep the section label separate from layout coordinates so it can move with a future layout. align highlights to observed elements and update the displayed path when navigation occurs

trim setup and dead air while keeping the result readable. retain the interaction and loading transitions needed as evidence; edits must not imply an unverified performance claim. keep ticket, environment and commit metadata outside the video

## verify and deliver

fully decode the final file with `ffmpeg` and check its metadata with `ffprobe`. inspect the demonstrated outcomes, pointer motion/cuts, section boundary and ending at the intended viewing size. nominal frame rate alone does not prove smooth motion

check the final video and visible URLs for private data before sharing. redact without hiding behaviour needed as proof. re-record failed outcomes rather than editing them into apparent success

return the video, what it demonstrates, and any limitations. include text chapter timestamps when useful

for PRs, upload the video using `/github-image-upload` and include it in the description. otherwise provide the local file unless an upload was requested

when token usage is requested, report measured usage including workers where available, distinguish cached input from new input/output, and state missing coverage
