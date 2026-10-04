---
name: services
description: "Skill for the Services area of Securacy. 113 symbols across 25 files."
---

# Services

113 symbols | 25 files | Cohesion: 89%

## When to Use

- Working with code in `securacyfrontend/`
- Understanding how generate_key, create_api_key, list_api_keys work
- Modifying services-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `securacyfrontend/services/authService.ts` | syncUserToCookie, setupGoogleAuth, handleCredentialResponse, messageListener, handleOAuth2Callback (+18) |
| `backend/buddlyai/Services/llm_logger.py` | estimate_cost, _accumulate, to_dict, log_entry, _truncate (+12) |
| `backend/buddlyai/Services/logger.py` | get_logger, wrapper, debug, info, error (+4) |
| `backend/buddlyai/Services/mcp_keys.py` | _get_engine, _ensure_table, _hash_key, generate_key, create_api_key (+3) |
| `backend/buddlyai/Routes/MCPController.py` | _check_rate_limit, _build_setup_instructions, create_api_key, list_api_keys, revoke_api_key (+1) |
| `securacyfrontend/services/xmlToIRParser.ts` | parseDrawioXmlToIR, detectNodeType, cleanLabel, extractTech, extractPortSides (+1) |
| `backend/buddlyai/Services/auth.py` | get_jwks, verify_token, verify_cognito_token, verify_jwt_only, verify_both_auth_required |
| `securacyfrontend/services/privacydiagramService.ts` | generateDiagram, initializeDiagram, loadDrawIo, handleMessage, downloadExportedData |
| `securacyfrontend/services/paymentService.ts` | loadRazorpayScript, toPaise, initiatePayment, initiateExtension |
| `securacyfrontend/context/AuthContext.tsx` | signOut, AuthProvider, initAuth, signIn |

## Entry Points

Start here when exploring this area:

- **`generate_key`** (Function) — `backend/buddlyai/Services/mcp_keys.py:63`
- **`create_api_key`** (Function) — `backend/buddlyai/Services/mcp_keys.py:67`
- **`list_api_keys`** (Function) — `backend/buddlyai/Services/mcp_keys.py:112`
- **`revoke_api_key`** (Function) — `backend/buddlyai/Services/mcp_keys.py:139`
- **`get_tenant_usage`** (Function) — `backend/buddlyai/Services/mcp_keys.py:158`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `generate_key` | Function | `backend/buddlyai/Services/mcp_keys.py` | 63 |
| `create_api_key` | Function | `backend/buddlyai/Services/mcp_keys.py` | 67 |
| `list_api_keys` | Function | `backend/buddlyai/Services/mcp_keys.py` | 112 |
| `revoke_api_key` | Function | `backend/buddlyai/Services/mcp_keys.py` | 139 |
| `get_tenant_usage` | Function | `backend/buddlyai/Services/mcp_keys.py` | 158 |
| `create_api_key` | Function | `backend/buddlyai/Routes/MCPController.py` | 90 |
| `list_api_keys` | Function | `backend/buddlyai/Routes/MCPController.py` | 120 |
| `revoke_api_key` | Function | `backend/buddlyai/Routes/MCPController.py` | 126 |
| `get_usage` | Function | `backend/buddlyai/Routes/MCPController.py` | 135 |
| `generate_privacythreat_json_reasoning_claude_bedrock` | Function | `backend/buddlyai/privacy/privacy_threat_analysis_prompt.py` | 249 |
| `estimate_cost` | Function | `backend/buddlyai/Services/llm_logger.py` | 60 |
| `to_dict` | Function | `backend/buddlyai/Services/llm_logger.py` | 190 |
| `log_entry` | Function | `backend/buddlyai/Services/llm_logger.py` | 230 |
| `wrapper` | Function | `backend/buddlyai/Services/llm_logger.py` | 293 |
| `wrap_bedrock_invoke` | Function | `backend/buddlyai/Services/llm_logger.py` | 520 |
| `on_llm_end` | Function | `backend/buddlyai/Services/llm_logger.py` | 658 |
| `on_llm_error` | Function | `backend/buddlyai/Services/llm_logger.py` | 700 |
| `run_privacythreat_analysis_with_rag` | Function | `backend/buddlyai/Routes/PrivacyController.py` | 428 |
| `initiatePayment` | Function | `securacyfrontend/services/paymentService.ts` | 79 |
| `initiateExtension` | Function | `securacyfrontend/services/paymentService.ts` | 186 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `HandleGoogleLogin → IsAllowedDomain` | cross_community | 7 |
| `HandleGoogleLogin → SyncUserToCookie` | cross_community | 7 |
| `PrivacyBot → _syncUserWithBackend` | cross_community | 6 |
| `AuthProvider → IsAllowedDomain` | cross_community | 6 |
| `AuthProvider → SyncUserToCookie` | cross_community | 6 |
| `AuthProvider → _syncUserWithBackend` | cross_community | 6 |
| `Constructor → StopSessionMonitoring` | cross_community | 6 |
| `Constructor → ClearUserCookie` | cross_community | 6 |
| `Constructor → _syncUserWithBackend` | cross_community | 6 |
| `PrivacyBot → StopSessionMonitoring` | cross_community | 5 |

## Connected Areas

| Area | Connections |
|------|-------------|
| _components | 6 calls |
| Securacymcp | 3 calls |

## How to Explore

1. `gitnexus_context({name: "generate_key"})` — see callers and callees
2. `gitnexus_query({query: "services"})` — find related execution flows
3. Read key files listed above for implementation details
