---
name: dns
description: DNS protocol and domain name resolution
category: networking
difficulty: intermediate
tags: [dns, domain, resolution, nameserver]
author: OpenCode Community
version: 1.0
last_updated: 2024-01-15
---

# DNS (Domain Name System)

## What I Do

I am DNS, the hierarchical naming system translating human-readable domain names into machine-readable IP addresses. I provide distributed, scalable hostname resolution through a global network of authoritative name servers, recursive resolvers, and caching servers. I support multiple record types (A, AAAA, CNAME, MX, TXT, NS, SRV) for various purposes. I implement caching at multiple levels to improve performance and reduce load. I support DNSSEC for authenticated responses, DNS-over-HTTPS for encrypted queries, and dynamic updates for real-time record management. I form the foundation of internet addressing, enabling users to access services using memorable names rather than numeric IP addresses.

## When to Use Me

- Implementing custom DNS resolution
- Configuring DNS records for services
- Building DNS-based service discovery
- DNS troubleshooting and diagnostics
- High-availability DNS infrastructure
- DNS-based load balancing (GeoDNS, latency-based)
- Domain registration and management
- DNSSEC implementation
- Private DNS zones

## Core Concepts

**Record Types**: A (IPv4), AAAA (IPv6), CNAME (alias), MX (mail), TXT (text), NS (nameserver), SRV (service), SOA (authority).

**DNS Hierarchy**: Root servers → TLD servers → Authoritative servers → Recursive resolvers.

**Caching**: TTL (Time to Live) controlling how long records are cached.

**Zones**: Portions of the DNS namespace managed by authoritative servers.

**DNSSEC**: DNS Security Extensions providing authentication for DNS responses.

**Anycast**: Multiple servers sharing the same IP for geographic distribution.

**Round-Robin**: Multiple IP addresses rotated for load distribution.

## Code Examples

### Example 1: DNS Client with Cache (Python)
```python
import socket
import struct
import time
import threading
from typing import Optional, Dict, List
from dataclasses import dataclass, field
from enum import Enum

class DNSRecordType(Enum):
    A = 1
    AAAA = 28
    CNAME = 5
    MX = 15
    NS = 2
    TXT = 16
    SOA = 6
    SRV = 33

@dataclass
class DNSRecord:
    name: str
    rtype: DNSRecordType
    rdata: str
    ttl: int
    timestamp: float = field(default_factory=time.time)

class DNSCache:
    def __init__(self, max_size: int = 1000, default_ttl: int = 300):
        self.cache: Dict[str, List[DNSRecord]] = {}
        self.lock = threading.RLock()
        self.max_size = max_size
        self.default_ttl = default_ttl
    
    def get(self, name: str, rtype: DNSRecordType) -> Optional[List[DNSRecord]]:
        with self.lock:
            key = f"{name}:{rtype.name}"
            if key not in self.cache:
                return None
            
            records = self.cache[key]
            now = time.time()
            valid = [r for r in records if r.ttl == 0 or (now - r.timestamp) < r.ttl]
            
            if not valid:
                del self.cache[key]
                return None
            
            if len(valid) < len(records):
                self.cache[key] = valid
            
            return valid
    
    def set(self, name: str, rtype: DNSRecordType, records: List[DNSRecord]):
        with self.lock:
            key = f"{name}:{rtype.name}"
            
            if len(self.cache) >= self.max_size:
                self.evict_oldest()
            
            self.cache[key] = records
    
    def evict_oldest(self):
        if not self.cache:
            return
        
        oldest_key = min(self.cache.keys(), 
                        key=lambda k: min(r.timestamp for r in self.cache[k]))
        del self.cache[oldest_key]
    
    def clear(self):
        with self.lock:
            self.cache.clear()
    
    def get_stats(self) -> Dict:
        with self.lock:
            return {
                'entries': len(self.cache),
                'records': sum(len(v) for v in self.cache.values())
            }


class DNSClient:
    DNS_SERVER = '8.8.8.8'
    DNS_PORT = 53
    TIMEOUT = 5.0
    
    def __init__(self, server: str = None, cache: DNSCache = None):
        self.server = server or self.DNS_SERVER
        self.cache = cache or DNSCache()
        self.socket = None
    
    def _create_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(self.TIMEOUT)
        return sock
    
    def resolve(self, name: str, rtype: DNSRecordType = DNSRecordType.A, 
                use_cache: bool = True) -> List[DNSRecord]:
        if use_cache:
            cached = self.cache.get(name, rtype)
            if cached:
                return cached
        
        records = self._query(name, rtype)
        
        if use_cache and records:
            self.cache.set(name, rtype, records)
        
        return records
    
    def _query(self, name: str, rtype: DNSRecordType) -> List[DNSRecord]]:
        sock = self._create_socket()
        
        try:
            # Build DNS query
            transaction_id = struct.pack("!H", 0x1234)
            flags = struct.pack("!H", 0x0100)  # Standard query, RD=1
            qdcount = struct.pack("!H", 1)
            ancount = struct.pack("!H", 0)
            nscount = struct.pack("!H", 0)
            arcount = struct.pack("!H", 0)
            
            # Encode domain name
            qname = b''
            for label in name.split('.'):
                qname += struct.pack("!B", len(label)) + label.encode()
            qname += b'\x00'
            
            # Question type and class
            qtype = struct.pack("!H", rtype.value)
            qclass = struct.pack("!H", 1)  # IN class
            
            query = transaction_id + flags + qdcount nscount + + ancount + arcount + qname + qtype + qclass
            
            sock.sendto(query, (self.server, self.DNS_PORT))
            response = sock.recv(512)
        
        finally:
            sock.close()
        
        return self._parse_response(response, name)
    
    def _parse_response(self, response: bytes, original_name: str) -> List[DNSRecord]:
        records = []
        
        transaction_id = struct.unpack("!H", response[0:2])[0]
        flags = struct.unpack("!H", response[2:4])[0]
        qdcount = struct.unpack("!H", response[4:6])[0]
        ancount = struct.unpack("!H", response[6:8])[0]
        
        offset = 12
        
        # Skip question section
        for _ in range(qdcount):
            while response[offset] != 0:
                offset += 1 + response[offset]
            offset += 5
        
        # Parse answer records
        for _ in range(ancount):
            name, offset = self._parse_name(response, offset)
            rtype = DNSRecordType(struct.unpack("!H", response[offset:offset+2])[0])
            offset += 2
            rclass = struct.unpack("!H", response[offset:offset+2])[0]
            offset += 2
            ttl = struct.unpack("!I", response[offset:offset+4])[0]
            offset += 4
            rdlength = struct.unpack("!H", response[offset:offset+2])[0]
            offset += 2
            rdata = response[offset:offset+rdlength]
            offset += rdlength
            
            parsed_rdata = self._parse_rdata(rdata, rtype, original_name)
            
            records.append(DNSRecord(
                name=name,
                rtype=rtype,
                rdata=parsed_rdata,
                ttl=ttl
            ))
        
        return records
    
    def _parse_name(self, response: bytes, offset: int) -> (str, int):
        name = []
        original_offset = offset
        
        while True:
            length = response[offset]
            
            if length == 0:
                offset += 1
                break
            
            if (length & 0xC0) == 0xC0:
                # Compression pointer
                pointer = struct.unpack("!H", response[offset:offset+2])[0] & 0x3FFF
                pointed_name, _ = self._parse_name(response, pointer)
                name.append(pointed_name)
                offset += 2
                break
            else:
                offset += 1
                name.append(response[offset:offset+length].decode())
                offset += length
        
        return '.'.join(name), offset
    
    def _parse_rdata(self, rdata: bytes, rtype: DNSRecordType, original_name: str) -> str:
        if rtype == DNSRecordType.A:
            return '.'.join(str(b) for b in rdata)
        elif rtype == DNSRecordType.AAAA:
            return ':'.join(f'{b:02x}{b+1:02x}' for b in rdata[::2])
        elif rtype == DNSRecordType.CNAME:
            name, _ = self._parse_name(rdata, 0)
            return name
        elif rtype == DNSRecordType.MX:
            preference = struct.unpack("!H", rdata[0:2])[0]
            name, _ = self._parse_name(rdata, 2)
            return f"{preference} {name}"
        elif rtype == DNSRecordType.TXT:
            length = rdata[0]
            return rdata[1:1+length].decode('utf-8')
        else:
            return rdata.hex()
    
    def resolve_a(self, name: str, use_cache: bool = True) -> List[str]:
        records = self.resolve(name, DNSRecordType.A, use_cache)
        return [r.rdata for r in records]
    
    def resolve_aaaa(self, name: str, use_cache: bool = True) -> List[str]:
        records = self.resolve(name, DNSRecordType.AAAA, use_cache)
        return [r.rdata for r in records]
    
    def resolve_mx(self, name: str, use_cache: bool = True) -> List[tuple]:
        records = self.resolve(name, DNSRecordType.MX, use_cache)
        return [(int(r.rdata.split()[0]), r.rdata.split()[1]) for r in records]
    
    def resolve_txt(self, name: str, use_cache: bool = True) -> List[str]:
        records = self.resolve(name, DNSRecordType.TXT, use_cache)
        return [r.rdata for r in records]


if __name__ == "__main__":
    client = DNSClient()
    
    # Resolve various record types
    print("Resolving A records for google.com:")
    a_records = client.resolve_a("google.com")
    for ip in a_records:
        print(f"  {ip}")
    
    print("\nResolving MX records for example.com:")
    mx_records = client.resolve_mx("example.com")
    for pref, server in mx_records:
        print(f"  Priority {pref}: {server}")
    
    print("\nCache statistics:")
    print(client.cache.get_stats())
```

### Example 2: DNS Server with Zone Files (Go)
```go
package main

import (
    "bufio"
    "bytes"
    "encoding/json"
    "fmt"
    "log"
    "net"
    "os"
    "strings"
    "sync"
    "time"
)

type DNSRecord struct {
    Name    string
    Type    string
    RData   string
    TTL     int
}

type Zone struct {
    Origin   string
    Records  []DNSRecord
    SOA      DNSRecord
    mutex    sync.RWMutex
}

type DNSServer struct {
    zones       map[string]*Zone
    cache       map[string][]DNSRecord
    cacheMutex  sync.RWMutex
    udpSocket   *net.UDPConn
    tcpListener *net.TCPListener
}

const (
    TYPE_A     = 1
    TYPE_NS    = 2
    TYPE_CNAME = 5
    TYPE_SOA   = 6
    TYPE_PTR   = 12
    TYPE_MX    = 15
    TYPE_TXT   = 16
    TYPE_AAAA  = 28
    TYPE_SRV   = 33
)

func NewDNSServer() *DNSServer {
    return &DNSServer{
        zones:  make(map[string]*Zone),
        cache:  make(map[string][]DNSRecord),
    }
}

func (s *DNSServer) LoadZoneFile(filename string, origin string) error {
    file, err := os.Open(filename)
    if err != nil {
        return fmt.Errorf("failed to open zone file: %w", err)
    }
    defer file.Close()
    
    zone := &Zone{
        Origin:  origin,
        Records: make([]DNSRecord, 0),
    }
    
    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        line := strings.TrimSpace(scanner.Text())
        if line == "" || strings.HasPrefix(line, ";") {
            continue
        }
        
        parts := strings.Fields(line)
        if len(parts) < 5 {
            continue
        }
        
        record := DNSRecord{
            Name: parts[0],
            Type: strings.ToUpper(parts[2]),
            RData: strings.Join(parts[4:], " "),
            TTL:  3600,
        }
        
        if parts[1] != "IN" {
            continue
        }
        
        zone.Records = append(zone.Records, record)
    }
    
    s.zones[origin] = zone
    return nil
}

func (s *DNSServer) StartUDP(address string) error {
    addr, err := net.ResolveUDPAddr("udp", address)
    if err != nil {
        return fmt.Errorf("failed to resolve address: %w", err)
    }
    
    s.udpSocket, err = net.ListenUDP("udp", addr)
    if err != nil {
        return fmt.Errorf("failed to listen: %w", err)
    }
    
    go s.handleUDP()
    
    return nil
}

func (s *DNSServer) StartTCP(address string) error {
    addr, err := net.ResolveTCPAddr("tcp", address)
    if err != nil {
        return fmt.Errorf("failed to resolve address: %w", err)
    }
    
    s.tcpListener, err = net.ListenTCP("tcp", addr)
    if err != nil {
        return fmt.Errorf("failed to listen: %w", err)
    }
    
    go s.handleTCP()
    
    return nil
}

func (s *DNSServer) handleUDP() {
    buffer := make([]byte, 512)
    
    for {
        n, clientAddr, err := s.udpSocket.ReadFromUDP(buffer)
        if err != nil {
            continue
        }
        
        response := s.processQuery(buffer[:n])
        s.udpSocket.WriteToUDP(response, clientAddr)
    }
}

func (s *DNSServer) handleTCP() {
    for {
        conn, err := s.tcpListener.AcceptTCP()
        if err != nil {
            continue
        }
        
        go func(conn *net.TCPConn) {
            defer conn.Close()
            
            lengthBuf := make([]byte, 2)
            if _, err := conn.Read(lengthBuf); err != nil {
                return
            }
            
            length := int(uint16(lengthBuf[0])<<8 | uint16(lengthBuf[1]))
            request := make([]byte, length)
            
            if _, err := conn.Read(request); err != nil {
                return
            }
            
            response := s.processQuery(request)
            
            responseLength := make([]byte, 2)
            responseLength[0] = byte(len(response) >> 8)
            responseLength[1] = byte(len(response))
            
            conn.Write(responseLength)
            conn.Write(response)
        }(conn)
    }
}

func (s *DNSServer) processQuery(query []byte) []byte {
    // Parse DNS header
    if len(query) < 12 {
        return s.createErrorResponse(0, 1) // Format error
    }
    
    transactionID := query[0:2]
    flags := query[2:4]
    qdcount := int(uint16(query[4])<<8 | uint16(query[5]))
    
    // For simplicity, handle single question
    offset := 12
    
    // Parse question name
    var name string
    for {
        length := int(query[offset])
        if length == 0 {
            offset++
            break
        }
        if (length & 0xC0) == 0xC0 {
            offset += 2
            break
        }
        if name != "" {
            name += "."
        }
        name += string(query[offset+1:offset+1+length])
        offset += 1 + length
    }
    
    qtype := uint16(query[offset])<<8 | uint16(query[offset+1])
    qclass := uint16(query[offset+2])<<8 | uint16(query[offset+3])
    offset += 4
    
    // Build response
    var response bytes.Buffer
    
    response.Write(transactionID)
    flags[1] &= 0x7F // Clear QR bit for response
    response.Write(flags)
    
    qdcountBytes := []byte{byte(qdcount >> 8), byte(qdcount & 0xFF)}
    response.Write(qdcountBytes)
    response.Write([]byte{0x00, 0x00}) // ANCOUNT
    response.Write([]byte{0x00, 0x00})  // NSCOUNT
    response.Write([]byte{0x00, 0x00}) // ARCOUNT
    
    // Write question section
    response.Write(query[12:offset])
    
    // Find and add answer records
    answers := s.lookupRecords(name, qtype)
    
    for _, answer := range answers {
        answerBytes := s.encodeRecord(answer, name, offset)
        response.Write(answerBytes)
        
        ancountBytes := []byte{
            byte(len(answers) >> 8),
            byte(len(answers) & 0xFF)
        }
        copy(response[6:8], ancountBytes)
    }
    
    return response.Bytes()
}

func (s *DNSServer) lookupRecords(name string, qtype uint16) []DNSRecord {
    name = strings.ToLower(name)
    
    if zone, ok := s.zones[name]; ok {
        zone.mutex.RLock()
        defer zone.mutex.RUnlock()
        
        var answers []DNSRecord
        for _, record := range zone.Records {
            if record.Name == name || record.Name == "@" {
                typeNum := s.typeStringToNumber(record.Type)
                if typeNum == qtype || qtype == TYPE_ANY {
                    answers = append(answers, record)
                }
            }
        }
        return answers
    }
    
    return nil
}

func (s *DNSServer) encodeRecord(record DNSRecord, name string, offset int) []byte {
    var encoded bytes.Buffer
    
    // Compressed name pointer
    encoded.WriteByte(0xC0)
    encoded.WriteByte(byte(offset))
    
    typeBytes := s.typeStringToBytes(record.Type)
    encoded.Write(typeBytes)
    
    encoded.Write([]byte{0x00, 0x01}) // Class IN
    ttlBytes := []byte{byte(record.TTL >> 24), byte(record.TTL >> 16),
                       byte(record.TTL >> 8), byte(record.TTL & 0xFF)}
    encoded.Write(ttlBytes)
    
    rdata := s.encodeRData(record.RData, record.Type)
    length := []byte{byte(len(rdata) >> 8), byte(len(rdata) & 0xFF)}
    encoded.Write(length)
    encoded.Write(rdata)
    
    return encoded.Bytes()
}

func (s *DNSServer) encodeRData(rdata string, rtype string) []byte {
    if rtype == "A" {
        parts := strings.Split(rdata, ".")
        var result []byte
        for _, part := range parts {
            result = append(result, byte(strings.ToInt(part)))
        }
        return result
    }
    return []byte(rdata)
}

func (s *DNSServer) typeStringToNumber(typeStr string) uint16 {
    switch strings.ToUpper(typeStr) {
    case "A": return TYPE_A
    case "NS": return TYPE_NS
    case "CNAME": return TYPE_CNAME
    case "SOA": return TYPE_SOA
    case "PTR": return TYPE_PTR
    case "MX": return TYPE_MX
    case "TXT": return TYPE_TXT
    case "AAAA": return TYPE_AAAA
    case "SRV": return TYPE_SRV
    default: return 0
    }
}

func (s *DNSServer) typeStringToBytes(typeStr string) []byte {
    t := s.typeStringToNumber(typeStr)
    return []byte{byte(t >> 8), byte(t & 0xFF)}
}

func (s *DNSServer) createErrorResponse(id []byte, errorCode uint16) []byte {
    response := make([]byte, 12)
    copy(response[0:2], id)
    response[2] = 0x80 | byte(errorCode>>4)
    response[3] = 0x00
    return response
}
```

### Example 3: Service Discovery with DNS SRV Records
```typescript
interface SRVRecord {
    priority: number;
    weight: number;
    port: number;
    target: string;
}

class DNSServiceDiscovery {
    private client: DNSClient;
    
    constructor() {
        this.client = new DNSClient();
    }
    
    async discoverService(
        service: string,
        protocol: string = 'tcp',
        domain: string = 'local'
    ): Promise<SRVRecord[]> {
        const queryName = `_${service}._${protocol}.${domain}`;
        
        const records = await this.client.resolve(queryName, DNSRecordType.SRV);
        
        return records.map(record => {
            const parts = record.rdata.split(' ');
            return {
                priority: parseInt(parts[0]),
                weight: parseInt(parts[1]),
                port: parseInt(parts[2]),
                target: parts[3]
            };
        }).sort((a, b) => {
            if (a.priority !== b.priority) {
                return a.priority - b.priority;
            }
            return a.weight - b.weight;
        });
    }
    
    async resolveServiceInstance(srv: SRVRecord): Promise<string[]> {
        return await this.client.resolve_a(srv.target);
    }
    
    async findHealthyService(
        service: string,
        protocol: string = 'tcp',
        domain: string = 'local'
    ): Promise<{ host: string; port: number } | null> {
        const srvRecords = await this.discoverService(service, protocol, domain);
        
        if (srvRecords.length === 0) {
            return null;
        }
        
        // Simple load balancing based on weight
        const totalWeight = srvRecords.reduce((sum, r) => sum + r.weight, 0);
        let random = Math.random() * totalWeight;
        
        let selected: SRVRecord | null = null;
        for (const record of srvRecords) {
            random -= record.weight;
            if (random <= 0) {
                selected = record;
                break;
            }
        }
        
        if (!selected) {
            selected = srvRecords[0];
        }
        
        const addresses = await this.resolveServiceInstance(selected);
        if (addresses.length === 0) {
            return null;
        }
        
        return {
            host: addresses[0],
            port: selected.port
        };
    }
}
```

### Example 4: Dynamic DNS Update Client
```python
import hashlib
import hmac
import base64
import requests
from typing import Optional

class DynamicDNSClient:
    def __init__(
        self,
        provider_url: str,
        hostname: str,
        api_key: str,
        secret: Optional[str] = None
    ):
        self.provider_url = provider_url
        self.hostname = hostname
        self.api_key = api_key
        self.secret = secret
    
    def get_current_ip(self) -> str:
        """Get current public IP address."""
        try:
            response = requests.get('https://api.ipify.org?format=json', timeout=10)
            return response.json()['ip']
        except Exception:
            raise RuntimeError("Failed to get current IP address")
    
    def create_auth_header(self, timestamp: str) -> str:
        """Create authentication header for TSIG-style authentication."""
        if not self.secret:
            return f"DDNS {self.api_key}"
        
        message = f"{self.hostname}:{timestamp}"
        signature = hmac.new(
            self.secret.encode(),
            message.encode(),
            hashlib.sha256
        ).digest()
        
        return f"DDNS {self.api_key}:{base64.b64encode(signature).decode()}"
    
    def update(
        self,
        ip_address: Optional[str] = None,
        record_type: str = 'A',
        ttl: int = 600
    ) -> dict:
        """Update DNS record with current IP address."""
        if ip_address is None:
            ip_address = self.get_current_ip()
        
        timestamp = str(int(time.time()))
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': self.create_auth_header(timestamp)
        }
        
        payload = {
            'hostname': self.hostname,
            'ip': ip_address,
            'type': record_type,
            'ttl': ttl,
            'timestamp': timestamp
        }
        
        try:
            response = requests.post(
                self.provider_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"DNS update failed: {e}")
    
    def delete(self) -> dict:
        """Delete DNS record."""
        timestamp = str(int(time.time()))
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': self.create_auth_header(timestamp)
        }
        
        payload = {
            'hostname': self.hostname,
            'timestamp': timestamp
        }
        
        try:
            response = requests.delete(
                self.provider_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"DNS delete failed: {e}")


class DDNSUpdater:
    def __init__(self, client: DynamicDNSClient, check_interval: int = 300):
        self.client = client
        self.check_interval = check_interval
        self.last_ip: Optional[str] = None
        self.running = False
        self.thread: Optional[threading.Thread] = None
    
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
    
    def _run(self):
        while self.running:
            try:
                current_ip = self.client.get_current_ip()
                
                if current_ip != self.last_ip:
                    print(f"IP changed: {self.last_ip} -> {current_ip}")
                    result = self.client.update(current_ip)
                    print(f"DNS update result: {result}")
                    self.last_ip = current_ip
                else:
                    print(f"IP unchanged: {current_ip}")
                    
            except Exception as e:
                print(f"Error: {e}")
            
            for _ in range(self.check_interval):
                if not self.running:
                    return
                time.sleep(1)
```

## Best Practices

- Use short TTLs for records that may change frequently
- Implement DNSSEC for production DNS infrastructure
- Use multiple authoritative nameservers for redundancy
- Monitor DNS propagation after changes
- Implement rate limiting on DNS servers to prevent abuse
- Use anycast for geographic distribution
- Consider DNS-over-HTTPS for privacy-sensitive applications
- Maintain proper SOA records for zone management
- Implement proper zone transfers for secondary servers
- Use monitoring to detect DNS issues early

## Core Competencies

- DNS record types and their uses
- DNS resolution process
- Zone file management
- DNSSEC implementation
- DNS caching strategies
- DNS-based load balancing
- Service discovery patterns
- Dynamic DNS updates
- DNS monitoring and troubleshooting
- DNS security considerations
- DNS propagation
- Anycast configuration
- DNS query optimization
