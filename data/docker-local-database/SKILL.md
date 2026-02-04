---
name: docker-local-database
description: Database operations with docker-local - create, connect, backup, restore for MySQL and PostgreSQL
---

# Docker-Local Database Skill

## Overview

This skill manages database operations in docker-local:
- Create databases
- Connect to database CLIs
- Backup and restore
- Run migrations
- Manage Redis

## Available Database Services

| Service | Version | Port | Use Case |
|---------|---------|------|----------|
| MySQL | 9.1 | 3306 | Traditional relational database |
| PostgreSQL | 17 | 5432 | Advanced features, pgvector for AI |
| Redis | 8 | 6379 | Cache, sessions, queues |

## MANDATORY: Prerequisite Check

**Before ANY docker-local command, verify installation:**

```bash
which docker-local > /dev/null 2>&1
```

**If docker-local is NOT found:**
1. Stop and ask the user if they want to install it
2. If yes, install via: `composer global require mwguerra/docker-local`
3. Add to PATH: `export PATH="$HOME/.composer/vendor/bin:$PATH"`
4. Initialize: `docker-local init`
5. Verify: `which docker-local && docker-local --version`

## Database Commands

### Connect to Database CLIs

```bash
# MySQL CLI
docker-local db:mysql

# PostgreSQL CLI
docker-local db:postgres

# Redis CLI
docker-local db:redis
```

### Create Database

```bash
# Create MySQL database
docker-local db:create myapp

# Creates:
# - myapp (main database)
# - myapp_testing (for tests)
```

### Backup Database

```bash
# Dump current project database
docker-local db:dump

# Dump specific database
docker-local db:dump myapp

# Output goes to: myapp_YYYY-MM-DD_HH-MM-SS.sql
```

**Manual backup commands:**
```bash
# MySQL
docker exec mysql mysqldump -u laravel -psecret myapp > backup.sql

# PostgreSQL
docker exec postgres pg_dump -U laravel myapp > backup.sql
```

### Restore Database

```bash
# Restore from SQL file
docker-local db:restore backup.sql

# Restore to specific database
docker-local db:restore backup.sql myapp
```

**Manual restore commands:**
```bash
# MySQL
docker exec -i mysql mysql -u laravel -psecret myapp < backup.sql

# PostgreSQL
docker exec -i postgres psql -U laravel myapp < backup.sql
```

### Run Migrations

```bash
# Fresh migration with seeds
docker-local db:fresh

# Regular migration
docker-local tinker <<< "Artisan::call('migrate')"

# Or via artisan
docker exec -w /var/www/myapp php php artisan migrate
```

## Default Credentials

### MySQL
```
Host:     mysql (inside Docker) / localhost (from host)
Port:     3306
User:     laravel (or root)
Password: secret
```

### PostgreSQL
```
Host:     postgres (inside Docker) / localhost (from host)
Port:     5432
User:     laravel
Password: secret
```

### Redis
```
Host:     redis (inside Docker) / localhost (from host)
Port:     6379
Password: (none)
```

## Connecting from Host Machine

For GUI tools like TablePlus, DBeaver, or DataGrip:

### MySQL Connection
```
Host:     localhost (or 127.0.0.1)
Port:     3306
User:     laravel (or root)
Password: secret
Database: myapp
```

### PostgreSQL Connection
```
Host:     localhost (or 127.0.0.1)
Port:     5432
User:     laravel
Password: secret
Database: myapp
```

## Connecting from Inside Container

Laravel .env should use Docker service names:

```bash
# MySQL
DB_HOST=mysql
DB_PORT=3306

# PostgreSQL
DB_HOST=postgres
DB_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
```

**Important:** Use service names (mysql, postgres, redis), NOT localhost!

## PostgreSQL with pgvector

PostgreSQL 17 includes pgvector for AI embeddings:

```sql
-- Extension is pre-installed
-- Just use it in your tables:
CREATE TABLE items (
  id SERIAL PRIMARY KEY,
  embedding vector(1536)
);

-- Similarity search
SELECT * FROM items ORDER BY embedding <-> '[...]' LIMIT 10;
```

## Redis Database Allocation

Redis has 16 databases (0-15). Docker-local allocates 3 per project:

| Project | Cache DB | Session DB | Queue DB |
|---------|----------|------------|----------|
| 1st project | 0 | 1 | 2 |
| 2nd project | 3 | 4 | 5 |
| 3rd project | 6 | 7 | 8 |
| 4th project | 9 | 10 | 11 |
| 5th project | 12 | 13 | 14 |

**Check Redis usage:**
```bash
# Connect to Redis
docker-local db:redis

# List all keys in current DB
KEYS *

# Switch databases
SELECT 0
SELECT 3

# Count keys per database
INFO keyspace
```

## Database Troubleshooting

### Cannot Connect to Database

```bash
# Check if container is running
docker-local status

# Check database logs
docker-local logs mysql
docker-local logs postgres

# Test connection
docker exec mysql mysqladmin ping -h localhost -u root -psecret
docker exec postgres pg_isready -U laravel
```

### Permission Denied

```bash
# MySQL - grant privileges
docker exec mysql mysql -u root -psecret -e "GRANT ALL ON myapp.* TO 'laravel'@'%';"

# PostgreSQL - check ownership
docker exec postgres psql -U laravel -c "\l"
```

### Database Not Found

```bash
# List existing databases
# MySQL
docker exec mysql mysql -u root -psecret -e "SHOW DATABASES;"

# PostgreSQL
docker exec postgres psql -U laravel -c "\l"

# Create missing database
docker-local db:create myapp
```

### Reset Database

```bash
# Drop and recreate
# MySQL
docker exec mysql mysql -u root -psecret -e "DROP DATABASE myapp; CREATE DATABASE myapp;"

# PostgreSQL
docker exec postgres psql -U laravel -c "DROP DATABASE myapp; CREATE DATABASE myapp;"

# Then migrate
docker-local db:fresh
```

## Useful SQL Commands

### MySQL
```sql
-- Show databases
SHOW DATABASES;

-- Show tables
USE myapp;
SHOW TABLES;

-- Show table structure
DESCRIBE users;

-- Export specific table
docker exec mysql mysqldump -u laravel -psecret myapp users > users.sql
```

### PostgreSQL
```sql
-- List databases
\l

-- Connect to database
\c myapp

-- List tables
\dt

-- Describe table
\d users

-- Show running queries
SELECT * FROM pg_stat_activity;
```

### Redis
```bash
# List all keys
KEYS *

# Get key type
TYPE mykey

# Get string value
GET mykey

# Get hash
HGETALL myhash

# Clear current database
FLUSHDB

# Clear all databases (careful!)
FLUSHALL

# Monitor commands in real-time
MONITOR
```

$ARGUMENTS
