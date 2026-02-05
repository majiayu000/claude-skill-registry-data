---
name: networking
description: Game networking protocols, WebSocket/UDP implementation, latency optimization for real-time multiplayer
sasmp_version: "1.3.0"
version: "2.0.0"
bonded_agent: 02-networking-specialist
bond_type: PRIMARY_BOND

# Parameters
parameters:
  required:
    - protocol_type
    - connection_count
  optional:
    - latency_target_ms
    - bandwidth_limit_kbps
  validation:
    protocol_type:
      type: string
      enum: [websocket, udp, quic, tcp]
    connection_count:
      type: integer
      min: 1
      max: 100000
    latency_target_ms:
      type: integer
      min: 10
      max: 500
      default: 100

# Retry Configuration
retry_config:
  max_attempts: 3
  backoff: exponential
  initial_delay_ms: 100
  max_delay_ms: 5000
  retryable_errors:
    - ECONNRESET
    - ETIMEDOUT
    - ECONNREFUSED

# Observability
observability:
  logging:
    level: info
    fields: [connection_id, latency_ms, packet_size]
  metrics:
    - name: network_connections_active
      type: gauge
    - name: network_latency_ms
      type: histogram
    - name: network_bytes_sent
      type: counter
  tracing:
    enabled: true
    sample_rate: 0.1
---

# Game Networking

Implement **real-time multiplayer networking** with WebSocket, UDP, and latency optimization.

## WebSocket Game Server

```javascript
const WebSocket = require('ws');

class GameServer {
  constructor(port = 8080) {
    this.wss = new WebSocket.Server({ port });
    this.players = new Map();
    this.setupHandlers();
  }

  setupHandlers() {
    this.wss.on('connection', (ws, req) => {
      const playerId = this.generateId();
      const player = { ws, state: {}, joinedAt: Date.now() };
      this.players.set(playerId, player);

      ws.on('message', (data) => this.handleMessage(playerId, data));
      ws.on('close', () => this.handleDisconnect(playerId));
      ws.on('error', (err) => this.handleError(playerId, err));

      this.sendToPlayer(playerId, { type: 'connected', playerId });
    });
  }

  handleMessage(playerId, data) {
    try {
      const msg = JSON.parse(data);
      // Validate message structure
      if (!msg.type) throw new Error('Missing message type');
      this.processGameMessage(playerId, msg);
    } catch (err) {
      console.error(`Invalid message from ${playerId}:`, err.message);
    }
  }

  broadcast(msg, exclude = null) {
    const data = JSON.stringify(msg);
    this.players.forEach((player, id) => {
      if (id !== exclude && player.ws.readyState === WebSocket.OPEN) {
        player.ws.send(data);
      }
    });
  }
}
```

## UDP for Low Latency

```javascript
const dgram = require('dgram');

class UDPGameServer {
  constructor(port = 7777) {
    this.socket = dgram.createSocket('udp4');
    this.clients = new Map(); // address:port -> client
    this.sequence = 0;

    this.socket.on('message', (msg, rinfo) => {
      const key = `${rinfo.address}:${rinfo.port}`;
      this.handlePacket(key, msg, rinfo);
    });

    this.socket.bind(port);
  }

  send(client, data, reliable = false) {
    const packet = this.createPacket(data, reliable);
    this.socket.send(packet, client.port, client.address);
  }

  createPacket(data, reliable) {
    const seq = this.sequence++;
    const header = Buffer.alloc(4);
    header.writeUInt16LE(seq, 0);
    header.writeUInt8(reliable ? 1 : 0, 2);
    return Buffer.concat([header, data]);
  }
}
```

## Protocol Selection Guide

| Protocol | Latency | Reliability | Use Case |
|----------|---------|-------------|----------|
| WebSocket | 20-50ms | High | Web games, chat |
| UDP | 5-20ms | None | FPS, racing |
| QUIC | 10-30ms | Configurable | Modern hybrid |
| TCP | 30-100ms | High | Turn-based, MMO |

## Troubleshooting

### Common Failure Modes

| Error | Root Cause | Solution |
|-------|------------|----------|
| ECONNRESET | Client disconnect | Graceful handling |
| High latency | Network congestion | Enable delta compression |
| Packet loss | UDP unreliability | Add reliability layer |
| WebSocket timeout | Idle connection | Implement heartbeat |

### Debug Checklist

```bash
# Check active connections
netstat -an | grep :8080 | wc -l

# Monitor bandwidth
iftop -i eth0 -f "port 8080"

# Capture packets
tcpdump -i eth0 port 8080 -w capture.pcap
```

## Unit Test Template

```javascript
describe('GameServer', () => {
  let server, client;

  beforeEach(() => {
    server = new GameServer(8081);
    client = new WebSocket('ws://localhost:8081');
  });

  afterEach(() => {
    client.close();
    server.close();
  });

  test('accepts connections', (done) => {
    client.on('open', () => {
      expect(server.players.size).toBe(1);
      done();
    });
  });

  test('broadcasts messages', (done) => {
    client.on('message', (data) => {
      const msg = JSON.parse(data);
      expect(msg.type).toBe('connected');
      done();
    });
  });
});
```

## Resources

- `assets/` - Server templates
- `scripts/` - Network testing tools
- `references/` - Protocol guides
