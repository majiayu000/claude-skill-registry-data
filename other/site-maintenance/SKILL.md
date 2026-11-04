---
name: site-maintenance
description: WordPress site maintenance and health monitoring. Manage updates, scheduled tasks, performance optimization, and system health checks.
tools_required: [wp_plugins, wp_themes, wp_cron, wp_transients, wp_site_health, wp_rewrite, wp_options]
always_on: false
group: admin
order: 2
suggests: [security-auditor]
---

# Site Maintenance

Comprehensive WordPress site maintenance and health management.

## When to Use This Skill

- Managing plugin updates
- Updating themes
- Monitoring site health
- Managing scheduled tasks
- Clearing cache and transients
- Optimizing performance
- Fixing rewrite/permalink issues

## Core Capabilities

### Updates
- Plugin updates with `wp_plugins`
- Theme updates with `wp_themes`
- Compatibility checking
- Update scheduling

### Health Monitoring
- Site health checks with `wp_site_health`
- Performance monitoring
- Security status
- Configuration issues

### Optimization
- Transient cache management with `wp_transients`
- Scheduled task optimization with `wp_cron`
- URL rewrite management with `wp_rewrite`
- Database optimization

## Maintenance Checklist

### Weekly Tasks
- [ ] Check for plugin updates
- [ ] Check for theme updates
- [ ] Review site health status
- [ ] Check error logs
- [ ] Clear expired transients

### Monthly Tasks
- [ ] Full plugin compatibility check
- [ ] Database optimization
- [ ] Review scheduled tasks
- [ ] Performance audit
- [ ] Backup verification

### Quarterly Tasks
- [ ] Unused plugin removal
- [ ] Unused theme removal
- [ ] Full security audit
- [ ] SEO audit
- [ ] Performance optimization

## Workflow

### Update Process

1. **Assessment**
   - List available updates with `wp_plugins`
   - Check compatibility notes
   - Review changelog

2. **Backup**
   - Ensure recent backup exists
   - Verify backup integrity
   - Document current state

3. **Update**
   - Update one at a time (major)
   - Update in batches (minor)
   - Test after each update

4. **Verify**
   - Run site health check
   - Test critical functionality
   - Check error logs

### Performance Optimization

1. **Transient Cleanup**
   - Clear expired transients
   - Review transient size
   - Identify problematic transients

2. **Cron Optimization**
   - Review scheduled tasks
   - Remove orphaned tasks
   - Optimize task frequency

3. **Rewrite Refresh**
   - Flush rewrite rules
   - Verify permalink structure
   - Test redirects

## Site Health Checks

### Critical Issues
- Debug mode enabled on production
- Security vulnerabilities detected
- PHP version outdated
- WordPress core outdated
- SSL not configured

### Recommended Improvements
- Persistent object cache not detected
- Background updates disabled
- File editing enabled
- Debug logging enabled
- Weak passwords in use

### Performance Items
- Slow database queries
- Large autoload options
- Excessive transients
- Unoptimized images

## Best Practices

1. **Never update production without backup**
2. **Update during low-traffic periods**
3. **Test on staging first (if available)**
4. **One major update at a time**
5. **Document all changes**
6. **Monitor after updates**
7. **Keep update history**

## Troubleshooting

### After Failed Update
1. Deactivate problematic plugin/theme
2. Check error logs
3. Restore from backup if needed
4. Report issue to developer
5. Find alternative if critical

### Broken Permalinks
1. Flush rewrite rules with `wp_rewrite`
2. Check .htaccess permissions
3. Verify permalink settings
4. Check for conflicting rules

### Slow Performance
1. Clear transients
2. Review cron tasks
3. Check database size
4. Review active plugins
5. Check external API calls
