---
name: bpmn-creator
description: Create valid BPMN 2.0 XML with complete diagram interchange (DI) from process descriptions, ASCII diagrams or flowcharts. Use for BPMN creation, process modeling, workflow diagrams. Output opens in Camunda Modeler or bpmn.io.
---

# BPMN Creator

Create valid BPMN 2.0 XML diagrams with complete visual layout information. Output complies with the OMG BPMN 2.0 spec, opens in Camunda Modeler or bpmn.io, and supports collaborations (pools, lanes, message flows).

## Workflow

1. **Understand the process.** Identify participants (pools), lanes, activities and sub-processes, events (start, intermediate, end), gateways (exclusive, parallel, inclusive), sequence and message flows, data objects and stores.
2. **Design the structure.** Group activities by participant and lane, identify message exchanges, map the sequence flow of each process, note parallel and conditional branches.
3. **Generate the XML.** Start from `references/example-process.bpmn` and follow the patterns in `references/xml-and-layout.md` (root definitions, collaboration, process, gateways, event types, task types, DI shapes and edges, layout dimensions).
4. **Validate.** Run `python3 scripts/validate_bpmn.py <file.bpmn>`, then walk the checklist below.

## Non-negotiables

- **Always include complete DI** (`bpmndi:BPMNDiagram`, `BPMNPlane`, one `BPMNShape` per node, pool and lane, one `BPMNEdge` per flow). Without DI the diagram does not display.
- Standard sizes: start/end events 36x36, activities 100x80, gateways 50x50. Use multiples of 10 for waypoints.
- Save files with the `.bpmn` extension to `/mnt/user-data/outputs/` and provide a download link.

## Validation checklist

- [ ] All `flowNodeRef` elements match actual node IDs
- [ ] All `incoming`/`outgoing` references match sequence flow IDs
- [ ] All `sourceRef`/`targetRef` point to valid elements
- [ ] Every process element has a DI shape or edge
- [ ] Every DI element references a valid element via `bpmnElement`
- [ ] Shapes do not overlap and sit inside their pool or lane
- [ ] Waypoints create valid connections, in logical order
- [ ] Start events have no incoming flows, end events no outgoing flows
- [ ] Gateways have at least 2 outgoing (split) or 2 incoming (join) flows
- [ ] All IDs are unique, namespaces are declared on `<definitions>`

## Troubleshooting

- "No diagram to display": the DI section is missing or incomplete. Check every element has a shape or edge and every `bpmnElement` is a valid ID.
- Import errors: check namespace declarations, ID uniqueness and element nesting (the process contains the flow nodes).
- Layout issues: check bounds overlap, waypoint order and pool/lane containment.

## References

- `references/xml-and-layout.md`: XML skeletons, DI shape and edge snippets, layout guidelines, common patterns.
- `references/bpmn-elements.md`: full BPMN 2.0 element reference.
- `references/example-process.bpmn`: working multi-participant example (5 user pools with lanes, 3 system pools, timer/message/standard events, user and service tasks, exclusive gateways, message flows, full DI).
