---
name: iot-system-architect
description: Expert IoT system architecture covering distributed systems, event-driven design, edge computing, and microservices patterns. Use when designing multi-device systems, planning communication architecture, implementing event-driven patterns, scaling IoT deployments, or documenting architecture decisions for distributed IoT systems.
---

# IoT System Architect

## Overview

This skill provides comprehensive guidance for designing and implementing scalable, resilient distributed IoT systems. Apply this skill when architecting multi-device systems, designing communication patterns, implementing event-driven architectures, or making critical architecture decisions for IoT deployments.

The skill encompasses distributed systems principles, communication architecture, microservices patterns, state management, scalability strategies, and design patterns specifically tailored for IoT environments.

## When to Use This Skill

Invoke this skill when:

- **Designing a new IoT system** from scratch
- **Planning communication architecture** between multiple devices
- **Implementing event-driven patterns** with MQTT or similar protocols
- **Scaling existing IoT deployments** beyond initial MVP
- **Documenting architecture decisions** for IoT systems
- **Resolving architectural challenges** in distributed device networks
- **Evaluating trade-offs** between different architecture approaches
- **Designing for offline-first** or eventually consistent systems
- **Planning state synchronization** across distributed devices
- **Implementing microservices** for IoT backend systems

## Core Architecture Capabilities

### 1. Distributed Systems Design

Apply distributed systems principles to create resilient, scalable IoT architectures.

**Key Concepts:**
- Event-driven architecture with publish-subscribe messaging
- Edge computing vs cloud processing trade-offs
- Data consistency models (strong, eventual, causal)
- CAP theorem implications for IoT systems
- Offline-first design patterns

**When to Apply:**
- Designing systems with multiple autonomous devices
- Planning data flow and processing locations
- Determining consistency requirements
- Handling network partitions and failures

**Reference Material:**
For detailed patterns and implementation strategies, read:
```
references/architecture-patterns.md
```

This reference contains:
- Event-driven architecture with MQTT pub/sub
- Edge vs cloud processing decision frameworks
- Data consistency in distributed environments
- CAP theorem trade-offs for IoT
- Eventually consistent data models
- Offline-first design patterns

**Example Application:**

When designing a timer system with multiple displays that need to stay synchronized:

1. **Determine consistency requirements**: Do all displays need to show exactly the same time instantly (strong consistency) or is eventual consistency acceptable?

2. **Choose processing location**: Should timer logic run on each device (edge) or centrally (cloud/hub)?

3. **Design for partitions**: What happens when devices lose network connectivity?

4. **Implement offline-first**: Each device maintains local state and syncs when possible

For the Argus timer system, review the specific implementation:
```
references/argus-system.md
```

### 2. Communication Architecture

Design robust, efficient communication patterns for device coordination.

**Key Patterns:**
- Hub-and-spoke topology (centralized broker)
- Mesh networking (peer-to-peer)
- Message broker design and configuration
- Topic naming conventions and hierarchy
- Quality of Service (QoS) strategies
- Message payload optimization

**When to Apply:**
- Choosing communication topology for device network
- Designing MQTT topic structure
- Selecting appropriate QoS levels
- Optimizing message payloads for bandwidth
- Configuring message broker (Mosquitto, RabbitMQ)

**Topic Structure Best Practices:**

Design hierarchical topic structures:
```
{system}/{location}/{device-type}/{device-id}/{data-type}

Examples:
argus/desk/timer/device01/state
argus/desk/timer/device01/command
argus/wrist/display/device02/telemetry
```

Use wildcards for flexible subscriptions:
```
argus/+/timer/+/state      # All timer states
argus/desk/#               # All desk devices
+/+/+/+/telemetry         # All telemetry
```

**QoS Selection Guidelines:**
- QoS 0: High-frequency sensor data, non-critical telemetry
- QoS 1: Important events, commands, state updates
- QoS 2: Financial transactions, critical commands

For comprehensive communication patterns, read:
```
references/architecture-patterns.md
  - Hub-and-Spoke Topology
  - Message Broker Design
  - Topic Naming Conventions
  - QoS Strategy
  - Payload Optimization
```

### 3. Microservices Patterns

Apply microservices architecture to IoT backend systems for modularity and scalability.

**Decomposition Strategies:**
- Service boundaries by device type
- Service boundaries by business capability
- Domain-Driven Design (bounded contexts)

**Key Patterns:**
- API design for device coordination
- Service discovery mechanisms
- Inter-service communication (sync vs async)
- Failure isolation and resilience
- Container orchestration with Docker

**When to Apply:**
- Breaking down monolithic IoT backend
- Scaling specific system components independently
- Isolating failures to prevent cascading issues
- Supporting multiple development teams
- Enabling technology diversity

**Example Decomposition for Argus System:**
```
mqtt-broker/           - Mosquitto MQTT broker
device-service/        - Device registration and discovery
timer-service/         - Timer logic and state management
notification-service/  - Notification delivery
ai-service/            - ML inference (Jetson Nano)
telemetry-service/     - Metrics collection and storage
```

**Implementation Guidance:**

For detailed microservices patterns and scalability strategies, read:
```
references/microservices-scalability.md
```

This reference covers:
- Service boundary definition
- API design patterns (REST, GraphQL, gRPC)
- Service discovery mechanisms
- Communication patterns (sync/async)
- Resilience patterns (circuit breaker, bulkhead)
- Container orchestration
- Scalability considerations
- Database sharding
- Caching strategies
- Connection pooling

### 4. State Management

Implement robust state synchronization across distributed devices.

**Patterns:**
- Device state synchronization
- State machine design for device modes
- Conflict-Free Replicated Data Types (CRDTs)
- Event sourcing
- State recovery after connection loss
- Idempotent operations

**When to Apply:**
- Synchronizing state across multiple devices
- Handling concurrent state updates
- Recovering from network partitions
- Implementing device operating modes
- Ensuring eventual consistency

**State Machine Example (Timer Modes):**

Define clear state transitions:
```
States: Idle → Working → Break → LongBreak
Events: start(), pause(), resume(), complete()

Transitions:
  Idle + start() → Working
  Working + complete() → Break
  Break + complete() → Working (or LongBreak after N cycles)
```

**Conflict Resolution:**

When devices update state concurrently:
1. Use vector clocks to detect concurrent updates
2. Apply Last-Write-Wins (LWW) for simple fields
3. Implement custom merge functions for complex state
4. Use timestamps as tiebreaker

For implementation patterns, reference:
```
references/architecture-patterns.md
  - Eventually Consistent Data Models
  - Offline-First Design Patterns

references/argus-system.md
  - State Synchronization Strategy
  - Conflict Resolution
```

### 5. Design Patterns for IoT

Apply proven design patterns to IoT system implementation.

**Core Patterns:**

**Observer Pattern** - MQTT subscriptions for state changes
```python
# Devices publish state changes
# Services observe via MQTT subscriptions
topic: "device/{id}/state"
subscribers: notification-service, telemetry-service, ui-dashboard
```

**State Pattern** - Device operating modes
```python
# Timer device with work/break/idle states
# Each state encapsulates mode-specific behavior
class WorkState, BreakState, IdleState
```

**Strategy Pattern** - Different timer modes (Pomodoro, custom, countdown)
```python
# Interchangeable algorithms for timer duration calculation
class PomodoroStrategy, CustomStrategy, CountdownStrategy
```

**Factory Pattern** - Device-specific MQTT handlers
```python
# Create appropriate handler based on device type
HandlerFactory.create_handler('timer') → TimerHandler
HandlerFactory.create_handler('display') → DisplayHandler
```

**Singleton Pattern** - MQTT broker connection
```python
# Single shared connection to MQTT broker
MQTTConnectionManager.get_instance()
```

**Publish-Subscribe Pattern** - Core MQTT communication
```python
# One-to-many event distribution
Publisher → MQTT Broker → Multiple Subscribers
```

For detailed implementations and examples, read:
```
references/design-patterns.md
```

This reference includes complete code examples for:
- Observer, State, Strategy, Factory, Singleton patterns
- Publish-Subscribe, Command, Adapter patterns
- Proxy and Template Method patterns
- IoT-specific implementations and use cases

### 6. Scalability Planning

Design systems that scale from MVP to production loads.

**Scaling Dimensions:**
- Horizontal vs vertical scaling
- Load balancing strategies
- Database sharding for device data
- Caching strategies (Redis)
- Message queue sizing
- Connection pooling

**When to Apply:**
- Planning for growth beyond initial deployment
- Optimizing system performance under load
- Identifying bottlenecks
- Designing for multi-tenant scenarios
- Supporting increasing device counts

**Scaling Strategy Template:**

1. **Current Scale (MVP)**: Define baseline (devices, users, messages/sec)
2. **Near-Term Scale**: Plan for 10x growth
3. **Future Scale**: Envision 100x growth
4. **Bottlenecks**: Identify potential scaling limitations
5. **Mitigation**: Plan scaling approach for each bottleneck

**Example for Argus System:**
```
Current: 3 devices, 1 user, single location
Near-Term: 10 devices, 2 users, multiple rooms
Future: 50 devices, 10 users, multiple locations

Scaling Strategy:
- MQTT Broker: Vertical scaling, then clustering
- Timer Service: Horizontal scaling (stateless)
- Database: Vertical + read replicas
- Cache: Redis for shared state
```

For comprehensive scalability patterns, read:
```
references/microservices-scalability.md
  - Horizontal vs Vertical Scaling
  - Load Balancing Strategies
  - Database Sharding
  - Caching Strategies
  - Message Queue Sizing
  - Connection Pooling
```

### 7. Architecture Decision Records (ADRs)

Document significant architecture decisions with rationale and trade-offs.

**When to Create ADRs:**
- Choosing communication protocol (MQTT vs WebSocket vs HTTP)
- Selecting database technology
- Deciding on consistency model
- Adopting new technology or framework
- Making trade-offs with significant implications

**ADR Structure:**
1. **Context**: What forces drive this decision?
2. **Decision**: What are we doing?
3. **Rationale**: Why is this the right choice?
4. **Alternatives**: What else was considered?
5. **Consequences**: What are the trade-offs?
6. **Implementation Impact**: How does this affect the system?

**Using the ADR Template:**

Copy the ADR template to document decisions:
```
assets/adr-template.md
```

The template includes:
- Complete structure with all required sections
- Example filled-out ADR (MQTT for Device Communication)
- Guidance for each section
- Success metrics and follow-up actions

**Best Practices:**
- Create ADRs early in the decision process
- Include multiple alternatives with honest trade-offs
- Be specific about consequences (positive and negative)
- Define measurable success metrics
- Update ADRs as decisions evolve (revision history)

### 8. Architecture Visualization

Create clear diagrams to communicate system design.

**Diagram Types:**

**System Context Diagram** - High-level view of system and external actors
**Container Diagram** - System components and their interactions
**Sequence Diagram** - Message flow for specific scenarios
**State Diagram** - Device state machines
**Deployment Diagram** - Physical infrastructure layout

**Using Diagram Templates:**

PlantUML templates are provided for C4 model diagrams:
```
assets/c4-diagram-template.puml
```

Templates include:
- Container diagram (system components)
- Sequence diagram (message flow)
- Deployment diagram (infrastructure)
- State machine diagram (device states)
- Component diagram (internal structure)

**Generating Diagrams:**

Use PlantUML to render diagrams:
```bash
# Install PlantUML
apt install plantuml

# Generate diagram
plantuml diagram.puml
```

Online rendering available at: https://www.plantuml.com/plantuml/

**Customization:**
- Update component names and relationships
- Adjust styles and colors for device types
- Add notes for important details
- Use tags for visual grouping

## Architecture Workflow

### 1. Requirements Analysis

Identify system requirements and constraints:
- Functional requirements (what must the system do?)
- Non-functional requirements (performance, reliability, security)
- Technical constraints (hardware, connectivity, power)
- Business constraints (budget, timeline, resources)

### 2. Architecture Design

Apply capabilities from this skill:

1. **Choose topology**: Hub-and-spoke, mesh, or hybrid
2. **Design communication**: Protocol, topic structure, QoS
3. **Plan state management**: Consistency model, synchronization
4. **Apply patterns**: Identify relevant design patterns
5. **Plan for scale**: Anticipate growth and bottlenecks
6. **Design for failure**: Offline operation, recovery strategies

### 3. Documentation

Create architecture documentation:

1. **System diagrams**: Use C4 model templates
2. **ADRs**: Document key decisions
3. **Communication specs**: Topic structure, message formats
4. **State machines**: Define device operating modes
5. **API documentation**: REST/MQTT interface specs

### 4. Implementation

Implement architecture with best practices:

1. **Start with communication**: MQTT broker and topic structure
2. **Implement state management**: Local state + synchronization
3. **Add resilience**: Offline-first, retry logic, circuit breakers
4. **Instrument for observability**: Logging, metrics, monitoring
5. **Test edge cases**: Network failures, concurrent updates, scale

### 5. Iteration and Evolution

Continuously improve architecture:

1. **Monitor performance**: Latency, throughput, resource usage
2. **Validate decisions**: Review ADRs against actual metrics
3. **Identify bottlenecks**: Profile and optimize
4. **Plan evolution**: Create ADRs for significant changes
5. **Refactor incrementally**: Avoid big-bang rewrites

## Argus System as Reference Implementation

The Argus productivity tracking system serves as a concrete reference implementation demonstrating these architecture principles in practice.

**System Overview:**
- Multiple devices (Presto, T-Embed, Stream Deck, Android)
- Hub-and-spoke topology with Jetson Nano as central hub
- MQTT-based event-driven architecture
- Offline-first design with eventual consistency
- Microservices backend on Jetson Nano

**Key Architectural Decisions:**
- MQTT for device communication (low latency, pub/sub)
- Eventually consistent state (AP in CAP theorem)
- Edge processing for real-time responses
- Hub for coordination and intelligence

**Learning from Argus:**

Study the complete system architecture:
```
references/argus-system.md
```

This reference provides:
- Complete system architecture diagram
- Component details for each device
- Communication patterns and topic structure
- State synchronization strategy
- Failure modes and recovery
- Performance characteristics
- Security considerations
- Scalability path from MVP to production

Use Argus as a template for similar distributed IoT systems.

## Resources

### references/

In-depth documentation loaded into context as needed:

- **architecture-patterns.md**: Distributed systems patterns, communication architecture, consistency models, offline-first design
- **microservices-scalability.md**: Microservices decomposition, API design, resilience patterns, scaling strategies
- **design-patterns.md**: Implementation patterns with code examples (Observer, State, Strategy, Factory, Singleton, Pub/Sub)
- **argus-system.md**: Complete reference implementation with architecture diagrams, communication patterns, and implementation details

### assets/

Templates for architecture documentation and visualization:

- **adr-template.md**: Architecture Decision Record template with complete example (MQTT decision)
- **c4-diagram-template.puml**: PlantUML templates for system diagrams (container, sequence, deployment, state, component)

## Architecture Principles

Follow these principles when designing IoT systems:

1. **Loose Coupling**: Devices and services operate independently through well-defined interfaces
2. **High Cohesion**: Related functionality grouped together in components or services
3. **Fail-Safe**: Graceful degradation when components fail or network partitions occur
4. **Observability**: Comprehensive logging, metrics, and monitoring for debugging and optimization
5. **Maintainability**: Clear module boundaries, documentation, and testability
6. **Performance**: Meet real-time constraints with appropriate processing location and communication patterns
7. **Security**: Defense in depth with authentication, authorization, and encryption where appropriate

## Getting Started

To apply this skill to a new project:

1. **Define requirements**: Identify functional and non-functional requirements
2. **Study Argus**: Review the reference implementation for patterns
3. **Choose topology**: Select appropriate communication architecture
4. **Design communication**: Create MQTT topic structure and message formats
5. **Plan state management**: Define consistency model and synchronization approach
6. **Create ADRs**: Document key architecture decisions
7. **Generate diagrams**: Use C4 templates to visualize architecture
8. **Implement incrementally**: Start with core communication, add features iteratively
9. **Monitor and evolve**: Instrument system, gather metrics, refine architecture

For any architecture questions or trade-offs, consult the relevant reference documentation and apply the patterns and principles outlined in this skill.
