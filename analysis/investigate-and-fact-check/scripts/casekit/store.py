"""Persistent case records, evidence registration, validation, and portable exports.

Use a stable case directory under your control. File digests compare bytes; they
do not establish authenticity or independently protected custody. This module
never opens a network connection or executes instructions found in evidence.
"""

from __future__ import annotations

from contextlib import closing, contextmanager
import csv
from datetime import datetime, timezone
import hashlib
import html
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sqlite3
import stat
import tempfile
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
import uuid
import zipfile


SCHEMA_VERSION = 1
MAX_CHECKPOINT_BYTES = 1024 * 1024 * 1024
MAX_CHECKPOINT_FILES = 10000
MAX_MANIFEST_BYTES = 4 * 1024 * 1024
KINDS = {
    "sources": ("S", "source_id", "source-ledger.csv"),
    "evidence": ("E", "evidence_id", "evidence-log.csv"),
    "claims": ("C", "claim_id", "claim-ledger.csv"),
    "entities": ("N", "entity_id", "entities.csv"),
    "relationships": ("R", "relationship_id", "entity-links.csv"),
    "leads": ("D", "lead_id", "leads.csv"),
    "runs": ("U", "run_id", "runs.csv"),
}
ALIASES = {key.rstrip("s"): key for key in KINDS}
ALIASES.update({"entity": "entities", "evidence": "evidence"})
EXTRA_HEADERS = {
    "entities": ["entity_id", "name", "entity_type", "identifier", "limitations", "duplicate_of", "registered_at_utc"],
    "leads": ["lead_id", "kind", "value", "evidence_id", "source_id", "origin_module", "limitations", "verification_status", "duplicate_of", "registered_at_utc"],
    "runs": ["run_id", "adapter", "status", "started_at_utc", "finished_at_utc", "parameters", "inputs", "outputs", "error"],
}
VERDICTS = {"Supported", "Contradicted", "Misleading", "Mixed", "Unsubstantiated", "Unresolved", "Not fact-checkable"}
SECRET_KEY = re.compile(r"(?:token|secret|password|authorization|cookie|api.?key|access.?key|credential)", re.I)


class CaseError(ValueError):
    """A case input, record, or filesystem condition is invalid."""


def utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def utc_timestamp(value):
    if not isinstance(value, str) or not value.endswith("Z"):
        raise CaseError("UTC timestamps must end in Z.")
    try:
        result = datetime.fromisoformat(value[:-1] + "+00:00")
        if result.utcoffset().total_seconds() != 0:
            raise ValueError("Not UTC")
    except (ValueError, AttributeError) as error:
        raise CaseError("Invalid UTC timestamp.") from error
    return result


def safe_path(value):
    path = Path(os.path.abspath(os.path.expanduser(str(value))))
    for part in (path, *path.parents):
        if part.is_symlink():
            raise CaseError(f"Symlink refused: {part}")
    return path


def safe_name(name):
    if not isinstance(name, str) or not name or "\\" in name or "\x00" in name:
        raise CaseError("Invalid relative path.")
    parts = name.split("/")
    if PurePosixPath(name).is_absolute() or any(p in {"", ".", ".."} or ":" in p for p in parts):
        raise CaseError("Unsafe relative path.")
    for part in parts:
        if part.endswith((".", " ")) or any(ord(char) < 32 for char in part) or re.fullmatch(r"(?i)(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?", part):
            raise CaseError("Checkpoint path is not portable across supported platforms.")
    return name


def fingerprint(path):
    path = safe_path(path)
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    with os.fdopen(os.open(path, flags), "rb") as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode):
            raise CaseError("Only regular files can be registered.")
        digest, length = hashlib.sha256(), 0
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
            length += len(chunk)
        after = os.fstat(stream.fileno())
    identity = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
    if identity(before) != identity(after) or length != after.st_size:
        raise CaseError("File changed during collection; retry with stable originals.")
    return {"sha256": digest.hexdigest(), "bytes": length}


def clean(value):
    """Redact credential-bearing parameters before storing execution records."""
    if isinstance(value, dict):
        return {str(k): "[REDACTED]" if SECRET_KEY.search(str(k)) else clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean(v) for v in value]
    if isinstance(value, str):
        value = re.sub(r"(?i)Bearer\s+[A-Za-z0-9._~+/-]+=*", "Bearer [REDACTED]", value)
        value = re.sub(r"(?i)((?:token|secret|password|api[_-]?key|authorization)=)[^\s&]+", r"\1[REDACTED]", value)
        if value.startswith(("https://", "http://")):
            parts = urlsplit(value)
            host = parts.netloc.rsplit("@", 1)[-1]
            query = [(k, "[REDACTED]" if SECRET_KEY.search(k) else v) for k, v in parse_qsl(parts.query, keep_blank_values=True)]
            value = urlunsplit((parts.scheme, host, parts.path, urlencode(query), parts.fragment))
        return value
    if value is None or isinstance(value, (bool, int, float)):
        return value
    return str(value)


def _kind(kind):
    kind = ALIASES.get(kind, kind)
    if kind not in KINDS:
        raise CaseError(f"Unknown record kind: {kind}")
    return kind


def _refs(value):
    if value is None:
        return []
    if isinstance(value, str):
        return [part.strip() for part in re.split(r"[;,]", value) if part.strip()]
    return list(dict.fromkeys(str(part) for part in value))


def _json(data):
    return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def _write_new(path, data):
    path = safe_path(path)
    if not path.parent.is_dir():
        raise CaseError("Output parent directory must exist.")
    with path.open("xb") as stream:
        stream.write(data)


def _md(value):
    value = html.escape(str(value), quote=True)
    return re.sub(r"([\\`*{}\[\]()#+.!_|>~-])", r"\\\1", value).replace("\r", "").replace("\n", "<br>")


class Case:
    def __init__(self, path):
        self.path = safe_path(path)
        if not self.path.is_dir():
            raise CaseError("Case directory does not exist.")
        metadata = safe_path(self.path / "case.json")
        database = safe_path(self.path / "case.sqlite3")
        if not metadata.is_file() or not database.is_file():
            raise CaseError("Case metadata or database is missing.")
        self.metadata = json.loads(metadata.read_text(encoding="utf-8"))
        if type(self.metadata.get("schema_version")) is not int or self.metadata["schema_version"] != SCHEMA_VERSION:
            raise CaseError("Unsupported case schema_version; migration is required.")
        if not isinstance(self.metadata.get("title"), str) or not self.metadata["title"].strip():
            raise CaseError("Case title is invalid.")
        try:
            uuid.UUID(self.metadata["case_id"])
            utc_timestamp(self.metadata["created_at_utc"])
        except (KeyError, TypeError, ValueError) as error:
            raise CaseError("Case identity or creation timestamp is invalid.") from error
        with self._db(readonly=True) as connection:
            if connection.execute("PRAGMA user_version").fetchone()[0] != SCHEMA_VERSION:
                raise CaseError("Case database schema_version differs from metadata.")

    @classmethod
    def create(cls, path, title):
        destination = safe_path(path)
        if not str(title).strip():
            raise CaseError("Case title is required.")
        if not destination.parent.is_dir():
            raise CaseError("Case parent directory must exist.")
        destination.mkdir(exist_ok=False)
        try:
            for name in ("originals", "derivatives", "analysis", "logs", "publication"):
                (destination / name).mkdir()
            metadata = {"schema_version": SCHEMA_VERSION, "case_id": str(uuid.uuid4()), "title": str(title), "created_at_utc": utc_now()}
            (destination / "case.json").write_text(_json(metadata), encoding="utf-8", newline="\n")
            with closing(sqlite3.connect(destination / "case.sqlite3")) as connection:
                connection.executescript("CREATE TABLE records (kind TEXT NOT NULL, id TEXT NOT NULL PRIMARY KEY, payload TEXT NOT NULL); CREATE TABLE counters (kind TEXT PRIMARY KEY, value INTEGER NOT NULL);")
                connection.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
                connection.commit()
            case = cls(destination)
            (destination / "logs" / "README.txt").write_text("Execution records are authoritative in case.sqlite3 and exported as runs.csv. Credentials are not required for local case operations.\n", encoding="utf-8")
            return case
        except Exception:
            shutil.rmtree(destination)
            raise

    @contextmanager
    def _db(self, readonly=False):
        database = safe_path(self.path / "case.sqlite3")
        connection = sqlite3.connect(database.as_uri() + "?mode=ro" if readonly else str(database), uri=readonly, timeout=10)
        try:
            if not readonly:
                connection.execute("BEGIN IMMEDIATE")
            yield connection
            if not readonly:
                connection.commit()
        except Exception:
            if not readonly:
                connection.rollback()
            raise
        finally:
            connection.close()

    def _insert(self, connection, kind, payload):
        kind = _kind(kind)
        connection.execute("INSERT INTO counters(kind,value) VALUES (?,1) ON CONFLICT(kind) DO UPDATE SET value=value+1", (kind,))
        number = connection.execute("SELECT value FROM counters WHERE kind=?", (kind,)).fetchone()[0]
        record_id = f"{KINDS[kind][0]}{number:03d}"
        result = {**payload, KINDS[kind][1]: record_id}
        connection.execute("INSERT INTO records(kind,id,payload) VALUES (?,?,?)", (kind, record_id, _json(result)))
        return result

    def _require(self, connection, record_id, kind=None):
        row = connection.execute("SELECT kind,payload FROM records WHERE id=?", (record_id,)).fetchone()
        if row is None or (kind is not None and row[0] != _kind(kind)):
            raise CaseError(f"Unknown {kind or 'record'} ID: {record_id}")
        return json.loads(row[1])

    def read_records(self, kind):
        with self._db(readonly=True) as connection:
            rows = connection.execute("SELECT payload FROM records WHERE kind=? ORDER BY length(id),id", (_kind(kind),)).fetchall()
        return [json.loads(row[0]) for row in rows]

    def _headers(self, kind):
        kind = _kind(kind)
        if kind in EXTRA_HEADERS:
            return EXTRA_HEADERS[kind]
        template = Path(__file__).resolve().parents[2] / "assets" / KINDS[kind][2]
        with template.open(encoding="utf-8", newline="") as stream:
            return next(csv.reader(stream))

    def _empty(self, kind):
        return dict.fromkeys(self._headers(kind), "")

    def add_source(self, locator, name="", origin_group="", source_type="", limitations="", derived_from_source_ids=None, **fields):
        if not str(locator).strip():
            raise CaseError("A source locator is required.")
        dependencies = _refs(derived_from_source_ids)
        with self._db() as connection:
            for ref in dependencies:
                self._require(connection, ref, "sources")
            previous = [json.loads(row[0]) for row in connection.execute("SELECT payload FROM records WHERE kind='sources'")]
            duplicate = next((s["source_id"] for s in previous if s["stable_locator"] == str(locator)), "")
            values = self._empty("sources")
            values.update(fields)
            values.update(stable_locator=str(locator), public_name_or_protected_code=name, origin_group=origin_group, source_type=source_type, limitations=limitations, derived_from_source_ids=dependencies, independence_status="unknown", duplicate_of=duplicate, registered_at_utc=utc_now())
            return self._insert(connection, "sources", values)

    def add_evidence(self, file, source_id, method, limitations="", parent_evidence_id="", retrieved_at_utc="", run_id="", **fields):
        original = safe_path(file)
        if retrieved_at_utc:
            utc_timestamp(retrieved_at_utc)
        if not str(method).strip():
            raise CaseError("Evidence collection method is required.")
        digest = fingerprint(original)
        relative = "originals/" + digest["sha256"]
        stored = safe_path(self.path / relative)
        with self._db() as connection:
            source = self._require(connection, source_id, "sources")
            if parent_evidence_id:
                self._require(connection, parent_evidence_id, "evidence")
            if run_id:
                self._require(connection, run_id, "runs")
            previous = [json.loads(row[0]) for row in connection.execute("SELECT payload FROM records WHERE kind='evidence'")]
            duplicate = next((e["evidence_id"] for e in previous if e["sha256"] == digest["sha256"]), "")
            if stored.exists():
                if fingerprint(stored) != digest:
                    raise CaseError("Stored original differs from its digest; case check is required.")
            else:
                try:
                    with original.open("rb") as src, stored.open("xb") as dst:
                        shutil.copyfileobj(src, dst, length=1024 * 1024)
                    if fingerprint(stored) != digest or fingerprint(original) != digest:
                        raise CaseError("Original changed during registration.")
                except Exception:
                    stored.unlink(missing_ok=True)
                    raise
            values = self._empty("evidence")
            values.update(fields)
            values.update(action="registered", logged_at_utc=utc_now(), retrieved_at_utc=retrieved_at_utc, collector="casekit", source_id=source_id, source_locator=source["stable_locator"], relative_file_path=relative, parent_evidence_id=parent_evidence_id, sha256=digest["sha256"], bytes=digest["bytes"], original_filename=original.name, method_and_version=str(method), context_and_limitations=limitations, duplicate_of=duplicate, run_id=run_id)
            result = self._insert(connection, "evidence", values)
            result["log_id"] = "L" + result["evidence_id"][1:]
            connection.execute("UPDATE records SET payload=? WHERE id=?", (_json(result), result["evidence_id"]))
            return result

    def add_claim(self, text, support=None, contradict=None, verdict="Unresolved", confidence="", **fields):
        if not str(text).strip() or verdict not in VERDICTS or confidence.lower() not in {"", "high", "medium", "low"}:
            raise CaseError("Claim text, verdict, or confidence is invalid.")
        support, contradict = _refs(support), _refs(contradict)
        with self._db() as connection:
            groups = set()
            for ref in support + contradict:
                evidence = self._require(connection, ref, "evidence")
                source = self._require(connection, evidence["source_id"], "sources")
                if ref in support and source.get("origin_group"):
                    groups.add(source["origin_group"])
            values = self._empty("claims")
            values.update(fields)
            values.update(exact_claim=str(text), supporting_evidence_ids=support, contradicting_evidence_ids=contradict, origin_groups=sorted(groups), verdict=verdict, confidence=confidence.lower(), as_of_utc=utc_now())
            return self._insert(connection, "claims", values)

    def add_entity(self, name, entity_type="", identifier="", limitations=""):
        if not str(name).strip():
            raise CaseError("Entity name is required.")
        with self._db() as connection:
            previous = [json.loads(row[0]) for row in connection.execute("SELECT payload FROM records WHERE kind='entities'")]
            duplicate = next((n["entity_id"] for n in previous if identifier and n.get("identifier") == identifier and n.get("entity_type") == entity_type), "")
            return self._insert(connection, "entities", {"name": name, "entity_type": entity_type, "identifier": identifier, "limitations": limitations, "duplicate_of": duplicate, "registered_at_utc": utc_now()})

    def add_relationship(self, subject, relationship_type, object, evidence_ids=None, **fields):
        evidence_ids = _refs(evidence_ids)
        if not str(relationship_type).strip():
            raise CaseError("Relationship type is required.")
        with self._db() as connection:
            self._require(connection, subject, "entities")
            self._require(connection, object, "entities")
            for ref in evidence_ids:
                self._require(connection, ref, "evidence")
            values = self._empty("relationships")
            values.update(fields)
            values.update(subject_entity_id=subject, relationship_type=relationship_type, object_entity_id=object, evidence_ids=evidence_ids)
            return self._insert(connection, "relationships", values)

    def add_lead(self, kind, value, evidence_id, source_id, origin_module="", limitations=""):
        if not str(kind).strip() or not str(value).strip():
            raise CaseError("Lead kind and value are required.")
        with self._db() as connection:
            evidence = self._require(connection, evidence_id, "evidence")
            self._require(connection, source_id, "sources")
            if evidence["source_id"] != source_id:
                raise CaseError("Lead source must match the originating evidence.")
            previous = [json.loads(row[0]) for row in connection.execute("SELECT payload FROM records WHERE kind='leads'")]
            duplicate = next((n["lead_id"] for n in previous if n["kind"] == kind and n["value"] == value), "")
            return self._insert(connection, "leads", {"kind": kind, "value": value, "evidence_id": evidence_id, "source_id": source_id, "origin_module": origin_module, "limitations": limitations, "verification_status": "unverified", "duplicate_of": duplicate, "registered_at_utc": utc_now()})

    def start_run(self, adapter, parameters, inputs):
        if not str(adapter).strip():
            raise CaseError("Run adapter is required.")
        with self._db() as connection:
            return self._insert(connection, "runs", {"adapter": str(adapter), "status": "running", "started_at_utc": utc_now(), "finished_at_utc": "", "parameters": clean(parameters), "inputs": clean(inputs), "outputs": [], "error": ""})

    def finish_run(self, run_id, status, outputs, error=""):
        if status not in {"succeeded", "partial", "failed"}:
            raise CaseError("A completed run must be succeeded, partial, or failed.")
        with self._db() as connection:
            result = self._require(connection, run_id, "runs")
            if result["status"] != "running":
                raise CaseError("A completed run cannot be overwritten.")
            result.update(status=status, finished_at_utc=utc_now(), outputs=clean(outputs), error=clean(str(error)))
            connection.execute("UPDATE records SET payload=? WHERE id=?", (_json(result), run_id))
            return result

    def record_run(self, adapter, status, parameters, inputs, outputs, error=""):
        if status not in {"succeeded", "partial", "failed"}:
            raise CaseError("Run status must be succeeded, partial, or failed.")
        result = self.start_run(adapter, parameters, inputs)
        return self.finish_run(result["run_id"], status, outputs, error)

    def status(self):
        records = {kind: self.read_records(kind) for kind in KINDS}
        return {"status": "ready", "case": self.metadata, "counts": {k: len(v) for k, v in records.items()}, "runs": {state: sum(r["status"] == state for r in records["runs"]) for state in ("running", "succeeded", "partial", "failed")}, "duplicate_observations": sum(bool(row.get("duplicate_of")) for rows in records.values() for row in rows)}

    def check(self):
        errors, warnings = [], []
        def issue(collection, code, record, message):
            collection.append({"code": code, "record_id": record, "message": message})
        records = {kind: [] for kind in KINDS}
        by_id = {}
        with self._db(readonly=True) as connection:
            for kind, stored_id, payload in connection.execute("SELECT kind,id,payload FROM records ORDER BY length(id),id"):
                try:
                    row = json.loads(payload)
                except (ValueError, TypeError):
                    issue(errors, "invalid_record", stored_id, "Record payload is not valid JSON.")
                    continue
                if kind not in KINDS or not isinstance(row, dict):
                    issue(errors, "invalid_record", stored_id, "Unknown record kind or malformed payload.")
                    continue
                record_id = row.get(KINDS[kind][1])
                if record_id != stored_id or not re.fullmatch(re.escape(KINDS[kind][0]) + r"[0-9]{3,}", str(record_id)):
                    issue(errors, "record_id_mismatch", stored_id, "Stored ID differs from its payload or kind.")
                    continue
                if record_id in by_id:
                    issue(errors, "duplicate_record_id", stored_id, "Duplicate record ID in payloads.")
                    continue
                records[kind].append(row)
                by_id[record_id] = (kind, row)
            counters = dict(connection.execute("SELECT kind,value FROM counters"))
            for kind, rows in records.items():
                highest = max((int(row[KINDS[kind][1]][1:]) for row in rows), default=0)
                if type(counters.get(kind, 0)) is not int or counters.get(kind, 0) < highest:
                    issue(errors, "invalid_counter", kind, "ID counter is behind existing records.")
        def reference(value, kind, owner):
            if value not in by_id or by_id[value][0] != kind:
                issue(errors, "dangling_reference", owner, f"Missing {kind} reference: {value}")
        for kind, rows in records.items():
            for row in rows:
                record = row[KINDS[kind][1]]
                for field in ("registered_at_utc", "logged_at_utc", "retrieved_at_utc", "checked_at_utc", "as_of_utc", "started_at_utc", "finished_at_utc"):
                    if row.get(field):
                        try:
                            utc_timestamp(row[field])
                        except CaseError:
                            issue(errors, "invalid_timestamp", record, f"Invalid {field}")
                if row.get("duplicate_of"):
                    reference(row["duplicate_of"], kind, record)
        source_edges = {}
        for source in records["sources"]:
            sid = source["source_id"]
            source_edges[sid] = _refs(source.get("derived_from_source_ids"))
            for ref in source_edges[sid]:
                reference(ref, "sources", sid)
            if not source.get("origin_group"):
                issue(warnings, "unknown_independence", sid, "Source origin group is unspecified; independence is unknown.")
        colors = {}
        for source in source_edges:
            stack = [(source, False)]
            while stack:
                node, leaving = stack.pop()
                if leaving:
                    colors[node] = 2
                elif colors.get(node) == 1:
                    issue(errors, "source_dependency_cycle", node, "Source dependency cycle found.")
                elif colors.get(node) != 2:
                    colors[node] = 1
                    stack.append((node, True))
                    stack.extend((child, False) for child in reversed(source_edges.get(node, [])))
        def root_sources(source):
            pending, visited, roots = [source], set(), set()
            while pending:
                node = pending.pop()
                if node in visited:
                    continue
                visited.add(node)
                children = source_edges.get(node, [])
                if children:
                    pending.extend(children)
                else:
                    roots.add(node)
            return roots
        for evidence in records["evidence"]:
            eid = evidence["evidence_id"]
            reference(evidence.get("source_id"), "sources", eid)
            for field, kind in (("parent_evidence_id", "evidence"), ("run_id", "runs")):
                if evidence.get(field):
                    reference(evidence[field], kind, eid)
            try:
                name = safe_name(evidence["relative_file_path"])
                if not name.startswith("originals/"):
                    raise CaseError("Original must be stored in originals/.")
                actual = fingerprint(self.path / name)
                if actual["sha256"] != evidence["sha256"] or actual["bytes"] != evidence["bytes"]:
                    issue(errors, "changed_original", eid, "Stored original differs from its registered bytes.")
            except (CaseError, OSError, KeyError):
                issue(errors, "missing_or_unsafe_original", eid, "Original is missing or has an unsafe path/type.")
        for claim in records["claims"]:
            cid = claim["claim_id"]
            for ref in _refs(claim.get("supporting_evidence_ids")) + _refs(claim.get("contradicting_evidence_ids")):
                reference(ref, "evidence", cid)
            if claim.get("verdict") not in VERDICTS:
                issue(errors, "invalid_verdict", cid, "Unknown claim verdict.")
            if not claim.get("supporting_evidence_ids") and not claim.get("contradicting_evidence_ids"):
                issue(warnings, "claim_without_evidence", cid, "Claim has no registered evidence.")
            roots_by_evidence, groups, seen_hashes = [], set(), set()
            for eid in _refs(claim.get("supporting_evidence_ids")):
                evidence = by_id.get(eid)
                if evidence is None or evidence[0] != "evidence":
                    continue
                digest = evidence[1].get("sha256")
                if digest and digest in seen_hashes:
                    issue(warnings, "duplicate_support_bytes", cid, "Supporting evidence includes repeated bytes. Review the separate observations before counting corroboration.")
                if digest:
                    seen_hashes.add(digest)
                roots = root_sources(evidence[1].get("source_id"))
                roots_by_evidence.append(roots)
                for source_id in roots:
                    source = by_id.get(source_id)
                    group = source[1].get("origin_group") if source and source[0] == "sources" else ""
                    if group:
                        groups.add(group)
                    else:
                        issue(warnings, "unknown_independence", cid, "Supporting source ancestry has an unspecified origin group.")
            if any(left & right for index, left in enumerate(roots_by_evidence) for right in roots_by_evidence[index + 1:]):
                issue(warnings, "dependent_sources", cid, "Supporting evidence shares underlying source ancestry; distinct URLs or labels do not establish corroboration.")
            if claim.get("verdict") == "Supported" and len(groups) < 2:
                issue(warnings, "limited_corroboration", cid, "Fewer than two named origin groups; document any controlling-original exception.")
        for relation in records["relationships"]:
            rid = relation["relationship_id"]
            reference(relation.get("subject_entity_id"), "entities", rid)
            reference(relation.get("object_entity_id"), "entities", rid)
            for ref in _refs(relation.get("evidence_ids")):
                reference(ref, "evidence", rid)
        for lead in records["leads"]:
            reference(lead.get("evidence_id"), "evidence", lead["lead_id"])
            reference(lead.get("source_id"), "sources", lead["lead_id"])
            evidence = by_id.get(lead.get("evidence_id"))
            if evidence and evidence[1].get("source_id") != lead.get("source_id"):
                issue(errors, "lead_source_mismatch", lead["lead_id"], "Lead source differs from evidence source.")
        for run in records["runs"]:
            if run.get("status") not in {"running", "succeeded", "partial", "failed"}:
                issue(errors, "invalid_run_status", run["run_id"], "Unknown run status.")
            if run.get("status") == "running":
                issue(warnings, "unfinished_run", run["run_id"], "Run remains incomplete; review before resuming collection.")
        return {"status": "ok" if not errors else "invalid", "errors": errors, "warnings": warnings, "counts": {k: len(v) for k, v in records.items()}}

    def export(self, output):
        output = safe_path(output)
        if not output.parent.is_dir():
            raise CaseError("Export parent directory must exist.")
        output.mkdir(exist_ok=False)
        try:
            records = {kind: self.read_records(kind) for kind in KINDS}
            (output / "case-records.json").write_text(_json({"case": self.metadata, "records": records}), encoding="utf-8", newline="\n")
            for kind, rows in records.items():
                headers = self._headers(kind)
                with (output / KINDS[kind][2]).open("w", encoding="utf-8", newline="") as stream:
                    writer = csv.DictWriter(stream, fieldnames=headers, extrasaction="ignore", lineterminator="\n")
                    writer.writeheader()
                    for row in rows:
                        values = {}
                        for key in headers:
                            value = row.get(key, "")
                            if isinstance(value, list):
                                value = ";".join(str(v) for v in value)
                            elif isinstance(value, dict):
                                value = json.dumps(value, ensure_ascii=False, sort_keys=True)
                            value = str(value)
                            values[key] = "'" + value if value.startswith(("=", "+", "-", "@", "\t", "\r")) else value
                        writer.writerow(values)
            return {"status": "exported", "output": str(output), "records": sum(len(v) for v in records.values()), "csv_formula_prefix": "Leading spreadsheet formula characters receive an apostrophe; JSON preserves original values."}
        except Exception:
            shutil.rmtree(output)
            raise

    def report(self, output):
        records = {kind: self.read_records(kind) for kind in KINDS}
        checks = self.check()
        lines = [f"# {_md(self.metadata['title'])}", "", f"Case ID: {_md(self.metadata['case_id'])}", "", "Record-based research report. Recorded verdicts and confidence are researcher assertions; this export supplies no editorial or legal approval.", "", "## Claims", ""]
        for claim in records["claims"]:
            lines.extend([
                f"### {claim['claim_id']}: {_md(claim['exact_claim'])}", "",
                f"Scope: {_md(claim.get('scope_and_definitions') or 'not recorded')}.",
                f"Verdict: {_md(claim['verdict'])}. Confidence: {_md(claim.get('confidence') or 'not assigned')}.",
                f"Confidence reason: {_md(claim.get('confidence_reason') or 'not recorded')}.", "",
                f"Supporting evidence: {_md('; '.join(_refs(claim.get('supporting_evidence_ids'))) or 'none registered')}.",
                f"Contrary evidence: {_md('; '.join(_refs(claim.get('contradicting_evidence_ids'))) or 'none registered')}.",
                f"Recorded origin labels: {_md('; '.join(_refs(claim.get('origin_groups'))) or 'unknown')}.",
                f"Unresolved question: {_md(claim.get('unresolved_question') or 'not recorded')}.",
                f"Next check: {_md(claim.get('next_test') or 'not recorded')}.", "",
            ])
        if not records["claims"]:
            lines.extend(["No claims registered.", ""])
        for kind, title, fields in (("evidence", "Evidence", ("evidence_id", "source_id", "relative_file_path", "sha256", "method_and_version", "retrieved_at_utc", "context_and_limitations", "duplicate_of")), ("sources", "Sources", ("source_id", "public_name_or_protected_code", "stable_locator", "origin_group", "derived_from_source_ids", "limitations")), ("entities", "Entities", EXTRA_HEADERS["entities"]), ("relationships", "Relationships", tuple(self._headers("relationships"))), ("leads", "Unverified leads", EXTRA_HEADERS["leads"]), ("runs", "Collection runs", EXTRA_HEADERS["runs"])):
            lines.extend([f"## {title}", ""])
            for row in records[kind]:
                lines.extend(["- " + "; ".join(f"{_md(field)}: {_md(json.dumps(row.get(field), ensure_ascii=False, sort_keys=True) if isinstance(row.get(field), (dict, list)) else row.get(field, ''))}" for field in fields), ""])
            if not records[kind]:
                lines.extend(["None registered.", ""])
        lines.extend(["## Record integrity checks", "", f"Status: {checks['status']}.", ""])
        for level in ("errors", "warnings"):
            for finding in checks[level]:
                lines.append(f"- {level}: {_md(finding['record_id'])}: {_md(finding['message'])}")
        lines.append("")
        _write_new(output, "\n".join(lines).encode("utf-8"))
        return {"status": "reported", "output": str(safe_path(output)), "case_check": checks["status"], "errors": len(checks["errors"]), "warnings": len(checks["warnings"])}

    def checkpoint(self, output):
        output = safe_path(output)
        if output == self.path or self.path in output.parents:
            raise CaseError("Checkpoint output must be outside the case directory.")
        if output.exists() or not output.parent.is_dir():
            raise CaseError("Checkpoint output must be new and its parent must exist.")
        if self.check()["errors"]:
            raise CaseError("Case integrity checks failed; checkpoint was not published.")

        def inventory():
            paths, folded, total = {}, set(), 0
            for directory, dirs, names in os.walk(self.path, followlinks=False):
                for name in sorted(dirs + names):
                    path = Path(directory) / name
                    info = path.lstat()
                    if stat.S_ISLNK(info.st_mode) or not (stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode)):
                        raise CaseError("Checkpoint refuses symlinks and special files.")
                    relative = safe_name(path.relative_to(self.path).as_posix())
                    if relative.casefold() in folded or relative.casefold() == "checkpoint-manifest.json":
                        raise CaseError("Reserved or non-portable duplicate case filename.")
                    folded.add(relative.casefold())
                    if stat.S_ISDIR(info.st_mode):
                        continue
                    if relative in {"case.sqlite3", "case.sqlite3-journal", "case.sqlite3-wal", "case.sqlite3-shm"}:
                        continue
                    total += info.st_size
                    if total > MAX_CHECKPOINT_BYTES or len(paths) >= MAX_CHECKPOINT_FILES - 1:
                        raise CaseError("Checkpoint exceeds the supported file-count or byte limit.")
                    paths[relative] = path
            return paths, total

        paths, total = inventory()
        with tempfile.TemporaryDirectory() as temporary:
            temporary = Path(temporary).resolve()
            database_copy = temporary / "case.sqlite3"
            with self._db(readonly=True) as source, closing(sqlite3.connect(database_copy)) as target:
                source.backup(target)
            if total + database_copy.stat().st_size > MAX_CHECKPOINT_BYTES:
                raise CaseError("Checkpoint exceeds the supported byte limit.")
            paths["case.sqlite3"] = database_copy
            fingerprints = {name: fingerprint(path) for name, path in sorted(paths.items())}
            manifest = {"schema_version": SCHEMA_VERSION, "case_id": self.metadata["case_id"], "files": fingerprints}
            manifest_bytes = _json(manifest).encode("utf-8")
            if len(manifest_bytes) > MAX_MANIFEST_BYTES:
                raise CaseError("Checkpoint manifest exceeds supported size.")
            archive_path = temporary / "checkpoint.zip"
            with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                for name, path in sorted(paths.items()):
                    entry = zipfile.ZipInfo(name, (2020, 1, 1, 0, 0, 0))
                    entry.create_system = 3
                    entry.external_attr = (stat.S_IFREG | 0o644) << 16
                    entry.compress_type = zipfile.ZIP_DEFLATED
                    digest, length = hashlib.sha256(), 0
                    with safe_path(path).open("rb") as source, archive.open(entry, "w") as target:
                        for chunk in iter(lambda: source.read(1024 * 1024), b""):
                            length += len(chunk)
                            if length > fingerprints[name]["bytes"]:
                                raise CaseError("Case file changed during checkpoint.")
                            digest.update(chunk)
                            target.write(chunk)
                    if length != fingerprints[name]["bytes"] or digest.hexdigest() != fingerprints[name]["sha256"] or fingerprint(path) != fingerprints[name]:
                        raise CaseError("Case file changed during checkpoint.")
                archive.writestr("checkpoint-manifest.json", manifest_bytes, compress_type=zipfile.ZIP_DEFLATED)
            current, _ = inventory()
            if set(current) != set(paths) - {"case.sqlite3"}:
                raise CaseError("Case inventory changed during checkpoint.")
            # Verify the captured database and originals together before exposing a
            # successful checkpoint. This also checks concurrent database changes
            # cannot leave a published snapshot with dangling original references.
            Case.restore(archive_path, temporary / "validation-case")
            created = False
            try:
                with archive_path.open("rb") as source, output.open("xb") as target:
                    created = True
                    shutil.copyfileobj(source, target, length=1024 * 1024)
            except BaseException:
                if created:
                    output.unlink(missing_ok=True)
                raise
        return {"status": "checkpointed", "output": str(output), "files": len(paths), "sha256": fingerprint(output)["sha256"]}

    @classmethod
    def restore(cls, archive_path, destination):
        archive_path, destination = safe_path(archive_path), safe_path(destination)
        if destination.exists() or not destination.parent.is_dir():
            raise CaseError("Restore destination must be new and its parent must exist.")
        with zipfile.ZipFile(archive_path) as archive:
            entries = archive.infolist()
            if len(entries) > MAX_CHECKPOINT_FILES + 1 or sum(e.file_size for e in entries) > MAX_CHECKPOINT_BYTES + 1024 * 1024:
                raise CaseError("Checkpoint exceeds supported restore limits.")
            names, casefold = set(), set()
            for entry in entries:
                name = safe_name(entry.filename)
                mode = entry.external_attr >> 16
                if name in names or name.casefold() in casefold or entry.is_dir() or (stat.S_IFMT(mode) not in {0, stat.S_IFREG}):
                    raise CaseError("Duplicate, non-regular, or incompatible checkpoint entry.")
                names.add(name)
                casefold.add(name.casefold())
            if "checkpoint-manifest.json" not in names:
                raise CaseError("Checkpoint manifest is missing.")
            if archive.getinfo("checkpoint-manifest.json").file_size > MAX_MANIFEST_BYTES:
                raise CaseError("Checkpoint manifest exceeds supported size.")
            def unique_pairs(pairs):
                result = {}
                for key, value in pairs:
                    if key in result:
                        raise CaseError("Duplicate checkpoint manifest key.")
                    result[key] = value
                return result
            manifest = json.loads(archive.read("checkpoint-manifest.json"), object_pairs_hook=unique_pairs)
            if not isinstance(manifest, dict):
                raise CaseError("Checkpoint manifest must be a JSON object.")
            expected = manifest.get("files")
            if type(manifest.get("schema_version")) is not int or manifest["schema_version"] != SCHEMA_VERSION or not isinstance(expected, dict) or set(expected) != names - {"checkpoint-manifest.json"} or not {"case.json", "case.sqlite3"}.issubset(expected):
                raise CaseError("Checkpoint manifest inventory is invalid.")
            for name, entry in expected.items():
                safe_name(name)
                if not isinstance(entry, dict) or type(entry.get("bytes")) is not int or entry["bytes"] < 0 or not re.fullmatch(r"[0-9a-f]{64}", str(entry.get("sha256"))):
                    raise CaseError("Invalid checkpoint fingerprint.")
                if archive.getinfo(name).file_size != entry["bytes"]:
                    raise CaseError("Checkpoint entry size differs from its manifest.")
            destination.mkdir(exist_ok=False)
            try:
                for name in sorted(expected):
                    target = destination / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    digest, length = hashlib.sha256(), 0
                    with archive.open(name) as src, target.open("xb") as dst:
                        for chunk in iter(lambda: src.read(1024 * 1024), b""):
                            length += len(chunk)
                            if length > expected[name]["bytes"]:
                                raise CaseError("Checkpoint entry exceeds its declared length.")
                            digest.update(chunk)
                            dst.write(chunk)
                    if length != expected[name]["bytes"] or digest.hexdigest() != expected[name]["sha256"]:
                        raise CaseError("Checkpoint content differs from its manifest.")
                for name in ("originals", "derivatives", "analysis", "logs", "publication"):
                    (destination / name).mkdir(exist_ok=True)
                restored = cls(destination)
                if restored.metadata["case_id"] != manifest.get("case_id"):
                    raise CaseError("Checkpoint case ID differs from metadata.")
                check = restored.check()
                if check["errors"]:
                    raise CaseError("Restored case fails record or evidence integrity checks.")
                return restored
            except Exception:
                shutil.rmtree(destination)
                raise
