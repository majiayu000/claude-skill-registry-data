"""Register collector outputs as evidence and unverified leads in a case.

Provider responses and imported exports remain original artifacts. Their rows
are discovery leads, not verified claims or independent corroboration.
"""

from __future__ import annotations

from pathlib import Path
import tempfile

from .connectors import ADAPTERS, collect, parse_recon_export
from .store import Case


def _artifact_name(value):
    if not isinstance(value, str) or not value or Path(value).name != value or "\\" in value or value in {".", ".."}:
        raise ValueError("Collector artifact names must be simple filenames")
    return value


def _register_result(case, result, run_id):
    artifacts = {}
    source_ids, evidence_ids, lead_ids = [], [], []
    limitations = list(result.limitations)
    metadata = getattr(result, "metadata", {})
    adapter_version = metadata.get("version", "unknown")
    try:
        with tempfile.TemporaryDirectory(prefix="fact-check-collection-") as temporary:
            staging = Path(temporary).resolve()
            for artifact in result.artifacts:
                name = _artifact_name(artifact.name)
                if name in artifacts:
                    raise ValueError("Collector returned duplicate artifact names")
                path = staging / name
                path.write_bytes(artifact.data)
                locator = artifact.source_url or f"recon-ng-export:sha256:{artifact.sha256}"
                cached = bool(artifact.from_cache)
                notes = [f"Adapter: {result.adapter}; raw response or supplied export, not independent verification."]
                if cached:
                    notes.append(f"Cached bytes; fetched at {artifact.retrieved_at_utc or 'unknown'}, reused at {artifact.observed_at_utc or 'unknown'}.")
                if getattr(artifact, "truncated", False):
                    notes.append("Response truncated at the byte limit; this artifact is not the complete response.")
                source = case.add_source(
                    locator=locator,
                    name=f"{result.adapter}: {result.input_value}",
                    origin_group=f"collector:{result.adapter}",
                    source_type="local-export" if result.adapter == "recon-ng-import" else "api-response",
                    limitations=" ".join(notes),
                )
                source_ids.append(source["source_id"])
                evidence = case.add_evidence(
                    file=path,
                    source_id=source["source_id"],
                    method=f"case-tool/1.1.0 adapter={result.adapter}@{adapter_version}",
                    limitations=" ".join(notes),
                    retrieved_at_utc=artifact.retrieved_at_utc or "",
                    run_id=run_id,
                )
                evidence_ids.append(evidence["evidence_id"])
                artifacts[name] = (evidence["evidence_id"], source["source_id"])
            for observation in result.observations:
                parent = artifacts.get(observation.get("artifact_name"))
                if parent is None:
                    raise ValueError("Collector observation has no corresponding original artifact")
                details = observation.get("limitations", "")
                if isinstance(details, list):
                    details = "; ".join(str(item) for item in details)
                provenance = observation.get("provenance_status", "unverified")
                duplicate = observation.get("duplicate_of")
                notes = f"Unverified discovery lead. Provenance: {provenance}. {details}"
                if duplicate is not None:
                    notes += f" Duplicate candidate of observation {duplicate}; retained as a separate observation."
                lead = case.add_lead(
                    kind=observation["kind"],
                    value=observation["value"],
                    evidence_id=parent[0],
                    source_id=parent[1],
                    origin_module=observation.get("origin_module", ""),
                    limitations=notes.strip(),
                )
                lead_ids.append(lead["lead_id"])
        outputs = {"source_ids": source_ids, "evidence_ids": evidence_ids, "lead_ids": lead_ids,
                   "requests": result.requests, "limitations": limitations,
                   "adapter_metadata": metadata,
                   "observations": result.observations,
                   "artifacts": [{"name": item.name, "source_url": item.source_url,
                                  "sha256": item.sha256, "http_status": item.http_status,
                                  "retrieved_at_utc": item.retrieved_at_utc,
                                  "observed_at_utc": item.observed_at_utc,
                                  "from_cache": item.from_cache,
                                  "truncated": bool(getattr(item, "truncated", False))}
                                 for item in result.artifacts]}
        run = case.finish_run(run_id, status=result.status, outputs=outputs, error=result.error or "")
        return {
            "status": result.status,
            "run_id": run["run_id"],
            "adapter": result.adapter,
            **outputs,
            "requests": result.requests,
            "limitations": limitations,
            "error": result.error or "",
        }
    except Exception as error:
        case.finish_run(
            run_id,
            status="partial" if evidence_ids else "failed",
            outputs={"source_ids": source_ids, "evidence_ids": evidence_ids, "lead_ids": lead_ids,
                     "requests": result.requests, "limitations": limitations},
            error=str(error),
        )
        raise


def run_collection(case_path, adapter, input_value, *, refresh=False, token_env=None, timeout=10, max_pages=3, use_cache=True):
    case_path = Path(case_path)
    case = Case(case_path)
    parameters = {"input": input_value, "refresh": bool(refresh), "timeout": timeout, "max_pages": max_pages, "cache_enabled": bool(use_cache)}
    run = case.start_run(adapter=adapter, parameters=parameters, inputs=[input_value])
    try:
        result = collect(
            adapter, input_value,
            cache_dir=case_path / "analysis" / "collector-cache" if use_cache else None,
            refresh=refresh, token_env=token_env, timeout=timeout, max_pages=max_pages,
        )
    except Exception as error:
        case.finish_run(run["run_id"], status="failed", outputs={}, error=str(error))
        raise
    return _register_result(case, result, run["run_id"])


def import_recon(case_path, export_path, *, table=None):
    case = Case(case_path)
    run = case.start_run(adapter="recon-ng-import", parameters={"table": table}, inputs=[Path(export_path).name])
    try:
        result = parse_recon_export(export_path, table=table)
    except Exception as error:
        case.finish_run(run["run_id"], status="failed", outputs={}, error=str(error))
        raise
    return _register_result(case, result, run["run_id"])


def register_commands(subparsers):
    collect_parser = subparsers.add_parser("collect", help="List or explicitly run optional public-source adapters")
    collection = collect_parser.add_subparsers(dest="collection_command", required=True)
    listing = collection.add_parser("list", help="Show adapter requirements and coverage limits")
    listing.set_defaults(func=lambda args: {"adapters": ADAPTERS})
    run = collection.add_parser("run", help="Collect public provider responses into a case as unverified leads")
    run.add_argument("--case", required=True, type=Path)
    run.add_argument("--adapter", required=True)
    run.add_argument("--input", required=True)
    run.add_argument("--refresh", action="store_true", help="Request fresh responses instead of reusing cached bytes")
    run.add_argument("--no-cache", action="store_true")
    run.add_argument("--token-env", help="Explicit environment variable name for an optional GitHub token")
    run.add_argument("--timeout", type=float, default=10)
    run.add_argument("--max-pages", type=int, default=3)
    run.set_defaults(func=lambda args: run_collection(args.case, args.adapter, args.input, refresh=args.refresh, token_env=args.token_env, timeout=args.timeout, max_pages=args.max_pages, use_cache=not args.no_cache))
    recon = subparsers.add_parser("recon", help="Import a supplied Recon-ng export without running Recon-ng")
    imports = recon.add_subparsers(dest="recon_command", required=True)
    load = imports.add_parser("import", help="Preserve an export and register selected rows as unverified leads")
    load.add_argument("--case", required=True, type=Path)
    load.add_argument("--file", required=True, type=Path)
    load.add_argument("--table", choices=("domains", "hosts", "repositories"), help="Required for CSV; optional table selection for JSON")
    load.set_defaults(func=lambda args: import_recon(args.case, args.file, table=args.table))
