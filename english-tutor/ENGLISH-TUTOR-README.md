# English Tutor Skill - Export Package

## Contents

This package contains the English Tutor skill files WITHOUT any learner data.

### Included Files:

```
english-tutor/
├── SKILL.md                          # Main skill configuration and documentation
├── scripts/
│   └── progress_manager.py           # Progress management script with export/import
└── references/
    ├── assessment-guide.md           # Vocabulary assessment methodology
    ├── vocabulary-lists.md           # Word lists by level
    └── spaced-repetition.md          # Spaced repetition algorithm details
```

**File:** `english-tutor-skill-export.tar.gz` (20 KB)

## What's NOT Included

- Learner data files (stored separately in `~/.english-tutor/`)
- Individual user profiles and progress
- Vocabulary tracking data

## Installation Instructions

### Option 1: Extract to Claude Skills Directory

```bash
# Extract to Claude skills directory
cd ~/.claude/skills/
tar -xzf /path/to/english-tutor-skill-export.tar.gz

# Or create the directory first if needed
mkdir -p ~/.claude/skills
cd ~/.claude/skills
tar -xzf /path/to/english-tutor-skill-export.tar.gz
```

### Option 2: Extract to Project Directory

```bash
# Extract to your projects folder
cd ~/projects/skills/
tar -xzf /path/to/english-tutor-skill-export.tar.gz
```

## Features

### Latest Updates (January 2026)

1. **Multi-age support**: Children (8-12) and adults
2. **Language customization**: 80% English / 20% mother tongue for kids, English-only for adults
3. **Diverse themes**: Personalized story generation based on learner interests
4. **Sequential questioning**: One question at a time for better learning
5. **Export/Import**: Transfer profiles between computers
6. **Reduced open questions for kids**: Mostly multiple-choice for easier learning

### Key Capabilities

- Vocabulary assessment and level placement
- Spaced repetition system (SM-2 algorithm)
- Daily word selection with review scheduling
- Personalized story generation
- Progress tracking and statistics
- Multi-environment support (study on multiple computers)

## Quick Start

1. Extract the archive to your desired location
2. Initialize a new learner:
   ```bash
   # For children
   python3 scripts/progress_manager.py init <name> --age <age> --level <level>

   # For adults
   python3 scripts/progress_manager.py init <name> --level <level>
   ```

3. Start learning with: "Let's do [Name]'s daily English Tasks!"

## Transferring Learner Data

Learner data is stored separately in `~/.english-tutor/` and can be exported/imported:

```bash
# Export learner profile
python3 scripts/progress_manager.py export <name> --output backup.json

# Import on another computer
python3 scripts/progress_manager.py import backup.json
```

## Requirements

- Python 3.6 or higher
- Claude Code CLI with skills support

## Documentation

Full documentation is available in `SKILL.md` including:
- Teaching styles for different age groups
- Content generation guidelines
- Session workflows
- Quality scoring guide
- Complete command reference

## Version

Export Date: January 14, 2026
Skill Version: 2.0 (Multi-age with export/import support)

## License

This skill is provided as-is for educational purposes.
