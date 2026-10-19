#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PikPak task guardian: observe by default; notifications/resubmissions opt in.

No native `task retry` is advertised by CLI v0.5.3. Optional known-source
resubmission is NOT an in-place retry, never deletes the original task, and
stops on ambiguous results. Fixture mode forbids all processes/notifications
and requires an explicit private state directory (no real home-state reads).
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import math
import os
import random
import stat
import subprocess
import sys
import tempfile
import time
import re
from datetime import datetime
from pathlib import Path

MAX_RETRIES = 3
MAX_SUBMISSIONS_PER_ROUND = 3
ACCOUNT_MIN_INTERVAL = 60
_CREDENTIAL_TEXT_RE = re.compile(
    r"token|password|passwd|pass[ _-]?code|secret|authorization|bearer|cookie|"
    r"credential|api[ _-]?key|session[ _-]?(?:id|key)|https?://[^/\s]+@",
    re.IGNORECASE,
)


def _require_private_file(path, label):
    """Allow only an existing single-link regular file with exact 0600 mode."""
    path = Path(path)
    try:
        info = path.lstat()
    except FileNotFoundError:
        return
    if (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1
            or (info.st_mode & 0o777) != 0o600 or (info.st_mode & 0o7000)):
        raise ValueError(f"{label} 必须是单硬链接普通文件且权限为 0600")


PIKPAK_FAILURE_KINDS = frozenset({"rate_limit", "service", "transport", "authentication", "schema", "unknown"})
PIKPAK_LEDGER_PREFIX = "pikpak-account-"


class PikPakCooldownStore:
    """Durable account-wide PikPak cooldown shared with the Telegram bot."""
    def __init__(self, directory, account):
        if not account:
            raise ValueError("PikPak 状态必须绑定账号")
        self.scope = hashlib.sha256(account.encode()).hexdigest()
        self.path = Path(directory) / (PIKPAK_LEDGER_PREFIX + self.scope + ".json")

    @staticmethod
    def _valid_failure(value):
        return (isinstance(value, dict) and isinstance(value.get("kind"), str)
                and value["kind"] in PIKPAK_FAILURE_KINDS
                and type(value.get("retry_after")) in (int, float)
                and not isinstance(value.get("retry_after"), bool)
                and math.isfinite(value["retry_after"]) and value["retry_after"] >= 0)

    def read(self):
        _require_private_file(self.path, "PikPak 共享状态")
        try:
            state = json.loads(self.path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return {"scope": self.scope, "cooldown_until": 0, "failures": 0}
        except (OSError, ValueError):
            raise ValueError("PikPak 共享状态不可读；拒绝静默重置") from None
        if (not isinstance(state, dict) or state.get("scope") != self.scope
                or type(state.get("failures")) is not int or not 0 <= state["failures"] <= 6
                or type(state.get("cooldown_until")) not in (int, float)
                or isinstance(state.get("cooldown_until"), bool)
                or not math.isfinite(state["cooldown_until"])
                or state["cooldown_until"] < 0
                or ("last_failure" in state and not self._valid_failure(state["last_failure"]))
                or type(state.get("failure_generation", 0)) is not int
                or state.get("failure_generation", 0) < 0):
            raise ValueError("PikPak 共享状态结构错误；拒绝重置")
        return state

    def save(self, state):
        save_json(self.path, state)

    def _with_lock(self):
        lock_path = self.path.with_suffix(".lock")
        _require_private_file(lock_path, "PikPak 共享锁")
        fd = os.open(lock_path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
        return fd

    def sync_account(self, account_state):
        """Merge legacy guardian state into the shared ledger, never lowering it."""
        fd = self._with_lock()
        with os.fdopen(fd, "w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            shared = self.read()
            changed = False
            if account_state["cooldown_until"] > shared["cooldown_until"]:
                shared["cooldown_until"] = account_state["cooldown_until"]
                changed = True
            if account_state["failures"] > shared["failures"]:
                shared["failures"] = account_state["failures"]
                changed = True
            if account_state.get("last_failure") and (
                    "last_failure" not in shared or account_state["cooldown_until"] >= shared["cooldown_until"]):
                shared["last_failure"] = account_state["last_failure"]
                changed = True
            if changed:
                shared["failure_generation"] = shared.get("failure_generation", 0) + 1
                self.save(shared)
            return shared

    def record_failure(self, error, now):
        failure = safe_failure(error)
        fd = self._with_lock()
        with os.fdopen(fd, "w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            state = self.read()
            state["failure_generation"] = state.get("failure_generation", 0) + 1
            state["failures"] = min(6, state["failures"] + 1)
            delay = max(failure["retry_after"], min(3600, 60 * 2 ** (state["failures"] - 1)))
            state["cooldown_until"] = max(state["cooldown_until"], now + delay)
            state["last_failure"] = failure
            self.save(state)
            return state

    def ensure_cooldown(self, until):
        fd = self._with_lock()
        with os.fdopen(fd, "w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            state = self.read()
            if until > state["cooldown_until"]:
                state["cooldown_until"] = until
                self.save(state)
            return state

    def admit(self, *, now=None, clock=None, reserve_seconds=0):
        """Linearize admission under the shared lock, never hold it over CLI.

        Only state-lock -> account-lock ordering is allowed. A later failure
        cannot cancel this admitted call, but must survive its success merge.
        """
        fd = self._with_lock()
        with os.fdopen(fd, "w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            state = self.read()
            observed = _clock_now(clock, now)
            allowed = observed >= state["cooldown_until"]
            if allowed and reserve_seconds:
                state["cooldown_until"] = max(state["cooldown_until"], observed + reserve_seconds)
                self.save(state)
            return state, allowed

    def record_success(self, started=None, *, preserve_until=0):
        fd = self._with_lock()
        with os.fdopen(fd, "w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            state = self.read()
            if started is not None and state == started:
                state["failures"] = 0
                state.pop("last_failure", None)
            state["cooldown_until"] = max(state["cooldown_until"], preserve_until)
            self.save(state)
            return state


NOTIFICATION_SCRIPT = """on run argv
    display notification (item 2 of argv) with title (item 1 of argv)
end run"""


def _clock_now(clock=None, fallback=None):
    """Read an injected clock when supplied; fallback preserves old callers."""
    return clock() if callable(clock) else (time.time() if fallback is None else fallback)


def display_text(value, limit=120):
    """Return only bounded printable non-credential strings for notifications."""
    if (type(value) is not str or not value or len(value) > limit
            or not value.isprintable() or _CREDENTIAL_TEXT_RE.search(value)):
        return "unknown"
    return value


def _observed_now(clock, initial, supplied_now):
    """Re-read production time after a slow operation unless time was frozen."""
    return _clock_now(clock) if callable(clock) or supplied_now is None else initial


def log(message):
    print(time.strftime("[%Y-%m-%d %H:%M:%S] ") + message, flush=True)


def load_json(path, default):
    path = Path(path)
    _require_private_file(path, "状态/源文件")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default
    except (OSError, ValueError):
        raise ValueError("状态/源文件不可读；拒绝静默重置") from None


def save_json(path, data):
    """Same-directory private temporary file, fsync, atomic replace, dir fsync."""
    path = Path(path)
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    _require_private_file(path, "状态文件")
    fd, temporary = tempfile.mkstemp(prefix=".guardian-", dir=path.parent)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def safe_failure(error=None, *, kind="unknown", retry_after=0):
    """Allowlisted classification only; never retain CLI/body/exception text.

    Numeric error_code + parameters.retry_after is a synthetic supported
    envelope, NOT a verified claim about the installed CLI's real schema.
    Unknown nonzero exits are not assumed to be HTTP status codes.
    """
    if isinstance(error, dict):
        if (isinstance(error.get("kind"), str)
                and error["kind"] in {"rate_limit", "service", "transport", "authentication", "schema", "unknown"}):
            kind = error["kind"]
            retry_after = error.get("retry_after", 0)
        else:
            code = error.get("error_code")
            if type(code) is int:
                if code == 429:
                    kind = "rate_limit"
                elif 500 <= code <= 599:
                    kind = "service"
                elif code in (401, 403):
                    kind = "authentication"
            params = error.get("parameters")
            retry_after = params.get("retry_after", 0) if isinstance(params, dict) else 0
    if not isinstance(retry_after, (int, float)) or isinstance(retry_after, bool) or not math.isfinite(retry_after) or retry_after < 0:
        retry_after = 0
    return {"kind": kind, "retry_after": retry_after}


def account_failure(state, error, now, *, shared=None):
    if shared is not None:
        shared_state = shared.record_failure(error, now)
        account = state.setdefault("account_retry", {"cooldown_until": 0, "failures": 0})
        account.update(cooldown_until=shared_state["cooldown_until"],
                       failures=shared_state["failures"])
        if "last_failure" in shared_state:
            account["last_failure"] = dict(shared_state["last_failure"])
    else:
        account = state.setdefault("account_retry", {"cooldown_until": 0, "failures": 0})
        failure = safe_failure(error)
        account["failures"] = min(6, account["failures"] + 1)
        delay = max(failure["retry_after"], min(3600, 60 * 2 ** (account["failures"] - 1)))
        account.update(cooldown_until=max(account["cooldown_until"], now + delay), last_failure=failure)
    state["run_status"] = "degraded"


def pikpak_json(*args, timeout=120):
    try:
        proc = subprocess.run([os.environ.get("PIKPAK_BIN", "pikpak"), *args, "-F", "json"],
                              capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired):
        return None, safe_failure(kind="transport")
    try:
        data = json.loads(proc.stdout)
    except ValueError:
        return None, safe_failure(kind="unknown" if proc.returncode else "schema")
    if (proc.returncode != 0 or not isinstance(data, dict) or data.get("error") or data.get("error_code")
            or data.get("ok") is False or data.get("success") is False):
        return None, safe_failure(data)
    return data, None


def notify(title, message):
    """Only static AppleScript is executable; bounded safe text is argv data."""
    safe_title = display_text(title, 80)
    safe_message = display_text(message, 120)
    if sys.platform == "darwin":
        try:
            proc = subprocess.run(["osascript", "-e", NOTIFICATION_SCRIPT, "--", safe_title, safe_message],
                                  capture_output=True, text=True, timeout=10)
            if proc.returncode == 0:
                return True
        except (OSError, subprocess.TimeoutExpired):
            pass
    log("系统通知未确认送达；请查看巡检状态（未输出远端名称/错误正文）")
    return False


def phase(task):
    value = str(task.get("phase") or task.get("status") or "").upper()
    if value.startswith("PHASE_TYPE_"):
        value = value[len("PHASE_TYPE_"):]
    return value.lower() if value in {"PENDING", "RUNNING", "ERROR", "COMPLETE"} else "unknown"


def fetch_tasks(fixture):
    """All pages or an explicit error; never report a partial list as complete."""
    if fixture is not None:
        data = fixture
        pages = None
    else:
        data, error = pikpak_json("task", "ls", "-l", "100")
        if error:
            return None, error
        pages = set()
    tasks = {}
    while True:
        if (not isinstance(data, dict) or not isinstance(data.get("tasks"), list)
                or data.get("error") or data.get("ok") is False):
            return None, "任务列表结构错误"
        for task in data["tasks"]:
            if not isinstance(task, dict) or not isinstance(task.get("id"), str) or not task["id"]:
                return None, "任务记录缺少有效 ID"
            tasks[task["id"]] = task
        if "next_page_token" not in data:
            token = ""
        else:
            token = data["next_page_token"]
            if not isinstance(token, str):
                return None, "分页 token 类型错误"
        if not token:
            return list(tasks.values()), None
        if pages is None:
            return None, "fixture 含未提供的后页，拒绝部分结果"
        if not isinstance(token, str) or token in pages or len(pages) >= 1000:
            return None, "分页 token 重复或超过上限，结果不完整"
        pages.add(token)
        data, error = pikpak_json("task", "ls", "-l", "100", "--token", token)
        if error:
            return None, error


def confirmed_task_id(data):
    """Reject conflicting or malformed supported identity fields, never coerce."""
    if not isinstance(data, dict):
        return None
    values = [data["task_id"]] if "task_id" in data else []
    if "task" in data:
        if not isinstance(data["task"], dict):
            return None
        values.extend(data["task"][key] for key in ("id", "task_id") if key in data["task"])
    if not values or any(type(value) is not str or not value for value in values):
        return None
    return values[0] if all(value == values[0] for value in values) else None


def retry_task(task, sources, state, *, persist=None, now=None, clock=None, round_budget=None, shared=None):
    """Exact-ID, lineage-budgeted resubmission. Caller holds the state lock.

    No source/name inference, no deletes, no replay after timeout/crash. A
    returned task ID proves only CLI acceptance, not eventual cloud completion.
    """
    tid = task.get("id")
    jobs = state.setdefault("jobs", {})
    candidates = []
    for entry in sources:
        if not isinstance(entry, dict) or not isinstance(entry.get("url"), str):
            continue
        origin = entry.get("task_id")
        url, parent = entry["url"], str(entry.get("parent_id") or "")
        if not url.startswith(("https://", "http://", "magnet:?")):
            continue
        key = hashlib.sha256(json.dumps([url, parent]).encode()).hexdigest()
        previous = jobs.get(key, {})
        if origin == tid or (previous.get("current_id") == tid and previous.get("origin_id") == origin):
            candidates.append((key, entry, previous))
    if len(candidates) != 1:
        return False
    key, entry, job = candidates[0]
    if not callable(persist):
        raise ValueError("重提交必须先提供持久化事务回调")
    supplied_now = now
    now = _clock_now(clock, now)
    if round_budget is not None and round_budget["remaining"] <= 0:
        return False  # This round's own durable cap is limited, not a new fault.
    account = state.setdefault("account_retry", {"cooldown_until": 0, "failures": 0})
    if shared is not None:
        current = shared.read()
        account.update(cooldown_until=current["cooldown_until"], failures=current["failures"])
        if "last_failure" in current:
            account["last_failure"] = dict(current["last_failure"])
    if now < account["cooldown_until"]:
        state["run_status"] = "degraded"
        persist(state)
        return False
    if job and (job.get("current_id") != tid or job.get("status") in {"submitting", "unknown", "exhausted"}):
        return False
    attempts = job.get("attempts", 0)
    if attempts >= MAX_RETRIES or now < job.get("next_retry_at", 0):
        return False
    cap_claimed = False
    if round_budget is not None:
        if round_budget["remaining"] <= 0:
            return False
        round_budget["remaining"] -= 1
        state["round_submissions"] += 1
        if round_budget["remaining"] == 0:
            account["cooldown_until"] = max(account["cooldown_until"], now + ACCOUNT_MIN_INTERVAL)
            cap_claimed = True
    attempts += 1
    delay = min(3600, 60 * 2 ** (attempts - 1))
    job = {"origin_id": entry["task_id"], "current_id": tid, "attempts": attempts,
           "status": "submitting", "next_retry_at": now + min(3600, delay + random.uniform(0, delay / 4))}
    jobs[key] = job
    persist(state)  # Count attempts (including failures) BEFORE invoking CLI.
    args = ["task", "add", entry["url"]]
    if entry.get("parent_id"):
        args.extend(["-p", str(entry["parent_id"])])
    started = None
    if shared is not None:
        started, allowed = shared.admit(now=supplied_now, clock=clock,
                                       reserve_seconds=ACCOUNT_MIN_INTERVAL if cap_claimed else 0)
        if not allowed:
            account.update(cooldown_until=started["cooldown_until"], failures=started["failures"])
            if "last_failure" in started:
                account["last_failure"] = dict(started["last_failure"])
            job["status"] = "unknown"  # Durable intent was already claimed; never replay.
            state["run_status"] = "degraded"
            persist(state)
            return False
    new_id, error = None, None
    try:
        data, error = pikpak_json(*args, timeout=180)
        new_id = confirmed_task_id(data)
        accepted = (isinstance(data, dict) and not error and isinstance(new_id, str) and bool(new_id)
                    and not data.get("error") and not data.get("error_code")
                    and data.get("ok") is not False and data.get("success") is not False)
    except Exception:
        accepted = False
    observed_at = _observed_now(clock, now, supplied_now)
    if accepted:
        job.update(current_id=new_id, status="submitted")
        account["failures"] = 0  # Preserve a cap deadline already claimed before CLI.
        if cap_claimed:
            account["cooldown_until"] = max(account["cooldown_until"], observed_at + ACCOUNT_MIN_INTERVAL)
        if shared is not None:
            merged = shared.record_success(started, preserve_until=account["cooldown_until"] if cap_claimed else 0)
            account.update(cooldown_until=merged["cooldown_until"], failures=merged["failures"])
            if "last_failure" in merged:
                account["last_failure"] = dict(merged["last_failure"])
            else:
                account.pop("last_failure", None)
            if merged["failures"]:
                state["run_status"] = "degraded"
    else:
        job["status"] = "unknown"  # Might have been accepted remotely; never blindly repeat.
        job["failure"] = safe_failure(error)
        account_failure(state, error, observed_at, shared=shared)
    persist(state)
    return accepted


def validate_retry_state(state):
    def timestamp(value):
        # The range also rejects NaN/infinity and unbounded integers safely.
        return type(value) in (int, float) and 0 <= value <= 253402300799

    def failure(value):
        return (isinstance(value, dict) and isinstance(value.get("kind"), str)
                and value["kind"] in {"rate_limit", "service", "transport", "authentication", "schema", "unknown"}
                and timestamp(value.get("retry_after")) and value == safe_failure(value))

    for values in (state["seen_done"], state["seen_failed"]):
        if any(not isinstance(value, str) or not value for value in values):
            raise ValueError("任务去重账本结构错误")
    for key, job in state["jobs"].items():
        if (not isinstance(key, str) or not key or not isinstance(job, dict)
                or not all(isinstance(job.get(k), str) and job[k] for k in ("origin_id", "current_id"))
                or not isinstance(job.get("status"), str)
                or job["status"] not in {"submitting", "submitted", "unknown", "exhausted"}
                or type(job.get("attempts")) is not int or not 0 <= job["attempts"] <= MAX_RETRIES
                or not timestamp(job.get("next_retry_at"))
                or ("failure" in job and not failure(job["failure"]))):
            raise ValueError("重提交作业账本结构错误；拒绝重置")
    if any(not isinstance(key, str) or not isinstance(value, str)
           or value not in {"claimed", "delivered", "failed"} for key, value in state["events"].items()):
        raise ValueError("通知事件账本结构错误")
    account = state.setdefault("account_retry", {"cooldown_until": 0, "failures": 0})
    if (not isinstance(account, dict) or not timestamp(account.get("cooldown_until"))
            or type(account.get("failures")) is not int or not 0 <= account["failures"] <= 6
            or ("last_failure" in account and not failure(account["last_failure"]))
            or type(state.get("round_submissions", 0)) is not int
            or not 0 <= state.get("round_submissions", 0) <= MAX_SUBMISSIONS_PER_ROUND):
        raise ValueError("账号调度账本结构错误；拒绝重置")


def once(fixture=None, *, state_path=None, account_scope=None,
         enable_notifications=False, retry_known=False, sources=None, now=None, clock=None):
    if not account_scope or state_path is None:
        raise ValueError("必须显式提供账号作用域与隔离状态路径")
    state_path = Path(state_path)
    state_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    scope = hashlib.sha256(account_scope.encode()).hexdigest()
    lock_path = state_path.with_suffix(".lock")
    _require_private_file(lock_path, "状态锁")
    lock_fd = os.open(lock_path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    with os.fdopen(lock_fd, "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        state = load_json(state_path, {"version": 1, "scope": scope, "seen_done": [], "seen_failed": [], "jobs": {}, "events": {}})
        if (not isinstance(state, dict) or state.get("version") != 1 or state.get("scope") != scope
                or not all(isinstance(state.get(k), list) for k in ("seen_done", "seen_failed"))
                or not all(isinstance(state.get(k), dict) for k in ("jobs", "events"))):
            raise ValueError("状态格式/账号不匹配；不读取或迁移旧 home 状态")
        validate_retry_state(state)
        shared = PikPakCooldownStore(state_path.parent, account_scope)
        account = state.setdefault("account_retry", {"cooldown_until": 0, "failures": 0})
        shared_state = shared.sync_account(account)
        previous_until = account["cooldown_until"]
        account["cooldown_until"] = max(previous_until, shared_state["cooldown_until"])
        account["failures"] = max(account["failures"], shared_state["failures"])
        if shared_state.get("last_failure") and shared_state["cooldown_until"] >= previous_until:
            account["last_failure"] = dict(shared_state["last_failure"])
        supplied_now = now
        now = _clock_now(clock, now)
        if now < account["cooldown_until"]:
            state["run_status"] = "degraded"
            save_json(state_path, state)
            log("账号持久冷却中；未查询或重提交")
            return state
        state["run_status"] = "ok"
        state["round_submissions"] = 0
        round_budget = {"remaining": MAX_SUBMISSIONS_PER_ROUND}
        tasks, error = fetch_tasks(fixture)
        if error or tasks is None:
            account_failure(state, error, _observed_now(clock, now, supplied_now), shared=shared)
            save_json(state_path, state)
            log("巡检降级：任务列表未确认；已持久化账号冷却，未输出敏感正文")
            return state
        counts = {p: sum(phase(t) == p for t in tasks) for p in ("pending", "running", "complete", "error", "unknown")}
        for task in tasks:
            status, tid = phase(task), task["id"]
            if status not in {"complete", "error"}:
                continue
            seen = state["seen_done" if status == "complete" else "seen_failed"]
            fresh = tid not in seen
            if fresh:
                seen.append(tid)
            # Fixture is a hard capability boundary, not merely a fake task list.
            if fixture is None and retry_known and status == "error":
                retry_task(task, sources or [], state, persist=lambda value: save_json(state_path, value),
                           now=supplied_now, clock=clock, round_budget=round_budget, shared=shared)
                if state["run_status"] == "degraded":
                    break  # First uncertain/shared fault stops the entire round.
            if fresh and fixture is None and enable_notifications:
                key = status + ":" + tid
                state["events"][key] = "claimed"
                save_json(state_path, state)
                title = "PikPak 转存完成" if status == "complete" else "PikPak 任务失败"
                delivered = notify(title, display_text(task.get("name")))
                state["events"][key] = "delivered" if delivered is True else "failed"
        if round_budget["remaining"] == 0 and state["run_status"] == "ok":
            state["run_status"] = "limited"
            account["cooldown_until"] = max(account["cooldown_until"],
                                            _clock_now(clock, now) + ACCOUNT_MIN_INTERVAL)
            shared.ensure_cooldown(account["cooldown_until"])
        state["counts"] = counts
        state["last_run"] = datetime.fromtimestamp(_clock_now(clock, now)).astimezone().isoformat(timespec="seconds")
        save_json(state_path, state)
        summary = {"ok": "巡检完成", "limited": "巡检已达提交上限", "degraded": "巡检降级"}[state["run_status"]]
        log(summary + "：" + "、".join(f"{key} {value}" for key, value in counts.items()))
        return state


def daily_report(state):
    # Historical helper name retained, but deliberately no false 'yesterday' claim.
    return f"PikPak 累计观察完成 {len(state.get('seen_done', []))} 个任务（非昨日报表）。"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--interval", type=int, default=300)
    parser.add_argument("--from-fixture", type=Path)
    parser.add_argument("--state-dir", type=Path)
    parser.add_argument("--account-scope", help="当前 CLI 账号的非敏感别名；切换账号必须更换")
    parser.add_argument("--notify", action="store_true", help="显式允许本地通知（fixture 强制禁止）")
    parser.add_argument("--retry-known", action="store_true", help="允许精确登记源重提交；不是原生 retry")
    parser.add_argument("--sources", type=Path, help="显式提供私有源登记 JSON；不读默认 home 源")
    args = parser.parse_args()
    if args.interval < 1:
        parser.error("--interval 必须为正数")
    if args.from_fixture and (not args.state_dir or args.notify or args.retry_known or args.sources):
        parser.error("fixture 必须显式 --state-dir，且禁止 --notify/--retry-known/--sources")
    if not args.from_fixture and not args.account_scope:
        parser.error("真实巡检必须显式 --account-scope")
    account = args.account_scope or "fixture"
    fixture = load_json(args.from_fixture, None) if args.from_fixture else None
    if args.from_fixture and fixture is None:
        parser.error("fixture 文件不存在或为 null")
    sources = []
    if args.sources:
        source_data = load_json(args.sources, None)
        if not isinstance(source_data, dict) or source_data.get("account_scope") != account or not isinstance(source_data.get("sources"), list):
            parser.error("源登记必须含匹配的 account_scope 与 sources 数组")
        sources = source_data["sources"]
    if args.retry_known and not args.sources:
        parser.error("--retry-known 需要 --sources 精确登记")
    directory = args.state_dir or Path.home() / ".pikpak" / "automation"
    path = directory / ("guardian-" + hashlib.sha256(account.encode()).hexdigest() + ".json")
    failures = 0
    while True:
        state = None
        try:
            state = once(fixture, state_path=path, account_scope=account, enable_notifications=args.notify,
                         retry_known=args.retry_known, sources=sources)
            if state["run_status"] == "degraded":
                failures += 1
                if args.once or args.from_fixture:
                    parser.exit(1, "巡检降级；持久冷却生效，未知提交不重放\n")
            else:
                failures = 0
        except (ValueError, OSError) as exc:
            if args.once or args.from_fixture:
                parser.exit(1, "巡检失败 (" + type(exc).__name__ + ")；未输出敏感正文\n")
            failures += 1
            log("巡检失败 (" + type(exc).__name__ + ")；未输出敏感正文")
        if args.once or args.from_fixture:
            return
        cooldown = max(0, state["account_retry"]["cooldown_until"] - time.time()) if state else 0
        time.sleep(max(args.interval, cooldown, min(3600, 2 ** min(failures, 12))))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n已退出。")
