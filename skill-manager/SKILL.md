---
name: skill-manager
description: Comprehensive skill management system for opencode. Installs, validates, lists, and manages skills in the opencode skills directory. Use when users need to: (1) Install a skill from directory or .skill file, (2) Validate skill structure before installation, (3) List installed skills with details, (4) Update existing skills, or (5) Manage opencode skill ecosystem.
---

# Skill Manager

Comprehensive tool for managing opencode skills. Provides installation, validation, listing, and management capabilities for skills in the opencode ecosystem.

## Quick Start

### Installation Methods

**From a skill directory:**
```bash
python scripts/install_skill.py /path/to/skill-directory
```

**From a .skill file:**
```bash
python scripts/install_skill.py /path/to/skill-file.skill
```

**Update existing skill:**
```bash
python scripts/install_skill.py /path/to/skill --update
```

### Validation
```bash
python scripts/validate_skill.py /path/to/skill
```

### Listing Skills
```bash
python scripts/list_skills.py
python scripts/list_skills.py --details
```

## Core Capabilities

### 1. Skill Installation

Install skills from directories or packaged .skill files to `~/.config/opencode/skill/`.

**Install from directory:**
```bash
# Basic installation
python scripts/install_skill.py ../my-new-skill

# Update existing skill
python scripts/install_skill.py ../my-new-skill --update

# Force overwrite
python scripts/install_skill.py ../my-new-skill --force
```

**Install from .skill file:**
```bash
python scripts/install_skill.py downloads/english-tutor.skill
```

**Features:**
- Validates skill structure before installation
- Checks for existing skills (prevents accidental overwrites)
- Supports update mode for existing skills
- Creates skills directory if it doesn't exist

### 2. Skill Validation

Validate skill structure to ensure compatibility with opencode.

**Validate directory:**
```bash
python scripts/validate_skill.py /path/to/skill-directory
```

**Validate .skill file:**
```bash
python scripts/validate_skill.py /path/to/skill-file.skill
```

**Checks performed:**
- SKILL.md existence and format
- YAML frontmatter with required fields
- Skill naming conventions (hyphen-case)
- Basic structure validity

### 3. Skill Listing

List all installed skills with various detail levels.

**Basic listing:**
```bash
python scripts/list_skills.py
```

**Detailed view:**
```bash
python scripts/list_skills.py --details
```

**With paths:**
```bash
python scripts/list_skills.py --path
```

**JSON output:**
```bash
python scripts/list_skills.py --json
```

**Features:**
- Shows skill name, description, size, and modification time
- Identifies skills missing SKILL.md
- Supports machine-readable JSON output
- Handles both directories and .skill files

## Skill Structure Requirements

For detailed skill structure requirements, see [Skill Structure Reference](references/skill-structure.md).

**Minimum requirements:**
- `SKILL.md` with YAML frontmatter
- `name` and `description` fields in frontmatter
- Hyphen-case naming (e.g., `my-skill`)

## Workflow Examples

### New Skill Installation

1. **Validate the skill first:**
   ```bash
   python scripts/validate_skill.py ~/projects/my-new-skill
   ```

2. **Install the skill:**
   ```bash
   python scripts/install_skill.py ~/projects/my-new-skill
   ```

3. **Verify installation:**
   ```bash
   python scripts/list_skills.py --details
   ```

### Updating Existing Skill

1. **Update with new version:**
   ```bash
   python scripts/install_skill.py ~/projects/my-skill-updated --update
   ```

2. **Check the update:**
   ```bash
   python scripts/list_skills.py
   ```

### Troubleshooting Installation

**Skill already exists:**
```bash
# Error: Skill 'my-skill' already exists
python scripts/install_skill.py ../my-skill --update  # Use update flag
```

**Invalid skill structure:**
```bash
# First validate to see errors
python scripts/validate_skill.py ../my-skill

# Fix issues based on validation output
# Then install
python scripts/install_skill.py ../my-skill
```

**Missing skills directory:**
```bash
# The installer creates the directory automatically
python scripts/install_skill.py ../my-skill
# Creates ~/.config/opencode/skill/ if needed
```

## Script Reference

### install_skill.py

**Purpose:** Install skills to opencode skills directory.

**Usage:**
```bash
python scripts/install_skill.py <skill_path> [--update] [--force]
```

**Arguments:**
- `skill_path`: Path to skill directory or .skill file
- `--update`: Update existing skill (overwrites)
- `--force`: Force installation without prompts

**Exit codes:**
- `0`: Success
- `1`: Error (validation failed, installation failed, etc.)

### validate_skill.py

**Purpose:** Validate skill structure.

**Usage:**
```bash
python scripts/validate_skill.py <skill_path>
```

**Arguments:**
- `skill_path`: Path to skill directory or .skill file

**Exit codes:**
- `0`: Valid
- `1`: Invalid or error

### list_skills.py

**Purpose:** List installed skills.

**Usage:**
```bash
python scripts/list_skills.py [--details] [--path] [--json]
```

**Arguments:**
- `--details`, `-d`: Show detailed information
- `--path`, `-p`: Show full paths
- `--json`, `-j`: Output as JSON

**Exit codes:**
- `0`: Success
- `1`: Error reading skills directory

## Resources

- **Skill Structure Reference**: [references/skill-structure.md](references/skill-structure.md) - Detailed requirements and validation rules

## Notes

- Skills are installed to `~/.config/opencode/skill/<skill-name>/`
- .skill files are zip archives containing skill directories
- Validation follows opencode skill specification
- Update mode removes existing skill before installing new version