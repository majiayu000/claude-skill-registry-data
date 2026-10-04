---
name: vpn
description: Virtual Private Network implementation and configuration
category: networking
difficulty: intermediate
tags: [vpn, security, tunnel, encryption]
author: OpenCode Community
version: 1.0
last_updated: 2024-01-15
---

# VPN (Virtual Private Network)

## What I Do

I am VPN, a technology that creates secure, encrypted connections (tunnels) over public networks to extend private networks securely. I enable remote users to access resources as if connected directly to the private network. I support various protocols including OpenVPN, WireGuard, IPsec, and SSL/TLS-based VPNs. I provide encryption for data in transit, authentication of connecting clients, and IP address translation. I enable site-to-site connectivity between geographically distributed offices. I help organizations maintain security boundaries while supporting remote workforces. Modern VPNs like WireGuard offer improved performance and simpler configurations than traditional solutions.

## When to Use Me

- Remote employee network access
- Site-to-site connectivity
- Securing public WiFi connections
- Bypassing geographic restrictions
- IoT device secure connectivity
- Cloud hybrid networking
- Secure access to sensitive systems
- Regulatory compliance requirements

## Core Concepts

**Tunneling**: Encapsulating packets within other protocols for transport across networks.

**Encryption Protocols**: WireGuard (Noise protocol), OpenVPN (SSL/TLS), IPsec (ESP, AH).

**Authentication Methods**: Pre-shared keys, certificates, multi-factor authentication.

**Routing**: Split tunneling vs full tunneling, routing tables.

**Kill Switch**: Network cut-off when VPN connection drops.

**Protocol Selection**: WireGuard for performance, OpenVPN for compatibility, IPsec for enterprise.

## Code Examples

### Example 1: WireGuard Configuration (Linux)
```bash
#!/bin/bash

# WireGuard VPN Server Setup Script
set -e

# Configuration variables
WG_INTERFACE="wg0"
WG_PORT=51820
WG_NETWORK="10.0.0.0/24"
SERVER_PRIVATE_KEY="REPLACE_WITH_PRIVATE_KEY"
SERVER_PUBLIC_KEY="REPLACE_WITH_PUBLIC_KEY"

# Generate keys
generate_keys() {
    umask 077
    wg genkey | tee privatekey | wg pubkey > publickey
    cat privatekey
    cat publickey
}

# Install WireGuard
install_wireguard() {
    apt update
    apt install -y wireguard wireguard-tools
    
    # Enable IP forwarding
    echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
    echo "net.ipv6.conf.all.forwarding=1" >> /etc/sysctl.conf
    sysctl -p
}

# Configure server
configure_server() {
    cat > /etc/wireguard/${WG_INTERFACE}.conf << EOF
[Interface]
Address = ${WG_NETWORK}
ListenPort = ${WG_PORT}
PrivateKey = ${SERVER_PRIVATE_KEY}
PostUp = iptables -A FORWARD -i %i -j ACCEPT
PostDown = iptables -D FORWARD -i %i -j ACCEPT
PostUp = iptables -t nat -A POSTROUTING -s ${WG_NETWORK} -o eth0 -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -s ${WG_NETWORK} -o eth0 -j MASQUERADE

# Client: alice
[Peer]
# PublicKey = CLIENT_PUBLIC_KEY
# AllowedIPs = 10.0.0.2/32

# Client: bob
[Peer]
# PublicKey = CLIENT_PUBLIC_KEY
# AllowedIPs = 10.0.0.3/32
EOF

    chmod 600 /etc/wireguard/${WG_INTERFACE}.conf
}

# Add client peer
add_peer() {
    local CLIENT_NAME=$1
    local CLIENT_PUBLIC_KEY=$2
    local CLIENT_IP=$3
    
    cat >> /etc/wireguard/${WG_INTERFACE}.conf << EOF

[Peer]
PublicKey = ${CLIENT_PUBLIC_KEY}
AllowedIPs = ${CLIENT_IP}/32
EOF
    
    wg syncconf ${WG_INTERFACE} <(wg-quick strip ${WG_INTERFACE})
    
    echo "Client ${CLIENT_NAME} added with IP ${CLIENT_IP}"
}

# Start and enable service
enable_service() {
    systemctl enable wg-quick@${WG_INTERFACE}
    systemctl start wg-quick@${WG_INTERFACE}
    wg show ${WG_INTERFACE}
}

# Generate client configuration
generate_client_config() {
    local CLIENT_NAME=$1
    local SERVER_PUBLIC_IP=$2
    local CLIENT_PRIVATE_KEY=$3
    
    cat > ~/${CLIENT_NAME}.conf << EOF
[Interface]
PrivateKey = ${CLIENT_PRIVATE_KEY}
Address = ${CLIENT_IP}/32
DNS = 1.1.1.1

[Peer]
PublicKey = ${SERVER_PUBLIC_KEY}
AllowedIPs = 0.0.0.0/0
Endpoint = ${SERVER_PUBLIC_IP}:${WG_PORT}
PersistentKeepalive = 25
EOF

    chmod 600 ~/${CLIENT_NAME}.conf
    echo "Client configuration saved to ~/${CLIENT_NAME}.conf"
}

# Monitor connections
monitor_connections() {
    while true; do
        clear
        echo "=== WireGuard Connection Monitor ==="
        echo "Time: $(date)"
        echo ""
        wg show ${WG_INTERFACE}
        echo ""
        echo "Connected clients:"
        wg show ${WG_INTERFACE} dump | tail -n +2 | awk '{print "  "$1": "$3" ("$4")"}'
        sleep 5
    done
}

# Usage examples
case "${1:-help}" in
    install)
        install_wireguard
        configure_server
        enable_service
        ;;
    add-peer)
        add_peer "$2" "$3" "$4"
        ;;
    client-config)
        generate_client_config "$2" "$3" "$4"
        ;;
    monitor)
        monitor_connections
        ;;
    *)
        echo "Usage: $0 {install|add-peer|client-config|monitor}"
        ;;
esac
```

### Example 2: OpenVPN Server Configuration
```bash
# OpenVPN Server Configuration
# /etc/openvpn/server.conf

# Protocol and port
proto udp
port 1194

# Device and tunneling
dev tun
topology subnet

# Certificate paths
ca ca.crt
cert server.crt
key server.key
dh dh2048.pem
tls-auth ta.key 0

# Network configuration
server 10.8.0.0 255.255.255.0
ifconfig-pool-persist ipp.txt
push "route 192.168.10.0 255.255.255.0"
push "route 192.168.20.0 255.255.255.0"
push "dhcp-option DNS 8.8.8.8"
push "dhcp-option DNS 8.8.4.4"

# Client-to-client communication
client-to-client
duplicate-cn

# Keepalive and compression
keepalive 10 120
compress lz4-v2
push "compress lz4-v2"

# Cryptography
cipher AES-256-GCM
auth SHA256

# Persistence
persist-key
persist-tun

# Status and logging
status openvpn-status.log
log /var/log/openvpn.log
verb 3

# Maximum clients
max-clients 100

# Security enhancements
user nobody
group nogroup

# MTU settings
mtu-test
tun-mtu 1500

# Redirect gateway for full tunneling
;push "redirect-gateway def1 bypass-dhcp"
```

### Example 3: VPN Client Implementation (Python)
```python
import socket
import struct
import threading
import time
from dataclasses import dataclass
from typing import Optional, Dict, List
from enum import Enum

class VPNProtocol(Enum):
    OPENVPN = "openvpn"
    WIREGUARD = "wireguard"
    IPSEC = "ipsec"

@dataclass
class VPNClientConfig:
    protocol: VPNProtocol
    server_address: str
    port: int
    username: str
    password: str
    ca_cert: Optional[str] = None
    client_cert: Optional[str] = None
    client_key: Optional[str] = None
    dns_servers: List[str] = None
    routes: List[str] = None
    split_tunnel: bool = False

class VPNClient:
    def __init__(self, config: VPNClientConfig):
        self.config = config
        self.socket: Optional[socket.socket] = None
        self.tunnel_interface = None
        self.connected = False
        self.reconnecting = False
        self.event_callbacks: Dict[str, List[callable]] = {}
    
    def on(self, event: str, callback: callable):
        if event not in self.event_callbacks:
            self.event_callbacks[event] = []
        self.event_callbacks[event].append(callback)
    
    def _emit(self, event: str, *args):
        for callback in self.event_callbacks.get(event, []):
            try:
                callback(*args)
            except Exception as e:
                print(f"Event callback error: {e}")
    
    def connect(self, timeout: int = 30) -> bool:
        try:
            self._emit('connecting')
            
            if self.config.protocol == VPNProtocol.WIREGUARD:
                return self._connect_wireguard(timeout)
            elif self.config.protocol == VPNProtocol.OPENVPN:
                return self._connect_openvpn(timeout)
            else:
                raise NotImplementedError(f"Protocol {self.config.protocol} not implemented")
                
        except Exception as e:
            self._emit('error', e)
            return False
    
    def _connect_wireguard(self, timeout: int) -> bool:
        import wgconfig.wgconfig as wg
        
        wgconf = wg.WGConfig()
        wgconf.add_interface(
            privatekey=self.config.client_key,
            address="10.0.0.2/32",
            dns=self.config.dns_servers or ["1.1.1.1"]
        )
        
        wgconf.add_peer(
            publickey=self._get_server_public_key(),
            endpoint=f"{self.config.server_address}:{self.config.port}",
            allowedips=self.config.routes or ["0.0.0.0/0"],
            persistentkeepalive=25
        )
        
        wgconf.write('/tmp/wg0.conf')
        
        try:
            wgconf.apply('/tmp/wg0.conf')
            self.connected = True
            self._emit('connected')
            return True
        except Exception as e:
            self._emit('error', e)
            return False
    
    def _connect_openvpn(self, timeout: int) -> bool:
        import subprocess
        import os
        
        # Create OpenVPN configuration file
        config_lines = [
            f"remote {self.config.server_address} {self.config.port}",
            "client",
            "dev tun",
            "proto udp",
            "resolv-retry infinite",
            "nobind",
            "persist-key",
            "persist-tun",
            "remote-cert-tls server",
            f"cipher {self.config.cipher or 'AES-256-GCM'}",
            f"auth {self.config.auth or 'SHA256'}",
        ]
        
        if self.config.ca_cert:
            config_lines.append(f"ca {self.config.ca_cert}")
        if self.config.client_cert:
            config_lines.append(f"cert {self.config.client_cert}")
        if self.config.client_key:
            config_lines.append(f"key {self.config.client_key}")
        
        if self.config.split_tunnel:
            config_lines.append("route-nopull")
            for route in self.config.routes or []:
                config_lines.append(f"route {route}")
        
        with open('/tmp/client.ovpn', 'w') as f:
            f.write('\n'.join(config_lines))
        
        # Start OpenVPN process
        self.openvpn_process = subprocess.Popen(
            ['openvpn', '--config', '/tmp/client.ovpn'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid
        )
        
        # Wait for connection
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self._check_openvpn_connected():
                self.connected = True
                self._emit('connected')
                return True
            time.sleep(1)
        
        self._emit('error', TimeoutError("Connection timeout"))
        return False
    
    def _check_openvpn_connected(self) -> bool:
        try:
            result = subprocess.run(
                ['ip', 'addr', 'show', 'tun0'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0 and 'inet' in result.stdout.decode()
        except:
            return False
    
    def disconnect(self):
        if self.config.protocol == VPNProtocol.WIREGUARD:
            try:
                subprocess.run(['wg-quick', 'down', 'wg0'], capture_output=True)
            except:
                pass
        elif self.config.protocol == VPNProtocol.OPENVPN:
            if hasattr(self, 'openvpn_process'):
                self.openvpn_process.terminate()
                self.openvpn_process.wait()
        
        self.connected = False
        self._emit('disconnected')
    
    def get_status(self) -> Dict:
        return {
            'connected': self.connected,
            'protocol': self.config.protocol.value,
            'server': f"{self.config.server_address}:{self.config.port}",
            'timestamp': time.time()
        }
    
    def _get_server_public_key(self) -> str:
        # Retrieve server public key
        return ""
```

### Example 4: VPN Performance Monitor
```python
import time
import statistics
from typing import Dict, List, Optional
from dataclasses import dataclass
from collections import deque

@dataclass
class VPNMetrics:
    latency_ms: float
    jitter_ms: float
    packets_sent: int
    packets_received: int
    packets_lost: int
    bytes_sent: int
    bytes_received: int
    connection_time: float

class VPNPerformanceMonitor:
    def __init__(self, sample_size: int = 60):
        self.sample_size = sample_size
        self.latency_samples = deque(maxlen=sample_size)
        self.jitter_samples = deque(maxlen=sample_size)
        self.packets_sent = 0
        self.packets_received = 0
        self.packets_lost = 0
        self.bytes_sent = 0
        self.bytes_received = 0
        self.connection_start_time: Optional[float] = None
        self.running = False
        self.monitoring_thread = None
    
    def start(self):
        self.running = True
        self.connection_start_time = time.time()
        self.monitoring_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitoring_thread.start()
    
    def stop(self):
        self.running = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
    
    def _monitor_loop(self):
        while self.running:
            try:
                self._measure_connection()
            except Exception as e:
                print(f"Monitoring error: {e}")
            time.sleep(1)
    
    def _measure_connection(self):
        import subprocess
        
        # Measure latency
        start = time.time()
        try:
            result = subprocess.run(
                ['ping', '-c', '1', '-W', '1', '10.0.0.1'],
                capture_output=True,
                timeout=5
            )
            latency = (time.time() - start) * 1000
            
            if result.returncode == 0:
                self.latency_samples.append(latency)
                self.packets_received += 1
            else:
                self.packets_lost += 1
            
            self.packets_sent += 1
            
        except Exception:
            self.packets_lost += 1
            self.packets_sent += 1
    
    def get_metrics(self) -> VPNMetrics:
        latencies = list(self.latency_samples)
        jitter = 0
        
        if len(latencies) > 1:
            jitter = statistics.stdev(latencies) if len(latencies) > 1 else 0
        
        connection_time = 0
        if self.connection_start_time:
            connection_time = time.time() - self.connection_start_time
        
        return VPNMetrics(
            latency_ms=statistics.mean(latencies) if latencies else 0,
            jitter_ms=jitter,
            packets_sent=self.packets_sent,
            packets_received=self.packets_received,
            packets_lost=self.packets_lost,
            bytes_sent=self.bytes_sent,
            bytes_received=self.bytes_received,
            connection_time=connection_time
        )
    
    def get_statistics(self) -> Dict:
        metrics = self.get_metrics()
        
        loss_rate = 0
        if self.packets_sent > 0:
            loss_rate = (self.packets_lost / self.packets_sent) * 100
        
        return {
            'connection_time_seconds': round(metrics.connection_time, 2),
            'latency': {
                'current_ms': round(metrics.latency_ms, 2),
                'average_ms': round(statistics.mean(self.latency_samples), 2) if self.latency_samples else 0,
                'min_ms': round(min(self.latency_samples), 2) if self.latency_samples else 0,
                'max_ms': round(max(self.latency_samples), 2) if self.latency_samples else 0,
                'stddev_ms': round(statistics.stdev(self.latency_samples), 2) if len(self.latency_samples) > 1 else 0
            },
            'jitter_ms': round(metrics.jitter_ms, 2),
            'packets': {
                'sent': self.packets_sent,
                'received': self.packets_received,
                'lost': self.packets_lost,
                'loss_rate_percent': round(loss_rate, 2)
            },
            'bytes': {
                'sent': self.bytes_sent,
                'received': self.bytes_received
            }
        }
```

## Best Practices

- Use WireGuard for new deployments (better performance, simpler code)
- Implement VPN kill switches to prevent data leaks
- Use strong authentication (certificates + MFA)
- Configure proper routing to avoid DNS leaks
- Use split tunneling to optimize performance
- Monitor VPN connections for anomalies
- Keep VPN software updated for security patches
- Implement proper logging and auditing
- Use hardware security modules for key storage
- Test failover and reconnection logic

## Core Competencies

- VPN protocol implementation (WireGuard, OpenVPN, IPsec)
- Tunnel configuration and management
- Certificate-based authentication
- Routing and network configuration
- VPN security best practices
- Performance monitoring
- Kill switch implementation
- Split tunneling configuration
- DNS leak prevention
- Multi-factor authentication integration
