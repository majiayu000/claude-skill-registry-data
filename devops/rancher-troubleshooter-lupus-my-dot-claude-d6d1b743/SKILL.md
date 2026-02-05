---
name: rancher-troubleshooter
description: Diagnose and troubleshoot Rancher Desktop on WSL2, focusing on Kubernetes/K3s issues including slow API operations, etcd health problems, cluster component failures, and pod networking issues. Use when encountering Rancher Desktop errors, timeouts, or performance degradation.
---

# Rancher Troubleshooter

## Overview

This skill provides systematic diagnostic workflows and solutions for troubleshooting Rancher Desktop on WSL2. It focuses on common Kubernetes cluster issues including control plane failures, etcd health problems, slow API operations, and resource constraints.

Use this skill when:
- Kubernetes API operations timeout or are extremely slow
- `kubectl` commands take longer than expected or fail
- Rancher Desktop reports errors or fails to start
- Pods show unexpected failures or ImagePullBackOff
- Control plane components report unhealthy status
- User reports "Rancher Desktop not working" or similar issues

## Diagnostic Workflow

Follow this systematic approach to troubleshoot Rancher Desktop issues:

### 1. Initial Assessment

Start by gathering comprehensive diagnostic information to understand the current state:

**Run the diagnostic script:**
```bash
bash /path/to/scripts/diagnose-rancher.sh
```

This script collects:
- WSL distribution status
- Kubernetes cluster info and version
- Node status and resource usage
- Control plane component health
- System pod status
- Recent cluster events
- K3s service status

**Manual quick check (if script unavailable):**
```bash
# Component health (most important)
kubectl get componentstatuses

# Node and resource status
kubectl get nodes -o wide
kubectl top nodes

# Unhealthy pods
kubectl get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded
```

### 2. Issue Identification

Analyze the diagnostic output to identify the primary issue category:

#### ETCD Unhealthy
**Indicators:**
- `kubectl get componentstatuses` shows `etcd-0` as `Unhealthy`
- Error: `context deadline exceeded`
- kubectl commands timeout (especially writes like creating services)
- K3s service shows recent restart (uptime < 5 minutes)

**Action:** Proceed to "Resolving ETCD Issues" section below.

#### Image Pull Failures
**Indicators:**
- Pods in `ImagePullBackOff` or `ErrImagePull` state
- Error mentions: `failed to pull and unpack image`
- Error mentions: `pull access denied, repository does not exist`
- Image name suggests it should be local (no registry prefix, or development tags)

**Action:** Proceed to "Resolving Image Issues" section below.

#### Slow API Performance
**Indicators:**
- kubectl commands take 10+ seconds
- No specific component unhealthy, but everything is slow
- Resource usage appears normal

**Action:** Proceed to "Resolving Performance Issues" section below.

#### Service Not Starting
**Indicators:**
- Rancher Desktop UI stuck on "Starting..."
- `wsl.exe -d rancher-desktop` shows distribution stopped
- K3s service not in rc-status output

**Action:** Proceed to "Resolving Startup Issues" section below.

### 3. Resolving ETCD Issues

ETCD health issues are the most common cause of Rancher Desktop problems. K3s uses embedded etcd (not a separate pod).

**Solution 1: Restart Rancher Desktop** (fixes 80% of cases)
```bash
# From Windows: Right-click Rancher Desktop tray icon → Quit
# Wait 10-15 seconds
# Start Rancher Desktop again
# Wait 2-3 minutes for full initialization
```

**Verification:**
```bash
kubectl get componentstatuses
# All components should show "Healthy"

# Test API operation speed
time kubectl create service clusterip test --tcp=80:80 -n default --dry-run=client
# Should complete in < 2 seconds
```

**Solution 2: Reset Kubernetes** (if restart doesn't work)
- Open Rancher Desktop UI
- Navigate to: Settings → Kubernetes → Reset Kubernetes
- Click "Reset Kubernetes"
- Wait 3-5 minutes for reset to complete
- Verify with `kubectl get componentstatuses`

**Solution 3: Check WSL2 Resources** (if issue persists)

Insufficient resources can cause etcd slowness:
```bash
# Check current memory usage
free -h

# Check if .wslconfig exists and review limits
cat /mnt/c/Users/<username>/.wslconfig
```

If memory is constrained, increase WSL2 resources:
1. Edit `C:\Users\<username>\.wslconfig` (create if missing)
2. Add or update:
   ```ini
   [wsl2]
   memory=8GB
   processors=4
   swap=2GB
   ```
3. Restart WSL: `wsl.exe --shutdown` (from PowerShell)
4. Start Rancher Desktop again

**For detailed solutions:** Load `references/common-issues.md` section "ETCD Unhealthy"

### 4. Resolving Image Issues

Local images showing ImagePullBackOff typically means the image wasn't built or isn't accessible to Kubernetes.

**Diagnosis:**
```bash
# Get detailed pod information
kubectl describe pod <pod-name> -n <namespace>

# Look for the image name and error message
# Example: Failed to pull image "dev-main:latest"
```

**Solution 1: Build with DevSpace** (if project uses DevSpace)
```bash
# DevSpace handles image building and registry setup
devspace build

# Or full deployment
devspace dev
```

**Solution 2: Build with nerdctl** (Rancher Desktop's CLI)
```bash
# Check if image exists
nerdctl images | grep <image-name>

# Build if missing
nerdctl build -t <image-name>:<tag> .

# Verify
nerdctl images | grep <image-name>
```

**Solution 3: Set imagePullPolicy** (for testing)
```yaml
# In pod/deployment spec
spec:
  containers:
  - name: container
    image: imagename:tag
    imagePullPolicy: Never  # Forces use of local images only
```

**For detailed solutions:** Load `references/common-issues.md` section "ImagePullBackOff for Local Images"

### 5. Resolving Performance Issues

If all components are healthy but operations are slow:

**Check resource utilization:**
```bash
kubectl top nodes
free -h
df -h
```

**If high resource usage:**
- Check for resource-intensive pods: `kubectl top pods -A --sort-by=memory`
- Consider scaling down workloads
- Increase WSL2 resource limits (see ETCD issues section)

**If disk I/O is slow:**
- Check if WSL2 is on HDD vs SSD
- Consider moving WSL2 to faster storage
- Reduce log verbosity in applications

**Test API responsiveness:**
```bash
time kubectl get nodes
time kubectl create deployment test --image=nginx --dry-run=client

# Both should complete in < 2 seconds
```

**For detailed solutions:** Load `references/common-issues.md` section "Slow Kubernetes API Operations"

### 6. Resolving Startup Issues

If Rancher Desktop won't start or K3s service fails:

**Check WSL status:**
```bash
wsl.exe -l -v
# Look for: rancher-desktop   Stopped
```

**Solution 1: Restart WSL**
```powershell
# Run from PowerShell
wsl.exe --shutdown
# Wait 10 seconds
# Start Rancher Desktop
```

**Solution 2: Check port conflicts**
```powershell
# Check if port 6443 is in use
netstat -ano | findstr ":6443"

# If in use by another process, stop that process or change K3s port
```

**Solution 3: Verify Hyper-V**
```powershell
# Run in elevated PowerShell
Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V
# Should show: State: Enabled
```

**For detailed solutions:** Load `references/common-issues.md` section "Rancher Desktop Service Not Starting"

## Using Bundled Resources

### Diagnostic Script

Location: `scripts/diagnose-rancher.sh`

Run comprehensive diagnostics:
```bash
bash scripts/diagnose-rancher.sh > rancher-diagnostics.txt
```

The script automates data collection for all major health indicators and creates a report suitable for sharing or analysis.

### Common Issues Reference

Location: `references/common-issues.md`

Load this reference when encountering issues not covered in the main workflow or when detailed solution steps are needed:

```bash
# Example: For deep dive into ETCD issues
# Read: references/common-issues.md section "ETCD Unhealthy"
```

The reference includes:
- Detailed root cause analysis for each issue type
- Step-by-step solutions with command examples
- Useful debugging commands
- WSL2-specific considerations

## Quick Reference Commands

### Health Check
```bash
kubectl get componentstatuses               # Control plane health
kubectl get nodes -o wide                   # Node status
kubectl top nodes                           # Resource usage
```

### Event Investigation
```bash
kubectl get events -A --sort-by='.lastTimestamp' | tail -20
kubectl describe pod <pod-name> -n <namespace>
kubectl logs -n kube-system <pod-name>
```

### WSL Investigation
```bash
wsl.exe -l -v                               # WSL distributions
wsl.exe -d rancher-desktop rc-status        # Service status
wsl.exe -d rancher-desktop ps aux | grep k3s # Process check
```

### Performance Testing
```bash
time kubectl create service clusterip test --tcp=80:80 --dry-run=client
time kubectl get nodes
```

## Troubleshooting Tips

1. **Always start with component health**: `kubectl get componentstatuses` reveals most issues
2. **ETCD problems are most common**: Try restarting Rancher Desktop first
3. **Check recent events**: `kubectl get events` shows what happened recently
4. **Resource constraints manifest slowly**: Check `kubectl top nodes` and `free -h`
5. **WSL2 adds complexity**: Remember commands may need `wsl.exe -d rancher-desktop` prefix
6. **Local images need explicit building**: Kubernetes can't pull from your local Docker/nerdctl without proper setup

## When to Escalate

Consider escalating beyond this skill when:
- All solutions attempted but issue persists
- Windows Hypervisor or WSL2 core functionality is broken
- Rancher Desktop logs show kernel panics or system-level errors
- Issue appears to be a bug in Rancher Desktop itself
- Data corruption suspected in etcd database

For GitHub issues or community support, include output from `scripts/diagnose-rancher.sh`.
