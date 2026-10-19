#!/usr/bin/env python3
"""Bounded HTTP sample measurement. No account access or source URLs in reports."""
from __future__ import annotations

import hashlib
import http.client
import ipaddress
import json
import math
import os
import stat
import re
import socket
import ssl
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

MAX_SAMPLE_BYTES = 16 * 1024 * 1024
MAX_TIMEOUT = 60.0


def validate_url(url: str) -> urllib.parse.SplitResult:
    """Allow HTTPS, or explicitly requested loopback HTTP; never URL userinfo."""
    if not isinstance(url, str) or not url or any(ord(c) < 33 for c in url):
        raise ValueError("invalid_url")
    parsed = urllib.parse.urlsplit(url)
    host = parsed.hostname
    if not host or parsed.username is not None or parsed.password is not None or parsed.fragment:
        raise ValueError("invalid_url")
    port = parsed.port  # Validate separately; never reinterpret an explicit zero as a default.
    if port == 0:
        raise ValueError("invalid_port")
    try:
        local = host.lower() == "localhost" or ipaddress.ip_address(host).is_loopback
    except ValueError:
        local = host.lower() == "localhost"
    if parsed.scheme != "https" and not (parsed.scheme == "http" and local):
        raise ValueError("https_required")
    return parsed


class DestinationDenied(ValueError):
    """The initial URL or actual endpoint violates the destination policy."""


def resolve_destination(parsed):
    """Resolve once: HTTPS must be globally routable; explicit HTTP is loopback only."""
    host = parsed.hostname or ""
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    local_http = parsed.scheme == "http"
    records = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
    if not records:
        raise DestinationDenied("destination_denied")
    endpoints = []
    for family, kind, proto, _, address in records:
        try:
            ip = ipaddress.ip_address(address[0])
            permitted = ip.is_loopback if local_http else (ip.is_global and not ip.is_multicast and not ip.is_reserved)
            if ip.version == 6 and ip.ipv4_mapped is not None:
                permitted = permitted and ip.ipv4_mapped.is_global
            if (not permitted or "%" in address[0] or address[1] != port
                    or family not in (socket.AF_INET, socket.AF_INET6) or kind != socket.SOCK_STREAM
                    or proto != socket.IPPROTO_TCP):
                raise DestinationDenied("destination_denied")
        except (ValueError, TypeError, IndexError) as exc:
            raise DestinationDenied("destination_denied") from exc
        endpoint = (family, kind, proto, address)
        if endpoint not in endpoints:
            endpoints.append(endpoint)
    return {"host": host, "port": port, "scheme": parsed.scheme, "endpoints": endpoints}


def _connect_pinned(destination, timeout):
    """Connect numeric sockaddrs only, with no second resolver/proxy step."""
    last_error = None
    for family, kind, proto, address in destination["endpoints"]:
        sock = socket.socket(family, kind, proto)
        try:
            sock.settimeout(timeout)
            sock.connect(address)
            peer = sock.getpeername()
            if ipaddress.ip_address(peer[0]) != ipaddress.ip_address(address[0]) or peer[1] != address[1]:
                raise DestinationDenied("destination_denied")
            destination["connected_ip"] = str(ipaddress.ip_address(peer[0]))
            return sock
        except OSError as exc:
            last_error = exc
            sock.close()
        except Exception:
            sock.close()
            raise
    raise last_error or OSError("connection_failed")


class _PinnedHTTPConnection(http.client.HTTPConnection):
    def __init__(self, host, destination, **kwargs):
        self.destination = destination
        super().__init__(host, **kwargs)

    def connect(self):
        if self._tunnel_host:
            raise DestinationDenied("proxy_not_supported")
        self.sock = _connect_pinned(self.destination, self.timeout)


class _PinnedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, host, destination, **kwargs):
        self.destination = destination
        super().__init__(host, context=ssl.create_default_context(), **kwargs)

    def connect(self):
        if self._tunnel_host:
            raise DestinationDenied("proxy_not_supported")
        raw = _connect_pinned(self.destination, self.timeout)
        try:
            self.sock = self._context.wrap_socket(raw, server_hostname=self.host)
        except Exception:
            raw.close()
            raise


class _DirectHTTPHandler(urllib.request.HTTPHandler):
    def __init__(self, destination):
        super().__init__()
        self.destination = destination

    def http_open(self, req):
        return self.do_open(lambda host, **kw: _PinnedHTTPConnection(host, self.destination, **kw), req)


class _DirectHTTPSHandler(urllib.request.HTTPSHandler):
    def __init__(self, destination):
        super().__init__()
        self.destination = destination

    def https_open(self, req):
        return self.do_open(lambda host, **kw: _PinnedHTTPSConnection(host, self.destination, **kw), req)


def direct_opener(destination):
    """No environment/system proxies; redirects are rejected for every request."""
    return urllib.request.build_opener(urllib.request.ProxyHandler({}), SafeRedirect(),
                                      _DirectHTTPHandler(destination), _DirectHTTPSHandler(destination))


class SafeRedirect(urllib.request.HTTPRedirectHandler):
    """Reject every redirect, closing rather than draining its response body."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("redirect_denied")

    def http_error_302(self, req, fp, code, msg, headers):
        # urllib's inherited handler calls fp.read() with no size before following.
        # Do not invoke it, including for a same-origin/loopback destination.
        error = urllib.error.HTTPError(req.full_url, code, "redirect_denied", headers, fp)
        error.close()  # Close the owned stream and mark the error wrapper closed.
        raise error

    http_error_301 = http_error_303 = http_error_307 = http_error_308 = http_error_302


def validate_parameters(url, sample_bytes, timeout):
    parsed = validate_url(url)
    if type(sample_bytes) is not int or not 1 <= sample_bytes <= MAX_SAMPLE_BYTES:
        raise ValueError("invalid_sample_bytes")
    if (not isinstance(timeout, (int, float)) or isinstance(timeout, bool)
            or not 0 < timeout <= MAX_TIMEOUT or not math.isfinite(timeout)):
        raise ValueError("invalid_timeout")
    return parsed


def _read_sample(url: str, sample_bytes: int, timeout: float) -> dict:
    try:
        parsed = validate_parameters(url, sample_bytes, timeout)
    except (ValueError, TypeError, OverflowError):
        return {"ok": False, "error": "invalid_input"}
    req = urllib.request.Request(url, headers={
        "Range": f"bytes=0-{sample_bytes - 1}",
        "Accept-Encoding": "identity",
        "Connection": "close",
        "User-Agent": "pikpak-skills-sample/1",
    })
    started = time.perf_counter()
    result = {"ok": False, "requested_bytes": sample_bytes, "bytes_read": 0,
              "route": "direct_no_proxy"}
    try:
        destination = resolve_destination(parsed)
        opener = direct_opener(destination)
        with opener.open(req, timeout=timeout) as response:
            result["connected_ip"] = destination["connected_ip"]
            result["http_status"] = response.status
            if response.status != 206:
                result["error"] = "range_not_honored"
                return result
            ranges = response.headers.get_all("Content-Range", [])
            if len(ranges) != 1:
                result["error"] = "invalid_content_range"
                return result
            match = re.fullmatch(r"bytes (\d+)-(\d+)/(\d+)", ranges[0])
            if not match:
                result["error"] = "invalid_content_range"
                return result
            start, end, total = map(int, match.groups())
            expected = min(sample_bytes, total)
            if start != 0 or total <= 0 or end != expected - 1:
                result["error"] = "invalid_content_range"
                return result
            encodings = response.headers.get_all("Content-Encoding", [])
            if len(encodings) > 1 or (encodings and encodings[0].lower() != "identity"):
                result["error"] = "unexpected_encoding"
                return result
            lengths = response.headers.get_all("Content-Length", [])
            if (response.headers.get_all("Transfer-Encoding", []) or len(lengths) != 1
                    or not re.fullmatch(r"[0-9]+", lengths[0]) or int(lengths[0]) != expected):
                result["error"] = "invalid_framing"
                return result
            # We request connection-close and require EOF after the declared sample.
            # HTTPResponse.read caps at Content-Length and can hide excess wire bytes;
            # read the bounded underlying stream instead, including one sentinel byte.
            first_byte = response.fp.read(1)
            result["ttfb_ms"] = round((time.perf_counter() - started) * 1000, 3)
            body = first_byte + response.fp.read(expected)
            result["bytes_read"] = len(body)
            if len(body) != expected:
                result["error"] = "sample_length_mismatch"
                return result
            elapsed = time.perf_counter() - started
            result.update(ok=True, total_bytes=total, elapsed_seconds=elapsed,
                          sample_sha256=hashlib.sha256(body).hexdigest(),
                          mib_per_second=len(body) / (1024 * 1024) / elapsed)
            return result
    except DestinationDenied:
        result["error"] = "destination_denied"
    except urllib.error.HTTPError as exc:
        result.update(error="redirect_denied" if 300 <= exc.code < 400 else "http_error", http_status=exc.code)
        if exc.fp is not None:
            exc.close()  # Never drain error or redirect bodies.
    except (TimeoutError, socket.timeout):
        result["error"] = "timeout"
    except ssl.SSLError:
        result["error"] = "tls_error"
    except urllib.error.URLError as exc:
        reason = exc.reason
        if isinstance(reason, (TimeoutError, socket.timeout)):
            result["error"] = "timeout"
        elif isinstance(reason, ssl.SSLError):
            result["error"] = "tls_error"
        elif isinstance(reason, socket.gaierror):
            result["error"] = "dns_error"
        else:
            result["error"] = "connection_error"
    except Exception:
        # Exception messages may contain a signed URL: never echo them.
        result["error"] = "measurement_error"
    return result


def measure(url: str, sample_bytes: int = 4 * 1024 * 1024, timeout: float = 10.0) -> dict:
    """Isolate DNS/HTTP in a killable worker to enforce a wall-clock deadline."""
    try:
        validate_parameters(url, sample_bytes, timeout)
    except (ValueError, TypeError, OverflowError):
        return {"ok": False, "error": "invalid_input"}
    try:
        proc = subprocess.run(
            [sys.executable, __file__, "--worker"],
            input=json.dumps({"url": url, "sample_bytes": sample_bytes, "timeout": timeout}),
            text=True, capture_output=True, timeout=timeout + 0.5,
        )
        if proc.returncode:
            return {"ok": False, "error": "worker_error"}
        return json.loads(proc.stdout)
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "deadline_exceeded"}
    except Exception:
        return {"ok": False, "error": "worker_error"}


def _finite_number(value, *, positive=False):
    try:
        return (isinstance(value, (int, float)) and not isinstance(value, bool)
                and math.isfinite(value) and (value > 0 if positive else value >= 0))
    except (TypeError, ValueError, OverflowError):
        return False


def _valid_measurement(item):
    size, total, digest = (item.get(key) for key in ("bytes_read", "total_bytes", "sample_sha256"))
    return (type(size) is int and 1 <= size <= MAX_SAMPLE_BYTES and type(total) is int and total >= size
            and isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest) is not None
            and _finite_number(item.get("mib_per_second"), positive=True)
            and _finite_number(item.get("elapsed_seconds"), positive=True)
            and _finite_number(item.get("ttfb_ms")))


def compare(baseline: list[dict], candidate: list[dict]) -> dict:
    """Only compare complete finite metrics for identical prefix samples."""
    import statistics

    invalid = {"comparable": False, "reason": "invalid_measurement"}
    if not isinstance(baseline, list) or not isinstance(candidate, list):
        return invalid
    combined = baseline + candidate
    if any(not isinstance(item, dict) for item in combined):
        return invalid
    if not baseline or not candidate or any(item.get("ok") is not True for item in combined):
        return {"comparable": False, "reason": "incomplete_measurement"}
    if any(not _valid_measurement(item) for item in combined):
        return invalid
    signatures = {(item["bytes_read"], item["total_bytes"], item["sample_sha256"]) for item in combined}
    if len(signatures) != 1:
        return {"comparable": False, "reason": "sample_mismatch"}
    before = statistics.median(item["mib_per_second"] for item in baseline)
    after = statistics.median(item["mib_per_second"] for item in candidate)
    if not _finite_number(before, positive=True) or not _finite_number(after, positive=True):
        return invalid
    ratio = after / before
    delta = statistics.median(item["ttfb_ms"] for item in candidate) - statistics.median(item["ttfb_ms"] for item in baseline)
    if not _finite_number(ratio, positive=True) or not math.isfinite(delta):
        return invalid
    return {"comparable": True, "scope": "prefix_sample_only",
            "baseline_median_mib_s": before, "candidate_median_mib_s": after,
            "throughput_ratio": ratio, "ttfb_delta_ms": delta}


def read_private_url_file(source):
    """Unix private regular file only; no FIFO wait or final symlink following.

    Network --timeout is not a deadline for potentially stalled filesystem I/O.
    """
    if not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "getuid"):
        raise ValueError("secure_file_open_unavailable")
    fd = os.open(source, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0))
    try:
        before = os.fstat(fd)
        if (not stat.S_ISREG(before.st_mode) or before.st_uid != os.getuid()
                or stat.S_IMODE(before.st_mode) & 0o077 or not 1 <= before.st_size <= 16384):
            raise ValueError("invalid_private_file")
        content = bytearray()
        while len(content) <= 16384:
            block = os.read(fd, 16385 - len(content))
            if not block:
                break
            content.extend(block)
        after = os.fstat(fd)
        if (len(content) != before.st_size or
                (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_mode, before.st_uid)
                != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_mode, after.st_uid)):
            raise ValueError("url_file_changed")
        value = bytes(content).decode("utf-8").strip()
        validate_url(value)
        return value
    finally:
        os.close(fd)


def main() -> int:
    import argparse
    from datetime import datetime

    parser = argparse.ArgumentParser(description="Measure a bounded prefix sample; no PikPak account calls.")
    parser.add_argument("--baseline-url-file", required=True, help="Private local text file containing the authorized sample URL")
    parser.add_argument("--candidate-url-file", help="Private local file containing the alternate path to the SAME sample")
    parser.add_argument("--bytes", dest="sample_bytes", type=int, default=4 * 1024 * 1024)
    parser.add_argument("--repeat", type=int, default=3)
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.sample_bytes <= MAX_SAMPLE_BYTES or not 1 <= args.repeat <= 5 or not 0 < args.timeout <= MAX_TIMEOUT:
        parser.error("bytes must be 1..16777216, repeat 1..5, timeout >0 and <=60")
    urls = {}
    try:
        for label, source in [("baseline", args.baseline_url_file), ("candidate", args.candidate_url_file)]:
            if source is not None:
                urls[label] = read_private_url_file(source)
    except (OSError, ValueError, UnicodeError):
        print(json.dumps({"ok": False, "error": "invalid_url_file"}))
        return 2
    samples = {label: [] for label in urls}
    for iteration in range(args.repeat):
        order = list(urls)
        if iteration % 2:
            order.reverse()
        for label in order:
            samples[label].append(measure(urls[label], args.sample_bytes, args.timeout))
    comparison = compare(samples["baseline"], samples.get("candidate", []))
    report = {
        "schema_version": 1,
        "route": "direct_no_proxy",
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "requested_body_bytes_max": args.sample_bytes * args.repeat * len(urls),
        "baseline": samples["baseline"], "candidate": samples.get("candidate", []),
        "comparison": comparison,
        "limitations": ["Prefix samples only, not full-file integrity verification.",
                        "direct_no_proxy ignores system/environment proxies; this is not a proxy-chain A/B test.",
                        "Application body reads include at most one extra framing sentinel; headers, TLS and socket buffers are not the sample budget.",
                        "Requested byte ranges do not bound upstream proxy prefetch or billing.",
                        "Cache, route and time-of-day can affect this measurement; no guaranteed speedup."],
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("PikPak 有限样本测量（不访问账号）")
        print("direct_no_proxy：不沿用系统/环境代理；不是用户既有代理链的 A/B 测速。")
        for label, values in samples.items():
            for index, value in enumerate(values, 1):
                if value.get("ok"):
                    print(f"{label} #{index}: {value['bytes_read']} bytes, {value['mib_per_second']:.3f} MiB/s, response {value['ttfb_ms']:.1f} ms")
                else:
                    print(f"{label} #{index}: failed ({value.get('error', 'unknown')})")
        if comparison["comparable"]:
            print(f"相同片段校验通过；候选/基线吞吐比 {comparison['throughput_ratio']:.3f}，不是保证提速。")
        else:
            print(f"不生成提速结论：{comparison['reason']}")
        print("仅比较文件头部样本；缓存会影响结果，代理预取可能消耗额外流量。")
    if any(not value.get("ok") for values in samples.values() for value in values):
        return 3
    if "candidate" in urls and not comparison["comparable"]:
        return 4
    return 0


def worker_main():
    """Revalidate direct invocations and self-expire even during DNS/body waits."""
    def expire():
        # A fixed, non-secret result; no Python buffered output can block cleanup.
        try:
            os.write(1, b'{"ok": false, "error": "deadline_exceeded", "route": "direct_no_proxy"}\n')
        finally:
            os._exit(0)

    started = time.monotonic()
    timer = threading.Timer(1.0, expire)  # Bound an idle/unframed stdin producer too.
    timer.daemon = True
    timer.start()
    try:
        raw = sys.stdin.readline(32769)
        if len(raw) > 32768:
            raise ValueError("invalid_input")
        params = json.loads(raw)
        if not isinstance(params, dict) or set(params) != {"url", "sample_bytes", "timeout"}:
            raise ValueError("invalid_input")
        validate_parameters(params["url"], params["sample_bytes"], params["timeout"])
        timer.cancel()
        remaining = params["timeout"] - (time.monotonic() - started)
        if remaining <= 0:
            return {"ok": False, "error": "deadline_exceeded", "route": "direct_no_proxy"}
        timer = threading.Timer(remaining, expire)
        timer.daemon = True
        timer.start()
        return _read_sample(params["url"], params["sample_bytes"], params["timeout"])
    except Exception:
        return {"ok": False, "error": "invalid_input"}
    finally:
        timer.cancel()


if __name__ == "__main__":
    if sys.argv[1:] == ["--worker"]:
        print(json.dumps(worker_main(), ensure_ascii=False))
    else:
        try:
            sys.exit(main())
        except KeyboardInterrupt:
            sys.exit(130)
