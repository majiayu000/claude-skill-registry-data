---
name: windows-vm
description: "Use when provisioning a headless Windows 11 VM in Docker for testing, running Windows-only tools, or installing Claude Code on Windows. Triggers on: 'windows vm', 'windows docker', 'headless windows', 'windows 11 container', 'windows vm ssh', 'kvm windows', 'dockur windows', 'windows dev environment', 'windows claude code', 'windows test environment'."
source: obra/superpowers-lab (MIT) — superpowers-lab/skills/windows-vm
tier: TIER 3 — PRODUCTIVITY
---

# Windows VM — Headless Windows 11 in Docker
# Source: obra/superpowers-lab (MIT) — github.com/obra/superpowers-lab

Spin up Windows 11 headless trong Docker với KVM acceleration + SSH access.
Full Windows environment, không cần license riêng (dùng evaluation build).

---

## Requirements

```
Host:    Docker, KVM support (/dev/kvm), sshpass
VM:      8GB RAM, 4 CPU cores, 64GB disk (allocated từ host)
Network: localhost:2222 (SSH), localhost:8006 (VNC web UI)
Time:    First setup 20-30 min (Windows install), sau đó ~2 min boot
```

---

## VM Lifecycle Commands

```bash
# Create / full setup (first time)
# → creates Docker volumes + installs Windows
bash core/skills/windows-vm/vm-manage.sh create

# Start existing VM
bash core/skills/windows-vm/vm-manage.sh start

# Stop gracefully
bash core/skills/windows-vm/vm-manage.sh stop

# Restart
bash core/skills/windows-vm/vm-manage.sh restart

# SSH into VM
bash core/skills/windows-vm/vm-manage.sh ssh

# Check status
bash core/skills/windows-vm/vm-manage.sh status

# Debug via VNC (opens browser)
bash core/skills/windows-vm/vm-manage.sh screenshot
```

---

## Manual Docker Setup

```bash
# Create local storage dirs
mkdir -p ~/windows-vm/storage ~/windows-vm/config

# create install.bat (runs after Windows installs)
cat > ~/windows-vm/config/install.bat << 'EOF'
@echo off
:: Install OpenSSH Server
powershell -Command "Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0"
powershell -Command "Set-Service -Name sshd -StartupType Automatic"
powershell -Command "Start-Service sshd"

:: Allow SSH through firewall
netsh advfirewall firewall add rule name="OpenSSH" dir=in action=allow protocol=tcp localport=22
EOF

# Launch container
docker run -d \
  --name windows-vm \
  -p 2222:22 \
  -p 8006:8006 \
  -e RAM_SIZE="8G" \
  -e CPU_CORES="4" \
  -e DISK_SIZE="64G" \
  -e USERNAME="user" \
  -e PASSWORD="password" \
  -v ~/windows-vm/storage:/storage \
  -v ~/windows-vm/config:/shared \
  --device /dev/kvm \
  --cap-add NET_ADMIN \
  dockurr/windows

# Follow install progress
docker logs -f windows-vm
```

---

## SSH Access

```bash
# Default credentials: user / password
ssh -p 2222 user@localhost

# Non-interactive (sshpass)
sshpass -p "password" ssh -p 2222 -o StrictHostKeyChecking=no user@localhost "dir C:\\"

# Run PowerShell command
sshpass -p "password" ssh -p 2222 user@localhost \
  "powershell -Command \"Get-Process | Select-Object -First 5\""
```

---

## Install Dev Tools (Claude Code)

```bash
# Cách đúng: pipe qua PowerShell, không pipe trực tiếp vào bash
sshpass -p "password" ssh -p 2222 user@localhost \
  'powershell -Command "iwr https://nodejs.org/dist/v20.11.0/node-v20.11.0-x64.msi -OutFile node.msi; Start-Process msiexec -Args \"/i node.msi /quiet\" -Wait"'

# Install Claude Code sau khi Node.js ready
sshpass -p "password" ssh -p 2222 user@localhost \
  'powershell -Command "npm install -g @anthropic-ai/claude-code"'

# Fix PATH (system-level, không phải user-level!)
sshpass -p "password" ssh -p 2222 user@localhost \
  'powershell -Command "[System.Environment]::SetEnvironmentVariable(\"PATH\", $env:PATH + \";C:\\Users\\user\\AppData\\Roaming\\npm\", \"Machine\")"'
```

---

## Critical Gotchas

```
1. PATH phải set ở MACHINE level, không phải USER level
   Lý do: SSH sessions không load user profile đầy đủ

2. PowerShell execution policy cần RemoteSigned:
   Set-ExecutionPolicy RemoteSigned -Scope LocalMachine

3. Lần đầu boot mất 20-30 min — không SSH trong khi đang install
   Theo dõi: docker logs -f windows-vm | grep -i "ready\|complete\|ssh"

4. VNC debug UI: http://localhost:8006 (không cần VNC client)

5. Interactive SSH cần custom PowerShell profile để inherit env vars từ registry
```

---

## Status Check

```bash
docker inspect windows-vm --format '{{.State.Status}}'
# → running / exited / created

# Kiểm tra SSH ready
sshpass -p "password" ssh -p 2222 -o ConnectTimeout=5 \
  -o StrictHostKeyChecking=no user@localhost "echo ok" 2>/dev/null \
  && echo "SSH ready" || echo "SSH not ready yet"
```

---

## Cleanup

```bash
docker stop windows-vm
docker rm windows-vm
# Xóa disk (64GB) nếu không cần nữa
docker volume rm windows-vm_storage
```

---

## Anti-Fake-Pass Checks

```
❌ FAIL nếu SSH trong khi Windows vẫn đang install (mất 20-30 min)
❌ FAIL nếu set PATH ở user level thay vì machine level
❌ FAIL nếu host không có /dev/kvm (VM chạy rất chậm không dùng được)
✅ PASS khi: ssh trả về "ok" + node --version + claude --version chạy được
```

## See also
- `docker-patterns` — Docker container management
- `execution-environment` — sandbox isolation policy

