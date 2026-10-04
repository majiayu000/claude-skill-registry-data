---
name: reactflow-expert
license: Apache-2.0
description: Builds DAG visualizations using ReactFlow v12 with custom nodes, ELKjs auto-layout, Zustand state management, and live state updates via WebSocket. Use when implementing workflow visualization dashboards, creating custom agent node components, integrating ELK layout algorithms, or wiring execution state into React components. Activate on "ReactFlow", "workflow visualization", "DAG visualization", "ELKjs", "custom nodes", "node-based editor", "graph visualization". NOT for writing Mermaid diagrams (use mermaid-graph-writer), general React development, or static diagram rendering.
allowed-tools: Read,Write,Edit,Bash,Grep,Glob
metadata:
  tags:
    - reactflow
    - workflow-visualization
    - dag-visualization
  pairs-with:
    - skill: websocket-streaming
      reason: Live DAG state updates flow through WebSocket connections to ReactFlow visualizations
    - skill: human-gate-designer
      reason: Human approval gates are rendered as interactive ReactFlow custom nodes
    - skill: task-decomposer
      reason: Decomposed task DAGs are visualized as ReactFlow node graphs with ELKjs layout
category: Frontend & UI
tags:
  - reactflow
  - node-editor
  - graph-visualization
  - interactive
  - react
---

# ReactFlow Expert

Builds DAG visualizations using ReactFlow v12 with custom agent nodes, ELKjs auto-layout, Zustand state management, and live execution state updates.

## Decision Points

### State Management Strategy Selection
```
Graph Size <= 50 nodes?
├─ YES: Use useNodesState/useEdgesState hooks (simpler)
└─ NO: Use Zustand store
    ├─ Real-time updates required? → Include WebSocket integration
    ├─ Multi-component access? → Global Zustand store
    └─ Complex interactions? → Add action methods (updateNodeData, bulkUpdate)
```

### Layout Algorithm by DAG Shape
```
Node Count:
├─ < 20 nodes: Use 'layered' algorithm with direction='DOWN'
├─ 20-100 nodes: Use 'layered' with direction='RIGHT' 
├─ > 100 nodes: Use 'stress' algorithm (better for large graphs)
└─ Highly connected (edges > 2x nodes): Use 'force' algorithm

Aspect Ratio:
├─ Wide dashboard: direction='RIGHT'
├─ Tall sidebar: direction='DOWN' 
└─ Square viewport: Let ELK choose optimal direction
```

### Custom Node Complexity Decision
```
Node Data Fields:
├─ Only status + name: Use built-in node types with custom styling
├─ 3-5 fields: Custom node with simple layout
├─ 6+ fields or nested data: Custom node with collapsible sections
└─ Interactive elements: Custom node + "nodrag" className on controls
```

### Sync Strategy for Live Updates
```
Update Frequency:
├─ Real-time (< 1s): WebSocket with optimistic updates
├─ Frequent (1-10s): WebSocket with batching
├─ Periodic (> 10s): HTTP polling
└─ User-triggered: Manual refresh button

Data Size:
├─ Full DAG < 1MB: Send complete state
├─ Large DAG: Send delta updates (node ID + changed fields)
└─ Huge DAG: Implement viewport-based loading
```

## Failure Modes

### **Infinite Re-render Loop** 
**Symptom**: Browser tab freezes, React DevTools shows constant re-renders
**Detection**: If `nodeTypes` object is defined inside component body
**Fix**: Move `nodeTypes` outside component or wrap in `useMemo`

### **Stale State Updates**
**Symptom**: Node status changes don't appear visually, but store updates correctly
**Detection**: If mutating existing node objects instead of creating new ones
**Fix**: Always spread objects: `{ ...node, data: { ...node.data, newField } }`

### **Layout Thrashing**
**Symptom**: Nodes jump around constantly, poor performance with live updates
**Detection**: If ELK layout runs on every state change instead of topology changes
**Fix**: Only trigger layout when nodes/edges are added/removed, not data updates

### **Handle Positioning Mismatch**
**Symptom**: Edges connect to wrong positions or don't connect at all
**Detection**: If using v11 position properties (`xPos`, `yPos`) in v12
**Fix**: Update to v12 properties: `positionAbsoluteX`, `positionAbsoluteY`

### **Drag Interference**
**Symptom**: Buttons/inputs inside custom nodes trigger node dragging
**Detection**: If interactive elements don't have proper event handling
**Fix**: Add `className="nodrag"` to all buttons, inputs, selects inside nodes

## Worked Examples

### Complete WebSocket DAG Sync → ELK Layout → Custom Node Render

**Scenario**: Build a live workflow dashboard showing agent execution status

**Step 1: Setup Zustand Store with WebSocket Integration**
```typescript
const useDAGStore = create<DAGStore>((set, get) => ({
  nodes: [],
  edges: [],
  onNodesChange: (changes) => set({ nodes: applyNodeChanges(changes, get().nodes) }),
  onEdgesChange: (changes) => set({ edges: applyEdgeChanges(changes, get().edges) }),
  updateNodeData: (nodeId, data) => {
    // EXPERT MOVE: Create new object to trigger React re-render
    set({
      nodes: get().nodes.map((n) =>
        n.id === nodeId ? { ...n, data: { ...n.data, ...data } } : n
      ),
    });
  },
}));
```

**Step 2: WebSocket Handler (Novice Miss: Updating in place)**
```typescript
function useDAGStream(dagId: string) {
  const updateNodeData = useDAGStore((s) => s.updateNodeData);
  
  useEffect(() => {
    const ws = new WebSocket(`ws://api/dag/${dagId}/stream`);
    ws.onmessage = (event) => {
      const update = JSON.parse(event.data);
      if (update.type === 'node_status') {
        // EXPERT: Only update data, don't re-layout
        updateNodeData(update.nodeId, { 
          status: update.status, 
          metrics: update.metrics 
        });
      } else if (update.type === 'topology_change') {
        // EXPERT: Only NOW do we re-layout
        triggerLayout();
      }
    };
  }, [dagId, updateNodeData]);
}
```

**Step 3: ELK Layout with Performance Optimization**
```typescript
const useAutoLayout = () => {
  const { fitView } = useReactFlow();
  const { nodes, edges, setNodes } = useDAGStore();
  
  return useCallback(async (direction = 'DOWN') => {
    // EXPERT: Check node count and choose algorithm
    const algorithm = nodes.length > 100 ? 'stress' : 'layered';
    
    const layouted = await elk.layout({
      id: 'root',
      layoutOptions: {
        'elk.algorithm': algorithm,
        'elk.direction': direction,
        'elk.spacing.nodeNode': nodes.length > 50 ? '60' : '80',
      },
      children: nodes.map((n) => ({
        ...n,
        // EXPERT: Pass measured dimensions to prevent layout jumps
        width: n.measured?.width ?? 220,
        height: n.measured?.height ?? 120,
      })),
      edges,
    });
    
    const positioned = layouted.children!.map((elkN) => ({
      ...nodes.find((n) => n.id === elkN.id)!,
      position: { x: elkN.x!, y: elkN.y! },
    }));
    
    setNodes(positioned);
    // EXPERT: Defer fitView until after DOM update
    requestAnimationFrame(() => fitView());
  }, [nodes, edges, setNodes, fitView]);
};
```

**Step 4: Custom Agent Node with Status Colors**
```typescript
// EXPERT: Define outside component to prevent re-registration
const nodeTypes = { agentNode: AgentNode };

function AgentNode({ data }: NodeProps) {
  return (
    <div className={`agent-node status-${data.status}`}>
      <Handle type="target" position={Position.Top} />
      <div className="node-header">
        <span className={`status-dot ${data.status}`} />
        <span>{data.role}</span>
      </div>
      {data.status === 'running' && data.progress && (
        <div className="progress-bar">
          <div style={{ width: `${data.progress}%` }} />
        </div>
      )}
      {/* EXPERT: Interactive elements need nodrag */}
      <button className="nodrag" onClick={() => pauseAgent(data.id)}>
        Pause
      </button>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}
```

**Performance Tradeoffs Demonstrated**:
- **Zustand vs useState**: Zustand handles 100+ node updates without re-rendering parent
- **ELK algorithm choice**: 'layered' fast for < 100 nodes, 'stress' for larger graphs
- **WebSocket batching**: Group status updates to avoid layout thrashing

## Quality Gates

### Functional Validation
- [ ] ReactFlow component renders without console errors
- [ ] All custom node types appear in nodeTypes registry
- [ ] ELK layout completes within 2 seconds for target node count
- [ ] WebSocket connections establish and receive test messages
- [ ] Node data updates trigger visual changes within 200ms

### Performance Thresholds
- [ ] Initial render completes within 1 second for 50 nodes
- [ ] Layout computation finishes within 3 seconds for 100 nodes
- [ ] Memory usage stays under 100MB for 200-node graphs
- [ ] Frame rate maintains 30fps during zoom/pan operations
- [ ] WebSocket updates don't cause visible stuttering

### Visual Quality Checks
- [ ] Edges connect to correct handle positions (not node centers)
- [ ] Node labels remain readable at 50% zoom level
- [ ] Status colors match design system specifications
- [ ] Interactive elements (buttons, inputs) don't trigger node dragging
- [ ] fitView() centers graph with appropriate padding margins

### Accessibility Requirements
- [ ] All interactive nodes have proper ARIA labels
- [ ] Keyboard navigation works for node selection
- [ ] Color-based status indicators have text/icon alternatives
- [ ] Focus indicators visible on custom node components
- [ ] Screen reader announces node status changes

## NOT-FOR Boundaries

**Static Diagrams**: For Mermaid flowcharts or architectural diagrams, use `mermaid-graph-writer` instead. ReactFlow is for interactive, live-updating visualizations.

**Simple Charts**: For bar charts, line graphs, or pie charts, use dedicated charting libraries (recharts, d3) instead. ReactFlow is specifically for node-edge graphs.

**General React Development**: For standard React components, forms, or layouts, use general React skills instead. This skill is ReactFlow-specific.

**3D Visualizations**: For 3D network graphs or spatial layouts, use three.js or WebGL libraries instead. ReactFlow is 2D-only.

**Mobile-First Apps**: For touch-first mobile interfaces, consider native gestures instead. ReactFlow is optimized for mouse/trackpad interaction.

**Real-time Collaboration**: For multi-user editing like Figma, use specialized real-time sync libraries instead. ReactFlow handles read-only live updates well but not collaborative editing.