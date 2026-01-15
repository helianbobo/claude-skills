#!/usr/bin/env python3
"""
Skill Installer - Installs skills to opencode skills directory

Usage:
    python install_skill.py <skill_path> [--update] [--force]
    
Examples:
    python install_skill.py /path/to/my-skill
    python install_skill.py /path/to/my-skill.skill --update
    python install_skill.py /path/to/my-skill --force
"""

import argparse
import os
import shutil
import sys
import zipfile
from pathlib import Path
import tempfile

# Default opencode skills directory
SKILLS_DIR = Path.home() / ".config" / "opencode" / "skill"

def validate_skill_structure(skill_path: Path) -> tuple[bool, str]:
    """
    Validate basic skill structure.
    Returns (is_valid, message)
    """
    # Check if it's a directory
    if not skill_path.exists():
        return False, f"Path does not exist: {skill_path}"
    
    # Check for SKILL.md
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, f"SKILL.md not found in {skill_path}"
    
    # Read SKILL.md to check frontmatter
    try:
        content = skill_md.read_text()
        if not content.startswith("---"):
            return False, "SKILL.md does not have YAML frontmatter"
        
        # Basic frontmatter check
        lines = content.split("\n")
        if lines[0] != "---":
            return False, "Invalid frontmatter format"
        
        # Look for second "---" to end frontmatter
        try:
            end_idx = lines.index("---", 1)
            frontmatter_lines = lines[1:end_idx]
            frontmatter = "\n".join(frontmatter_lines)
            
            # Check for name and description fields
            if "name:" not in frontmatter:
                return False, "Missing 'name:' in frontmatter"
            if "description:" not in frontmatter:
                return False, "Missing 'description:' in frontmatter"
                
        except ValueError:
            return False, "Frontmatter not properly closed with '---'"
            
    except Exception as e:
        return False, f"Error reading SKILL.md: {e}"
    
    return True, "Skill structure is valid"

def extract_skill_name(skill_path: Path) -> str:
    """
    Extract skill name from SKILL.md frontmatter or directory name.
    """
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        try:
            content = skill_md.read_text()
            lines = content.split("\n")
            if lines[0] == "---":
                end_idx = lines.index("---", 1) if "---" in lines[1:] else len(lines)
                for i in range(1, end_idx):
                    line = lines[i].strip()
                    if line.startswith("name:"):
                        name = line[5:].strip()
                        # Remove quotes if present
                        name = name.strip("'\"")
                        return name
        except:
            pass
    
    # Fallback to directory name
    return skill_path.name

def install_from_directory(source_dir: Path, update: bool = False, force: bool = False) -> bool:
    """
    Install a skill from a directory.
    """
    source_dir = source_dir.resolve()
    
    # Validate source
    if not source_dir.exists() or not source_dir.is_dir():
        print(f"❌ Error: Source directory not found: {source_dir}")
        return False
    
    # Validate skill structure
    valid, message = validate_skill_structure(source_dir)
    if not valid:
        print(f"❌ Validation failed: {message}")
        return False
    
    # Get skill name
    skill_name = extract_skill_name(source_dir)
    if not skill_name:
        print("❌ Error: Could not determine skill name")
        return False
    
    # Target directory
    target_dir = SKILLS_DIR / skill_name
    
    # Check if already exists
    if target_dir.exists():
        if not update and not force:
            print(f"❌ Skill '{skill_name}' already exists at {target_dir}")
            print("   Use --update to update existing skill or --force to overwrite")
            return False
        else:
            # Backup or remove existing
            print(f"⚠️  Skill '{skill_name}' already exists, updating...")
            try:
                shutil.rmtree(target_dir)
            except Exception as e:
                print(f"❌ Error removing existing skill: {e}")
                return False
    
    # Create target directory
    try:
        target_dir.parent.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"❌ Error creating target directory: {e}")
        return False
    
    # Copy the skill directory
    try:
        shutil.copytree(source_dir, target_dir)
        print(f"✅ Successfully installed skill '{skill_name}' to {target_dir}")
        return True
    except Exception as e:
        print(f"❌ Error copying skill: {e}")
        # Clean up partial copy
        if target_dir.exists():
            shutil.rmtree(target_dir, ignore_errors=True)
        return False

def install_from_skill_file(skill_file: Path, update: bool = False, force: bool = False) -> bool:
    """
    Install a skill from a .skill file (zip).
    """
    skill_file = skill_file.resolve()
    
    # Validate file
    if not skill_file.exists():
        print(f"❌ Error: Skill file not found: {skill_file}")
        return False
    
    if skill_file.suffix != ".skill":
        print(f"❌ Error: File must have .skill extension: {skill_file}")
        return False
    
    # Create temporary directory for extraction
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Extract the .skill file
        try:
            with zipfile.ZipFile(skill_file, 'r') as zipf:
                zipf.extractall(temp_path)
        except zipfile.BadZipFile:
            print(f"❌ Error: Invalid .skill file (not a valid zip): {skill_file}")
            return False
        except Exception as e:
            print(f"❌ Error extracting .skill file: {e}")
            return False
        
        # Find the skill directory in the extracted contents
        # The .skill file should contain a directory with the skill name
        items = list(temp_path.iterdir())
        if not items:
            print(f"❌ Error: Empty .skill file: {skill_file}")
            return False
        
        # Assume the first directory is the skill directory
        extracted_dir = None
        for item in items:
            if item.is_dir():
                extracted_dir = item
                break
        
        if not extracted_dir:
            print(f"❌ Error: No directory found in .skill file: {skill_file}")
            return False
        
        # Install from the extracted directory
        return install_from_directory(extracted_dir, update, force)

def main():
    parser = argparse.ArgumentParser(description="Install a skill to opencode skills directory")
    parser.add_argument("skill_path", help="Path to skill directory or .skill file")
    parser.add_argument("--update", action="store_true", help="Update existing skill")
    parser.add_argument("--force", action="store_true", help="Force overwrite without confirmation")
    
    args = parser.parse_args()
    
    skill_path = Path(args.skill_path)
    
    # Check if skills directory exists
    if not SKILLS_DIR.exists():
        print(f"⚠️  Skills directory does not exist: {SKILLS_DIR}")
        print("   Creating directory...")
        try:
            SKILLS_DIR.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created skills directory: {SKILLS_DIR}")
        except Exception as e:
            print(f"❌ Error creating skills directory: {e}")
            return 1
    
    # Determine if it's a directory or .skill file
    if skill_path.is_dir():
        success = install_from_directory(skill_path, args.update, args.force)
    elif skill_path.is_file() and skill_path.suffix == ".skill":
        success = install_from_skill_file(skill_path, args.update, args.force)
    else:
        print(f"❌ Error: Path must be a directory or .skill file: {skill_path}")
        print("   Directory must contain SKILL.md")
        print("   .skill file must have .skill extension")
        return 1
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())