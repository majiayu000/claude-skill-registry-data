#!/usr/bin/env python3
"""Manage a local investigation case with optional, explicitly invoked collectors."""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import zipfile

from casekit import Case, CaseError


def _case(args):
    return Case(args.case)


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    top = parser.add_subparsers(dest="command", required=True)
    case = top.add_parser("case", help="Create, validate, export, and checkpoint cases.")
    commands = case.add_subparsers(dest="operation", required=True)
    init = commands.add_parser("init", help="Create a new case; existing paths are refused.")
    init.add_argument("path")
    init.add_argument("--title", required=True)
    init.set_defaults(func=lambda a: Case.create(a.path, a.title).status())
    for name in ("status", "check"):
        command = commands.add_parser(name)
        command.add_argument("case")
        command.set_defaults(func=lambda a, name=name: getattr(_case(a), name)())
    for name in ("report", "export", "checkpoint"):
        command = commands.add_parser(name)
        command.add_argument("case")
        command.add_argument("--output", required=True)
        command.set_defaults(func=lambda a, name=name: getattr(_case(a), name)(a.output))
    restore = commands.add_parser("restore", help="Restore a verified checkpoint to a new directory.")
    restore.add_argument("archive")
    restore.add_argument("destination")
    restore.set_defaults(func=lambda a: Case.restore(a.archive, a.destination).status())

    source = top.add_parser("source", help="Register source provenance, not a truth verdict.")
    commands = source.add_subparsers(dest="operation", required=True)
    add = commands.add_parser("add")
    add.add_argument("--case", required=True)
    add.add_argument("--locator", required=True)
    add.add_argument("--name", default="")
    add.add_argument("--origin-group", default="")
    add.add_argument("--type", default="", dest="source_type")
    add.add_argument("--limitations", default="")
    add.add_argument("--derived-from", action="append", default=[])
    add.set_defaults(func=lambda a: _case(a).add_source(a.locator, a.name, a.origin_group, a.source_type, a.limitations, a.derived_from))

    evidence = top.add_parser("evidence", help="Copy originals and register distinct observations.")
    commands = evidence.add_subparsers(dest="operation", required=True)
    add = commands.add_parser("add")
    add.add_argument("--case", required=True)
    add.add_argument("--file", required=True)
    add.add_argument("--source-id", required=True)
    add.add_argument("--method", default="local-file-registration/1")
    add.add_argument("--limitations", default="")
    add.add_argument("--parent-evidence-id", default="")
    add.add_argument("--retrieved-at-utc", default="")
    add.add_argument("--run-id", default="")
    add.set_defaults(func=lambda a: _case(a).add_evidence(a.file, a.source_id, a.method, a.limitations, a.parent_evidence_id, a.retrieved_at_utc, a.run_id))

    claim = top.add_parser("claim", help="Record a researcher's scoped claim assessment.")
    commands = claim.add_subparsers(dest="operation", required=True)
    add = commands.add_parser("add")
    add.add_argument("--case", required=True)
    add.add_argument("--text", required=True)
    add.add_argument("--support", action="append", default=[])
    add.add_argument("--contradict", action="append", default=[])
    add.add_argument("--verdict", default="Unresolved")
    add.add_argument("--confidence", default="")
    add.add_argument("--confidence-reason", default="")
    add.add_argument("--scope", default="")
    add.add_argument("--unresolved-question", default="")
    add.add_argument("--next-test", default="")
    add.set_defaults(func=lambda a: _case(a).add_claim(a.text, a.support, a.contradict, a.verdict, a.confidence, confidence_reason=a.confidence_reason, scope_and_definitions=a.scope, unresolved_question=a.unresolved_question, next_test=a.next_test))

    entity = top.add_parser("entity")
    commands = entity.add_subparsers(dest="operation", required=True)
    add = commands.add_parser("add")
    add.add_argument("--case", required=True)
    add.add_argument("--name", required=True)
    add.add_argument("--type", dest="entity_type", default="")
    add.add_argument("--identifier", default="")
    add.add_argument("--limitations", default="")
    add.set_defaults(func=lambda a: _case(a).add_entity(a.name, a.entity_type, a.identifier, a.limitations))

    relation = top.add_parser("relationship")
    commands = relation.add_subparsers(dest="operation", required=True)
    add = commands.add_parser("add")
    add.add_argument("--case", required=True)
    add.add_argument("--subject", required=True)
    add.add_argument("--type", dest="relationship_type", required=True)
    add.add_argument("--object", required=True)
    add.add_argument("--evidence", action="append", default=[])
    add.add_argument("--limitations", default="")
    add.add_argument("--basis", choices=("directly_documented", "inferred"), default="inferred")
    add.set_defaults(func=lambda a: _case(a).add_relationship(a.subject, a.relationship_type, a.object, a.evidence, limitations=a.limitations, directly_documented_or_inferred=a.basis))

    records = top.add_parser("records", help="Read case records as JSON.")
    records.add_argument("--case", required=True)
    records.add_argument("kind", choices=("sources", "evidence", "claims", "entities", "relationships", "leads", "runs"))
    records.set_defaults(func=lambda a: {"status": "read", "kind": a.kind, "records": _case(a).read_records(a.kind)})

    # The core remains offline; integration commands must be explicitly selected.
    from casekit.integration import register_commands
    register_commands(top)
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = args.func(args)
        print(json.dumps(result, ensure_ascii=True, sort_keys=True))
        return 1 if result.get("status") in {"invalid", "failed", "partial"} else 0
    except (CaseError, OSError, ValueError, sqlite3.Error, zipfile.BadZipFile) as error:
        print(json.dumps({"status": "error", "error": str(error)}, ensure_ascii=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
