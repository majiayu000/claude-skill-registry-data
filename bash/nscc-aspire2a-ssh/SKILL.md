---
name: nscc-aspire2a-ssh
description: Configure NSCC Singapore ASPIRE 2A SSH access for NUS users from an NSCC username and private SSH key. Use when a user wants to set up, repair, share, or explain terminal-based SSH/SCP/rsync access to aspire2a.nus.edu.sg, including ~/.ssh key placement, ~/.ssh/config aliases, VPN checks, qsub interactive GPU jobs, and common login troubleshooting.
---

# NSCC ASPIRE 2A SSH

## Workflow

Use the bundled setup script for deterministic local configuration:

```bash
bash scripts/setup_nscc_aspire2a_ssh.sh
```

The script prompts for the NSCC user ID and private key, writes the key to `~/.ssh/nscc_aspire2a`, generates the `.pub` file, and installs a global SSH config block for:

```bash
ssh aspire2a
scp file.py aspire2a:~/CoLLM/
rsync -av ./ aspire2a:~/openonerec/
```

For scripted use:

```bash
bash scripts/setup_nscc_aspire2a_ssh.sh e1538xxx /path/to/private_key
```

## Defaults

- Login node: `aspire2a.nus.edu.sg`
- SSH aliases: `aspire2a` and `nscc`
- SSH key file: `~/.ssh/nscc_aspire2a`
- Config block marker: `# >>> nscc-aspire2a-ssh`
- Off-campus NUS users must connect NUS VPN before SSH.

## Validation

After configuration, check:

```bash
ssh -G aspire2a | grep -E '^(user|hostname|identityfile|identitiesonly) '
route -n get aspire2a.nus.edu.sg
nc -vz -G 5 aspire2a.nus.edu.sg 22
ssh aspire2a
```

On Linux, replace the `nc -G 5` timeout flag with `nc -w 5`.

## HPC Flow

Once logged into the ASPIRE 2A login node:

```bash
qsub -I \
  -P personal-e1538xxx \
  -q normal \
  -l select=1:ngpus=2:ncpus=32:mem=110gb \
  -l walltime=01:00:00
```

Then activate the project environment and monitor jobs:

```bash
source ~/collmenv/bin/activate
cd ~/CoLLM
qstat -u "$USER"
tail -100 stage1_dpo_v2.out
```

## References

Read `references/classmate-quickstart.md` when preparing a message for classmates or explaining the setup in human-friendly terms.
