---
name: restart-4get
description: Restart the 4get proxy search engine systemd user service and verify its status
---

# restart-4get Skill

This skill provides standard procedures for restarting the **4get Proxy Search Engine** systemd user service (`4get.service`) and checking its health.

## Service Details
- **Systemd Unit**: `4get.service` (User service)
- **Unit Path**: `~/.config/systemd/user/4get.service`
- **Working Directory**: `/home/chihmin/4get-deploy`
- **Container Name**: `4get-app`
- **Local Endpoint**: `http://localhost:8088`

## Restart Instructions

### 1. Restart Service via systemd
To restart the systemd service:
```bash
systemctl --user restart 4get.service
```

### 2. Verify Systemd Status
```bash
systemctl --user status 4get.service
```

### 3. Verify Search Functionality
After restarting, run a test query to verify 4get search API:
```bash
curl -s "http://localhost:8088/api/v1/web?s=test"
```
