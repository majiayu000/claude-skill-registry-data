---
name: communication-protocols
description: Game server communication protocols including gRPC, REST, and custom binary protocols
sasmp_version: "1.3.0"
version: "2.0.0"
bonded_agent: 02-networking-specialist
bond_type: SECONDARY_BOND

# Parameters
parameters:
  required:
    - protocol_type
  optional:
    - serialization_format
    - compression
  validation:
    protocol_type:
      type: string
      enum: [grpc, rest, websocket, custom_binary, quic]
    serialization_format:
      type: string
      enum: [protobuf, json, msgpack, flatbuffers]
      default: protobuf
    compression:
      type: string
      enum: [none, gzip, lz4, zstd]
      default: none

# Retry Configuration
retry_config:
  max_attempts: 3
  backoff: exponential
  initial_delay_ms: 100
  retryable_errors:
    - UNAVAILABLE
    - DEADLINE_EXCEEDED

# Observability
observability:
  logging:
    level: info
    fields: [protocol, method, duration_ms, status]
  metrics:
    - name: rpc_duration_seconds
      type: histogram
    - name: rpc_requests_total
      type: counter
    - name: rpc_errors_total
      type: counter
    - name: message_size_bytes
      type: histogram
---

# Communication Protocols for Game Servers

Implement **efficient communication protocols** between game services and clients.

## Protocol Selection Guide

| Protocol | Latency | Throughput | Use Case |
|----------|---------|------------|----------|
| **Custom Binary** | Lowest | Highest | Real-time gameplay |
| **gRPC** | Low | High | Service-to-service |
| **WebSocket** | Low | Medium | Browser clients |
| **REST** | Medium | Medium | Admin APIs, lobbies |
| **QUIC** | Low | High | Mobile, unreliable networks |

## gRPC for Game Services

```protobuf
// matchmaking.proto
syntax = "proto3";

package game.matchmaking;

service Matchmaking {
    rpc FindMatch(MatchRequest) returns (MatchResponse);
    rpc JoinQueue(QueueRequest) returns (stream QueueUpdate);
    rpc CancelQueue(CancelRequest) returns (CancelResponse);
}

message MatchRequest {
    string player_id = 1;
    string game_mode = 2;
    int32 skill_rating = 3;
    repeated string preferred_regions = 4;
}

message MatchResponse {
    string match_id = 1;
    string server_address = 2;
    int32 server_port = 3;
    repeated TeamAssignment teams = 4;
    string connection_token = 5;
}

message QueueUpdate {
    enum Status {
        SEARCHING = 0;
        MATCH_FOUND = 1;
        CANCELLED = 2;
    }
    Status status = 1;
    int32 estimated_wait_seconds = 2;
    int32 players_in_queue = 3;
}
```

### Go gRPC Server

```go
type matchmakingServer struct {
    pb.UnimplementedMatchmakingServer
    matchmaker *Matchmaker
}

func (s *matchmakingServer) FindMatch(
    ctx context.Context,
    req *pb.MatchRequest,
) (*pb.MatchResponse, error) {
    match, err := s.matchmaker.FindMatch(ctx, req.PlayerId, req.GameMode, req.SkillRating)
    if err != nil {
        return nil, status.Errorf(codes.Internal, "matchmaking failed: %v", err)
    }

    return &pb.MatchResponse{
        MatchId:       match.ID,
        ServerAddress: match.ServerAddr,
        ServerPort:    int32(match.ServerPort),
        ConnectionToken: match.Token,
    }, nil
}

func (s *matchmakingServer) JoinQueue(
    req *pb.QueueRequest,
    stream pb.Matchmaking_JoinQueueServer,
) error {
    updates := s.matchmaker.Subscribe(req.PlayerId)
    defer s.matchmaker.Unsubscribe(req.PlayerId)

    for update := range updates {
        if err := stream.Send(update); err != nil {
            return err
        }
        if update.Status == pb.QueueUpdate_MATCH_FOUND {
            return nil
        }
    }
    return nil
}
```

## Custom Binary Protocol

```cpp
// Packet header (8 bytes)
struct PacketHeader {
    uint8_t type;        // Message type
    uint8_t flags;       // Compression, reliability flags
    uint16_t length;     // Payload length
    uint32_t sequence;   // Packet sequence for ordering/ack
};

enum PacketType : uint8_t {
    PLAYER_INPUT    = 0x01,
    STATE_UPDATE    = 0x02,
    PLAYER_JOIN     = 0x03,
    PLAYER_LEAVE    = 0x04,
    CHAT_MESSAGE    = 0x10,
    PING            = 0xFE,
    PONG            = 0xFF
};

enum PacketFlags : uint8_t {
    FLAG_RELIABLE   = 0x01,
    FLAG_COMPRESSED = 0x02,
    FLAG_ENCRYPTED  = 0x04
};

// Zero-copy packet builder
class PacketBuilder {
    uint8_t buffer[MAX_PACKET_SIZE];
    size_t offset = sizeof(PacketHeader);

public:
    PacketBuilder& writeU8(uint8_t v) {
        buffer[offset++] = v;
        return *this;
    }

    PacketBuilder& writeU16(uint16_t v) {
        *reinterpret_cast<uint16_t*>(&buffer[offset]) = htons(v);
        offset += 2;
        return *this;
    }

    PacketBuilder& writeFloat(float v) {
        *reinterpret_cast<float*>(&buffer[offset]) = v;
        offset += 4;
        return *this;
    }

    std::span<uint8_t> build(PacketType type, uint8_t flags = 0) {
        auto* header = reinterpret_cast<PacketHeader*>(buffer);
        header->type = static_cast<uint8_t>(type);
        header->flags = flags;
        header->length = htons(offset - sizeof(PacketHeader));
        header->sequence = htonl(nextSequence++);
        return {buffer, offset};
    }
};

// Player input packet (compact)
struct PlayerInputPacket {
    uint32_t tick;          // 4 bytes
    uint8_t keys;           // 1 byte: WASD + jump + fire (bitfield)
    int16_t aim_x;          // 2 bytes: quantized aim [-32768, 32767]
    int16_t aim_y;          // 2 bytes: quantized aim
};  // Total: 9 bytes
```

## WebSocket for Browser Games

```javascript
// Server (Node.js with ws)
const WebSocket = require('ws');

const wss = new WebSocket.Server({
    port: 8080,
    perMessageDeflate: true,  // Compression
    maxPayload: 64 * 1024     // 64KB limit
});

wss.on('connection', (ws, req) => {
    const playerId = authenticate(req);

    ws.on('message', (data, isBinary) => {
        if (isBinary) {
            // Binary protocol for gameplay
            const view = new DataView(data.buffer);
            const type = view.getUint8(0);
            handleBinaryMessage(playerId, type, view);
        } else {
            // JSON for lobby/chat
            const msg = JSON.parse(data);
            handleJsonMessage(playerId, msg);
        }
    });

    ws.on('close', () => {
        onPlayerDisconnect(playerId);
    });

    // Send binary state updates at 60Hz
    const tickInterval = setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) {
            const state = serializeGameState(playerId);
            ws.send(state, { binary: true });
        }
    }, 16);

    ws.on('close', () => clearInterval(tickInterval));
});

// Client
class GameClient {
    constructor(url) {
        this.ws = new WebSocket(url);
        this.ws.binaryType = 'arraybuffer';

        this.ws.onmessage = (event) => {
            if (event.data instanceof ArrayBuffer) {
                this.handleStateUpdate(new DataView(event.data));
            } else {
                this.handleJsonMessage(JSON.parse(event.data));
            }
        };
    }

    sendInput(keys, aimX, aimY) {
        const buffer = new ArrayBuffer(9);
        const view = new DataView(buffer);
        view.setUint32(0, this.currentTick);
        view.setUint8(4, keys);
        view.setInt16(5, aimX);
        view.setInt16(7, aimY);
        this.ws.send(buffer);
    }
}
```

## REST API for Game Services

```go
// Lobby API with proper error handling
type LobbyHandler struct {
    lobbyService *LobbyService
}

func (h *LobbyHandler) CreateLobby(w http.ResponseWriter, r *http.Request) {
    var req CreateLobbyRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        respondError(w, http.StatusBadRequest, "invalid request body")
        return
    }

    lobby, err := h.lobbyService.Create(r.Context(), req)
    if err != nil {
        switch {
        case errors.Is(err, ErrPlayerAlreadyInLobby):
            respondError(w, http.StatusConflict, err.Error())
        case errors.Is(err, ErrMaxLobbiesReached):
            respondError(w, http.StatusTooManyRequests, err.Error())
        default:
            respondError(w, http.StatusInternalServerError, "internal error")
        }
        return
    }

    respondJSON(w, http.StatusCreated, lobby)
}

func respondJSON(w http.ResponseWriter, status int, data interface{}) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(status)
    json.NewEncoder(w).Encode(data)
}
```

## Protocol Selection Matrix

| Scenario | Protocol | Reason |
|----------|----------|--------|
| Real-time gameplay | Custom UDP binary | Lowest latency |
| Microservices | gRPC | Type safety, streaming |
| Web/mobile lobby | WebSocket JSON | Browser compatibility |
| Admin dashboard | REST | Standard tooling |
| Streaming updates | gRPC streaming | Backpressure handling |

## Troubleshooting

### Common Failure Modes

| Error | Root Cause | Solution |
|-------|------------|----------|
| Connection reset | Message too large | Chunk large messages |
| Timeout | Slow processing | Async handlers |
| Parse error | Version mismatch | Protocol versioning |
| High latency | No compression | Enable compression |

### Debug Checklist

```bash
# gRPC debugging
GRPC_VERBOSITY=DEBUG GRPC_TRACE=all ./game-server

# WebSocket inspection
wscat -c ws://localhost:8080

# Protocol buffer decoding
protoc --decode=game.StateUpdate game.proto < message.bin

# Network trace
tcpdump -i any port 8080 -w capture.pcap
```

## Unit Test Template

```go
func TestMatchmakingRPC(t *testing.T) {
    server := setupTestServer()
    defer server.Stop()

    conn, err := grpc.Dial(server.Addr, grpc.WithInsecure())
    require.NoError(t, err)
    defer conn.Close()

    client := pb.NewMatchmakingClient(conn)

    resp, err := client.FindMatch(context.Background(), &pb.MatchRequest{
        PlayerId:    "player123",
        GameMode:    "ranked",
        SkillRating: 1500,
    })

    require.NoError(t, err)
    assert.NotEmpty(t, resp.MatchId)
    assert.NotEmpty(t, resp.ServerAddress)
}

func TestBinaryProtocol(t *testing.T) {
    builder := NewPacketBuilder()
    packet := builder.
        WriteU32(12345).  // tick
        WriteU8(0x0F).    // keys
        WriteI16(1000).   // aim_x
        WriteI16(-500).   // aim_y
        Build(PLAYER_INPUT)

    parsed := ParsePlayerInput(packet)
    assert.Equal(t, uint32(12345), parsed.Tick)
    assert.Equal(t, uint8(0x0F), parsed.Keys)
}
```

## Resources

- `assets/` - Protocol templates
- `references/` - Performance benchmarks
