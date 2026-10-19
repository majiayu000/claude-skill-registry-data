#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PikPak WebDAV 元数据提示（不验证 WebDAV 权限或传输配额）。

默认不访问账号。开发/演示使用中性 fixture：
  python3 webdav_check.py --from-fixture metadata.json --json

仅在已确认自有账号且授权本次查询后：
  python3 webdav_check.py --account-owner-confirmed --json

CLI 元数据中的会员状态不是 WebDAV 开通/连接验收；存储空间不是传输配额。
PIKPAK_BIN 可指定官方 CLI 路径；本工具不读取认证缓存、不生成凭据。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from typing import NoReturn


def die(msg: str, code: int = 1) -> NoReturn:
    print(f"错误：{msg}", file=sys.stderr)
    raise SystemExit(code)


def pikpak_json(*args: str, timeout: int = 60):
    bin_path = os.environ.get("PIKPAK_BIN", "pikpak")
    try:
        proc = subprocess.run([bin_path, *args, "-F", "json"],
                              capture_output=True, text=True, timeout=timeout)
    except FileNotFoundError:
        return None, f"找不到 pikpak 命令（官方安装页：https://mypikpak.com/cli）"
    except subprocess.TimeoutExpired:
        return None, "pikpak 命令超时"
    except (OSError, UnicodeError):
        return None, "无法执行或解码 pikpak 输出；请在本机检查安装和权限"
    if proc.returncode != 0:
        return None, f"pikpak 调用失败（退出码 {proc.returncode}）；原始输出仅在本机检查，不回显私密字段"
    try:
        return json.loads(proc.stdout), None
    except json.JSONDecodeError:
        return None, "无法解析 pikpak 输出"


def storage_value(value):
    """Allow only bounded nonnegative byte integers or size-display text.

    This is an unverified CLI display field, not a quota measurement. Never
    stringify containers or arbitrary strings from account metadata.
    """
    if type(value) is int and 0 <= value <= (1 << 63) - 1:
        return value
    if (isinstance(value, str) and len(value) <= 64
            and re.fullmatch(r"(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?: (?:B|[KMGTPE]i?B))?", value)):
        return value
    return None


def vip_label(value, allowed):
    """Only export adapter-supported labels, never arbitrary account strings."""
    if type(value) is not str or len(value) > 32:
        return "unknown"
    label = value.strip().lower()
    return label if label in allowed else "unknown"


def vip_expiry(value):
    """Accept a bounded, timezone-aware ISO timestamp; discard rejected input."""
    if (type(value) is not str or len(value) > 40
            or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?(?:Z|[+-][0-9]{2}:[0-9]{2})", value)):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed if parsed.tzinfo is not None else None
    except ValueError:
        return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", dest="json_out", action="store_true", help="JSON 输出")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--account-owner-confirmed", action="store_true", help="确认账号为本人所有且授权本次只读元数据查询")
    mode.add_argument("--from-fixture", metavar="FILE", help="离线中性 JSON 元数据，不访问账号或网络")
    args = ap.parse_args()
    if args.from_fixture is not None:
        try:
            with open(args.from_fixture, encoding="utf-8") as stream:
                raw = stream.read(1024 * 1024 + 1)
            if len(raw) > 1024 * 1024:
                die("fixture 超出 1 MiB 字符预算")
            status = json.loads(raw)
        except (OSError, UnicodeError, json.JSONDecodeError):
            die("无法读取中性 JSON fixture；不回显文件内容")
    elif args.account_owner_confirmed:
        status, err = pikpak_json("auth", "status")
        if err or status is None:
            die(f"获取账号状态失败：{err}")
    else:
        ap.error("默认不访问账号；用 --from-fixture 离线检查，或自有账号授权本次查询后用 --account-owner-confirmed")

    if not isinstance(status, dict):
        die("账号元数据 schema 错误：根值必须是对象")
    if status.get("logged_in") is not None and not isinstance(status["logged_in"], bool):
        die("账号元数据 schema 错误：logged_in 必须是布尔值")
    for key in ("vip", "storage"):
        if status.get(key) is not None and not isinstance(status[key], dict):
            die(f"账号元数据 schema 错误：{key} 必须是对象")
    for key in ("type", "status", "expire_time"):
        value = (status.get("vip") or {}).get(key)
        if value is not None and not isinstance(value, str):
            die(f"账号元数据 schema 错误：vip.{key} 必须是字符串")
    logged_in = status.get("logged_in")
    result = {
        "schema_version": 1,
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "source": "fixture" if args.from_fixture is not None else "cli_metadata",
        "logged_in": logged_in,
        "can_use_webdav": None,
        "membership": {"state": "unknown", "verification": "cli_metadata_only"},
        "webdav_connection": "not_tested",
        "transfer_quota": {"state": "unknown", "reason": "storage_is_not_transfer_quota"},
        "checks": [],
    }

    if logged_in is None:
        result["checks"].append("登录状态未知：元数据缺失或为 null；WebDAV 权限保持未验证")
        emit(result, args.json_out)
        return
    if logged_in is False:
        result["checks"].append("未登录：先运行 `pikpak auth login`")
        emit(result, args.json_out)
        return

    vip = status.get("vip") or {}
    # These labels describe this adapter's fixture contract, not verified rights.
    vip_type = vip_label(vip.get("type"), {"platinum", "free", "none"})
    vip_status = vip_label(vip.get("status"), {"ok", "active", "expired", "inactive", "disabled"})
    expires_at = vip_expiry(vip.get("expire_time"))
    expire = expires_at.isoformat() if expires_at is not None else ""
    membership_state = "unknown"
    if vip_type in ("free", "none"):
        membership_state = "reported_free"
    elif vip_type == "platinum" and vip_status in ("expired", "inactive", "disabled"):
        membership_state = "reported_expired"
    elif vip_type == "platinum" and vip_status in ("ok", "active") and expires_at is not None:
        membership_state = ("reported_expired" if expires_at <= datetime.now().astimezone()
                            else "reported_current")

    result["vip"] = {"type": vip_type, "status": vip_status, "expire_time": expire}
    result["membership"] = {"state": membership_state, "verification": "cli_metadata_only"}
    result["can_use_webdav"] = None
    result["webdav_connection"] = "not_tested"
    result["transfer_quota"] = {"state": "unknown", "reason": "storage_is_not_transfer_quota"}
    result["checks"].append(f"CLI 会员元数据提示：{membership_state}；不是服务端 WebDAV 权限验收")
    result["checks"].append("WebDAV 开通、凭据有效性和实际传输配额均未检查；请在官方账户页面核对")

    storage = status.get("storage") or {}
    result["storage"] = {
        key: storage_value(storage.get(key)) for key in ("total", "used", "in_trash")
    }
    if any(storage.get(key) is not None and result["storage"][key] is None
           for key in ("total", "used", "in_trash")):
        result["checks"].append("存储字段含未知类型或格式：已置为 null，不导出原始值")
    trash = result["storage"]["in_trash"]
    if trash not in (None, 0, "0", "0 B"):
        result["checks"].append(f"CLI 回收站存储提示：{trash}；未验证恢复或释放容量语义")

    result["checks"].append("提示：WebDAV 属于「已连接的应用」，与 CLI/MCP 共享月度配额的 25%（触顶降速至约 100 KB/s）")
    result["checks"].append("配置入口：PikPak 网页版 → 设置 → 访问与集成 → WebDAV")

    emit(result, args.json_out)


def emit(result: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    print("═══ PikPak WebDAV 准备检查 ═══")
    login_label = {True: "已登录", False: "未登录", None: "未知"}[result["logged_in"]]
    access_label = {True: "是", False: "否", None: "未验证"}[result.get("can_use_webdav")]
    print(f"登录状态：{login_label}")
    print(f"可用 WebDAV：{access_label}")
    print()
    for c in result.get("checks", []):
        print(f"  {c}")


if __name__ == "__main__":
    main()
