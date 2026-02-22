---
name: k8s-nfs-mount-troubleshooting
description: |
  Debug Kubernetes NFS volume mount failures. Use when: (1) Pod stuck in ContainerCreating 
  for extended time, (2) kubectl describe shows "MountVolume.SetUp failed" with NFS errors,
  (3) Error message shows "Protocol not supported" or "mount.nfs: access denied", 
  (4) NFS volume defined in pod spec but container won't start. Common root cause is 
  missing NFS export on the server, not a protocol issue.
author: Claude Code
version: 1.0.0
date: 2026-01-28
---

# Kubernetes NFS Mount Troubleshooting

## Problem
Pods with NFS volumes get stuck in `ContainerCreating` state indefinitely. The error 
messages from `kubectl describe pod` can be misleading, showing protocol or permission 
errors when the actual issue is the NFS export doesn't exist.

## Context / Trigger Conditions
- Pod status shows `ContainerCreating` for more than 1-2 minutes
- `kubectl describe pod` shows events like:
  - `MountVolume.SetUp failed for volume "data" : mount failed: exit status 32`
  - `mount.nfs: Protocol not supported`
  - `mount.nfs: access denied by server`
- Pod spec includes an NFS volume mount
- Other pods on the same node work fine

## Solution

### Step 1: Identify the NFS path
```bash
kubectl describe pod -n <namespace> <pod-name> | grep -A5 "Volumes:"
```
Look for the NFS server and path (e.g., `10.0.10.15:/mnt/main/myservice`)

### Step 2: Verify the export exists on NFS server
SSH to the NFS server and check:
```bash
ssh root@<nfs-server> "ls -la /mnt/main/myservice"
```

### Step 3: If directory doesn't exist, create it
```bash
ssh root@<nfs-server> "mkdir -p /mnt/main/myservice && chmod 777 /mnt/main/myservice"
```

### Step 4: Add to NFS exports (TrueNAS specific)
For TrueNAS, add the path to the NFS share configuration:
1. Add directory to `scripts/nfs_directories.txt`
2. Run `scripts/nfs_exports.sh` to update the share via API

### Step 5: Restart the pod
```bash
kubectl delete pod -n <namespace> -l app=<app-label>
```
The deployment will create a new pod that should now mount successfully.

## Verification
```bash
kubectl get pods -n <namespace>
# Should show 1/1 Running instead of 0/1 ContainerCreating

kubectl exec -n <namespace> <pod-name> -- ls -la /app/data
# Should show the mounted directory contents
```

## Example
**Symptom:**
```
Events:
  Warning  FailedMount  55s (x13 over 11m)  kubelet  MountVolume.SetUp failed for volume "data" : mount failed: exit status 32
  Mounting command: mount
  Mounting arguments: -t nfs 10.0.10.15:/mnt/main/resume /var/lib/kubelet/pods/.../data
  Output: mount.nfs: Protocol not supported
```

**Root Cause:** The directory `/mnt/main/resume` didn't exist on the TrueNAS server.

**Fix:**
```bash
ssh root@10.0.10.15 'mkdir -p /mnt/main/resume && chmod 777 /mnt/main/resume'
# Then add to NFS exports and restart pod
```

## Notes
- The "Protocol not supported" error is misleading - it often means the export path doesn't exist
- Always check the NFS server first before investigating protocol/firewall issues
- For TrueNAS, the NFS share must be updated via API/UI after creating new directories
- NFSv3 vs NFSv4 issues are rare in modern setups; missing paths are more common
- Check that the NFS client packages are installed on Kubernetes nodes if this is a new cluster

## See Also
- TrueNAS NFS configuration documentation
- Kubernetes NFS volume documentation
