---
name: ssh
description: SSH 连接和管理远程服务器。使用 paramiko (Python) 库，支持在 Windows/Linux 上通过 SSH 执行远程命令、安装软件、查看日志等操作。
---

# SSH Server Management

## Quick Connect

使用 paramiko 进行 SSH 连接：

```python
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('目标IP', username='用户名', password='密码')

# 执行命令
stdin, stdout, stderr = ssh.exec_command('你的命令')
print(stdout.read().decode())

ssh.close()
```

## Parameters

- `host`: 服务器 IP 地址
- `username`: SSH 用户名
- `password`: SSH 密码
- `command`: 要执行的命令

## Usage Examples

**基本连接测试：**
```python
ssh.connect('10.0.3.120', username='root', password='7758258Cc')
```

**执行单个命令：**
```python
stdin, stdout, stderr = ssh.exec_command('uptime')
print(stdout.read().decode())
```

**执行多个命令：**
```python
commands = ['cd /var/log', 'ls -la', 'cat syslog | tail -20']
for cmd in commands:
    ssh.exec_command(cmd)
```

**交互式会话：**
```python
shell = ssh.invoke_shell()
shell.send('apt update\n')
time.sleep(2)
print(shell.recv(4096).decode())
```

## Best Practices

- ✅ 使用 paramiko 是 Windows/Linux 通用的最可靠方案
- ✅ 始终使用 `paramiko.AutoAddPolicy()` 自动处理主机密钥
- ⚠️ Windows OpenSSH 不支持某些 OpenSSH 语法
- ⚠️ sshpass 仅限 Linux
- ⚠️ plink 语法与 OpenSSH 不兼容

## Troubleshooting

**连接超时：** 检查 IP、用户名、密码是否正确
**权限错误：** 确认用户有执行权限
**主机密钥拒绝：** 使用 `AutoAddPolicy()` 或手动添加主机密钥

## See Also

- [Usage Guide](references/usage.md) - 详细使用说明
- [Common Commands](references/commands.md) - 常用命令参考
