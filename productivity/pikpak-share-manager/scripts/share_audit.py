#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PikPak 分享审计（只读）：列出分享链接，标记已过期/临期/零访问项。

用法：
  python3 share_audit.py
  python3 share_audit.py --json report.json
  python3 share_audit.py --from-fixture dev/fixtures/shares.json

只读：仅调用 `pikpak share ls`；不创建、不删除任何分享。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import subprocess
import sys
from datetime import datetime, timezone
from datetime import timedelta
from decimal import Decimal, DecimalException
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


def validate_page(data, *, snapshot=False):
    """Raw pages need an explicit token; fixture snapshots are complete lists."""
    if type(data) is not dict:
        die("schema_error (share_root)")
    if (any(k in data for k in ("error", "errors", "error_code", "error_description", "error_message", "code"))
            or data.get("success", True) is not True or data.get("ok", True) is not True
            or ("status" in data and data["status"] not in ("ok", "success"))):
        die("schema_error (share_envelope)")
    if type(data.get("shares")) is not list:
        die("schema_error (share_collection)")
    token = data.get("next_page_token", "") if snapshot else data.get("next_page_token")
    if type(token) is not str or (snapshot and token):
        die("schema_error (share_token_or_incomplete_snapshot)")
    ids = set()
    for row in data["shares"]:
        if (type(row) is not dict or type(row.get("share_id")) is not str or not row["share_id"].strip()
                or type(row.get("title")) is not str or row["share_id"] in ids):
            die("schema_error (share_item_or_duplicate_id)")
        ids.add(row["share_id"])
    return data


_UNSET_FIXTURE = object()


def fetch_shares(fixture=_UNSET_FIXTURE):
    """返回全部分享列表（自动翻页）。"""
    if fixture is not _UNSET_FIXTURE:
        if fixture is None:
            die("schema_error (fixture_root)")
        return validate_page(fixture, snapshot=True)["shares"]

    shares = []
    token, tokens, ids = "", set(), set()
    for _ in range(20):  # 最多 20 页安全上限
        if token in tokens:
            die("分享分页 token 重复，审计未完成。")
        tokens.add(token)
        cmd = [os.environ.get("PIKPAK_BIN", "pikpak"), "share", "ls", "-F", "json", "-l", "100"]
        if token:
            cmd += ["--token", token]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        except FileNotFoundError:
            die("cli_unavailable (exit_code=127)")
        except subprocess.TimeoutExpired:
            die("cli_timeout (exit_code=124)")
        except OSError:
            die("cli_os_error (exit_code=126)")
        if proc.returncode != 0:
            die(f"cli_failed (exit_code={proc.returncode})")
        data = validate_page(decode_json(proc.stdout, "share_json"))
        for row in data["shares"]:
            sid = row.get("share_id")
            if not sid or sid in ids:
                die("分享 ID 缺失或重复，拒绝输出完整审计。")
            ids.add(sid)
            shares.append(row)
        token = data["next_page_token"]
        if not token:
            break
    if token:
        die("分享超过 20 页安全上限，审计未完成。")
    return shares


def parse_time(value, *, epoch_unit="auto") -> datetime | None:
    """ISO or explicit seconds/milliseconds; auto prefers representable seconds.

    Numeric values valid in both units are ambiguous: use s:/ms: or epoch_unit.
    Auto falls back to milliseconds only if UTC seconds exceed datetime's range.
    Convert decimals at microsecond precision, without float threshold heuristics.
    """
    if type(value) not in (str, int, float) or epoch_unit not in ("auto", "seconds", "milliseconds"):
        return None
    try:
        text = str(value).strip()
    except (ValueError, OverflowError):
        return None
    if text.startswith(("s:", "ms:")):
        prefix, text = text.split(":", 1)
        epoch_unit = "milliseconds" if prefix == "ms" else "seconds"
    if re.fullmatch(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?", text):
        try:
            number = Decimal(text)
            if not number.is_finite():
                return None
            units = ("seconds", "milliseconds") if epoch_unit == "auto" else (epoch_unit,)
            for unit in units:
                seconds = number / 1000 if unit == "milliseconds" else number
                # Avoid constructing huge integers/timedeltas from corrupt input.
                if not Decimal("-62135596800") <= seconds < Decimal("253402300800"):
                    continue
                try:
                    return datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(microseconds=int(seconds * 1000000))
                except (ValueError, OverflowError):
                    continue
        except DecimalException:
            pass
        return None
    if type(value) is not str or not text or text.lower() in ("nan", "infinity", "inf"):
        return None
    try:
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def safe_count(value) -> int | None:
    if type(value) is not int or value < 0:
        return None
    try:
        if len(str(value)) > MAX_DECIMAL_DIGITS:
            return None
    except (ValueError, OverflowError):
        return None
    return value


def audit(shares, now=None, *, epoch_unit="auto") -> list[dict]:
    now = now or datetime.now(timezone.utc)
    result = []
    for s in shares:
        exp_raw = s.get("expiration")
        forever = (type(exp_raw) is int and exp_raw == -1) or (type(exp_raw) is str and exp_raw == "-1")
        exp = parse_time(exp_raw, epoch_unit=epoch_unit)
        created = parse_time(s.get("created"), epoch_unit=epoch_unit)
        raw_views = s.get("views")
        views = safe_count(raw_views)
        raw_files = s.get("files")
        files = safe_count(raw_files)
        flags = []
        if forever:
            flags.append("无过期时间（长期有效）")
        elif exp_raw in (None, ""):
            flags.append("过期时间未知（缺失字段）")
        elif exp is None:
            flags.append("过期时间无法解析（未知）")
        elif exp <= now:
            flags.append("已过期")
        elif exp - now <= timedelta(days=7):
            flags.append("7 天内将过期")
        if views == 0 and created and (now - created).days >= 30:
            flags.append("30 天以上零访问")
        result.append({
            "share_id": s.get("share_id", "") if type(s.get("share_id")) is str else "",
            "title": s.get("title", "") if type(s.get("title")) is str else "",
            "status": s.get("status", "") if type(s.get("status")) is str else "",
            "views": views,
            "expiration_raw": exp_raw if forever or exp is not None else None,
            "expiration_parsed": exp.isoformat() if exp is not None and not forever else None,
            "created": s.get("created") if created is not None else None,
            "files": files,
            "flags": flags,
        })
    return result


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
    ap.add_argument("--from-fixture", help="离线模式（测试用）")
    ap.add_argument("--now", help="固定审计基准时间（ISO UTC、s:秒或 ms:毫秒）")
    ap.add_argument("--epoch-unit", choices=["auto", "seconds", "milliseconds"], default="auto",
                    help="无前缀数字的单位，应用于 now/expiration/created；auto 优先可表示的秒，否则毫秒")
    ap.add_argument("--json", dest="json_out", help='写入 JSON 报告（"-" 到 stdout，人类可读转 stderr）')
    ap.add_argument("--overwrite", action="store_true", help="明确允许替换已有普通报告文件；不跟随符号链接")
    args = ap.parse_args()
    now = parse_time(args.now, epoch_unit=args.epoch_unit) if args.now else datetime.now(timezone.utc)
    if now is None:
        die("无法解析 --now。")
    now = now.astimezone(timezone.utc)

    fixture = _UNSET_FIXTURE
    if args.from_fixture is not None:
        fixture = load_fixture(args.from_fixture)

    shares = fetch_shares(fixture)
    report = audit(shares, now=now, epoch_unit=args.epoch_unit)

    out = sys.stderr if args.json_out == "-" else sys.stdout

    def say(*a):
        print(*a, file=out)

    say(f"共 {len(report)} 个分享：")
    say()
    for r in report:
        flags = "；".join(r["flags"]) if r["flags"] else "正常"
        say(f"标题：{json.dumps(r['title'] or '(无标题)', ensure_ascii=False)}  [views={r['views']}]")
        say(f"  {json.dumps(r['share_id'], ensure_ascii=False)}  → {flags}")
    problematic = [r for r in report if any(f.startswith(("已过期", "7 天内")) for f in r["flags"])]
    if problematic:
        say()
        say("需人工复核的分享 ID（不生成或执行 shell 命令）：")
        for r in problematic:
            say("  " + json.dumps(r['share_id'], ensure_ascii=False))
    say()
    say("提示：本工具只读；未知字段不能作为撤销依据。")

    if args.json_out:
        text = json.dumps({"generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                           "audited_at": now.isoformat(), "complete": True,
                           "count": len(report), "shares": report}, ensure_ascii=False, indent=2)
        if args.json_out == "-":
            print(text)
        else:
            write_report(args.json_out, text, overwrite=args.overwrite)
            print(f"报告已写入：{args.json_out}")


if __name__ == "__main__":
    main()
