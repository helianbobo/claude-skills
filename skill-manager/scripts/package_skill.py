#!/usr/bin/env python3
"""
Simple Skill Packager - Creates a .skill file from a skill directory

Usage:
    python package_skill.py <skill_directory> [output_file]
    
Examples:
    python package_skill.py ../my-skill
    python package_skill.py ../my-skill ../dist/my-skill.skill
"""

import argparse
import sys
import zipfile
from pathlib import Path

def package_skill(skill_dir: Path, output_file: Path = None) -> bool:
    """
    Package a skill directory into a .skill file.
    """
    skill_dir = skill_dir.resolve()
    
    # Validate directory exists
    if not skill_dir.exists():
        print(f"❌ Error: Skill directory not found: {skill_dir}")
        return False
    
    if not skill_dir.is_dir():
        print(f"❌ Error: Path is not a directory: {skill_dir}")
        return False
    
    # Check for SKILL.md
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        print(f"❌ Error: SKILL.md not found in {skill_dir}")
        return False
    
    # Determine output filename
    if output_file is None:
        skill_name = skill_dir.name
        output_file = Path.cwd() / f"{skill_name}.skill"
    else:
        output_file = Path(output_file).resolve()
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Create the .skill file (zip format)
    try:
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk through the skill directory
            for file_path in skill_dir.rglob('*'):
                if file_path.is_file():
                    # Calculate the relative path within the zip
                    # Include skill directory name in the zip (like skill-creator does)
                    arcname = file_path.relative_to(skill_dir.parent)
                    zipf.write(file_path, arcname)
                    print(f"  Added: {arcname}")
        
        print(f"\n✅ Successfully packaged skill to: {output_file}")
        print(f"   Size: {output_file.stat().st_size / 1024:.1f} KB")
        return True
        
    except Exception as e:
        print(f"❌ Error creating .skill file: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Package a skill directory into a .skill file")
    parser.add_argument("skill_dir", help="Path to skill directory")
    parser.add_argument("output_file", nargs="?", help="Output .skill file path (optional)")
    
    args = parser.parse_args()
    
    skill_dir = Path(args.skill_dir)
    output_file = Path(args.output_file) if args.output_file else None
    
    print(f"📦 Packaging skill: {skill_dir}")
    if output_file:
        print(f"   Output file: {output_file}")
    print()
    
    success = package_skill(skill_dir, output_file)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())