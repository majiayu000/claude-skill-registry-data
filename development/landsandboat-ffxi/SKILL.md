---
name: landsandboat-ffxi
description: Expert knowledge of Final Fantasy XI private server development using LandSandBoat codebase. Use when working with FFXI game mechanics, LandSandBoat source code, database schema, Lua scripting, GM tools, or server administration.
allowed-tools: Read, Grep, Glob, WebFetch, Bash, Edit, Write
---

# LandSandBoat FFXI Development Skill

Expert knowledge base for Final Fantasy XI private server development using the LandSandBoat codebase.

## When to Activate This Skill

Claude should activate this skill when the user's request involves:

- **LandSandBoat Development**: Server configuration, troubleshooting, or modifications
- **FFXI Game Mechanics**: Combat systems, status effects, abilities, magic, crafting
- **Database Work**: Schema design, queries, character data, game data tables
- **Lua Scripting**: Zone scripts, NPCs, quests, missions, mob behaviors
- **GM Tools & APIs**: Building admin tools, player management, server utilities
- **Network Protocols**: FFXI packet structures, IPC, HTTP API integration
- **Server Architecture**: Understanding multi-process design, ZeroMQ, C++20 implementation

## Available Documentation

This skill provides comprehensive reference documentation in the `docs/` directory:

### Core Documentation Files

1. **architecture-overview.md** (24 KB)
   - Multi-process server design (login, map, world, search servers)
   - Technology stack (C++20, Lua, MariaDB, ZeroMQ)
   - Build system and configuration
   - Module system for extensions

2. **gameplay-systems.md** (32 KB)
   - Combat system (physical, magical, ranged)
   - Entity system (characters, mobs, NPCs, pets, trusts)
   - Status effects and buffs
   - Quest and mission systems
   - Zone management and navigation
   - NPC interaction patterns

3. **database.md** (56 KB) - **Primary reference for database work**
   - Complete schema documentation for 126+ tables
   - Table relationships and foreign keys
   - Character data structures
   - Game data (items, mobs, abilities, spells)
   - Economy systems (auction house, synth recipes)
   - Binary blob field documentation

4. **networking.md** (28 KB)
   - Network architecture and ports
   - IPC via ZeroMQ (localhost:54003)
   - Optional HTTP API (disabled by default)
   - Packet structures (C2S and S2C)
   - Security considerations

5. **scripting.md** (16 KB)
   - Lua integration architecture
   - Zone script structure (OnInitialize, OnZoneIn, onTrigger, etc.)
   - Entity interaction patterns
   - Common scripting patterns and examples
   - Enumerations and constants

6. **utilities.md** (8 KB)
   - Python development tools (dbtool.py, announce.py, etc.)
   - Database management utilities
   - CI/CD tools and testing utilities

## Setup Instructions

### First-Time Setup

When this skill is first activated, verify if the LandSandBoat reference codebase is available:

1. **Check for reference directory**: Look for `reference/` directory in the skill folder
2. **If missing**: Offer to run the setup script to clone the complete LandSandBoat codebase
3. **Run setup**: Execute `./scripts/setup-reference.sh` from the skill directory

The reference directory provides:
- Complete C++20 source code (~26% of codebase)
- All 297 zone Lua scripts (~63% of codebase)
- 126+ SQL schema files
- Python development tools
- Configuration examples

### Path References

All documentation and reference paths use the pattern: `landsandboat-skill/path/to/file`

Examples:
- `landsandboat-skill/docs/database.md` - Database schema reference
- `landsandboat-skill/reference/src/map/zone.cpp` - Zone C++ implementation
- `landsandboat-skill/reference/scripts/zones/` - Zone Lua scripts

## Working with This Skill

### Strategy for Different Tasks

#### Building GM Tools or APIs

1. **Start with architecture**: Read `docs/architecture-overview.md` to understand server processes
2. **Database access**: Reference `docs/database.md` for schema (tables, relationships, constraints)
3. **Network options**: Check `docs/networking.md` for:
   - Direct database access (most common)
   - HTTP API integration (if enabled)
   - ZeroMQ IPC (for advanced server integration)
4. **Examples**: Review `reference/tools/*.py` for Python tool patterns

**Recommended stack**: TypeScript + TanStack Query for modern API development

#### Lua Scripting

1. **Patterns**: Read `docs/scripting.md` for architecture and common patterns
2. **Reference code**: Browse `reference/scripts/zones/` for real examples
3. **Enumerations**: Check `reference/scripts/enum/` for game constants
4. **Globals**: Review `reference/scripts/globals/` for shared functions

#### Understanding Game Mechanics

1. **Overview**: Start with `docs/gameplay-systems.md` for high-level concepts
2. **C++ implementation**: Reference `reference/src/map/` for core engine logic
3. **Lua formulas**: Check `reference/scripts/globals/` for damage calculations, status effects
4. **Database data**: Query game data tables documented in `docs/database.md`

#### Database Design & Queries

1. **Schema reference**: Use `docs/database.md` as primary reference (56 KB, comprehensive)
2. **Table relationships**: Understand foreign keys (e.g., `charid` → `chars.charid`)
3. **Binary blobs**: Character missions, abilities, key items stored as binary (see schema docs)
4. **Constraints**: Respect game limits (inventory slots, stacking, job restrictions)
5. **Transactions**: Always use transactions for multi-table modifications

#### Network Protocol & Packets

1. **Architecture**: Read `docs/networking.md` for multi-server communication
2. **Packet definitions**: Reference `reference/src/map/packets/` for C++ structures
3. **IPC patterns**: Check `reference/src/common/ipc.h` for message types
4. **Security**: Note that IPC is localhost-only, HTTP API disabled by default

## Important Considerations

### Data Integrity

- Character data has complex interdependencies across multiple tables
- Binary blob fields (missions, abilities) require careful parsing
- **Always backup database** before bulk operations
- Test on development environment first

### Game Balance

- Server rates configured in `reference/settings/default/main.lua`
- Era-specific settings affect gameplay (level caps, job abilities, expansion content)
- Use module system for customizations without modifying core

### Security

- Database credentials in `reference/settings/default/network.lua`
- IPC bound to localhost only (no external access)
- HTTP API disabled by default - requires explicit enabling
- DDoS protection settings available in network config

### Performance

- Lua scripts are hot-reloadable (no server restart needed)
- Optimize database queries (use indexed columns)
- ZeroMQ provides high-performance IPC
- Multiple map servers can run for load distribution

## Common Use Cases

### Player Management
- Query `chars` table for character data
- Modify stats, inventory, position
- Track sessions in `accounts_sessions`

### Item Distribution
- Insert into `char_inventory` with proper item IDs
- Respect stacking limits and container slots
- Validate items exist in `item_basic` table

### Server Announcements
- Use `reference/tools/announce.py`
- Or integrate with World Server IPC

### Economy Monitoring
- Query `auction_house` for transactions
- Track price trends and market activity
- Check `char_points` for currency tracking

### World State Management
- Conquest system tables
- Campaign and besieged status
- Zone weather and time-of-day

## Additional Resources

- **LandSandBoat Repository**: https://github.com/LandSandBoat/server
- **GitHub Wiki**: 48+ pages on installation, configuration, development
- **Module Development**: Guides for Lua, C++, and SQL modules
- **Community Discord**: Active development community

## Debugging and Troubleshooting

If Claude isn't using this skill effectively:

1. **Verify skill activation**: Check that request mentions FFXI or LandSandBoat
2. **Documentation access**: Ensure `docs/` directory is readable
3. **Reference code**: Run setup script if `reference/` directory is missing
4. **Specific queries**: Provide context (e.g., "using LandSandBoat" or "FFXI private server")

## Version Information

- **LandSandBoat Version**: Latest stable (reference cloned from main branch)
- **Skill Version**: 1.0.0
- **Last Updated**: 2025-11-05
- **Documentation Coverage**: ~164 KB across 6 primary documentation files
