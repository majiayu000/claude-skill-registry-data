#!/usr/bin/env python3
"""PikPak 分步管道：单次创建、按 ID 查询、单文件下载、只打印清理建议。

每项资源使用独立 --state 文件。CLI 不提供服务端幂等键：提交超时或
返回缺失 ID 时保留 submitting 状态，禁止自动再次创建。状态文件不是凭据。
PIKPAK_BIN 可指定可执行文件；测试只使用中性假程序。
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import hmac
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile
from typing import NoReturn
from urllib.parse import urlsplit


ID_PATTERN = r"[A-Za-z0-9_][A-Za-z0-9_-]{0,255}"
ACCOUNT_SCOPE_PATTERN = r"[A-Za-z0-9_][A-Za-z0-9_.-]{0,63}"
ACCOUNT_SCOPE_BINDING = 'operator_declared_unverified'
ACCOUNT_ID_KEYS = ('account_id', 'accountId', 'user_id', 'userId', 'uid')
ACCOUNT_ID_CONTAINERS = ('profile', 'user', 'account')
_CREDENTIAL_TEXT_RE = re.compile(
    r"token|password|passwd|pass[ _-]?code|secret|authorization|bearer|cookie|"
    r"credential|api[ _-]?key|session[ _-]?(?:id|key)|https?://",
    re.IGNORECASE,
)


def safe_progress(value):
    """Return only a bounded, credential-free percentage scalar."""
    if type(value) is str:
        candidate = value.strip()
    elif type(value) is int and 0 <= value <= 100:
        candidate = f"{value}%"
    elif type(value) is float and value == value and value not in (float('inf'), float('-inf')) \
            and 0 <= value <= 100:
        candidate = f"{value:g}%"
    else:
        return 'unknown'
    if (not candidate or len(candidate) > 16 or not candidate.isprintable()
            or _CREDENTIAL_TEXT_RE.search(candidate)
            or not re.fullmatch(r"(?:0|[1-9][0-9]{0,2})(?:\.[0-9]{1,2})?%", candidate)
            or float(candidate.rstrip('%')) > 100):
        return 'unknown'
    return candidate


def die(msg: str, code: int = 1) -> NoReturn:
    print(f"错误：{msg}", file=sys.stderr)
    raise SystemExit(code)


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(ID_PATTERN, value):
        die("ID 格式不安全；不修正、不执行、不生成命令。")
    return value


def account_scope(value):
    if not isinstance(value, str) or not re.fullmatch(ACCOUNT_SCOPE_PATTERN, value):
        die("必须显式确认当前账号与收据归属；account scope 仅为操作者声明，不是身份验证。")
    return value


def identity_digest(value):
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise ValueError('账号身份字段类型非法')
    text = str(value)
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.:@-]{0,255}', text):
        raise ValueError('账号身份字段格式非法')
    return hashlib.sha256(('pikpak-account-v1:' + text).encode()).hexdigest()


def auth_identity_digest(data):
    if not isinstance(data, dict):
        raise ValueError('登录响应不是对象')
    candidates = []
    for key in ACCOUNT_ID_KEYS:
        if key in data:
            candidates.append(identity_digest(data[key]))
    for container_name in ACCOUNT_ID_CONTAINERS:
        container = data.get(container_name)
        if not isinstance(container, dict):
            continue
        if 'id' in container:
            candidates.append(identity_digest(container['id']))
        for key in ACCOUNT_ID_KEYS:
            if key in container:
                candidates.append(identity_digest(container[key]))
    if len(set(candidates)) != 1:
        raise ValueError('缺少稳定账号身份或身份字段冲突')
    return candidates[0]


def runtime_identity_digest(args):
    value = getattr(args, '_account_identity_hash', None)
    if not isinstance(value, str) or not re.fullmatch(r'[0-9a-f]{64}', value):
        die('当前登录响应没有可核对的稳定账号身份；停止，不把 account scope 当作身份验证。')
    return value


def require_account_scope(args, state):
    stored = state.get('account_scope')
    if not isinstance(stored, str):
        die("旧收据缺少 account scope；不静默迁移或跨账号继续。")
    if state.get('account_scope_binding') != ACCOUNT_SCOPE_BINDING:
        die("收据未标明 account scope 只是操作者声明；不把它当作账号身份验证。")
    stored = account_scope(stored)
    requested = account_scope(getattr(args, 'account_scope', None))
    if requested != stored:
        die("当前 account scope 与收据不一致；不跨账号继续。")
    runtime = runtime_identity_digest(args)
    stored_identity = state.get('account_identity_sha256')
    if not isinstance(stored_identity, str) or not re.fullmatch(r'[0-9a-f]{64}', stored_identity):
        die('收据缺少稳定账号身份收据；不跨账号继续。')
    if not hmac.compare_digest(stored_identity, runtime):
        die('当前登录账号与收据身份不一致；停止，不跨账号继续。')
    return stored


def response_containers(data):
    if not isinstance(data, dict):
        raise ValueError('响应不是 JSON 对象')
    nested = data.get('task')
    if 'task' in data and not isinstance(nested, dict):
        raise ValueError('任务包络结构非法')
    return (data, nested) if isinstance(nested, dict) else (data,)


def reject_failure_envelope(data):
    for container in response_containers(data):
        for field in ('ok', 'success'):
            if field in container and container[field] is not True:
                raise ValueError('显式失败或畸形包络')
        if any(field in container for field in ('error', 'error_code', 'code')):
            raise ValueError('显式失败包络')


def response_ids(data):
    task_ids, file_ids = [], []
    for container in response_containers(data):
        for field in ('task_id', 'id'):
            if field in container:
                value = container[field]
                if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_-]{0,255}", value):
                    raise ValueError('任务 ID 字段非法')
                task_ids.append(value)
        if 'file_id' in container:
            value = container['file_id']
            if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_-]{0,255}", value):
                raise ValueError('文件 ID 字段非法')
            file_ids.append(value)
    if len(set(task_ids)) > 1 or len(set(file_ids)) > 1:
        raise ValueError('任务或文件 ID 字段冲突')
    return (task_ids[0] if task_ids else None,
            file_ids[0] if file_ids else None)


def response_status(data):
    statuses = []
    for container in response_containers(data):
        for field in ('status', 'phase'):
            if field in container:
                value = container[field]
                if not isinstance(value, str):
                    raise ValueError('状态字段非法')
                value = value.strip().lower()
                if value.startswith('phase_type_'):
                    value = value.removeprefix('phase_type_')
                if value not in ('pending', 'running', 'error', 'complete'):
                    raise ValueError('未知任务状态')
                statuses.append(value)
    if len(set(statuses)) > 1:
        raise ValueError('状态字段冲突')
    if not statuses:
        raise ValueError('缺少任务状态')
    return statuses[0]


def response_folder(data, requested):
    observed = []
    for container in response_containers(data):
        for field in ('folder_id', 'parent_id', 'parent_folder_id', 'folder', 'parent'):
            if field in container:
                value = container[field]
                if not isinstance(value, str) or not re.fullmatch(
                        r"[A-Za-z0-9_][A-Za-z0-9_-]{0,255}", value):
                    raise ValueError('目录字段非法')
                observed.append(value)
    if len(set(observed)) > 1:
        raise ValueError('目录字段冲突')
    if not requested:
        return 'not_requested'
    if not observed:
        return 'unknown'
    if observed[0] != requested:
        raise ValueError('目录字段不匹配')
    return 'matched'


def pikpak(*args: str, timeout: int = 300, fmt_json: bool = False):
    cmd = [os.environ.get("PIKPAK_BIN", "pikpak"), *args]
    if fmt_json:
        cmd += ["-F", "json"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return proc.returncode, proc.stdout, proc.stderr
    except FileNotFoundError:
        die("找不到 PikPak CLI。安装页：https://mypikpak.com/cli")
    except subprocess.TimeoutExpired:
        # Return a classified failure so callers can persist their safe state:
        # task get revokes old qualification; task add remains submitting.
        # Never retain partial output or the exception's command/body.
        return 124, '', ''


def pikpak_json(*args: str, timeout: int = 300):
    rc, out, _ = pikpak(*args, timeout=timeout, fmt_json=True)
    if rc != 0:
        # Do not echo arbitrary stdout/stderr: it may contain URLs or tokens.
        return None, f"CLI 退出码 {rc}；请在本地核对错误，勿粘贴凭据或直链"
    try:
        data = json.loads(out)
        if not isinstance(data, dict):
            raise ValueError("object required")
    except (ValueError, TypeError):
        return None, "CLI 未返回 JSON 对象，停止而非猜测字段"
    try:
        reject_failure_envelope(data)
    except ValueError:
        return None, "CLI 返回显式失败或畸形包络，停止而非使用成功字段"
    return data, None


def check_login():
    # `logged_in` alone does not identify the account. Require one stable ID from
    # a small allowlist of profile fields and retain only its domain-separated hash.
    data, err = pikpak_json("auth", "status", timeout=60)
    if err or not data or data.get("logged_in") is not True:
        die("未确认 CLI 登录状态；由用户先完成 `pikpak auth login`，并另行确认 account scope。")
    try:
        reject_failure_envelope(data)
        return auth_identity_digest(data)
    except ValueError:
        die('当前登录响应没有可核对的稳定账号身份或包含失败包络；停止，不把 account scope 当作身份验证。')


def read_state(args):
    path = getattr(args, 'state', None)
    if not path:
        return {}
    path = Path(path).expanduser()
    if path.is_symlink():
        die("拒绝符号链接状态文件")
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text())
        if not isinstance(data, dict) or data.get('version') != 1:
            raise ValueError('state schema')
        return data
    except (OSError, ValueError):
        die("状态文件损坏或版本未知；保留文件，人工核对，禁止重新创建。")


def write_state(args, data):
    path = getattr(args, 'state', None)
    if not path:
        return
    path = Path(path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent,
                                     prefix=path.name + '.', delete=False) as handle:
        json.dump({'version': 1, **data}, handle, ensure_ascii=False, indent=2)
        handle.flush()
        os.fsync(handle.fileno())
        tmp = handle.name
    os.replace(tmp, path)


def revoke_qualification(args, state, category):
    if state.get('stage') not in ('ready', 'downloaded') and state.get('latest_task_status') != 'complete':
        return
    revoked = dict(state)
    revoked['stage'] = 'blocked'
    revoked.pop('latest_task_status', None)
    revoked['last_rejected_observation'] = category
    write_state(args, revoked)


def reject_observation(args, state, message, category='response_rejected') -> NoReturn:
    revoke_qualification(args, state, category)
    die(message)


def bound_state(args):
    state = read_state(args)
    fingerprint = state.get('fingerprint')
    if (not getattr(args, 'state', None) or not isinstance(fingerprint, str)
            or not re.fullmatch(r'[0-9a-f]{64}', fingerprint)
            or not isinstance(state.get('folder'), str)):
        die('缺少完整来源指纹/目录状态；不能把孤立状态标志当作本次任务收据。')
    require_account_scope(args, state)
    if state['folder']:
        identifier(state['folder'])
    if not state.get('task_id'):
        die('状态缺少已确认的任务 ID；提交结果未知时须先人工对账，不能通过查询认领。')
    identifier(state['task_id'])
    return state


@contextmanager
def state_lock(args):
    path = Path(args.state).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = path.with_name(path.name + '.lock')
    try:
        fd = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        die("状态已被锁定；不要并行提交。崩溃后先人工核对进程和远端任务，再移走旧锁。")
    try:
        os.close(fd)
        yield
    finally:
        lock.unlink()


def emit(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


def step1_add(args):
    url = args.magnet
    if not isinstance(url, str) or any(c in url for c in '\r\n\x00'):
        die('链接格式不安全')
    parsed = urlsplit(url)
    if parsed.scheme not in ('magnet', 'http', 'https') or (parsed.scheme != 'magnet' and not parsed.netloc):
        die('只接受明确的 magnet / HTTP / HTTPS 链接')
    scope = account_scope(getattr(args, 'account_scope', None))
    if args.folder:
        identifier(args.folder)
    fingerprint = hashlib.sha256(json.dumps([url, args.folder], ensure_ascii=False).encode()).hexdigest()
    state = read_state(args)
    runtime_identity = runtime_identity_digest(args)
    if state:
        if state.get('account_scope') != scope:
            die('状态缺少或不匹配 account scope；不静默迁移或跨账号继续。')
        if state.get('account_scope_binding') != ACCOUNT_SCOPE_BINDING:
            die('状态未标明 account scope 只是操作者声明；不静默迁移旧收据。')
        stored_identity = state.get('account_identity_sha256')
        if (not isinstance(stored_identity, str)
                or not hmac.compare_digest(stored_identity, runtime_identity)):
            die('当前登录账号与状态收据身份不一致；不跨账号继续。')
        if state.get('fingerprint') != fingerprint:
            die('状态属于不同链接或目录；请为新资源指定另一 --state 文件。')
        if state.get('task_id'):
            identifier(state['task_id'])
            emit({'step': 'add', 'status': 'reused', 'task_id': state['task_id']})
            return
        die('上次提交结果未知；先人工核对确切任务 ID，不自动重试或按名称猜测。')
    state = {'fingerprint': fingerprint, 'stage': 'submitting', 'folder': args.folder,
             'account_scope': scope, 'account_scope_binding': ACCOUNT_SCOPE_BINDING,
             'account_identity_sha256': runtime_identity}
    write_state(args, state)  # Persist intent before any non-idempotent network call.
    cmd = ['task', 'add', url]
    if args.folder:
        cmd += ['-p', args.folder]
    data, err = pikpak_json(*cmd, timeout=180)
    if err or data is None:
        die('提交未确认；错误分类：response_unavailable；保留 submitting 状态。')
    try:
        reject_failure_envelope(data)
        tid, _ = response_ids(data)
        folder_status = response_folder(data, args.folder)
        containers = response_containers(data)
        if any(field in container for container in containers for field in ('status', 'phase')):
            if response_status(data) == 'error':
                raise ValueError('提交状态为 error')
    except ValueError:
        die('提交响应失败或字段非法；保留 submitting 状态，不自动重提。')
    if not tid:
        die('返回缺少任务 ID；可能已创建，保留 submitting 状态，禁止自动重提。')
    identifier(tid)
    state.update(task_id=tid, stage='submitted', folder_verification=folder_status)
    write_state(args, state)
    emit({'step': 'add', 'status': 'submitted', 'task_id': tid})


def step2_status(args):
    tid = identifier(args.task_id)
    state = bound_state(args)
    if state['task_id'] != tid:
        die('任务 ID 与状态记录不一致')
    data, err = pikpak_json('task', 'get', tid, timeout=120)
    if err or data is None:
        reject_observation(args, state, '查询失败；未授予 ready。', 'query_failure')
    try:
        reject_failure_envelope(data)
        returned, file_id = response_ids(data)
        task = response_containers(data)[-1]
        folder_status = response_folder(data, state['folder'])
    except ValueError:
        reject_observation(args, state,
                           '查询响应失败或字段非法；不使用其他任务的文件。',
                           'response_rejected')
    if returned != tid:
        reject_observation(args, state,
                           '返回的任务 ID 缺失或不匹配；不使用其他任务的文件。',
                           'identity_mismatch')
    try:
        status = response_status(data)
    except ValueError:
        reject_observation(args, state,
                           '查询响应状态非法或冲突；停止且不授予 ready。',
                           'status_conflict')
    result = {'step': 'status', 'task_id': tid, 'status': status,
              'progress': safe_progress(task.get('progress')), 'file_id': file_id or '',
              'folder_verification': folder_status}
    state['latest_task_status'] = status
    state['folder_verification'] = folder_status
    if status == 'complete':
        if not file_id:
            reject_observation(args, state,
                               'complete 响应缺少有效 file_id；不授予 ready。',
                               'missing_file_id')
        if state.get('file_id') != file_id:
            # A previous local receipt must never be rebound to another file.
            for field in ('local_path', 'local_size', 'local_sha256'):
                state.pop(field, None)
        state.update(stage='ready', file_id=file_id)
        if local_receipt_matches(state):
            state['stage'] = 'downloaded'
        write_state(args, state)
    elif status == 'error':
        if state:
            state.update(stage='failed')
            write_state(args, state)
        emit({**result, 'next': '任务失败；本地核对原因/额度/容量。不自动删除或重新创建。'})
        raise SystemExit(2)
    else:
        state.update(stage='waiting')
        write_state(args, state)
    emit(result)


def step3_download(args):
    fid = identifier(args.file_id)
    state = bound_state(args)
    if (state.get('file_id') != fid or state.get('stage') not in ('ready', 'downloaded')
            or state.get('latest_task_status') != 'complete'
            or (state.get('folder') and state.get('folder_verification') != 'matched')):
        die('尚无匹配的 complete 任务；先执行 step2-status。')
    dest = Path(args.dest).expanduser().resolve()
    dest.mkdir(parents=True, exist_ok=True)
    target = dest / fid  # -o is a file path, NOT a destination directory.
    if target.exists() or target.is_symlink():
        die('目标文件已存在；先人工核验或指定新目录，不覆盖。')
    partial = dest / (fid + '.part')
    if partial.exists() or partial.is_symlink():
        die('存在中断文件；先人工核验/移走，再重试，不承诺 CLI 断点续传。')
    if state:
        state.update(stage='ready', local_path=str(target))
        write_state(args, state)
    rc, _, _ = pikpak('download', fid, '-o', str(partial), timeout=7200)
    if rc != 0:
        die('下载失败；保留本地中断文件，未改变目标目录，也不生成清理命令。')
    if not partial.is_file() or partial.is_symlink():
        die('CLI 未生成预期普通文件；不标记下载成功。文件夹请改用批量备份。')
    # Never overwrite a target that appeared while the CLI was running.
    try:
        os.link(partial, target)
    except FileExistsError:
        die('目标文件在下载期间出现；保留 .part，不覆盖。')
    partial.unlink()
    if state:
        state.update(stage='downloaded', local_path=str(target), local_size=target.stat().st_size,
                     local_sha256=hash_file(target))
        write_state(args, state)
    emit({'step': 'download', 'status': 'downloaded_unverified', 'file_id': fid,
          'local_path': str(target), 'bytes': target.stat().st_size,
          'next': '人工核对内容、大小/校验和；CLI 成功退出不等于内容完整。'})


def hash_file(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def local_receipt_matches(state):
    path = state.get('local_path')
    if not isinstance(path, str) or not path:
        return False
    local = Path(path)
    return (local.is_file() and not local.is_symlink()
            and local.stat().st_size == state.get('local_size')
            and hash_file(local) == state.get('local_sha256'))


def step4_cleanup(args):
    # Validate every ID BEFORE printing anything executable.
    fids = list(dict.fromkeys(identifier(fid) for fid in args.file_ids))
    state = bound_state(args)
    if not getattr(args, 'state', None):
        die('清理必须提供本流程状态收据，不能仅凭任意 ID 生成命令。')
    if getattr(args, 'state', None):
        if (state.get('stage') != 'downloaded' or fids != [state.get('file_id')]
                or state.get('latest_task_status') != 'complete'
                or (state.get('folder') and state.get('folder_verification') != 'matched')):
            die('清理对象必须是本次已下载且目录绑定已验证的唯一文件；不是任意批量删除入口。')
        if not local_receipt_matches(state):
            die('本地文件缺失、大小或 SHA-256 变化，不能生成清理建议。')
        if not getattr(args, 'verified_local', False):
            die('须人工验证本地副本后显式提供 --verified-local；本地 SHA-256 未证明远端源内容一致。')
    print('仅为命令预览，未删除。请确认后手动执行；先核对当前账号和本地文件。')
    print('删除命令的回收站与恢复语义未由 --help 保证，不能承诺可恢复或已释放空间。')
    for fid in fids:
        print(shlex.join(['pikpak', 'rm', fid]))


def preflight_account_scope(args):
    state = read_state(args)
    scope = account_scope(getattr(args, 'account_scope', None))
    if args.cmd == 'step1-add':
        if state and state.get('account_scope') != scope:
            die('状态缺少或不匹配 account scope；不静默迁移或跨账号继续。')
        if state and state.get('account_scope_binding') != ACCOUNT_SCOPE_BINDING:
            die('状态未标明 account scope 只是操作者声明；不静默迁移旧收据。')
        return
    stored = state.get('account_scope')
    if not isinstance(stored, str) or state.get('account_scope_binding') != ACCOUNT_SCOPE_BINDING:
        die('状态缺少 account scope 或声明标记；不静默迁移旧收据。')
    if account_scope(stored) != scope:
        die('当前 account scope 与收据不一致；不跨账号继续。')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='cmd', required=True)
    p1 = sub.add_parser('step1-add', help='单次提交；同一状态文件重复执行复用任务')
    p1.add_argument('magnet')
    p1.add_argument('--folder', default='')
    p1.set_defaults(func=step1_add)
    p2 = sub.add_parser('step2-status', help='按精确任务 ID 查询一次，不无限轮询')
    p2.add_argument('task_id')
    p2.set_defaults(func=step2_status)
    p3 = sub.add_parser('step3-download', help='下载单文件，失败不改变目标目录')
    p3.add_argument('file_id')
    p3.add_argument('--dest', default='./downloads')
    p3.set_defaults(func=step3_download)
    cleanup_help = '先只读 auth status 核对身份摘要；人工验证后仅打印建议，不查询 task/file、不删除'
    p4 = sub.add_parser('step4-cleanup', help=cleanup_help, description=cleanup_help)
    p4.add_argument('file_ids', nargs='+')
    p4.add_argument('--verified-local', action='store_true')
    p4.set_defaults(func=step4_cleanup)
    for p in (p1, p2, p3, p4):
        p.add_argument('--state', default='./.pikpak-pipeline.json')
        p.add_argument('--account-scope', help='操作者声明的非敏感账号 scope 别名；不是身份验证')
    args = parser.parse_args()
    try:
        with state_lock(args):
            preflight_account_scope(args)
            args._account_identity_hash = check_login()
            args.func(args)
    except OSError:
        die('本地文件读写失败；保留状态和中断文件，勿自动重提或清理云端。')


if __name__ == '__main__':
    main()
