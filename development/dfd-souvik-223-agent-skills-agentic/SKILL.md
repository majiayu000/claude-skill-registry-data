---
name: dfd
description: "Skill for the Dfd area of Securacy. 58 symbols across 7 files."
---

# Dfd

58 symbols | 7 files | Cohesion: 96%

## When to Use

- Working with code in `securacyfrontend/`
- Understanding how assignBoundary, buildBoundaries, nameToId work
- Modifying dfd-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `securacyfrontend/components/dfd/DFDEditor.tsx` | pushHistory, scheduleShowUI, onNodeDragStop, onKeyDown, addNode (+13) |
| `securacyfrontend/services/dfd/jsonToIR.ts` | isKnownIntegration, assignBoundary, buildBoundaries, nameToId, findNodeIdByName (+8) |
| `securacyfrontend/services/dfd/xmlToIRParser.ts` | parseDrawioXmlToIR, inferContainmentFromGeometry, computeOverlapRatio, detectNodeType, cleanLabel (+3) |
| `securacyfrontend/services/dfd/dfdLayoutEngine.ts` | layoutDFD, assignBoundaryColumns, layoutNodesInBoundary, assignNodesToLayers, minimizeCrossings (+3) |
| `securacyfrontend/services/dfd/layoutDFDThreatModel.ts` | layoutDFDThreatModel, computeBoundingBox, addBoundary, layoutGrid, topologicalSort (+2) |
| `securacyfrontend/services/dfd/irToDataFlows.ts` | irToDataFlows, inferProtocol |
| `securacyfrontend/services/dfd/diagramService.ts` | initializeDiagram, loadDrawIo |

## Entry Points

Start here when exploring this area:

- **`assignBoundary`** (Function) — `securacyfrontend/services/dfd/jsonToIR.ts:126`
- **`buildBoundaries`** (Function) — `securacyfrontend/services/dfd/jsonToIR.ts:135`
- **`nameToId`** (Function) — `securacyfrontend/services/dfd/jsonToIR.ts:169`
- **`parseDataFlowStrings`** (Function) — `securacyfrontend/services/dfd/jsonToIR.ts:194`
- **`jsonToIR`** (Function) — `securacyfrontend/services/dfd/jsonToIR.ts:237`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `assignBoundary` | Function | `securacyfrontend/services/dfd/jsonToIR.ts` | 126 |
| `buildBoundaries` | Function | `securacyfrontend/services/dfd/jsonToIR.ts` | 135 |
| `nameToId` | Function | `securacyfrontend/services/dfd/jsonToIR.ts` | 169 |
| `parseDataFlowStrings` | Function | `securacyfrontend/services/dfd/jsonToIR.ts` | 194 |
| `jsonToIR` | Function | `securacyfrontend/services/dfd/jsonToIR.ts` | 237 |
| `deriveProtocol` | Function | `securacyfrontend/services/dfd/jsonToIR.ts` | 370 |
| `deriveAuthType` | Function | `securacyfrontend/services/dfd/jsonToIR.ts` | 395 |
| `parseThreatModelingData` | Function | `securacyfrontend/services/dfd/jsonToIR.ts` | 666 |
| `generateId` | Function | `securacyfrontend/services/dfd/jsonToIR.ts` | 724 |
| `parseLLMNestedBoundaries` | Function | `securacyfrontend/services/dfd/jsonToIR.ts` | 731 |
| `layoutDFDThreatModel` | Function | `securacyfrontend/services/dfd/layoutDFDThreatModel.ts` | 38 |
| `computeBoundingBox` | Function | `securacyfrontend/services/dfd/layoutDFDThreatModel.ts` | 93 |
| `addBoundary` | Function | `securacyfrontend/services/dfd/layoutDFDThreatModel.ts` | 112 |
| `parseDrawioXmlToIR` | Function | `securacyfrontend/services/dfd/xmlToIRParser.ts` | 11 |
| `layoutDFD` | Function | `securacyfrontend/services/dfd/dfdLayoutEngine.ts` | 118 |
| `irToDataFlows` | Function | `securacyfrontend/services/dfd/irToDataFlows.ts` | 34 |
| `pushHistory` | Function | `securacyfrontend/components/dfd/DFDEditor.tsx` | 224 |
| `scheduleShowUI` | Function | `securacyfrontend/components/dfd/DFDEditor.tsx` | 814 |
| `onNodeDragStop` | Function | `securacyfrontend/components/dfd/DFDEditor.tsx` | 837 |
| `onKeyDown` | Function | `securacyfrontend/components/dfd/DFDEditor.tsx` | 1021 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `PrivacyBot → FindNodeIdByName` | cross_community | 6 |
| `AppsecBot → FindNodeIdByName` | cross_community | 6 |
| `PrivacyBot → NormalizeNodeType` | cross_community | 5 |
| `PrivacyBot → IsKnownIntegration` | cross_community | 5 |
| `PrivacyBot → NameToId` | cross_community | 5 |
| `AppsecBot → NormalizeNodeType` | cross_community | 5 |
| `AppsecBot → IsKnownIntegration` | cross_community | 5 |
| `AppsecBot → NameToId` | cross_community | 5 |
| `HandleSaveAnalysis → FindNodeIdByName` | cross_community | 5 |
| `HandleSaveAnalysis → FindNodeIdByName` | cross_community | 5 |

## How to Explore

1. `gitnexus_context({name: "assignBoundary"})` — see callers and callees
2. `gitnexus_query({query: "dfd"})` — find related execution flows
3. Read key files listed above for implementation details
