---
name: gemini-robotics
description: Integrate and debug Gemini Robotics ER perception, function calls, and guarded execution. For a first natural-language robot assistant demo, start with architect's reference-app selection.
---

# Gemini Robotics

Keep Gemini on the perception and planning side of an actuator boundary. The
model may choose a capability; deterministic robot software validates and
executes it.

## Choose the endpoint from the interaction

- For a new robot assistant or first simulation demo, read
  [architect](../architect/SKILL.md) before building a model/robot integration.
  It discovers the saved apps checkout and checks compatible examples. If a
  baseline was already selected, continue here; existing integration fixes
  and API explanations do not need onboarding.
- Use `gemini-robotics-er-2-streaming-preview` for a stateful Live API session
  that receives text, JPEG frames, or audio and orchestrates robot tools with
  low latency.
- Use `gemini-robotics-er-2-preview` for discrete embodied-reasoning requests
  such as spatial analysis or offline video work. The standard endpoint does
  not provide the Live API.
- Treat both model IDs and feature support as preview surfaces. Re-check the
  current [model overview](https://ai.google.dev/gemini-api/docs/robotics-overview)
  before changing dependencies or deployment assumptions.

## Make the stream an observe-act-observe loop

- Keep one `client.aio.live.connect` session open for the task and run a receive
  loop that handles both model content and tool calls.
- Serialize user turns and model-facing heartbeats around unresolved turns and
  blocking tools. A text heartbeat is a new reasoning input, not a transport
  keepalive, and can interrupt an action as barge-in.
- Declare physical actions with `behavior: BLOCKING`. Execute each call through
  the robot adapter, then manually return a `FunctionResponse` with the call ID,
  name, and structured result using `send_tool_response`.
- Stream raw 16-bit, 16 kHz, little-endian PCM for speech input and explicitly
  end finite audio with `audio_stream_end=True`. Send JPEG camera frames at no
  more than the endpoint's current one-frame-per-second limit.
- A camera frame alone updates context but does not trigger reasoning. Pair it
  with user audio/text, or use an intentional heartbeat prompt. Heartbeats are
  turns and can interrupt generation.
- When a tool exists specifically to observe the world, attach its fresh image
  to that call's `FunctionResponse` when the SDK supports inline media. This
  binds the evidence to the requesting call more deterministically than placing
  an unrelated realtime frame immediately before the response.
- The streaming endpoint returns text, not synthesized audio. Route speech
  through an independently replaceable TTS adapter or expose speaking as a
  bounded tool.

Use Google's current [robotics streaming guide](https://ai.google.dev/gemini-api/docs/robotics-streaming)
for the volatile SDK syntax. Read [FAILURES.md](FAILURES.md) when a session
stalls, ignores images, overlaps actions, or never finishes an audio turn.

## Guard the robot outside the model

- Expose semantic capabilities such as named-waypoint navigation, bounded
  inspection, or grasping a currently grounded object. Do not expose raw motor
  commands, arbitrary poses, or unrestricted coordinates merely because the
  function schema can describe them.
- Validate the tool allowlist, exact arguments, ranges, named resources, and
  current perception-issued object IDs in ordinary code. A system instruction
  and JSON schema improve model behavior but are not the safety boundary.
- Build the advertised tool list from capabilities that passed preflight. Do
  not leave a disconnected robot, camera, or accessory visible to the model as
  a callable tool.
- Return completion, rejection, and failure states to the model. After motion,
  send a fresh observation so the next decision is based on the resulting
  scene rather than the pre-action frame.
- Give every long-running action cancellation and a deadline. On session or
  tool timeout, invoke the robot's stop/cancel path independently of the model.
- On half-duplex hardware, pause microphone ingestion before speech or another
  device action and resume it explicitly afterward. Keep this device handoff
  outside the model's control.
- Prove the same semantic contract against a fake adapter, representative
  simulation, and finally supervised hardware. Keep simulator- and robot-
  specific motion details behind the adapter.

For the evidence behind these choices and their current validation limits, read
[SILLY-TURTLEBOT.md](SILLY-TURTLEBOT.md) for a ROS/Nav2 mobile robot and
[STACKCHAN-ER2.md](STACKCHAN-ER2.md) for a USB, audio, camera, and BLE companion.
Use `integration` for process or transport boundaries, `ros2` and `navigation`
for deterministic mobile-robot execution, and `testing` for the
fake-to-simulation-to-hardware acceptance ladder.

## Done

- A complete user turn can stream input, execute a blocking semantic action,
  return its result, and reason from a fresh observation.
- An undeclared or invalid action is rejected before reaching the robot SDK.
- Timeout and cancellation behavior is proven without depending on a model
  response.
