---
name: cisco-network-diagram
description: Generate Draw.io network topology diagrams from Cisco router and switch configurations. Use when asked to visualize network topology, create network diagrams, map network infrastructure, or generate visual representations from Cisco device configs. Supports parsing show commands, configuration files, CDP/LLDP neighbor data, and routing protocol information to automatically create professional network diagrams.
license: MIT
---

# Cisco Network Diagram Generator

Generate professional Draw.io network topology diagrams from Cisco device configurations using the `drawio-network-plot` Python library.

## Overview

This skill automates the creation of network topology diagrams by:
1. Parsing Cisco device configurations to extract topology data
2. Identifying devices, interfaces, connections, and network relationships
3. Generating Draw.io XML diagrams with proper device icons and layouts
4. Supporting multi-layer visualization (physical, logical, L2, L3)

**Assumption**: Device configurations have already been collected. This skill focuses on parsing and visualization, not SSH access or data collection.

## Installation

Install required library:
```bash
pip install drawio-network-plot --break-system-packages
```

## Quick Start Workflow

1. **Parse configurations** - Extract topology data from config files
2. **Build topology model** - Create device and connection objects
3. **Generate diagram** - Use drawio-network-plot to create XML
4. **Save output** - Write to `/mnt/user-data/outputs/network-diagram.drawio`

## Parsing Cisco Configurations

### Key Data to Extract

Extract these elements from Cisco configs:

**Device Information:**
- Hostname: `hostname <name>`
- Device type: Infer from model (router/switch/firewall/L3 switch)
- Management IP: `interface <mgmt>` + `ip address`

**Interface Details:**
- Interface name, status, IP address, subnet mask
- VLANs: `switchport access vlan`, `switchport trunk allowed vlan`
- Descriptions: `description <text>`
- Speed/duplex settings

**Layer 2 Connections:**
- CDP neighbors: Parse `show cdp neighbors detail` output
- LLDP neighbors: Parse `show lldp neighbors detail` output
- Port channels: `interface Port-channel`, member interfaces

**Layer 3 Information:**
- Static routes: `ip route`
- OSPF: `router ospf`, network statements, areas
- BGP: `router bgp`, neighbors, AS numbers
- EIGRP: `router eigrp`, network statements
- HSRP/VRRP: `standby`, `vrrp` configurations

**Important**: Use `references/cisco-parser.md` for detailed parsing patterns and regular expressions for each configuration type.

## Using drawio-network-plot

### Basic Structure

```python
from drawio_network_plot import create_graph, Node, Edge

# Create graph
graph = create_graph(filename="network.drawio", direction="LR")

# Add devices as nodes
router = Node(
    id="rtr1",
    label="Core-Router-01",
    device_type="router",
    ip_address="10.0.0.1"
)
graph.add_node(router)

# Add connections as edges
link = Edge(
    source="rtr1",
    target="sw1",
    label="Gi0/0/0 → Gi1/0/1\n10.1.1.0/30"
)
graph.add_edge(link)

# Generate diagram
graph.draw()
```

### Device Types and Icons

Map Cisco devices to appropriate icons:

- **Router**: `device_type="router"` - Routers, multilayer switches doing L3
- **Switch**: `device_type="switch"` - L2 switches, access switches
- **Firewall**: `device_type="firewall"` - ASA, Firepower
- **Server**: `device_type="server"` - Services, appliances
- **Cloud**: `device_type="cloud"` - Internet, WAN, external networks
- **PC**: `device_type="pc"` - End devices, workstations

### Layout Strategies

**Hierarchical (Top-Down):**
```python
graph = create_graph(filename="network.drawio", direction="TB")
```
Best for: Core → Distribution → Access topologies

**Left-to-Right:**
```python
graph = create_graph(filename="network.drawio", direction="LR")
```
Best for: Service chains, data flows, sequential processing

**Manual Positioning:**
```python
node = Node(id="sw1", label="Switch", x=100, y=200, width=120, height=80)
```
Best for: Complex topologies, specific physical layouts, data center rows

### Edge Labeling Best Practices

Include relevant information on connection labels:

```python
# L3 Point-to-Point
Edge(label="Gi0/0 → Gi0/1\n10.1.1.0/30\nOSPF Area 0")

# L2 Trunk
Edge(label="Trunk\nVLANs: 10,20,30,100\n1Gbps")

# Port Channel
Edge(label="Po1 (LACP)\nGi0/1-2\n2Gbps")
```

## Complete Workflow Example

Use `scripts/generate_network_diagram.py` for a complete implementation:

```bash
python scripts/generate_network_diagram.py <config_directory> <output_file>
```

Or follow this manual workflow:

```python
import re
from drawio_network_plot import create_graph, Node, Edge

# 1. Parse configurations
devices = {}
connections = []

for config_file in config_files:
    # Parse device info
    hostname = extract_hostname(config_file)
    device_type = infer_device_type(config_file)
    mgmt_ip = extract_mgmt_ip(config_file)
    
    devices[hostname] = {
        'type': device_type,
        'mgmt_ip': mgmt_ip,
        'interfaces': extract_interfaces(config_file)
    }
    
    # Parse CDP neighbors to find connections
    cdp_neighbors = parse_cdp_neighbors(config_file)
    for neighbor in cdp_neighbors:
        connections.append({
            'source': hostname,
            'source_int': neighbor['local_interface'],
            'target': neighbor['device_id'],
            'target_int': neighbor['remote_interface']
        })

# 2. Create graph
graph = create_graph(filename="network.drawio", direction="TB")

# 3. Add devices
for hostname, info in devices.items():
    node = Node(
        id=hostname,
        label=f"{hostname}\n{info['mgmt_ip']}",
        device_type=info['type']
    )
    graph.add_node(node)

# 4. Add connections (deduplicate bidirectional links)
seen_connections = set()
for conn in connections:
    conn_key = tuple(sorted([
        f"{conn['source']}:{conn['source_int']}", 
        f"{conn['target']}:{conn['target_int']}"
    ]))
    
    if conn_key not in seen_connections:
        edge = Edge(
            source=conn['source'],
            target=conn['target'],
            label=f"{conn['source_int']} ↔ {conn['target_int']}"
        )
        graph.add_edge(edge)
        seen_connections.add(conn_key)

# 5. Generate diagram
graph.draw()
```

## Advanced Features

### Multi-Layer Diagrams

Create separate diagrams for different network layers:

**Physical Layer**: All devices and physical connections
**Logical Layer**: VLANs, broadcast domains, subnets
**Layer 3**: Routers, routing protocols, subnets
**Security Zones**: Firewalls, ACLs, security boundaries

### Grouping and Containers

Use containers for logical grouping:

```python
from drawio_network_plot import Container

# Create data center container
dc1 = Container(
    id="dc1",
    label="Data Center 1",
    children=["rtr1", "sw1", "sw2", "fw1"]
)
graph.add_container(dc1)
```

### Styling and Customization

Customize colors for different device roles:

```python
node = Node(
    id="core-rtr",
    label="Core Router",
    device_type="router",
    fill_color="#FF6B6B",  # Red for core devices
    font_color="#FFFFFF"
)
```

### Adding Metadata

Include additional information as node properties:

```python
node = Node(
    id="rtr1",
    label="Core-Router-01",
    device_type="router",
    metadata={
        "model": "ISR4451-X",
        "ios_version": "17.6.3",
        "location": "Building A - MDF",
        "serial": "FDO2148B0X1"
    }
)
```

## Handling Complex Topologies

### Large Networks (50+ devices)

For large topologies:
1. Create hierarchical sub-diagrams by location or function
2. Use containers to group related devices
3. Generate separate diagrams for L2 and L3 views
4. Create summary diagrams showing only core infrastructure

### Redundant Paths

Show redundancy clearly:
```python
# Primary path
edge1 = Edge(source="rtr1", target="rtr2", label="Primary\nGi0/0", style="solid")
# Backup path  
edge2 = Edge(source="rtr1", target="rtr2", label="Backup\nGi0/1", style="dashed")
```

### MPLS/VPN Topologies

Represent virtual connections:
```python
# VPN tunnel
vpn_edge = Edge(
    source="site1-rtr",
    target="site2-rtr",
    label="IPsec VPN\n10.100.0.0/24",
    style="dashed",
    color="#0066CC"
)
```

## Output and Delivery

1. Save to outputs directory:
```python
import shutil
shutil.move("network.drawio", "/mnt/user-data/outputs/network-diagram.drawio")
```

2. Generate multiple formats if needed:
   - Primary: `.drawio` (editable XML)
   - Export via Draw.io: PNG, SVG, PDF

3. Provide user with link:
```python
print("[View your network diagram](computer:///mnt/user-data/outputs/network-diagram.drawio)")
```

## Troubleshooting

**Issue**: Overlapping nodes
**Solution**: Use manual positioning or adjust layout direction

**Issue**: Missing connections  
**Solution**: Verify CDP/LLDP data parsing, check for hostname mismatches

**Issue**: Incorrect device types
**Solution**: Review device type inference logic, use explicit type mapping

**Issue**: Too much information on diagram
**Solution**: Create multiple focused diagrams (L2, L3, security) instead of one complex diagram

## Best Practices

1. **Start simple**: Begin with physical connectivity, add layers incrementally
2. **Validate data**: Cross-reference parsed data with source configs before generating diagram
3. **Use meaningful labels**: Include interface names, IP addresses, and protocol info
4. **Group logically**: Use containers for sites, VLANs, or security zones
5. **Handle missing data gracefully**: Use placeholder values when CDP/LLDP is unavailable
6. **Document assumptions**: Note which connections are discovered vs. inferred
7. **Provide context**: Add title, legend, and timestamp to diagrams

## Reference Files

- **`references/cisco-parser.md`**: Detailed regex patterns and parsing functions for all Cisco configuration types
- **`references/drawio-examples.md`**: Complete working examples for different network scenarios
- **`scripts/generate_network_diagram.py`**: Production-ready script with full parsing and generation logic

## Common Use Cases

**Use Case 1: Data Center Topology**
```python
# Create top-down diagram with core, aggregation, and access layers
# Group servers by rack, show redundant uplinks
```

**Use Case 2: Branch Office WAN**
```python
# Show hub-and-spoke topology with MPLS/VPN connections
# Highlight primary and backup WAN links
```

**Use Case 3: VLAN Visualization**
```python
# Create L2 diagram showing VLAN trunks and access ports
# Color-code by VLAN or security zone
```

**Use Case 4: Routing Protocol View**
```python
# Show OSPF areas, BGP peerings, route reflectors
# Label edges with metrics and next-hops
```

## Next Steps After Generation

1. Open diagram in Draw.io (web: app.diagrams.net)
2. Manually refine layout and positioning as needed
3. Add annotations, labels, or documentation
4. Export to PNG/PDF for documentation or presentations
5. Version control the .drawio file for change tracking
