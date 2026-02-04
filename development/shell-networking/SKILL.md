---
name: shell-networking
description: Production-grade shell networking - curl, ssh, ports, debugging
sasmp_version: "1.3.0"
bonded_agent: 05-networking
bond_type: PRIMARY_BOND
version: "2.0.0"
difficulty: intermediate
estimated_time: "6-8 hours"
---

# Shell Networking Skill

> Master networking operations from the command line

## Learning Objectives

After completing this skill, you will be able to:
- [ ] Make HTTP requests with curl
- [ ] Use SSH for remote operations
- [ ] Check ports and connections
- [ ] Debug network issues
- [ ] Transfer files securely

## Prerequisites

- Bash basics
- Basic networking concepts
- Understanding of HTTP

## Core Concepts

### 1. Curl Essentials
```bash
# Basic requests
curl https://api.example.com            # GET
curl -X POST https://api.example.com    # POST
curl -o file.zip https://example.com/f  # Download

# Headers and data
curl -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"key":"value"}' \
     https://api.example.com

# Common options
curl -v url        # Verbose
curl -s url        # Silent
curl -L url        # Follow redirects
curl -k url        # Skip SSL verify
curl -w "%{http_code}" -o /dev/null -s url
```

### 2. SSH Operations
```bash
# Connect
ssh user@host
ssh -p 2222 user@host
ssh -i ~/.ssh/key.pem user@host

# File transfer
scp file.txt user@host:/path/
scp -r dir/ user@host:/path/
scp user@host:/path/file.txt ./

# Tunnels
ssh -L 8080:localhost:80 user@host
ssh -D 1080 user@host     # SOCKS proxy
```

### 3. Port Checking
```bash
# List listening ports
ss -tlnp                  # TCP
ss -ulnp                  # UDP
netstat -tlnp             # Alternative

# Check specific port
nc -zv host 80            # Port check
lsof -i :8080             # What's using port

# Scan ports
nmap -sT host             # TCP scan
nmap -p 80,443 host       # Specific ports
```

### 4. DNS Operations
```bash
# DNS lookup
dig example.com
dig +short example.com    # IP only
dig example.com MX        # MX records
dig @8.8.8.8 example.com  # Specific DNS

# Alternatives
host example.com
nslookup example.com
```

## Common Patterns

### API Request with Error Handling
```bash
response=$(curl -s -w "\n%{http_code}" \
    -H "Authorization: Bearer $TOKEN" \
    "https://api.example.com/data")
http_code=$(echo "$response" | tail -1)
body=$(echo "$response" | sed '$d')

if [[ "$http_code" != "200" ]]; then
    echo "Error: HTTP $http_code"
    exit 1
fi
```

### Wait for Port
```bash
wait_for_port() {
    local host="$1" port="$2" timeout="${3:-30}"
    for ((i=0; i<timeout; i++)); do
        if nc -z "$host" "$port" 2>/dev/null; then
            return 0
        fi
        sleep 1
    done
    return 1
}
```

### SSH Config
```bash
# ~/.ssh/config
Host myserver
    HostName 192.168.1.100
    User admin
    Port 2222
    IdentityFile ~/.ssh/mykey
```

## Anti-Patterns

| Don't | Do | Why |
|-------|-----|-----|
| `curl \| bash` | Download, inspect, run | Security risk |
| Store passwords | Use SSH keys | More secure |
| Skip SSL verify | Fix certificates | Security |

## Practice Exercises

1. **API Client**: Script to interact with REST API
2. **Health Checker**: Check if services are up
3. **SSH Automation**: Run commands on multiple hosts
4. **Port Scanner**: Simple port availability checker

## Troubleshooting

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Connection refused` | Service down | Check if running |
| `Connection timed out` | Firewall/routing | Check network |
| `Name not resolved` | DNS issue | Check DNS |
| `Permission denied (publickey)` | SSH key | Check authorized_keys |

### Debug Techniques
```bash
# Test connectivity
ping -c 2 host
traceroute host

# Debug curl
curl -v https://example.com

# Debug SSH
ssh -vvv user@host
```

## Security Guidelines

1. **Use SSH keys** instead of passwords
2. **Verify SSL certificates** in production
3. **Don't store secrets** in scripts
4. **Use environment variables** for credentials
5. **Audit SSH access** regularly

## Resources

- [curl Manual](https://curl.se/docs/manual.html)
- [SSH Manual](https://man.openbsd.org/ssh)
- [tcpdump Manual](https://www.tcpdump.org/manpages/)
