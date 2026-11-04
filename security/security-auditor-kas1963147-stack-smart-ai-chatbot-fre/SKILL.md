---
name: security-auditor
description: WordPress security auditing and hardening. Scan for vulnerabilities, manage security settings, monitor threats, and implement best practices.
tools_required: [security_scan, security_malware, security_firewall, security_login, security_2fa, security_audit, security_headers, security_backup, security_monitor, security_harden]
always_on: false
group: admin
order: 1
suggests: [site-maintenance]
---

# Security Auditor

Comprehensive WordPress security management and auditing.

## When to Use This Skill

- Performing security audits
- Scanning for malware
- Hardening WordPress installation
- Monitoring security threats
- Managing firewall rules
- Reviewing login security
- Implementing two-factor authentication
- Setting security headers

## Core Capabilities

### Scanning
- Vulnerability scanning with `security_scan`
- Malware detection with `security_malware`
- File integrity monitoring
- Database security checks

### Protection
- Firewall management with `security_firewall`
- Login protection with `security_login`
- Two-factor authentication with `security_2fa`
- Brute force prevention
- IP blocking

### Monitoring
- Security event logging with `security_audit`
- Threat monitoring with `security_monitor`
- Failed login tracking
- File change detection

### Hardening
- Security headers with `security_headers`
- WordPress hardening with `security_harden`
- Database prefix changes
- File permissions

## Security Audit Checklist

### Core Security
- [ ] WordPress core up to date
- [ ] All plugins up to date
- [ ] All themes up to date
- [ ] Unused plugins removed
- [ ] Unused themes removed
- [ ] Debug mode disabled
- [ ] File editing disabled

### Login Security
- [ ] Strong admin password
- [ ] Two-factor authentication enabled
- [ ] Login attempt limits set
- [ ] CAPTCHA on login form
- [ ] Default "admin" username changed
- [ ] Failed login lockout configured

### File Security
- [ ] Correct file permissions (644/755)
- [ ] wp-config.php secured
- [ ] .htaccess protected
- [ ] Directory listing disabled
- [ ] PHP execution blocked in uploads

### Database Security
- [ ] Non-default table prefix
- [ ] Database user has limited privileges
- [ ] Regular backups scheduled
- [ ] Backup files stored off-site

### Server Security
- [ ] SSL/HTTPS enabled
- [ ] Security headers configured
- [ ] PHP version current
- [ ] Server software updated
- [ ] Firewall active

## Security Headers

```
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy: [configured per site]
Permissions-Policy: [configured per site]
Strict-Transport-Security: max-age=31536000
```

## Workflow

### Weekly Security Audit

1. **Scan**
   - Run vulnerability scan
   - Check for malware
   - Review recent changes

2. **Review**
   - Check security logs
   - Review failed logins
   - Monitor file changes

3. **Update**
   - Apply security patches
   - Update security rules
   - Refresh firewall lists

4. **Report**
   - Document findings
   - Note action items
   - Track improvements

### Incident Response

1. **Detect** - Identify the breach
2. **Contain** - Limit the damage
3. **Investigate** - Understand the attack
4. **Remediate** - Fix vulnerabilities
5. **Recover** - Restore from backup
6. **Report** - Document and learn

## Best Practices

1. **Keep everything updated** - WordPress, plugins, themes
2. **Use strong passwords** - 12+ characters, mixed
3. **Enable 2FA** - For all admin accounts
4. **Limit login attempts** - 3-5 attempts max
5. **Regular backups** - Daily, stored off-site
6. **Monitor activity** - Review logs regularly
7. **Least privilege** - Only needed permissions

## Critical Metrics

- Security scan score
- Days since last vulnerability
- Failed login attempts (daily)
- Time since last backup
- Number of blocked attacks
- Update compliance rate
