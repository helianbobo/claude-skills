# Skill Structure Reference

## Required Files

Every skill must have:

### SKILL.md (required)
- **Location**: Root of skill directory
- **Format**: YAML frontmatter + Markdown content
- **Required frontmatter fields**:
  - `name`: Skill identifier in hyphen-case (e.g., "my-skill")
  - `description`: Comprehensive description including when to use the skill

### Example SKILL.md:
```markdown
---
name: my-skill
description: Comprehensive tool for doing X. Use when Claude needs to work with Y files for: (1) Creating new Y, (2) Modifying existing Y, (3) Processing Y data, etc.
---

# My Skill

## Overview

[Skill instructions go here...]
```

## Directory Structure

```
skill-name/
├── SKILL.md                 # Required: Main skill documentation
├── scripts/                 # Optional: Executable code
│   ├── script1.py          # Python scripts
│   └── script2.sh          # Shell scripts
├── references/             # Optional: Reference documentation
│   ├── api-reference.md    # API docs
│   └── schemas.md          # Data schemas
└── assets/                 # Optional: Output resources
    ├── templates/          # Template files
    └── images/             # Image assets
```

## Naming Conventions

- **Skill name**: hyphen-case, lowercase letters/digits/hyphens only
  - ✅ `my-skill`, `data-analyzer`, `pdf-processor-v2`
  - ❌ `MySkill`, `data_analyzer`, `-bad-name-`
- **Directory name**: Must match skill name in SKILL.md frontmatter
- **File names**: Use lowercase with hyphens or underscores

## Validation Rules

A valid skill must pass these checks:

1. **SKILL.md exists** in root directory
2. **YAML frontmatter** present with `---` delimiters
3. **Required fields**: `name` and `description`
4. **Name format**: hyphen-case, no leading/trailing hyphens
5. **Description**: Non-empty, no angle brackets

## .skill Files

.skill files are zip archives containing a skill directory. When packaged:

```
my-skill.skill (zip file)
└── my-skill/              # Root directory named after skill
    ├── SKILL.md
    ├── scripts/
    └── ...
```

## Installation Locations

Skills are installed to:
- `~/.config/opencode/skill/` (default)
- Each skill gets its own subdirectory: `~/.config/opencode/skill/<skill-name>/`

## Common Issues

### Missing SKILL.md
```
❌ SKILL.md not found in /path/to/skill
```

### Invalid Frontmatter
```
❌ SKILL.md does not start with YAML frontmatter (---)
```

### Missing Required Fields
```
❌ Missing 'name:' field in frontmatter
❌ Missing 'description:' field in frontmatter
```

### Invalid Name Format
```
❌ Name 'MySkill' should be hyphen-case (lowercase letters, digits, and hyphens only)
❌ Name '-bad-' cannot start or end with hyphen
```

## Best Practices

1. **Keep SKILL.md concise** - Focus on essential instructions
2. **Use references for details** - Move detailed documentation to references/ directory
3. **Test scripts** - Ensure scripts run without errors
4. **Include examples** - Show concrete usage examples in SKILL.md
5. **Follow existing patterns** - Look at other skills for structure inspiration