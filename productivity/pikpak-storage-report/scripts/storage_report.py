#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PikPak 空间体检：目录体积排行 + 大文件清单（只读；不执行删除）。

用法：
  python3 storage_report.py --folder "" --depth 2
  python3 storage_report.py --folder "" --top 30
  python3 storage_report.py --folder "" --json report.json
  python3 storage_report.py --from-fixture dev/fixtures/sample_tree.json --folder ""

环境变量：
  PIKPAK_BIN      pikpak 可执行文件路径（默认 "pikpak"）
  PIKPAK_TIMEOUT  单次 ls 超时秒数（默认 90）
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import stat
import subprocess
import sys
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime
from typing import NoReturn


def die(msg: str, code: int = 1) -> NoReturn:
    print(f"错误：{msg}", file=sys.stderr)
    raise SystemExit(code)


def to_int(value) -> int:
    if value is None:
        return 0
    m = re.search(r"\d+", str(value))
    return int(m.group(0)) if m else 0


def byte_size(value):
    """Unknown/invalid byte counts must not become a convincing zero."""
    if isinstance(value, bool):
        return None
    if isinstance(value, int) and value >= 0:
        return value
    if isinstance(value, str) and re.fullmatch(r"[0-9]+", value):
        return int(value)
    return None


def human_size(n: int) -> str:
    if n <= 0:
        return "0 B"
    units = ("B", "KB", "MB", "GB", "TB")
    i = 0
    try:
        value = float(n)
    except OverflowError:
        raise ScanError("字节大小超出当前展示范围；报告未完成。", code="INVALID_METADATA") from None
    while value >= 1024 and i < len(units) - 1:
        value /= 1024.0
        i += 1
    return f"{value:.0f} {units[i]}" if i == 0 else f"{value:.1f} {units[i]}"


MAX_PAGES = 10000
MAX_DEPTH = 100
LIVE = object()  # Never confuse JSON null with an omitted --from-fixture.


class ScanError(RuntimeError):
    def __init__(self, message, truncated=False, code="SCAN_FAILED", cli_exit_code=None):
        super().__init__(message)
        self.truncated = truncated
        self.code = code
        self.cli_exit_code = cli_exit_code


def optional_time(value):
    if value is None or value == "":
        return ""
    if not isinstance(value, str):
        raise ScanError("可选时间必须为 ISO 字符串或 null。", code="INVALID_METADATA")
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise ScanError("可选时间不是有效 ISO 时间。", code="INVALID_METADATA") from None
    return value


def validate_page(page):
    if (not isinstance(page, dict)
            or any(key in page for key in ("error", "errors", "error_code",
                                           "error_description", "error_message", "code"))
            or ("ok" in page and page["ok"] is not True)
            or ("success" in page and page["success"] is not True)
            or not isinstance(page.get("files"), list)
            or (page.get("next_page_token") is not None
                and not isinstance(page.get("next_page_token"), str))):
        raise ScanError("目录响应结构无效；不能视为空目录")
    files = []
    for entry in page["files"]:
        if (not isinstance(entry, dict) or not isinstance(entry.get("id"), str)
                or not entry["id"] or not isinstance(entry.get("name"), str)
                or entry.get("kind") not in ("drive#file", "drive#folder")):
            raise ScanError("目录条目缺少有效 ID/name/kind；扫描未完成")
        if ((entry.get("params") is not None and not isinstance(entry["params"], dict))
                or (entry.get("hash") is not None and not isinstance(entry["hash"], str))):
            raise ScanError("目录条目 params/hash 类型无效；扫描未完成")
        files.append({**entry, "modified_time": optional_time(entry.get("modified_time")),
                      "created_time": optional_time(entry.get("created_time"))})
    return {**page, "files": files}


MAX_JSON_BYTES = 16 * 1024 * 1024
MAX_JSON_DEPTH = 64  # Counts object/array containers, including the root.


def read_json_bytes(path):
    """No special streams/links; ordinary neutral 0644 inputs remain valid."""
    fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW)
    try:
        info = os.fstat(fd)
        if (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1
                or info.st_uid != os.geteuid() or info.st_mode & 0o022):
            raise ValueError("unsafe JSON input")
        if info.st_size > MAX_JSON_BYTES:
            raise ValueError("JSON byte limit")
        chunks, total = [], 0
        while True:
            chunk = os.read(fd, min(65536, MAX_JSON_BYTES + 1 - total))
            if not chunk:
                return b"".join(chunks)
            chunks.append(chunk)
            total += len(chunk)
            if total > MAX_JSON_BYTES:
                raise ValueError("JSON byte limit")
    finally:
        os.close(fd)


def parse_json(raw, code):
    """Bound bytes and lexical nesting BEFORE the recursive JSON decoder."""
    try:
        if len(raw) > MAX_JSON_BYTES:
            raise ValueError("JSON byte limit")
        if isinstance(raw, str):
            if len(raw.encode("utf-8")) > MAX_JSON_BYTES:
                raise ValueError("JSON byte limit")
            text = raw
        else:
            text = raw.decode("utf-8")
        depth, quoted, escaped = 0, False, False
        for char in text:
            if quoted:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    quoted = False
            elif char == '"':
                quoted = True
            elif char in "[{":
                depth += 1
                if depth > MAX_JSON_DEPTH:
                    raise ValueError("JSON depth limit")
            elif char in "]}":
                depth -= 1
        return json.loads(text)
    except (UnicodeError, ValueError, RecursionError):
        raise ScanError(f"{code}；JSON 无效或超过字节/嵌套深度上限。", code=code) from None


def write_report(path, text):
    """Write only a private regular report file after checking its link count."""
    fd = None
    try:
        flags = os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK
        fd = os.open(path, flags, 0o600)
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise OSError("unsafe report target")
        os.fchmod(fd, 0o600)
        os.ftruncate(fd, 0)
        stream = os.fdopen(fd, "w", encoding="utf-8")
        fd = None
        with stream:
            stream.write(text)
    finally:
        if fd is not None:
            os.close(fd)


def abort_scan(args, counters, exc):
    report = {
        "complete": False, "truncated": exc.truncated, "errors": [str(exc)],
        "error_code": exc.code, "cli_exit_code": exc.cli_exit_code,
        "identity_conflict": exc.code == "IDENTITY_CONFLICT",
        "folder": args.folder, "source": "fixture" if args.from_fixture is not None else "live",
        "scanned_files": counters["files"], "scanned_folders": counters["folders"],
    }
    if args.json_out is not None:
        text = json.dumps(report, ensure_ascii=False, indent=2)
        if args.json_out == "-":
            print(text)
        else:
            try:
                write_report(args.json_out, text)
            except (OSError, UnicodeError, ValueError):
                report["original_error_code"] = exc.code
                report["error_code"] = "REPORT_WRITE_FAILED"
                report["errors"] = ["REPORT_WRITE_FAILED；目标未能更新，不得使用旧报告。"]
                print(json.dumps(report, ensure_ascii=False, indent=2))
                print("REPORT_WRITE_FAILED；失败 JSON 改送 stdout；不要使用旧报告。", file=sys.stderr)
    print(f"扫描未完成：{exc}；不提供清理命令或完整统计。", file=sys.stderr)
    raise SystemExit(2)


def ls_page(folder_id: str, fixture, page_token: str = "") -> dict:
    """Only the private LIVE sentinel permits a CLI read."""
    if fixture is not LIVE:
        node = fixture.get(folder_id) if isinstance(fixture, dict) else None
        if not isinstance(node, dict) or page_token not in node:
            raise ScanError("fixture 缺少所请求的目录/分页；扫描未完成")
        return validate_page(node[page_token])

    cmd = [os.environ.get("PIKPAK_BIN", "pikpak"), "ls", "--raw", "-l", "500"]
    if folder_id:
        cmd += ["-p", folder_id]
    if page_token:
        cmd += ["-t", page_token]
    timeout = timeout_seconds()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except FileNotFoundError:
        raise ScanError("找不到只读 CLI；请独立检查安装。", code="CLI_UNAVAILABLE") from None
    except subprocess.TimeoutExpired:
        raise ScanError(f"pikpak ls 超时（{timeout}s），请检查网络后重试。")
    if proc.returncode != 0:
        # CLI streams may contain credentials or signed URLs. Never echo them.
        raise ScanError(f"CLI_FAILED (exit_code={proc.returncode})；请独立检查 CLI/授权状态。",
                        code="CLI_FAILED", cli_exit_code=proc.returncode)
    return validate_page(parse_json(proc.stdout, "INVALID_CLI_JSON"))


class Node:
    """目录树节点。"""

    def __init__(self, name: str, fid: str):
        self.name = name
        self.id = fid
        self.size = 0
        self.file_count = 0
        self.unknown_size_files = 0
        self.children: list["Node"] = []
        self.files: list[dict] = []

    def to_dict(self):
        return {
            "name": self.name,
            "id": self.id,
            "size": self.size,
            "size_h": human_size(self.size),
            "file_count": self.file_count,
            "unknown_size_files": self.unknown_size_files,
            "size_complete": self.unknown_size_files == 0,
            "children": [c.to_dict() for c in self.children],
        }


def register_identity(entry, counters):
    """Deduplicate only identical identity/evidence, across files AND folders."""
    index = counters.setdefault("_identities", {})
    identity = json.dumps({key: entry.get(key) for key in (
        "kind", "name", "size", "hash", "params", "modified_time", "created_time"
    )}, sort_keys=True, ensure_ascii=False)
    fid = entry["id"]
    if fid in index:
        if index[fid] != identity:
            raise ScanError("identity_conflict：同一 ID 的身份/证据冲突；整份报告禁止清理。",
                            code="IDENTITY_CONFLICT")
        return False
    index[fid] = identity
    return True


def walk_tree(folder_id: str, fixture, name: str, counters, max_items: int) -> Node:
    node = Node(name, folder_id)
    active = counters.setdefault("_active", set())
    if folder_id in active:
        raise ScanError("发现目录环；扫描未完成")
    if len(active) >= MAX_DEPTH:
        raise ScanError(f"目录深度超过安全上限（{MAX_DEPTH}）", truncated=True)
    active.add(folder_id)

    tokens = set()
    token = ""
    while True:
        if token in tokens:
            raise ScanError("分页 token 循环；扫描未完成")
        tokens.add(token)
        if counters.get("_pages", 0) >= MAX_PAGES:
            raise ScanError(f"页数超过安全上限（{MAX_PAGES}）", truncated=True)
        counters["_pages"] = counters.get("_pages", 0) + 1
        page = ls_page(folder_id, fixture, token)
        for f in page.get("files", []):
            kind = f.get("kind")
            if kind == "drive#file" and f["id"] in active:
                raise ScanError("identity_conflict：目录 ID 同时用作文件；整份报告禁止清理。",
                                code="IDENTITY_CONFLICT")
            if kind == "drive#folder" and f["id"] in active:
                raise ScanError("发现目录环；扫描未完成")
            if not register_identity(f, counters):
                continue
            if kind == "drive#folder":
                if counters["folders"] >= 5000:
                    raise ScanError("目录数量超过安全上限（5000）", truncated=True)
                counters["folders"] += 1
                child = walk_tree(f.get("id", ""), fixture, f.get("name", ""), counters, max_items)
                node.size += child.size
                node.file_count += child.file_count
                node.unknown_size_files += child.unknown_size_files
                node.children.append(child)
            elif kind == "drive#file":
                if counters["files"] >= max_items:
                    raise ScanError(f"文件数量超过安全上限（{max_items}）", truncated=True)
                counters["files"] += 1
                size = byte_size(f.get("size"))
                node.unknown_size_files += size is None
                node.size += size or 0
                node.file_count += 1
                node.files.append({
                    "id": f.get("id", ""),
                    "name": f.get("name", ""),
                    "size": size,
                    "size_h": human_size(size) if size is not None else "未知",
                    "modified": f.get("modified_time", ""),
                })
        token = page.get("next_page_token", "") or ""
        if not token:
            break
    active.remove(folder_id)
    return node


def collect_files(node: Node, rel_path: list[str], out: list[dict]):
    for f in node.files:
        out.append({**f, "path": "/".join(rel_path + [f["name"]])})
    for c in node.children:
        collect_files(c, rel_path + [c.name], out)


def print_tree(node: Node, depth: int, max_depth: int, indent: int = 0, file=None):
    pad = "  " * indent
    print(f"{pad}{human_size(node.size):>10}  {node.name} ({node.file_count} 文件)", file=file)
    if indent < max_depth:
        for c in sorted(node.children, key=lambda n: n.size, reverse=True):
            print_tree(c, depth + 1, max_depth, indent + 1, file=file)


class ScanArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        # argparse's message may contain raw user data; keep diagnostics stable.
        raise ScanError("INVALID_ARGUMENTS；请检查命令参数及非负/正整数范围。", code="INVALID_ARGUMENTS")


def failure_context(argv):
    args = argparse.Namespace(folder="", from_fixture=None, json_out=None)
    fields = {"--folder": "folder", "--from-fixture": "from_fixture", "--json": "json_out"}
    for index, arg in enumerate(argv):
        if arg == "--":
            break
        key, sep, value = arg.partition("=")
        if key in fields:
            if not sep and index + 1 < len(argv) and not argv[index + 1].startswith("--"):
                value = argv[index + 1]
            elif not sep:
                continue
            setattr(args, fields[key], value)
    return args


def timeout_seconds():
    raw = os.environ.get("PIKPAK_TIMEOUT", "90")
    if not re.fullmatch(r"[0-9]{1,6}", raw) or not 1 <= int(raw) <= 86400:
        raise ScanError("INVALID_CONFIG；PIKPAK_TIMEOUT 必须为 1–86400 的整数秒数。", code="INVALID_CONFIG")
    return int(raw)


def load_fixture(path):
    if path is None:
        return LIVE
    try:
        fixture = parse_json(read_json_bytes(path), "INVALID_FIXTURE")
    except (OSError, UnicodeError, ValueError):
        raise ScanError("INVALID_FIXTURE；无法读取有效的 UTF-8 JSON fixture；禁止回退云端。", code="INVALID_FIXTURE") from None
    if not isinstance(fixture, dict):
        raise ScanError("INVALID_FIXTURE；顶层必须是对象；禁止回退云端。", code="INVALID_FIXTURE")
    return fixture


def main() -> None:
    args = failure_context(sys.argv[1:])
    counters = {"files": 0, "folders": 0}
    out, err = io.StringIO(), io.StringIO()
    try:
        # Publish neither a partial success display nor a half-written JSON stdout.
        with redirect_stdout(out), redirect_stderr(err):
            run_main(args, counters)
    except ScanError as exc:
        abort_scan(args, counters, exc)
    except (OSError, UnicodeError, ValueError):
        abort_scan(args, counters, ScanError("IO_ERROR；输入/输出失败，报告未完成。", code="IO_ERROR"))
    except SystemExit:
        sys.stdout.write(out.getvalue())
        sys.stderr.write(err.getvalue())
        raise
    else:
        sys.stdout.write(out.getvalue())
        sys.stderr.write(err.getvalue())


def run_main(args, counters) -> None:
    ap = ScanArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--folder", default="", help="要分析的目录 ID（默认根目录）")
    ap.add_argument("--from-fixture", help="离线模式：从 JSON fixture 读取（测试用）")
    ap.add_argument("--depth", type=int, default=2, help="目录树展示深度（默认 2）")
    ap.add_argument("--top", type=int, default=20, help="大文件榜数量（默认 20；0=不显示）")
    ap.add_argument("--json", dest="json_out", help='写入完整 JSON 报告（"-" 输出到 stdout）')
    ap.add_argument("--max-items", type=int, default=50000, help="文件数量安全上限（默认 50000）")
    args = ap.parse_args(namespace=args)

    if args.max_items <= 0 or args.top < 0 or args.depth < 0:
        ap.error("数值参数超出范围")
    timeout_seconds()
    fixture = load_fixture(args.from_fixture)

    root = walk_tree(args.folder, fixture, "根目录", counters, args.max_items)

    # --json - 时人类可读信息全部走 stderr，stdout 只输出纯 JSON
    info = sys.stderr if args.json_out == "-" else sys.stdout

    def say(*a, **k):
        print(*a, file=info, **k)

    say(f"扫描完成：目录 {counters['folders']} 个，文件 {counters['files']} 个"
        + ("（离线 fixture 模式）" if fixture is not LIVE else ""))
    say()
    say(f"已知总量：{human_size(root.size)}，共 {root.file_count} 个文件"
        + (f"；{root.unknown_size_files} 个大小未知，体积仅为下界" if root.unknown_size_files else ""))
    say()
    say(f"目录体积排行（前 {args.depth} 层）：")
    for c in sorted(root.children, key=lambda n: n.size, reverse=True):
        print_tree(c, 1, args.depth, 1, file=info)
    say()

    all_files = []
    collect_files(root, [], all_files)
    all_files.sort(key=lambda f: (-(f["size"] if f["size"] is not None else -1), f["id"]))
    if args.top > 0:
        say(f"大文件 TOP {args.top}：")
        for f in all_files[: args.top]:
            say(f"  {f['size_h']:>10}  {f['modified'][:16]}  {f['path']}")
        say()

    if args.json_out is not None:
        report = {
            "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "folder": args.folder,
            "source": "fixture" if fixture is not LIVE else "live",
            "complete": True, "truncated": False, "errors": [],
            "account_overview": None,
            "account_overview_status": "not_queried",
            "display_depth": args.depth,
            "top_files": all_files[:max(0, args.top)],
            "unknown_size_files": root.unknown_size_files,
            "total_size_is_lower_bound": root.unknown_size_files > 0,
            "total_size": root.size,
            "total_size_h": human_size(root.size),
            "total_files": root.file_count,
            "tree": root.to_dict(),
        }
        text = json.dumps(report, ensure_ascii=False, indent=2)
        if args.json_out == "-":
            print(text)
        else:
            write_report(args.json_out, text)
            print(f"报告已写入：{args.json_out}")


if __name__ == "__main__":
    main()
