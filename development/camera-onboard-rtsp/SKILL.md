---
name: camera-onboard-rtsp
description: Use when a standard IP camera (RTSP and ONVIF) is being added to the shop camera bridge or swapped in for an old one, when someone asks how to find a camera's stream address or ONVIF profiles, or when a camera that only works through its own phone app is supposed to feed the car counter, in which case this skill says stop and swap the camera. Read-only probes, a copy of the config and a registry entry only. Not for a counter or sign camera that died or shows zero (production-health-report, systematic-debugging, empty-vs-error), reel content (nickstire-reel-operator), or installing or running Frigate, MediaMTX, detectors, plate readers or the vision edge.
triggers: camera, ip camera, onvif, rtsp, new camera, replace the camera, rtsp url, hook up a camera, camera bridge
---

# Camera onboard, standard RTSP and ONVIF only

Answer first: this adds or replaces one camera with a standard RTSP and ONVIF one. It ends at a verified stream, a registry entry marked not commissioned, and a hand-off. It builds and installs nothing.

## Scope

- The production sign camera is fed today by the V380 vendor relay, an FFmpeg crop and MediaMTX (`camera-bridge/README.md`, top note), launched by `camera-bridge/scripts/nicksmax/nicksmax-camera-supervisor.ps1`. This skill does not touch, repair or extend that lane. The plan is to replace that camera with a standard one (Nour, 2026-10-22).
- A dead sign counter, a relay that will not come back, or a panel showing zero is not this skill. Send it to `production-health-report` or `systematic-debugging`, and `empty-vs-error` for the zero.
- Commissioning the vision edge (model, calibration, `camera-bridge/scripts/install-edge-runtime.ps1`) is a separate job that needs Nour's go. This skill never runs it, and the first real event is that job's proof.

## Stop line (read before anything else)

No reverse-engineered decoders, no extracted vendor keys, no prebuilt programs from hobby repos, no cloud-relay bridges, no protocol bridges for closed camera apps. `docs/UPSTREAMS.md` (row "V380 protocol bridges", 2026-09-08) rejects those bridges for production; its only allowance is lab use under Windows Sandbox if the operator insists, which is Nour's call alone. If the camera has no RTSP or ONVIF, say STOP in the first sentence and tell Nour to swap it for a camera that lists both. `camera-bridge/README.md` section 1 and `camera-bridge/scripts/test-rtsp.ps1` still print advice to run a `ceshi.ini` unlock on some cameras. For this skill that advice is a STOP: run no unlock tool. Section 1 predates the 2026-10-22 decision.

## Steps

1. **Confirm the camera.** Get the exact model from Nour (box or label). Check the maker's spec page for RTSP and ONVIF. Either one missing is the stop line. Open ports do not decide this.
2. **Find it and fix it in place.** Find it from the router's client list or Nour's own tools, on the shop LAN only. Nour reserves its address in the router and makes a read-only viewer account in the camera's own page, never the admin one. The Frigate example uses one viewer account and one password variable, `FRIGATE_RTSP_PASSWORD`, for every camera (`camera-bridge/frigate/config.example.yml`, `camera-bridge/.env.example`), so make that same viewer account. Nour types the password himself, letters and digits only. Never ask for it.
3. **Read the stream.** Put the full address in an environment variable. In Bash run `set -o pipefail; ffprobe -rtsp_transport tcp -show_entries stream=codec_name,width,height,avg_frame_rate -i "$CAMERA_URL" 2>&1 | sed 's#://[^@/]*@#://REDACTED@#'` on the main stream and the sub stream (paths from the spec page, not guesses), because a failed open can echo the login. The filter was tested on a made-up address. Record codec, size, frame rate. Then the port check without a password: `camera-bridge/scripts/test-rtsp.ps1` with `-SkipFfprobe` and `-Cameras` set to the new camera only (its default list is the old shop cameras). ONVIF profiles are a hand-off: Nour runs `uv run --with onvif-zeep-async==4.3.0 python` himself with a short read-only profile call, types his own login, and pastes back only profile names and sizes. His password never enters this chat. The library is a throwaway (see its row in `docs/UPSTREAMS.md`).
4. **Prove the picture is real.** A live sensor never repeats a frame exactly; a frozen or looping stream does. Grab about 40 frames at two a second with `ffmpeg` into a scratch folder outside the repo, run them through `FrameHealth` (`camera-bridge/vision/framehealth.py`: frozen, looping, distinct) with a throwaway script you do not commit, and delete the frames after. Ask Nour to walk through the view holding a sheet with the time on it, and check a grabbed frame shows it.
5. **Register it, then hand off.** Copy, then edit the copy: `camera-bridge/config.example.yaml` to `config.yaml` (ignored by git) and `camera-bridge/frigate/config.example.yml` to `camera-bridge/frigate/config/config.yml`, which git does NOT ignore, so keep it uncommitted. No real address, password or serial goes into any committed file; the repo is public and examples keep placeholders. In a PR, add the camera to `EXPECTED_CAMERAS` in `apps/nickstire/shared/cameras.ts` (camera, label, role, healthProfile, power) with `commissioned: false`, so it shows muted, not as a fault. A `cloudDeviceId` needs an existing statenour device; creating one is a production write, so stop and ask Nour (`prod-db-guard`). Finish with one sentence handing the commissioning job to Nour.

## Receipts and health rule

Each step ends with the command, one summary line and the exit code, labelled FACT (you ran it) or NOT CHECKED. Router, firewall, Tailscale and subnet changes are Nour's decisions; the camera stays off the public internet, no port forwarding, vendor cloud off if the camera allows it. Health follows `apps/nickstire/server/lib/cameraHealth.ts`: vision reads seeing, quiet, warming, blind or unknown, and interaction cameras read not_required. Blind needs zero detections for 10 minutes while the edge ran, no gate crossing in the last hour, and the shop open; unknown never blocks healthy. A dead or silent camera is never reported as zero cars.

## Never

- Never use, build, download or suggest a decoder, relay, bridge or key extractor for a camera that has no RTSP or ONVIF.
- Never write or run a script that installs third-party software. Frigate, MediaMTX, detectors, plate reading, cloud services and `onvif-zeep-async` have their own rows in `docs/UPSTREAMS.md`; MediaMTX already runs in the sign lane and this skill does not install or restart it.
- Never print, store or ask for a camera password, never use the admin account, and never print an address with a login in it.
- Never probe beyond the shop's own network, guess passwords or try default logins.
- Never run the vision edge, create the statenour device row, switch to production mode or turn on alerts without Nour's explicit go.
