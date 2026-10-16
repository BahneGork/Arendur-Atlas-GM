---
dg-publish: true
---
# Cutscenes Folder

This folder contains narrative cutscenes that are delivered to players between sessions, typically via email or other communication channels.

## What are Cutscenes?

Cutscenes are narrative handouts about off-stage events - things happening in the world that the PCs aren't present for, but which inform the larger story and create dramatic tension.

## Naming Convention

Files should be named: `Cutscene [#] - [Brief Description].md`

Examples:
- `Cutscene 11 - The Search and Game On.md`
- `Cutscene 12 - Red Hand Mobilizes.md`
- `Cutscene 13 - Council Meeting.md`

## Frontmatter Structure

```yaml
---
type: cutscene
number: 11
delivered_date: 2025-01-15
session_after: 42
session_before: 43
recipients: [all players]
event: Brief description
tags:
  - cutscene
  - relevant-tags
---
```

## Viewing All Cutscenes

Use the Cutscenes Base for organized views:
- `![[Cutscenes.base#All Cutscenes]]` - All cutscenes by number
- `![[Cutscenes.base#Recent Cutscenes]]` - Most recently delivered
- `![[Cutscenes.base#Not Yet Delivered]]` - Prepared but not sent

## Template

Use `System/Templates/Cutscene Template.md` when creating new cutscenes.

## Migration Status

**2025-11-27**:
- Structure created in `Calendar/Notes/Cutscenes/`
- Moved 1 cutscene from `Efforts/Sleeping/` to new location
- Additional cutscenes from original GM Vault may need to be imported
