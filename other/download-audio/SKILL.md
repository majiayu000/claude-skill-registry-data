---
name: download-audio
description: Download audio recordings from Coval voice simulations. Use when user wants to listen to or analyze call recordings.
argument-hint: "[simulation-id or run-id]"
---

# Download Simulation Audio

Download audio for `$ARGUMENTS`.

## Single Simulation

```bash
coval simulations audio <simulation_id> -o recording.wav
```

This downloads the audio file with a progress bar.

## Bulk Download (All from Run)

### Step 1: List Simulations with Audio

```bash
coval simulations list --run-id <run_id> --format json | \
  jq -r '.[] | select(.has_audio == true) | .simulation_id'
```

### Step 2: Download Each

```bash
for sim_id in $(coval simulations list --run-id <run_id> --format json | jq -r '.[] | select(.has_audio == true) | .simulation_id'); do
  coval simulations audio $sim_id -o "${sim_id}.wav"
done
```

### Step 3: Organize

Suggest organizing by test case:

```bash
mkdir -p audio/<run_id>
# Download files into organized directory
```

## Audio URL Only

To get the URL without downloading:

```bash
coval simulations audio <simulation_id>
```

This prints the presigned URL (valid for 1 hour).

## Notes

- Audio is only available for voice agent simulations
- URLs expire after 1 hour
- Format is typically WAV or MP3
- Files include both agent and simulated caller audio
