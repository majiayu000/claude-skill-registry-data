---
name: meta-muse-video-analysis
description: Analyze local video files with the fixed Meta Model API model Muse Spark 1.2 Contributor and a user-defined prompt. Use when Codex or Claude Code is asked to inspect, summarize, transcribe, timestamp, inventory, review, or extract information from a video and the META_MUSE_KEY Windows environment variable is available.
---

# Meta Muse Video Analysis

Analyze one local video with `scripts/analyze_video.py`. Keep the model fixed; never add or substitute a model selector.

## Workflow

1. Resolve the user's video to an absolute local path.
2. Preserve the user's analysis prompt verbatim unless they ask for prompt improvement.
3. Confirm that `META_MUSE_KEY` exists without printing its value.
4. Run:

```powershell
python "<skill-directory>\scripts\analyze_video.py" "C:\absolute\path\video.mp4" --prompt "Describe the requested analysis"
```

For long or multiline prompts, write the prompt to a temporary UTF-8 text file and use `--prompt-file`. Use `--output` when the user requests a saved result:

```powershell
python "<skill-directory>\scripts\analyze_video.py" "C:\absolute\path\video.mp4" --prompt-file "C:\absolute\path\prompt.txt" --output "C:\absolute\path\analysis.md"
```

5. Return the analysis or link the saved output. Surface API errors exactly enough to diagnose access, quota, format, or region issues, but never expose the API key.

## Operational rules

- Read the API key only from `META_MUSE_KEY`.
- Use only `muse-spark-1.2-contributor` through `https://api.meta.ai/v1`.
- In Codex, run the script with network approval. The key may be visible only in the approved outside-sandbox process; never copy it into command arguments or output.
- Check the model catalog before upload. If Contributor access is absent, stop without uploading and never fall back to standard `muse-spark-1.2`.
- Upload the video through the Files API and attach it to a Responses API request.
- Delete the remote file after the response, including after failures. Use `--keep-upload` only when the user explicitly asks to retain it.
- Do not silently preprocess, transcode, shorten, or split the video. If Meta rejects its format or size, report that limitation and ask before transforming the source.
- Treat Contributor uploads as externally shared data. Warn before sending secrets, private customer material, unreleased footage, or other sensitive content unless the user has already confirmed that the Contributor data terms are acceptable.
- Do not print, log, persist, or copy the API key.

## CLI reference

```text
analyze_video.py VIDEO (--prompt TEXT | --prompt-file FILE)
                 [--output FILE] [--json] [--keep-upload]
                 [--timeout SECONDS]
```

If neither prompt option is supplied, the script reads redirected stdin or asks interactively. `--json` emits a machine-readable result envelope. Progress and warnings go to stderr; the analysis goes to stdout.
