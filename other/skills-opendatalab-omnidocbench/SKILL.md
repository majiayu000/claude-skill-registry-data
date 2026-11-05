---
name: omnidocbench-eval-helper
description: Help users deploy, validate, run, and parse OmniDocBench evaluations. Use this skill whenever the user mentions OmniDocBench, document parsing/OCR benchmark scoring, MinerU or other model evaluation on OmniDocBench, CDM formula metrics, end2end/md2md configs, Docker/conda deployment, remote SSH/H-cluster execution, result JSON parsing, or troubleshooting TeX Live/ImageMagick/Ghostscript/Docker/worker/OOM issues. Prefer Docker first, generate concrete commands from the user's paths, validate inputs before running, and report final Overall/Text/Formula/Table/Reading-order scores with result file paths.
---

# OmniDocBench evaluation helper

Help community users run OmniDocBench reproducibly. Prefer a practical, path-specific workflow over generic setup advice:

1. Validate GT/prediction paths and runtime access.
2. Generate an isolated config using stable container paths.
3. Run `python pdf_validation.py --config ...` in Docker when possible.
4. Parse `*_metric_result.json`, `*_run_summary.json`, `*_stage_execution.json`, and `*_runtime_environment.json`.
5. Report scores, output paths, and any warnings that affect score credibility.

Be concise for simple questions, but include copy-paste commands when the user gives paths.

## What to ask for

Ask only for missing details that affect commands or config:

- Deployment mode: Docker, conda/source, or remote SSH. Recommend Docker when CDM is needed.
- Evaluation type: default to `end2end` for OmniDocBench JSON + page markdown predictions.
- Paths:
  - ground-truth JSON, commonly `OmniDocBench.json` with exact capitalization on Linux
  - prediction markdown directory, often a nested `markdown/` folder such as `.../mineru/markdown`
  - output directory, or permission to create a timestamped output directory
- Whether CDM is required.
- CPU/RAM or node size if the user mentions slowness, OOM, or cluster execution.

If the user explicitly asks you to run a job on a remote host and provides an SSH command, treat that as authorization for that host/path scope. Avoid destructive operations: do not delete, overwrite, or chmod shared data/results.

## Key facts

- Entrypoint: `python pdf_validation.py --config <config_path>`.
- Default config: `configs/end2end.yaml`.
- Package: `omnidocbench-eval`, Python `>=3.10,<3.12`.
- Recommended Docker image: `ghcr.io/zeng-weijun/omnidocbench-eval:repro-ubuntu2204`.
- CDM depends on TeX Live/CJK, ImageMagick PDF read/write, and Ghostscript. Docker avoids most CDM dependency failures.
- Worker keys:
  - `dataset.match_workers`: page matching
  - `metrics.display_formula.cdm_workers`: CDM rendering/comparison, memory-heavy
  - `metrics.table.teds_workers`: table TEDS
- Worker rule: on 4 CPU / 8 GB, use `2` for match/CDM/TEDS; if unstable, use `1`. Do not keep README default `13` on small nodes.

## Input validation before running

Always validate before launching a long Docker evaluation. For remote runs, execute this on the remote host via SSH.

```bash
GT=/path/to/OmniDocBench.json
PRED=/path/to/prediction/markdown

test -f "$GT" && echo "GT_OK=$GT" || echo "GT_MISSING=$GT"
test -d "$PRED" && echo "PRED_OK=$PRED" || echo "PRED_MISSING=$PRED"
[ -f "$GT" ] && wc -c "$GT"
[ -d "$PRED" ] && echo "md_count=$(find "$PRED" -maxdepth 1 -name '*.md' | wc -l)"
[ -d "$PRED" ] && echo "empty_md=$(find "$PRED" -maxdepth 1 -name '*.md' -empty | wc -l)"
[ -d "$PRED" ] && find "$PRED" -maxdepth 1 -name '*.md' | sort | head -5
nproc
free -h || true
```

Interpretation:

- Full OmniDocBench v1.6 has 1651 pages. `md_count` should usually be close to 1651 for a full run.
- `md_count=0` usually means the user passed a parent directory instead of the actual `markdown/` directory.
- `empty_md > 0` is not fatal, but report it because empty predictions lower scores.
- Linux paths are case-sensitive: `OmniDocBench.json` and `omnidocbench.json` differ. If GT is missing, check nearby JSON filenames before concluding the data is absent.

## Docker workflow

Use Docker when possible, especially for CDM.

### Check Docker access

```bash
DOCKER=docker
if ! docker ps >/dev/null 2>&1; then
  if sudo -n docker ps >/dev/null 2>&1; then
    DOCKER="sudo -n docker"
  else
    echo "Docker daemon is not accessible by docker or sudo -n docker"
    exit 4
  fi
fi
$DOCKER --version
```

Use `sudo -n docker` only when the user is authorized on that host. Do not try interactive sudo in an automated workflow.

### Local end2end command

Use stable container paths and write a custom config inside the container. This avoids editing the repository and keeps host paths out of YAML.

```bash
GT=/abs/path/to/OmniDocBench.json
PRED=/abs/path/to/prediction/markdown
OUT=/abs/path/to/output_dir
WORKERS=4   # use 2 on 4CPU/8G; use 1 if CDM OOMs
IMAGE=ghcr.io/zeng-weijun/omnidocbench-eval:repro-ubuntu2204

mkdir -p "$OUT"

DOCKER=docker
if ! docker ps >/dev/null 2>&1; then
  if sudo -n docker ps >/dev/null 2>&1; then DOCKER="sudo -n docker"; else exit 4; fi
fi

$DOCKER pull "$IMAGE"
$DOCKER run --rm --entrypoint bash \
  -v "$GT":/workspace/gt/OmniDocBench.json:ro \
  -v "$PRED":/workspace/data_md/predictions:ro \
  -v "$OUT":/workspace/result \
  "$IMAGE" \
  -lc "cat > configs/custom_end2end.yaml <<EOF
end2end_eval:
  metrics:
    text_block:
      metric: [Edit_dist]
    display_formula:
      metric: [Edit_dist, CDM]
      cdm_workers: ${WORKERS}
    table:
      metric: [TEDS, Edit_dist]
      teds_workers: ${WORKERS}
    reading_order:
      metric: [Edit_dist]
  dataset:
    dataset_name: end2end_dataset
    ground_truth:
      data_path: ./gt/OmniDocBench.json
    prediction:
      data_path: ./data_md/predictions
    match_method: quick_match
    match_workers: ${WORKERS}
    quick_match_truncated_timeout_sec: 300
    match_timeout_sec: 420
    timeout_fallback_max_chunk_span: 10
    timeout_fallback_order_penalty: 0.10
EOF
python pdf_validation.py --config configs/custom_end2end.yaml 2>&1 | tee /workspace/result/eval.log"
```

If CDM is not needed, remove `CDM` from `display_formula.metric` and remove `cdm_workers`. This avoids TeX/ImageMagick/Ghostscript dependency failures, but the final report will not include Formula CDM.

## Remote SSH / H-cluster workflow

When the user provides an SSH command, run the same validation and Docker workflow on the remote host. Use a heredoc remote script to avoid nested quoting bugs.

```bash
ssh -CAXY user@host 'bash -s' <<'REMOTE'
set -euo pipefail

GT=/mnt/shared-storage-user/.../1.6/OmniDocBench.json
PRED=/mnt/shared-storage-user/.../mineru/markdown
OUT_ROOT=/mnt/shared-storage-user/.../omnidocbench_eval
OUT="$OUT_ROOT/mineru_$(date +%Y%m%d_%H%M%S)"
LATEST=/tmp/omnidocbench_latest_out.txt
IMAGE=ghcr.io/zeng-weijun/omnidocbench-eval:repro-ubuntu2204

mkdir -p "$OUT"
echo "$OUT" > "$LATEST"

test -f "$GT" || { echo "GT_MISSING=$GT"; exit 2; }
test -d "$PRED" || { echo "PRED_MISSING=$PRED"; exit 2; }
MD_COUNT=$(find "$PRED" -maxdepth 1 -name '*.md' | wc -l)
EMPTY_MD=$(find "$PRED" -maxdepth 1 -name '*.md' -empty | wc -l)
echo "GT_OK=$GT"
echo "PRED_OK=$PRED"
echo "md_count=$MD_COUNT"
echo "empty_md=$EMPTY_MD"
[ "$MD_COUNT" -gt 0 ] || { echo "No markdown files found; check nested markdown directory"; exit 3; }

DOCKER=docker
if ! docker ps >/dev/null 2>&1; then
  if sudo -n docker ps >/dev/null 2>&1; then
    DOCKER="sudo -n docker"
  else
    echo "Docker daemon is not accessible by docker or sudo -n docker"
    exit 4
  fi
fi

CPU=$(nproc)
MEM_KB=$(awk '/MemTotal/ {print $2}' /proc/meminfo 2>/dev/null || echo 0)
MEM_GB=$((MEM_KB / 1024 / 1024))
if [ -n "${FORCE_WORKERS:-}" ]; then
  WORKERS="$FORCE_WORKERS"
elif [ "$CPU" -le 4 ] || [ "$MEM_GB" -lt 10 ]; then
  WORKERS=2
else
  WORKERS=4
fi

echo "output_dir=$OUT"
echo "latest_pointer=$LATEST"
echo "cpu=$CPU mem_gb=$MEM_GB workers=$WORKERS"

$DOCKER pull "$IMAGE"
$DOCKER run --rm --entrypoint bash \
  -v "$GT":/workspace/gt/OmniDocBench.json:ro \
  -v "$PRED":/workspace/data_md/predictions:ro \
  -v "$OUT":/workspace/result \
  "$IMAGE" \
  -lc "cat > configs/custom_end2end.yaml <<EOF
end2end_eval:
  metrics:
    text_block:
      metric: [Edit_dist]
    display_formula:
      metric: [Edit_dist, CDM]
      cdm_workers: ${WORKERS}
    table:
      metric: [TEDS, Edit_dist]
      teds_workers: ${WORKERS}
    reading_order:
      metric: [Edit_dist]
  dataset:
    dataset_name: end2end_dataset
    ground_truth:
      data_path: ./gt/OmniDocBench.json
    prediction:
      data_path: ./data_md/predictions
    match_method: quick_match
    match_workers: ${WORKERS}
    quick_match_truncated_timeout_sec: 300
    match_timeout_sec: 420
    timeout_fallback_max_chunk_span: 10
    timeout_fallback_order_penalty: 0.10
EOF
python pdf_validation.py --config configs/custom_end2end.yaml 2>&1 | tee /workspace/result/eval.log"

echo "DONE_OUT=$OUT"
ls -lh "$OUT"
REMOTE
```

Practical H-cluster lessons from a real MinerU v1.6 run:

- `ssh -CAXY` may print X11 warnings such as `No xauth data`; they are harmless for CLI evaluation.
- Docker may be installed but inaccessible through the daemon socket. Check `docker ps`; if it fails and `sudo -n docker ps` works, use `sudo -n docker` for the run.
- Record the output directory in `/tmp/omnidocbench_latest_out.txt` or a user-specific variant so it can be recovered after disconnection.
- GT capitalization matters: `/.../OmniDocBench.json` worked where lowercase `omnidocbench.json` did not.
- MinerU predictions may live in a nested `markdown/` directory. Passing the parent directory can produce zero or inflated markdown counts.
- For 4CPU/8G with CDM, start with workers `2`; use `1` if unstable.

## Bundled helper scripts

This skill includes scripts that can be copied into the repo or run from the skill directory:

- `scripts/generate_end2end_config.py`: generate an end2end YAML.
- `scripts/parse_results.py`: parse a result directory and print a compact score/validation report.

Example:

```bash
python scripts/generate_end2end_config.py \
  --gt ./gt/OmniDocBench.json \
  --pred ./data_md/predictions \
  --out configs/custom_end2end.yaml \
  --workers 2

python scripts/parse_results.py /path/to/result_dir
```

Use `--no-cdm` with `generate_end2end_config.py` to omit CDM and `cdm_workers`.

## Conda/source workflow

Use only when Docker is unavailable or the user needs to modify OmniDocBench code.

```bash
conda create -n omnidocbench python=3.10 -y
conda activate omnidocbench
pip install -e .
python -c "from src.core.pipeline import run_config_file; print('OK')"
```

For CDM in source installs, verify:

```bash
pdflatex --version | head -2
kpsewhich CJK.sty && kpsewhich c70gkai.fd
gs --version
magick --version | head -2
python -m pytest tools/test_environment_and_smoke.py::TestEnvironmentVersions -v -s
```

If ImageMagick blocks PDF read/write, adjust the ImageMagick 7 `policy.xml`. Prefer Docker instead when possible.

## Config guidance

### End2end

Use `dataset_name: end2end_dataset`, OmniDocBench JSON as `ground_truth.data_path`, and page-level markdown files as `prediction.data_path`. Use `match_method: quick_match` unless the user has a specific reason not to.

Prediction filenames should correspond to page image names with `.jpg`/`.png` replaced by `.md`. Some code paths also accept `.mmd`, but `.md` is the community-standard expectation.

### md2md

Use md2md when both ground truth and prediction are markdown directories:

```yaml
dataset:
  dataset_name: md2md_dataset
  ground_truth:
    data_path: /path/to/gt_mds
    page_info: /path/to/OmniDocBench.json
  prediction:
    data_path: /path/to/pred_mds
  match_method: quick_match
```

`page_info` enables page-level attributes and filtering.

### Single-module recognition and detection

For formula/text/table recognition, the JSON usually contains both ground-truth and prediction fields; set `prediction.data_key` to the model field such as `pred`.

For layout/formula detection, ask for prediction JSON box schema and category names before writing `pred_cat_mapping`.

## Result parsing and validation

After a successful run, list result files. Key files usually include:

- `*_metric_result.json`: raw metric data and attribute breakdowns
- `*_run_summary.json`: notebook-style summary and `overall_notebook`
- `*_stage_execution.json`: page count, worker counts, timeout/error/exception counts
- `*_runtime_environment.json`: Python/system/TeX/ImageMagick/Ghostscript details
- `eval.log`: full console log

Extract and report these fields:

```text
overall = run_summary.notebook_metric_summary.overall_notebook
text_edit = metric_result.text_block.all.Edit_dist.ALL_page_avg
formula_cdm = metric_result.display_formula.page.CDM.ALL * 100
formula_edit = metric_result.display_formula.all.Edit_dist.ALL_page_avg
table_teds = metric_result.table.page.TEDS.ALL * 100
table_teds_structure = metric_result.table.page.TEDS_structure_only.ALL * 100
table_edit = metric_result.table.all.Edit_dist.ALL_page_avg
reading_order_edit = metric_result.reading_order.all.Edit_dist.ALL_page_avg
```

Also report validation counters:

- input prediction count and empty markdown count, if checked
- `stage_execution.page_match.page_count`
- `stage_execution.page_match.fallbacks.quick_match_timeout.count`
- `stage_execution.metrics.display_formula.CDM.sample_count`, `timeout_case_count`, `error_case_count`, `exception_case_count`
- `stage_execution.metrics.table.TEDS.sample_count`, `timeout_case_count`, `error_case_count`, `exception_case_count`
- runtime environment for TeX/CJK, ImageMagick, and Ghostscript

A clean run has CDM/TEDS timeout/error/exception counts equal to zero. Nonzero `quick_match_timeout` is a warning, not automatically a failed run.

### Final report template

Use this structure after running evaluation:

```markdown
## Result paths
- Output dir: `...`
- Metric JSON: `.../*_metric_result.json`
- Run summary: `.../*_run_summary.json`
- Stage execution: `.../*_stage_execution.json`
- Runtime environment: `.../*_runtime_environment.json`

## Scores
| Metric | Score |
|---|---:|
| Overall | **95.651953** |
| Text Edit Distance ↓ | **0.036843** |
| Formula CDM ↑ | **97.076037** |
| Formula Edit Distance ↓ | **0.093306** |
| Table TEDS ↑ | **93.564123** |
| Table TEDS Structure Only ↑ | **96.123305** |
| Table Edit Distance ↓ | **0.063565** |
| Reading Order Edit Distance ↓ | **0.125134** |

## Validation
- pages: 1651
- prediction md files: 1651, empty: 2
- quick_match_timeout_count: 2
- CDM samples/timeouts/errors/exceptions: 2352 / 0 / 0 / 0
- TEDS samples/timeouts/errors/exceptions: 665 / 0 / 0 / 0
- runtime: TeX Live 2025, ImageMagick 7.1.1-47, Ghostscript 9.55.0, CJK ok
```

Mention empty prediction files by name if there are only a few.

## Troubleshooting playbook

- **GT missing**: check `OmniDocBench.json` capitalization and parent directory.
- **Prediction count zero**: use the actual page-level markdown folder, not the parent.
- **Prediction count too high**: parent directory may contain multiple model outputs; use the exact model `markdown/` folder.
- **Docker permission denied**: try `sudo -n docker`; if that fails, ask for Docker group/sudo setup.
- **CDM OOM or hang**: reduce all workers, especially `cdm_workers`; on 4CPU/8G use `2`, then `1`.
- **ImageMagick PDF policy error**: Docker should avoid it; in source installs, allow PDF read/write in ImageMagick 7 `policy.xml`.
- **`pdflatex`/`kpsewhich`/CJK missing**: use Docker or install TeX Live 2025 and CJK resources.
- **`latexmlc` unavailable**: not necessarily fatal for standard end2end HTML-table evaluation; report only if the chosen table pipeline requires LaTeX-to-HTML conversion.

## Safety and execution guidance

- Ask before starting long Docker pulls or evaluations unless the user explicitly says to run them.
- On remote/shared systems, create new timestamped output directories; do not overwrite or delete existing results.
- Use read-only mounts for GT and prediction inputs (`:ro`). Mount only the output directory writable.
- If running in the background, tell the user the task ID and output path, then parse results when complete.
