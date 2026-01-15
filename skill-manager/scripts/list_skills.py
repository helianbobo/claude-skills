#!/usr/bin/env python3
"""
List Installed Skills - Lists all skills installed in opencode skills directory

Usage:
    python list_skills.py [--details] [--path]
    
Examples:
    python list_skills.py
    python list_skills.py --details
    python list_skills.py --path
"""

import argparse
import sys
from pathlib import Path
import json
from datetime import datetime

# Default opencode skills directory
SKILLS_DIR = Path.home() / ".config" / "opencode" / "skill"

def get_skill_info(skill_dir: Path) -> dict:
    """
    Get information about a skill from its directory.
    """
    skill_md = skill_dir / "SKILL.md"
    
    info = {
        "name": skill_dir.name,
        "path": str(skill_dir),
        "has_skill_md": skill_md.exists(),
        "size_mb": 0,
        "modified": datetime.fromtimestamp(skill_dir.stat().st_mtime).isoformat()
    }
    
    # Calculate directory size
    try:
        total_size = 0
        for file in skill_dir.rglob('*'):
            if file.is_file():
                total_size += file.stat().st_size
        info["size_mb"] = round(total_size / (1024 * 1024), 2)
    except:
        pass
    
    # Try to read skill name and description from SKILL.md
    if skill_md.exists():
        try:
            content = skill_md.read_text()
            lines = content.split("\n")
            
            if lines[0] == "---":
                try:
                    end_idx = lines.index("---", 1)
                    frontmatter_lines = lines[1:end_idx]
                    
                    for line in frontmatter_lines:
                        line = line.strip()
                        if line.startswith("name:"):
                            name = line[5:].strip().strip("'\"")
                            if name:
                                info["name_from_md"] = name
                        elif line.startswith("description:"):
                            desc = line[12:].strip().strip("'\"")
                            if desc:
                                # Truncate long descriptions
                                if len(desc) > 100:
                                    desc = desc[:97] + "..."
                                info["description"] = desc
                except ValueError:
                    pass
        except:
            pass
    
    return info

def list_skills(details: bool = False, show_path: bool = False) -> bool:
    """
    List all installed skills.
    Returns True if successful.
    """
    if not SKILLS_DIR.exists():
        print(f"❌ Skills directory does not exist: {SKILLS_DIR}")
        return False
    
    # Get all subdirectories in skills directory
    skill_dirs = []
    try:
        for item in SKILLS_DIR.iterdir():
            if item.is_dir():
                skill_dirs.append(item)
            elif item.is_file() and item.suffix == ".skill":
                # Also list .skill files (packaged skills)
                skill_dirs.append(item)
    except Exception as e:
        print(f"❌ Error reading skills directory: {e}")
        return False
    
    if not skill_dirs:
        print("📭 No skills installed")
        print(f"   Skills directory: {SKILLS_DIR}")
        return True
    
    print(f"📚 Installed Skills ({len(skill_dirs)})")
    print(f"   Location: {SKILLS_DIR}")
    print()
    
    # Sort by name
    skill_dirs.sort(key=lambda x: x.name.lower())
    
    for i, skill_path in enumerate(skill_dirs, 1):
        if skill_path.is_dir():
            info = get_skill_info(skill_path)
            
            # Display skill
            print(f"{i:2d}. {info['name']}")
            
            if details:
                if 'description' in info:
                    print(f"     Description: {info['description']}")
                
                print(f"     Size: {info['size_mb']} MB")
                print(f"     Modified: {info['modified']}")
                
                if not info['has_skill_md']:
                    print("     ⚠️  Missing SKILL.md")
            
            if show_path:
                print(f"     Path: {info['path']}")
            
            if not details and not show_path:
                # Brief mode - just show name
                if 'description' in info:
                    # Show first line of description
                    desc = info['description']
                    first_line = desc.split('\n')[0] if '\n' in desc else desc
                    if len(first_line) > 60:
                        first_line = first_line[:57] + "..."
                    print(f"     {first_line}")
            
        elif skill_path.is_file() and skill_path.suffix == ".skill":
            # .skill file (packaged)
            print(f"{i:2d}. {skill_path.name} (.skill file)")
            if show_path:
                print(f"     Path: {skill_path}")
            if details:
                size_mb = skill_path.stat().st_size / (1024 * 1024)
                modified = datetime.fromtimestamp(skill_path.stat().st_mtime).isoformat()
                print(f"     Size: {size_mb:.2f} MB")
                print(f"     Modified: {modified}")
        
        print()
    
    return True

def main():
    parser = argparse.ArgumentParser(description="List installed skills in opencode skills directory")
    parser.add_argument("--details", "-d", action="store_true", help="Show detailed information")
    parser.add_argument("--path", "-p", action="store_true", help="Show full paths")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    if not SKILLS_DIR.exists():
        print(f"❌ Skills directory does not exist: {SKILLS_DIR}")
        return 1
    
    if args.json:
        # JSON output mode
        skill_dirs = []
        try:
            for item in SKILLS_DIR.iterdir():
                if item.is_dir():
                    info = get_skill_info(item)
                    skill_dirs.append(info)
        except Exception as e:
            print(json.dumps({"error": str(e)}, indent=2))
            return 1
        
        print(json.dumps({"skills": skill_dirs, "count": len(skill_dirs)}, indent=2))
        return 0
    else:
        # Normal output mode
        success = list_skills(args.details, args.path)
        return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())