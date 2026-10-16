# Arendur Atlas - Claude Instructions

This document extends the general Claude instructions with project-specific requirements.

## Project Context
The **GM atlas** for the owner's Arendur Rising campaign (the owner is the GM; the group is the Shadow Company), in the repo BahneGork/Arendur-Atlas-GM. The repo and its GitHub Pages site (bahnegork.github.io/Arendur-Atlas-GM, noindex) are **public by the owner's choice**: players simply don't get the link. Never link to it from the players' site. The same build also writes the **players' edition** into the public repo `../Arendur-Atlas` (GitHub Pages: bahnegork.github.io/Arendur-Atlas). Seeded from the Erukana atlas (`../Atlassian`); see the `campaign-atlas` skill and `docs/assessment.md`.

## Additional Requirements
- **Hidden by default**: everything in `tools/curation.py` is GM-only unless it has `players=True` (places, maps, party members). GM-only text on a player-visible place goes in `gm="..."`; `secret_at=True` hides a known place's position.
- **Players' text is player knowledge only**: for `players=True` entries, name/summary/where/aliases may only state what the players know. Claude may read all GM notes (owner's permission), but GM facts go in `gm=` or on GM-only entries.
- **Publishing**: the public repo's workflow "Publish players' edition" builds the players' edition from this repo every hour (or run it from its Actions tab). Locally: `python3 tools/build.py --players ../Arendur-Atlas`, then commit and push that repo. The build refuses to write the players' edition if any GM-only name or text would appear in it (`tools/players.py`). Never copy files to the public repo any other way.
- **No owner attribution on the site**: facts the owner (the GM) tells Claude are canon; never write "ifølge Bahne" in site text. Record the source in a code comment.
- Every placement and statement must trace to a source; chronicle points are cited as (K12).
- Notes are read only (published notes from GMnostes, only the folders in `CAMPAIGN["notes_dirs"]`); never modify the vault or GMnostes.
- Geography: the Worldographer map `../GM-vault/Hexmaps/Main diamor hex1.wxx` is the source of truth for where things are relative to each other (see GM-vault's CLAUDE.md, "Geographic Toolset Protocol"). The Misty Falls hex map (`MistyFallsRegion-Ursia.png`) lines up with it; the Ursia barony map and the players' East Blackwood map do not.
- **Keep GitHub up to date**: after every change, commit and push this repo (`git pull --rebase` first; the site's "Gem for alle" commits here).
- View the GM atlas at https://bahnegork.github.io/Arendur-Atlas-GM/ or locally: `python3 -m http.server 8000` here, then http://localhost:8000.

## Overrides
None yet.

<!-- Below this line: Copy all universal standards from root CLAUDE.md -->
```

**Why this approach**: Ensures consistency across projects while allowing customization without losing universal standards.

### New Project Creation Protocol

**When asked to create a new project:**

1. **Create project directory**: `mkdir /home/exit/dev/projects/[project-name]`
2. **Copy this file**: `cp /home/exit/dev/projects/CLAUDE.md /home/exit/dev/projects/[project-name]/CLAUDE.md`
3. **Edit the copied file** to add project-specific content following the template structure above
4. **Create basic project structure** as appropriate (src/, docs/, README.md, etc.)
5. **Initialize version control** if requested: `git init`

**Script available**: Use `/home/exit/dev/projects/create-project.sh project-name` for automated setup.

## Core Behavioral Standards

1. Think Before Coding
Don't assume. Don't hide confusion. Surface tradeoffs.

Before implementing:

State your assumptions explicitly. If uncertain, ask.
If multiple interpretations exist, present them - don't pick silently.
If a simpler approach exists, say so. Push back when warranted.
If something is unclear, stop. Name what's confusing. Ask.
2. Simplicity First
Minimum code that solves the problem. Nothing speculative.

No features beyond what was asked.
No abstractions for single-use code.
No "flexibility" or "configurability" that wasn't requested.
No error handling for impossible scenarios.
If you write 200 lines and it could be 50, rewrite it.
Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

3. Surgical Changes
Touch only what you must. Clean up only your own mess.

When editing existing code:

Don't "improve" adjacent code, comments, or formatting.
Don't refactor things that aren't broken.
Match existing style, even if you'd do it differently.
If you notice unrelated dead code, mention it - don't delete it.
When your changes create orphans:

Remove imports/variables/functions that YOUR changes made unused.
Don't remove pre-existing dead code unless asked.
The test: Every changed line should trace directly to the user's request.

4. Goal-Driven Execution
Define success criteria. Loop until verified.

Transform tasks into verifiable goals:

"Add validation" → "Write tests for invalid inputs, then make them pass"
"Fix the bug" → "Write a test that reproduces it, then make it pass"
"Refactor X" → "Ensure tests pass before and after"
For multi-step tasks, state a brief plan:

1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]

### Obsidian Vault Knowledge Protocol
- **SKILL FILE**: `~/.claude/skills/obsidian-vault/SKILL.md` is the living reference for Obsidian Bases, Dataview, wikilinks, MOC design, and frontmatter schemas
- **MANDATORY UPDATE**: When working on any Obsidian vault and you discover a syntax correction, unexpected behaviour, or new pattern — add it to the skill file immediately
- **READ FIRST**: When starting Obsidian vault work without the skill invoked, read the skill file before generating any Bases or Dataview syntax

### Source Verification Protocol
- **MANDATORY**: Every factual claim must include proper citation when referencing specific sources
- **EXACT QUOTES**: When referencing specific details, quote source text exactly
- **NO ASSUMPTIONS**: Never proceed with unverified details as established facts
- **EVIDENCE HIERARCHY**: Primary sources > Secondary sources > Inferences

### Critical Analysis Requirements
- **NO PEOPLE-PLEASING**: Challenge user requests when they contain logical flaws or inconsistencies - being helpful means being honest, not agreeable
- **DEVIL'S ADVOCATE**: Consider "what could go wrong?" with proposed scenarios
- **ASSUMPTION CHALLENGING**: Question underlying assumptions, even if they seem reasonable
- **LOGIC OVER POLITENESS**: Prioritize logical accuracy over agreeableness

## Content Creation Guidelines

### Universal Standards
- **CONSISTENCY**: All new content must fit naturally into established context
- **LOGICAL MOTIVATION**: Every element must serve clear purposes
- **INTEGRATION**: When appropriate, connect new content to existing elements

### File Organization Standards

Use clear, descriptive markdown structure for content:

```markdown
# [Title]

## Basic Information
- **Key Details**: [Relevant specifics]

## Description
[Main content description]

## Implementation
- **Requirements**: [What's needed]
- **Process**: [How to proceed]

## Integration
- **Context**: [How it fits with existing work]
- **Dependencies**: [What it relies on]

## Tags
#relevant #tags #here
```

## Development Standards

### Coding Requirements
- **Plan Before Coding**: Always brainstorm and plan approach before writing code
- **Environment Awareness**: Account for platform limitations and constraints
- **Syntax Validation**: Double-check against official documentation
- **Best Practices**: Follow established patterns and conventions

### Quality Assurance
- **Test Thoroughly**: Verify functionality before delivery
- **Document Clearly**: Include necessary explanations and comments
- **Error Handling**: Anticipate and handle potential issues
- **Performance**: Consider efficiency and resource usage

## File Management Protocol

### Content Location
**ORGANIZED STRUCTURE**: Maintain logical file organization:
- Use descriptive filenames
- Group related content appropriately
- Follow consistent naming conventions
- Include relevant metadata and tags

### File Naming Convention
- Format: `[Type]-[Name]-[Date].md` (for general content)
- Use clear, descriptive names
- Avoid special characters that cause issues
- Include version numbers when relevant

### Required Documentation
Every significant file should include:
- Clear purpose and description
- Creation/modification dates
- Relevant tags for organization
- Dependencies and requirements

## Quality Assurance Checklist

Before submitting any response:
- [ ] Can I cite specific sources for each factual claim?
- [ ] Have I distinguished facts from inferences?
- [ ] Does my logic follow clear cause-and-effect chains?
- [ ] Have I challenged assumptions rather than just agreeing?
- [ ] Is the content consistent with established context?
- [ ] Have I verified technical accuracy when applicable?
- [ ] Are all recommendations practical and implementable?
- [ ] Have I considered potential issues and edge cases?

## User Credentials & Configuration

**Credentials File**: `/home/exit/.claude/credentials.json`

This file stores frequently-needed user information to avoid repetitive questions:
- GitHub username, email, and personal access token (for commits, API calls, repository URLs)
- Personal preferences (name, timezone)
- Common paths (projects root, MCP servers)
- Development preferences (commit style, license, editor)

**Always check this file first** before asking for user credentials or preferences.

If the file doesn't exist or is incomplete, ask the user to fill it out.

## Absolute Restrictions

- **NEVER** proceed with unverified information as established fact
- **NEVER** agree just to be agreeable - use critical thinking
- **NEVER** create content that could be used maliciously
- **NEVER** make assumptions about technical requirements without verification
- **NEVER** ignore security best practices
- **NEVER** create external dependencies without explicit approval

## Success Metrics

**Successful assistance includes:**
- Accurate information properly sourced and cited
- Creative solutions that enhance rather than complicate existing work
- Logical suggestions that follow clear reasoning chains
- Proactive identification of potential issues
- Critical analysis that challenges assumptions
- Properly formatted, well-documented content

---

## MCP (Model Context Protocol) Integration

### Available MCP Servers

When working in environments with MCP support, two specialized servers are available to enhance development workflows:

#### 1. Software Planning MCP
**Location**: `/home/exit/dev/projects/software-planning-mcp/`  
**Purpose**: Project planning, task management, and development workflow coordination

**Key Functions**:
- `start_planning(goal)` - Initialize planning session for software development goals
- `add_todo(title, description, complexity, codeExample?)` - Add structured development tasks
- `get_todos()` - Retrieve current development tasks and status
- `update_todo_status(todoId, isComplete)` - Update task completion status
- `save_plan(plan)` - Save implementation plans and development roadmaps
- `remove_todo(todoId)` - Remove completed or obsolete tasks

**When to Use**:
- Starting new development features or projects
- Breaking down complex development tasks
- Tracking implementation progress across development sessions
- Creating structured development plans with complexity estimation
- Managing development roadmaps and milestone planning

**Usage Examples**:
```
"Let's start planning the implementation of user authentication"
"Add a todo for implementing password validation with complexity 4"
"Save our implementation plan for the dashboard redesign"
```

#### 2. D&D Coding MCP
**Location**: `/home/exit/dev/projects/dnd-coding-mcp/`  
**Purpose**: Code quality assurance, regression prevention, and D&D 5e rule validation

**Key Functions**:
- `validate_function_call(functionCall, context?)` - Verify function exists in project registry
- `suggest_correct_function(attemptedFunction, intendedAction?)` - Suggest correct function names
- `analyze_css_changes(cssChanges, targetFile?, scope?)` - Detect CSS conflicts before applying
- `check_regression_patterns(codeChanges, affectedFiles?, changeDescription?)` - Analyze against known bug patterns
- `verify_dnd_calculations(calculationType, implementation, expectedFormula?)` - Validate D&D 5e math
- `analyze_proposed_changes(changes, files?, context?, codeSnippets?)` - Comprehensive pre-change analysis

**When to Use**:
- Before making code changes (prevent regressions)
- When encountering "function does not exist" errors
- Before adding CSS changes (prevent conflicts)
- When implementing D&D 5e mathematical calculations
- For comprehensive code quality analysis

**Usage Examples**:
```
"Check if this function call is valid before I implement it"
"Analyze these CSS changes for potential conflicts"
"Verify this D&D ability modifier calculation is correct"
```

### MCP Integration Protocol

#### **For Software Development Projects**:
1. **Planning Phase**: Use Software Planning MCP to structure development approach
2. **Implementation Phase**: Use D&D Coding MCP for quality assurance (if applicable)
3. **Progress Tracking**: Update todos and maintain development plans
4. **Quality Gates**: Validate code changes before committing

#### **Session Workflow**:
1. **Session Start**: Check planning status and active todos
2. **Work Planning**: Break down complex tasks using planning tools
3. **Code Changes**: Validate changes using coding assistance tools
4. **Progress Update**: Mark completed tasks and update implementation plans
5. **Session End**: Save updated plans and document progress

### Project Documentation Standards

When using MCP systems, maintain these documentation files:
- `project-plan.md` - Vision, scope, success criteria, and roadmap
- `progress-log.md` - Development diary and milestone tracking
- `qa-checklist.md` - Quality assurance procedures and testing protocols
- `requirements.md` - Detailed specifications and acceptance criteria
- `design-decisions.md` - Key architectural and technical choices
- `research-notes.md` - Background research and technical insights

### MCP Server Organization & Development

#### **MANDATORY MCP Development Protocol**

**NEVER create MCP servers in random project directories.** All MCP development must follow this centralized approach:

**Central MCP Directory**: `/home/exit/dev/mcp-servers/`
**Build Standard**: All servers use `build/index.js` output
**Development Location**: Always develop in `/home/exit/dev/mcp-servers/[server-name]/`

#### **When Creating New MCP Servers**

**Before Development**:
1. **Check existing inventory**: Review `/home/exit/dev/mcp-servers/` for similar functionality
2. **Choose descriptive name**: Use pattern `[purpose]-mcp` (e.g., `pdf-handler-mcp`)
3. **Create in central location**: `mkdir /home/exit/dev/mcp-servers/[server-name]`

**Development Standards**:
```bash
# Setup new MCP server
cd /home/exit/dev/mcp-servers/
mkdir [server-name]
cd [server-name]

# Initialize with standard structure
npm init -y
npm install @modelcontextprotocol/sdk
mkdir src
touch src/index.ts
touch README.md

# Standard package.json scripts
"scripts": {
  "build": "tsc",
  "start": "node build/index.js",
  "dev": "tsx src/index.ts"
}

# Use TypeScript config for consistency
tsc --init
```

**Documentation Requirements**:
- `README.md` with purpose, functions, and usage examples
- List all available functions in package.json keywords
- Include integration instructions for Claude Code

**Current MCP Server Inventory** (as of 2025-09-20):
- `software-planning-mcp` - Project planning and task management
- `dnd-coding-mcp` - Code quality and D&D rule validation
- `monster-framework-assistant-mcp` - D&D monster design framework
- `pdf-handler-mcp` - PDF processing and content extraction
- `cosmic-game-mcp` - Cosmic Game campaign management
- `youtube-channel-builder-mcp` - YouTube automation and content creation
- `gm-vault-search-mcp` - GM content search and retrieval
- `creative-lifecycle-mcp` - Creative workflow synchronization

#### **MCP Server Configuration**

**IMPORTANT: MCP servers are configured at USER SCOPE for universal availability.**

All MCP servers are configured in `~/.claude.json` with `--scope user`, making them available in **every Claude Code session regardless of working directory**.

**Current Global Configuration**:
- ✓ software-planning-tool
- ✓ dnd-coding-assistant
- ✓ pdf-handler
- ✓ gm-vault-search
- ✓ monster-framework-assistant
- ✓ creative-lifecycle

**Standard Installation Paths**:
- All servers: `/home/exit/dev/mcp-servers/[server-name]/build/index.js`

**To add new MCP servers globally**:
```bash
# Add at user scope (available everywhere)
claude mcp add [server-name] --scope user node /home/exit/dev/mcp-servers/[server-name]/build/index.js

# Verify configuration
claude mcp list
```

**Quick Setup Reference**: See `/home/exit/dev/projects/MCP-SETUP-INSTRUCTIONS.md` for project-specific MCP setup

**Universal MCP Guide**: See `/home/exit/dev/projects/GENERAL-MCP-INTEGRATION-GUIDE.md` for integrating any MCP server

**Claude Desktop Configuration Example**:
```json
{
  "mcpServers": {
    "software-planning-tool": {
      "command": "node",
      "args": ["/home/exit/dev/projects/software-planning-mcp/build/index.js"],
      "disabled": false
    },
    "dnd-coding-assistant": {
      "command": "node", 
      "args": ["/home/exit/dev/projects/dnd-coding-mcp/build/index.js"],
      "disabled": false
    }
  }
}
```

*This document establishes the framework for all Claude interactions. All work should maintain these standards while adapting to specific task requirements.*