---
name: linux-filesystems
description: >
  Navigate, inspect, manage, and troubleshoot Linux filesystems (ext4, XFS),
  mount points, inodes, and links. Use when resolving disk space or inode exhaustion,
  distinguishing hardlinks from symlinks, analyzing disk usage with du and df,
  inspecting /etc/fstab and mount options, or understanding the Linux FHS.
compatibility: >
  Agent Skills-compatible coding agents operating on Linux systems with
  standard storage inspection utilities.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "linux, filesystems, ext4, xfs, inodes, mounts, fstab, storage"
  topics: "operating-systems, devtools"
---

# Linux Filesystems and Storage Management

Understanding the Linux Filesystem Hierarchy Standard (FHS), inode architecture, mount behaviors, and journaling filesystems (ext4, XFS) is critical for system administration, storage optimization, and data recovery.

## Core Rules

1. **Files are referenced by inodes, not filenames**: A directory is just an index mapping names to inode numbers. A file is only deleted when all hardlinks are removed AND all open file descriptors are closed.
2. **Never confuse free space (`df -h`) with free inodes (`df -i`)**: A disk can have 500GB free space but fail with "No space left on device" if all inodes are exhausted by millions of zero-byte files.
3. **Use relative symlinks where portability matters**: Absolute symlinks break when directories or containers are mounted at different root paths.
4. **Inspect mounts before unmounting**: Never run `umount -f` (force unmount) on active filesystems without checking open files with `lsof` or `fuser`.
5. **Be cautious with `/etc/fstab` edits**: A syntax error in `/etc/fstab` can prevent a Linux system from booting. Always test with `mount -a` before rebooting.

---

## 1. Storage Inspection Commands

### Disk Space and Inodes
```bash
# Human-readable disk space utilization per mount point
df -hT

# Check inode usage per filesystem
df -i

# Find top 10 largest directories in /var (depth 2)
sudo du -h --max-depth=2 /var 2>/dev/null | sort -hr | head -n 10
```

### Mount Points and Block Devices
```bash
# List block devices with UUIDs, labels, and filesystem types
lsblk -f

# View active mount options for a specific mount point
findmnt /data
```

---

## 2. Inodes, Hardlinks, and Symlinks

### Comparing Link Types
- **Hardlink (`ln target link`)**: Creates an additional directory entry pointing to the **same inode**. Target and link share identical permissions, modification times, and data blocks. Cannot cross filesystem boundaries. Cannot link directories.
- **Symlink (`ln -s target link`)**: A special file whose data is the path string of the target. Can cross filesystems and link directories. If target is deleted, symlink becomes a "dangling" link.

```bash
# Inspect inode number of a file (-i)
ls -li report.txt
# Example: 1048576 -rw-r--r-- 2 user user 4096 Oct 15 10:00 report.txt (2 links)

# Find all hardlinks pointing to a specific inode on /data
find /data -xdev -inum 1048576

# Locate dangling symbolic links
find /var/www -xtype l
```

---

## 3. Filesystem Characteristics: ext4 vs XFS

| Feature | ext4 | XFS |
| :--- | :--- | :--- |
| **Default in** | Debian, Ubuntu | RHEL, Rocky, CentOS, Fedora |
| **Inode Allocation** | Fixed at format time (`mkfs.ext4`) | Dynamic allocation on demand |
| **Shrinking / Resizing**| Can grow and shrink (offline) | Can grow online; **CANNOT shrink** |
| **Performance** | Excellent for small files & general use | Superior scalability for large files & high parallel I/O |
| **Metadata Check** | `fsck.ext4` | `xfs_repair` (cannot run e2fsck on XFS) |

---

## 4. Safe Mounting and `/etc/fstab`

Every entry in `/etc/fstab` contains 6 fields:
`fs_spec  fs_file  fs_vfstype  fs_mntops  fs_freq  fs_passno`

```text
# Best practice: use UUID instead of transient /dev/sdX device names
UUID=4a1b2c3d-e4f5-6789-abcd-ef0123456789  /mnt/data  ext4  defaults,noatime,nodev  0  2
```

- `noatime`: Disables recording file access timestamps, significantly reducing disk write I/O on read-heavy workloads.
- `nodev`: Prevents interpretation of character or block devices on this mount (security best practice for user mounts).

**Safety verification after editing `/etc/fstab`:**
```bash
# Tests all entries in /etc/fstab without rebooting. If errors occur, fix immediately!
sudo mount -a
```

---

## 5. Common Mistakes and Anti-Patterns

| Anti-Pattern | Risk | Correct Practice |
| :--- | :--- | :--- |
| Deleting open files with `rm` to free disk space | Space is not reclaimed until the process closes the file | Identify process with `lsof +L1` and reload/restart it |
| Using `/dev/sdb1` in `/etc/fstab` | Drive letters can change on reboot if hardware order changes | Always use `UUID=...` (`blkid /dev/sdb1`) |
| Creating absolute symlinks inside containers | Broken links when inspected from host or different mount | Use relative symlinks: `ln -s ../lib/app.so link.so` |
| Forcing `fsck` on a mounted filesystem | Severe filesystem corruption | Always unmount filesystem before running `e2fsck` |

---

## 6. Verification Checklist

- [ ] Free disk space verified with `df -h`.
- [ ] Free inode count verified with `df -i`.
- [ ] `/etc/fstab` modifications validated with `mount -a` before reboot.
- [ ] No dangling symbolic links in deployment directories (`find -xtype l`).
- [ ] Mount options include `noatime` on high-throughput data volumes.
