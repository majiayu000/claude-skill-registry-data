---
name: new-homelab-guest
description: Add new homelab guest LXC using standard Terraform pattern for hummel.casa infrastructure
---

# Claude Code Instructions for hummel.casa Terraform Infrastructure

This repository manages Proxmox LXC guests using Terraform for the hummel.casa homelab infrastructure.

## Primary Workflow: Adding New LXC Guests

### Prerequisites (Manual Steps Outside Repository)
1. **Reserve MAC Address**: Get next virtual MAC address from MAC address table in Notion doc (format: 0A:BC:DE:00:00:XX)
2. **Reserve IP Address**: Get next private IP in homelab CIDR range (10.20.71.XXX) from Notion doc
3. **Create DHCP Reservation**: Add MAC/IP pair to Unifi controller
4. **Plan Application**: Select docker image/tag and subdomain (e.g., my-app -> my-app.hummel.casa)
5. **Create Ansible Playbook**: Add playbook to ansible repository at https://gitea.hummel.casa/hummel.casa/ansible

### Repository Structure
- `main.tf`: Core infrastructure with locals.guests definitions and shared resources
- Individual `{guest-name}.tf` files: Each guest has its own file with random_password, proxmox_lxc, and cloudflare_record resources
- `setup-ansible-pull-cron.sh`: Provisioner script that configures new guests

### Steps to Add New Guest

#### 1. Add Guest Definition to main.tf
Add new entry to `locals.guests` in main.tf:
```hcl
guest_name = {
  mac              = "0A:BC:DE:00:00:XX"
  dhcp_reservation = "10.20.71.XXX"
  domain           = "subdomain.hummel.casa"
  target_node      = "pveX"           # Available: pve, pve2, pve4, pve5, pve6, pve7, pve8, pve9
  cpu_cores        = 1                # Typically 1
  ram_mib          = 512              # Common: 256, 512, 1024, 2048, 4096
  root_fs_size     = "8G"             # Common: 5G, 8G, 12G, 16G, 24G, 25G
  playbook         = "playbook.yml"   # Ansible playbook name
}
```

#### 2. Create Individual Guest File
Create `{guest-name}.tf` with three resources:

```hcl
resource "random_password" "guest_name" {
  length           = 30
  special          = true
  override_special = "_%@"
}

resource "proxmox_lxc" "guest_name" {
  target_node  = local.guests.guest_name.target_node
  start        = true
  onboot       = true
  hostname     = local.guests.guest_name.domain
  ostemplate   = local.debian_12_bookwork_lxc_template
  password     = random_password.guest_name.result
  unprivileged = true

  memory = local.guests.guest_name.ram_mib
  cores  = local.guests.guest_name.cpu_cores

  features {
    nesting = true  # Required for Docker
  }

  rootfs {
    storage = "local-lvm"
    size    = local.guests.guest_name.root_fs_size
  }

  ssh_public_keys = <<-EOT
    ${local.public_keys.lxc_guest_ssh}
    ${local.public_keys.atlantis_root_2}
    ${local.public_keys.gitea_hummel_casa}
  EOT

  network {
    name   = "eth0"
    bridge = "vmbr0"
    ip     = "dhcp"
    hwaddr = local.guests.guest_name.mac
  }

  provisioner "file" {
    source      = "setup-ansible-pull-cron.sh"
    destination = "/tmp/script.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/script.sh",
      "/tmp/script.sh ${local.guests.guest_name.playbook}"
    ]
  }

  connection {
    type        = "ssh"
    user        = "root"
    private_key = file("/root/.ssh/id_ed25519")
    host        = local.guests.guest_name.dhcp_reservation
  }

  lifecycle {
    ignore_changes = [ostemplate]
  }
}

resource "cloudflare_record" "guest_name" {
  zone_id = data.cloudflare_zone.hummel_casa.zone_id
  name    = element(split(".", local.guests.guest_name.domain), 0)
  content = local.guests.guest_name.dhcp_reservation
  type    = "A"
  ttl     = 1
  proxied = false
  comment = local.dns_comment
}
```

#### 3. Git Workflow
```bash
git checkout -b add-guest-name-guest
git add main.tf guest-name.tf
git commit -m "add guest-name guest"
git push -u origin add-guest-name-guest
# Create PR via Gitea web interface
```

#### 4. Post-Deployment Monitoring Setup
After the guest is successfully deployed and the application is running:

1. **Access Uptime Kuma**: Navigate to the monitoring dashboard
2. **Add HTTP Monitor**: Create a new monitor for the guest's public endpoint
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: Guest application name (e.g., "Notes App")
   - **URL**: Full application URL (e.g., `https://notes.hummel.casa`)
   - **Heartbeat Interval**: 60 seconds (recommended)
   - **Max Retries**: 1
   - **Timeout**: 48 seconds
3. **Configure Notifications**: Ensure the monitor is connected to appropriate notification channels
4. **Test Monitor**: Verify the monitor can successfully reach the application

This ensures all public services are properly monitored for uptime and availability.

### Current Infrastructure Details

**Domain**: hummel.casa
**Terraform Backend**: PostgreSQL at pg.hummel.casa:5432/terraform_backend
**LXC Template**: debian-12-standard_12.7-1_amd64.tar.zst
**Ansible Repository**: https://gitea.hummel.casa/hummel.casa/ansible
**Provisioner**: setup-ansible-pull-cron.sh (runs every 60 minutes)

### Available Proxmox Nodes
- `pve`: 10.20.71.10
- `pve2`: 10.20.71.20
- `pve4`: 10.20.71.40
- `pve5`: 10.20.71.50
- `pve6`: 10.20.71.60
- `pve7`: 10.20.71.15
- `pve8`: 10.20.71.25
- `pve9`: 10.20.71.35

### SSH Public Keys Included
All guests receive these SSH public keys for access:
- lxc_guest_ssh: General LXC access key
- atlantis_root_2: Atlantis/automation access
- gitea_hummel_casa: Gitea integration key

## Provisioner Script Details

The `setup-ansible-pull-cron.sh` script automatically configures each new LXC guest:

```bash
#!/bin/bash

ANSIBLE_PLAYBOOK=$1

apt-get update
apt-get install ansible -y
apt-get install git -y

cat > /etc/systemd/system/ansible-pull.timer <<EOF
[Unit]
Description=Run ansible-pull every few minutes

[Timer]
OnBootSec=5min
OnUnitActiveSec=60min
Unit=ansible-pull.service

[Install]
WantedBy=timers.target
EOF

cat > /etc/systemd/system/ansible-pull.service <<EOF
[Unit]
Description=ansible-pull

[Service]
ExecStart=/usr/bin/ansible-pull -U https://gitea.hummel.casa/hummel.casa/ansible.git -C main -i localhost, $ANSIBLE_PLAYBOOK
EOF

ansible-galaxy install geerlingguy.docker,7.0.2
ansible-galaxy install git+https://github.com/tphummel/ansible-role-caddy-tls-dns.git,main
ansible-galaxy role install geerlingguy.node_exporter,2.1.0

systemctl daemon-reload
systemctl enable ansible-pull.timer
systemctl start ansible-pull.timer
# run ansible-pull once, adhoc, right now
systemctl start ansible-pull.service

# block until ansible-pull is done
while systemctl is-active --quiet ansible-pull.service;
do
  echo "Waiting for adhoc run of ansible-pull to finish...";
  sleep 2;
done
```

### Script Functions:
1. **System Setup**: Updates packages, installs Ansible and Git
2. **Timer Configuration**: Creates systemd timer running every 60 minutes after initial 5-minute delay
3. **Service Configuration**: Sets up ansible-pull to fetch from gitea.hummel.casa/hummel.casa/ansible
4. **Role Installation**: Installs common Ansible roles (Docker, Caddy, Node Exporter)
5. **Initial Run**: Executes the specified playbook immediately after guest creation

## Example Guest Configurations

### Typical Web Application Guest
```hcl
example_app = {
  mac              = "0A:BC:DE:00:00:XX"
  dhcp_reservation = "10.20.71.XXX"
  domain           = "example-app.hummel.casa"
  target_node      = "pve8"
  cpu_cores        = 1
  ram_mib          = 512
  root_fs_size     = "8G"
  playbook         = "example-app.yml"
}
```

### Resource-Heavy Application Guest
```hcl
heavy_app = {
  mac              = "0A:BC:DE:00:00:XX"
  dhcp_reservation = "10.20.71.XXX"
  domain           = "heavy-app.hummel.casa"
  target_node      = "pve2"
  cpu_cores        = 1
  ram_mib          = 4096
  root_fs_size     = "25G"
  playbook         = "heavy-app.yml"
}
```

## Troubleshooting

### Common Issues
- **Guest won't start**: Check target_node availability and LXC template existence
- **Ansible fails**: Verify playbook exists in ansible repository and syntax is valid
- **DNS not resolving**: Confirm Cloudflare record was created and propagated
- **SSH access issues**: Verify DHCP reservation matches guest IP assignment

### Required Environment Variables
```bash
# Proxmox API access
export PM_API_TOKEN_ID="terraform-prov@pve!mytoken"
export PM_API_TOKEN_SECRET="token"

# Cloudflare DNS management
export CLOUDFLARE_API_TOKEN="token"

# PostgreSQL backend access
export PGUSER="user"
export PGPASSWORD="password"
```

## Best Practices

1. **Resource Allocation**: Start with minimal resources, scale up as needed
2. **Node Distribution**: Spread guests across available Proxmox nodes for load balancing
3. **Naming Convention**: Use descriptive, URL-friendly names for domains
4. **Branch Strategy**: Always create feature branches for new guests
5. **Documentation**: Update ansible playbooks with service-specific configurations
6. **Monitoring**: Always add new public endpoints to Uptime Kuma after deployment for availability monitoring
