---
name: starcraft-god-mode-ui
description: Implement a StarCraft 2 / RTS-inspired "God Mode" command interface for orchestrating autonomous systems. Use this skill when building dashboards for AI orchestration, multi-agent systems, autonomous manufacturing, robotics control, or any interface requiring real-time monitoring of multiple resources/units with command-and-control capabilities. Includes D3.js global network map for visualizing and onboarding distributed printer fleets. Applies to React 19 + TypeScript + Vite projects targeting dark sci-fi aesthetics with resource bars, minimaps, command panels, event logs, and geographic site selection.
---

# StarCraft God Mode UI

This skill implements a Real-Time Strategy (RTS) game-inspired interface for orchestrating autonomous systems. The design philosophy draws from StarCraft 2's proven patterns for managing complexity through spatial awareness, resource visualization, and hierarchical command structures.

## ADAM Install Base Overview

The ADAM (Autonomous Discovery and Advanced Manufacturing) platform will onboard a distributed network of 3D printers:

- **215 sites** across the United States
- **378 printer installations** (Studio: 243, InnX: 79, Shop: 56)
- **Priority tiers**: Tier A (highest), Tier B, Tier C for phased rollout
- **Product lines**: Shop System, Studio System, InnoventX

The Global Network Map (D3.js) enables visualization and selection of sites for onboarding. See `references/d3-global-map.md` for complete implementation and `assets/install-base-sample.json` for data structure.

## Core Philosophy: God's-Eye UX

RTS interfaces excel at autonomous system orchestration because they solve the same fundamental problem: managing many independent units/agents performing parallel tasks while maintaining situational awareness and issuing contextual commands.

### Key Principles

1. **Spatial Awareness**: Agents/units positioned on a tactical map, clustered by function
2. **Resource Dashboards**: Real-time metrics displayed as consumable resources (like lumber/gold → tokens/compute/jobs)
3. **Units as Agents**: Each autonomous agent represented as a selectable unit with status, capabilities, and commands
4. **Command Panel**: Context-sensitive actions based on current selection
5. **Event Stream**: Chronological feed of system events with filtering
6. **Hierarchical Control**: Select one, select many, issue orders to groups

## Visual Design System

### Color Palette

```css
:root {
  /* Primary dark theme */
  --bg-primary: #0a0e14;
  --bg-secondary: #121a24;
  --bg-tertiary: #1a2532;
  --bg-panel: rgba(10, 20, 30, 0.95);
  
  /* Accent colors - faction-inspired */
  --accent-primary: #00d4ff;      /* Cyan - Protoss */
  --accent-secondary: #00ff88;    /* Green - success/online */
  --accent-warning: #ffaa00;      /* Orange - caution */
  --accent-danger: #ff3366;       /* Red - error/critical */
  --accent-purple: #aa44ff;       /* Purple - AI/autonomous */
  
  /* Glows and effects */
  --glow-primary: 0 0 20px rgba(0, 212, 255, 0.4);
  --glow-success: 0 0 20px rgba(0, 255, 136, 0.4);
  --glow-warning: 0 0 20px rgba(255, 170, 0, 0.4);
  
  /* Text hierarchy */
  --text-primary: #e4e8ed;
  --text-secondary: #8899aa;
  --text-muted: #556677;
  
  /* Borders */
  --border-subtle: rgba(0, 212, 255, 0.2);
  --border-active: rgba(0, 212, 255, 0.6);
}
```

### Typography

```css
/* Use monospace for data, tech-style display fonts for headers */
--font-display: 'Orbitron', 'Audiowide', 'Rajdhani', sans-serif;
--font-body: 'Exo 2', 'Titillium Web', 'Roboto Condensed', sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', 'Source Code Pro', monospace;
```

### Border Treatments with Augmented-UI

Install augmented-ui for sci-fi clipped corners:

```bash
npm install augmented-ui
```

```css
@import 'augmented-ui/augmented-ui.min.css';

.panel {
  --aug-border-all: 1px;
  --aug-border-bg: var(--accent-primary);
  --aug-tl: 12px;
  --aug-br: 12px;
}
```

```html
<div class="panel" data-augmented-ui="tl-clip br-clip border">
  Panel content
</div>
```

## Layout Architecture

### Screen Regions

```
┌────────────────────────────────────────────────────────────────────┐
│                         RESOURCE BAR                                │
│  [Compute: ████░░ 67%] [Jobs: 14/50] [Agents: 8 Online] [Tokens: 2.3M]│
├──────────────────────────────────────────────────────┬─────────────┤
│                                                      │             │
│                                                      │   MINIMAP   │
│                    MAIN VIEWPORT                     │  (System    │
│                  (Tactical Map or                    │   Overview) │
│                   Detail View)                       │             │
│                                                      ├─────────────┤
│                                                      │  SELECTION  │
│                                                      │    INFO     │
├──────────────────────────────────────────────────────┼─────────────┤
│              EVENT LOG / CONSOLE                     │  COMMAND    │
│  [12:34:01] Job X25-001 completed                   │   PANEL     │
│  [12:34:05] Agent Nova analyzing results            │  [Actions]  │
└──────────────────────────────────────────────────────┴─────────────┘
```

### React Component Structure

```
src/
├── layouts/
│   └── GodModeLayout.tsx        # Main layout container
├── components/
│   ├── ResourceBar/
│   │   ├── ResourceBar.tsx      # Top resource metrics
│   │   ├── ResourceGauge.tsx    # Individual resource display
│   │   └── ResourceBar.css
│   ├── TacticalMap/
│   │   ├── TacticalMap.tsx      # Main viewport with unit positions
│   │   ├── UnitMarker.tsx       # Individual unit/agent marker
│   │   ├── SelectionBox.tsx     # Drag-select rectangle
│   │   └── TacticalMap.css
│   ├── Minimap/
│   │   ├── Minimap.tsx          # System overview minimap
│   │   └── Minimap.css
│   ├── SelectionPanel/
│   │   ├── SelectionPanel.tsx   # Info about selected units
│   │   ├── UnitCard.tsx         # Single unit detail card
│   │   └── SelectionPanel.css
│   ├── CommandPanel/
│   │   ├── CommandPanel.tsx     # Context-sensitive actions
│   │   ├── CommandButton.tsx    # Individual action button
│   │   └── CommandPanel.css
│   ├── EventLog/
│   │   ├── EventLog.tsx         # Scrolling event stream
│   │   ├── EventEntry.tsx       # Single event row
│   │   └── EventLog.css
│   └── shared/
│       ├── Panel.tsx            # Reusable augmented panel
│       ├── StatusIndicator.tsx  # Online/offline/busy dots
│       ├── ProgressBar.tsx      # Styled progress bars
│       └── GlowButton.tsx       # Sci-fi styled button
└── hooks/
    ├── useSelection.ts          # Multi-select state management
    ├── useKeyboardShortcuts.ts  # Hotkey bindings
    └── useRealTimeData.ts       # WebSocket data subscription
```

## Component Implementation Patterns

### 1. Resource Bar

Displays system resources like RTS lumber/gold:

```tsx
interface Resource {
  id: string;
  label: string;
  current: number;
  max: number;
  unit?: string;
  status: 'normal' | 'warning' | 'critical';
}

const ResourceBar: React.FC<{ resources: Resource[] }> = ({ resources }) => (
  <div className="resource-bar" data-augmented-ui="bl-clip br-clip border">
    {resources.map(r => (
      <ResourceGauge key={r.id} {...r} />
    ))}
  </div>
);
```

```css
.resource-bar {
  display: flex;
  gap: 2rem;
  padding: 0.75rem 1.5rem;
  background: var(--bg-panel);
  --aug-border-all: 1px;
  --aug-border-bg: var(--border-subtle);
  --aug-bl: 8px;
  --aug-br: 8px;
}

.resource-gauge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-family: var(--font-mono);
}

.resource-gauge__bar {
  width: 120px;
  height: 8px;
  background: var(--bg-tertiary);
  border-radius: 2px;
  overflow: hidden;
}

.resource-gauge__fill {
  height: 100%;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
  transition: width 0.3s ease;
  box-shadow: var(--glow-primary);
}

.resource-gauge--warning .resource-gauge__fill {
  background: var(--accent-warning);
  box-shadow: var(--glow-warning);
}
```

### 2. Tactical Map with Selectable Units

```tsx
interface Agent {
  id: string;
  name: string;
  type: 'printer' | 'orchestrator' | 'analyzer' | 'worker';
  position: { x: number; y: number };
  status: 'idle' | 'working' | 'error' | 'offline';
  currentTask?: string;
}

const TacticalMap: React.FC<{
  agents: Agent[];
  selectedIds: Set<string>;
  onSelect: (ids: string[]) => void;
}> = ({ agents, selectedIds, onSelect }) => {
  const [selectionBox, setSelectionBox] = useState<Rect | null>(null);
  
  return (
    <div 
      className="tactical-map"
      onMouseDown={handleDragStart}
      onMouseMove={handleDragMove}
      onMouseUp={handleDragEnd}
    >
      {/* Grid overlay for spatial reference */}
      <svg className="tactical-map__grid">
        <defs>
          <pattern id="grid" width="50" height="50" patternUnits="userSpaceOnUse">
            <path d="M 50 0 L 0 0 0 50" fill="none" stroke="var(--border-subtle)" strokeWidth="0.5"/>
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />
      </svg>
      
      {/* Agent markers */}
      {agents.map(agent => (
        <UnitMarker
          key={agent.id}
          agent={agent}
          isSelected={selectedIds.has(agent.id)}
          onClick={() => onSelect([agent.id])}
        />
      ))}
      
      {/* Selection box */}
      {selectionBox && <SelectionBox rect={selectionBox} />}
    </div>
  );
};
```

```css
.tactical-map {
  position: relative;
  flex: 1;
  background: 
    radial-gradient(circle at 30% 40%, rgba(0, 212, 255, 0.05) 0%, transparent 50%),
    var(--bg-primary);
  overflow: hidden;
}

.unit-marker {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: transform 0.2s;
}

.unit-marker:hover {
  transform: scale(1.1);
}

.unit-marker--selected {
  filter: drop-shadow(var(--glow-primary));
}

.unit-marker__icon {
  width: 48px;
  height: 48px;
  border: 2px solid var(--accent-primary);
  border-radius: 4px;
  background: var(--bg-panel);
  display: flex;
  align-items: center;
  justify-content: center;
}

.unit-marker--selected .unit-marker__icon {
  border-color: var(--accent-secondary);
  box-shadow: var(--glow-success);
}

.unit-marker__health {
  width: 100%;
  height: 4px;
  background: var(--bg-tertiary);
  margin-top: 4px;
}

.unit-marker__health-fill {
  height: 100%;
  background: var(--accent-secondary);
}
```

### 3. Command Panel (Context-Sensitive)

```tsx
interface Command {
  id: string;
  label: string;
  icon: React.ReactNode;
  hotkey?: string;
  disabled?: boolean;
  variant?: 'primary' | 'danger' | 'warning';
}

const CommandPanel: React.FC<{
  selection: Agent[];
  onCommand: (commandId: string, targets: Agent[]) => void;
}> = ({ selection, onCommand }) => {
  const commands = useMemo(() => getCommandsForSelection(selection), [selection]);
  
  return (
    <div className="command-panel" data-augmented-ui="tl-clip tr-clip border">
      <div className="command-panel__header">
        COMMANDS {selection.length > 0 && `(${selection.length})`}
      </div>
      <div className="command-panel__grid">
        {commands.map(cmd => (
          <CommandButton
            key={cmd.id}
            command={cmd}
            onClick={() => onCommand(cmd.id, selection)}
          />
        ))}
      </div>
    </div>
  );
};
```

```css
.command-panel {
  --aug-tl: 8px;
  --aug-tr: 8px;
  --aug-border-all: 1px;
  --aug-border-bg: var(--border-subtle);
  background: var(--bg-panel);
  padding: 0.75rem;
}

.command-panel__header {
  font-family: var(--font-display);
  font-size: 0.75rem;
  letter-spacing: 0.1em;
  color: var(--text-muted);
  margin-bottom: 0.5rem;
  text-transform: uppercase;
}

.command-panel__grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 4px;
}

.command-button {
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  background: var(--bg-tertiary);
  border: 1px solid transparent;
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.15s;
  font-size: 0.7rem;
}

.command-button:hover:not(:disabled) {
  border-color: var(--accent-primary);
  box-shadow: var(--glow-primary);
}

.command-button__hotkey {
  position: absolute;
  bottom: 2px;
  right: 4px;
  font-size: 0.6rem;
  color: var(--text-muted);
  font-family: var(--font-mono);
}
```

### 4. Event Log / Console

```tsx
interface SystemEvent {
  id: string;
  timestamp: Date;
  level: 'info' | 'success' | 'warning' | 'error';
  source: string;
  message: string;
}

const EventLog: React.FC<{ events: SystemEvent[] }> = ({ events }) => {
  const logRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    // Auto-scroll to bottom on new events
    logRef.current?.scrollTo({ top: logRef.current.scrollHeight });
  }, [events.length]);
  
  return (
    <div className="event-log" data-augmented-ui="tl-clip border">
      <div className="event-log__header">
        <span>EVENT LOG</span>
        <div className="event-log__filters">
          {/* Filter toggles */}
        </div>
      </div>
      <div className="event-log__content" ref={logRef}>
        {events.map(e => (
          <EventEntry key={e.id} event={e} />
        ))}
      </div>
    </div>
  );
};
```

```css
.event-log {
  --aug-tl: 8px;
  --aug-border-all: 1px;
  --aug-border-bg: var(--border-subtle);
  background: var(--bg-panel);
  display: flex;
  flex-direction: column;
  font-family: var(--font-mono);
  font-size: 0.8rem;
}

.event-log__content {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
}

.event-entry {
  display: flex;
  gap: 0.75rem;
  padding: 0.25rem 0;
  border-bottom: 1px solid var(--border-subtle);
}

.event-entry__time {
  color: var(--text-muted);
  flex-shrink: 0;
}

.event-entry__source {
  color: var(--accent-primary);
  flex-shrink: 0;
  min-width: 80px;
}

.event-entry--error { color: var(--accent-danger); }
.event-entry--warning { color: var(--accent-warning); }
.event-entry--success { color: var(--accent-secondary); }
```

### 5. Minimap

```tsx
const Minimap: React.FC<{
  agents: Agent[];
  viewportBounds: Rect;
  onNavigate: (position: Point) => void;
}> = ({ agents, viewportBounds, onNavigate }) => (
  <div 
    className="minimap" 
    data-augmented-ui="tl-clip br-clip border"
    onClick={handleClick}
  >
    <div className="minimap__viewport" style={viewportStyle} />
    {agents.map(a => (
      <div 
        key={a.id}
        className={`minimap__dot minimap__dot--${a.status}`}
        style={{ left: `${a.position.x}%`, top: `${a.position.y}%` }}
      />
    ))}
  </div>
);
```

## Animations and Effects

### Scan Line Effect

```css
.scan-line {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: linear-gradient(
    to bottom,
    transparent 0%,
    rgba(0, 212, 255, 0.03) 50%,
    transparent 100%
  );
  animation: scan 4s linear infinite;
}

@keyframes scan {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100%); }
}
```

### Panel Entrance Animation

```css
.panel-enter {
  animation: panelReveal 0.4s ease-out forwards;
}

@keyframes panelReveal {
  0% {
    opacity: 0;
    clip-path: polygon(0 0, 0 0, 0 100%, 0 100%);
  }
  100% {
    opacity: 1;
    clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%);
  }
}
```

### Glowing Pulse for Active Elements

```css
.pulse-glow {
  animation: pulseGlow 2s ease-in-out infinite;
}

@keyframes pulseGlow {
  0%, 100% { box-shadow: 0 0 5px var(--accent-primary); }
  50% { box-shadow: 0 0 20px var(--accent-primary), 0 0 40px var(--accent-primary); }
}
```

## Keyboard Shortcuts Pattern

```tsx
const useKeyboardShortcuts = (commands: Map<string, () => void>) => {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      // Ignore if typing in input
      if (e.target instanceof HTMLInputElement) return;
      
      const key = e.key.toUpperCase();
      const command = commands.get(key);
      if (command) {
        e.preventDefault();
        command();
      }
    };
    
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [commands]);
};

// Usage
useKeyboardShortcuts(new Map([
  ['A', () => selectAll()],
  ['S', () => stopSelected()],
  ['Q', () => executeCommand('queue')],
  ['ESCAPE', () => clearSelection()],
]));
```

## ADAM Platform Integration Notes

For integrating with the ADAM platform's existing React 19 + TypeScript + Vite stack:

1. **WebSocket Integration**: Connect EventLog and ResourceBar to existing WebSocket gateway for real-time updates
2. **Agent Mapping**: Map Desktop Metal printers (X25 Pro, Shop System, etc.) as "units" on the tactical map
3. **Nova Orchestrator**: Display Nova's AI decisions in the event log with `--accent-purple` styling
4. **INTERSECT Events**: Subscribe to MQTT topics for instrument status updates
5. **Experiment Campaigns**: Show active campaigns as "mission objectives" in a sidebar panel

## Dependencies

```json
{
  "dependencies": {
    "augmented-ui": "^2.0.0",
    "framer-motion": "^11.0.0",
    "lucide-react": "^0.400.0",
    "d3": "^7.9.0",
    "topojson-client": "^3.1.0"
  },
  "devDependencies": {
    "@types/d3": "^7.4.0",
    "@types/topojson-client": "^3.1.0"
  }
}
```

## Global Network Map (D3.js)

The ADAM platform includes a global visualization of the entire printer install base. This D3.js-powered map enables operators to visualize, filter, and select sites for onboarding into the autonomous manufacturing network.

### Map Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│  ADAM GLOBAL NETWORK                           [Filter] [Search]     │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│     ┌─────────────────────────────────────────────────────────┐     │
│     │                                                         │     │
│     │                    D3.js US/World Map                   │     │
│     │                                                         │     │
│     │        ◆ Tier A (Gold)    ● Tier B (Cyan)              │     │
│     │        ○ Tier C (Gray)    ◇ Selected (Green)           │     │
│     │                                                         │     │
│     └─────────────────────────────────────────────────────────┘     │
│                                                                      │
├────────────────────────────────────┬─────────────────────────────────┤
│  SITE DETAILS                      │  SELECTION QUEUE               │
│  ┌────────────────────────────┐    │  ┌───────────────────────────┐ │
│  │ Anduril Industries         │    │  │ 3 sites selected          │ │
│  │ Irvine, CA                 │    │  │ 7 printers total          │ │
│  │ 2 installations (Shop)     │    │  │                           │ │
│  │ Priority: B                │    │  │ [Onboard to ADAM]         │ │
│  │ Contact: mdiaz@anduril.com │    │  └───────────────────────────┘ │
│  └────────────────────────────┘    │                                 │
└────────────────────────────────────┴─────────────────────────────────┘
```

### Dependencies

```bash
npm install d3 @types/d3 topojson-client @types/topojson-client
```

### Core Map Component

```tsx
// components/GlobalMap/GlobalMap.tsx
import { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import * as topojson from 'topojson-client';
import type { Topology, GeometryCollection } from 'topojson-specification';
import './GlobalMap.css';

interface Site {
  id: string;
  name: string;
  city: string;
  state: string;
  lat: number;
  lng: number;
  installations: number;
  productLines: string[];
  priorityTier: 'A' | 'B' | 'C';
  priorityScore: number;
  contactName?: string;
  contactEmail?: string;
  hasShop: boolean;
  hasStudio: boolean;
  hasInnX: boolean;
}

interface GlobalMapProps {
  sites: Site[];
  selectedIds: Set<string>;
  onSiteSelect: (siteId: string, additive?: boolean) => void;
  onSiteHover: (site: Site | null) => void;
  filters: {
    productLines: string[];
    priorityTiers: string[];
    states: string[];
  };
}

const TIER_COLORS = {
  A: '#ffd700',  // Gold
  B: '#00d4ff',  // Cyan
  C: '#556677',  // Muted gray
};

export const GlobalMap: React.FC<GlobalMapProps> = ({
  sites,
  selectedIds,
  onSiteSelect,
  onSiteHover,
  filters,
}) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const [dimensions, setDimensions] = useState({ width: 960, height: 600 });

  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    // US Albers projection optimized for continental US
    const projection = d3.geoAlbersUsa()
      .scale(1200)
      .translate([dimensions.width / 2, dimensions.height / 2]);

    const path = d3.geoPath().projection(projection);

    // Load US TopoJSON
    d3.json<Topology>('https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json')
      .then((us) => {
        if (!us) return;

        const states = topojson.feature(
          us,
          us.objects.states as GeometryCollection
        );

        // Draw state boundaries
        const g = svg.append('g').attr('class', 'map-layer');

        g.selectAll('path.state')
          .data(states.features)
          .join('path')
          .attr('class', 'state')
          .attr('d', path)
          .attr('fill', 'var(--bg-secondary)')
          .attr('stroke', 'var(--border-subtle)')
          .attr('stroke-width', 0.5);

        // Filter sites based on current filters
        const filteredSites = sites.filter((site) => {
          if (filters.states.length && !filters.states.includes(site.state)) {
            return false;
          }
          if (filters.priorityTiers.length && !filters.priorityTiers.includes(site.priorityTier)) {
            return false;
          }
          if (filters.productLines.length) {
            const hasMatch = filters.productLines.some((pl) =>
              site.productLines.includes(pl)
            );
            if (!hasMatch) return false;
          }
          return true;
        });

        // Draw site markers
        const markers = svg.append('g').attr('class', 'markers-layer');

        markers
          .selectAll('circle.site-marker')
          .data(filteredSites)
          .join('circle')
          .attr('class', (d) => `site-marker ${selectedIds.has(d.id) ? 'selected' : ''}`)
          .attr('cx', (d) => {
            const coords = projection([d.lng, d.lat]);
            return coords ? coords[0] : 0;
          })
          .attr('cy', (d) => {
            const coords = projection([d.lng, d.lat]);
            return coords ? coords[1] : 0;
          })
          .attr('r', (d) => Math.max(6, Math.sqrt(d.installations) * 6))
          .attr('fill', (d) => selectedIds.has(d.id) 
            ? 'var(--accent-secondary)' 
            : TIER_COLORS[d.priorityTier]
          )
          .attr('stroke', (d) => selectedIds.has(d.id) 
            ? 'var(--accent-secondary)' 
            : 'var(--bg-primary)'
          )
          .attr('stroke-width', 2)
          .style('cursor', 'pointer')
          .on('click', (event, d) => {
            onSiteSelect(d.id, event.shiftKey || event.ctrlKey);
          })
          .on('mouseenter', (_, d) => onSiteHover(d))
          .on('mouseleave', () => onSiteHover(null));

        // Add glow filter for selected markers
        const defs = svg.append('defs');
        const filter = defs.append('filter').attr('id', 'glow');
        filter
          .append('feGaussianBlur')
          .attr('stdDeviation', '3')
          .attr('result', 'coloredBlur');
        const feMerge = filter.append('feMerge');
        feMerge.append('feMergeNode').attr('in', 'coloredBlur');
        feMerge.append('feMergeNode').attr('in', 'SourceGraphic');
      });
  }, [sites, selectedIds, filters, dimensions, onSiteSelect, onSiteHover]);

  return (
    <div className="global-map" data-augmented-ui="tl-clip br-clip border">
      <svg
        ref={svgRef}
        width={dimensions.width}
        height={dimensions.height}
        viewBox={`0 0 ${dimensions.width} ${dimensions.height}`}
      />
    </div>
  );
};
```

### Map Styles

```css
/* GlobalMap.css */
.global-map {
  --aug-tl: 12px;
  --aug-br: 12px;
  --aug-border-all: 1px;
  --aug-border-bg: var(--border-subtle);
  background: var(--bg-primary);
  overflow: hidden;
}

.global-map svg {
  display: block;
}

.global-map .state {
  transition: fill 0.2s;
}

.global-map .state:hover {
  fill: var(--bg-tertiary);
}

.global-map .site-marker {
  transition: all 0.2s;
  filter: drop-shadow(0 0 2px rgba(0, 0, 0, 0.5));
}

.global-map .site-marker:hover {
  filter: drop-shadow(0 0 8px currentColor);
  transform-origin: center;
}

.global-map .site-marker.selected {
  filter: url(#glow) drop-shadow(0 0 10px var(--accent-secondary));
  animation: markerPulse 2s ease-in-out infinite;
}

@keyframes markerPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}
```

### Filter Panel Component

```tsx
// components/GlobalMap/MapFilters.tsx
interface MapFiltersProps {
  filters: {
    productLines: string[];
    priorityTiers: string[];
    states: string[];
  };
  onFiltersChange: (filters: MapFiltersProps['filters']) => void;
  availableStates: string[];
}

export const MapFilters: React.FC<MapFiltersProps> = ({
  filters,
  onFiltersChange,
  availableStates,
}) => {
  const toggleFilter = (
    category: keyof typeof filters,
    value: string
  ) => {
    const current = filters[category];
    const updated = current.includes(value)
      ? current.filter((v) => v !== value)
      : [...current, value];
    onFiltersChange({ ...filters, [category]: updated });
  };

  return (
    <div className="map-filters" data-augmented-ui="tl-clip border">
      <div className="map-filters__section">
        <h4>Product Lines</h4>
        <div className="map-filters__buttons">
          {['Shop', 'Studio', 'InnX'].map((pl) => (
            <button
              key={pl}
              className={`filter-btn ${filters.productLines.includes(pl) ? 'active' : ''}`}
              onClick={() => toggleFilter('productLines', pl)}
            >
              {pl}
            </button>
          ))}
        </div>
      </div>

      <div className="map-filters__section">
        <h4>Priority Tier</h4>
        <div className="map-filters__buttons">
          {['A', 'B', 'C'].map((tier) => (
            <button
              key={tier}
              className={`filter-btn tier-${tier} ${filters.priorityTiers.includes(tier) ? 'active' : ''}`}
              onClick={() => toggleFilter('priorityTiers', tier)}
            >
              Tier {tier}
            </button>
          ))}
        </div>
      </div>

      <div className="map-filters__section">
        <h4>Region</h4>
        <select
          multiple
          value={filters.states}
          onChange={(e) => {
            const selected = Array.from(e.target.selectedOptions, (o) => o.value);
            onFiltersChange({ ...filters, states: selected });
          }}
          className="state-select"
        >
          {availableStates.map((st) => (
            <option key={st} value={st}>{st}</option>
          ))}
        </select>
      </div>
    </div>
  );
};
```

### Site Detail Panel

```tsx
// components/GlobalMap/SiteDetailPanel.tsx
interface SiteDetailPanelProps {
  site: Site | null;
  isSelected: boolean;
  onSelect: () => void;
  onDeselect: () => void;
}

export const SiteDetailPanel: React.FC<SiteDetailPanelProps> = ({
  site,
  isSelected,
  onSelect,
  onDeselect,
}) => {
  if (!site) {
    return (
      <div className="site-detail-panel empty" data-augmented-ui="tl-clip br-clip border">
        <p className="text-muted">Hover over a site to view details</p>
      </div>
    );
  }

  return (
    <div 
      className={`site-detail-panel ${isSelected ? 'selected' : ''}`} 
      data-augmented-ui="tl-clip br-clip border"
    >
      <div className="site-detail-panel__header">
        <span className={`tier-badge tier-${site.priorityTier}`}>
          Tier {site.priorityTier}
        </span>
        <span className="priority-score">Score: {site.priorityScore}</span>
      </div>

      <h3 className="site-detail-panel__name">{site.name}</h3>
      <p className="site-detail-panel__location">
        {site.city}, {site.state}
      </p>

      <div className="site-detail-panel__stats">
        <div className="stat">
          <span className="stat__value">{site.installations}</span>
          <span className="stat__label">Printers</span>
        </div>
        <div className="stat">
          <span className="stat__value">{site.productLines.join(', ')}</span>
          <span className="stat__label">Product Lines</span>
        </div>
      </div>

      <div className="site-detail-panel__products">
        {site.hasShop && <span className="product-badge shop">Shop</span>}
        {site.hasStudio && <span className="product-badge studio">Studio</span>}
        {site.hasInnX && <span className="product-badge innx">InnX</span>}
      </div>

      {site.contactEmail && (
        <div className="site-detail-panel__contact">
          <p><strong>Contact:</strong> {site.contactName}</p>
          <p><a href={`mailto:${site.contactEmail}`}>{site.contactEmail}</a></p>
        </div>
      )}

      <button
        className={`onboard-btn ${isSelected ? 'selected' : ''}`}
        onClick={isSelected ? onDeselect : onSelect}
        data-augmented-ui="tl-clip br-clip border"
      >
        {isSelected ? 'Remove from Selection' : 'Add to ADAM Network'}
      </button>
    </div>
  );
};
```

### Selection Queue Panel

```tsx
// components/GlobalMap/SelectionQueue.tsx
interface SelectionQueueProps {
  selectedSites: Site[];
  onRemoveSite: (siteId: string) => void;
  onClearAll: () => void;
  onOnboardSelected: () => void;
}

export const SelectionQueue: React.FC<SelectionQueueProps> = ({
  selectedSites,
  onRemoveSite,
  onClearAll,
  onOnboardSelected,
}) => {
  const totalPrinters = selectedSites.reduce((sum, s) => sum + s.installations, 0);

  return (
    <div className="selection-queue" data-augmented-ui="tl-clip tr-clip border">
      <div className="selection-queue__header">
        <h4>ONBOARDING QUEUE</h4>
        {selectedSites.length > 0 && (
          <button className="clear-btn" onClick={onClearAll}>Clear All</button>
        )}
      </div>

      <div className="selection-queue__summary">
        <div className="summary-stat">
          <span className="summary-stat__value">{selectedSites.length}</span>
          <span className="summary-stat__label">Sites</span>
        </div>
        <div className="summary-stat">
          <span className="summary-stat__value">{totalPrinters}</span>
          <span className="summary-stat__label">Printers</span>
        </div>
      </div>

      <div className="selection-queue__list">
        {selectedSites.map((site) => (
          <div key={site.id} className="queue-item">
            <div className="queue-item__info">
              <span className="queue-item__name">{site.name}</span>
              <span className="queue-item__meta">
                {site.city}, {site.state} • {site.installations} units
              </span>
            </div>
            <button
              className="queue-item__remove"
              onClick={() => onRemoveSite(site.id)}
            >
              ×
            </button>
          </div>
        ))}
      </div>

      {selectedSites.length > 0 && (
        <button
          className="onboard-all-btn"
          onClick={onOnboardSelected}
          data-augmented-ui="tl-clip br-clip border"
        >
          <span className="btn-icon">⚡</span>
          Onboard {selectedSites.length} Sites to ADAM
        </button>
      )}
    </div>
  );
};
```

### Geocoding Utility

Since the install base data may not have coordinates, include a geocoding utility:

```typescript
// utils/geocoding.ts

// US State centroid coordinates for approximate positioning
export const STATE_CENTROIDS: Record<string, [number, number]> = {
  AL: [-86.9023, 32.3182], AK: [-153.4937, 64.2008], AZ: [-111.0937, 34.0489],
  AR: [-92.3731, 35.2010], CA: [-119.4179, 36.7783], CO: [-105.3111, 39.0598],
  CT: [-72.7554, 41.6032], DE: [-75.5277, 38.9108], FL: [-81.5158, 27.6648],
  GA: [-82.9071, 32.1656], HI: [-155.5828, 19.8968], ID: [-114.7420, 44.0682],
  IL: [-89.3985, 40.6331], IN: [-86.1349, 40.2672], IA: [-93.0977, 41.8780],
  KS: [-98.4842, 39.0119], KY: [-84.2700, 37.8393], LA: [-91.9623, 30.9843],
  ME: [-69.4455, 45.2538], MD: [-76.6413, 39.0458], MA: [-71.3824, 42.4072],
  MI: [-85.6024, 44.3148], MN: [-94.6859, 46.7296], MS: [-89.3985, 32.3547],
  MO: [-91.8318, 37.9643], MT: [-110.3626, 46.8797], NE: [-99.9018, 41.4925],
  NV: [-116.4194, 38.8026], NH: [-71.5724, 43.1939], NJ: [-74.4057, 40.0583],
  NM: [-105.8701, 34.5199], NY: [-75.4999, 43.2994], NC: [-79.0193, 35.7596],
  ND: [-101.0020, 47.5515], OH: [-82.9071, 40.4173], OK: [-97.0929, 35.0078],
  OR: [-120.5542, 43.8041], PA: [-77.1945, 41.2033], RI: [-71.4774, 41.5801],
  SC: [-81.1637, 33.8361], SD: [-99.9018, 43.9695], TN: [-86.5804, 35.5175],
  TX: [-99.9018, 31.9686], UT: [-111.0937, 39.3210], VT: [-72.5778, 44.5588],
  VA: [-78.6569, 37.4316], WA: [-120.7401, 47.7511], WV: [-80.4549, 38.5976],
  WI: [-89.6165, 43.7844], WY: [-107.2903, 43.0760], DC: [-77.0369, 38.9072],
};

// Major US cities with coordinates
export const CITY_COORDINATES: Record<string, [number, number]> = {
  'new york|ny': [-74.006, 40.7128],
  'los angeles|ca': [-118.2437, 34.0522],
  'chicago|il': [-87.6298, 41.8781],
  'houston|tx': [-95.3698, 29.7604],
  'phoenix|az': [-112.074, 33.4484],
  'philadelphia|pa': [-75.1652, 39.9526],
  'san antonio|tx': [-98.4936, 29.4241],
  'san diego|ca': [-117.1611, 32.7157],
  'dallas|tx': [-96.797, 32.7767],
  'san jose|ca': [-121.8863, 37.3382],
  'austin|tx': [-97.7431, 30.2672],
  'boston|ma': [-71.0589, 42.3601],
  'seattle|wa': [-122.3321, 47.6062],
  'denver|co': [-104.9903, 39.7392],
  'detroit|mi': [-83.0458, 42.3314],
  'irvine|ca': [-117.8265, 33.6846],
  'cupertino|ca': [-122.0322, 37.323],
  'fremont|ca': [-121.9886, 37.5485],
  'pittsburgh|pa': [-79.9959, 40.4406],
  'cleveland|oh': [-81.6944, 41.4993],
  'cincinnati|oh': [-84.512, 39.1031],
  'columbus|oh': [-82.9988, 39.9612],
  'dayton|oh': [-84.1916, 39.7589],
  'salt lake city|ut': [-111.891, 40.7608],
  'albuquerque|nm': [-106.6504, 35.0844],
  'knoxville|tn': [-83.9207, 35.9606],
};

export function geocodeSite(city: string, state: string): [number, number] | null {
  // Try exact city match first
  const cityKey = `${city.toLowerCase()}|${state.toLowerCase()}`;
  if (CITY_COORDINATES[cityKey]) {
    return CITY_COORDINATES[cityKey];
  }

  // Fall back to state centroid with random jitter
  if (STATE_CENTROIDS[state]) {
    const [lng, lat] = STATE_CENTROIDS[state];
    // Add small random offset to prevent overlapping markers
    const jitter = () => (Math.random() - 0.5) * 2;
    return [lng + jitter(), lat + jitter()];
  }

  return null;
}
```

### Data Loading Hook

```typescript
// hooks/useInstallBaseData.ts
import { useState, useEffect } from 'react';
import { geocodeSite } from '../utils/geocoding';

interface RawSiteData {
  'Site Key': string;
  'Site Name': string;
  City: string;
  ST: string;
  Installations: number;
  'Product Lines': string;
  'Priority Tier': string;
  'Priority Score': number;
  'Contact Name'?: string;
  'Contact Email'?: string;
  'Has Shop': number;
  'Has Studio': number;
  'Has InnX': number;
}

export function useInstallBaseData(dataUrl: string) {
  const [sites, setSites] = useState<Site[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetch(dataUrl)
      .then((res) => res.json())
      .then((data: RawSiteData[]) => {
        const processed = data
          .map((raw): Site | null => {
            const coords = geocodeSite(raw.City, raw.ST);
            if (!coords) return null;

            return {
              id: raw['Site Key'],
              name: raw['Site Name'],
              city: raw.City,
              state: raw.ST,
              lat: coords[1],
              lng: coords[0],
              installations: raw.Installations || 0,
              productLines: raw['Product Lines']?.split(',').map((s) => s.trim()) || [],
              priorityTier: (raw['Priority Tier'] as 'A' | 'B' | 'C') || 'C',
              priorityScore: raw['Priority Score'] || 0,
              contactName: raw['Contact Name'],
              contactEmail: raw['Contact Email'],
              hasShop: raw['Has Shop'] === 1,
              hasStudio: raw['Has Studio'] === 1,
              hasInnX: raw['Has InnX'] === 1,
            };
          })
          .filter((s): s is Site => s !== null);

        setSites(processed);
        setLoading(false);
      })
      .catch((err) => {
        setError(err);
        setLoading(false);
      });
  }, [dataUrl]);

  return { sites, loading, error };
}
```

## Quick Start Checklist

1. [ ] Install augmented-ui and add CSS import
2. [ ] Create GodModeLayout with grid regions
3. [ ] Implement ResourceBar with system metrics
4. [ ] Build TacticalMap with selectable unit markers
5. [ ] Add CommandPanel with context-sensitive actions
6. [ ] Create EventLog with real-time WebSocket subscription
7. [ ] Add keyboard shortcut bindings
8. [ ] Apply scan-line and glow effects for sci-fi polish
9. [ ] Connect to ADAM's existing WebSocket gateway
10. [ ] Map printer fleet to unit positions on tactical map
11. [ ] **Install D3.js and topojson-client for global map**
12. [ ] **Create GlobalMap component with US projection**
13. [ ] **Implement site filtering by product line, tier, state**
14. [ ] **Build selection queue for ADAM onboarding workflow**
15. [ ] **Load and geocode install base data from spreadsheet**
