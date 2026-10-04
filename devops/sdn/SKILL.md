---
name: sdn
description: Software-defined networking
license: MIT
compatibility: opencode
metadata:
  audience: network-engineers
  category: networking
---

## What I do

- Design and implement SDN architectures
- Program network behavior through controllers
- Separate control plane from data plane
- Implement network virtualization
- Create dynamic network policies
- Manage network through software APIs
- Deploy network automation with SDN

## When to use me

Use me when:
- Building programmable network infrastructure
- Implementing network virtualization
- Managing data center networks
- Creating dynamic network policies
- Requiring network-wide visibility
- Automating network operations at scale

## Key Concepts

### SDN Architecture
```
┌─────────────────────────────────────────────────────┐
│                  Application Layer                   │
│              (Network Apps & Orchestration)          │
└─────────────────────┬───────────────────────────────┘
                      │ Northbound API
┌─────────────────────▼───────────────────────────────┐
│               SDN Controller                          │
│           (OpenDaylight, ONOS, Ryu)                  │
│         - Network state                              │
│         - Topology discovery                         │
│         - Path computation                           │
└─────────────────────┬───────────────────────────────┘
                      │ Southbound API
┌─────────────────────▼───────────────────────────────┐
│                 Data Plane                            │
│            (Switches, Routers)                        │
│         - Forwarding                                 │
│         - Flow tables                                 │
└─────────────────────────────────────────────────────┘
```

### OpenFlow Protocol
Standard southbound protocol for SDN:

```python
# Ryu SDN Controller example
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, set_ev_cls
from ryu.lib.packet import packet, ethernet, ipv4

class SimpleSwitch(app_manager.RyuApp):
    def __init__(self, *args, **kwargs):
        super(SimpleSwitch, self).__init__(*args, **kwargs)
        
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        dp = msg.datapath
        ofp = dp.ofproto_parser
        
        # Install flow rule
        actions = [ofp.OFPActionOutput(ofp.OFPP_FLOOD)]
        self.add_flow(dp, 1, actions)
```

### SDN Use Cases
- **Data Center**: Network virtualization, tenant isolation
- **WAN**: SD-WAN for branch connectivity
- **Campus**: Centralized policy management
- **Service Provider**: Network slicing

### Controllers
- **OpenDaylight**: Enterprise, feature-rich
- **ONOS**: Carrier-grade, performance
- **Ryu**: Python, lightweight
- **ODL**: Vendor-neutral
