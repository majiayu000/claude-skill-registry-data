#!/usr/bin/env python3
"""Inspect a JSON task receipt from stdin; no CLI, network or credential access."""
import argparse
import json
import re
import sys


ID_PATTERN = r'[A-Za-z0-9_][A-Za-z0-9_-]{0,255}'


def _response_containers(data):
    if not isinstance(data, dict):
        raise ValueError('需要 JSON 对象')
    nested = data.get('task')
    if 'task' in data and not isinstance(nested, dict):
        raise ValueError('任务包络结构非法')
    return (data, nested) if isinstance(nested, dict) else (data,)


def _reject_failure_envelope(containers):
    for container in containers:
        for field in ('ok', 'success'):
            if field in container and container[field] is not True:
                raise ValueError('显式失败或畸形包络；不输出成功下一步')
        if any(field in container for field in ('error', 'error_code', 'code')):
            raise ValueError('显式失败包络；不输出成功下一步')


def _collect_ids(containers):
    task_ids, file_ids = [], []
    for container in containers:
        for field in ('task_id', 'id'):
            if field in container:
                value = container[field]
                if not isinstance(value, str) or not re.fullmatch(ID_PATTERN, value):
                    raise ValueError('任务 ID 字段非法')
                task_ids.append(value)
        if 'file_id' in container:
            value = container['file_id']
            if not isinstance(value, str) or not re.fullmatch(ID_PATTERN, value):
                raise ValueError('文件 ID 字段非法')
            file_ids.append(value)
    if len(set(task_ids)) > 1 or len(set(file_ids)) > 1:
        raise ValueError('任务或文件 ID 字段冲突')
    return (task_ids[0] if task_ids else None,
            file_ids[0] if file_ids else None)


def _normalise_status(value):
    if not isinstance(value, str):
        raise ValueError('状态字段非法')
    value = value.strip().lower()
    if value.startswith('phase_type_'):
        value = value.removeprefix('phase_type_')
    if value not in ('pending', 'running', 'complete', 'error'):
        raise ValueError('未知状态；停止而不是无限等待')
    return value


def _collect_status(containers):
    statuses = []
    for container in containers:
        for field in ('status', 'phase'):
            if field in container:
                statuses.append(_normalise_status(container[field]))
    if len(set(statuses)) > 1:
        raise ValueError('状态字段冲突')
    return statuses[0] if statuses else None


def inspect_task(data, expected_id):
    containers = _response_containers(data)
    _reject_failure_envelope(containers)
    task = containers[-1]
    task_id, file_id = _collect_ids(containers)
    if not isinstance(expected_id, str) or not re.fullmatch(ID_PATTERN, expected_id):
        raise ValueError('预期任务 ID 格式不安全')
    if task_id != expected_id:
        raise ValueError('任务 ID 缺失或不匹配；不得按文件名/首条任务猜测')
    status = _collect_status(containers)
    if status is None:
        raise ValueError('未知状态；停止而不是无限等待')
    if status == 'complete' and file_id is None:
        raise ValueError('complete 仍须有有效 file_id；不输出播放/下载指令')
    actions = {'complete': '按此 file_id 核对文件；不从根目录猜测',
               'error': '保留错误记录；核对配额/容量，不自动删除或重新创建',
               'pending': '稍后按相同 task_id 查询一次；达到用户等待预算就停止',
               'running': '稍后按相同 task_id 查询一次；达到用户等待预算就停止'}
    return {'task_id': task_id, 'status': status, 'file_id': file_id if status == 'complete' else '',
            'next': actions[status]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--task-id', required=True)
    args = parser.parse_args()
    try:
        result = inspect_task(json.load(sys.stdin), args.task_id)
    except (ValueError, TypeError):
        print('任务收据非法、缺字段或 ID 不符；停止并在本地检查 CLI 契约。', file=sys.stderr)
        raise SystemExit(1)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result['status'] == 'error':
        raise SystemExit(2)


if __name__ == '__main__':
    main()
