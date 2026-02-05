---
name: rpg-api-development
description: Use this skill when working on rpg-api codebase - provides layered architecture patterns, outside-in development, and integration with rpg-toolkit
---

# RPG API Development Skill

Use this skill when working on the rpg-api project to ensure consistency with established patterns and architecture.

## When to Use This Skill

- Working on rpg-api codebase
- Implementing gRPC handlers and services
- Creating orchestrators that integrate with rpg-toolkit
- Building repository layers for data persistence
- Mapping between proto messages and internal types

## Related Tools

**See also:**
- `/home/kirk/personal/.claude/agents/golang-architect/` - Go patterns and best practices
- `/home/kirk/personal/rpg-toolkit/.claude/skills/rpg-toolkit-development/` - Toolkit integration patterns

## Core Philosophy

**rpg-api stores data. rpg-toolkit handles rules. rpg-dnd5e-web renders data.**

This three-layer separation is fundamental:

### The Stack
```
rpg-dnd5e-web (React)  → Pure renderer, makes visual decisions from data
         ↕ (references + intent)
rpg-api                → Data-driven orchestrator, game-agnostic
         ↕ (toolkit calls)
rpg-toolkit            → Rules engine, knows D&D 5e mechanics
```

### Critical Principles

1. **API is Data-Driven**
   - Doesn't know what "rage" does
   - Processes references: `"dnd5e:features:rage"`
   - Calls toolkit: `feature.Activate(ref, context)`
   - Returns rich data for rendering

2. **API is NOT a Rules Engine**
   - ❌ Don't calculate attack bonuses in API
   - ❌ Don't validate "can barbarian rage?" in API
   - ❌ Don't implement feature mechanics in API
   - ✅ Let toolkit handle ALL game rules

3. **Return Data for Rendering**
   - Client needs rich breakdowns to make visual decisions
   - `damage_breakdown: [{source: "rage", amount: 2}]` → Client shows red glow
   - `monster_status: "bloodied"` → Client changes sprite color
   - Client is untrusted but can make rendering choices

4. **Use Toolkit Types Directly**
   - ❌ Don't create API-specific entities
   - ✅ Use `character.Data`, `combat.AttackResult` from toolkit
   - API stores toolkit types in Redis (as JSON)
   - **ONE conversion point**: toolkit types ↔ proto
   - No intermediate translation layers

**See `/home/kirk/personal/ARCHITECTURE.md` for complete architectural vision**

## Layered Architecture

### Layer Responsibilities

```
┌─────────────────────────────────────────────────┐
│ Handlers (gRPC)                                 │
│ - Validate requests                             │
│ - Call service layer                            │
│ - Convert responses to proto                    │
│ - NO business logic                             │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│ Services (Interfaces)                           │
│ - Define business logic contracts               │
│ - Input/Output types                            │
│ - Generated mocks for testing                   │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│ Orchestrators (Implementation)                  │
│ - Coordinate repositories                       │
│ - Integrate with rpg-toolkit                    │
│ - Handle workflows and state transitions        │
│ - Transform data between layers                 │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│ Repositories (Storage)                          │
│ - Storage abstraction                           │
│ - Redis, in-memory, etc.                        │
│ - Own ID generation and timestamps              │
└─────────────────────────────────────────────────┘
```

### Directory Structure

```
/cmd/server/              # Cobra commands, server startup
/internal/
  ├── entities/           # Simple data models (just structs)
  ├── handlers/           # gRPC handlers (API layer)
  │   └── dnd5e/
  │       └── v1alpha1/   # Proto version naming
  │           ├── character/
  │           │   ├── handler.go
  │           │   └── converters.go
  │           └── encounter/
  ├── orchestrators/      # Service interfaces + implementations
  │   ├── character/
  │   │   ├── service.go      # Interface with Input/Output types
  │   │   ├── orchestrator.go # Implementation
  │   │   └── mock/           # Generated mocks
  │   └── encounter/
  └── repositories/       # Storage interfaces and implementations
      ├── character/
      │   ├── repository.go   # Interface + types
      │   └── redis.go        # Implementation
      └── encounters/
```

## Development Approach: Outside-In

**Always work from the API inward, ONE LAYER AT A TIME.**

### Critical Rule: Tests Define Contracts

Each layer writes tests with mocked dependencies BEFORE implementing the next layer inward.

```
Handler (tests with mock service)
   ↓ defines contract
Service Interface
   ↓ implemented by
Orchestrator (tests with mock repos)
   ↓ defines contract
Repository Interface
   ↓ implemented by
Repository (tests with real storage)
```

### Step 1: Create Handler Stub

Return `codes.Unimplemented` initially:

```go
func (h *Handler) Attack(ctx context.Context, req *Request) (*Response, error) {
    return nil, status.Error(codes.Unimplemented, "not implemented")
}
```

**Why:** Validates proto definitions work, server can start.

### Step 2: Define Service Interface

Based on what handler needs:

```go
//go:generate mockgen -destination=mock/mock_service.go -package=encountermock github.com/KirkDiggler/rpg-api/internal/orchestrators/encounter Service

type Service interface {
    ResolveAttack(ctx context.Context, input *ResolveAttackInput) (*ResolveAttackOutput, error)
}

type ResolveAttackInput struct {
    EncounterID string
    AttackerID  string
    TargetID    string
}

type ResolveAttackOutput struct {
    Result *combat.AttackResult  // Toolkit type
    MonsterHP int
}
```

**Generate mocks:** `go generate ./internal/orchestrators/encounter/`

### Step 3: Implement Handler + Write Tests

**Update handler to call service:**

```go
func (h *Handler) Attack(ctx context.Context, req *AttackRequest) (*AttackResponse, error) {
    // Validate
    if req.GetEncounterId() == "" {
        return nil, status.Error(codes.InvalidArgument, "encounter_id required")
    }

    // Call service
    output, err := h.encounterService.ResolveAttack(ctx, &encounter.ResolveAttackInput{
        EncounterID: req.EncounterId,
        AttackerID:  req.AttackerId,
        TargetID:    req.TargetId,
    })
    if err != nil {
        return nil, status.Error(codes.Internal, err.Error())
    }

    // Convert to proto
    return &AttackResponse{
        Success: true,
        Result:  convertAttackResult(output.Result),
    }, nil
}
```

**Write tests with mocked service:**

```go
func (s *HandlerTestSuite) TestAttack_Success() {
    // Mock service behavior
    s.mockService.EXPECT().
        ResolveAttack(gomock.Any(), &encounter.ResolveAttackInput{
            EncounterID: "enc-1",
            AttackerID:  "char-1",
            TargetID:    "goblin-1",
        }).
        Return(&encounter.ResolveAttackOutput{
            Result: &combat.AttackResult{
                Hit:         true,
                TotalDamage: 10,
            },
            MonsterHP: 5,
        }, nil)

    // Call handler
    resp, err := s.handler.Attack(ctx, &AttackRequest{
        EncounterId: "enc-1",
        AttackerId:  "char-1",
        TargetId:    "goblin-1",
    })

    // Assert handler behavior
    s.Require().NoError(err)
    s.Assert().True(resp.Success)
    s.Assert().Equal(int32(10), resp.Result.Damage)
}
```

**Handler tests MUST pass before moving to orchestrator.**

### Step 4: Implement Orchestrator + Write Tests

**Now implement the service interface:**

```go
type Orchestrator struct {
    charRepo character.Repository
    encRepo  encounters.Repository
}

func (o *Orchestrator) ResolveAttack(ctx context.Context, input *ResolveAttackInput) (*ResolveAttackOutput, error) {
    // Implementation using mocked repos
}
```

**Write orchestrator tests with mocked repos:**

```go
func (s *OrchestratorTestSuite) TestResolveAttack_Success() {
    // Mock repo behavior
    s.mockCharRepo.EXPECT().Get(...)
    s.mockEncRepo.EXPECT().Get(...)

    // Call orchestrator
    output, err := s.orchestrator.ResolveAttack(ctx, input)

    // Assert orchestrator behavior
}
```

**Orchestrator tests MUST pass before implementing repos.**

### Step 5: Implement Repositories

Last layer - actual storage implementation.

## The Outside-In Workflow

```
1. Create handler stub (Unimplemented)
2. Define service interface (what handler needs)
3. Generate mocks
4. Implement handler + write handler tests (with mock service)
   ✅ Handler tests pass
5. Implement orchestrator + write orchestrator tests (with mock repos)
   ✅ Orchestrator tests pass
6. Implement repositories + write repo tests
   ✅ All tests pass
```

## Key Principle: Don't Skip Ahead

❌ **WRONG:** Create handler, define interface, implement orchestrator all at once

✅ **RIGHT:**
- Implement handler + tests with mocks
- Tests pass
- Then implement orchestrator + tests with mocks
- Tests pass
- Then implement repos

**Each layer proves its contract through tests BEFORE the next layer is implemented.**

## Key Patterns

### 1. Input/Output Types Everywhere

**This is the #1 principle.** Every function at every layer:

```go
// ❌ BAD
func CreateSession(name string, dmID string, maxPlayers int) (*Session, error)

// ✅ GOOD
func CreateSession(ctx context.Context, input *CreateSessionInput) (*CreateSessionOutput, error)
```

**Benefits:**
- No interface changes when adding fields
- No mock regeneration
- Future-proof for pagination
- Clear contracts between layers

### 2. Handler Pattern

Handlers are thin translation layers:

```go
func (h *Handler) Attack(ctx context.Context, req *AttackRequest) (*AttackResponse, error) {
    // 1. Validate request
    if req.GetEncounterId() == "" {
        return nil, status.Error(codes.InvalidArgument, "encounter_id is required")
    }

    // 2. Create service input
    input := &encounter.ResolveAttackInput{
        EncounterID: req.EncounterId,
        AttackerID:  req.AttackerId,
        TargetID:    req.TargetId,
    }

    // 3. Call service
    output, err := h.encounterService.ResolveAttack(ctx, input)
    if err != nil {
        return nil, status.Error(codes.Internal, err.Error())
    }

    // 4. Convert to proto response
    return &AttackResponse{
        Success: true,
        Result:  convertAttackResultToProto(output.Result),
    }, nil
}
```

**Key rules:**
- NO business logic in handlers
- Conversions in separate `converters.go` file
- Use `status.Error()` for gRPC error codes

### 3. Config Pattern

Every component uses config struct:

```go
type Config struct {
    CharacterRepo character.Repository
    EncounterRepo encounters.Repository
}

func (c *Config) Validate() error {
    if c.CharacterRepo == nil {
        return errors.New("CharacterRepo is required")
    }
    if c.EncounterRepo == nil {
        return errors.New("EncounterRepo is required")
    }
    return nil
}

func New(cfg *Config) (*Orchestrator, error) {
    if err := cfg.Validate(); err != nil {
        return nil, err
    }
    return &Orchestrator{
        charRepo: cfg.CharacterRepo,
        encRepo:  cfg.EncounterRepo,
    }, nil
}
```

### 4. Mock Organization

Following rpg-toolkit's pattern:

- **Location**: `mock/` subdirectory next to interface
- **Package naming**: `<parent>mock` (e.g., `charactermock`, `encountermock`)
- **File naming**: `mock_<interface>.go`
- **Generation**: `//go:generate` above interface

```go
// In service.go:
//go:generate mockgen -destination=mock/mock_service.go -package=charactermock github.com/KirkDiggler/rpg-api/internal/orchestrators/character Service

type Service interface {
    // ...
}

// Usage in tests:
mockService := charactermock.NewMockService(ctrl)
```

### 5. Repository Pattern

```go
type Repository interface {
    Get(ctx context.Context, input *GetInput) (*GetOutput, error)
    Save(ctx context.Context, input *SaveInput) (*SaveOutput, error)
    Update(ctx context.Context, input *UpdateInput) (*UpdateOutput, error)
    Delete(ctx context.Context, input *DeleteInput) (*DeleteOutput, error)
}

type GetInput struct {
    ID string
}

type GetOutput struct {
    CharacterData *character.Data
}
```

**Repository responsibilities:**
- Own ID generation
- Set timestamps
- Hide storage backend details
- Convert between storage format and domain types

### 6. Use Toolkit Types (No Internal Entities)

**Don't create API-specific entity types. Use toolkit types directly.**

```go
// ❌ WRONG: Creating internal entities
// /internal/entities/character.go
type Character struct {
    ID    string
    Name  string
    Level int
}

// ✅ RIGHT: Use toolkit types
import "github.com/KirkDiggler/rpg-toolkit/rulebooks/dnd5e/character"

type CharacterRepository interface {
    Get(ctx, input) (*GetOutput, error)
}

type GetOutput struct {
    CharacterData *character.Data  // Toolkit type
}

// Store toolkit type in Redis as JSON
func (r *RedisRepo) Save(ctx, input) error {
    json, _ := json.Marshal(input.CharacterData)  // character.Data
    r.client.Set(key, json)
}
```

**Why:**
- Toolkit defines canonical data structures
- API just stores/retrieves them
- One conversion point: toolkit ↔ proto
- No duplicate entity definitions
- No translation layers

### 7. Converter Pattern

Separate file for proto conversions:

```go
// converters.go
func convertAttackResultToProto(result *combat.AttackResult) *proto.AttackResult {
    return &proto.AttackResult{
        Hit:         result.Hit,
        AttackRoll:  int32(result.AttackRoll),
        AttackTotal: int32(result.TotalAttack),
        Damage:      int32(result.TotalDamage),
        DamageType:  result.DamageType,
        Critical:    result.Critical,
    }
}

func convertCharacterDataToProto(data *character.Data) *proto.Character {
    // ... conversion logic
}
```

**Why separate file:**
- Keeps handler code clean
- Easy to find conversion logic
- Reusable across multiple handlers

## RPG-Toolkit Integration

### Calling Toolkit from Orchestrators

```go
import (
    "github.com/KirkDiggler/rpg-toolkit/events"
    "github.com/KirkDiggler/rpg-toolkit/rulebooks/dnd5e/character"
    "github.com/KirkDiggler/rpg-toolkit/rulebooks/dnd5e/combat"
    "github.com/KirkDiggler/rpg-toolkit/rulebooks/dnd5e/monster"
)

func (o *Orchestrator) ResolveAttack(ctx context.Context, input *ResolveAttackInput) (*ResolveAttackOutput, error) {
    // 1. Create EventBus for combat interaction
    bus := events.NewEventBus()

    // 2. Load character with features
    charData, err := o.charRepo.Get(ctx, &character.GetInput{ID: input.AttackerID})
    if err != nil {
        return nil, err
    }

    // LoadFromData reconstructs Character with features subscribed to events
    char, err := character.LoadFromData(ctx, charData.CharacterData, bus)
    if err != nil {
        return nil, err
    }

    // 3. Reconstruct monster
    mon := monster.NewGoblin(input.TargetID)

    // 4. Call toolkit combat
    result, err := combat.ResolveAttack(ctx, &combat.AttackInput{
        Attacker:         char,
        Defender:         mon,
        Weapon:           weapon,
        AttackerScores:   char.AbilityScores(),
        DefenderAC:       mon.AC(),
        ProficiencyBonus: char.ProficiencyBonus(),
        EventBus:         bus,
        Roller:           dice.NewRoller(),
    })

    // 5. Persist updates
    if result.Hit {
        // Update monster HP in encounter state
    }

    return &ResolveAttackOutput{Result: result}, nil
}
```

### EventBus Lifecycle

**Critical**: Combat requires EventBus for event-driven features like Rage.

**Pattern:**
- Create fresh EventBus per combat interaction
- Load character with `character.LoadFromData(ctx, data, bus)`
- Character features auto-subscribe to combat events
- Pass same bus to `combat.ResolveAttack()`
- Features (like Rage) participate in damage chains

**Why not persist EventBus:**
- Stateless API design
- Fresh state per request
- No memory leaks from subscriptions

### Character Features Persistence

**Key finding**: Features ARE persisted in character.Data:

```go
type Data struct {
    // ... other fields
    Features   []json.RawMessage  // e.g., Rage feature
    Conditions []json.RawMessage  // e.g., Raging condition
}

// When saved
func (c *Character) ToData() *Data {
    data.Features = make([]json.RawMessage, 0, len(c.features))
    for _, feature := range c.features {
        jsonData, _ := feature.ToJSON()
        data.Features = append(data.Features, jsonData)
    }
    return data
}

// When loaded
func LoadFromData(ctx context.Context, d *Data, bus events.EventBus) (*Character, error) {
    // Reconstructs Feature objects from JSON
    for _, rawFeature := range d.Features {
        feature, _ := features.LoadJSON(rawFeature)
        char.features = append(char.features, feature)
    }

    // Character subscribes to events with features
    char.subscribeToEvents(ctx)
    return char, nil
}
```

**Implication**: Loading character from repo automatically includes Rage and other features, ready for combat.

## Testing Patterns

### Test Suite Pattern

Always use testify suites:

```go
type OrchestratorTestSuite struct {
    suite.Suite
    ctrl         *gomock.Controller
    mockCharRepo *charactermock.MockRepository
    mockEncRepo  *encountermock.MockRepository
    orchestrator *Orchestrator
}

func (s *OrchestratorTestSuite) SetupTest() {
    s.ctrl = gomock.NewController(s.T())
    s.mockCharRepo = charactermock.NewMockRepository(s.ctrl)
    s.mockEncRepo = encountermock.NewMockRepository(s.ctrl)

    s.orchestrator = New(&Config{
        CharacterRepo: s.mockCharRepo,
        EncounterRepo: s.mockEncRepo,
    })
}

func (s *OrchestratorTestSuite) TearDownTest() {
    s.ctrl.Finish()
}

func TestOrchestratorSuite(t *testing.T) {
    suite.Run(t, new(OrchestratorTestSuite))
}
```

### Handler Testing

```go
func (s *HandlerTestSuite) TestAttack_Success() {
    // Arrange
    expectedOutput := &encounter.ResolveAttackOutput{
        Result: &combat.AttackResult{
            Hit:         true,
            AttackRoll:  15,
            TotalAttack: 20,
            TotalDamage: 10,
        },
    }

    s.mockService.EXPECT().
        ResolveAttack(gomock.Any(), &encounter.ResolveAttackInput{
            EncounterID: "enc-1",
            AttackerID:  "char-1",
            TargetID:    "mon-1",
        }).
        Return(expectedOutput, nil)

    // Act
    resp, err := s.handler.Attack(context.Background(), &proto.AttackRequest{
        EncounterId: "enc-1",
        AttackerId:  "char-1",
        TargetId:    "mon-1",
    })

    // Assert
    s.Require().NoError(err)
    s.Assert().True(resp.Success)
    s.Assert().Equal(int32(10), resp.Result.Damage)
}
```

### Orchestrator Testing

```go
func (s *OrchestratorTestSuite) TestResolveAttack_CharacterWithRage() {
    // Arrange - Mock character repo
    charData := createTestCharacterWithRage()
    s.mockCharRepo.EXPECT().
        Get(gomock.Any(), &character.GetInput{ID: "char-1"}).
        Return(&character.GetOutput{CharacterData: charData}, nil)

    // Arrange - Mock encounter repo
    encData := createTestEncounter()
    s.mockEncRepo.EXPECT().
        Get(gomock.Any(), &encounters.GetInput{EncounterID: "enc-1"}).
        Return(&encounters.GetOutput{Data: encData}, nil)

    // Arrange - Expect HP update
    s.mockEncRepo.EXPECT().
        Update(gomock.Any(), gomock.Any()).
        Return(nil)

    // Act
    output, err := s.orchestrator.ResolveAttack(ctx, &ResolveAttackInput{
        EncounterID: "enc-1",
        AttackerID:  "char-1",
        TargetID:    "goblin-1",
    })

    // Assert
    s.Require().NoError(err)
    s.Assert().True(output.Result.Hit)
    // Rage should add +2 damage
    s.Assert().GreaterOrEqual(output.Result.DamageBonus, 2)
}
```

## Error Handling

### NEVER Return (nil, nil)

```go
// ❌ BAD - Never do this
if input == nil {
    return nil, nil
}

// ✅ GOOD - Return error
if input == nil {
    return nil, errors.New("input is required")
}

// ✅ GOOD - Return empty/default if valid
if items == nil {
    return &ListOutput{Items: []*Item{}, Total: 0}, nil
}
```

### Package-Level Errors

```go
var (
    ErrSessionNotFound    = errors.New("session not found")
    ErrCharacterNotFound  = errors.New("character not found")
    ErrEncounterNotFound  = errors.New("encounter not found")
)

// Wrap with context
return fmt.Errorf("failed to get session %s: %w", id, ErrSessionNotFound)
```

### gRPC Error Codes

```go
import "google.golang.org/grpc/codes"
import "google.golang.org/grpc/status"

// Map internal errors to gRPC codes
if errors.Is(err, ErrCharacterNotFound) {
    return nil, status.Error(codes.NotFound, err.Error())
}

if errors.Is(err, ErrInvalidInput) {
    return nil, status.Error(codes.InvalidArgument, err.Error())
}

// Generic internal error
return nil, status.Error(codes.Internal, err.Error())
```

## Common Mistakes to Avoid

1. ❌ Putting business logic in handlers
2. ❌ Calling repositories directly from handlers (skip service layer)
3. ❌ Not using Input/Output types
4. ❌ Mixing proto types into orchestrator layer
5. ❌ Forgetting to create EventBus for toolkit integration
6. ❌ Not loading characters with LoadFromData (features won't work)
7. ❌ Mocking entities instead of behaviors
8. ❌ Skipping handler tests with mocked services

## Development Workflow

### Pre-commit Checks

**ALWAYS** run before committing:
```bash
make pre-commit  # Runs fmt, tidy, lint, test
```

**NEVER use `git commit --no-verify`** - CI will fail anyway

### Local CI Checks

**ALWAYS** run before pushing:
```bash
make ci-check  # Detect CI failures locally
make ci-fix    # Auto-fix what can be fixed
```

### Feature Development Workflow

1. **Start from latest main**
   ```bash
   gcm  # git checkout main
   gl   # git pull
   ```

2. **Create feature branch**
   ```bash
   git checkout -b feat/attack-endpoint
   ```

3. **Follow outside-in development**
   - Handler stub → Service interface → Tests → Orchestrator → Repo

4. **Run tests continuously**
   ```bash
   go test ./...
   go test ./internal/orchestrators/encounter -v
   ```

5. **Run CI checks before push**
   ```bash
   make ci-check
   make ci-fix
   ```

6. **Create PR**
   ```bash
   git push origin feat/attack-endpoint
   gh pr create
   ```

## Quick Reference

### Creating a New Endpoint

1. **Verify proto exists** in rpg-api-protos
2. **Create handler** at `/internal/handlers/dnd5e/v1alpha1/<service>/`
3. **Define service interface** at `/internal/orchestrators/<service>/service.go`
4. **Generate mocks** with `//go:generate` and `go generate`
5. **Write handler tests** using mocked service
6. **Implement orchestrator** at `/internal/orchestrators/<service>/orchestrator.go`
7. **Wire to server** in `/cmd/server/server.go`

### Integrating with RPG-Toolkit

1. **Create EventBus** for the interaction
2. **Load character** with `LoadFromData(ctx, data, bus)`
3. **Construct toolkit entities** (Monster, Weapon, etc.)
4. **Call toolkit function** (combat.ResolveAttack, etc.)
5. **Persist results** back to repositories
6. **Return structured output** with Input/Output types

### Testing Checklist

- [ ] Handler tests with mocked service
- [ ] Orchestrator tests with mocked repos
- [ ] Request validation tests
- [ ] Error handling tests
- [ ] Proto conversion tests
- [ ] Integration test (optional, for complex flows)
