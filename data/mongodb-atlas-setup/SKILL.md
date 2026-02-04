---
name: mongodb-atlas-setup
version: "2.1.0"
description: Master MongoDB Atlas cloud setup, cluster configuration, security, networking, backups, and monitoring. Get production-ready cloud database in minutes. Use when setting up cloud MongoDB, configuring clusters, or managing Atlas.
sasmp_version: "1.3.0"
bonded_agent: 08-mongodb-devops-migration
bond_type: PRIMARY_BOND

# Production-Grade Skill Configuration
capabilities:
  - cluster-provisioning
  - network-configuration
  - user-management
  - backup-configuration
  - monitoring-setup
  - performance-advisor

input_validation:
  required_context:
    - tier_requirement
    - region
  optional_context:
    - cloud_provider
    - vpc_peering
    - backup_schedule

output_format:
  cluster_config: object
  connection_string: string
  security_setup: object
  monitoring_dashboard: string

error_handling:
  common_errors:
    - code: ATLAS001
      condition: "IP not whitelisted"
      recovery: "Add IP address to Network Access in Atlas console"
    - code: ATLAS002
      condition: "Cluster tier insufficient"
      recovery: "Upgrade to M10+ for production features"
    - code: ATLAS003
      condition: "Connection timeout"
      recovery: "Check network access, VPC peering, firewall rules"

prerequisites:
  mongodb_version: "Atlas managed"
  required_knowledge:
    - cloud-basics
    - mongodb-fundamentals
  account_requirements:
    - "MongoDB Atlas account"
    - "Organization and project created"

testing:
  unit_test_template: |
    // Verify Atlas connection
    const client = new MongoClient(atlasUri)
    await client.connect()
    const result = await client.db('admin').command({ ping: 1 })
    expect(result.ok).toBe(1)
---

# MongoDB Atlas Setup & Configuration

Get your MongoDB database in the cloud with enterprise-grade features.

## Quick Start

### Create Free Tier Cluster (5 minutes)

1. **Sign up** at https://www.mongodb.com/cloud/atlas
2. **Create Organization** and Project
3. **Deploy Free Cluster**:
   - Choose cloud provider (AWS, Google Cloud, Azure)
   - Select region closest to your application
   - Accept M0 sandbox tier (512MB, free forever)
4. **Create Database User**:
   - Username: your_username
   - Password: strong password (auto-generated)
5. **Setup Network Access**:
   - Whitelist your IP address
   - Or allow access from anywhere (0.0.0.0/0) for development
6. **Get Connection String**:
   ```
   mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/database_name
   ```
7. **Connect**:
   ```javascript
   const { MongoClient } = require('mongodb');
   const client = new MongoClient(connectionString);
   ```

## Cluster Tiers

### M0 Sandbox (FREE - Perfect for Learning)
- 512MB storage
- Shared infrastructure
- Single region
- No backup
- **Best for:** Learning, development, prototyping

### M2/M5 Shared Tier ($9-57/month)
- 2GB-10GB storage
- Shared infrastructure
- Global clusters available
- Daily backups
- **Best for:** Staging, small production apps

### M10+ Dedicated Tier ($57+/month)
- 10GB+ storage (scalable)
- Dedicated servers
- All MongoDB features
- Point-in-time recovery
- **Best for:** Production systems

## Cluster Configuration

### Region Selection Strategy
```
Global users? → Multi-region cluster
USA only? → us-east-1 or us-west-2
EU users? → eu-west-1
Asia-Pacific? → ap-southeast-1
```

### Network Security
```javascript
// 1. IP Whitelist (RECOMMENDED)
// Add specific IPs that can access cluster
// e.g., your office, AWS security group, CI/CD runner

// 2. Public Internet (NOT RECOMMENDED)
// Allow 0.0.0.0/0 - anyone can try to connect
// Must have strong password!

// 3. VPC Peering (ENTERPRISE)
// Connect via private network
// Most secure option
```

### Connection String Options
```javascript
// Standard: Direct connection
mongodb+srv://user:pass@cluster.mongodb.net/database

// With options
mongodb+srv://user:pass@cluster.mongodb.net/database?retryWrites=true&w=majority

// Connection pooling
mongodb+srv://user:pass@cluster.mongodb.net/database?maxPoolSize=100

// TLS required
mongodb+srv://user:pass@cluster.mongodb.net/database?ssl=true
```

## Database Users & Authentication

### Create Users in Atlas
```
1. Security → Database Access
2. Add Database User
3. Choose authentication method:
   - Password: Username + strong password
   - Certificate: X.509 certificates
   - LDAP: Enterprise directory
4. Assign roles:
   - Atlas admin
   - Project owner
   - Editor
   - Viewer
   - Custom roles
```

### User Roles Explained
- **Project Owner**: Full control of project
- **Editor**: Create/delete databases, manage users
- **Viewer**: Read-only access to project
- **Database User**: Application-level authentication

## Backups & Disaster Recovery

### Atlas Backups
```
Free M0: No automatic backups
M2-M5: Daily snapshots
M10+: Hourly snapshots + point-in-time recovery

Backup retention:
- 2 weeks default (M10+)
- 90 days for M10+
- Longer retention available
```

### Restore Process
```
1. Atlas Console → Backup
2. Select snapshot
3. Restore to new cluster or existing
4. Wait for restore to complete
5. Verify data integrity
```

### Backup Best Practices
1. **Test Restores Regularly** - Verify backups work
2. **Keep Backups in Different Region** - Disaster recovery
3. **Export Important Data** - Separate backup outside Atlas
4. **Monitor Backup Size** - Affects storage costs
5. **Set Retention Policy** - Balance cost vs. recoverability

## Monitoring & Performance

### Atlas Monitoring Dashboard
```
- Connections: Active connections, client info
- Operations: Reads, writes, inserts, updates
- CPU: CPU usage percentage
- Memory: Memory usage
- Storage: Database size growth
- Network: Incoming/outgoing bytes
- Queries: Slow queries
- Locks: Lock contention
```

### Performance Advisor
```
Automatic recommendations:
- Missing indexes on frequently queried fields
- Schema improvements
- Connection pooling suggestions
- Storage optimization

Implement recommendations:
1. Review suggestion
2. Preview impact
3. Apply with one click
4. Monitor results
```

### Alerts Configuration
```
Set alerts for:
- High CPU (> 75%)
- High memory (> 90%)
- Low disk space (< 10% available)
- Slow queries (> 1000ms)
- Replication lag
- Connection issues
- Long-running operations
```

## Advanced Features

### Global Clusters (Enterprise)
```
Multi-region replication:
- Write to any region
- Read from nearest region
- Low-latency access globally
- Automatic failover
```

### VPC Peering
```
Private network connection:
- Connect from AWS VPC
- No internet exposure
- Lowest latency
- Most secure
```

### Encryption at Rest
```
Enabled on M10+ by default:
- AES-256 encryption
- Managed by AWS/GCP/Azure
- Automatic key rotation
- HIPAA/SOC2 compliant
```

### LDAP Integration
```
Enterprise directory authentication:
- Connect to company LDAP/Active Directory
- Centralized user management
- Automatic sync
- Role mapping
```

## Cost Optimization

### Estimate Costs
```
Free: $0/month (M0)
Small App: $9-57/month (M2-M5)
Production: $57-500+/month (M10-M30)

Plus data transfer costs:
- Within AWS region: Free
- Cross-region: $0.02/GB
- Internet egress: $0.03/GB
```

### Reduce Costs
1. **Use Free M0** - During development
2. **Choose Right Region** - Avoid data transfer costs
3. **Monitor Growth** - Scale appropriately
4. **Compress Data** - Reduces storage, network
5. **Archive Old Data** - Keep only active data

## Troubleshooting

### Connection Issues
```
❌ "IP not whitelisted"
✅ Add your IP to whitelist in Security → Network Access

❌ "Authentication failed"
✅ Check username/password, correct database

❌ "Cluster not available"
✅ Wait a few minutes, clusters take time to start

❌ "Connection timeout"
✅ Check firewall, increase timeout, check IP whitelist
```

### Performance Issues
```
❌ Slow queries
✅ Check Performance Advisor, add indexes

❌ High CPU
✅ Review resource usage, optimize queries, upgrade tier

❌ Storage full
✅ Archive data, delete old records, upgrade tier
```

## Best Practices

✅ **Security:**
1. Use strong, random passwords (20+ characters)
2. Restrict IP whitelist to specific IPs
3. Enable encryption (M10+)
4. Use separate users per application
5. Rotate passwords regularly

✅ **Performance:**
1. Monitor metrics regularly
2. Create indexes early
3. Test under production load
4. Use connection pooling
5. Archive old data

✅ **Operations:**
1. Set up alerts
2. Test backup/restore process
3. Monitor costs monthly
4. Document setup procedure
5. Plan capacity growth

## Next Steps

1. **Create MongoDB Atlas Account** - Free tier
2. **Deploy M0 Cluster** - 5 minutes
3. **Load Sample Data** - Understand structure
4. **Create Application User** - Separate from admin
5. **Setup Monitoring** - Alerts configured
6. **Plan Backup Strategy** - Before going production

---

**Ready to power your app with MongoDB in the cloud!** ☁️
