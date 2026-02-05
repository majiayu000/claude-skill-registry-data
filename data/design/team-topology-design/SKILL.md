---
name: team-topology-design
description: "Team Topologies methodology for organizational design. Covers the four fundamental team types, three interaction modes, cognitive load assessment, Inverse Conway Maneuver, and team evolution patterns. Use when designing team structures that align with architecture."
allowed-tools: Read, Write, Glob, Grep, Task
---

# Team Topologies Design

A modern approach to team organization that optimizes for fast flow of change while managing cognitive load.

## When to Use This Skill

**Keywords:** team topologies, stream-aligned, platform, enabling, complicated subsystem, interaction mode, collaboration, x-as-a-service, facilitating, cognitive load, Inverse Conway, Conway's Law, team API, team boundaries, fast flow

**Use this skill when:**

- Designing or reorganizing team structures
- Aligning teams with software architecture
- Reducing cognitive load on teams
- Improving flow of change delivery
- Applying Inverse Conway Maneuver
- Defining team interactions and boundaries
- Planning organizational evolution

## Conway's Law

> "Any organization that designs a system will produce a design whose structure is a copy of the organization's communication structure."
> — Melvin Conway, 1968

### Implications

```yaml
conways_law:
  observation: "Architecture mirrors communication structures"

  implications:
    - "Team structure shapes system architecture"
    - "Siloed teams create siloed systems"
    - "Cross-functional teams create integrated systems"
    - "Team boundaries become system boundaries"

  inverse_conway:
    principle: "Design the organization to match the desired architecture"
    approach: "If you want a certain system architecture, structure teams accordingly"
    warning: "Architecture and team structure will drift back together over time"
```

## The Four Team Types

### 1. Stream-Aligned Team

```yaml
stream_aligned:
  definition: "Team aligned to a single, valuable stream of work"

  characteristics:
    - "End-to-end responsibility for a flow of value"
    - "Cross-functional (dev, ops, test, UX, etc.)"
    - "Long-lived, product-focused"
    - "Owns one or more bounded contexts"
    - "Primary team type (majority of teams)"

  size: "5-9 members"

  examples:
    - "Customer onboarding team"
    - "Checkout experience team"
    - "Mobile app team"
    - "B2B integration team"

  owns:
    - "Customer-facing features"
    - "Specific user journeys"
    - "Bounded context(s)"
    - "Full software lifecycle"

  does_not_own:
    - "Shared infrastructure"
    - "Complex specialist components"
    - "Cross-cutting capabilities"

  success_metrics:
    - "Lead time for changes"
    - "Deployment frequency"
    - "Customer satisfaction"
    - "Time to restore service"
```

### 2. Platform Team

```yaml
platform_team:
  definition: "Team providing internal services to reduce cognitive load on stream-aligned teams"

  characteristics:
    - "Treats internal teams as customers"
    - "Provides self-service capabilities"
    - "Focuses on developer experience"
    - "Operates as internal product team"
    - "Reduces duplication across teams"

  size: "5-9 members (can scale with platform size)"

  examples:
    - "Developer platform team"
    - "Infrastructure team"
    - "Data platform team"
    - "ML platform team"

  provides:
    - "Self-service infrastructure"
    - "CI/CD pipelines"
    - "Monitoring and observability"
    - "Common libraries and frameworks"

  does_not_do:
    - "Build features for end users"
    - "Dictate how teams work"
    - "Create bottlenecks"

  success_metrics:
    - "Time to provision resources"
    - "Platform adoption rate"
    - "Developer satisfaction score"
    - "Reduction in support tickets"
```

### 3. Enabling Team

```yaml
enabling_team:
  definition: "Team helping stream-aligned teams adopt new capabilities"

  characteristics:
    - "Temporary engagement with other teams"
    - "Upskills rather than builds"
    - "Identifies patterns and best practices"
    - "Cross-pollinates knowledge"
    - "Limited lifespan with each team"

  size: "3-6 members (small, specialized)"

  examples:
    - "DevOps enablement team"
    - "Security champions team"
    - "Architecture guidance team"
    - "Agile coaching team"

  activities:
    - "Training and workshops"
    - "Pair programming / mob sessions"
    - "Creating guides and playbooks"
    - "Identifying impediments"

  does_not_do:
    - "Build production systems"
    - "Permanent embedding"
    - "Gatekeeping"

  engagement_pattern:
    initial: "Assess team needs"
    active: "Collaborate intensively (weeks)"
    handoff: "Leave team self-sufficient"
    follow_up: "Periodic check-ins"

  success_metrics:
    - "Capability adoption rate"
    - "Time to team independence"
    - "Practice spread across org"
```

### 4. Complicated Subsystem Team

```yaml
complicated_subsystem:
  definition: "Team responsible for component requiring deep specialist knowledge"

  characteristics:
    - "Heavy specialist expertise required"
    - "Complexity would overwhelm stream teams"
    - "Clear interfaces to other teams"
    - "Rare team type (most orgs have 0-2)"

  size: "3-9 members (specialist-heavy)"

  examples:
    - "Video encoding team"
    - "Financial modeling team"
    - "Machine learning algorithm team"
    - "Real-time data processing team"

  when_appropriate:
    - "Math/science-heavy components"
    - "Regulatory complexity"
    - "Deep domain expertise"
    - "Years of specialized learning needed"

  when_inappropriate:
    - "General complexity any team could learn"
    - "Components that should be platform"
    - "Historical knowledge hoarding"

  success_metrics:
    - "Interface stability"
    - "Accuracy/performance of subsystem"
    - "Support burden on consumers"
```

## The Three Interaction Modes

### Collaboration

```yaml
collaboration_mode:
  definition: "Two teams working closely together on a shared goal"

  characteristics:
    - "High bandwidth communication"
    - "Shared discovery and innovation"
    - "Blurred boundaries temporarily"
    - "Intensive but time-boxed"

  appropriate_for:
    - "Rapid discovery phases"
    - "New integrations"
    - "Novel problems"
    - "Building shared understanding"

  duration: "Time-limited (weeks to months)"

  warning_signs:
    - "Collaboration lasting more than 6 months"
    - "Permanent dependency"
    - "Teams can't work independently"

  transition_to: "X-as-a-Service after discovery"
```

### X-as-a-Service

```yaml
xaas_mode:
  definition: "One team provides service to another with clear interface"

  characteristics:
    - "Clear API/contract"
    - "Minimal coordination needed"
    - "Provider team owns service evolution"
    - "Consumer team uses without deep involvement"

  appropriate_for:
    - "Mature, stable interfaces"
    - "Platform to stream-aligned"
    - "Reducing cognitive load"
    - "Scaling interactions"

  success_factors:
    - "Well-documented API"
    - "Self-service provisioning"
    - "SLA agreements"
    - "Clear support channels"

  anti_patterns:
    - "Too many meetings for simple requests"
    - "Ticket queue for everything"
    - "Hidden complexity"
```

### Facilitating

```yaml
facilitating_mode:
  definition: "One team helps another learn or adopt capabilities"

  characteristics:
    - "Teaching over doing"
    - "Temporary, with handoff"
    - "Goal is independence"
    - "Enabling team primary mode"

  appropriate_for:
    - "Capability building"
    - "New practice adoption"
    - "Impediment removal"
    - "Cross-pollination"

  engagement_cycle:
    assess: "Understand team needs"
    teach: "Active coaching/training"
    support: "Available for questions"
    exit: "Team is self-sufficient"

  anti_patterns:
    - "Permanent dependency"
    - "Doing work for them"
    - "Gatekeeping knowledge"
```

## Cognitive Load

### Types of Cognitive Load

```yaml
cognitive_load_types:
  intrinsic:
    definition: "Load from the problem space itself"
    examples:
      - "Business domain complexity"
      - "Technical complexity of task"
      - "Regulatory requirements"
    strategy: "Can't eliminate, but can train for it"

  extraneous:
    definition: "Load from environment/process"
    examples:
      - "Legacy system quirks"
      - "Poor tooling"
      - "Unclear requirements"
    strategy: "Minimize through platforms, automation"

  germane:
    definition: "Load from learning and growing"
    examples:
      - "Learning new technologies"
      - "Exploring new domains"
      - "Building mental models"
    strategy: "Invest in this - it builds capability"
```

### Cognitive Load Assessment

```yaml
cognitive_load_assessment:
  questions:
    domain_complexity:
      - "How many domains does the team own?"
      - "How deep is the domain knowledge required?"
      - "How often do domain rules change?"

    technical_complexity:
      - "How many systems does the team maintain?"
      - "What's the technology diversity?"
      - "How much legacy code exists?"

    environmental_friction:
      - "How much time spent on non-value work?"
      - "How many other teams must be coordinated with?"
      - "How painful is the deployment process?"

  scoring:
    1_3: "Manageable - team can focus on value"
    4_6: "Elevated - some overhead impacting flow"
    7_9: "Overloaded - need to reduce scope"
    10: "Critical - team cannot function effectively"

  red_flags:
    - "Team owns more than 3 bounded contexts"
    - "More than 50% time on coordination"
    - "High defect rate from context switching"
    - "Burnout indicators"
```

### Team Size Heuristics

```yaml
team_sizing:
  dunbar_numbers:
    5: "Core working group"
    15: "Extended team with coordination"
    50: "Department boundary"
    150: "Organization boundary"

  two_pizza_rule:
    description: "Team should be fed by two pizzas"
    practical_size: "5-9 members"
    rationale: "Communication overhead grows exponentially"

  brooks_law:
    statement: "Adding people to late project makes it later"
    implication: "Teams should be right-sized from start"
```

## Inverse Conway Maneuver

### Principle

```yaml
inverse_conway:
  definition: "Design organization to achieve desired architecture"

  process:
    1: "Define desired target architecture"
    2: "Identify bounded contexts and their relationships"
    3: "Design team structure to mirror desired architecture"
    4: "Allow teams to evolve the architecture they own"

  example:
    desired_architecture: "Independent microservices with clear boundaries"
    team_design: "Stream-aligned teams owning 1-2 services each"
    platform: "Shared infrastructure as platform team"
    result: "Architecture naturally evolves to match team structure"
```

### Implementation Steps

```yaml
inverse_conway_implementation:
  step_1_architecture_vision:
    activities:
      - "Define target bounded contexts"
      - "Map integration patterns between contexts"
      - "Identify shared capabilities (platform)"
      - "Document interfaces and dependencies"
    output: "Target architecture diagram with boundaries"

  step_2_team_mapping:
    activities:
      - "Map bounded contexts to potential teams"
      - "Identify platform team needs"
      - "Assess enabling team requirements"
      - "Flag complicated subsystem candidates"
    output: "Initial team structure proposal"

  step_3_cognitive_load_validation:
    activities:
      - "Assess load per proposed team"
      - "Adjust scope if overloaded"
      - "Validate skill availability"
      - "Plan for enabling support"
    output: "Validated team structure"

  step_4_interaction_design:
    activities:
      - "Define initial interaction modes"
      - "Identify collaboration needs"
      - "Design platform interfaces"
      - "Plan team APIs"
    output: "Team interaction map"

  step_5_evolution_plan:
    activities:
      - "Define transition timeline"
      - "Plan skill development"
      - "Design feedback mechanisms"
      - "Establish review cadence"
    output: "Organization transition roadmap"
```

## Team API

### Definition

```yaml
team_api:
  definition: "Explicit interface for how other teams interact with a team"

  components:
    service_offerings:
      - "What the team provides"
      - "How to consume services"
      - "SLAs and commitments"

    communication:
      - "Primary contact channels"
      - "Response time expectations"
      - "Escalation paths"

    ways_of_working:
      - "Collaboration preferences"
      - "Meeting availability"
      - "Decision-making process"

    code_and_artifacts:
      - "Repository locations"
      - "Documentation"
      - "API specifications"

  benefits:
    - "Reduces ambiguity"
    - "Scales interactions"
    - "Enables asynchronous work"
    - "Supports team autonomy"
```

### Team API Template

```markdown
# Team API: {Team Name}

## Mission
{Team's purpose in 1-2 sentences}

## Services We Provide
| Service | Description | How to Request | SLA |
|---------|-------------|----------------|-----|
| {Service} | {What it does} | {Channel} | {Response time} |

## What We Own
- {Bounded context(s)}
- {Systems/repos}
- {Documentation location}

## Interaction Preferences
- **Preferred contact:** {Slack channel, email, etc.}
- **Office hours:** {When available for synchronous discussion}
- **Request process:** {How to make requests}

## Current Interaction Modes
| Team | Mode | Duration | Notes |
|------|------|----------|-------|
| {Team} | {Collaboration/X-as-a-Service/Facilitating} | {Timeframe} | {Context} |

## Dependencies
### We Depend On
- {Team/Service}: {What we need}

### Who Depends On Us
- {Team}: {What they need from us}

## Metrics We Track
- {Metric 1}
- {Metric 2}

## Feedback Channels
- {How to provide feedback}
```

## Team Evolution Patterns

### Evolution Triggers

```yaml
evolution_triggers:
  growing_load:
    signal: "Team cognitive load increasing"
    options:
      - "Split team along bounded contexts"
      - "Create platform team for shared concerns"
      - "Spin off complicated subsystem"

  maturing_collaboration:
    signal: "Collaboration mode lasting too long"
    action: "Transition to X-as-a-Service"

  repeated_enablement:
    signal: "Same capability needed by multiple teams"
    action: "Move to platform team"

  specialist_bottleneck:
    signal: "Specialist knowledge creating bottleneck"
    options:
      - "Create complicated subsystem team"
      - "Enable teams to build capability"
```

### Splitting Teams

```yaml
team_splitting:
  when_to_split:
    - "Team owns too many bounded contexts (>3)"
    - "Cognitive load consistently high"
    - "Team size exceeding 9"
    - "Clear domain boundary exists"

  how_to_split:
    identify_boundary: "Find natural seam in domain/code"
    ensure_viability: "Each new team must be viable alone"
    plan_transition: "Gradual handoff, not big bang"
    maintain_interfaces: "Keep X-as-a-Service with old team"

  anti_patterns:
    - "Splitting by technology layer (UI team, API team)"
    - "Splitting without clear ownership"
    - "Creating too many tiny teams"
```

### Team Merging

```yaml
team_merging:
  when_to_merge:
    - "Too much collaboration overhead"
    - "Teams too small to be effective"
    - "Bounded contexts closely related"
    - "Artificial boundaries causing friction"

  how_to_merge:
    assess_fit: "Will combined load be manageable?"
    plan_integration: "How will skills combine?"
    redefine_scope: "New team's bounded context(s)"
    update_interactions: "Revise team API"
```

## .NET/C# Context

### Team-to-Architecture Alignment

```csharp
namespace Organization.TeamDesign;

// Model for team topology design
public record Team
{
    public required string Name { get; init; }
    public required TeamType Type { get; init; }
    public required string Mission { get; init; }
    public required int Size { get; init; }
    public List<string> BoundedContexts { get; init; } = [];
    public CognitiveLoadAssessment? CognitiveLoad { get; init; }
    public TeamApi? Api { get; init; }
}

public enum TeamType
{
    StreamAligned,
    Platform,
    Enabling,
    ComplicatedSubsystem
}

public record TeamInteraction
{
    public required string FromTeam { get; init; }
    public required string ToTeam { get; init; }
    public required InteractionMode Mode { get; init; }
    public string? Purpose { get; init; }
    public DateOnly? StartDate { get; init; }
    public DateOnly? PlannedEndDate { get; init; }
}

public enum InteractionMode
{
    Collaboration,
    XAsAService,
    Facilitating
}

public record CognitiveLoadAssessment
{
    public required DateOnly AssessmentDate { get; init; }
    public required int DomainComplexityScore { get; init; } // 1-10
    public required int TechnicalComplexityScore { get; init; } // 1-10
    public required int EnvironmentalFrictionScore { get; init; } // 1-10
    public int TotalScore => DomainComplexityScore +
                             TechnicalComplexityScore +
                             EnvironmentalFrictionScore;
    public LoadLevel Level => TotalScore switch
    {
        <= 9 => LoadLevel.Manageable,
        <= 18 => LoadLevel.Elevated,
        <= 24 => LoadLevel.High,
        _ => LoadLevel.Critical
    };
    public string? Notes { get; init; }
    public List<string> Recommendations { get; init; } = [];
}

public enum LoadLevel
{
    Manageable,
    Elevated,
    High,
    Critical
}

public record TeamApi
{
    public required string TeamName { get; init; }
    public required string Mission { get; init; }
    public List<ServiceOffering> Services { get; init; } = [];
    public CommunicationPreferences? Communication { get; init; }
    public List<string> OwnedSystems { get; init; } = [];
    public List<Dependency> DependsOn { get; init; } = [];
    public List<Dependency> DependedOnBy { get; init; } = [];
}

public record ServiceOffering(
    string Name,
    string Description,
    string RequestChannel,
    string Sla
);

public record CommunicationPreferences(
    string PreferredChannel,
    string OfficeHours,
    string RequestProcess
);

public record Dependency(
    string TeamName,
    string Description
);
```

### Team Topology Analyzer

```csharp
public class TeamTopologyAnalyzer
{
    public TeamTopologyAssessment Analyze(IEnumerable<Team> teams, IEnumerable<TeamInteraction> interactions)
    {
        var teamList = teams.ToList();
        var interactionList = interactions.ToList();

        return new TeamTopologyAssessment
        {
            TotalTeams = teamList.Count,
            TeamsByType = teamList.GroupBy(t => t.Type)
                .ToDictionary(g => g.Key, g => g.Count()),
            StreamAlignedRatio = CalculateStreamAlignedRatio(teamList),
            CognitiveLoadWarnings = IdentifyCognitiveLoadWarnings(teamList),
            InteractionConcerns = IdentifyInteractionConcerns(interactionList),
            Recommendations = GenerateRecommendations(teamList, interactionList)
        };
    }

    private decimal CalculateStreamAlignedRatio(List<Team> teams)
    {
        if (teams.Count == 0) return 0;
        var streamAligned = teams.Count(t => t.Type == TeamType.StreamAligned);
        return (decimal)streamAligned / teams.Count;
    }

    private List<string> IdentifyCognitiveLoadWarnings(List<Team> teams)
    {
        var warnings = new List<string>();

        foreach (var team in teams)
        {
            if (team.CognitiveLoad?.Level >= LoadLevel.High)
            {
                warnings.Add($"Team '{team.Name}' has {team.CognitiveLoad.Level} cognitive load");
            }

            if (team.BoundedContexts.Count > 3)
            {
                warnings.Add($"Team '{team.Name}' owns {team.BoundedContexts.Count} bounded contexts (recommended max: 3)");
            }

            if (team.Size > 9)
            {
                warnings.Add($"Team '{team.Name}' has {team.Size} members (exceeds two-pizza size)");
            }
        }

        return warnings;
    }

    private List<string> IdentifyInteractionConcerns(List<TeamInteraction> interactions)
    {
        var concerns = new List<string>();

        // Check for long-running collaborations
        var longCollaborations = interactions
            .Where(i => i.Mode == InteractionMode.Collaboration)
            .Where(i => i.StartDate.HasValue &&
                        i.StartDate.Value.AddMonths(6) < DateOnly.FromDateTime(DateTime.Today));

        foreach (var collab in longCollaborations)
        {
            concerns.Add($"Collaboration between '{collab.FromTeam}' and '{collab.ToTeam}' may be lasting too long - consider transitioning to X-as-a-Service");
        }

        return concerns;
    }

    private List<string> GenerateRecommendations(List<Team> teams, List<TeamInteraction> interactions)
    {
        var recommendations = new List<string>();

        // Check stream-aligned ratio
        var ratio = CalculateStreamAlignedRatio(teams);
        if (ratio < 0.6m)
        {
            recommendations.Add("Consider increasing stream-aligned team ratio (currently " +
                              $"{ratio:P0}, recommended 60-80%)");
        }

        // Check for missing platform teams
        var hasInfraOverhead = teams
            .Where(t => t.Type == TeamType.StreamAligned)
            .Any(t => t.CognitiveLoad?.EnvironmentalFrictionScore > 5);

        if (hasInfraOverhead && !teams.Any(t => t.Type == TeamType.Platform))
        {
            recommendations.Add("Consider creating a platform team to reduce infrastructure cognitive load on stream-aligned teams");
        }

        return recommendations;
    }
}

public record TeamTopologyAssessment
{
    public int TotalTeams { get; init; }
    public Dictionary<TeamType, int> TeamsByType { get; init; } = new();
    public decimal StreamAlignedRatio { get; init; }
    public List<string> CognitiveLoadWarnings { get; init; } = [];
    public List<string> InteractionConcerns { get; init; } = [];
    public List<string> Recommendations { get; init; } = [];
}
```

## Output Format

### Team Topology Document

```yaml
team_topology:
  metadata:
    organization: "{Org Name}"
    date: "{ISO-8601}"
    version: "1.0"

  teams:
    stream_aligned:
      - name: "{Team Name}"
        mission: "{Mission}"
        bounded_contexts:
          - "{Context 1}"
        size: {N}
        cognitive_load: "{Manageable/Elevated/High}"

    platform:
      - name: "{Platform Team}"
        mission: "{Mission}"
        services:
          - "{Service 1}"
        size: {N}

    enabling:
      - name: "{Enabling Team}"
        focus: "{Current focus area}"
        engaged_with:
          - "{Team 1}"
        size: {N}

    complicated_subsystem:
      - name: "{Subsystem Team}"
        domain: "{Specialty domain}"
        interfaces_to:
          - "{Consumer team 1}"
        size: {N}

  interactions:
    - from: "{Team A}"
      to: "{Team B}"
      mode: "{Collaboration/X-as-a-Service/Facilitating}"
      purpose: "{Why this interaction}"
      status: "{Active/Planned/Ending}"

  evolution_plans:
    - trigger: "{What triggers change}"
      action: "{What will change}"
      timeline: "{When}"
```

## Integration with Other Skills

### Upstream

- **context-mapping** - Bounded context → team mapping
- **wardley-mapping** - Evolution stage → team type alignment
- **togaf-guidance** - Enterprise architecture context

### Downstream

- **modular-architecture** - Code organization matching teams
- **fitness-functions** - Team boundary enforcement
- **adr-management** - Document team structure decisions

## References

For additional guidance:

- [Anti-Patterns](references/team-anti-patterns.md)
- [Assessment Templates](references/assessment-templates.md)

## Version History

- v1.0.0 (2025-12-26): Initial release - Team Topology Design skill

---

**Last Updated:** 2025-12-26
