---
name: privacy
description: "Skill for the Privacy area of Securacy. 73 symbols across 9 files."
---

# Privacy

73 symbols | 9 files | Cohesion: 85%

## When to Use

- Working with code in `backend/`
- Understanding how add_exchange, mark_topic_complete, move_to_next_topic work
- Modifying privacy-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `backend/buddlyai/privacy/interactive_privacy_questionnaire_langchain.py` | add_exchange, mark_topic_complete, move_to_next_topic, get_remaining_topics, _build_enhanced_input (+22) |
| `securacyfrontend/app/home/(bots)/privacy/page.tsx` | mapAnswersToAnalysisData, getAnswerForTopic, handleNextQuestion, getPrivacyThreatSummarySubtitle, getPrivacyThreatCount (+9) |
| `backend/buddlyai/Routes/PrivacyController.py` | start_privacy_questionnaire, get_privacy_questionnaire_progress, get_privacy_questionnaire_summary, privacy_download_pdf, privacy_download_csv (+3) |
| `securacyfrontend/lib/questions.ts` | getDomainSpecificOptions, toTitleCase, getDomainFromResponse, respondQuestion, startQuestion (+1) |
| `backend/buddlyai/privacy/downloadresultsprivacy.py` | split_to_bullet_points, downloadresultsaspdf, downloadresultsascsv, downloadresultsasjson, main |
| `securacyfrontend/app/home/(bots)/appsec/page.tsx` | mapAnswersToAnalysisData, getAnswerForTopic, handleNextQuestion, initSession |
| `backend/buddlyai/privacy/generate_dfd_with_ai.py` | generatelevel0dfdprivacy, _validate_and_clean_xml, _get_fallback_xml, main |
| `backend/buddlyai/privacy/privacy_threat_analysis_prompt.py` | create_threat_dashboard, calculate_confidence, find_matching_threats, validate_with_rag |
| `securacyfrontend/services/privacyquestions.ts` | startPrivacyQuestion |

## Entry Points

Start here when exploring this area:

- **`add_exchange`** (Function) — `backend/buddlyai/privacy/interactive_privacy_questionnaire_langchain.py:45`
- **`mark_topic_complete`** (Function) — `backend/buddlyai/privacy/interactive_privacy_questionnaire_langchain.py:50`
- **`move_to_next_topic`** (Function) — `backend/buddlyai/privacy/interactive_privacy_questionnaire_langchain.py:55`
- **`get_remaining_topics`** (Function) — `backend/buddlyai/privacy/interactive_privacy_questionnaire_langchain.py:66`
- **`process_response`** (Function) — `backend/buddlyai/privacy/interactive_privacy_questionnaire_langchain.py:742`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `add_exchange` | Function | `backend/buddlyai/privacy/interactive_privacy_questionnaire_langchain.py` | 45 |
| `mark_topic_complete` | Function | `backend/buddlyai/privacy/interactive_privacy_questionnaire_langchain.py` | 50 |
| `move_to_next_topic` | Function | `backend/buddlyai/privacy/interactive_privacy_questionnaire_langchain.py` | 55 |
| `get_remaining_topics` | Function | `backend/buddlyai/privacy/interactive_privacy_questionnaire_langchain.py` | 66 |
| `process_response` | Function | `backend/buddlyai/privacy/interactive_privacy_questionnaire_langchain.py` | 742 |
| `get_system_context` | Function | `backend/buddlyai/privacy/interactive_privacy_questionnaire_langchain.py` | 93 |
| `get_progress_summary` | Function | `backend/buddlyai/privacy/interactive_privacy_questionnaire_langchain.py` | 101 |
| `add_context` | Function | `backend/buddlyai/privacy/interactive_privacy_questionnaire_langchain.py` | 168 |
| `start_interview` | Function | `backend/buddlyai/privacy/interactive_privacy_questionnaire_langchain.py` | 701 |
| `generate_summary` | Function | `backend/buddlyai/privacy/interactive_privacy_questionnaire_langchain.py` | 985 |
| `save_session` | Function | `backend/buddlyai/privacy/interactive_privacy_questionnaire_langchain.py` | 1078 |
| `get_memory_summary` | Function | `backend/buddlyai/privacy/interactive_privacy_questionnaire_langchain.py` | 1106 |
| `run_interactive_session` | Function | `backend/buddlyai/privacy/interactive_privacy_questionnaire_langchain.py` | 1115 |
| `start_privacy_questionnaire` | Function | `backend/buddlyai/Routes/PrivacyController.py` | 64 |
| `get_privacy_questionnaire_progress` | Function | `backend/buddlyai/Routes/PrivacyController.py` | 180 |
| `get_privacy_questionnaire_summary` | Function | `backend/buddlyai/Routes/PrivacyController.py` | 212 |
| `respondQuestion` | Function | `securacyfrontend/lib/questions.ts` | 348 |
| `mapAnswersToAnalysisData` | Function | `securacyfrontend/app/home/(bots)/privacy/page.tsx` | 510 |
| `getAnswerForTopic` | Function | `securacyfrontend/app/home/(bots)/privacy/page.tsx` | 531 |
| `handleNextQuestion` | Function | `securacyfrontend/app/home/(bots)/privacy/page.tsx` | 588 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `PrivacyBot → DecodeJwt` | cross_community | 8 |
| `AppsecBot → DecodeJwt` | cross_community | 8 |
| `HandleNextQuestion → DecodeJwt` | cross_community | 7 |
| `HandleNextQuestion → DecodeJwt` | cross_community | 7 |
| `PrivacyBot → FindNodeIdByName` | cross_community | 6 |
| `PrivacyBot → _syncUserWithBackend` | cross_community | 6 |
| `PrivacyBot → NormalizeNodeType` | cross_community | 5 |
| `PrivacyBot → IsKnownIntegration` | cross_community | 5 |
| `PrivacyBot → NameToId` | cross_community | 5 |
| `PrivacyBot → StopSessionMonitoring` | cross_community | 5 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Hooks | 2 calls |
| Services | 1 calls |
| Appsec | 1 calls |
| Dfd | 1 calls |

## How to Explore

1. `gitnexus_context({name: "add_exchange"})` — see callers and callees
2. `gitnexus_query({query: "privacy"})` — find related execution flows
3. Read key files listed above for implementation details
