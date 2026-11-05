---
name: windows-vm
description: Operate a Windows guest under libvirt from the Linux host without a human relaying screens — find the VM and its disks, start and stop it safely, take screenshots, type and click, and run PowerShell through the QEMU guest agent. Use when asked to do something "in Windows" or "in the VM", to drive a dual-boot Windows install booted as a VM, or when a libvirt Windows guest needs inspecting or controlling.
---

# windows-vm

Every command here talks to the system libvirt instance. Set it once per shell:

```bash
export LIBVIRT_DEFAULT_URI=qemu:///system
```

## Find the VM

```bash
virsh list --all                          # name and state of every domain
virsh domblklist <dom> --details          # its disks: Type "block" is a physical disk
virsh dumpxml <dom>                       # full definition
virsh qemu-agent-command <dom> '{"execute":"guest-ping"}'   # {"return":{}} = guest agent is up
```

A domain whose disk has Type `block` and points at `/dev/disk/by-id/...`, or at a
`/dev/mapper/...` device built from a real disk's partitions, boots a real disk, often the
same Windows install the machine also boots natively. Treat its disks as
Windows' own: never mount, `dd`, `ntfsfix` or partition them while `virsh domstate <dom>`
says anything other than `shut off`. Two writers on one NTFS volume corrupt it.

## Start and stop

```bash
virsh start <dom>
virt-manager --connect qemu:///system --show-domain-console <dom>   # window for the user
```

A start can be refused by a libvirt `prepare` hook (`virsh start` prints its message):
a Windows partition mounted on the host, a hibernated or unclean volume, another
process holding the disk, or a partition table the guest changed (partition changes belong
in native Windows). Report the message; don't work around the check. A hibernated
or unclean volume clears only after Windows boots natively and shuts down.

To stop, ask Windows to shut down and wait for it:

```bash
virsh shutdown <dom> --mode agent || virsh shutdown <dom> --mode acpi
for _ in $(seq 60); do [ "$(virsh domstate <dom>)" = "shut off" ] && break; sleep 5; done
```

`virsh destroy` is pulling the power cord. Use it only on a guest that is hung (frozen
screenshot, agent not answering) and say that you did.

## See the screen

```bash
virsh screenshot <dom> --file /tmp/<dom>.ppm
nix run nixpkgs#imagemagick -- /tmp/<dom>.ppm /tmp/<dom>.png
```

Then read the PNG. Take one after every action that changes the screen: boot, a click,
a dialog. Compare `md5sum` of successive shots to tell a hung screen from a slow one
without reading every image.

## Keyboard

Keys are Linux keycode names; keys given in one call are pressed together.

```bash
virsh send-key <dom> KEY_ENTER
virsh send-key <dom> KEY_LEFTCTRL KEY_LEFTALT KEY_DELETE     # Ctrl+Alt+Del
virsh send-key <dom> KEY_LEFTMETA KEY_R                      # Win+R
virsh send-key <dom> KEY_LEFTSHIFT KEY_A                     # capital A
```

Text goes one `send-key` per character, so keep it short (a Run box command, a search
term). Anything longer goes through the guest agent. Windows boot and recovery screens
(F8 startup settings, "Press Enter to try again") take keys too.

## Mouse

The VM has a USB tablet, so positions are absolute: 0–32767 on each axis, whatever the
resolution. Scale from the screenshot: `x = px * 32767 / width`.

```bash
virsh qemu-monitor-command <dom> '{"execute":"input-send-event","arguments":{"events":[
  {"type":"abs","data":{"axis":"x","value":16384}},
  {"type":"abs","data":{"axis":"y","value":16384}}]}}'
virsh qemu-monitor-command <dom> '{"execute":"input-send-event","arguments":{"events":[
  {"type":"btn","data":{"down":true,"button":"left"}}]}}'
virsh qemu-monitor-command <dom> '{"execute":"input-send-event","arguments":{"events":[
  {"type":"btn","data":{"down":false,"button":"left"}}]}}'
```

## Run commands (guest agent)

Needs the QEMU guest agent service in Windows (from virtio-win) and a
`org.qemu.guest_agent.0` channel in the domain. Commands run as SYSTEM in session 0: no
desktop, no user profile, no visible windows. Use the screen for anything the user should
see.

`guest-exec` starts the process and returns a pid; `guest-exec-status` reports it, with
output base64-encoded:

```bash
ps1='Get-Volume | Format-Table -AutoSize | Out-String -Width 200'
pid=$(virsh qemu-agent-command <dom> "$(jq -nc --arg c "$ps1" '{execute:"guest-exec",arguments:{
  path:"powershell.exe",arg:["-NoProfile","-NonInteractive","-Command",$c],"capture-output":true}}')" \
  | jq .return.pid)
until st=$(virsh qemu-agent-command <dom> "{\"execute\":\"guest-exec-status\",\"arguments\":{\"pid\":$pid}}") \
  && [ "$(jq .return.exited <<<"$st")" = true ]; do sleep 1; done
jq -r '.return["out-data"] // "" | @base64d' <<<"$st"
jq -r '.return["err-data"] // "" | @base64d' <<<"$st"
jq .return.exitcode <<<"$st"
```

Other agent calls: `guest-get-osinfo`, `guest-get-fsinfo`, `guest-network-get-interfaces`,
`guest-file-open`/`-read`/`-write`/`-close` for files without a shell.

## Without the agent

Before virtio-win is installed there is no agent: drive the screen. Win+R, type
`powershell`, Enter, then type a short command. Install the agent first when the task is
more than a few commands; the virtio-win ISO comes from
`https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso`
(attach it with `virsh change-media` or `virsh attach-disk ... --type cdrom`), and its
`virtio-win-guest-tools.exe` installs the drivers, the guest agent and the SPICE agent
in one go.
