#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PikPak 重复/新旧版本资源分析器（只读；绝不执行删除）。

在同一目录树内按「文件名归一化」把疑似同一资源的多个版本分组，按策略给出
「保留最新/最大/最高分辨率」的人工候选，输出报告；名称不代表内容重复。
命令仅从冻结报告按摘要和批准 ID 生成，不执行删除，不承诺恢复或容量释放。

归一化规则（保守设计）：
  - 统一小写、去掉扩展名、括号/分隔符转空格
  - 去掉清晰度/编码/来源/音轨等「包装噪音」词（1080p、x264、WEB-DL、HEVC…）
  - 保留语义信息：集数（S01E02、第01集）、语言音轨（国语/粤语/中字）、
    版本说明（未删减/重制版等）——这些不同则视为不同资源，不合并

用法：
  python3 analyze_dupes.py --folder <folderID>
  python3 analyze_dupes.py --folder <folderID> --policy newest
  python3 analyze_dupes.py --folder <folderID> --json report.json
  python3 analyze_dupes.py --from-report report.json --report-sha256 <digest> --approve-id <id> --emit-trash-cmd
  python3 analyze_dupes.py --from-fixture dev/fixtures/sample_tree.json --folder ""

环境变量：
  PIKPAK_BIN      pikpak 可执行文件路径（默认 "pikpak"）
  PIKPAK_TIMEOUT  单次 ls 超时秒数（默认 90）
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import stat
import subprocess
import sys
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from typing import NoReturn

# ---------------------------------------------------------------------------
# 归一化配置（可按需调整；调整后请重跑 dev/run_tests.py）
# ---------------------------------------------------------------------------

# 会被剔除的「包装噪音」词（全小写）。故意不含语言/版本语义词。
QUALITY_TOKENS = {
    "1080p", "720p", "2160p", "4k", "8k", "uhd", "fhd", "hd", "sd",
    "x264", "x265", "h264", "h265", "hevc", "avc", "av1", "xvid", "divx",
    "web", "webdl", "webrip", "bluray", "bdrip", "brrip", "bd", "remux",
    "hdrip", "dvdrip", "hdtv", "hdr", "hdr10", "dv", "dolby", "atmos",
    "10bit", "8bit", "hi10p", "aac", "ac3", "eac3", "dts", "flac", "mp3",
    "truehd", "repack", "proper", "dl", "web-dl",
}

KNOWN_EXTS = {
    "mp4", "mkv", "avi", "mov", "wmv", "flv", "ts", "m2ts", "rmvb", "webm",
    "mpg", "mpeg", "m4v", "3gp", "vob", "f4v", "mp3", "flac", "wav", "m4a",
    "aac", "ogg", "jpg", "jpeg", "png", "gif", "webp", "bmp", "txt", "url",
    "html", "htm", "srt", "ass", "vtt", "zip", "rar", "7z", "iso", "pdf",
    "nfo", "sub", "idx", "sup", "md",
}

VIDEO_EXTS = {"mp4", "mkv", "avi", "mov", "wmv", "flv", "ts", "m2ts", "rmvb",
              "webm", "mpg", "mpeg", "m4v", "3gp", "vob", "f4v"}
AUDIO_EXTS = {"mp3", "flac", "wav", "m4a", "aac", "ogg"}


def media_family(name):
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    return "video" if ext in VIDEO_EXTS else "audio" if ext in AUDIO_EXTS else None


DOMAIN_TOKEN_RE = re.compile(r"^(?:https?://)?(?:[\w-]+\.)+[a-z]{2,6}(?:/\S*)?$")

# ---------------------------------------------------------------------------


def die(msg: str, code: int = 1) -> NoReturn:
    print(f"错误：{msg}", file=sys.stderr)
    raise SystemExit(code)


def to_int(value) -> int:
    if value is None:
        return 0
    m = re.search(r"\d+", str(value))
    return int(m.group(0)) if m else 0


def byte_size(value):
    """Accept only nonnegative integer bytes; no units, signs or digit mining."""
    if isinstance(value, bool):
        return None
    if isinstance(value, int) and value >= 0:
        return value
    if isinstance(value, str) and re.fullmatch(r"[0-9]+", value):
        return int(value)
    return None


MAX_PIXEL_DIMENSION = 2147483647  # Supported metadata range, not a quality claim.


def pixel_dimension(value):
    """Positive integer pixels only; unknown is never repaired by digit mining."""
    if isinstance(value, bool):
        return None
    if isinstance(value, str):
        if not re.fullmatch(r"[0-9]+", value):
            return None
        digits = value.lstrip("0")
        if not digits or len(digits) > 10:
            return None  # Bound conversion before int(), including huge strings.
        value = int(digits)
    if isinstance(value, int) and 1 <= value <= MAX_PIXEL_DIMENSION:
        return value
    return None


def has_invalid_resolution_metadata(f: dict) -> bool:
    """Reject present-but-invalid dimensions without treating absent params as forged."""
    params = f.get("params")
    if params is None:
        return False
    if not isinstance(params, dict):
        return True
    return any(key in params and pixel_dimension(params[key]) is None
               for key in ("width", "height"))


def human_size(n: int) -> str:
    units = ("B", "KB", "MB", "GB", "TB")
    if n <= 0:
        return "0 B"
    i = 0
    try:
        value = float(n)
    except OverflowError:
        raise ScanError("字节大小超出当前展示范围；报告未完成。", code="INVALID_METADATA") from None
    while value >= 1024 and i < len(units) - 1:
        value /= 1024.0
        i += 1
    return f"{value:.0f} {units[i]}" if i == 0 else f"{value:.1f} {units[i]}"


def normalize_name(name: str) -> str:
    """把文件名归一化为「资源标识 key」。保守：只剔除包装噪音。"""
    n = name.lower()
    # 去扩展名（仅识别已知扩展名，避免误删名称尾段）
    m = re.search(r"\.([a-z0-9]{1,8})$", n)
    if m and m.group(1) in KNOWN_EXTS:
        n = n[: m.start()]
    # 括号、分隔符统一为空格
    n = re.sub(r"[\[\](){}【】（）《》]", " ", n)
    n = re.sub(r"[_\-\.\+·]+", " ", n)
    tokens = n.split()
    kept = []
    for t in tokens:
        if DOMAIN_TOKEN_RE.match(t):
            continue  # 发布站域名 token
        if t in QUALITY_TOKENS:
            continue
        kept.append(t)
    return " ".join(kept).strip()


def parse_time(value: str) -> datetime:
    if not value:
        return datetime.min.replace(tzinfo=timezone.utc)
    text = value.strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(text)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return datetime.min.replace(tzinfo=timezone.utc)


# ---------------------------------------------------------------------------


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


def walk(folder_id: str, fixture, rel_path, out, counters, max_items: int) -> None:
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
            name = f.get("name", "")
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
                walk(f.get("id", ""), fixture, rel_path + [name], out, counters, max_items)
            elif kind == "drive#file":
                if counters["files"] >= max_items:
                    raise ScanError(f"文件数量超过安全上限（{max_items}）", truncated=True)
                counters["files"] += 1
                out.append((rel_path, f))
        token = page.get("next_page_token", "") or ""
        if not token:
            break
    active.remove(folder_id)


def resolution_of(f: dict):
    params = f.get("params") or {}
    w = pixel_dimension(params.get("width"))
    h = pixel_dimension(params.get("height"))
    return max(w, h) if w is not None and h is not None else None


def member_record(rel_path, f):
    params = f.get("params") or {}
    w = pixel_dimension(params.get("width"))
    h = pixel_dimension(params.get("height"))
    res = f"{w}x{h}" if w is not None and h is not None else ""
    size = byte_size(f.get("size"))
    return {
        "id": f.get("id", ""),
        "name": f.get("name", ""),
        "path": "/".join(rel_path + [f.get("name", "")]),
        "size": size, "size_known": size is not None,
        "size_h": human_size(size) if size is not None else "未知",
        "modified": f.get("modified_time", ""),
        "created": f.get("created_time", ""),
        "resolution": res,
        "hash": (f.get("hash") or "").strip(),
    }


def pick_keeper(members, policy: str):
    if any(m["size"] is None for m in members):
        return None  # Unknown bytes cannot qualify a threshold or a size tie-break.
    if policy == "largest":
        return max(members, key=lambda m: (m["size"], parse_time(m["modified"])))
    if policy == "highest-res":
        ranked = []
        for member in members:
            width, _, height = member["resolution"].partition("x")
            w, h = pixel_dimension(width), pixel_dimension(height)
            if w is None or h is None:
                return None  # Even one unknown member prevents resolution ordering.
            ranked.append((max(w, h), member))
        return max(ranked, key=lambda pair: (pair[0], pair[1]["size"],
                                            parse_time(pair[1]["modified"])))[1]
    # 默认 newest：最新修改（导入）时间优先
    return max(members, key=lambda m: (parse_time(m["modified"]), m["size"]))


def emit_trash_cmd(ids):
    # Validate the ENTIRE batch before printing anything; never repair an opaque ID.
    if any(not isinstance(fid, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,255}", fid)
           for fid in ids):
        raise ValueError("ID 不符合安全命令格式；拒绝生成整批命令，请人工核验")
    ids = list(dict.fromkeys(ids))
    for i in range(0, len(ids), 30):
        batch = ids[i:i + 30]
        print("pikpak rm " + " ".join(batch))


def emit_approved_report(args):
    """Offline, byte-bound approval only. Never rescan or execute a command."""
    try:
        raw = read_json_bytes(args.from_report)
    except (OSError, ValueError):
        raise ScanError("INVALID_REPORT；无法读取冻结报告。", code="INVALID_REPORT") from None
    if hashlib.sha256(raw).hexdigest() != args.report_sha256:
        raise ValueError("报告 SHA-256 已变化；必须重新展示并取得批准")
    report = parse_json(raw, "INVALID_REPORT")
    if not isinstance(report, dict) or report.get("complete") is not True or report.get("truncated") is not False:
        raise ValueError("只允许从完整的冻结报告生成命令")
    try:
        candidates = [it for group in report["groups"] for it in group["trash_candidates"]]
        protected = {group["keeper"]["id"] for group in report["groups"]}
        allowed = {it["id"] for it in candidates}
    except (KeyError, TypeError):
        raise ValueError("冻结报告结构不匹配") from None
    if not args.approve_id or any(fid not in allowed or fid in protected for fid in args.approve_id):
        raise ValueError("批准 ID 不在该报告候选中，或属于保护/保留项")
    emit_trash_cmd(args.approve_id)


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
    ap.add_argument("--folder", default="", help='要扫描的目录 ID（默认根目录，即空字符串）')
    ap.add_argument("--from-fixture", help="离线模式：从 JSON fixture 读取目录数据（测试用，不访问网络）")
    ap.add_argument("--policy", choices=["newest", "largest", "highest-res"], default="newest",
                    help="保留策略：newest=保留最新修改（默认）；largest=保留最大；highest-res=保留最高分辨率")
    ap.add_argument("--min-size", type=int, default=102400,
                    help="只分析不小于该字节数的文件（默认 102400，即 100 KB；避免把小图/说明文本卷入分组）")
    ap.add_argument("--json", dest="json_out", help='把完整报告写入该文件（"-" 输出到标准输出）')
    ap.add_argument("--emit-trash-cmd", action="store_true",
                    help="仅从冻结报告打印明确批准 ID 的 pikpak rm 命令；不执行，恢复语义未核验")
    ap.add_argument("--max-items", type=int, default=50000, help="最大扫描文件数安全上限（默认 50000）")
    ap.add_argument("--from-report", help="仅从冻结 JSON 报告生成命令，不扫描云端")
    ap.add_argument("--report-sha256", help="人工审核时记录的报告原始字节 SHA-256")
    ap.add_argument("--approve-id", action="append", help="明确批准的单个候选 ID；可重复")
    args = ap.parse_args(namespace=args)
    if args.emit_trash_cmd:
        if not args.from_report or not args.report_sha256 or not args.approve_id:
            ap.error("生成命令必须同时提供 --from-report / --report-sha256 / --approve-id；禁止重新扫描扩大批准范围")
        if args.from_fixture is not None or args.folder or args.json_out is not None:
            ap.error("冻结报告模式不得同时扫描或写入报告")
        try:
            emit_approved_report(args)
        except (ValueError, OSError) as exc:
            ap.error(str(exc))
        return
    if args.from_report or args.report_sha256 or args.approve_id:
        ap.error("冻结批准参数只能配合 --emit-trash-cmd")

    if args.max_items <= 0 or args.min_size < 0:
        ap.error("数值参数超出范围")
    timeout_seconds()
    fixture = load_fixture(args.from_fixture)

    files = []
    walk(args.folder, fixture, [], files, counters, args.max_items)

    groups = {}
    invalid_resolution_ids = set()
    unassessed_files = [member_record(rel, f) for rel, f in files if byte_size(f.get("size")) is None]
    for rel_path, f in files:
        if has_invalid_resolution_metadata(f):
            invalid_resolution_ids.add(f["id"])
        size = byte_size(f.get("size"))
        if size is not None and size < args.min_size:
            continue
        family = media_family(f.get("name", ""))
        if family is None:
            continue  # Documents, archives, subtitles and unknown types are protected.
        key = normalize_name(f.get("name", ""))
        if len(key.replace(" ", "")) < 4:
            continue
        groups.setdefault((family, key), []).append(member_record(rel_path, f))

    dup_groups = []
    unassessed_groups = []
    for family, key in sorted(groups):
        members = groups[(family, key)]
        if len(members) < 2:
            continue
        resolution_invalid = any(member["id"] in invalid_resolution_ids for member in members)
        keeper = None if resolution_invalid else pick_keeper(members, args.policy)
        if keeper is None:
            unassessed_groups.append({
                "key": key, "media_family": family, "members": members,
                "keeper": None, "trash_candidates": [],
                "reason": "unknown_resolution" if resolution_invalid else
                          "unknown_size" if any(m["size"] is None for m in members) else
                          "unknown_resolution",
                "exact": False, "match_type": "name_candidate",
                "evidence": {"same_size": False, "remote_hash_match": False,
                             "hash_algorithm_verified": False},
            })
            continue
        others = [m for m in members if m["id"] != keeper["id"]]
        hashes = {m["hash"] for m in members if m["hash"]}
        same_size = all(m["size"] is not None for m in members) and len({m["size"] for m in members}) == 1
        remote_hash_match = same_size and len(hashes) == 1 and all(m["hash"] for m in members)
        # The CLI's opaque hash has no verified full-content algorithm contract.
        # Neither a name match nor matching remote metadata proves byte equality.
        dup_groups.append({
            "key": key, "media_family": family,
            "count": len(members),
            "policy": args.policy,
            "keeper": keeper,
            "trash_candidates": others,
            "match_type": "name_candidate", "exact": False,
            "evidence": {"normalized_name": key, "same_size": same_size,
                         "remote_hash_match": remote_hash_match,
                         "hash_algorithm_verified": False},
            "note": "同名/多版本候选，未校验内容"
                    + ("；远端 hash 与大小相同（算法未核验）" if remote_hash_match else ""),
        })

    report = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "folder": args.folder,
        "source": "fixture" if fixture is not LIVE else "live",
        "complete": True, "truncated": False, "errors": [],
        "policy": args.policy,
        "scanned_files": counters["files"],
        "scanned_folders": counters["folders"],
        "min_size": args.min_size,
        "groups": dup_groups,
        "size_complete": not unassessed_files,
        "analysis_complete": not unassessed_files and not unassessed_groups,
        "unknown_size_files": len(unassessed_files),
        "unassessed_files": unassessed_files, "unassessed_groups": unassessed_groups,
    }

    if args.json_out == "-":
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    print(f"扫描完成：目录 {counters['folders']} 个，文件 {counters['files']} 个"
          + ("（离线 fixture 模式）" if fixture is not LIVE else ""))
    if unassessed_files or unassessed_groups:
        print(f"\n{len(unassessed_files)} 个文件大小未知；{len(unassessed_groups)} 组因大小或分辨率证据不足，"
              "不提供保留/清理建议，见 unassessed_files/groups。")
    if not dup_groups:
        print("\n未生成可比较的多版本候选。" if unassessed_files or unassessed_groups else "\n未发现疑似重复/多版本资源。")
    else:
        total_trash = sum(len(g["trash_candidates"]) for g in dup_groups)
        print(f"\n发现 {len(dup_groups)} 组疑似重复资源，建议清理 {total_trash} 个旧版本"
              f"（策略：保留{'最新' if args.policy == 'newest' else '最大' if args.policy == 'largest' else '最高分辨率'}）：\n")
        for g in dup_groups:
            note = f"（{g['note']}）" if g["note"] else ""
            print(f"【{g['key']}】{g['count']} 个版本{note}")
            k = g["keeper"]
            print(f"  ✓ 保留： {k['size_h']:>10}  {k['modified'][:16]}  {k['path']}"
                  + (f"  [{k['resolution']}]" if k["resolution"] else ""))
            for t in g["trash_candidates"]:
                print(f"  ✗ 清理： {t['size_h']:>10}  {t['modified'][:16]}  {t['path']}"
                      + (f"  [{t['resolution']}]" if t["resolution"] else ""))
            print()
        print("\n提示：候选须人工核对；仅从摘要绑定的冻结报告生成命令，不自动删除，不承诺恢复语义。")
        print("      如策略不合适可用 --policy largest / highest-res 重跑。")

    if args.json_out is not None:
        text = json.dumps(report, ensure_ascii=False, indent=2)
        if args.json_out == "-":
            print(text)
        else:
            write_report(args.json_out, text)
            print(f"\n报告已写入：{args.json_out}")



if __name__ == "__main__":
    main()
