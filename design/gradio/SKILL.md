---
name: gradio
description: Building ML demos and web UIs in Python with Gradio 6 — gr.Interface for wrapping a function, gr.Blocks for custom layouts with event listeners, gr.ChatInterface for LLM chat, streaming generator outputs, gr.State, image/audio components, queueing and concurrency, launch()/share links, and mounting into FastAPI with gr.mount_gradio_app. Use when demoing a model (image, audio, text, LLM), building a quick UI around a Python function, sharing a prototype via a public link, or hosting on Hugging Face Spaces.
---

# Gradio — ML demos and model UIs

## Overview

Gradio wraps Python functions in web UIs: declare input/output components, Gradio builds
the frontend, the API, and (optionally) a public share link. The default UI for
[[transformers]] models and Hugging Face Spaces (manage Spaces with [[hf-cli]]). For
dashboards and multipage data tools, [[streamlit]] is usually the better fit (see below).

Verified against **gradio 6.24** (Python 3.10+). Gradio 6 removed the legacy tuple chat
format and `show_api`/`type=` params — patterns below are current.

```bash
uv add gradio
uv run python app.py        # or: gradio app.py  (dev mode with auto-reload)
```

## Interface vs Blocks vs ChatInterface

| Class | Use for |
|---|---|
| `gr.Interface(fn, inputs, outputs)` | One function, auto layout — fastest demo |
| `gr.Blocks()` | Custom layout, multiple functions, cross-component events |
| `gr.ChatInterface(fn)` | LLM chat — history, streaming, retry/undo built in |

```python
import gradio as gr

def greet(name: str, intensity: int) -> str:
    return "Hello " + name + "!" * intensity

demo = gr.Interface(fn=greet, inputs=[gr.Textbox(), gr.Slider(1, 10, step=1)],
                    outputs=gr.Textbox(label="greeting"), flagging_mode="never")
demo.launch()
```

## Blocks: layout + event wiring

```python
with gr.Blocks() as demo:
    with gr.Row():
        inp = gr.Textbox(label="input")
        out = gr.Textbox(label="output")
    btn = gr.Button("Run")

    btn.click(fn=lambda s: s.upper(), inputs=inp, outputs=out)
    inp.submit(lambda s: s.upper(), inp, out)          # Enter key, same handler

    # one handler for several triggers:
    gr.on([btn.click, inp.submit], lambda s: s.upper(), inp, out)

demo.launch()
```

- Events live on components: `.click`, `.change`, `.submit`, `.upload`, `.select`, and
  `demo.load` (fires when a session opens). `gr.Timer(2).tick(...)` polls on an interval.
- To update component *properties* (not just value), return a component constructor:
  `return gr.Textbox(visible=False)` — or `gr.update(visible=False)`. Return a dict
  `{out_a: ..., out_b: gr.update(...)}` to update a subset of outputs.
- Chain steps with `.then()` (always runs) / `.success()` (only if no error):
  `btn.click(f1, ...).then(f2, ...)`.
- Raise `gr.Error("msg")` for a user-visible error toast; `gr.Warning`/`gr.Info` for
  non-fatal toasts.

## Streaming outputs

Any handler that `yield`s streams to the UI:

```python
def stream_reply(prompt):
    text = ""
    for token in llm.stream(prompt):
        text += token
        yield text                       # yield the FULL value so far, not the delta

btn.click(stream_reply, prompt_box, out_box)
```

Streaming *inputs* (webcam/mic): set `streaming=True` on `gr.Audio`/`gr.Image` and use
`stream_every=` on the event. Show progress in slow non-streaming fns by adding a
`progress=gr.Progress()` arg and calling `progress(0.5, desc="...")`, or
`gr.Progress(track_tqdm=True)`.

## Chat UIs

```python
def chat(message: str, history: list[dict]):   # history = OpenAI-style messages:
    # [{"role": "user", "content": "hi"}, {"role": "assistant", "content": "hello"}]
    partial = ""
    for tok in llm.stream(history + [{"role": "user", "content": message}]):
        partial += tok
        yield partial

demo = gr.ChatInterface(fn=chat, examples=["Explain X"], save_history=True,
                        additional_inputs=[gr.Slider(0, 1, label="temperature")])
demo.launch()
```

Gradio 6: messages format is the *only* history format (the `type=` param and tuple
format are gone). `multimodal=True` accepts file uploads (`message` becomes
`{"text": ..., "files": [...]}`). Return a `dict`/component/list for rich replies.

## State

- **Plain globals** are shared by *all* users — fine for read-only models, wrong for
  per-user data.
- **`gr.State(init)`**: per-session state. Pass it in `inputs` and `outputs`; the handler
  receives the value and returns the new value. Deep-copied per session, reset on reload.
- **`gr.BrowserState(default)`**: persists in localStorage across page reloads.

```python
with gr.Blocks() as demo:
    count = gr.State(0)
    btn = gr.Button("count")
    out = gr.Number()
    btn.click(lambda c: (c + 1, c + 1), count, [count, out])
```

## ML demo patterns (image/audio)

```python
def classify(img):                       # gr.Image default type="numpy"; also "pil"/"filepath"
    preds = pipe(Image.fromarray(img))   # e.g. a transformers pipeline
    return {p["label"]: p["score"] for p in preds}

demo = gr.Interface(classify, gr.Image(), gr.Label(num_top_classes=3),
                    examples=["examples/cat.jpg"])    # cached example gallery
```

- `gr.Audio(type="numpy")` → `(sample_rate, np.ndarray)`; `type="filepath"` → path str.
  Return audio the same way.
- `gr.Gallery` for image lists, `gr.Label` for classification dicts, `gr.ImageEditor`
  for sketch/mask input, `gr.Dataframe`/`gr.Plot` for tabular/figure output.
- Load a heavy model **once at module level** (before `demo.launch()`), not inside the
  handler.

## Queueing & concurrency

The request queue is always on. Defaults: each event runs with `concurrency_limit=1`
(one request at a time per event) — raise it for I/O-bound handlers:

```python
btn.click(fn, inp, out, concurrency_limit=8)          # 8 concurrent for this event
demo.queue(default_concurrency_limit=4, max_size=64)  # app-wide default + queue cap
gen_a.click(f, ..., concurrency_id="gpu")             # share one limit across events
gen_b.click(g, ..., concurrency_id="gpu")
```

## Launch options & deployment

```python
demo.launch(
    server_name="0.0.0.0", server_port=7860,   # bind for Docker/remote access
    share=True,                                  # free *.gradio.live public tunnel (72h)
    auth=("user", "pass"),                       # basic auth; or a callable
    max_file_size="10mb", allowed_paths=["/data/imgs"],
    mcp_server=True,                             # expose handlers as MCP tools
)
```

Every app auto-exposes an API (see the "Use via API" footer link) callable with
`gradio_client`. Deploy on Hugging Face Spaces by pushing `app.py` + `requirements.txt`
to a Space repo ([[hf-cli]]). Note: Gradio 6 replaced `show_api=False` with
`footer_links=[...]`, and per-event `api_name=False` hides an endpoint.

## Mounting into FastAPI

```python
from fastapi import FastAPI
import gradio as gr

app = FastAPI()

with gr.Blocks() as demo:
    ...

app = gr.mount_gradio_app(app, demo, path="/gradio")
# uvicorn main:app --host 0.0.0.0 --port 8000   → UI at /gradio, your routes elsewhere
```

Use this to add a demo UI to an existing [[fastapi]] service; don't call `demo.launch()`
when mounting. A handler can take a `request: gr.Request` arg to read headers/cookies.

## Gradio vs Streamlit

Gradio is **function-first**: you wrap `fn(inputs) -> outputs` and get a UI + API +
share link — ideal for model demos, quick prototypes, and Spaces. [[streamlit]] is
**script-first**: the whole script reruns per interaction — ideal for dashboards,
multipage internal tools, and dataframe-heavy exploration with fine layout control.
UI around one model/function → Gradio; interactive report/tool → Streamlit.

## Gotchas

- **Gradio 6 breaking changes**: chat history is messages-format only (no `type=` on
  `Chatbot`/`ChatInterface`); `show_api` → `footer_links`; check the migration guide
  before copying pre-6 snippets.
- **Yield cumulative values** when streaming — yielding only the delta makes the output
  flicker with fragments.
- **Mutable globals** = shared across users. Per-user data goes in `gr.State`.
- **GPU handlers with `concurrency_limit` > 1** will OOM; serialize them with a shared
  `concurrency_id` instead.
- **`share=True` exposes your machine** through a public tunnel — never with
  `allowed_paths` pointing at sensitive dirs.
- **Blocking startup**: `demo.launch()` blocks; in notebooks it embeds inline, use
  `demo.close()` to free the port.

## Related

Sibling UI framework: [[streamlit]] (dashboards, data tools). Models from
[[transformers]], Spaces/Hub via [[hf-cli]]; embed in a [[fastapi]] backend with
`gr.mount_gradio_app`.
