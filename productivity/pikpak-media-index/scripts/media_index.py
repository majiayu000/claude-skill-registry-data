#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PikPak 媒体库索引生成器（只读）。

扫描目录树，提取视频元数据（时长/分辨率/编码/来源），生成 Markdown 或 CSV 索引。

用法：
  python3 media_index.py --folder "" --output /tmp/media_index.md
  python3 media_index.py --folder "" --format csv --output /tmp/media.csv
  python3 media_index.py --folder "" --filter 4k
  python3 media_index.py --from-fixture dev/fixtures/sample_tree.json --folder ""

环境变量：
  PIKPAK_BIN      pikpak 可执行文件路径（默认 "pikpak"）
  PIKPAK_TIMEOUT  单次 ls 超时秒数（默认 90）
"""

from __future__ import annotations

import argparse
import csv
import html
import io
import json
import math
import os
import re
import string
import stat
import subprocess
import sys
import time
from datetime import datetime
from typing import NoReturn
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

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


def to_int(value) -> int:
    if type(value) is int:
        try:
            text = str(value)
        except (ValueError, OverflowError):
            return 0
    elif type(value) is str:
        text = value
    else:
        return 0
    if (not text or len(text) > MAX_DECIMAL_DIGITS
            or not re.fullmatch(r"[0-9]+", text)):
        return 0
    try:
        return int(text)
    except (ValueError, OverflowError):
        return 0


def human_size(n: int) -> str:
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


def hms(seconds: int) -> str:
    if seconds <= 0:
        return "-"
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


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
        if row.get("medias") is not None:
            if type(row["medias"]) is not list:
                die("schema_error (ls_medias)")
            for item in row["medias"]:
                if type(item) is not dict or (item.get("video") is not None and type(item["video"]) is not dict):
                    die("schema_error (ls_media_item)")
    return data


def ls_page(folder_id: str, fixture: "dict | None", page_token: str = "", *, timeout: float | None = None) -> dict:
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
    visited = counters.setdefault("_folder_ids", set())
    if folder_id in visited or len(rel_path) > 100:
        die("目录循环或深度超过安全上限。")
    visited.add(folder_id)
    token, tokens = "", set()
    while True:
        if token in tokens:
            die("分页 token 重复，索引未完成。")
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
                counters["folders"] += 1
                if counters["folders"] > 5000:
                    die("目录数量超过安全上限。")
                walk(f.get("id", ""), fixture, rel_path + [f.get("name", "")], out, counters, max_items)
            elif kind == "drive#file":
                counters["files"] += 1
                if counters["files"] > max_items:
                    die(f"文件数超过安全上限（{max_items}）。")
                out.append((rel_path, f))
        token = page["next_page_token"]
        if not token:
            break


def safe_codec(value) -> str:
    if type(value) is not str or not value or len(value) > 128:
        return ""
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9 ._+\-]{0,127}", value):
        return ""
    return value


def video_record(rel_path, f):
    params = f.get("params") or {}
    duration = to_int(params.get("duration"))
    width = to_int(params.get("width"))
    height = to_int(params.get("height"))
    long_edge = max(width, height) if width and height else 0
    codec = ""
    for media in f.get("medias") or []:
        v = (media.get("video") or {})
        codec_value = v.get("video_codec")
        if media.get("is_origin") is True:
            codec = safe_codec(codec_value)
            if codec:
                break
    source = safe_source(params.get("url")) or safe_source(f.get("original_url"))
    return {
        "name": f.get("name", ""),
        "path": "/".join(rel_path),
        "size": to_int(f.get("size")),
        "duration": duration,
        "resolution": f"{width}x{height}" if width and height else "",
        "long_edge": long_edge,
        "is_4k": long_edge >= 3840,
        "codec": codec,
        "source": source,
        "pending": f.get("phase") == "PHASE_TYPE_RUNNING",
        "metadata_status": "available" if duration else "unknown",
        "modified": f.get("modified_time", ""),
    }


def safe_source(value):
    if type(value) is not str:
        return ""
    try:
        u = urlsplit(value)
        if u.scheme in ("http", "https") and u.hostname:
            host = u.hostname
            if ":" in host:
                host = "[" + host + "]"
            if u.port:
                host += ":" + str(u.port)
            return urlunsplit((u.scheme, host, u.path, "", ""))
        if u.scheme == "magnet":
            return "magnet:?" + urlencode([(k,v) for k,v in parse_qsl(u.query) if k == "xt"])
    except (TypeError, ValueError):
        pass
    return ""


def export_scalar(value):
    """Keep report fields scalar; never stringify nested raw metadata."""
    return value if type(value) in (str, int, float, bool) else ""


def md_cell(value):
    # Encode punctuation as character data, never Markdown/HTML syntax.
    # This also preserves literal entity-looking text and backslashes.
    text = str(export_scalar(value)).replace("\r", " ").replace("\n", " ")
    return "".join(f"&#{ord(c)};" if c in string.punctuation else html.escape(c) for c in text)


def csv_cell(value):
    value = export_scalar(value)
    text = str(value)
    # CSV quoting alone does not stop spreadsheet formula execution.
    if text.lstrip(" \t\r\n").startswith(("=", "+", "-", "@")) or text.startswith(("\t", "\r", "\n")):
        return "'" + text
    return value


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
    ap.add_argument("--folder", default="", help="要扫描的目录 ID（默认根目录）")
    ap.add_argument("--from-fixture", help="离线模式（测试用）")
    ap.add_argument("--format", choices=["md", "csv"], default="md", help="输出格式（默认 md）")
    ap.add_argument("--output", help="写入文件（默认 stdout）")
    ap.add_argument("--filter", choices=["all", "4k", "hd", "short"], default="all",
                    help="筛选：all/4k（长边≥3840）/hd（长边≥1280）/short（≤1小时）")
    ap.add_argument("--max-items", type=int, default=50000, help="文件数安全上限")
    ap.add_argument("--overwrite", action="store_true", help="明确允许替换已有普通报告文件；不跟随符号链接")
    ap.add_argument("--max-pages", type=int, default=10000, help="全树列表页数上限，超限标 incomplete")
    ap.add_argument("--scan-timeout", type=float, default=900, help="列表扫描总秒数预算；不含报告生成/下载/正则执行")
    args = ap.parse_args()
    if args.max_pages < 1 or not math.isfinite(args.scan_timeout) or args.scan_timeout <= 0 or args.max_items < 1:
        die("扫描预算和 max-items 必须为有限正数。")

    fixture = None
    if args.from_fixture is not None:
        fixture = load_fixture(args.from_fixture)

    files = []
    counters = {"files": 0, "folders": 0, "_max_pages": args.max_pages, "_scan_seconds": args.scan_timeout}
    walk(args.folder, fixture, [], files, counters, args.max_items)

    videos = []
    for rel_path, f in files:
        ext = re.search(r"\.([A-Za-z0-9]+)$", f.get("name", ""))
        mime = str(f.get("mime_type", ""))
        category = f.get("file_category")
        if mime.startswith("audio/") or category == "AUDIO":
            continue
        metadata_video = (mime.startswith("video/")
                          or category == "VIDEO"
                          or any(m.get("video") for m in f.get("medias") or [])
                          or to_int((f.get("params") or {}).get("duration")) > 0)
        if metadata_video or (ext and ext.group(1).lower() in {"mp4", "mkv", "avi", "mov", "ts", "m2ts", "webm", "rmvb", "wmv", "flv"}):
            videos.append(video_record(rel_path, f))

    if args.filter == "4k":
        videos = [v for v in videos if v["is_4k"]]
    elif args.filter == "hd":
        videos = [v for v in videos if v["long_edge"] >= 1280]
    elif args.filter == "short":
        videos = [v for v in videos if 0 < v["duration"] <= 3600]

    total_size = sum(v["size"] for v in videos)
    now = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M")

    if args.format == "csv":
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["name", "duration", "resolution", "codec", "size_bytes", "size_h", "path", "modified", "source"])
        for v in sorted(videos, key=lambda x: x["size"], reverse=True):
            writer.writerow([csv_cell(cell) for cell in
                             [v["name"], hms(v["duration"]), v["resolution"], v["codec"],
                              v["size"], human_size(v["size"]), v["path"], v["modified"], v["source"]]])
        text = buf.getvalue()
    else:
        lines = [
            f"# 媒体库索引（{now}）",
            "",
            f"共 {len(videos)} 个视频，总量 {human_size(total_size)}"
            + (f"（筛选：{args.filter}）" if args.filter != "all" else ""),
            "",
            "| # | 名称 | 时长 | 分辨率 | 大小 | 原始编码 | 路径 | 来源（已脱敏） |",
            "|---|------|------|--------|------|------|------|------|",
        ]
        for i, v in enumerate(sorted(videos, key=lambda x: x["size"], reverse=True), 1):
            cells = [i, v['name'], hms(v['duration']), v['resolution'] or '-',
                     human_size(v['size']), v['codec'] or '-', v['path'] or '/', v['source'] or '-']
            lines.append("| " + " | ".join(md_cell(c) for c in cells) + " |")
        pending = [v for v in videos if v["metadata_status"] == "unknown"]
        if pending:
            lines += ["", f"注：{len(pending)} 个视频时长未知；缺字段不代表正在转码，已包含在列表中。"]
        text = "\n".join(lines) + "\n"

    if args.output:
        write_report(args.output, text, overwrite=args.overwrite)
        print(f"索引已写入：{args.output}（{len(videos)} 个视频）")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
