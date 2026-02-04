---
name: data-serialization
description: Efficient data serialization for game networking including Protobuf, FlatBuffers, and custom binary
sasmp_version: "1.3.0"
version: "2.0.0"
bonded_agent: 02-networking-specialist
bond_type: SECONDARY_BOND

# Parameters
parameters:
  required:
    - format
  optional:
    - compression
    - schema_validation
  validation:
    format:
      type: string
      enum: [protobuf, flatbuffers, msgpack, json, custom_binary]
    compression:
      type: string
      enum: [none, lz4, zstd]
      default: none
    schema_validation:
      type: boolean
      default: true

# Retry Configuration
retry_config:
  max_attempts: 1
  fallback: json

# Observability
observability:
  logging:
    level: debug
    fields: [format, size_bytes, compression_ratio]
  metrics:
    - name: serialization_duration_ms
      type: histogram
    - name: serialized_bytes
      type: counter
---

# Data Serialization for Games

Implement **efficient serialization** for low-latency game networking.

## Format Comparison

| Format | Size | Speed | Schema | Use Case |
|--------|------|-------|--------|----------|
| Protobuf | Small | Fast | Required | Most games |
| FlatBuffers | Small | Fastest | Required | Real-time |
| MsgPack | Small | Fast | Optional | Flexible |
| JSON | Large | Slow | None | Debug |
| Custom Binary | Smallest | Fastest | Custom | Ultra-low latency |

## Protocol Buffers

```protobuf
syntax = "proto3";

message PlayerState {
    uint32 player_id = 1;
    float x = 2;
    float y = 3;
    float z = 4;
    uint32 health = 5;
}

message GameUpdate {
    uint64 tick = 1;
    repeated PlayerState players = 2;
}
```

```cpp
GameUpdate update;
update.set_tick(current_tick);
auto* player = update.add_players();
player->set_player_id(1);
player->set_x(pos.x);

std::string serialized;
update.SerializeToString(&serialized);
```

## Custom Binary Format

```cpp
struct PacketHeader {
    uint16_t type;
    uint16_t length;
    uint32_t sequence;
};

struct PlayerUpdate {
    uint32_t player_id;
    float position[3];
    uint16_t angle;  // Compressed rotation
    uint8_t flags;
};

void serialize(Buffer& buf, const PlayerUpdate& p) {
    buf.write_u32(htonl(p.player_id));
    for (int i = 0; i < 3; i++)
        buf.write_float(p.position[i]);
    buf.write_u16(htons(p.angle));
    buf.write_u8(p.flags);
}
```

## Compression Techniques

| Technique | Savings | Complexity |
|-----------|---------|------------|
| Delta | 50-80% | Medium |
| Quantization | 30-50% | Low |
| LZ4 | 50-70% | Low |

## Troubleshooting

### Common Failure Modes

| Error | Root Cause | Solution |
|-------|------------|----------|
| Parse error | Version mismatch | Schema versioning |
| Large packets | No compression | Enable delta/LZ4 |
| Slow parsing | JSON in hot path | Use binary format |
| Corruption | Byte order | Use htonl/ntohl |

### Debug Checklist

```cpp
// Check serialized size
std::string data;
message.SerializeToString(&data);
std::cout << "Size: " << data.size() << " bytes\n";

// Validate roundtrip
Message parsed;
parsed.ParseFromString(data);
assert(parsed.id() == message.id());
```

## Unit Test Template

```cpp
TEST(Serialization, RoundTrip) {
    PlayerState original{1, 10.0f, 20.0f, 30.0f, 100};

    std::string data;
    original.SerializeToString(&data);

    PlayerState parsed;
    parsed.ParseFromString(data);

    EXPECT_EQ(original.player_id(), parsed.player_id());
    EXPECT_FLOAT_EQ(original.x(), parsed.x());
}
```

## Resources

- `assets/` - Schema templates
- `references/` - Format benchmarks
