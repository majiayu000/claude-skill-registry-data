---
name: linux-networking
description: >
  Inspect, test, and diagnose Linux network interfaces, IP routing, DNS
  resolution, open sockets, and firewalls using modern Linux network utilities.
  Use when troubleshooting connectivity issues, checking listening ports with ss,
  diagnosing DNS lookup failures, inspecting packet flows, or testing API endpoints.
compatibility: >
  Agent Skills-compatible coding agents operating in Linux environments
  with iproute2, curl, and network diagnostic tools.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "linux, networking, ip, dns, sockets, curl, firewall"
  topics: "operating-systems, devtools"
---

# Linux Networking and Diagnostics

Systematic Linux networking diagnosis follows the OSI/TCP model layers: from physical/link interface up through IP routing, DNS resolution, transport layer sockets, and application protocol responses. This skill provides modern, non-destructive tools and recipes for diagnosing connectivity problems.

## Core Rules

1. **Diagnose layer by layer**: Link -> IP/Route -> DNS -> Transport (TCP/UDP) -> Application (HTTP/TLS). Never jump to complex application debugging before verifying basic reachability.
2. **Use modern replacements**: Prefer `ip` over deprecated `ifconfig`, `ss` over deprecated `netstat`, and `dig`/`resolvectl` over `nslookup`.
3. **Capture diagnostic evidence**: Always check port binding, interface status, and DNS resolution before concluding that an external service is down.
4. **Distinguish local bind from external reachability**: Listening on `127.0.0.1:8080` means the port is inaccessible from other hosts; listening on `0.0.0.0:8080` binds to all network interfaces.
5. **Never flush firewall rules blindly**: Running `iptables -F` on a remote server with default DROP policies will instantly terminate the SSH session and lock out administrators.

---

## 1. Network Layer Diagnostics

### Layer 1 & 2: Interface and Link State
```bash
# Show all network interfaces and link status (UP/DOWN, MTU, MAC)
ip link show

# Show IP addresses assigned to interfaces
ip -brief address show
```

### Layer 3: Routing and Default Gateway
```bash
# Display IP routing table
ip route show

# Identify which interface and gateway will be used to reach a specific destination
ip route get 8.8.8.8
# Example output: 8.8.8.8 via 192.168.1.1 dev eth0 src 192.168.1.50
```

---

## 2. DNS Resolution Inspection

When domain resolution fails or returns unexpected addresses:

```bash
# Inspect system DNS configuration
cat /etc/resolv.conf

# Check systemd-resolved status (standard on modern Ubuntu/Debian/Fedora)
resolvectl status

# Query DNS record directly using dig (bypassing local caches if directed)
dig +short api.github.com A
dig +nocmd api.github.com ANY +multiline +noall +answer

# Test against a specific DNS resolver (e.g. Cloudflare 1.1.1.1 or Google 8.8.8.8)
dig @1.1.1.1 api.github.com A
```

---

## 3. Sockets and Listening Ports with `ss`

To find out what services are listening and which connections are active:

```bash
# List all listening TCP and UDP sockets with process names and PIDs
# (-t = TCP, -u = UDP, -l = listening, -p = processes, -n = numeric ports)
sudo ss -tulpn

# Check if a specific port (e.g. 5432 PostgreSQL) is listening
ss -tln 'sport = :5432'

# Show active established TCP connections
ss -tne state established
```

Interpretation of socket addresses:
- `127.0.0.1:8000` / `[::1]:8000`: Localhost only. Remote machines cannot connect.
- `0.0.0.0:8000` / `*:8000`: All IPv4 interfaces. Accessible remotely if firewall allows.
- `:::8000`: All IPv6 (and often IPv4 via dual-stack) interfaces.

---

## 4. Application Connectivity and HTTP Testing

### Precision Testing with `curl`
```bash
# Inspect headers, timing, and TLS certificate without downloading body
curl -Iv https://api.example.com/health

# Test specific host header or IP override (useful when testing staging before DNS cutover)
curl -Iv --resolve "api.example.com:443:127.0.0.1" https://api.example.com/health

# Measure connection timing breakdown
curl -w "DNS: %{time_namelookup}s | Connect: %{time_connect}s | TLS: %{time_appconnect}s | TTFB: %{time_starttransfer}s | Total: %{time_total}s\n" \
  -o /dev/null -s https://api.example.com/
```

### Raw TCP Port Testing
```bash
# Test if a remote TCP port is open with netcat (timeout 3 seconds)
nc -zv -w 3 db.internal 5432
```

---

## 5. Packet Inspection with `tcpdump`

For intermittent connection failures, resets, or handshake drops:

```bash
# Capture packets on port 443 on interface eth0 (print headers, limit 20 packets)
sudo tcpdump -i eth0 -n -c 20 port 443

# Capture HTTP/API requests on local loopback interface
sudo tcpdump -i lo -nn -A -s 0 'tcp port 8080 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12:1]>>4)<<2)) != 0)'
```

---

## 6. Common Mistakes and Anti-Patterns

| Anti-Pattern | Risk | Correct Practice |
| :--- | :--- | :--- |
| `ping` as sole connectivity check | ICMP is often blocked by corporate firewalls/cloud security groups while TCP is open | Test the specific TCP port: `nc -zv host port` or `curl -v` |
| Binding service to `127.0.0.1` expecting container reachability | Containerized apps cannot receive traffic from host or other containers | Bind service to `0.0.0.0` inside container |
| Flushing iptables without checking default policy | Instantly drops all network connections including SSH | Check default policies with `iptables -L -n` first |
| Relying on `netstat` on modern systems | May be missing or produce truncated information | Use `ss -tulpn` |

---

## 7. Troubleshooting Workflow

When a service reports `Connection refused` or `Connection timed out`:

```
                       Failure Symptom
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
   "Connection Refused"              "Connection Timed Out"
            │                                 │
  Target host is reachable,         Packet dropped along the path.
  but nothing is listening          No TCP RST or ACK returned.
  on that specific port.                      │
            │                        1. Check routing: `ip route get <dest>`
   1. Check ss -tulpn                2. Check firewall (iptables/nftables/cloud)
   2. Check service status           3. Check MTU issues or dropped ICMP
   3. Check bind address (0.0.0.0)   4. Test path with traceroute/mtr
```

---

## 8. Verification Checklist

- [ ] Network interface is in `UP` state (`ip link`).
- [ ] Valid IP and default route exist (`ip route show`).
- [ ] DNS resolver returns valid A/AAAA records (`dig`).
- [ ] Service is listening on the expected interface and port (`ss -tulpn`).
- [ ] Remote connectivity succeeds via TCP handshake (`curl -v` or `nc -zv`).
