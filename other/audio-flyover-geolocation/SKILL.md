---
name: audio-flyover-geolocation
description: >-
  Acoustic fly-over geolocation: locate where an audio or video recording was made from the near-inaudible
  Doppler curves of propeller aircraft and helicopters in the background, matched against historical ADS-B
  tracks (about 100 m in good conditions), with an honest uncertainty region. Also covers thunder plus
  lightning-data localisation and a pre-publication acoustic privacy self-audit. Use this skill whenever the
  user wants to locate, verify or time a video, recording, livestream or call from its sound, background noise,
  aircraft noise, Doppler shift, spectrogram, ADS-B data or thunder; mentions acoustic geolocation, audio OSINT,
  "where was this recorded", verifying a video's location by sound, or colsto's method; or wants to check whether
  their own video leaks its location through sound, even if they never say Doppler or ADS-B. For OSINT
  verification, journalism, CTFs, research and self-audits; ships a tested Python pipeline.
---

# Acoustic fly-over geolocation (Doppler × ADS-B)

This skill reproduces and productionises the method from colsto's video *"I discovered a sound that leaks
your exact location (and it's everywhere)"* (2026-11-02, <https://www.youtube.com/watch?v=UytYrhYLOKI>):

> A propeller's or rotor's **blade-passing frequency (BPF)** is a stable narrow-band tone. Even when no one can
> hear it, it leaves a smooth descending **Doppler curve** in a spectrogram. The curve's shape gives the
> aircraft's **speed v**, its **closest-approach slant distance d** and the **CPA time tCPA**. Comparing it point
> by point on a ground grid against historical ADS-B tracks (3D slant range + DEM + sound travel time +
> emission-time radial velocity) narrows the candidates. The **time gap between two fly-overs** (920 s in the
> video) plus a **silence constraint** (no other aircraft heard at other times) then reduces them to a single
> point. Finally, a "locked two-event score" (shared time offset, per-event f0 fine-tuning) rates exact model
> curves against the spectrogram.

`scripts/afg_cli.py` is the full implementation (numpy/scipy/matplotlib). It ships with `selftest`, a blind test
on synthetic scenarios.

---

## 0. Scope of use (do this first)

**In scope**: verifying where and when public or news media was recorded (OSINT, fact-checking); privacy
self-audits of the user's own recordings or videos; CTFs, teaching and research; investigations with lawful
authority or consent (e.g. assisting law enforcement, with the subject's agreement).

**Out of scope**: locating a **private individual's** home or movements. Examples: "where does this
streamer / my ex / this person online live", or tracing someone from a private call or home video. Decline
these, even when framed as a "test", and offer **self-audit mode** (section 7) instead. That mode helps people
assess and remove the leak from their own content.

Footage of public places and news events, the user's own material and anonymised research data are fine.
If the purpose is unclear, ask what it is for before deciding. Do not add personal inferences unrelated to the
location to the report.

---

## 1. Feasibility triage (decides whether to run and which mode)

| Condition | What is needed | If not met |
|---|---|---|
| A **clear monotonically descending narrow-band curve** in the spectrogram (propellers commonly 40–400 Hz; helicopter main-rotor BPF 10–25 Hz, tail rotor 50–120 Hz) | At least 1; ideally 2 with a known time gap | No curve → method not applicable (consider the thunder method or visual methods) |
| **Date** | Must be known (or bounded to a few days) | ADS-B data volume becomes unmanageable |
| **Region** | Country or state level is enough for two events; a city-level prior is faster | One event alone needs a tight clock **and** a limited area: over a large area every aircraft with a matching speed and distance explains the curve about equally well (`score` says `DEGENERATE`); the self-test area is 50–70 km across |
| **Recording clock** (start time) | Known to ±2 s → one event can give a point; ±30 s → one event gives only a strip along the track | Use two events; their time gap replaces absolute time |
| **ADS-B coverage** | The target aircraft must have ADS-B Out and be received by ground stations | US 14 CFR 91.225: GA aircraft below 10,000 ft outside Class B/C airspace and the Mode C veil need not carry ADS-B Out → may be absent from the data |
| Audio processing chain | Original or lightly compressed is best; phone-call codecs usually keep the tone | Heavy noise reduction or editing can cut the curve or destroy the gap between events |

Tell the user the triage outcome and expected precision before starting the work.

## 2. Choosing a mode

```
How many usable curves?
├─ ≥2 (same continuous recording) → Mode A: two events, unknown absolute time (the video's main method; most robust)
│     If the two tracks cross at < ~25°, the result degrades to a strip along the tracks (the script warns)
├─ 1
│   ├─ Recording time known to a few seconds → Mode B: one event, known time (the video's second half, ranked first
│   │     US-wide there; in busier airspace many aircraft can fit equally, so restrict the area)
│   │     A straight constant-speed pass is mirror-symmetric → there is always a "mirror candidate";
│   │     a second clue (visual, terrain) is needed to pick between them
│   └─ Time known only to ±30 s or worse → Mode B′: only a strip of length ≈ 2·v·Δt is possible; report it as such
├─ No aircraft curve, but thunder + known date → Mode T: thunder envelope × lightning data (km level, see references/thunder-method.md)
└─ The user wants to protect their own content → Mode S: self-audit (section 7)
```

---

## 3. Workflow (CLI)

Convention: `AFG="python <skill dir>/scripts/afg_cli.py"`, working directory `work/`. Every step writes PNGs.
**Look at the PNGs yourself** with your image-reading ability (spectrograms, fit overlays, heat maps) rather
than relying on the numbers alone.

Check the environment first: `pip install numpy scipy matplotlib` (the DEM needs `rasterio`; non-WAV input needs
`ffmpeg`). On first use, run `$AFG selftest --seed 7` (about 40–60 s; exit 0 means the pipeline works).

### 3.1 Get the audio and metadata
- `ffprobe -v quiet -show_entries format_tags=creation_time:stream_tags=creation_time -of json input.mp4`
  gives the capture time. Mind the time zone. Social platforms often strip or rewrite metadata on re-encode, so
  **treat it only as a lead and cross-check it**.
- Pass the original sample rate to the script; it resamples internally to 4 kHz mono (`--channel` selects
  left or right).

### 3.2 Spectrogram → detect → trace → fit
```bash
$AFG spectrogram input.mp4 --out work/rec            # whitened narrow-band spectrogram + work/rec.png
$AFG detect work/rec.spec.npz --out work/boxes.json  # candidate boxes (t0, t1, fmin, fmax, score_z) + boxes.diag.json
$AFG plot work/rec.spec.npz --t0 160 --t1 320 --fmin 60 --fmax 380 --out work/zoom1.png
$AFG trace work/rec.spec.npz --t0 166 --t1 315 --fmin 98 --fmax 364 --out work/e1.csv
$AFG fit work/e1.csv --temp-c 18 --out work/e1.json  # v, d, tCPA, f0, search windows; overlay in e1.fit.png
```
Key points:
- `boxes.json` is the event list (a JSON array); the detection status is in `boxes.diag.json`. Stdout prints
  both in one object (`detection`, `events`, `events_file`).
- An empty `boxes.json` means "no fly-over" only when `boxes.diag.json` says `status: ok`. `limited` (short
  clip judged against the calibrated noise model, or mostly gated audio) and `insufficient` (clip shorter than
  `--min-dur`, or almost everything gated) come with `reasons`: read them, inspect `rec.png`, and lower
  `--min-dur` for short clips.
- Each event carries `trend` (`descending` or `flat`) and `drop_pct`. A ridge that rises in frequency is not a
  fly-over: it is listed under `rejected` in `boxes.diag.json`, not in `boxes.json`. `warnings` on an event mean
  its ridge does what one pass cannot (rises again, or falls by more than 45 %): it probably joins two aircraft
  or two harmonics. Inspect it with `plot` and trace each part in its own narrow box.
- `--win`: use 0.5–1 s for close, steep curves and 2–4 s for distant or faint ones. For a faint curve, zoom in
  with `plot` and confirm it by eye first. Then give `trace` a narrow box containing **only one harmonic**, and
  if needed add a few manual points with `--anchors "t:f,t:f,..."`.
- `trace` reports `box_coverage`; below 50 % it adds a `hint`. A curve that rises before it falls (a turning or
  accelerating aircraft) needs `--no-monotone`.
- Check the `fit` output:
  - `implausible` non-empty = the trace ran onto noise, jumped harmonics or kept only a short piece. **Do not**
    go on to the search (the script refuses too).
  - `notes`: left/right residual asymmetry = a turn or speed change; different approach/recede speeds = a climb
    or acceleration.
  - `sigma` already allows for correlated residuals (`resid_corr_time`, `sigma_inflation`, `n_eff`), but it is
    statistical only: a speed change during the pass biases v and d by more than sigma. `corr_v_d` near 1
    means v and d trade off along k = v²/d. The search therefore uses wide speed windows and the k window.
  - `constraints.d_min/d_max` is the search's distance window, which follows from the speed and k windows.
    `d_fit_min/d_fit_max` is what the fit itself supports (3 sigma); a note says when the two differ a lot.
- If you know the air temperature, pass `--temp-c` (c = 20.05·√(T+273.15)). v and d both scale with c; without
  a temperature, keep the default ±4 %.
- f0 is just the rest frequency of whichever harmonic you traced, not necessarily the fundamental; v and d do
  not depend on the harmonic number.
- BPF = blades × RPM / 60 can **help** guess the type (C172, 2 blades × 2400 rpm ≈ 80 Hz; DHC-8-400, 6 blades
  × 1020 rpm ≈ 102 Hz). Do not use it as a hard candidate filter.

### 3.3 ADS-B data (details in `references/adsb-data.md`)
- Sources:
  - adsb.lol `globe_history_YYYY`: one global release per day, free, ODbL.
  - ADS-B Exchange free samples: **1st of each month only**.
  - OpenSky Trino: needs a research account; table `state_vectors_data4`.
  - Your own readsb/tar1090 receiver.
- Extract only the target date, the target window ± 1 h, and the target area padded by ~0.5°.
```bash
$AFG adsb-ingest --src traces_dir/ --start 2026-09-08T13:00Z --end 2026-09-08T18:00Z \
    --bbox 38.5,39.7,-95.4,-93.8 --qnh 1018 --geoid-n -29 --out work/tracks.npz
```
- **The altitude datum decides slant-range accuracy.**
  - `alt_baro` is standard pressure altitude: correct it with local QNH (≈ 8.3 m/hPa; see METAR).
  - `alt_geom` is WGS84 ellipsoidal height (HAE); MSL = HAE − N.
  - `--alt-source auto` prefers geometric altitude.

### 3.4 DEM and search
```bash
$AFG dem-fetch --bbox 38.5,39.7,-95.4,-93.8 --out work/dem      # Copernicus GLO-30 (AWS public bucket)
$AFG search --tracks work/tracks.npz --events work/e1.json work/e2.json \
    --bbox 38.5,39.7,-95.4,-93.8 --dem work/dem/*.tif --rec-duration 1450 --out work/cands.npy
```
The funnel has three stages:
1. **Event-1 corridor**: speed window, k = v²/d consistency, slant-range window, and the CPA must not fall at a
   track endpoint.
2. **Inter-event offset**: tCPA2 − tCPA1, including each event's d/c travel delay.
3. **Silence filter**: in the remaining quiet spans, no other propeller or rotor aircraft may pass within
   `--d-quiet`.

The search stats (`cands.stats.json`) also report:
- `crossing_angle_deg` (two events): if every pair crosses at < 25°, the result can only be a strip;
- `flight_pairs`: with one event, how many different aircraft can explain it;
- `ground_elev_m`: the elevation range used. With `--ground-elev` it is a constant; in relief use `dem-fetch`
  (300 m of elevation error at 1.3 km slant range shifts the modelled distance by ~75 m).

Options:
- Mode B: add `--rec-start <UTC> --rec-start-tol 2` (or 30).
- `--quiet "a-b,c-d"` names recording spans where you are sure nothing was heard (default: everything outside
  the events). Give fewer spans when the recording has a lot of wind or speech. **Silence is signal, but false
  silence kills the true answer.** In sparse airspace (night, remote areas) it removes little: most candidates
  had no aircraft nearby anyway. It only gains power with traffic and with recording length.
- Default grid is 200 m. If there are too many candidates, shrink the bbox rather than enlarging the grid.

### 3.5 Scoring and refinement
```bash
$AFG score --tracks work/tracks.npz --spec work/rec.spec.npz --events work/e1.json work/e2.json \
    --cands work/cands.npy --dem work/dem/*.tif --out work/result.json
```
- **Model curves**: for each candidate, generate an exact model curve at **emission time** from the
  interpolated ADS-B positions and velocities (gs/track/vrate, not differenced positions), and compare it with
  the spectrogram. One time offset δ is shared, which locks in the physical time gap between the two events.
  Each event's f0 is fine-tuned within ±0.6 %.
- **Refinement**: every kept node gets a shrinking 3×3 hill-climb (100 → 25 m).
- **Grouping**: results are grouped by **flight pair**. Each pair keeps up to 3 hypotheses more than 500 m
  apart, so both mirror sides survive.
- **Trace check**: every hypothesis' model curve is compared with the traced points within ±60 s of each CPA
  (`trace_check`). A bright texture under a wrong curve (speech, music, wind) can lift a brightness score;
  it cannot make the model reproduce the trace. With two events, hypotheses that fail go below all others.
- **Outputs**:
  - `result.json`: best, `n_consistent`, `margin_vs_2nd`, `robust_z`, `ambiguous_alternatives`,
    `coarse_plateau`, `geometry`, `scoring` (how many candidates were scored and why others were not),
    `verdict`, `diagnosis`.
  - The verdict starts with `NO CONSISTENT SITE` (two events, nothing reproduces both traces; `diagnosis`
    lists the likely causes), `STRIP ONLY` (tracks cross at < 25°), `DEGENERATE` (one event, three or more
    other aircraft within 2 %), `AMBIGUOUS` or `unique within scored set`.
  - `result.rankN.*.png`: model-curve overlays.
  - `result.heatmap.png/csv`: radius of the 0.9 region.
  - `result.plateau.csv`.
- With a known recording clock, add `--rec-start ...`. Scoring then also forbids time shifts outside the
  clock; without `--rec-start-tol` it uses the search's tolerance. The time shift spans at least event 1's
  CPA-time tolerance `t_tol`, the same window the funnel used.

### 3.6 Verification (not optional; see `references/verification.md`)
0. **Trace check**: `best.trace_check.consistent` must be true. `NO CONSISTENT SITE` means there is no answer,
   whatever the score.
1. **Overlays**: the model curve must fit the observation on **both asymptotes and through the CPA**, not just
   one segment.
2. **Heat map**: the 0.9-region radius is the error to report. Report a strip when either holds:
   - two events: `geometry.warning` is set (small crossing angle);
   - one event: `coarse_plateau.length_m` > 600 m.
3. **Mirror candidates and alternatives**: rule them out with visual clues (horizon, buildings, vegetation, road
   noise, echoes), DEM viewsheds and sun azimuth.
4. **Falsification**: should other fly-overs near the answer also have been heard?
   - Heard but not detected = a detection-threshold problem.
   - Present when they should not have been audible = the location is wrong.

## 4. Precision rules (and why)

1. **Emission time**: f_obs(t) = f0 / (1 + Ṙ(τ)/c), with t = τ + R(τ)/c. Using Ṙ at reception time gives a
   curve of the **wrong shape**, not just a shifted one.
2. **3D slant range + DEM**: observer elevation plus microphone height (default 2 m). Treating 500 m of
   terrain relief as 0 makes both d and tCPA wrong.
3. **Altitude datum**: uncorrected pressure altitude with a 30 hPa QNH offset ≈ 250 m of altitude error, which
   goes straight into d.
4. **Delayed CPA**: the moment f = f0 is observed is tCPA_emit + d/c (1 km ≈ 2.9 s). Event offsets and the
   clock must both be converted with this.
5. **k = v²/d is more reliable than v or d alone.**
   - The mid-curve slope, −f0·v²/(c·d), is pinned down tightly. The asymptotes are often polluted by noise,
     gating, or the aircraft accelerating or climbing.
   - So the search uses a wide speed window plus a narrow k window, and each candidate aircraft's own ground
     speed predicts its d.
6. **Locked scoring**: both events share one δ. Otherwise each event aligns its own time, and wrong locations
   score well too.
7. **Refine to ≤100 m**: the 200 m grid is only a coarse screen; the final point comes from sub-grid
   hill-climbing and the heat map.
8. **Silence is signal**, but keep the thresholds generous (defaults: propeller 3 km, rotor 2.5 km). Distant
   or low-power aircraft may genuinely be inaudible.
9. **Loose windows, strict scoring**: in the funnel, err wide, because a true answer filtered out can never be
   recovered. Leave discrimination to exact-model scoring.
10. **Group by flight pair and keep the mirror**: a straight constant-speed pass is symmetric about its track.
    Single-event results should report at least both sides.
11. **ADS-B gaps**: no match ≠ not in the area. Low-level GA, military aircraft and some helicopters may lack
    ADS-B or go unreceived (terrain masking, low altitude).
12. **Sound speed and wind**: v and d scale with c. With wind, c_eff = c + w·n; in strong wind (>8 m/s), widen
    the d window.

## 5. Report

Output using `assets/report_template.md`, in the user's language. It must include:
- the answer coordinate plus an error radius or strip;
- the matched flights (hex / registration / type) and the recording start time in UTC;
- the key evidence (fit parameters, overlays, heat map);
- ambiguities and alternatives, and data-coverage gaps;
- a confidence grade (see the rubric in verification.md) and what cannot be ruled out.

**Do not** present a single high score as "certain". When margin < 10 % or ambiguous_alternatives exist, say
explicitly that the result is "ambiguous".

## 6. Typical failures and fixes

| Symptom | Cause | Fix |
|---|---|---|
| fit gives v≈280 m/s or d=60 km | The trace ran onto noise, jumped between harmonics, or kept only a short piece (`trace` `hint`) | Narrow to a single-harmonic box; use `--anchors`; `--no-monotone` if the curve rises before it falls; inspect with `plot` before tracing |
| `detect` finds nothing in a short clip | `status` is `insufficient` (clip shorter than `--min-dur`) or the curve is weak | Read `boxes.diag.json`; lower `--min-dur`; look at `rec.png` and trace by hand with `--anchors` |
| An event has `warnings`, or one box spans two curves | Two aircraft audible at the same time, or the ridge jumped between harmonics | `plot` the box; trace each curve in its own box; `detect --window 20 --step 5` separates closer passes |
| A visible tone is missing from `boxes.json` | Its ridge rises, so it is listed under `rejected` in `boxes.diag.json` | A straight pass never rises; if it is a turning aircraft, trace it by hand with `--no-monotone`, not as a primary event |
| Empty funnel | Windows too narrow / wrong altitude datum / missing ADS-B / wrong time window | First widen `--v-margin/--k-margin/--c-uncert`; check QNH and `--start/--end`; check `--event-classes` |
| Many candidates with similar scores, `DEGENERATE` | One event over a large area or with no clock, near-parallel tracks, or a curve that is too short | Add a second event, pin down the clock, shrink the area, report a strip |
| `NO CONSISTENT SITE` | No candidate's model reproduces both traced curves: recordings from different places or a wrong offset between files, an aircraft missing from ADS-B, the site outside the bbox, or a bad trace | Read `diagnosis`; check each fit overlay; widen bbox and time window; say in the report that a missing aircraft cannot be ruled out |
| `score` says "nothing scored", or `scoring.rejected_clock` > 0 | Score's clock tolerance is tighter than the search's | Leave out `--rec-start-tol` in `score` (it then uses the search's) or pass the same value |
| The true speed lies far outside fit `sigma` | The aircraft changed speed or climb during the pass; sigma is statistical only | Expected; the search's speed and k windows cover it. Compare `fit_split` |
| Verdict says the f0 scale sits at the limit | The fitted f0 is off, often from a speed change in the pass | Re-run `score` with `--f-rel 0.012`; do not treat it as a reason to drop the answer |
| Best point's rec_start differs from metadata by tens of seconds | The metadata is the export/upload time | Trust the acoustic result and explain it in the report |
| Jet interference | Jets are broadband noise plus a few tones | By default only prop/rotor/unknown classes are events; jets only count for the silence check |

## 7. Self-audit mode (protecting your own content)

```bash
$AFG audit my_video.mp4 --out work/audit
```
This outputs candidate fly-overs, the detection status and a risk level. Only ridges that fall in frequency
count as fly-overs: rising tones are set aside (`detection.rejected`, mentioned in `notes`), and a candidate
with `warnings` counts as two. `undetermined` means the automatic check could not decide (for example a clip
shorter than 12 s, a tonal ridge too short or too flat to judge, or a rising tone that may hide a fly-over); it
is not a pass. A file shorter than the 1 s analysis window is `undetermined` with no PNG. Even `low` only covers
sustained aircraft tones this detector can see, so always look at the PNG.

**What works**:
- **Cut** at least one fly-over, or break the time gap between two fly-overs.
- Replace or remove the original audio track (re-record the narration).
- Also scrub GPS/EXIF/QuickTime metadata and visual clues.

**What doesn't**:
- High-pass filtering: it overlaps the voice band, and the residual can still be recovered.
- "Drowning it out": a narrow-band tone still stands out in the spectrogram.
- Call noise suppression: it only gates during silence.

See `references/countermeasures.md`.

## 8. Reference files (read as needed)

| File | When to read |
|---|---|
| `references/physics.md` | Derivations, identities, error propagation, wind/temperature, helicopters/multi-engine |
| `references/spectrogram.md` | Parameter choice, whitening/gating, diagnosing trace failures, identifying harmonics |
| `references/adsb-data.md` | How to download each data source, formats, fields, altitude datums, coverage gaps, type classification |
| `references/search-and-scoring.md` | Funnel and scoring algorithm details, every parameter, tuning advice |
| `references/verification.md` | Visual verification, confidence rubric, stereo-bearing extension, synthetic test baseline |
| `references/thunder-method.md` | Thunder × lightning-data localisation when there is no aircraft |
| `references/countermeasures.md` | How effective each privacy countermeasure is |
| `references/sources.md` | Video, paper, data and regulation sources |
