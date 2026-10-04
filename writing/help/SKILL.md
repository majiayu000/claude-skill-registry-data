---
name: help
description: Shows available skills, common workflows, and quick reference for the plugin. Use when the user asks for help, what skills are available, or how to do something.
---

## bitwize-music Plugin Help

Display this help information to the user in a clear, organized format.

---

### Getting Started

**New to the plugin?**
- the `tutorial` skill - Interactive guided album creation
- the `configure` skill - Set up configuration file
- the `about` skill - About bitwize and this plugin

**Resume existing work:**
- the `resume` skill <album-name>` - Find an album and see status/next steps

---

### Skills by Category

**Album & Track Creation**
- the `album-ideas` skill - Track and manage album ideas
- the `promote-idea` skill - Convert a Pending idea into a full album (one-shot)
- the `new-album` skill - Create new album with directory structure
- the `album-conceptualizer` skill - Album concepts and tracklist architecture
- the `lyric-writer` skill - Write/review lyrics, fix prosody
- the `suno-engineer` skill - Technical Suno prompting and genre selection

**Research & Sources**
- the `researcher` skill - Main research coordinator, fact-checking
- the `document-hunter` skill - Automated document search/download
- the `researchers-legal` skill - Court documents, indictments
- the `researchers-gov` skill - DOJ/FBI/SEC releases
- the `researchers-tech` skill - Project histories, changelogs
- the `researchers-journalism` skill - Investigative articles
- the `researchers-security` skill - Malware analysis, CVEs
- the `researchers-financial` skill - SEC filings, market data
- the `researchers-historical` skill - Archives, timelines
- the `researchers-biographical` skill - Personal backgrounds
- the `researchers-primary-source` skill - Tweets, blogs, forums
- the `researchers-verifier` skill - Quality control, citation validation

**Quality Control**
- the `lyric-reviewer` skill - Pre-generation QC gate (14-point checklist)
- the `pronunciation-specialist` skill - Scan for pronunciation risks
- the `explicit-checker` skill - Verify explicit content flags
- the `plagiarism-checker` skill - Check lyrics for phrases matching existing songs
- the `voice-checker` skill - Detect AI-written patterns in lyrics and prose
- the `pre-generation-check` skill - Final pre-generation checkpoint (6 gates)
- the `validate-album` skill - Validate album structure and paths

**Production & Release**
- the `album-art-director` skill - Visual concepts and AI art prompts
- the `mastering-engineer` skill - Audio mastering guidance
- the `promo-director` skill - Generate promo videos for social media
- the `cloud-uploader` skill - Upload promo videos to Cloudflare R2 or AWS S3
- the `sheet-music-publisher` skill - Convert audio to sheet music
- the `release-director` skill - Release coordination and distribution

**File Management**
- the `import-track` skill - Move track .md files to album location
- the `import-audio` skill - Move audio files to album location
- the `import-art` skill - Place album art in correct locations
- the `clipboard` skill - Copy track lyrics/prompts to clipboard

**Workflow & Status**
- the `session-start` skill - Run session startup procedure
- the `next-step` skill - Get recommended next action
- the `album-dashboard` skill - Visual album progress dashboard

**System & Maintenance**
- the `configure` skill - Edit plugin configuration
- the `test` skill - Run automated tests
- the `help` skill - Show this help (you are here!)
- the `about` skill - About bitwize and the plugin

---

### Common Workflows

**Creating a New Album:**
1. the `new-album` skill <name> <genre>` - Create structure (or the `promote-idea` skill "<idea title>"` if the idea lives in `IDEAS.md`)
2. Answer the 7 planning phases (concept, sonic direction, etc.)
3. Write lyrics for each track
4. Run the `lyric-reviewer` skill before generation
5. Generate in Suno, log results
6. Master audio with the `mastering-engineer` skill
7. [Optional] Generate promo videos with the `promo-director` skill
8. [Optional] Upload to cloud with the `cloud-uploader` skill
9. Release with the `release-director` skill

**True-Story Albums (with research):**
1. Use researcher skills to gather sources
2. All sources must be verified by human before production
3. Update track status from `❌ Pending` to `✅ Verified (DATE)`
4. Then proceed with lyric writing and generation

**Resume Existing Work:**
1. the `resume` skill <album-name>` - Get detailed status
2. Follow the recommended next steps

---

### Quick Tips

- **Config file:** `~/.bitwize-music/config.yaml` (always read this for paths)
- **Pronunciation:** Use phonetic spelling for tricky words (see pronunciation guide)
- **Explicit content:** Use flag for: fuck, shit, bitch, cunt, cock, dick, pussy, etc.
- **Mastering target:** -14 LUFS, -1.0 dBTP for streaming platforms
- **Promo videos:** Generate after mastering, 15s vertical (9:16) for social media
- **Track status flow:** Not Started → In Progress → Generated → Final
- **Album status flow:** Concept → In Progress → Complete → Released

---

### Key Documentation

- **CLAUDE.md** - Main workflow instructions
- **README.md** - Project overview
- `../../reference/suno/` - Suno V5 guides, pronunciation, tips
- `../../reference/workflows/` - Detailed workflow procedures
- `../../reference/mastering/` - Audio mastering documentation
- `../../templates/` - Templates for new content
- `../../skills/[skill-name]/SKILL.md` - Individual skill documentation

---

### Getting Help

- Use this skill anytime: the `help` skill
- For tutorial: the `tutorial` skill
- For status: the `resume` skill <album-name>`
- Ask Claude: "What should I do next?" for guidance
