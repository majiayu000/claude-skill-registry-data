#!/usr/bin/env python3
"""Print a registration plan; never install, authenticate or open a browser."""
import argparse
import json
import shlex
from pathlib import Path


def registration_argv(code, consent):
    # Explicit empty value is essential: omission inherits installer referral.
    return ['pikpak', 'auth', 'register', '--affiliate=' + (code if consent else '')]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--choice', required=True, choices=('accept', 'decline'),
                        help='Record the user choice after disclosure; no default')
    args = parser.parse_args()
    config = json.loads((Path(__file__).resolve().parents[1] / 'config.json').read_text())
    code = config.get('affiliate_code', '')
    if not isinstance(code, str):
        parser.error('affiliate_code must be a string; do not normalize invitation codes')
    command = registration_argv(code, args.choice == 'accept')
    print(json.dumps({'action': 'plan_only', 'affiliate_code': code,
        'disclosure': '邀请码来自本指南分享者；可能使分享者获得推广奖励。福利以官方页面为准，可拒绝，不影响本指南。',
        'choice': args.choice, 'argv': command, 'command': shlex.join(command),
        'next': '核对用户已知情选择，再由用户执行并检查注册页引荐信息；本工具不执行注册。'},
        ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
