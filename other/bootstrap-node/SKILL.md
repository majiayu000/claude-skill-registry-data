---
name: bootstrap-node
description: Prepare or review the repeatable bare-metal-to-managed-node workflow using the Ubuntu autoinstall installer stick, SSH bootstrap, inventory, and Ansible.
---
# Bootstrap node
Record the machine's hardware facts (CPU flags, RAM, disk serial, NICs) before assigning a role. Build its stick with scripts/build-installer-iso.py (installer/README.md): disk-serial guard, key-only SSH, Wi-Fi if needed, `--ssh-port` if a router forward must keep working, optional recovery bundle; write it with scripts/write-installer-usb.sh. Never add the `autoinstall` kernel argument and never bake passwords or private keys into the image. After install: pin the host key under its inventory name, add it to inventory/hosts.yml, then run base, overlay, security and fail2ban before any service role. Do not let the node talk to 10.44.0.x before wg1 is up (the range exists inside the ISP). Verify effective state (sshd -T, vgs free space, overlay guard live), then update PROJECT-CONTEXT §2 and the service catalog.
