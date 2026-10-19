#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PikPak 批量下载：安全规划、大小校验、本地 SHA-256 清单。

不覆盖已有文件，不提供字节断点续传或远端内容完整性保证。
--dry-run 不下载；只有 --from-fixture --dry-run 完全离线。

PIKPAK_BIN 仅是可信本地启动环境中的可执行文件覆写；命令以参数列表运行，不启用 shell。不要让远端输入、不可信 CI 或多租户调用方控制该环境变量、PATH 或父目录。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import stat
import subprocess
import sys
import time
import tempfile
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
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


def to_int(value) -> int:
    if type(value) is int:
        try:
            text = str(value)
        except (ValueError, OverflowError):
            die("schema_error (size)")
    elif type(value) is str:
        text = value
    else:
        die("schema_error (size)")
    if (not text or len(text) > MAX_DECIMAL_DIGITS
            or not re.fullmatch(r"[0-9]+", text)):
        die("schema_error (size)")
    try:
        return int(text)
    except (ValueError, OverflowError):
        die("schema_error (size)")


def human_size(n: int) -> str:
    units = ("B", "KB", "MB", "GB", "TB")
    try:
        value = float(n)
    except (ValueError, OverflowError):
        try:
            return f"{n} B" if len(str(n)) <= MAX_DECIMAL_DIGITS else "未知"
        except (ValueError, OverflowError):
            return "未知"
    i = 0
    while value >= 1024 and i < len(units) - 1:
        value /= 1024.0
        i += 1
    return f"{value:.0f} {units[i]}" if i == 0 else f"{value:.1f} {units[i]}"


def sanitize(name: str) -> str:
    name = name.replace("/", "_").replace("\\", "_").replace("\x00", "")
    name = re.sub(r"^\.+", "_", name)
    return name or "_"


def pikpak(*args: str, timeout: int = 3600):
    try:
        proc = subprocess.run([os.environ.get("PIKPAK_BIN", "pikpak"), *args],
                              capture_output=True, text=True, timeout=timeout)
        if proc.returncode:
            return proc.returncode, "", f"cli_failed (exit_code={proc.returncode})"
        return proc.returncode, proc.stdout, proc.stderr
    except FileNotFoundError:
        return 127, "", "cli_unavailable (exit_code=127)"
    except subprocess.TimeoutExpired:
        return 124, "", "cli_timeout (exit_code=124)"
    except OSError:
        return 126, "", "cli_os_error (exit_code=126)"


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
        if "size" in row and (type(row["size"]) not in (int, str)
                               or isinstance(row["size"], bool)):
            die("schema_error (ls_size)")
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
    rc, out, err = pikpak("ls", "--raw", "-l", "500", *(["-p", folder_id] if folder_id else []),
                          *(["-t", page_token] if page_token else []),
                          timeout=min(int(os.environ.get("PIKPAK_TIMEOUT", "90")), timeout) if timeout is not None else int(os.environ.get("PIKPAK_TIMEOUT", "90")))
    if rc:
        category = "cli_unavailable" if rc == 127 else "cli_timeout" if rc == 124 else "cli_failed"
        die(f"{category} (exit_code={rc})")
    return validate_page(decode_json(out, "ls_json"))


def walk(folder_id: str, fixture: "dict | None", rel_path, out, counters, max_items: int) -> None:
    folders = counters.setdefault("_folder_ids", set())
    if folder_id in folders:
        die("目录 ID 重复或形成循环，已中止。")
    folders.add(folder_id)
    token, tokens, names = "", set(), set()
    while True:
        if token in tokens:
            die("分页 token 重复，拒绝不完整备份。")
        tokens.add(token)
        remaining = counters.setdefault("_deadline", time.monotonic() + counters.get("_scan_seconds", 900)) - time.monotonic()
        if counters.get("_pages", 0) >= counters.get("_max_pages", 10000) or remaining <= 0:
            die("scan_budget_exceeded (incomplete)")
        counters["_pages"] = counters.get("_pages", 0) + 1
        page = ls_page(folder_id, fixture, token, timeout=remaining)
        if time.monotonic() >= counters["_deadline"]:
            die("scan_budget_exceeded (incomplete)")
        for f in page["files"]:
            name = sanitize(f.get("name", ""))
            key = unicodedata.normalize("NFC", name).casefold()
            if key in names or (not rel_path and key == "backup_manifest.json"):
                die(f"文件/目录名称碰撞或保留名称：{name}")
            names.add(key)
            if f.get("kind") == "drive#folder":
                counters["folders"] += 1
                if counters["folders"] > 5000 or len(rel_path) >= 100:
                    die("目录数量/深度超过安全上限。")
                if not f.get("id"):
                    die("目录缺少 ID。")
                walk(f["id"], fixture, rel_path + [name], out, counters, max_items)
            elif f.get("kind") == "drive#file":
                counters["files"] += 1
                if counters["files"] > max_items:
                    die(f"文件数超过安全上限（{max_items}）。")
                out.append((rel_path, f))
        token = page["next_page_token"]
        if not token:
            break


def open_dir(root: Path, parts=(), create=False) -> int:
    """Open every component without following symlinks (POSIX dir_fd)."""
    fd = os.open(root.anchor, os.O_RDONLY | os.O_DIRECTORY)
    try:
        components = list(root.parts[1:]) + list(parts)
        for component in components:
            if component in ("", ".", "..") or "/" in component or "\\" in component:
                raise ValueError("不安全路径分量")
            if create:
                try:
                    os.mkdir(component, mode=0o700, dir_fd=fd)
                except FileExistsError:
                    pass
            nxt = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = nxt
        return fd
    except BaseException:
        os.close(fd)
        raise


def plan_files(dest, files):
    names, plan = {}, []
    for rel, f in files:
        parts = [*rel, sanitize(f.get("name", ""))]
        if any(not p or p in (".", "..") or "/" in p or "\\" in p for p in parts):
            die("不安全的相对路径。")
        for i in range(1, len(parts) + 1):
            key = tuple(unicodedata.normalize("NFC", p).casefold() for p in parts[:i])
            kind = "file" if i == len(parts) else "directory"
            prior = names.get(key)
            if prior and (kind == "file" or prior != (kind, tuple(parts[:i]))):
                die("清洗/大小写/Unicode 归一化后路径碰撞。")
            names[key] = (kind, tuple(parts[:i]))
        if unicodedata.normalize("NFC", parts[0]).casefold() == "backup_manifest.json":
            die("远端名称占用了备份清单保留路径。")
        size = to_int(f.get("size"))
        if not f.get("id"):
            die("文件缺少 ID。")
        current = dest
        for p in parts:
            current /= p
            if current.is_symlink():
                die(f"拒绝符号链接：{current}")
        if current.exists():
            die(f"目标已存在，拒绝覆盖或仅按大小跳过：{current}")
        plan.append((parts, f, size))
    manifest = dest / "backup_manifest.json"
    if manifest.exists() or manifest.is_symlink():
        die("备份清单已存在；请使用一个新的空目标目录，避免覆盖。")
    return plan


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--folder", default="")
    ap.add_argument("--dest", required=True)
    ap.add_argument("--from-fixture", help="完全离线，必须同时 --dry-run")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--max-items", type=int, default=50000)
    ap.add_argument("--max-pages", type=int, default=10000, help="全树列表页数上限，超限标 incomplete")
    ap.add_argument("--scan-timeout", type=float, default=900, help="列表扫描总秒数预算；不含报告生成/下载/正则执行")
    args = ap.parse_args()
    if args.max_pages < 1 or not math.isfinite(args.scan_timeout) or args.scan_timeout <= 0 or args.max_items < 1:
        die("扫描预算和 max-items 必须为有限正数。")
    if args.max_items < 1:
        die("max-items 必须为正数。")
    if args.from_fixture is not None and not args.dry_run:
        die("fixture 模式必须使用 --dry-run，不允许下载。")
    fixture = None
    if args.from_fixture is not None:
        fixture = load_fixture(args.from_fixture)
    dest = Path(args.dest).expanduser().absolute()
    files, counters = [], {"files": 0, "folders": 0, "_max_pages": args.max_pages, "_scan_seconds": args.scan_timeout}
    walk(args.folder, fixture, [], files, counters, args.max_items)
    plan = plan_files(dest, files)
    print(f"计划备份：{counters['folders']} 个目录、{len(plan)} 个文件、{human_size(sum(p[2] for p in plan))}")
    print(f"目标目录：{dest}")
    if args.dry_run:
        for parts, f, size in plan[:50]:
            print(f"  {human_size(size):>10}  {'/'.join(parts)}")
        print("--dry-run：未实际下载；现有文件冲突会中止。")
        return
    if not dest.is_dir():
        die("目标目录必须已存在。")
    try:
        root_fd = open_dir(dest)
    except (OSError, ValueError) as exc:
        die(f"目标路径不安全：{exc}")
    manifest = {"schema_version": 1, "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "folder": args.folder, "dest": str(dest), "remote_integrity": "unverified", "files": []}
    failed = 0
    try:
        with tempfile.TemporaryDirectory(prefix=".pikpak-transfer-", dir=dest) as tmp:
            for index, (parts, f, size) in enumerate(plan):
                entry = {"id": f["id"], "path": "/".join(parts), "size": size, "status": "failed"}
                stage = Path(tmp) / str(index)
                target_fd = None
                try:
                    target_fd = open_dir(dest, parts[:-1], create=True)
                    print(f"  下载：{entry['path']}")
                    rc, out, err = pikpak("download", f["id"], "-o", str(stage))
                    if rc:
                        raise ValueError(f"cli_failed (exit_code={rc})")
                    fd = os.open(stage, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW)
                    try:
                        st = os.fstat(fd)
                        if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1 or st.st_size != size:
                            raise ValueError("下载不是常规文件或大小不符")
                        os.fchmod(fd, 0o600)
                        with os.fdopen(fd, "rb") as stream:
                            fd = None
                            digest = hashlib.sha256()
                            for block in iter(lambda: stream.read(1024 * 1024), b""):
                                digest.update(block)
                            os.fsync(stream.fileno())
                    finally:
                        if fd is not None:
                            os.close(fd)
                    # Hard-link publication is atomic and fails if a target appeared.
                    os.link(stage, parts[-1], dst_dir_fd=target_fd, follow_symlinks=False)
                    entry.update(status="ok", sha256=digest.hexdigest(), verification="size_only")
                except (OSError, ValueError) as exc:
                    failed += 1
                    entry["error"] = str(exc)
                finally:
                    if target_fd is not None:
                        os.close(target_fd)
                manifest["files"].append(entry)
            staged_manifest = Path(tmp) / "manifest"
            manifest_fd = os.open(
                staged_manifest,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_NONBLOCK,
                0o600,
            )
            try:
                manifest_st = os.fstat(manifest_fd)
                if not stat.S_ISREG(manifest_st.st_mode) or manifest_st.st_nlink != 1:
                    raise ValueError("清单不是常规文件或存在别名")
                os.fchmod(manifest_fd, 0o600)
                with os.fdopen(manifest_fd, "w", encoding="utf-8") as fh:
                    manifest_fd = None
                    json.dump(manifest, fh, ensure_ascii=False, indent=2)
                    fh.flush()
                    os.fsync(fh.fileno())
            finally:
                if manifest_fd is not None:
                    os.close(manifest_fd)
            os.link(staged_manifest, "backup_manifest.json", dst_dir_fd=root_fd, follow_symlinks=False)
    except (OSError, ValueError) as exc:
        die(f"备份失败：{exc}")
    finally:
        os.close(root_fd)
    print(f"完成：成功 {len(plan) - failed}、失败 {failed}；清单：{dest / 'backup_manifest.json'}")
    if failed:
        die("存在失败项；未完成内容未发布，不支持断点续传。")


if __name__ == "__main__":
    main()
