#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PikPak 云端文件搜索（只读）：遍历目录树，按关键词匹配文件名与路径。

本脚本使用目录遍历，不依赖服务端 search；CLI 缺少 search 不能证明服务端 API 已下线。
支持：多关键词（AND/OR）、正则、类型过滤、按大小/时间排序、结果数量限制。

用法：
  python3 search_files.py --folder "" --query "Sintel"
  python3 search_files.py --folder "" --query "4k 国语" --mode and
  python3 search_files.py --folder "" --query "\\.mkv$" --regex
  python3 search_files.py --folder "" --query "Sintel" --type file --sort size --limit 20
  python3 search_files.py --from-fixture dev/fixtures/sample_tree.json --folder "" --query "Sintel"

环境变量：
  PIKPAK_BIN      pikpak 可执行文件路径（默认 "pikpak"）
  PIKPAK_TIMEOUT  单次 ls 超时秒数（默认 90）
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import stat
import subprocess
import sys
import time
from datetime import datetime, timezone
from typing import NoReturn


MAX_DECIMAL_DIGITS = 4000


def bounded_json_int(text: str) -> int:
    digits = text[1:] if text.startswith("-") else text
    if not digits or len(digits) > MAX_DECIMAL_DIGITS:
        raise ValueError("integer exceeds safety limit")
    return int(text)


def decode_json(text, context: str):
    try:
        return json.loads(text, parse_int=bounded_json_int)
    except (TypeError, ValueError, OverflowError):
        die(f"schema_error ({context})")


def die(msg: str, code: int = 1) -> NoReturn:
    print(f"错误：{msg}", file=sys.stderr)
    raise SystemExit(code)


def load_fixture(path):
    if type(path) is not str or not path:
        die("fixture_path_invalid")
    try:
        with open(path, encoding="utf-8") as fh:
            fixture = decode_json(fh.read(), "fixture_input")
    except (OSError, UnicodeError):
        die("schema_error (fixture_input)")
    if type(fixture) is not dict:
        die("schema_error (fixture_root)")
    return fixture


def to_int(value) -> int | None:
    if type(value) is int:
        if value < 0:
            return None
        try:
            if len(str(value)) > MAX_DECIMAL_DIGITS:
                return None
        except (ValueError, OverflowError):
            return None
        return value
    if (type(value) is str and len(value) <= MAX_DECIMAL_DIGITS
            and re.fullmatch(r"[0-9]+", value)):
        try:
            return int(value)
        except (ValueError, OverflowError):
            pass
    return None


def human_size(n: int | None) -> str:
    if n is None:
        return "未知"
    if n <= 0:
        return "0 B"
    units = ("B", "KB", "MB", "GB", "TB")
    i = 0
    try:
        value = float(n)
    except (ValueError, OverflowError):
        try:
            return f"{n} B" if len(str(n)) <= MAX_DECIMAL_DIGITS else "未知"
        except (ValueError, OverflowError):
            return "未知"
    while value >= 1024 and i < len(units) - 1:
        value /= 1024.0
        i += 1
    return f"{value:.0f} {units[i]}" if i == 0 else f"{value:.1f} {units[i]}"


def parse_time(value: str) -> datetime:
    if not value:
        return datetime.min.replace(tzinfo=timezone.utc)
    text = value.strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(text)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return datetime.min.replace(tzinfo=timezone.utc)


def validate_page(data):
    """Validate this adapter's raw listing contract; never guess an empty page."""
    if type(data) is not dict:
        die("schema_error (ls_root)")
    if (any(k in data for k in ("error", "errors", "error_code", "error_description", "error_message", "code"))
            or data.get("success", True) is not True or data.get("ok", True) is not True
            or ("status" in data and data["status"] not in ("ok", "success"))):
        die("schema_error (ls_envelope)")
    if type(data.get("files")) is not list or type(data.get("next_page_token")) is not str:
        die("schema_error (ls_collection_or_token)")
    for row in data["files"]:
        if (type(row) is not dict or type(row.get("id")) is not str or not row["id"].strip()
                or type(row.get("name")) is not str or not row["name"]
                or row.get("kind") not in ("drive#file", "drive#folder")):
            die("schema_error (ls_item)")
        if "modified_time" in row and type(row["modified_time"]) is not str:
            die("schema_error (ls_modified_time)")
        if row.get("params") is not None and type(row["params"]) is not dict:
            die("schema_error (ls_params)")
        if type(row.get("size")) in (dict, list):
            die("schema_error (ls_size)")
        if row.get("medias") is not None:
            if type(row["medias"]) is not list:
                die("schema_error (ls_medias)")
            for item in row["medias"]:
                if type(item) is not dict or (item.get("video") is not None and type(item["video"]) is not dict):
                    die("schema_error (ls_media_item)")
    return data


def ls_page(folder_id: str, fixture: "dict | None", page_token: str = "", *, timeout: float | None = None) -> dict:
    """取一页目录列表。fixture 非 None 时离线读取。"""
    if fixture is not None:
        if type(fixture) is not dict:
            die("schema_error (fixture_root)")
        node = fixture.get(folder_id)
        if type(node) is not dict or page_token not in node:
            die("schema_error (fixture_page_missing)")
        return validate_page(node[page_token])

    cmd = [os.environ.get("PIKPAK_BIN", "pikpak"), "ls", "--raw", "-l", "500"]
    if folder_id:
        cmd += ["-p", folder_id]
    if page_token:
        cmd += ["-t", page_token]
    cli_timeout = int(os.environ.get("PIKPAK_TIMEOUT", "90"))
    timeout = min(cli_timeout, timeout) if timeout is not None else cli_timeout
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except FileNotFoundError:
        die("cli_unavailable (exit_code=127)")
    except subprocess.TimeoutExpired:
        die("cli_timeout (exit_code=124)")
    except OSError:
        die("cli_os_error (exit_code=126)")
    if proc.returncode != 0:
        die(f"cli_failed (exit_code={proc.returncode})")
    return validate_page(decode_json(proc.stdout, "ls_json"))


def walk(folder_id: str, fixture: "dict | None", rel_path, out, counters, max_items: int) -> None:
    """遍历目录树，收集 (rel_path, file_dict)。"""
    visited = counters.setdefault("_folder_ids", set())
    if folder_id in visited or len(rel_path) > 100:
        die("目录循环或深度超过安全上限。")
    visited.add(folder_id)
    token, tokens = "", set()
    while True:
        if token in tokens:
            die("分页 token 重复，搜索未完成。")
        tokens.add(token)
        remaining = counters.setdefault("_deadline", time.monotonic() + counters.get("_scan_seconds", 900)) - time.monotonic()
        if counters.get("_pages", 0) >= counters.get("_max_pages", 10000) or remaining <= 0:
            die("scan_budget_exceeded (incomplete)")
        counters["_pages"] = counters.get("_pages", 0) + 1
        page = ls_page(folder_id, fixture, token, timeout=remaining)
        if time.monotonic() >= counters["_deadline"]:
            die("scan_budget_exceeded (incomplete)")
        for f in page["files"]:
            kind = f.get("kind")
            if kind == "drive#folder":
                out.append((rel_path, f))
                counters["folders"] += 1
                if counters["folders"] > 5000:
                    die("目录数量超过安全上限（5000），已中止。请缩小搜索范围。")
                walk(f.get("id", ""), fixture, rel_path + [f.get("name", "")], out, counters, max_items)
            elif kind == "drive#file":
                counters["files"] += 1
                if counters["files"] > max_items:
                    die(f"文件数量超过安全上限（{max_items}），已中止。请缩小搜索范围。")
                out.append((rel_path, f))
        token = page["next_page_token"]
        if not token:
            break


def match(name: str, full_path: str, queries: list[str], mode: str, regex: bool) -> list[str]:
    """返回命中的关键词列表；全不中返回空列表。"""
    hits = []
    for q in queries:
        if regex:
            try:
                if re.search(q, name, re.IGNORECASE) or re.search(q, full_path, re.IGNORECASE):
                    hits.append(q)
            except re.error as exc:
                die(f"正则错误（{q}）：{exc}")
        else:
            ql = q.lower()
            if ql in name.lower() or ql in full_path.lower():
                hits.append(q)
    if mode == "and":
        return hits if len(hits) == len(queries) else []
    return hits  # or 模式：命中任一即可


def write_report(path, text, *, overwrite=False):
    """Create a private report exclusively; replacing a regular file is opt-in."""
    fd = None
    try:
        flags = os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK
        if not overwrite:
            flags |= os.O_EXCL
        fd = os.open(path, flags, 0o600)
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            die("report_target_not_regular_or_has_aliases")
        os.fchmod(fd, 0o600)
        if overwrite:
            os.ftruncate(fd, 0)
        stream = os.fdopen(fd, "w", encoding="utf-8")
        fd = None
        with stream:
            stream.write(text)
    except OSError:
        die("report_write_failed (existing_or_unsafe_target_or_io_error)")
    finally:
        if fd is not None:
            os.close(fd)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--folder", default="", help="搜索起点目录 ID（默认根目录）")
    ap.add_argument("--from-fixture", help="离线模式（测试用）")
    ap.add_argument("--query", required=True, help="搜索词（空格分隔多个；--mode and 时全部需命中）")
    ap.add_argument("--mode", choices=["or", "and"], default="or", help="多词逻辑：or（默认）/ and")
    ap.add_argument("--regex", action="store_true", help="把 query 当作正则表达式")
    ap.add_argument("--type", choices=["file", "folder", "any"], default="any", help="只搜文件/文件夹/不限")
    ap.add_argument("--sort", choices=["name", "size", "time"], default="name", help="排序方式")
    ap.add_argument("--desc", action="store_true", help="降序")
    ap.add_argument("--limit", type=int, default=50, help="结果数量上限（默认 50）")
    ap.add_argument("--json", dest="json_out", help='JSON 输出（"-" 到 stdout，人类可读转 stderr）')
    ap.add_argument("--max-items", type=int, default=50000, help="遍历文件数安全上限")
    ap.add_argument("--overwrite", action="store_true", help="明确允许替换已有普通报告文件；不跟随符号链接")
    ap.add_argument("--max-pages", type=int, default=10000, help="全树列表页数上限，超限标 incomplete")
    ap.add_argument("--scan-timeout", type=float, default=900, help="列表扫描总秒数预算；不含报告生成/下载/正则执行")
    args = ap.parse_args()
    if args.max_pages < 1 or not math.isfinite(args.scan_timeout) or args.scan_timeout <= 0 or args.max_items < 1:
        die("扫描预算和 max-items 必须为有限正数。")

    fixture = None
    if args.from_fixture is not None:
        fixture = load_fixture(args.from_fixture)

    if args.limit < 1 or args.max_items < 1:
        die("limit 和 max-items 必须为正数。")
    queries = [args.query] if args.regex else args.query.split()
    if not queries:
        die("query 为空。")
    if args.regex:
        try:
            re.compile(args.query, re.IGNORECASE)
        except re.error as exc:
            die(f"正则错误：{exc}")

    files = []
    counters = {"files": 0, "folders": 0, "_max_pages": args.max_pages, "_scan_seconds": args.scan_timeout}
    walk(args.folder, fixture, [], files, counters, args.max_items)

    results = []
    for rel_path, f in files:
        name = f.get("name", "")
        full_path = "/".join(rel_path + [name])
        if args.type == "file" and f.get("kind") != "drive#file":
            continue
        if args.type == "folder" and f.get("kind") != "drive#folder":
            continue
        hits = match(name, full_path, queries, args.mode, args.regex)
        if hits:
            results.append({
                "id": f.get("id", ""),
                "kind": f.get("kind", ""),
                "name": name,
                "path": full_path,
                "size": to_int(f.get("size")),
                "size_h": human_size(to_int(f.get("size"))),
                "modified": f.get("modified_time", ""),
                "hits": hits,
            })

    # 排序
    if args.sort == "size":
        known = [r for r in results if r["size"] is not None]
        unknown = [r for r in results if r["size"] is None]
        known.sort(key=lambda r: r["size"], reverse=args.desc)
        results = known + unknown
    elif args.sort == "time":
        results.sort(key=lambda r: parse_time(r["modified"]), reverse=args.desc)
    else:
        results.sort(key=lambda r: r["name"].lower(), reverse=args.desc)

    total_found = len(results)
    results = results[: args.limit]

    out = sys.stderr if args.json_out == "-" else sys.stdout

    def say(*a):
        print(*a, file=out)

    say(f"搜索完成：遍历 {counters['folders']} 个目录、{counters['files']} 个文件，"
        f"命中 {total_found} 个（显示前 {len(results)} 个）")
    say()
    for r in results:
        say(f"  {r['size_h']:>10}  {r['modified'][:10]}  {r['path']}")

    if args.json_out:
        report = {
            "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "query": args.query,
            "mode": args.mode,
            "regex": args.regex,
            "scanned_files": counters["files"],
            "scanned_folders": counters["folders"],
            "total_found": total_found,
            "results": results,
        }
        text = json.dumps(report, ensure_ascii=False, indent=2)
        if args.json_out == "-":
            print(text)
        else:
            write_report(args.json_out, text, overwrite=args.overwrite)
            print(f"报告已写入：{args.json_out}")


if __name__ == "__main__":
    main()
