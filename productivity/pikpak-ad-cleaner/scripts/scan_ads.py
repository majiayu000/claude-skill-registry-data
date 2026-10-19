#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PikPak 广告/垃圾文件扫描器（只读；绝不执行删除）。

通过 `pikpak ls --raw` 遍历云端目录树，按「扩展名 + 文件名特征 + 体积/时长」
识别磁力/种子资源包中常见的推广垃圾文件，输出分级报告：

  high      高置信度垃圾：.url/.website 快捷方式、文件名含网址或强推广词的文本/图片等
  review    需要人工确认：疑似宣传短片、可执行文件、弱推广词文件等
  protected 明确保护、不建议删除：字幕文件、解压密码/说明文件

命令生成仅接受 SHA-256 绑定的冻结报告和逐个批准 ID；从不执行删除。
rm 的可恢复语义须另行核验，不承诺即时释放空间。

用法：
  python3 scan_ads.py --folder <folderID>
  python3 scan_ads.py --folder <folderID> --json report.json
  python3 scan_ads.py --from-report report.json --report-sha256 <digest> --approve-id <id> --emit-trash-cmd high
  python3 scan_ads.py --from-fixture dev/fixtures/sample_tree.json --folder ""

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
from datetime import datetime
from typing import NoReturn

# ---------------------------------------------------------------------------
# 规则常量（可按需调整；调整后请重跑 dev/run_tests.py）
# ---------------------------------------------------------------------------

VIDEO_EXT = {
    "mp4", "mkv", "avi", "mov", "wmv", "flv", "ts", "m2ts", "rmvb", "webm",
    "mpg", "mpeg", "m4v", "3gp", "vob", "f4v",
}
JUNK_EXT = {
    "txt", "html", "htm", "md", "ico",
    "jpg", "jpeg", "png", "gif", "webp", "bmp", "svg",
}
SUBTITLE_EXT = {"srt", "ass", "ssa", "vtt", "sub", "idx", "smi", "sup"}
ARCHIVE_EXT = {"zip", "rar", "7z", "tar", "gz", "bz2", "xz", "iso"}
DANGER_EXT = {"exe", "msi", "bat", "cmd", "vbs", "scr", "apk", "dmg", "pkg", "jar"}
SHORTCUT_EXT = {"url", "website", "lnk", "webloc", "desktop"}

PASSWORD_KEYS = ["密码", "password", "passwd", "解压码"]

# 强推广词：单独命中即可怀疑（配合扩展名规则分级）
STRONG_KEYS = [
    "最新地址", "永久地址", "永久域名", "发布页", "发布站", "网址导航", "导航页",
    "防失联", "防走失", "不迷路", "收藏本站", "备用网址", "备用地址",
    "点击进入", "点击查看", "更多精彩", "更多资源", "更多福利",
    "加群", "进群", "入群", "扫码", "二维码", "加微信", "微信号",
    "客服", "官网", "官方网址", "免费领取", "领取福利", "免费观看",
    "影视大全", "看片神器", "看片", "广告", "宣传", "推广", "赞助", "邀请码",
]
# 弱推广词：需多个同时出现或配合其它信号
WEAK_KEYS = ["网址", "备用", "福利", "领取", "神器", "入口", "地址", "域名", "发布"]

DOMAIN_RE = re.compile(
    r"(?:https?://|www\.)"
    r"|(?<![\w@])[\w-]{2,}\.(?:com|net|org|cc|xyz|top|vip|icu|me|info|club|site"
    r"|online|shop|live|tv|app|link|pro|fun|pw|cyou|sbs|uno)(?![\w])",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------


class Fatal(Exception):
    """无法继续的错误。"""


def die(msg: str, code: int = 1) -> NoReturn:
    print(f"错误：{msg}", file=sys.stderr)
    raise SystemExit(code)


def file_ext(name: str) -> str:
    m = re.search(r"\.([A-Za-z0-9]{1,8})$", name)
    return m.group(1).lower() if m else ""


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


def classify(f: dict):
    """返回 (tier, reasons)；tier 为 high/review/protected/None。"""
    name = f.get("name", "")
    ext = file_ext(name)
    size = byte_size(f.get("size"))
    dur = byte_size((f.get("params") or {}).get("duration"))
    low = name.lower()

    # 1) 保护清单（优先于一切垃圾判定）
    if ext in SUBTITLE_EXT:
        return "protected", ["字幕文件"]
    if ext == "txt" and any(k in name or k in low for k in PASSWORD_KEYS):
        return "protected", ["疑似解压密码/说明文件"]
    if ext in ARCHIVE_EXT:
        return None, []  # 压缩包通常是资源本体，不参与广告判定

    # 2) 快捷方式文件
    if ext in SHORTCUT_EXT:
        return "high", [f".{ext} 网站快捷方式（典型引流文件）"]

    junkish = ext in JUNK_EXT
    strong = [k for k in STRONG_KEYS if k in name or k in low]
    weak = [k for k in WEAK_KEYS if k in name or k in low]
    has_domain = bool(DOMAIN_RE.search(name))

    # 3) 可执行文件：媒体包里出现即可疑，交给人工确认
    if ext in DANGER_EXT:
        why = "可执行文件（注意安全）"
        if strong:
            why += f"，含推广词：{'、'.join(strong[:3])}"
        return "review", [why]

    # 4) 文本/图片类（单个推广词降级为待确认，避免误伤「宣传海报」类正常文件名）
    if junkish:
        if has_domain:
            return "high", ["文件名含网址"]
        if len(strong) >= 2:
            return "high", [f"含多个推广词：{'、'.join(strong[:3])}"]
        if len(strong) == 1:
            return "review", [f"含推广词：{strong[0]}（需人工确认）"]
        if len(weak) >= 2:
            return "review", [f"含多个弱推广词：{'、'.join(weak[:3])}"]
        return None, []

    # 5) 视频：只有明显宣传短片特征才进 review
    if ext in VIDEO_EXT:
        small = (size and size <= 300 * 1024 * 1024) or (dur and dur <= 180)
        if strong and small:
            return "review", ["疑似宣传短片（含推广词且体积/时长很小）"]
        return None, []

    # 6) 其它扩展名：仅强推广词兜底
    if strong:
        return "review", [f"含推广词：{'、'.join(strong[:3])}"]
    return None, []


def item_record(rel_path, f, tier, reasons):
    name = f.get("name", "")
    size = byte_size(f.get("size"))
    return {
        "id": f.get("id", ""),
        "name": name,
        "path": "/".join(rel_path + [name]),
        "size": size, "size_known": size is not None,
        "size_h": human_size(size) if size is not None else "未知",
        "ext": file_ext(name),
        "tier": tier,
        "reasons": reasons,
        "modified": f.get("modified_time", ""),
    }


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
        candidates = report[args.emit_trash_cmd]
        protected = {it["id"] for it in report["protected"]}
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
    ap.add_argument("--json", dest="json_out", help='把完整报告写入该文件（"-" 输出到标准输出）')
    ap.add_argument("--emit-trash-cmd", choices=["high", "review"],
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

    if args.max_items <= 0:
        ap.error("数值参数超出范围")
    timeout_seconds()
    fixture = load_fixture(args.from_fixture)

    files = []
    walk(args.folder, fixture, [], files, counters, args.max_items)

    buckets = {"high": [], "review": [], "protected": []}
    for rel_path, f in files:
        tier, reasons = classify(f)
        if tier:
            buckets[tier].append(item_record(rel_path, f, tier, reasons))

    report = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "folder": args.folder,
        "source": "fixture" if fixture is not LIVE else "live",
        "complete": True, "truncated": False, "errors": [],
        "scanned_files": counters["files"],
        "scanned_folders": counters["folders"],
        "unknown_size_files": sum(byte_size(f.get("size")) is None for _, f in files),
        "size_complete": all(byte_size(f.get("size")) is not None for _, f in files),
        "high": buckets["high"],
        "review": buckets["review"],
        "protected": buckets["protected"],
    }

    if args.json_out == "-":
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    print(f"扫描完成：目录 {counters['folders']} 个，文件 {counters['files']} 个"
          + ("（离线 fixture 模式）" if fixture is not LIVE else ""))
    for tier, label in (("high", "高置信度垃圾（建议清理）"),
                        ("review", "待人工确认"), ("protected", "受保护（不建议删除）")):
        items = buckets[tier]
        if items:
            print(f"\n[{label}] {len(items)} 个：")
            for it in items:
                print(f"  {it['size_h']:>10}  {it['path']}  —— {'；'.join(it['reasons'])}")
    if not any(buckets.values()):
        print("\n未发现疑似广告/垃圾文件。")
    else:
        print("\n提示：候选须人工核对；仅从摘要绑定的冻结报告生成命令，不自动删除，不承诺恢复语义。")

    if args.json_out is not None:
        text = json.dumps(report, ensure_ascii=False, indent=2)
        if args.json_out == "-":
            print(text)
        else:
            write_report(args.json_out, text)
            print(f"\n报告已写入：{args.json_out}")



if __name__ == "__main__":
    try:
        main()
    except Fatal as exc:
        die(str(exc))
