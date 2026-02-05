---
name: bpmn-diagram
description: Converts BPMN 2.0 XML to PNG diagram images. Use when user provides BPMN XML content or file path and asks to visualize, render, or create a diagram from a BPMN process definition.
---

# BPMN Diagram Skill

This skill converts BPMN 2.0 XML into PNG diagram images using the bpmn-js rendering toolkit.

## Prerequisites

Before first use, ensure dependencies are installed:

```bash
cd ~/.claude/skills/bpmn-diagram/scripts && ./setup.sh
```

Or for project-local skills:

```bash
cd .claude/skills/bpmn-diagram/scripts && ./setup.sh
```

## Usage

### Input Formats

The skill accepts BPMN 2.0 XML in two ways:

1. **File path**: Path to an existing `.bpmn` or `.xml` file
2. **Inline XML**: Raw BPMN XML content provided directly

### Rendering a Diagram

**From a file:**

```bash
node scripts/render-bpmn.js /path/to/diagram.bpmn /path/to/output.png
```

**From inline XML:**

1. First, write the BPMN XML to a temporary file
2. Then run the render script
3. The PNG will be created at the specified output path

### Script Options

| Option | Description | Default |
|--------|-------------|---------|
| `--scale=N` | Image scale factor (e.g., 2 for 2x resolution) | 1 |
| `--min-dimensions=WxH` | Minimum output dimensions in pixels | 800x600 |

**Example with options:**

```bash
node scripts/render-bpmn.js input.bpmn output.png --scale=2 --min-dimensions=1200x800
```

## Workflow

When a user requests a BPMN diagram:

1. **Identify the input**: Determine if XML is inline or in a file
2. **Validate the XML**: Check for valid BPMN 2.0 structure
   - Must have `<definitions>` root element with BPMN namespace
   - Should contain `<bpmndi:BPMNDiagram>` for visual layout
3. **Prepare input file**: If inline XML, write to a temp `.bpmn` file
4. **Execute render script**: Run `node scripts/render-bpmn.js`
5. **Report result**: Provide the output PNG path to the user

## BPMN 2.0 XML Structure

Valid BPMN 2.0 XML must follow this structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<definitions
    xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL"
    xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
    xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
    xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
    id="Definitions_1"
    targetNamespace="http://bpmn.io/schema/bpmn">

  <!-- Process definition -->
  <process id="Process_1" isExecutable="false">
    <!-- BPMN elements: events, tasks, gateways, flows -->
  </process>

  <!-- Diagram interchange (visual layout) -->
  <bpmndi:BPMNDiagram id="BPMNDiagram_1">
    <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="Process_1">
      <!-- Shape and edge definitions for visual rendering -->
    </bpmndi:BPMNPlane>
  </bpmndi:BPMNDiagram>

</definitions>
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "Not valid XML" | Malformed XML syntax | Check XML structure, escape special characters |
| "Not BPMN 2.0 format" | Missing `<definitions>` root | Ensure proper BPMN namespace and root element |
| "No diagram layout" | Missing `<bpmndi:BPMNDiagram>` | Add diagram interchange section or use auto-layout |
| "Render failed" | Canvas/dependencies issue | Ensure setup.sh was run, check system dependencies |
| "File not found" | Invalid input path | Verify file path exists |

## Known Limitations

This skill uses a pure Node.js rendering approach with jsdom and canvas, which has some limitations compared to browser-based rendering:

1. **SVG Transform Positioning**: Some complex transform operations may not be perfectly positioned
2. **Text Rendering**: Font rendering depends on system fonts available
3. **Complex Diagrams**: Very large or complex diagrams may have rendering artifacts

For production use with complex diagrams, consider:
- Using `bpmn-to-image` with Puppeteer (requires Chrome/Chromium)
- Running the rendering in an actual browser environment

## Common BPMN Elements

See `references/bpmn-elements.md` for a complete reference of supported BPMN 2.0 elements.

### Quick Reference

**Events:**
- `startEvent`, `endEvent`, `intermediateCatchEvent`, `intermediateThrowEvent`

**Activities:**
- `task`, `userTask`, `serviceTask`, `scriptTask`, `sendTask`, `receiveTask`
- `subProcess`, `callActivity`

**Gateways:**
- `exclusiveGateway` (XOR), `parallelGateway` (AND), `inclusiveGateway` (OR)
- `eventBasedGateway`, `complexGateway`

**Flows:**
- `sequenceFlow`, `messageFlow`, `association`

**Swimlanes:**
- `participant` (Pool), `lane`

## Example

**Input (simple-process.bpmn):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL"
             xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
             xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
             id="Definitions_1">
  <process id="Process_1" isExecutable="false">
    <startEvent id="Start_1" name="Start"/>
    <task id="Task_1" name="Do Something"/>
    <endEvent id="End_1" name="End"/>
    <sequenceFlow id="Flow_1" sourceRef="Start_1" targetRef="Task_1"/>
    <sequenceFlow id="Flow_2" sourceRef="Task_1" targetRef="End_1"/>
  </process>
  <bpmndi:BPMNDiagram id="BPMNDiagram_1">
    <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="Process_1">
      <bpmndi:BPMNShape id="Start_1_di" bpmnElement="Start_1">
        <dc:Bounds x="152" y="102" width="36" height="36"/>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Task_1_di" bpmnElement="Task_1">
        <dc:Bounds x="240" y="80" width="100" height="80"/>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="End_1_di" bpmnElement="End_1">
        <dc:Bounds x="392" y="102" width="36" height="36"/>
      </bpmndi:BPMNShape>
      <bpmndi:BPMNEdge id="Flow_1_di" bpmnElement="Flow_1">
        <di:waypoint x="188" y="120"/>
        <di:waypoint x="240" y="120"/>
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Flow_2_di" bpmnElement="Flow_2">
        <di:waypoint x="340" y="120"/>
        <di:waypoint x="392" y="120"/>
      </bpmndi:BPMNEdge>
    </bpmndi:BPMNPlane>
  </bpmndi:BPMNDiagram>
</definitions>
```

**Command:**

```bash
node scripts/render-bpmn.js simple-process.bpmn simple-process.png
```

**Output:** `simple-process.png` - A PNG image of the rendered BPMN diagram
