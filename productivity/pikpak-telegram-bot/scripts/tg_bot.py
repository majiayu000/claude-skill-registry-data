#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PikPak Telegram Bot 遥控器。

在 Telegram 里发磁力/链接，本机自动转存到 PikPak 云盘。
纯标准库实现（urllib 长轮询 Telegram Bot API + subprocess 调 pikpak CLI）。

安全设计：
  - 白名单强制：PIKPAK_ALLOWED_CHAT_IDS 未设置或为空时，拒绝一切消息。
  - 只实现「转存 + 查询」；不提供删除/清空等危险操作。
  - token 通过环境变量传入，不写日志、不回显。

用法：
  export TG_BOT_TOKEN="123:ABC..."
  export PIKPAK_ALLOWED_CHAT_IDS="12345678"   # 逗号分隔
  python3 tg_bot.py                            # 前台运行
  python3 tg_bot.py --check                    # 列出最近跟 bot 说过话的 chat id
  python3 tg_bot.py --once                     # 真实处理一轮（不是离线测试）

环境变量：
  TG_BOT_TOKEN              Telegram bot token（必需）
  PIKPAK_ALLOWED_CHAT_IDS   允许的 chat id，逗号分隔（必需，空=拒绝所有人）
  PIKPAK_ALLOWED_USER_IDS   群内允许的发送者 user id，逗号分隔（群聊必需）
  PIKPAK_ACCOUNT_SCOPE      当前 CLI 账号的非敏感别名（必需，换账号须换）
  PIKPAK_AUTOMATION_STATE_DIR 可信私有状态目录（默认 ~/.pikpak/automation）
  PIKPAK_BIN                pikpak 可执行路径（默认 "pikpak"）
  TG_API_BASE               Telegram API 基址（默认 https://api.telegram.org）
"""

from __future__ import annotations

import json
import math
import hashlib
import fcntl
import os
import re
import stat
import subprocess
import sys
import time
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from http.client import HTTPException
from typing import NoReturn
from pathlib import Path
from contextlib import contextmanager

POLL_TIMEOUT = 30
# Stop before the known long-poll/request window could cross a week boundary.
IDLE_RESYNC_SECONDS = 7 * 24 * 60 * 60 - (POLL_TIMEOUT + 15)
MAX_PENDING_AGE_SECONDS = 24 * 60 * 60
RECEIPT_VALUES = frozenset({"started", "submitted", "submission_unknown", "handled",
                            "uncertain", "duplicate_message"})
PIKPAK_FAILURE_KINDS = frozenset({"rate_limit", "service", "transport", "authentication",
                                  "schema", "unknown"})
_RECEIPT_KEY_RE = re.compile(r"(?:0|[1-9][0-9]*)(?::(?:0|[1-9][0-9]*))?$")
_MESSAGE_KEY_RE = re.compile(r"-?[0-9]+:[1-9][0-9]*$")
_CREDENTIAL_TEXT_RE = re.compile(
    r"token|password|passwd|pass[ _-]?code|secret|authorization|bearer|cookie|"
    r"credential|api[ _-]?key|session[ _-]?(?:id|key)|https?://[^/\s]+@", re.IGNORECASE)


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


def _open_private_lock(path, label):
    _require_private_file(path, label)
    return os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)


def display_text(value, limit=120):
    """Outbound text is a bounded plain string, never a repr of raw metadata."""
    if (type(value) is not str or not value or len(value) > limit
            or not value.isprintable() or _CREDENTIAL_TEXT_RE.search(value)):
        return "unknown"
    return value


class ResyncRequired(ValueError):
    """Safe, operator-visible startup block; never silently lower an offset."""


class PikPakFailure:
    """Allowlisted CLI failure; raw output and exit codes never cross the seam."""
    def __init__(self, kind="unknown", retry_after=0, message="转存结果未确认；请人工核对，不要直接重发"):
        self.kind = kind if isinstance(kind, str) and kind in PIKPAK_FAILURE_KINDS else "unknown"
        self.retry_after = (retry_after if type(retry_after) in (int, float)
                            and not isinstance(retry_after, bool)
                            and math.isfinite(retry_after) and retry_after >= 0 else 0)
        self.message = message

    def __str__(self):
        return self.message


def safe_pikpak_failure(error=None):
    if isinstance(error, PikPakFailure):
        return error
    return PikPakFailure()


MAGNET_RE = re.compile(r"^(magnet:|https?://|thunder://|ed2k://)", re.IGNORECASE)
HELP_TEXT = """PikPak 遥控器指令：
• 直接发链接 → 转存到根目录
• /save <链接> [to <文件夹名>] → 转存（可指定文件夹）
• /tasks → 查看进行中任务
• /status <taskID> → 查询单个任务
• /ls → 列出根目录最近文件
• /help → 本帮助"""


def die(msg: str, code: int = 1) -> NoReturn:
    print(f"错误：{msg}", file=sys.stderr)
    raise SystemExit(code)


def log(msg: str) -> None:
    print(time.strftime("[%Y-%m-%d %H:%M:%S] ") + msg, flush=True)


class PikPakStore:
    """Account-scoped CLI failure gate, separate from Telegram transport state."""
    def __init__(self, directory: Path, account: str):
        if not account:
            raise ValueError("PikPak 状态必须绑定账号")
        self.scope = hashlib.sha256(account.encode()).hexdigest()
        self.path = Path(directory) / ("pikpak-account-" + self.scope + ".json")

    @staticmethod
    def _valid_failure(value):
        return (isinstance(value, dict) and isinstance(value.get("kind"), str)
                and value["kind"] in PIKPAK_FAILURE_KINDS
                and type(value.get("retry_after")) in (int, float)
                and not isinstance(value.get("retry_after"), bool)
                and math.isfinite(value["retry_after"]) and value["retry_after"] >= 0)

    def read(self):
        _require_private_file(self.path, "PikPak 状态")
        try:
            state = json.loads(self.path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return {"scope": self.scope, "cooldown_until": 0, "failures": 0}
        except (ValueError, OSError):
            raise ValueError("PikPak 状态不可读；拒绝静默重置") from None
        if (not isinstance(state, dict) or state.get("scope") != self.scope
                or type(state.get("failures")) is not int or not 0 <= state["failures"] <= 6
                or type(state.get("cooldown_until")) not in (int, float)
                or isinstance(state.get("cooldown_until"), bool)
                or not math.isfinite(state["cooldown_until"]) or state["cooldown_until"] < 0
                or ("last_failure" in state and not self._valid_failure(state["last_failure"]))
                or type(state.get("failure_generation", 0)) is not int
                or state.get("failure_generation", 0) < 0):
            raise ValueError("PikPak 状态结构错误；拒绝重置")
        return state

    def save(self, state):
        self.path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        _require_private_file(self.path, "PikPak 状态")
        fd, temporary = tempfile.mkstemp(prefix=".pikpak-account-", dir=self.path.parent)
        try:
            os.fchmod(fd, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                json.dump(state, stream, ensure_ascii=False)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, self.path)
            directory = os.open(self.path.parent, os.O_RDONLY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    def retry_after(self, now=None):
        now = time.time() if now is None else now
        return max(0, math.ceil(self.read()["cooldown_until"] - now))

    def admit(self):
        """Atomic admission, not cancellation: release before any external work.

        Never acquire an update/guardian/transport lock while holding this lock.
        Failures may arrive after admission; success must merge against this token.
        """
        fd = _open_private_lock(self.path.with_suffix(".lock"), "PikPak 状态锁")
        with os.fdopen(fd, "w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            state = self.read()
            return state if time.time() >= state["cooldown_until"] else None

    def record_failure(self, error=None, now=None):
        failure = safe_pikpak_failure(error)
        now = time.time() if now is None else now
        fd = _open_private_lock(self.path.with_suffix(".lock"), "PikPak 状态锁")
        with os.fdopen(fd, "w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            state = self.read()
            state["failure_generation"] = state.get("failure_generation", 0) + 1
            state["failures"] = min(6, state["failures"] + 1)
            delay = max(failure.retry_after, min(3600, 60 * 2 ** (state["failures"] - 1)))
            state["cooldown_until"] = max(state["cooldown_until"], now + delay)
            state["last_failure"] = {"kind": failure.kind, "retry_after": failure.retry_after}
            self.save(state)
        return state

    def record_success(self, started=None):
        fd = _open_private_lock(self.path.with_suffix(".lock"), "PikPak 状态锁")
        with os.fdopen(fd, "w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            state = self.read()
            # A legacy writer may not increment generation, so compare the full
            # snapshot too. Never erase a future deadline, even without a fault.
            if started is not None and state == started:
                state["failures"] = 0
                state.pop("last_failure", None)
                self.save(state)
        return state


class UpdateStore:
    """POSIX single-writer journal; a durable claim precedes any remote effect.

    Started/uncertain receipts are deliberately NOT replayed: the CLI has no
    idempotency key, so crash recovery needs human reconciliation, not guessing.
    """
    def __init__(self, directory: Path, account: str, bot: str):
        if not account or not bot:
            raise ValueError("状态必须绑定账号与 bot")
        directory = Path(directory)
        directory.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.directory = directory
        self.account = account
        self.scope = hashlib.sha256(json.dumps([account, bot.split(":", 1)[0]]).encode()).hexdigest()
        self.path = directory / ("telegram-" + self.scope + ".json")
        self.pikpak = PikPakStore(directory, account)

    def read(self):
        _require_private_file(self.path, "Telegram 状态")
        try:
            state = json.loads(self.path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            state = {"scope": self.scope, "receipts": {}, "messages": {}, "next_offset": None}
        except (ValueError, OSError):
            raise ValueError("状态不可读；拒绝重置以免重复提交") from None
        if (not isinstance(state, dict) or state.get("scope") != self.scope
                or not isinstance(state.get("receipts"), dict)
                or (state.get("next_offset") is not None and type(state["next_offset"]) is not int)):
            raise ValueError("状态格式或账号不匹配")
        if not isinstance(state.setdefault("messages", {}), dict):
            raise ValueError("消息去重状态格式错误")
        if not isinstance(state.setdefault("duplicate_messages", {}), dict):
            raise ValueError("重复消息引用状态格式错误")
        if any(not isinstance(key, str) or not _RECEIPT_KEY_RE.fullmatch(key)
               or not isinstance(value, str) or value not in RECEIPT_VALUES
               for key, value in state["receipts"].items()):
            raise ValueError("消息收据账本结构错误")
        if any(not isinstance(key, str) or not _MESSAGE_KEY_RE.fullmatch(key)
               or not isinstance(value, str) or not _RECEIPT_KEY_RE.fullmatch(value)
               or value not in state["receipts"]
               or state["receipts"][value] == "duplicate_message"
               for key, value in state["messages"].items()):
            raise ValueError("消息引用账本结构错误")
        if any(not isinstance(key, str) or not _RECEIPT_KEY_RE.fullmatch(key)
               or not isinstance(value, str) or not _MESSAGE_KEY_RE.fullmatch(value)
               or key not in state["receipts"] or state["receipts"][key] != "duplicate_message"
               or value not in state["messages"]
               or state["messages"].get(value) not in state["receipts"]
               or state["receipts"][state["messages"].get(value)] == "duplicate_message"
               for key, value in state["duplicate_messages"].items()):
            raise ValueError("重复消息引用账本结构错误")
        if any(value == "duplicate_message" and key not in state["duplicate_messages"]
               for key, value in state["receipts"].items()):
            raise ValueError("重复消息收据缺少规范引用")
        state.setdefault("epoch", 0)
        state.setdefault("last_observed_at", None)
        state.setdefault("idle_resync_seconds", IDLE_RESYNC_SECONDS)
        state.setdefault("resync_required", False)
        observed = state["last_observed_at"]
        if (type(state["epoch"]) is not int or state["epoch"] < 0
                or type(state["resync_required"]) is not bool
                or type(state["idle_resync_seconds"]) is not int
                or not 0 < state["idle_resync_seconds"] <= IDLE_RESYNC_SECONDS
                or (observed is not None and (type(observed) not in (int, float)
                    or not math.isfinite(observed) or observed < 0))
                or (state["next_offset"] is not None and state["next_offset"] < 0)):
            raise ValueError("序列状态格式错误")
        for key in state["receipts"]:
            parts = key.split(":")
            receipt_epoch, receipt_id = (0, int(parts[0])) if len(parts) == 1 else (int(parts[0]), int(parts[1]))
            if receipt_epoch > state["epoch"]:
                raise ValueError("收据 epoch 超前")
            if (state["next_offset"] is not None and receipt_epoch == state["epoch"]
                    and receipt_id >= state["next_offset"]):
                raise ValueError("收据与 next_offset 矛盾")
        return state

    @contextmanager
    def transaction(self):
        fd = _open_private_lock(self.path.with_suffix(".lock"), "PikPak 状态锁")
        with os.fdopen(fd, "w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            yield self.read()

    @staticmethod
    def needs_resync(state, now):
        last = state.get("last_observed_at")
        return (state.get("resync_required", False) or
                (state.get("next_offset") is not None and
                 (last is None or now < last or now - last >= state.get("idle_resync_seconds", IDLE_RESYNC_SECONDS))))

    def prepare_poll(self):
        with self.transaction() as state:
            if self.needs_resync(state, time.time()):
                state["resync_required"] = True
                self.save(state)
                raise ResyncRequired("空闲/旧账本序列不确定；已阻止旧 offset。停其他实例并经授权执行 --resync；不要删除账本")
            return state.get("next_offset")

    def save(self, state):
        _require_private_file(self.path, "Telegram 状态")
        fd, temp = tempfile.mkstemp(prefix=".telegram-", dir=self.path.parent)
        try:
            os.fchmod(fd, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                json.dump(state, stream, ensure_ascii=False)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temp, self.path)
            directory = os.open(self.path.parent, os.O_RDONLY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
        finally:
            if os.path.exists(temp):
                os.unlink(temp)

    def pikpak_retry_after(self, now=None):
        return self.pikpak.retry_after(now)


def _generation_time(update, now):
    message = update.get("message") if isinstance(update, dict) else None
    date = message.get("date") if isinstance(message, dict) else None
    if type(date) is int and date >= 0:
        return date, True
    # Unknown generation time keeps the maximum pending-age margin instead of
    # pretending local processing time was the server timestamp.
    return max(0, now - MAX_PENDING_AGE_SECONDS), False


def _observe_generation(state, update, now):
    generation, trusted = _generation_time(update, now)
    previous = state.get("last_observed_at")
    if previous is None:
        state["last_observed_at"] = generation
    elif trusted:
        state["last_observed_at"] = max(previous, generation)
    else:
        state["last_observed_at"] = min(previous, generation)


def _pending_generation_boundary(updates, now):
    return min(_generation_time(update, now)[0] for update in updates)


def process_updates(tg, updates, allowed, store):
    if not isinstance(updates, list):
        raise ValueError("Telegram updates 必须是数组")
    with store.transaction() as state:
        for update in updates:
            # A send failure constrains dispatch just as a polling failure does.
            retry_after = getattr(tg, "retry_after", 0)
            if (getattr(tg, "fatal", False) is True
                    or (type(retry_after) in (int, float) and retry_after > 0)):
                break
            if store.pikpak_retry_after() > 0:
                break
            if not isinstance(update, dict) or type(update.get("update_id")) is not int:
                raise ValueError("Telegram update_id 无效")
            uid = update["update_id"]
            if uid < 0:
                raise ValueError("Telegram update_id 无效")
            key = str(uid) if state["epoch"] == 0 else f"{state['epoch']}:{uid}"
            if key in state["receipts"]:
                continue
            if state.get("resync_required") or (state["next_offset"] is not None and uid < state["next_offset"]):
                state["resync_required"] = True
                store.save(state)
                raise ResyncRequired("未领取的低 update_id 与当前序列冲突；保持 offset，需人工 --resync")
            message = update.get("message")
            message_key = None
            if isinstance(message, dict):
                chat = message.get("chat")
                chat_id = chat.get("id") if isinstance(chat, dict) else None
                message_id = message.get("message_id")
                if type(chat_id) is int and type(message_id) is int and message_id > 0:
                    message_key = str(chat_id) + ":" + str(message_id)
            if message_key is not None and message_key in state["messages"]:
                state["receipts"][key] = "duplicate_message"
                state["duplicate_messages"][key] = message_key
                state["next_offset"] = max(state.get("next_offset") or 0, uid + 1)
                store.save(state)
                continue
            _observe_generation(state, update, time.time())
            state["receipts"][key] = "started"
            if message_key is not None:
                state["messages"][message_key] = key
            state["next_offset"] = max(state.get("next_offset") or 0, uid + 1)
            store.save(state)  # Never execute when the claim cannot be persisted.
            outcome = None
            try:
                if isinstance(message, dict):
                    outcome = process_message(tg, message, allowed, pikpak_store=store.pikpak)
                state["receipts"][key] = outcome or "handled"
            except Exception as exc:
                state["receipts"][key] = "uncertain"
                log(f"处理消息异常 ({type(exc).__name__})；已留去重记录，不自动重放")
            store.save(state)
            if outcome == "submission_unknown" or store.pikpak_retry_after() > 0:
                break
        return state.get("next_offset")


# ---------------------------------------------------------------------------
# Telegram API
# ---------------------------------------------------------------------------

class TransportStore(UpdateStore):
    """Separate journal/lock: transport writes cannot overwrite update claims."""
    def __init__(self, updates):
        self.scope = updates.scope
        self.path = updates.path.with_suffix(".transport.json")

    def read(self):
        _require_private_file(self.path, "传输状态")
        try:
            state = json.loads(self.path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return {"scope": self.scope, "cooldown_until": 0, "failures": 0, "fatal": False}
        except (ValueError, OSError):
            raise ValueError("传输状态不可读；拒绝静默重置") from None
        if (not isinstance(state, dict) or state.get("scope") != self.scope
                or type(state.get("fatal")) is not bool
                or type(state.get("failures")) is not int or not 0 <= state["failures"] <= 6
                or type(state.get("cooldown_until")) not in (int, float)
                or not math.isfinite(state["cooldown_until"]) or state["cooldown_until"] < 0):
            raise ValueError("传输状态结构错误")
        return state


class Telegram:
    def __init__(self, token: str, base: str = "https://api.telegram.org", *, store=None):
        parsed = urllib.parse.urlsplit(base)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError("Telegram API 基址必须是无凭据的 HTTPS URL")
        self.base = f"{base}/bot{token}"
        self.transport = TransportStore(store) if store is not None else None
        self.schedule = (self.transport.read() if self.transport else
                         {"cooldown_until": 0, "failures": 0, "fatal": False})

    @property
    def fatal(self):
        return self.schedule["fatal"]

    @property
    def retry_after(self):
        return max(0, math.ceil(self.schedule["cooldown_until"] - time.time()))

    def _save_schedule(self):
        if self.transport:
            self.transport.save(self.schedule)

    def _failed(self, code=None, payload=None):
        self.schedule["fatal"] = self.fatal or code in (401, 403, 409)
        self.schedule["failures"] = min(6, self.schedule["failures"] + 1)
        delay = min(60, 2 ** self.schedule["failures"])
        params = payload.get("parameters") if isinstance(payload, dict) else None
        seconds = params.get("retry_after") if isinstance(params, dict) else None
        if type(seconds) in (int, float) and math.isfinite(seconds) and seconds >= 0:
            delay = max(delay, seconds)
        elif code == 429:
            delay = max(delay, 60)
        self.schedule["cooldown_until"] = max(self.schedule["cooldown_until"], time.time() + delay)
        self._save_schedule()

    def _call(self, method: str, **params):
        if self.transport is None:
            return self._request(method, **params)
        fd = _open_private_lock(self.transport.path.with_suffix(".lock"), "传输状态锁")
        with os.fdopen(fd, "w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            self.schedule = self.transport.read()
            return self._request(method, **params)

    def _request(self, method: str, **params):
        # Every method shares this gate, including sendMessage and check mode.
        if self.fatal or self.retry_after:
            return None
        url = f"{self.base}/{method}"
        data = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request(url, data=data)
        try:
            with urllib.request.urlopen(req, timeout=POLL_TIMEOUT + 15) as resp:
                payload = json.loads(resp.read().decode())
        except urllib.error.HTTPError as exc:
            try:
                payload = json.loads(exc.read().decode())
            except (ValueError, TypeError, AttributeError, OSError, HTTPException):
                payload = None
            self._failed(exc.code, payload)
            log(f"Telegram API {method} HTTP {exc.code}")
            return None
        except (OSError, ValueError, TypeError, HTTPException) as exc:
            self._failed()
            # Never log exception strings, HTTP bodies or token-bearing URLs.
            log(f"Telegram API {method} 失败 ({type(exc).__name__})")
            return None
        if not isinstance(payload, dict) or payload.get("ok") is not True:
            self._failed(payload.get("error_code") if isinstance(payload, dict) else None, payload)
            log(f"Telegram API {method} 返回错误")
            return None
        result = payload.get("result")
        if ((method == "getUpdates" and not isinstance(result, list))
                or (method == "sendMessage" and (not isinstance(result, dict)
                    or type(result.get("message_id")) is not int or result["message_id"] <= 0))):
            self._failed()
            log(f"Telegram API {method} 返回未知结果结构")
            return None
        self.schedule.update(failures=0, cooldown_until=0)
        self._save_schedule()
        return result

    def get_updates(self, offset: int | None = None):
        params = {"timeout": POLL_TIMEOUT, "allowed_updates": '["message"]'}
        if offset is not None:
            params["offset"] = offset
        return self._call("getUpdates", **params)

    def send(self, chat_id, text: str):
        if len(text) > 4000:
            text = text[:3950] + "\n（内容已截断）"
        result = self._call("sendMessage", chat_id=chat_id, text=text,
                            disable_web_page_preview="true")
        if not isinstance(result, dict) or not result.get("message_id"):
            raise RuntimeError("Telegram 回复未确认送达；不自动重放业务命令")
        return result


# ---------------------------------------------------------------------------
# PikPak CLI 包装
# ---------------------------------------------------------------------------

def pikpak(*args: str, timeout: int = 120):
    """调用 pikpak CLI；返回 (rc, stdout, stderr)。"""
    bin_path = os.environ.get("PIKPAK_BIN", "pikpak")
    try:
        proc = subprocess.run([bin_path, *args], capture_output=True, text=True, timeout=timeout)
        return proc.returncode, proc.stdout, proc.stderr
    except FileNotFoundError:
        return 127, "", "找不到 pikpak 命令，请先安装 PikPak CLI"
    except subprocess.TimeoutExpired:
        return 124, "", f"pikpak 命令超时（{timeout}s）"


def pikpak_json(*args: str, timeout: int = 120):
    rc, out, err = pikpak(*args, "-F", "json", timeout=timeout)
    if rc != 0:
        # A nonzero process exit is only an unknown outcome, never an HTTP code.
        return None, PikPakFailure("unknown", message="CLI 提交失败；结果未知时请人工核对，勿直接重发")
    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        return None, PikPakFailure("schema", message="无法解析 pikpak 输出")
    if (not isinstance(data, dict) or data.get("error") or data.get("error_code")
            or data.get("ok") is False or data.get("success") is False):
        kind, retry_after = "unknown", 0
        code = data.get("error_code") if isinstance(data, dict) else None
        if type(code) is int:
            if code == 429:
                kind = "rate_limit"
            elif 500 <= code <= 599:
                kind = "service"
            elif code in (401, 403):
                kind = "authentication"
        params = data.get("parameters") if isinstance(data, dict) else None
        if isinstance(params, dict):
            candidate = params.get("retry_after")
            if type(candidate) in (int, float) and not isinstance(candidate, bool) \
                    and math.isfinite(candidate) and candidate >= 0:
                retry_after = candidate
        return None, PikPakFailure(kind, retry_after, "CLI 返回错误或不支持的结构")
    return data, None


def find_folder_id(name: str):
    """在根目录下按名称找文件夹 ID。"""
    token, pages, matches = "", set(), set()
    while True:
        args = ["ls", "--type", "folder"]
        if token:
            args += ["--token", token]
        data, err = pikpak_json(*args)
        if err:
            return None, err
        if not isinstance(data, dict) or not isinstance(data.get("files"), list):
            return None, PikPakFailure("schema", message="目录列表结构错误")
        for folder in data["files"]:
            if (not isinstance(folder, dict)
                    or type(folder.get("id")) is not str or not folder["id"]
                    or type(folder.get("name")) is not str or not folder["name"]
                    or folder.get("kind") != "drive#folder"):
                return None, PikPakFailure("schema", message="目录记录结构错误")
            if folder["name"] == name:
                matches.add(folder["id"])
        if "next_page_token" in data and type(data["next_page_token"]) is not str:
            return None, PikPakFailure("schema", message="目录分页结构错误")
        token = data["next_page_token"] if "next_page_token" in data else ""
        if not token:
            break
        if not isinstance(token, str) or token in pages or len(pages) >= 1000:
            return None, PikPakFailure("schema", message="目录分页不完整；拒绝猜测目标")
        pages.add(token)
    if len(matches) > 1:
        return None, "存在多个同名文件夹；请先消除歧义"
    if matches:
        return matches.pop(), None
    return None, f"根目录下没找到文件夹「{name}」"


# ---------------------------------------------------------------------------
# 指令处理
# ---------------------------------------------------------------------------

def confirmed_task_id(data):
    """All present supported identity fields must be nonempty strings and agree."""
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


def handle_save(tg: Telegram, chat_id, text: str, *, pikpak_store=None):
    m = re.match(r"^/save\s+(\S+)(?:\s+to\s+(.+))?$", text, re.IGNORECASE)
    if not m:
        tg.send(chat_id, "用法：/save <链接> [to <文件夹名>]")
        return
    url, folder_name = m.group(1), (m.group(2) or "").strip()
    if not MAGNET_RE.match(url):
        tg.send(chat_id, "只接受支持的链接，不能将 CLI 参数作为链接提交。")
        return

    args = ["task", "add", url]
    if folder_name:
        fid, err = find_folder_id(folder_name)
        if err:
            if isinstance(err, PikPakFailure) and pikpak_store is not None:
                pikpak_store.record_failure(err, now=time.time())
            tg.send(chat_id, "找不到文件夹：查询结果未确认。")
            return "submission_unknown" if isinstance(err, PikPakFailure) else None
        if type(fid) is not str or not fid:
            failure = PikPakFailure("schema", message="目标文件夹 ID 结构未确认")
            if pikpak_store is not None:
                pikpak_store.record_failure(failure, now=time.time())
            tg.send(chat_id, "找不到文件夹：目标 ID 结构未确认")
            return "submission_unknown"
        args += ["-p", fid]

    tg.send(chat_id, "正在请求转存，尚未确认提交结果…")
    started = pikpak_store.admit() if pikpak_store is not None else None
    if pikpak_store is not None and started is None:
        # The update claim remains durable; no automatic replay after denial.
        return "submission_unknown"
    data, err = pikpak_json(*args, timeout=180)
    if err:
        if pikpak_store is not None:
            pikpak_store.record_failure(err, now=time.time())
        tg.send(chat_id, "转存结果未确认：返回错误或未知结构。请人工核对，不要直接重发。")
        return "submission_unknown"
    if not isinstance(data, dict):
        failure = PikPakFailure("schema")
        if pikpak_store is not None:
            pikpak_store.record_failure(failure, now=time.time())
        tg.send(chat_id, "提交结果未确认：返回结构错误，请人工核对。")
        return "submission_unknown"
    task_id = confirmed_task_id(data)
    if not isinstance(task_id, str) or not task_id or data.get("error") or data.get("ok") is False:
        failure = PikPakFailure("unknown")
        if pikpak_store is not None:
            pikpak_store.record_failure(failure, now=time.time())
        tg.send(chat_id, "提交结果未确认：未获得任务 ID。请人工核对，不要直接重发。")
        return "submission_unknown"
    if pikpak_store is not None:
        pikpak_store.record_success(started)
    file_name = display_text(data.get("file_name"))
    tg.send(chat_id, f"✓ 已开始转存\n文件名：{file_name}\n任务 ID：{display_text(task_id)}\n\n用 /status {display_text(task_id)} 查进度")
    return "submitted"


def handle_tasks(tg: Telegram, chat_id):
    data, err = pikpak_json("task", "ls", "-s", "running,pending")
    if err or not isinstance(data, dict) or not isinstance(data.get("tasks"), list):
        tg.send(chat_id, "查询失败：返回错误或未知任务列表结构")
        return
    tasks = data.get("tasks", [])
    if not tasks:
        tg.send(chat_id, "当前没有进行中的任务。")
        return
    lines = ["进行中的任务："]
    for t in tasks[:15]:
        if not isinstance(t, dict):
            lines.append("• unknown\n  unknown unknown ID: unknown")
            continue
        name = display_text(t.get("name"), 40)
        status = display_text(t.get("status"), 32)
        progress = display_text(t.get("progress"), 32)
        task_id = display_text(t.get("id"), 80)
        lines.append(f"• {name}\n  {status} {progress} ID: {task_id}")
    if len(tasks) > 15 or data.get("next_page_token"):
        lines.append("仅显示部分任务；更多任务请在 CLI 查看。")
    tg.send(chat_id, "\n".join(lines))


def handle_status(tg: Telegram, chat_id, task_id: str):
    data, err = pikpak_json("task", "get", task_id)
    if err:
        tg.send(chat_id, "查询失败：返回错误或未知任务结构")
        return
    if not isinstance(data, dict):
        tg.send(chat_id, "查询失败：返回错误或未知任务结构")
        return
    safe_id = display_text(task_id, 80)
    tg.send(chat_id, f"任务 {safe_id}\n状态：{display_text(data.get('status'), 32)}\n进度：{display_text(data.get('progress'), 32)}\n文件名：{display_text(data.get('file_name'))}")


def handle_ls(tg: Telegram, chat_id):
    data, err = pikpak_json("ls", "-l", "10")
    if err:
        tg.send(chat_id, f"查询失败：{err}")
        return
    token = data.get("next_page_token", "") if isinstance(data, dict) else None
    if (not isinstance(data, dict) or not isinstance(data.get("files"), list)
            or not isinstance(token, str)
            or any(not isinstance(f, dict) or not isinstance(f.get("name"), str)
                   or ("kind" in f and not isinstance(f["kind"], str)) for f in data["files"])):
        tg.send(chat_id, "目录查询未确认：未知 files/记录/分页结构，不能判断目录为空。")
        return
    files = data["files"]
    if not files:
        tg.send(chat_id, "本页无条目，但仍有后页；目录查询未确认完整。" if token else "根目录是空的。")
        return
    lines = ["根目录最近文件："]
    for f in files[:10]:
        kind = "目录" if f.get("kind") == "drive#folder" else "文件"
        lines.append(f"{kind} {display_text(f['name'][:50], 50)}")
    if token or len(files) > 10:
        lines.append("仅展示部分条目；仍有后页或条目，请在 CLI 查看。")
    tg.send(chat_id, "\n".join(lines))


def process_message(tg: Telegram, msg: dict, allowed: set, *, pikpak_store=None):
    chat = msg.get("chat") or {}
    chat_id = str(chat.get("id", ""))
    text = (msg.get("text") or "").strip()
    if not text:
        return

    if chat_id not in allowed:
        log(f"拒绝未授权 chat_id={chat_id} 的消息")
        return  # 静默拒绝，不回复（不给陌生人任何反馈）

    sender = msg.get("from") or {}
    sender_id = str(sender.get("id", ""))
    users = parse_allowed(os.environ.get("PIKPAK_ALLOWED_USER_IDS", ""))
    private = chat.get("type") == "private" and sender_id == chat_id
    if (not sender_id or sender.get("is_bot") or msg.get("sender_chat")
            or chat.get("type") not in {"private", "group", "supergroup"}
            or (chat.get("type") == "private" and not private)
            or (not private and sender_id not in users)):
        log("拒绝未授权或匿名发送者")
        return

    log("收到已授权消息")

    if text.startswith("/help") or text == "/start":
        tg.send(chat_id, HELP_TEXT)
    elif text.startswith("/save"):
        return handle_save(tg, chat_id, text, pikpak_store=pikpak_store)
    elif text.startswith("/tasks"):
        handle_tasks(tg, chat_id)
    elif text.startswith("/status"):
        parts = text.split()
        if len(parts) < 2:
            tg.send(chat_id, "用法：/status <taskID>")
        else:
            handle_status(tg, chat_id, parts[1])
    elif text.startswith("/ls"):
        handle_ls(tg, chat_id)
    elif MAGNET_RE.match(text):
        # 纯链接消息：按默认保存处理
        return handle_save(tg, chat_id, f"/save {text}", pikpak_store=pikpak_store)
    else:
        tg.send(chat_id, "没看懂。发一个磁力/链接，或发送 /help 查看指令。")


# ---------------------------------------------------------------------------
# 主循环
# ---------------------------------------------------------------------------

def parse_allowed(value: str) -> set:
    return {x.strip() for x in value.split(",") if x.strip()}


def resynchronize(tg, store):
    """Explicit operator action: inspect pending IDs without acknowledging them.

    Keep every chat/message receipt. A new epoch namespaces reused update IDs.
    No offset is guessed and no business command is executed in this entry.
    """
    with store.transaction() as state:
        if not store.needs_resync(state, time.time()):
            raise ValueError("非空闲/阻塞状态不能任意 resync 或降低 offset")
        state["resync_required"] = True
        store.save(state)
        updates = tg.get_updates()  # Never send the stale high offset or -1.
        if (not isinstance(updates, list) or not updates
                or any(not isinstance(u, dict) or type(u.get("update_id")) is not int
                       or u["update_id"] < 0 for u in updates)):
            raise ResyncRequired("resync 未得到有效非空 pending updates；仍阻塞，请人工确认后重试 --resync")
        now = time.time()
        state.update(epoch=state["epoch"] + 1,
                     next_offset=min(u["update_id"] for u in updates),
                     last_observed_at=_pending_generation_boundary(updates, now),
                     resync_required=False)
        store.save(state)
        log("resync 已建立新序列；消息账本保留，本入口未执行业务；正常启动才处理 pending updates")


def check_mode(tg: Telegram):
    """列出最近跟 bot 有过对话的 chat（帮用户拿 chat_id）。"""
    updates = tg.get_updates()
    if updates is None:
        die("获取 updates 失败，请检查 token。")
    seen = {}
    for u in updates:
        msg = u.get("message") or {}
        chat = msg.get("chat") or {}
        if chat.get("id"):
            seen[str(chat["id"])] = chat.get("title") or chat.get("username") or chat.get("first_name") or "?"
    if not seen:
        print("还没有人给 bot 发过消息。请先在 Telegram 里给 bot 发一条消息（比如 /start），再重跑 --check。")
    else:
        print("发现以下 chat：")
        for cid, name in seen.items():
            print(f"  chat_id={cid}  ({name})")
        print("\n把要用的人的 chat_id 填进 PIKPAK_ALLOWED_CHAT_IDS（逗号分隔）。")


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    modes = ap.add_mutually_exclusive_group()
    modes.add_argument("--check", action="store_true", help="列出最近与 bot 对话的 chat id 后退出（真实轮询）")
    modes.add_argument("--once", action="store_true", help="真实处理一轮后退出（不是离线测试）")
    modes.add_argument("--resync", action="store_true", help="人工恢复空闲序列：不带 offset 查询并保留消息账本，不执行业务")
    args = ap.parse_args()

    token = os.environ.get("TG_BOT_TOKEN", "").strip()
    if not token:
        die("未设置 TG_BOT_TOKEN。请在 BotFather 创建 bot 后：export TG_BOT_TOKEN=\"...\"")

    scope = os.environ.get("PIKPAK_ACCOUNT_SCOPE", "").strip()
    if not scope:
        die("必须设置 PIKPAK_ACCOUNT_SCOPE 为当前账号的非敏感本地别名；换账号必须换别名")
    directory = os.environ.get("PIKPAK_AUTOMATION_STATE_DIR")
    store = UpdateStore(Path(directory) if directory else Path.home() / ".pikpak" / "automation", scope, token)
    base = os.environ.get("TG_API_BASE", "https://api.telegram.org")
    tg = Telegram(token, base, store=store)

    if args.resync:
        resynchronize(tg, store)
        return
    if args.check:
        check_mode(tg)
        return

    allowed = parse_allowed(os.environ.get("PIKPAK_ALLOWED_CHAT_IDS", ""))
    if not allowed:
        die("未设置 PIKPAK_ALLOWED_CHAT_IDS（白名单为空时拒绝所有消息）。\n"
            "先运行 --check 获取你的 chat_id，再设置后启动。")

    store.prepare_poll()  # Fail closed before version/any old-offset polling.
    # A durable account failure gates even the version probe after restart.
    if store.pikpak_retry_after() == 0:
        rc, out, err = pikpak("version", timeout=15)
        if rc != 0:
            log("警告：pikpak version 不可用；未输出错误正文。")

    log(f"Bot 启动。白名单 {len(allowed)} 个 chat。Ctrl+C 退出。")
    offset = store.read().get("next_offset")
    while True:
        if tg.fatal:
            die("Telegram 永久错误；请人工核对传输状态，未重放业务命令")
        pikpak_wait = store.pikpak_retry_after()
        if pikpak_wait:
            if args.once:
                die("PikPak 账号处于持久冷却；未领取后续消息")
            time.sleep(pikpak_wait)
            continue
        if tg.retry_after:
            if args.once:
                die("Telegram 尚在持久冷却期；未领取后续消息")
            time.sleep(tg.retry_after)
            continue
        offset = store.prepare_poll()
        updates = tg.get_updates(offset)
        if updates is None:
            if args.once or tg.fatal:
                die("Telegram 轮询失败；未输出请求 URL 或异常正文")
            continue  # All methods persist their cooldown before returning.
        offset = process_updates(tg, updates, allowed, store)
        if tg.fatal:
            die("Telegram 回复永久失败；未领取后续消息")
        if store.pikpak_retry_after():
            if args.once:
                die("PikPak 提交结果未确认并进入持久冷却；未领取后续消息")
            continue
        if args.once:
            if tg.retry_after:
                die("Telegram 回复失败并进入持久冷却；未领取后续消息")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n已退出。")
    except ResyncRequired as exc:
        die(str(exc))
    except Exception as exc:
        die(f"Bot 停止 ({type(exc).__name__})；未输出请求或异常正文")
