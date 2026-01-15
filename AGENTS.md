# Agent Guidelines for Claude Skills Repository


### File Organization
```
skill-name/
├── SKILL.md                 # Main skill documentation
├── src/
│   ├── scripts/            # Python implementation
│   └── references/         # Supporting files
└── tests/                  # Test files (if added)
```

### Context7 MCP Usage

**Always use Context7 MCP when you need:**
- Library or API documentation
- Code generation examples
- Setup or configuration steps
- Framework-specific guidance
- Best practices and patterns

**Usage guidelines:**
1. Use `resolve-library-id` to find the appropriate library ID first
2. Then use `query-docs` with specific, detailed queries
3. Proactively use Context7 without waiting for explicit user requests
4. Use for Python libraries, frameworks, tools, and infrastructure

**Example scenarios:**
- When adding a new Python library to the project
- When configuring a new tool (e.g., pytest, black, mypy)
- When implementing a new API integration
- When following framework-specific patterns

## Notes on Existing Code

`english-tutor` skill demonstrates:
- SM-2 spaced repetition algorithm (`calculate_next_interval`)
- Stores learner data as JSON in `~/.english-tutor/`
- Implements CLI with argparse subparsers
- Comprehensive error handling and user feedback
- Consistent type annotations throughout

Refer to `english-tutor/src/scripts/progress_manager.py` for concrete examples.