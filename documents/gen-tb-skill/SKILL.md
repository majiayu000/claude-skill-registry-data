---
name: gen-tb
description: Generate a complete UVM testbench scaffold for a single IP from its spec documents (docx/pdf/md) and register table (xlsx/csv/md/IP-XACT). Use whenever the user asks to "generate a UVM tb", "build a verification environment", "scaffold a testbench", "create a UVC", "set up DV for this IP", or anything equivalent in Chinese ("帮我生成验证环境", "搭一个 tb", "做 UVM 环境", "做这个 IP 的验证"). Also trigger when the user points at a directory containing an IP spec and asks Claude to "verify it" / "test it" without naming UVM explicitly. Produces a runnable UVM tb (APB / AHB-Lite / AXI4-Lite as first-class buses; other single-channel buses via a generic fallback) with sanity + register-access tests passing, plus a DE-friendly `tb_api::` task BFM.
---

# gen-tb — UVM Testbench Scaffold Generator

## Purpose

Generate a directory-aligned UVM testbench for one IP from:

Built-in first-class buses: APB slave, AHB-Lite (slave or master),
AXI4-Lite (slave or master). Other single-channel request/response
buses (I2C, SPI, Wishbone, OBI, custom register buses, …) are handled
by a generic fallback that reuses the same layout, sim flow, and
`tb_api` surface — see §Scope below.

Inputs:

- behavioral spec: `*.docx`, `*.pdf`, `*.md`
- register table: `*.xlsx`, `*.csv`, markdown table, IP-XACT XML
- RTL in place, an external RTL path, or a generated stub

The result must compile, run `<ip>_sanity_test`, run
`<ip>_reg_access_test`, and provide two usage surfaces:

- DV persona: UVM tests, sequences, agent, monitor, RAL hooks
- DE persona: `tb_api::write/read/expect_reg` task-style BFM

## Scope

| Dimension | Built-in (high-quality scaffold) | Generic fallback | Planned |
|---|---|---|---|
| Bus | APB slave, AHB-Lite (slave or master), AXI4-Lite (slave or master) | any single-channel request/response bus the scaffold sub-agent can infer from spec + the three built-in exemplars (e.g. I2C, SPI, Wishbone, OBI, custom register buses) | AXI4 full |
| Simulator | VCS, Questa (vlog/vsim — static-only, see note), xrun (Cadence Xcelium) | VCS, Questa, xrun | — |
| Ref model | none, SV, C-DPI | none, SV, C-DPI | Python-DPI |
| Spec input | docx, pdf, md | docx, pdf, md | — |
| Reg input | xlsx, csv, md, IP-XACT | xlsx, csv, md, IP-XACT (optional — set `register_semantics: no` for non-register buses) | — |

Generic fallback is a best-effort path: directory layout and sim flow
stay authoritative, but the bus-shaped pieces (`<bus>_if.sv`, agent,
sequence library, `tb_api` body) are inferred per-IP by a constrained
scaffold sub-agent that pattern-matches on the three built-in
references. Tell the user up-front that scaffold correctness is lower
and the chance of an `unresolved.md` delivery is higher than in
built-in mode. Load `references/generic_bus.md` only when entering
this path.

AXI4 full (bursts/IDs/outstanding) is out of scope in both modes — it
must never be routed to generic. If the DUT has AXI ports, follow the
AXI4-full detector in Phase 1 and the mandatory question in Phase 2.
For DUTs that expose AXI signals but use only single-beat transfers,
generate the AXI4-Lite environment with a monitor-side assertion that
`AWLEN == 0 && ARLEN == 0`, so any later burst use fails loud at sim
time rather than relying on user review.

Do not use this skill for debugging an existing UVM environment, formal
verification, gate-level sim, DFT, or a multi-master SoC subsystem.

## Pipeline

Each phase writes audit artifacts under `<ip>/work/_gen_audit/`.
Do not collapse phases; resumability and auditability are part of the
deliverable.

1. Discover: identify IP, spec, regs, RTL, optional external VIP
2. Intake: ask only unresolved questions
3. Normalize: produce `registers.yaml`, `behavior.md`, `parse_report.md`
4. Scaffold: write the generated tree
5. Compile-fix: run compile and use a constrained sub-agent if needed
6. Sanity: run mandatory tests and runtime-fix loop if needed
7. Hand-off: write `CLAUDE.md`, `unresolved.md`, and concise summary

### Pipeline Hooks (Optional)

After each phase finishes writing its audit artifacts, call:

```bash
python3 scripts/hooks.py <phase> <ip_root>
```

with `<phase>` ∈ `{discover, intake, normalize, scaffold, compile_fix,
sanity, handoff}`. The script looks for
`<ip_root>/.gen_tb_hooks/<phase>[.strict].{py,sh}` and is a no-op when
absent (zero cost in the common case). Non-strict hook failures are
logged to `work/_gen_audit/hooks/<phase>.log` and do not block the
pipeline; `.strict.` hooks abort the phase on non-zero exit. Hooks
receive a JSON payload on stdin and `GEN_TB_PHASE` / `GEN_TB_IP_ROOT` /
`GEN_TB_AUDIT_DIR` in env. Do not invoke hooks before audit artifacts
for the phase are on disk.

## Phase 1: Discover

### IP Selection

Pick the IP root in this order:

1. Explicit IP name/path from the user
2. Current directory if its basename looks like an IP name
3. The only child directory containing spec files
4. Otherwise ask the user to choose

Show the selected IP name and path once so the user can correct it.

### Spec And Registers

Search `spec/`, `doc/`, `docs/`, then IP root. Classify:

- register table: `*reg*table*.xlsx/csv`, `*regs*.xlsx/csv`, IP-XACT XML
- behavior spec: large `*.pdf`, `*.docx`, `*spec*.md`
- markdown tables that look like regs: confirm if ambiguous

Do not ingest README, license, unrelated datasheets, draft/old/bak files.

### RTL

Prefer an existing filelist. Otherwise scan `rtl/`, `src/`, `design/`,
`hdl/`, and `<ip_name>/` for RTL, excluding tb/test/sim/bench paths.
If no RTL exists, generate a stub only when the user confirms.

Infer top module using AST tooling if available; regex inference is
medium confidence. If top is ambiguous, ask. Record exact APB / AHB /
AXI4-Lite signal names and widths in `rtl_discovery.yaml`; never
normalize case. For AHB-Lite and AXI4-Lite, also record which side of
the bus the DUT sits on (`bus_direction: slave|master`) — slave is the
default and means the TB drives a master BFM; master means the TB
provides a memory-backed slave responder.

For buses that fall through to generic mode, `rtl_discovery.yaml`
does **not** record `bus_direction`. The direction is collected in
Phase 2 into `bus_handshake.yaml.direction` and that is the single
source of truth for generic mode.

For details, load `references/rtl_discovery.md` and
`references/rtl_stub.md`.

### Bus Classification

After signal recording, classify the bus:

1. If the top's port set matches the APB / AHB-Lite / AXI4-Lite
   signature, set `bus_protocol` accordingly. **Unchanged path.**
2. **AXI4-full detector.** If any of `awlen | arlen | awburst |
   arburst | awid | arid` is present with width > 0, set
   `axi_full_signature: true` in `rtl_discovery.yaml`. The Phase 2
   mandatory question below decides whether to refuse or degrade
   to AXI4-Lite. An AXI signal set must never be routed to
   `bus_protocol: generic`.
3. Otherwise set `bus_protocol: unknown` and emit a
   `candidate_signals:` block (the request/response-looking port
   group) into `rtl_discovery.yaml`. Do not guess a name — the
   bus name is collected in Phase 2.

### Existing Bus VIP

If the user says they already have an APB, AHB, or AXI4-Lite VIP, ask
for only:

- `<bus>_vip_path`
- desired reuse level: `import_only` or `drive_with_vip`

Use:

```yaml
bus_protocol: apb                  # or ahb, axi_lite
apb_vip_source: reuse_my_vip       # or ahb_vip_source / axi_lite_vip_source
apb_vip_path: <path>               # or ahb_vip_path / axi_lite_vip_path
apb_vip_reuse_level: import_only   # or ahb_vip_reuse_level / axi_lite_vip_reuse_level; default
```

`import_only` means scaffold imports the VIP into the compile tree and
keeps built-in tests on `tb_api`. `drive_with_vip` means Phase 5 must
also generate/adapt glue so the user's VIP can drive a minimal bus
read/write smoke sequence — **not implemented in v1**; `scaffold.py`
refuses `drive_with_vip` and the skill must default to `import_only`
or hand-author the VIP-driven smoke test post-hoc. Do not guess
third-party VIP APIs in Phase 4. For `import_only`, scaffold may skip
vendor `*_test_pkg.sv` files that only serve the VIP's standalone
harness.

Load `references/apb_external_vip.md`, `references/ahb_external_vip.md`,
or `references/axi_lite_external_vip.md` before implementing or fixing
external VIP reuse.

At phase end, if `<ip>/.gen_tb_hooks/` exists, run
`python3 scripts/hooks.py discover <ip_root>`.

## Phase 2: Intake

Ask unresolved items in small batches. Questions to ask only when not
already known.

**Preset bundles are allowed** (e.g. "Default config" / "Add C-DPI" /
"VCS + xrun"), but every preset menu must satisfy:

1. The currently supported simulators (`vcs`, `questa`, `xrun`) must
   all appear at least once across the offered presets, or be reachable
   via an explicit "Customize simulators" / "Type something" path that
   lists them. Never present a simulator-related preset that names only
   a subset (e.g. listing "VCS / xrun" while omitting Questa) — it
   misleads the user into thinking the missing one is unsupported.
2. The same rule applies to any other dimension with >1 first-class
   value (bus protocol, refmodel language). If a preset hides a
   first-class option, the menu must include a visible "Customize"
   escape that surfaces the full set.
3. The AXI4-full mandatory question (see below) is **never** allowed
   inside a preset bundle — it must be its own AskUserQuestion turn.

Fields to ask about when not already pinned by Phase 1:

- RTL state: found, external path, generated stub, none
- bus protocol: APB, AHB, AXI4-Lite, or `generic` (when Phase 1 set
  `bus_protocol: unknown`)
- bus direction (AHB-Lite, AXI4-Lite, generic): DUT is slave (default) or master
- bus VIP source: generate fresh, reuse existing VIP
- external VIP reuse level: import only, drive with VIP
- reference model language: none, SV, C-DPI (Python-DPI schema exists but is
  not yet emitted — see `references/refm_dpi.md`)
- clock/reset: `pclk/presetn`, `hclk/hresetn`, or `aclk/aresetn` frequency, polarity, reset cycles
- UVM version: default 1.2 unless user specifies otherwise
- **simulator toolchain** (multi-select): `vcs`, `questa`, `xrun`.
  Default `[vcs]` when unanswered. Record in `intake.yaml` as
  `simulators: [vcs]` / `[vcs, questa]` / `[vcs, xrun]` /
  `[vcs, questa, xrun]` / etc. At least one must be selected.
  Per-sim emission:
  - `vcs` → `script/makefile` (canonical `make all SV_CASE=<case>`).
  - `questa` → `script/makefile_questa`
    (`make -f makefile_questa all SV_CASE=<case>`). **Static-only** —
    gen-tb has no Questa install to validate against; tell the user to
    verify locally before trusting it in CI.
  - `xrun` → `script/makefile_xrun`
    (`make -f makefile_xrun all SV_CASE=<case>`).
  When `vcs` is not selected, `script/makefile` becomes a thin shim
  that `include`s whichever sim-specific makefile is present, so the
  canonical `make all SV_CASE=...` still works. `scripts/compile_and_sanity.py`
  drives VCS by default; for questa-only or xrun-only configurations,
  run the mandatory tests with `make -f makefile_<sim> all SV_CASE=<case>`
  manually. Recommended user-facing wording:
  *"Which simulators should I generate makefiles for? VCS / Questa /
  xrun (multi-select; default VCS)."*
- **tcsh/csh setup helper**: default no. If the user uses tcsh/csh,
  record `emit_setup_csh: true` in `intake.yaml`; scaffold still emits
  `script/setup.sh` and additionally emits `script/setup.csh`. Do not
  infer this from `$SHELL`; generated trees may be used by other users
  or CI shells.
- address width: `paddr_width`, `haddr_width`, or `axi_addr_width`, default 12
- endianness for multi-word arrays
- coverage: enabled or skipped
- required extra smoke tests

### AXI4-full Mandatory Question

When `rtl_discovery.yaml` has `axi_full_signature: true`, ask exactly:
*"Does this DUT use bursts (>1 beat), IDs, or outstanding?"* This
question is mandatory and cannot be skipped. Record the answer in
`intake.yaml` as `axi4_full_features: none` (No) or
`axi4_full_features: present` (Yes) — `scaffold.py` refuses to run
without it.

- Yes (`axi4_full_features: present`) → hard refuse. Write
  `unresolved.md` pointing to planned AXI4-full work and exit. Do not
  enter Phase 3.
- No (`axi4_full_features: none`) → route to the built-in AXI4-Lite
  path. Phase 4 must emit a monitor-side assertion that
  `AWLEN == 0 && ARLEN == 0`, so any later burst use fails loud at
  sim time.
- Unanswered / skipped → treat as Yes (refuse). `scaffold.py` exits
  FATAL when `axi_full_signature: true` and the intake key is absent.

### Generic Bus Intake Sub-Batch

When `bus_protocol` resolves to `generic`, collect the structured
handshake description into `work/_gen_audit/bus_handshake.yaml`:

```yaml
bus_name: <short token, used in filenames>
direction: slave | master
clock: { name: <port>, freq_mhz: <n> }
reset: { name: <port>, polarity: low|high, cycles: <n> }
addr:  { port: <port>, width: <n> } | null     # null = non-addressed
data:  { write_port: <port>, read_port: <port>, width: <n> }
handshake:
  kind: req_ack | valid_ready | strobe | custom
  req:   <port>
  ack:   <port>
  extra: [ <other control ports to model> ]
burst: none | simple_incr
register_semantics: yes | no
notes: |
  Free-form. Primary handshake hint to the scaffold sub-agent.
```

Confirm `register_semantics` explicitly. `no` means RAL and
`<ip>_reg_access_test` are not generated and Phase 6 degrades to
`<ip>_responder_smoke_test`.

All generated tests must be named `<ip>_<purpose>_test`.

Every question turn must include an abort/restart option. Save partial
answers to `work/_gen_audit/intake.yaml` and `bus_handshake.yaml`, and
resume from them if present.

At phase end, if `<ip>/.gen_tb_hooks/` exists, run
`python3 scripts/hooks.py intake <ip_root>`.

## Phase 3: Normalize

Create:

```text
work/_gen_audit/spec_normalized/registers.yaml
work/_gen_audit/spec_normalized/behavior.md
work/_gen_audit/spec_normalized/parse_report.md
```

Never proceed to Phase 4 without valid `registers.yaml`, **except**
when `bus_handshake.yaml.register_semantics == no` in generic mode —
that case has no register table by design, and `registers.yaml` is
optional. `behavior.md` and `parse_report.md` are still required in
all cases. Missing behavior parsers may degrade to warnings, but a
missing/unparseable register table is blocking outside the
`register_semantics: no` exception.

Field-level reset values win over register-level reset values. Emit
warnings for unparseable offsets, widths, bit ranges, PDF tables,
ambiguous aliases, and contradictions. The user must be told to read
`parse_report.md`.

Load `references/spec_parsing.md` and
`references/registers_yaml_schema.md` for schemas and parser rules.

At phase end, if `<ip>/.gen_tb_hooks/` exists, run
`python3 scripts/hooks.py normalize <ip_root>`.

## Phase 4: Scaffold

Use `scripts/scaffold.py` with the audit inputs. The generated layout is
fixed; load `references/directory_layout.md` for the authoritative tree.

Key scaffold rules:

- write `script/design.f`, not `rtl/design.f`
- write lowercase `script/makefile`
- write `script/tb.f` for tb-side sources
- always write bash-compatible `script/setup.sh`; when
  `emit_setup_csh: true`, also write `script/setup.csh`
- never copy or modify user RTL
- if `<bus>_vip_source: generate_fresh`, emit `tb/<bus>_agt_top/`
- if `reuse_my_vip`, emit `tb/external_vip.f` and skip fresh agent files
- external VIP reuse is supported only for built-in buses; generic
  mode always generates fresh (no `generic_vip_source: reuse_my_vip`)
- keep `tb_api` generated in all modes
- generate `top/<ip>_tb_top.sv`, `tb/<bus>_if.sv`, tests, audit
- RAL is generated when the configuration has register semantics: i.e.
  built-in slave direction, or generic slave direction with
  `register_semantics: yes`. Master direction in either mode skips
  RAL; generic `register_semantics: no` skips RAL.

For APB generation, load `references/apb.md`. For AHB generation, load
`references/ahb.md`. For AXI4-Lite generation, load
`references/axi_lite.md`. For external VIP reuse, load
`references/apb_external_vip.md`, `references/ahb_external_vip.md`, or
`references/axi_lite_external_vip.md`.
For top wiring, load
`references/top_sv.md`. For Makefile, load
`references/makefile_contract.md`. For `tb_api`, load
`references/tb_api.md`. For DPI, load `references/refm_dpi.md`.

### Generic Bus Branch

When `bus_protocol == generic`:

1. `scripts/scaffold.py` emits the bus-agnostic skeleton it already
   knows: top tree, `script/design.f`, lowercase `script/makefile`,
   `script/tb.f`, test directory, audit dirs, empty
   `tb/<bus>_agt_top/` with placeholder files, and a stub
   `tb/<bus>_if.sv` containing only the ports from
   `bus_handshake.yaml`. RAL is generated iff
   `register_semantics: yes`.
2. Invoke the **scaffold sub-agent** defined in
   `references/sub_agent_generic_scaffold.md`. Inputs:
   - `references/generic_bus.md` (contract)
   - `references/apb.md`, `ahb.md`, `axi_lite.md` (exemplars)
   - `references/directory_layout.md`, `top_sv.md`, `tb_api.md`
   - `bus_handshake.yaml`, `rtl_discovery.yaml`, and
     `registers.yaml` (only if `register_semantics: yes`)
   - the placeholder files from step 1
3. The sub-agent fills in `<bus>_if.sv`, driver, monitor, sequencer,
   sequence library, `tb_api` body, and `top` wiring. Hard
   constraints from §"Hard Constraints" still apply: writes confined
   to `tb/ top/ test/ script/`; no user RTL/VIP/spec/regs edits.
4. Persist:
   - `work/_gen_audit/generic_bus_scaffold_prompt.md` — prompt
     plus the sub-agent's assumption list,
   - `work/_gen_audit/generic_bus_scaffold_diff.patch` — unified
     diff of the sub-agent's writes against the placeholder
     skeleton.

   These are the audit artifacts a future maintainer reads when
   deciding whether to promote this bus to a first-class reference.

At phase end, if `<ip>/.gen_tb_hooks/` exists, run
`python3 scripts/hooks.py scaffold <ip_root>`.

## Phase 5: Compile-Fix

Run:

```bash
make comp
```

If compile fails, save the log under
`work/_gen_audit/compile_fix_attempts/attempt_N.log` and use a
constrained sub-agent. The sub-agent may edit only:

- `tb/`
- `top/`
- `test/`
- `script/`
- `work/_gen_audit/` (audit notes only — never `intake.yaml`,
  `rtl_discovery.yaml`, `bus_handshake.yaml`, or
  `spec_normalized/registers.yaml`)

It may not edit user RTL, user VIP source, specs, or register tables.

For `reuse_my_vip`:

- `import_only`: fix filelist/include/order issues needed to compile
- `drive_with_vip`: additionally create generated glue, interface
  bridge, config_db wiring, and one minimal read/write smoke sequence

Stop after 5 compile attempts in built-in mode, **8 in generic mode**.
Write `unresolved.md` with the last error, likely cause, and next
action. Do not fake success.

In generic mode, additionally load `references/generic_bus.md` and the
three exemplar files (`apb.md`, `ahb.md`, `axi_lite.md`) so the
compile-fix sub-agent can pattern-match against built-in buses. If
attempt N's log is dominated by structural errors in a bus-agent file
(not just typos), the sub-agent may **regenerate the whole file**
instead of patching. Record this in
`compile_fix_attempts/attempt_N.note.md`; it still counts as one
attempt. The sub-agent may also revise the interface clocking block
when a sampling-skew error is the diagnosed root cause. `tb_api`
signatures must not change.

Load `references/sub_agent_compile_fix.md` for the prompt template and
constraints.

At phase end, if `<ip>/.gen_tb_hooks/` exists, run
`python3 scripts/hooks.py compile_fix <ip_root>`.

## Phase 6: Sanity

Run mandatory tests:

```bash
make all SV_CASE=<ip>_sanity_test
make all SV_CASE=<ip>_reg_access_test
```

Sanity must include a positive bus check: read a register with known
non-zero reset when possible; otherwise read register 0 and prove the
DUT responds (`pready` / `hready` / `rvalid`) before timeout. For
AHB-Lite or AXI4-Lite with `bus_direction: master`, the mandatory test
is instead `<ip>_responder_smoke_test`: the slave responder must
observe at least one valid write or read handshake from the DUT within
a timeout. RAL and `<ip>_reg_access_test` are not generated for the
master direction.

In generic mode the mandatory test set depends on
`bus_handshake.yaml.register_semantics`:

- `yes` → `<ip>_sanity_test` + `<ip>_reg_access_test` (RAL-backed
  read of a known reset value if any field has non-zero reset; else
  read offset 0 and prove handshake completes).
- `no` → `<ip>_responder_smoke_test` only (observe ≥1 valid
  handshake under timeout). RAL is not generated.

For generic mode with `direction: master`, the
`<ip>_responder_smoke_test` rule applies regardless of
`register_semantics`.

If a mandatory runtime test fails, re-enter Phase 5 with a runtime-fix
sub-agent for up to 3 attempts in built-in mode, **5 in generic mode**.
Save results to `work/_gen_audit/sanity_result.json` — run
`python3 scripts/compile_and_sanity.py --ip-root <ip> --sanity`, which
compiles, runs every test in `test/sv_list`, and writes that file.

For algorithmic IPs with a reference model, also run one end-to-end
smoke test that proves scoreboard/refmodel integration.

For `drive_with_vip`, also run the generated external-VIP read/write
smoke test.

At phase end, if `<ip>/.gen_tb_hooks/` exists, run
`python3 scripts/hooks.py sanity <ip_root>`.

## Phase 7: Hand-Off

Write:

- `<ip>/CLAUDE.md`
- `<ip>/work/_gen_audit/unresolved.md`
- concise chat summary with exact next command

The summary should state generated IP, tests passed, compile-fix attempt
count, unresolved count, and (in generic mode) `bus_protocol: generic`
plus which exemplars were used and which mandatory test set
(`reg_access` vs `responder_smoke`) was applied. Generated `CLAUDE.md`
in generic mode must additionally carry the manual review checklist
from `references/generic_bus.md`.

The summary's exact next command depends on `intake.yaml: simulators`:

```bash
# VCS (default)
cd <ip>/script && source setup.sh && make all SV_CASE=<ip>_sanity_test

# Questa (when questa is in simulators; with vcs also selected, either works)
cd <ip>/script && source setup.sh && make -f makefile_questa all SV_CASE=<ip>_sanity_test

# xrun (when xrun is in simulators; with vcs also selected, either works)
cd <ip>/script && source setup.sh && make -f makefile_xrun all SV_CASE=<ip>_sanity_test
```

If `intake.yaml` has `emit_setup_csh: true`, also show the tcsh/csh
variant:

```tcsh
cd <ip>/script
source setup.csh
make all SV_CASE=<ip>_sanity_test
```

Load `references/generated_claude_md.md` for `CLAUDE.md`.

At phase end, if `<ip>/.gen_tb_hooks/` exists, run
`python3 scripts/hooks.py handoff <ip_root>`. Run this last so a
notification/dashboard hook sees the final tree.

## Hard Constraints

- Never copy user RTL.
- Never edit user RTL.
- Never edit user VIP source during generation or compile-fix.
- Never write through a symlink that resolves outside the IP root.
- Never silently overwrite without `--force` or backup policy from the
  implementation.
- Never invent registers; RAL is 1:1 from `registers.yaml`.
- Treat TraceWeave MCP, `eda-environment`, and `skill-creator` as
  optional, not hard dependencies.
- If using VCS fails due to license/environment, source the user's shell
  setup if instructed and rerun outside sandbox when needed.

## References

Load only the relevant file for the current phase.

| File | Use |
|---|---|
| `references/directory_layout.md` | generated tree and ownership |
| `references/makefile_contract.md` | makefile API |
| `references/rtl_discovery.md` | RTL discovery schema |
| `references/top_sv.md` | top/interface wiring |
| `references/apb.md` | generated APB agent |
| `references/apb_external_vip.md` | existing APB VIP reuse |
| `references/ahb.md` | generated AHB-Lite agent |
| `references/ahb_external_vip.md` | existing AHB VIP reuse |
| `references/axi_lite.md` | generated AXI4-Lite agent (slave + master directions) |
| `references/axi_lite_external_vip.md` | existing AXI4-Lite VIP reuse |
| `references/spec_parsing.md` | parser rules |
| `references/registers_yaml_schema.md` | normalized registers |
| `references/ral_gen.md` | RAL generation |
| `references/refm_dpi.md` | C/Python DPI |
| `references/tb_api.md` | DE task BFM |
| `references/rtl_stub.md` | generated RTL stub |
| `references/sub_agent_compile_fix.md` | compile-fix sub-agent |
| `references/sub_agent_generic_scaffold.md` | generic-mode scaffold sub-agent |
| `references/generic_bus.md` | generic-bus scaffold contract and review checklist |
| `references/generated_claude_md.md` | generated CLAUDE.md |

## Evaluation

This skill ships with a three-layer eval harness under `evals/`. See
`evals/README.md` for the operator-facing walkthrough; the contract
below is what the skill promises.

1. **Mechanical assertions** (`scripts/run_evals.py run`) —
   compile/sim must exit clean, log substrings must hit, generated
   files must exist. Deterministic, no LLM. Always run after a change
   to the skill or scaffolder. Per-eval artifacts land in
   `evals/iteration-N/<eval-name>/` (`outputs/`, `transcript.md`,
   `assertions_result.json`).

2. **Per-run quality Grader** (`run_evals.py run --grade`) —
   `claude -p` subprocess that reads `evals/agents/grader.md` and
   judges 8 quality dimensions assertions can't catch (scoreboard
   value, RAL fidelity, `tb_api::` BFM usability, hardcoding risk,
   `unresolved.md` honesty, …). Writes `grading.json` per eval with
   `strong/ok/weak/broken` verdicts and severity counts. Always run
   when iterating on the skill.

3. **Optional Comparator + Analyzer** (`run_evals.py compare A B
   --analyze`) — blind A/B between two iterations or candidate
   variants. Most iterations don't need this — mechanical assertions
   plus the Grader catch regressions. Use Comparator when you want a
   stronger statement that "vN is genuinely better than vN-1" (e.g.
   before promoting a major rewrite, or to pick between two candidate
   skill variants). Analyzer runs after Comparator picks a non-tie
   winner and writes `<eval>.analysis.md` with root-cause hypotheses
   and concrete suggested edits to this SKILL.md or `references/`.

The three agent contracts live in `evals/agents/{grader,comparator,
analyzer}.md`. They are written so the same contracts can be invoked
by the harness (`claude -p`) or by a conversational Claude via the
Task tool — pick whichever fits the iteration loop.

**Generic-mode sub-agent gate.** Evals tagged
`requires_generic_sub_agent: true` invoke the scaffold sub-agent
(`references/sub_agent_generic_scaffold.md`) between scaffold and
compile, via a constrained `claude -p` subprocess. This is off by
default — it costs Claude API tokens per run and is non-deterministic.
Enable with `--with-generic-sub-agent` (or env var
`GENTB_EVAL_GENERIC_SUB_AGENT=1`) when iterating on the generic-bus
scaffold contract or before promoting a generic bus to first-class.
If the `claude` CLI is unavailable, the eval is reported as `SKIP`
rather than failed.

## Done Checklist

Items marked *(conditional)* depend on the configuration; only the
applicable ones must hold.

- `<ip>/.prj_top` exists
- symlink guard clean
- `make comp` exits 0
- no dual-driver or structural/procedural driver warnings
- the **mandatory test set for this configuration** all pass:
  - built-in slave direction → `<ip>_sanity_test` (positive bus
    assertion) + `<ip>_reg_access_test`
  - built-in master direction → `<ip>_responder_smoke_test`
  - generic + `register_semantics: yes` (slave) → `<ip>_sanity_test`
    + `<ip>_reg_access_test`
  - generic + `register_semantics: no`, or generic master →
    `<ip>_responder_smoke_test`
- required extra smoke tests pass
- `parse_report.md`, `scaffold_audit.json`, `sanity_result.json`, and
  `unresolved.md` exist
- *(conditional, generic mode)* `bus_handshake.yaml`,
  `generic_bus_scaffold_prompt.md`, and
  `generic_bus_scaffold_diff.patch` exist
- generated `CLAUDE.md` exists (generic mode: includes the manual
  review checklist from `references/generic_bus.md`)
- user receives concise summary and exact next command
