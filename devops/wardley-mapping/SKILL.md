---
name: wardley-mapping
description: "Wardley Mapping for strategic positioning and situational awareness. Covers value chain mapping, evolution stages, landscape analysis, gameplay patterns, and strategic decision-making. Use for technology strategy, competitive analysis, and architectural investment decisions."
allowed-tools: Read, Write, Glob, Grep, Task
---

# Wardley Mapping

A strategic mapping technique for understanding competitive landscape, technology evolution, and making informed architectural decisions.

## When to Use This Skill

**Keywords:** wardley map, value chain, evolution, genesis, custom, product, commodity, strategy, landscape, doctrine, gameplay, situational awareness, strategic positioning, technology radar

**Use this skill when:**

- Making technology investment decisions
- Evaluating build vs. buy vs. outsource
- Understanding competitive positioning
- Planning technology evolution strategy
- Communicating architecture strategy to stakeholders
- Identifying strategic opportunities and threats
- Deciding where to focus innovation efforts

## What is Wardley Mapping?

Wardley Mapping, created by Simon Wardley, provides situational awareness for strategic decision-making by visualizing:

1. **Value Chain**: Components needed to meet user needs
2. **Evolution**: How components change over time
3. **Landscape**: The competitive environment
4. **Movement**: How the landscape changes

### The Map Structure

```text
                    EVOLUTION

        Genesis    Custom     Product    Commodity
           ↓          ↓          ↓          ↓
        ┌──────────────────────────────────────────┐
        │                                          │
Visible │   User Need ●                            │  ← Anchor
        │       │                                  │
        │       ↓                                  │
        │   Component A ●──────────→ ●             │
        │       │                                  │
        │       ↓                                  │
        │   Component B    ●                       │
        │       │                                  │
Hidden  │       ↓                                  │
        │   Component C              ●             │
        │       │                                  │
        │       ↓                                  │
        │   Component D                       ●    │  ← Commodity
        │                                          │
        └──────────────────────────────────────────┘

        Y-axis: Visibility (to user)
        X-axis: Evolution (certainty)
```

## Evolution Stages

### Stage Characteristics

```yaml
evolution_stages:
  genesis:
    position: "Far left"
    characteristics:
      - "Novel, unique, uncertain"
      - "Poorly understood"
      - "High failure rates"
      - "Requires experimentation"
    activities:
      - "Research & development"
      - "Exploration"
      - "Proof of concepts"
    examples:
      - "Quantum computing (for most use cases)"
      - "Novel AI architectures"
      - "Experimental materials"

  custom_built:
    position: "Center-left"
    characteristics:
      - "Understood but unique implementation"
      - "Bespoke solutions"
      - "Differentiating"
      - "High cost, high expertise"
    activities:
      - "Custom development"
      - "Integration work"
      - "Specialized teams"
    examples:
      - "Custom recommendation engine"
      - "Bespoke trading platform"
      - "Specialized analytics"

  product:
    position: "Center-right"
    characteristics:
      - "Increasingly understood"
      - "Multiple vendors/options"
      - "Feature differentiation"
      - "Growing competition"
    activities:
      - "Buy vs. build decisions"
      - "Vendor evaluation"
      - "Configuration over coding"
    examples:
      - "CRM systems"
      - "E-commerce platforms"
      - "Analytics tools"

  commodity:
    position: "Far right"
    characteristics:
      - "Well understood"
      - "Essential, expected"
      - "Low differentiation"
      - "Volume operations"
    activities:
      - "Utility consumption"
      - "Cost optimization"
      - "Operational excellence"
    examples:
      - "Cloud compute (IaaS)"
      - "Email services"
      - "Payment processing"
```

### Evolution Indicators

| Indicator | Genesis | Custom | Product | Commodity |
|-----------|---------|--------|---------|-----------|
| **Ubiquity** | Rare | Rare-Common | Common | Widespread |
| **Certainty** | Uncertain | Uncertain-Defined | Defined | Defined |
| **Market** | Undefined | Forming | Mature | Utility |
| **Failure Mode** | Research | Learning | Differentiation | Operational |
| **Talent** | Pioneers | Settlers | Town Planners | Utilities |

## Creating a Wardley Map

### Step 1: Identify the Anchor

```yaml
anchor:
  definition: "The user need being served"

  questions:
    - "Who is the user?"
    - "What do they need?"
    - "What visible outcome do they expect?"

  placement: "Top of map, visible to user"

  examples:
    - "Customer needs to purchase products online"
    - "Developer needs to deploy applications"
    - "Analyst needs to generate reports"
```

### Step 2: Build the Value Chain

```yaml
value_chain:
  approach: "Work backwards from user need"

  questions:
    - "What components are needed to meet this need?"
    - "What does each component depend on?"
    - "What components are hidden from the user?"

  tips:
    - "List capabilities, not just technologies"
    - "Include people, practices, and data"
    - "Map both technical and business components"
    - "Dependencies flow downward"
```

### Step 3: Position on Evolution

```yaml
positioning:
  method: "Assess each component's evolution stage"

  criteria:
    - "How well understood is it?"
    - "How many alternatives exist?"
    - "Is it commoditized or unique?"
    - "What's the market maturity?"

  common_mistakes:
    - "Positioning based on age, not maturity"
    - "Confusing internal unfamiliarity with market genesis"
    - "Not considering industry context"
```

### Step 4: Add Movement

```yaml
movement:
  notation: "Arrows showing direction of evolution"

  types:
    natural_evolution: "→ Component moving right over time"
    inertia: "× Resistance to movement"
    acceleration: ">> Forced rapid evolution"

  considerations:
    - "All components evolve rightward over time"
    - "Evolution can be accelerated by competition"
    - "Inertia can slow movement"
```

## Map Template

```text
Title: {Map Name}
Anchor: {User Need}
Date: {ISO-8601}

                    Genesis    Custom     Product    Commodity
                       │          │          │          │
                       ▼          ▼          ▼          ▼
Visible            ┌───────────────────────────────────────┐
                   │                                       │
                   │  {User Need}                          │
                   │      │                                │
                   │      ↓                                │
                   │  {Component 1}    ●──────→            │
                   │      │                                │
                   │      ├───────────────┐                │
                   │      ↓               ↓                │
                   │  {Component 2}  {Component 3}         │
                   │      ●               ●                │
                   │      │               │                │
                   │      ↓               │                │
                   │  {Component 4}       │                │
                   │           ●          │                │
Hidden             │           │          │                │
                   │           ↓          ↓                │
                   │  {Component 5}───────┘                │
                   │                  ●                    │
                   │                                       │
                   └───────────────────────────────────────┘

Legend:
● = Current position
→ = Movement direction
× = Inertia
```

## Doctrine

Universally useful patterns for strategy:

```yaml
doctrine_categories:
  communication:
    - "Use a common language"
    - "Challenge assumptions"
    - "Focus on user needs"

  development:
    - "Use appropriate methods for evolution stage"
    - "Think small (cell-based structures)"
    - "Manage inertia"
    - "Use standards where appropriate"

  operation:
    - "Think fast, inexpensive, restrained, elegant"
    - "Manage failure appropriately"
    - "Optimize flow"

  learning:
    - "Use a systematic mechanism of learning"
    - "Know your users"
    - "Know your details"

  leading:
    - "Be the owner"
    - "Move fast"
    - "Accept that strategy is iterative"
```

### Doctrine Assessment Template

```yaml
doctrine_assessment:
  communication:
    common_language:
      score: "{1-5}"
      evidence: "{How is strategic language standardized?}"

    challenge_assumptions:
      score: "{1-5}"
      evidence: "{How are assumptions questioned?}"

  development:
    appropriate_methods:
      score: "{1-5}"
      evidence: "{Are agile/lean/six sigma applied contextually?}"

    cell_based:
      score: "{1-5}"
      evidence: "{Are teams small and autonomous?}"

  # ... continue for all doctrine points
```

## Gameplay Patterns

Strategic moves based on landscape understanding:

### Offensive Patterns

```yaml
offensive_gameplay:
  tower_and_moat:
    description: "Build differentiating capabilities on commodity foundation"
    when: "Strong custom components exist"
    action: "Commoditize dependencies, invest in differentiation"
    map_signature: "Custom components with commodity dependencies"

  land_and_expand:
    description: "Enter market with narrow offering, expand from there"
    when: "New market entry"
    action: "Start simple, add components over time"

  open_source_play:
    description: "Commoditize competitor's differentiator"
    when: "Competitor relies on custom component you can replicate"
    action: "Open source alternative to accelerate commoditization"

  ecosystem:
    description: "Create platform others build upon"
    when: "Control infrastructure component"
    action: "Enable others to build on your platform"

  two_factor:
    description: "Satisfy two markets with one platform"
    when: "Platform can serve multiple user types"
    action: "Connect both sides of a market"
```

### Defensive Patterns

```yaml
defensive_gameplay:
  patents_and_ip:
    description: "Protect innovations legally"
    when: "Genesis/custom stage innovations"
    action: "File patents, protect trade secrets"

  creating_constraint:
    description: "Slow evolution of component you control"
    when: "Evolution threatens your position"
    action: "Limit interoperability, create switching costs"

  embrace_and_extend:
    description: "Adopt standard then differentiate"
    when: "Commodity/product threatens differentiation"
    action: "Add proprietary extensions"
```

## Strategic Decisions

### Build vs. Buy vs. Outsource

```yaml
build_buy_outsource:
  build:
    when:
      - "Component in Genesis/Custom stage"
      - "Core differentiator"
      - "No suitable market alternatives"
      - "Strategic advantage from ownership"
    examples:
      - "Core recommendation algorithm"
      - "Proprietary trading logic"

  buy:
    when:
      - "Component in Product stage"
      - "Not core differentiator"
      - "Multiple vendor options exist"
      - "Faster time to market needed"
    examples:
      - "CRM system"
      - "Marketing automation"

  outsource:
    when:
      - "Component is Commodity"
      - "No differentiation possible"
      - "Volume economics favor specialists"
      - "Operational burden not worth it"
    examples:
      - "Cloud infrastructure"
      - "Payment processing"
      - "Email delivery"
```

### Innovation Investment

```yaml
innovation_investment:
  genesis:
    investment_type: "Exploration"
    approach: "Experiments, PoCs, research"
    metrics: "Learning velocity, options created"
    failure_tolerance: "High"

  custom:
    investment_type: "Differentiation"
    approach: "Product development, custom builds"
    metrics: "Feature completion, user adoption"
    failure_tolerance: "Medium"

  product:
    investment_type: "Enhancement"
    approach: "Integration, configuration"
    metrics: "Time to value, TCO"
    failure_tolerance: "Low"

  commodity:
    investment_type: "Optimization"
    approach: "Cost reduction, automation"
    metrics: "Cost per unit, availability"
    failure_tolerance: "Very low"
```

## .NET/C# Architecture Implications

### Evolution-Appropriate Development

```csharp
namespace Architecture.Strategy;

// Model for tracking component evolution
public record WardleyComponent
{
    public required string Name { get; init; }
    public required EvolutionStage Evolution { get; init; }
    public required double EvolutionPosition { get; init; } // 0.0 (Genesis) to 1.0 (Commodity)
    public required double Visibility { get; init; } // 0.0 (Hidden) to 1.0 (Visible)
    public List<string> DependsOn { get; init; } = [];
    public MovementDirection? Movement { get; init; }
    public bool HasInertia { get; init; }
    public string? StrategicNotes { get; init; }
}

public enum EvolutionStage
{
    Genesis,       // 0.0 - 0.25
    CustomBuilt,   // 0.25 - 0.50
    Product,       // 0.50 - 0.75
    Commodity      // 0.75 - 1.0
}

public enum MovementDirection
{
    None,
    Evolving,      // Natural rightward movement
    Accelerating,  // Faster than normal evolution
    Decelerating   // Inertia slowing evolution
}

public record WardleyMap
{
    public required string Title { get; init; }
    public required string Anchor { get; init; }
    public required string UserNeed { get; init; }
    public DateOnly MapDate { get; init; }
    public List<WardleyComponent> Components { get; init; } = [];
    public List<StrategicPlay> IdentifiedPlays { get; init; } = [];
}

public record StrategicPlay
{
    public required string Name { get; init; }
    public required GameplayPattern Pattern { get; init; }
    public required string Rationale { get; init; }
    public List<string> AffectedComponents { get; init; } = [];
    public string? ExpectedOutcome { get; init; }
    public string? RiskAssessment { get; init; }
}

public enum GameplayPattern
{
    TowerAndMoat,
    LandAndExpand,
    OpenSourcePlay,
    Ecosystem,
    TwoFactor,
    PatentsAndIp,
    CreatingConstraint,
    EmbraceAndExtend
}
```

### Evolution-Based Architecture Decisions

```csharp
public class ArchitectureAdvisor
{
    public ArchitectureRecommendation Recommend(WardleyComponent component)
    {
        return component.Evolution switch
        {
            EvolutionStage.Genesis => new ArchitectureRecommendation
            {
                DevelopmentApproach = "Experimental, spike-driven",
                TeamType = "Small, cross-functional pioneers",
                Architecture = "Loosely coupled, easily replaceable",
                Practices = ["Rapid prototyping", "High test coverage", "Feature flags"],
                InfrastructureApproach = "Containerized, easy to tear down"
            },

            EvolutionStage.CustomBuilt => new ArchitectureRecommendation
            {
                DevelopmentApproach = "Agile, iterative",
                TeamType = "Product-focused settlers",
                Architecture = "Vertical slices, bounded contexts",
                Practices = ["TDD", "CI/CD", "Observability"],
                InfrastructureApproach = "Managed services where possible"
            },

            EvolutionStage.Product => new ArchitectureRecommendation
            {
                DevelopmentApproach = "Configuration over custom code",
                TeamType = "Integration specialists",
                Architecture = "Adapter patterns, plugin architecture",
                Practices = ["Vendor evaluation", "Contract testing"],
                InfrastructureApproach = "SaaS/PaaS preferred"
            },

            EvolutionStage.Commodity => new ArchitectureRecommendation
            {
                DevelopmentApproach = "Operational excellence",
                TeamType = "SRE, platform engineering",
                Architecture = "Standard interfaces, utility patterns",
                Practices = ["Cost optimization", "Automation", "Monitoring"],
                InfrastructureApproach = "Utility services, serverless"
            },

            _ => throw new ArgumentOutOfRangeException()
        };
    }
}

public record ArchitectureRecommendation
{
    public required string DevelopmentApproach { get; init; }
    public required string TeamType { get; init; }
    public required string Architecture { get; init; }
    public List<string> Practices { get; init; } = [];
    public required string InfrastructureApproach { get; init; }
}
```

## Map Analysis Checklist

```yaml
analysis_checklist:
  completeness:
    - "Is the anchor (user need) clearly defined?"
    - "Are all components necessary to meet the need included?"
    - "Are dependencies shown?"
    - "Are movement arrows present?"

  positioning:
    - "Is each component positioned based on market evolution, not internal capability?"
    - "Are commodity components on the right?"
    - "Are genuinely novel components on the left?"

  insights:
    - "What components have inertia?"
    - "Where are there opportunities to commoditize?"
    - "What genesis activities could become differentiators?"
    - "Where do we have technical debt (building custom where products exist)?"

  strategic:
    - "What gameplay patterns apply?"
    - "Where should we invest vs. outsource?"
    - "What climatic patterns affect our landscape?"
    - "What doctrine weaknesses exist?"
```

## Output Format

### Wardley Map Document

```yaml
wardley_map:
  metadata:
    title: "{Map Name}"
    author: "{Author}"
    date: "{ISO-8601}"
    version: "1.0"
    scope: "{What this map covers}"

  anchor:
    user: "{User description}"
    need: "{User need statement}"

  components:
    - name: "{Component Name}"
      evolution: "{Genesis/Custom/Product/Commodity}"
      position: "{0.0-1.0}"
      visibility: "{0.0-1.0}"
      depends_on:
        - "{Dependency 1}"
        - "{Dependency 2}"
      notes: "{Strategic notes}"
      movement: "{evolving/accelerating/inertia/none}"

  analysis:
    opportunities:
      - "{Opportunity 1}"
      - "{Opportunity 2}"

    threats:
      - "{Threat 1}"
      - "{Threat 2}"

    inertia_points:
      - component: "{Component}"
        reason: "{Why inertia exists}"

  recommendations:
    immediate:
      - "{Action with rationale}"
    short_term:
      - "{Action with rationale}"
    long_term:
      - "{Action with rationale}"
```

## Integration with Other Skills

### Upstream

- **togaf-guidance** - Enterprise architecture context
- **gap-analysis** - Current vs. target state analysis
- **adr-management** - Document strategic decisions

### Downstream

- **team-topology-design** - Align teams with evolution stages
- **fitness-functions** - Measure evolution progress
- **cloud-alignment** - Cloud strategy by evolution stage

## References

For additional guidance:

- [Climatic Patterns](references/climatic-patterns.md)
- [Mapping Examples](references/mapping-examples.md)

## Version History

- v1.0.0 (2025-12-26): Initial release - Wardley Mapping skill

---

**Last Updated:** 2025-12-26
