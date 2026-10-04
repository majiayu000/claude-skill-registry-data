---
name: CAN ASK MCP
version: 1.9.0
description: "Agent & MCP integration. CAN stamps what flows through any pipe. Verify, name, log locally."
homepage: https://github.com/xccx/can
metadata: {"openclaw":{"emoji":"❓","requires":{"bins":["sha256sum","date"]}}}
---

Version 1.9.0 of CAN focuses on integrating Clock Address Naming with AI agents, specifically those utilizing the Model Context Protocol (MCP). 

CAN provides a localized, verifiable naming and storage layer for the data agents retrieve from tools, operating entirely independently of the transport layer.

## Architecture: CAN + MCP

MCP handles tool connection and data transport. CAN handles verification, naming, and historical logging of the data retrieved via MCP.

Because CAN is strictly a local operation (computing a hash, timestamping, and writing to a file), it requires zero integration with the MCP server. The server does not need to know CAN exists.

**Workflow:**
1. Agent requests data from an MCP tool.
2. Agent receives the response payload.
3. Agent locally applies a CAN stamp (WHEN, WHERE, WHAT) to the payload.
4. Agent logs the stamp to its local `index.tsv`.

This allows agents to verifiably recall past tool outputs without re-querying the server, proving that the data has not been mutated since it was retrieved.

## Agent Implementation Tests

The 1.9.0 release asks agent developers to evaluate CAN as a standard logging and retrieval mechanism. The following tests demonstrate standard agent operations using CAN.

### Test 1: Basic Stamping
Agents can natively generate the requirements for a CAN entry using standard system utilities.

```bash
WHEN=$(date +%s%3N)
WHERE=$(sha256sum <<< "tool_output_string" | awk '{print $1}')
WHAT="tool_name.result"

echo -e "$WHEN\t$WHERE\t$WHAT" >> ~/.can/index.tsv
```

### Test 2: Local Verification
Before trusting cached data, agents verify the integrity of the data against the hash (`WHERE`) stored in the CAN index. 

```bash
CLAIMED_HASH="a948904f2f0f479b8f8564e9d7e91d9820b5..."
ACTUAL_HASH=$(sha256sum <<< "tool_output_string" | awk '{print $1}')

if [ "$ACTUAL_HASH" = "$CLAIMED_HASH" ]; then
    # Valid (CAN)
else
    # Invalid/Mutated (NOT)
fi
```

### Test 3: Stamping MCP Results
A practical example of an agent logging an MCP tool execution.

```bash
# 1. Execute MCP tool
RESULT=$(mcp_call fetch_report "Q3_Data")

# 2. Generate CAN stamp locally
WHEN=$(date +%s%3N)
WHERE=$(echo -n "$RESULT" | sha256sum | awk '{print $1}')
WHAT="fetch_report.Q3_Data SAVE"

# 3. Append to index
echo -e "$WHEN\t$WHERE\t$WHAT" >> ~/.can/index.tsv
```

## Advantages for Agents

Can optionally works in parallel with location-based naming (e.g., standard file paths) while offering several technical benefits for autonomous agents:

*   **Offline Recall:** Agents can verify and retrieve past MCP results without network overhead or re-querying the tool.
*   **Tamper Evidence:** Hash verification guarantees that context injected into prompts is exactly what was originally returned by the tool.
*   **Search Optimization:** Agents can filter local memory logs by timestamp (WHEN), exact content match (WHERE), or metadata/intent (WHAT).
*   **Decoupling:** If the MCP server goes offline or the tool's API changes, the historical data remains perfectly addressable and verifiable in the agent's local state.

## Version Roadmap
*   **1.8.0:** Core CAN specification (WHEN + WHERE + WHAT).
*   **1.9.0 (Current):** Agent/MCP integration and local evaluation logs.
*   **2.x (Future):** Peer-to-peer verification, physical co-presence proofs, and verifiable exchanges.
