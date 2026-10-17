---
name: system-design-visualizer-tool
description: Transform static system design diagrams into interactive, explorable visualizations using AI-powered analysis and React Flow.
triggers:
  - "convert my architecture diagram to interactive visualization"
  - "transform system design image into mermaid diagram"
  - "make my flowchart interactive with react flow"
  - "analyze this system design diagram with ai"
  - "create explorable visualization from architecture image"
  - "generate interactive graph from system design"
  - "turn static diagram into clickable components"
  - "visualize system architecture interactively"
---

# System Design Visualizer Tool

> Skill by [ara.so](https://ara.so) — Design Skills collection.

System Design Visualizer is an AI-powered tool that transforms static system design images (architecture diagrams, flowcharts, etc.) into interactive, explorable visualizations. It uses OpenAI's GPT-4o Vision to analyze uploaded images, generates Mermaid.js diagrams, and converts them into interactive React Flow graphs with detailed component information.

## Installation

```bash
git clone https://github.com/mallahyari/system-design-visualizer.git
cd system-design-visualizer
npm install
```

### Environment Configuration

Create a `.env` file in the root directory:

```env
VITE_OPENAI_API_KEY=your_openai_api_key_here
```

**Note**: If no API key is provided, the app runs in Mock Mode with sample data.

### Start Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:5173`.

## Core Architecture

The project uses a React + Vite setup with three main visualization stages:

1. **Image Upload**: Accepts system design diagrams
2. **Mermaid Generation**: AI converts image to Mermaid.js code
3. **Interactive Graph**: Converts Mermaid to React Flow visualization

## Key Components

### Image Upload Component

```javascript
import { useState } from 'react';
import { Upload } from 'lucide-react';

function ImageUploader({ onImageUpload }) {
  const [isDragging, setIsDragging] = useState(false);

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => onImageUpload(e.target.result);
      reader.readAsDataURL(file);
    }
  };

  return (
    <div
      onDrop={handleDrop}
      onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
      onDragLeave={() => setIsDragging(false)}
      className={`border-2 border-dashed rounded-lg p-12 text-center ${
        isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
      }`}
    >
      <Upload className="mx-auto h-12 w-12 text-gray-400" />
      <p className="mt-4 text-sm text-gray-600">
        Drag and drop your system design image here
      </p>
    </div>
  );
}
```

### OpenAI Integration for Image Analysis

```javascript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: import.meta.env.VITE_OPENAI_API_KEY,
  dangerouslyAllowBrowser: true
});

async function analyzeSystemDesign(imageDataUrl) {
  const response = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [
      {
        role: "user",
        content: [
          {
            type: "text",
            text: "Analyze this system design diagram and generate a Mermaid.js diagram representing the architecture. Include all components, connections, and relationships."
          },
          {
            type: "image_url",
            image_url: { url: imageDataUrl }
          }
        ]
      }
    ],
    max_tokens: 2000
  });

  return response.choices[0].message.content;
}
```

### Mermaid to React Flow Conversion

```javascript
function parseMermaidToReactFlow(mermaidCode) {
  const nodes = [];
  const edges = [];
  
  // Parse mermaid syntax (simplified example)
  const lines = mermaidCode.split('\n');
  const nodeMap = new Map();
  let nodeId = 0;
  
  lines.forEach((line, index) => {
    // Match patterns like: A[Load Balancer] --> B[Web Server]
    const connectionMatch = line.match(/(\w+)\[(.*?)\]\s*-->\s*(\w+)\[(.*?)\]/);
    
    if (connectionMatch) {
      const [_, sourceId, sourceLabel, targetId, targetLabel] = connectionMatch;
      
      // Add source node if not exists
      if (!nodeMap.has(sourceId)) {
        nodes.push({
          id: sourceId,
          type: 'custom',
          position: { x: 100, y: nodeId * 100 },
          data: { label: sourceLabel }
        });
        nodeMap.set(sourceId, true);
        nodeId++;
      }
      
      // Add target node if not exists
      if (!nodeMap.has(targetId)) {
        nodes.push({
          id: targetId,
          type: 'custom',
          position: { x: 400, y: nodeId * 100 },
          data: { label: targetLabel }
        });
        nodeMap.set(targetId, true);
        nodeId++;
      }
      
      // Add edge
      edges.push({
        id: `${sourceId}-${targetId}`,
        source: sourceId,
        target: targetId,
        type: 'smoothstep'
      });
    }
  });
  
  return { nodes, edges };
}
```

### Interactive React Flow Graph

```javascript
import ReactFlow, { 
  MiniMap, 
  Controls, 
  Background,
  useNodesState,
  useEdgesState 
} from 'reactflow';
import 'reactflow/dist/style.css';

function InteractiveGraph({ mermaidCode }) {
  const { nodes: initialNodes, edges: initialEdges } = parseMermaidToReactFlow(mermaidCode);
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [selectedNode, setSelectedNode] = useState(null);

  const onNodeClick = async (event, node) => {
    setSelectedNode(node);
    
    // Get detailed info about the component using AI
    const details = await getComponentDetails(node.data.label);
    setSelectedNode({ ...node, details });
  };

  return (
    <div className="h-screen">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={onNodeClick}
        fitView
      >
        <Background />
        <Controls />
        <MiniMap />
      </ReactFlow>
      
      {selectedNode && (
        <ComponentDetailsPanel node={selectedNode} />
      )}
    </div>
  );
}
```

### Component Details Analysis

```javascript
async function getComponentDetails(componentName) {
  const response = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [
      {
        role: "user",
        content: `Given a system design component named "${componentName}", provide:
1. Likely technology stack
2. Primary role in the architecture
3. Common configuration considerations
4. Best practices

Format as JSON with keys: technologies, role, configuration, bestPractices`
      }
    ],
    max_tokens: 500
  });

  return JSON.parse(response.choices[0].message.content);
}
```

### Custom Node Component

```javascript
import { Handle, Position } from 'reactflow';

function CustomNode({ data, selected }) {
  return (
    <div className={`px-4 py-2 rounded-lg border-2 bg-white shadow-md ${
      selected ? 'border-blue-500' : 'border-gray-300'
    }`}>
      <Handle type="target" position={Position.Top} />
      <div className="font-semibold text-sm">{data.label}</div>
      {data.description && (
        <div className="text-xs text-gray-500 mt-1">{data.description}</div>
      )}
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

const nodeTypes = {
  custom: CustomNode
};
```

## Mock Mode (No API Key)

When running without an OpenAI API key, use mock data:

```javascript
function getMockMermaidDiagram() {
  return `graph TB
    A[Load Balancer] --> B[Web Server 1]
    A --> C[Web Server 2]
    B --> D[Application Server]
    C --> D
    D --> E[Database Master]
    D --> F[Cache Layer]
    E --> G[Database Replica]`;
}

function getMockComponentDetails(componentName) {
  const mockDetails = {
    'Load Balancer': {
      technologies: ['NGINX', 'HAProxy', 'AWS ELB'],
      role: 'Distributes incoming traffic across multiple servers',
      configuration: 'Health checks, SSL termination, routing rules',
      bestPractices: 'Use multiple availability zones, enable auto-scaling'
    },
    // Add more mock data as needed
  };
  
  return mockDetails[componentName] || {
    technologies: ['Generic'],
    role: 'System component',
    configuration: 'Standard setup',
    bestPractices: 'Follow industry standards'
  };
}
```

## Full App Integration Example

```javascript
import { useState } from 'react';
import ReactFlow from 'reactflow';
import mermaid from 'mermaid';

function App() {
  const [step, setStep] = useState('upload'); // upload, mermaid, interactive
  const [imageData, setImageData] = useState(null);
  const [mermaidCode, setMermaidCode] = useState('');
  const [flowData, setFlowData] = useState({ nodes: [], edges: [] });

  const handleImageUpload = async (dataUrl) => {
    setImageData(dataUrl);
    setStep('mermaid');
    
    // Generate Mermaid diagram
    const code = await analyzeSystemDesign(dataUrl);
    setMermaidCode(code);
  };

  const handleConvertToInteractive = () => {
    const data = parseMermaidToReactFlow(mermaidCode);
    setFlowData(data);
    setStep('interactive');
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <header className="p-4 border-b border-gray-800">
        <h1 className="text-2xl font-bold">System Design Visualizer</h1>
      </header>
      
      <main className="p-8">
        {step === 'upload' && (
          <ImageUploader onImageUpload={handleImageUpload} />
        )}
        
        {step === 'mermaid' && (
          <div className="grid grid-cols-2 gap-4">
            <div>
              <h2 className="text-xl mb-4">Original Image</h2>
              <img src={imageData} alt="Original" className="w-full" />
            </div>
            <div>
              <h2 className="text-xl mb-4">Mermaid Diagram</h2>
              <pre className="bg-gray-800 p-4 rounded overflow-auto">
                {mermaidCode}
              </pre>
              <button 
                onClick={handleConvertToInteractive}
                className="mt-4 px-6 py-2 bg-blue-600 rounded hover:bg-blue-700"
              >
                Convert to Interactive
              </button>
            </div>
          </div>
        )}
        
        {step === 'interactive' && (
          <InteractiveGraph mermaidCode={mermaidCode} />
        )}
      </main>
    </div>
  );
}
```

## Common Patterns

### Copying Mermaid Code to Clipboard

```javascript
import { Copy } from 'lucide-react';

function CopyButton({ text }) {
  const handleCopy = () => {
    navigator.clipboard.writeText(text);
    // Show toast notification
  };

  return (
    <button 
      onClick={handleCopy}
      className="flex items-center gap-2 px-3 py-1 bg-gray-700 rounded hover:bg-gray-600"
    >
      <Copy size={16} />
      Copy Code
    </button>
  );
}
```

### Auto-Layout for React Flow Nodes

```javascript
import dagre from 'dagre';

function getLayoutedElements(nodes, edges) {
  const dagreGraph = new dagre.graphlib.Graph();
  dagreGraph.setDefaultEdgeLabel(() => ({}));
  dagreGraph.setGraph({ rankdir: 'TB' });

  nodes.forEach((node) => {
    dagreGraph.setNode(node.id, { width: 150, height: 50 });
  });

  edges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target);
  });

  dagre.layout(dagreGraph);

  const layoutedNodes = nodes.map((node) => {
    const nodeWithPosition = dagreGraph.node(node.id);
    return {
      ...node,
      position: {
        x: nodeWithPosition.x - 75,
        y: nodeWithPosition.y - 25
      }
    };
  });

  return { nodes: layoutedNodes, edges };
}
```

## Troubleshooting

### OpenAI API Errors

- **401 Unauthorized**: Check that `VITE_OPENAI_API_KEY` is correctly set in `.env`
- **429 Rate Limit**: Implement retry logic with exponential backoff
- **Image too large**: Resize images before upload (max 20MB)

### Mermaid Parsing Issues

- Ensure generated Mermaid code uses supported syntax (graph TB, graph LR)
- Validate node IDs are alphanumeric without special characters
- Check for balanced brackets in node labels

### React Flow Rendering

- Ensure parent container has explicit height/width
- Import `reactflow/dist/style.css` for proper styling
- Use `fitView` prop to auto-center the graph on mount

### Build Issues

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Check for peer dependency issues
npm list
```

## API Reference

### Main Functions

- `analyzeSystemDesign(imageDataUrl)`: Converts image to Mermaid code
- `parseMermaidToReactFlow(mermaidCode)`: Converts Mermaid to React Flow format
- `getComponentDetails(componentName)`: Gets AI-generated component details
- `getLayoutedElements(nodes, edges)`: Auto-layouts graph nodes

### Environment Variables

- `VITE_OPENAI_API_KEY`: OpenAI API key for AI analysis (optional for mock mode)
