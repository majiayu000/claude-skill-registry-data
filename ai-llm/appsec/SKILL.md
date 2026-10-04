---
name: appsec
description: "Skill for the Appsec area of Securacy. 152 symbols across 23 files."
---

# Appsec

152 symbols | 23 files | Cohesion: 88%

## When to Use

- Working with code in `backend/`
- Understanding how find_entity, find_store, find_processes work
- Modifying appsec-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `backend/buddlyai/appsec/interactive_cybersecurity_questionnaire_langchain.py` | add_exchange, mark_topic_complete, move_to_next_topic, get_remaining_topics, _extract_json_from_response (+18) |
| `backend/buddlyai/appsec/drawio.py` | find_entity, find_store, find_processes, find_matching_process, parse_flow (+12) |
| `backend/buddlyai/appsec/threat_analysis_prompt.py` | create_threat_dashboard, calculate_confidence, find_matching_threats, validate_with_rag, present_analysis_to_user (+8) |
| `backend/buddlyai/appsec/Input.py` | createsystempromptinputfromarchdiagramAndReturnresultsPure, createsystempromptinputfromterraformAndreturnresults, createsyextractsysteminputs, extract_features, createsystempromptdfddfeatures (+7) |
| `backend/buddlyai/appsec/test_appsecquestionairre_api.py` | call_responseApi, test_questionnaire_api_forEcommerce, test_questionnaire_api_forOilGas, test_questionnaire_api_forEcommerceWithProgress, test_questionnaire_api_forRetailWithProgress (+7) |
| `backend/buddlyai/appsec/test_prompt_injection_detection.py` | test_classic_prompt_injection_phrases, test_ai_specific_injection_tricks, test_subtle_social_engineering_prompts, test_combined_injection_attempts, test_valid_responses_not_flagged (+4) |
| `backend/buddlyai/Routes/AppSecController.py` | check_responses, get_Next_Question, get_input_options, download_pdf, download_csv (+4) |
| `securacyfrontend/app/home/(bots)/appsec/page.tsx` | AppsecBot, getThreatCount, getExecutiveSummarySnippet, getThreatSummarySubtitle, scrollToBottom (+4) |
| `backend/buddlyai/appsec/getInputOptionsAppsecy.py` | checkifTopicAndResponseusingLLM, count_tokens, loadprompt, getInputOptionsFordomain, getNextQuestion (+2) |
| `backend/buddlyai/appsec/downloadresults.py` | split_to_bullet_points, downloadresultsaspdf, downloadresultsascsv, downloadresultsasjson, main |

## Entry Points

Start here when exploring this area:

- **`find_entity`** (Function) — `backend/buddlyai/appsec/drawio.py:11`
- **`find_store`** (Function) — `backend/buddlyai/appsec/drawio.py:36`
- **`find_processes`** (Function) — `backend/buddlyai/appsec/drawio.py:45`
- **`find_matching_process`** (Function) — `backend/buddlyai/appsec/drawio.py:67`
- **`parse_flow`** (Function) — `backend/buddlyai/appsec/drawio.py:75`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `find_entity` | Function | `backend/buddlyai/appsec/drawio.py` | 11 |
| `find_store` | Function | `backend/buddlyai/appsec/drawio.py` | 36 |
| `find_processes` | Function | `backend/buddlyai/appsec/drawio.py` | 45 |
| `find_matching_process` | Function | `backend/buddlyai/appsec/drawio.py` | 67 |
| `parse_flow` | Function | `backend/buddlyai/appsec/drawio.py` | 75 |
| `generate_drawio_dfd` | Function | `backend/buddlyai/appsec/drawio.py` | 128 |
| `get_id` | Function | `backend/buddlyai/appsec/drawio.py` | 152 |
| `is_system_entity` | Function | `backend/buddlyai/appsec/drawio.py` | 254 |
| `get_component_bounds` | Function | `backend/buddlyai/appsec/drawio.py` | 491 |
| `normalize_arrows` | Function | `backend/buddlyai/appsec/drawio.py` | 586 |
| `check_process_overlap` | Function | `backend/buddlyai/appsec/drawio.py` | 952 |
| `find_non_overlapping_position` | Function | `backend/buddlyai/appsec/drawio.py` | 973 |
| `optimize_process_positions` | Function | `backend/buddlyai/appsec/drawio.py` | 1006 |
| `line_circle_intersection` | Function | `backend/buddlyai/appsec/drawio.py` | 1088 |
| `get_connection_line` | Function | `backend/buddlyai/appsec/drawio.py` | 1130 |
| `avoid_arrow_intersections` | Function | `backend/buddlyai/appsec/drawio.py` | 1182 |
| `test_classic_prompt_injection_phrases` | Function | `backend/buddlyai/appsec/test_prompt_injection_detection.py` | 26 |
| `test_ai_specific_injection_tricks` | Function | `backend/buddlyai/appsec/test_prompt_injection_detection.py` | 50 |
| `test_subtle_social_engineering_prompts` | Function | `backend/buddlyai/appsec/test_prompt_injection_detection.py` | 71 |
| `test_combined_injection_attempts` | Function | `backend/buddlyai/appsec/test_prompt_injection_detection.py` | 92 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `AppsecBot → DecodeJwt` | cross_community | 8 |
| `AppsecBot → FindNodeIdByName` | cross_community | 6 |
| `AppsecBot → NormalizeNodeType` | cross_community | 5 |
| `AppsecBot → IsKnownIntegration` | cross_community | 5 |
| `AppsecBot → NameToId` | cross_community | 5 |
| `HandleSaveAnalysis → FindNodeIdByName` | cross_community | 5 |
| `PrivacyBot → GenerateDfdJSON` | cross_community | 4 |
| `AppsecBot → GenerateDfdJSON` | cross_community | 4 |
| `Generate_privacyDFD → GetOrphanedProcessEntityAndStore` | cross_community | 4 |
| `Generate_privacyDFD → _find_suitable_entity` | cross_community | 4 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Services | 3 calls |
| Privacy | 1 calls |
| Dfd | 1 calls |

## How to Explore

1. `gitnexus_context({name: "find_entity"})` — see callers and callees
2. `gitnexus_query({query: "appsec"})` — find related execution flows
3. Read key files listed above for implementation details
