#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PikPak 速度问题诊断（只读）：网络连通性 + 延迟测试 + 方案建议。

不下载、不修改、不接触用户凭据；只做 HTTP 连通性和延迟探测。

用法：
  python3 speed_diag.py
  python3 speed_diag.py --json
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import json
import socket
import ssl
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime


TARGETS = [
    ("主站 mypikpak.com", "https://mypikpak.com"),
    ("WebDAV 入口 dav.mypikpak.com", "https://dav.mypikpak.com"),
    ("API api-drive.mypikpak.com", "https://api-drive.mypikpak.com"),
]


_transport_spec = importlib.util.spec_from_file_location("pikpak_direct_transport", Path(__file__).with_name("speed_bench.py"))
assert _transport_spec and _transport_spec.loader
transport = importlib.util.module_from_spec(_transport_spec)
_transport_spec.loader.exec_module(transport)


def probe(url: str, timeout: float = 8.0):
    """HEAD only: pinned public HTTPS, no redirects/proxies; loopback HTTP for tests."""
    result = {"host": "", "route": "direct_no_proxy", "ok": False}
    if type(timeout) not in (int, float) or not 0 < timeout <= transport.MAX_TIMEOUT:
        result["http_error"] = "invalid_input"
        return result
    t0 = time.perf_counter()
    try:
        parsed = transport.validate_url(url)
        result["host"] = parsed.hostname
        destination = transport.resolve_destination(parsed)
        result["dns_ms"] = round((time.perf_counter() - t0) * 1000, 1)
        result["resolved_ips"] = [entry[3][0] for entry in destination["endpoints"]]
    except transport.DestinationDenied:
        result["http_error"] = "destination_denied"
        return result
    except socket.gaierror:
        result["dns_error"] = "dns_error"
        return result
    except (ValueError, OSError):
        result["http_error"] = "invalid_input_or_resolution_failed"
        return result

    t1 = time.perf_counter()
    try:
        req = urllib.request.Request(url, method="HEAD",
                                     headers={"User-Agent": "pikpak-skills-head/1"})
        with transport.direct_opener(destination).open(req, timeout=timeout) as resp:
            result["http_status"] = resp.status
    except urllib.error.HTTPError as exc:
        result["http_status"] = exc.code
        if exc.fp is not None:
            exc.close()
        if 300 <= exc.code < 400:
            result["http_error"] = "redirect_denied"
    except transport.DestinationDenied:
        result["http_error"] = "destination_denied"
    except Exception:
        result["http_error"] = "connection_failed"  # Never repeat URL-bearing errors.
    result["total_ms"] = round((time.perf_counter() - t1) * 1000, 1)
    if "connected_ip" in destination:
        result["connected_ip"] = destination["connected_ip"]
        result["ip"] = destination["connected_ip"]
    result["ok"] = "http_error" not in result
    return result


def recommend(results: list[dict], vip_info: str = "") -> list[str]:
    """Describe observations without attributing a network root cause."""
    tips = ["HEAD 探测不能测量下载吞吐，也不能据此判定运营商 QoS 或账号限速。"]
    if not results:
        return tips + ["没有探测数据，尚不能提出网络结论。"]
    ok_count = sum(1 for r in results if r.get("ok"))
    slow = [r for r in results if r.get("ok") and r.get("total_ms", 0) > 1500]
    if ok_count == 0:
        tips.append("本次所有目标不可达；先核对本机网络和既有代理配置，不自动更改设置。")
    elif ok_count < len(results):
        tips.append("部分目标未响应；DNS、TLS、代理、服务状态均可能影响结果，根因待对照验证。")
    if slow:
        names = "、".join(r["host"] for r in slow)
        tips.append(f"本次 HTTP 响应超过 1.5s：{names}；这是延迟观察，不是限速证据。")
    for r in results:
        status = r.get("http_status", 0)
        if status in (401, 403):
            tips.append(f"{r['host']} 返回 HTTP {status}：已收到 HTTP 响应，但认证或访问受限。")
        elif status >= 500:
            tips.append(f"{r['host']} 返回 HTTP {status}：服务或中间代理错误，不等于服务健康。")
    if ok_count:
        tips.append("换网络或时段做同文件对比，并记录是否经过既有代理；不要一次改变多个条件。")
        tips.append("WebDAV 和本地代理仅是待验证的替代路径，不保证提速，也不突破会员或流量限制。")
    return tips


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", dest="json_out", action="store_true")
    args = ap.parse_args()

    results = [probe(url) for _, url in TARGETS]
    tips = recommend(results)

    report = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "results": results,
        "recommendations": tips,
    }

    if args.json_out:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    print("═══ PikPak 网络诊断 ═══")
    print()
    for name, r in zip([n for n, _ in TARGETS], results):
        if r.get("ok"):
            print(f"  ✓ {name}")
            print(f"      DNS {r.get('dns_ms')}ms | 总响应 {r.get('total_ms')}ms | IP {r.get('ip')}")
        else:
            err = r.get("dns_error") or r.get("http_error") or "未知错误"
            print(f"  ✗ {name} — {err}")
    print()
    print("诊断建议：")
    for t in tips:
        print(f"  {t}")


if __name__ == "__main__":
    main()
