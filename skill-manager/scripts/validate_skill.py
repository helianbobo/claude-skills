#!/usr/bin/env python3
"""
Skill Validator - Validates skill structure

Usage:
    python validate_skill.py <skill_path>
    
Examples:
    python validate_skill.py /path/to/my-skill
    python validate_skill.py /path/to/my-skill.skill
"""

import argparse
import os
import sys
import zipfile
import tempfile
from pathlib import Path

def validate_skill_directory(skill_path: Path) -> tuple[bool, str]:
    """
    Validate a skill directory structure.
    Returns (is_valid, message)
    """
    # Check if it's a directory
    if not skill_path.exists():
        return False, f"Path does not exist: {skill_path}"
    
    if not skill_path.is_dir():
        return False, f"Path is not a directory: {skill_path}"
    
    # Check for SKILL.md
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, f"SKILL.md not found in {skill_path}"
    
    # Read SKILL.md to check frontmatter
    try:
        content = skill_md.read_text()
        
        # Check for YAML frontmatter
        if not content.startswith("---"):
            return False, "SKILL.md does not start with YAML frontmatter (---)"
        
        lines = content.split("\n")
        
        # Find end of frontmatter
        try:
            end_idx = lines.index("---", 1)
        except ValueError:
            return False, "YAML frontmatter not properly closed with '---'"
        
        frontmatter_lines = lines[1:end_idx]
        
        # Check for required fields
        has_name = False
        has_description = False
        
        for line in frontmatter_lines:
            line = line.strip()
            if line.startswith("name:"):
                has_name = True
                # Check name format
                name_value = line[5:].strip()
                if not name_value:
                    return False, "Name field is empty"
            elif line.startswith("description:"):
                has_description = True
                # Check description
                desc_value = line[12:].strip()
                if not desc_value:
                    return False, "Description field is empty"
        
        if not has_name:
            return False, "Missing 'name:' field in frontmatter"
        
        if not has_description:
            return False, "Missing 'description:' field in frontmatter"
        
        # Check naming convention (hyphen-case)
        # Extract name from frontmatter for better validation
        for line in frontmatter_lines:
            line = line.strip()
            if line.startswith("name:"):
                name_value = line[5:].strip().strip("'\"")
                # Check hyphen-case: lowercase letters, digits, hyphens
                import re
                if not re.match(r'^[a-z0-9-]+$', name_value):
                    return False, f"Name '{name_value}' should be hyphen-case (lowercase letters, digits, and hyphens only)"
                if name_value.startswith('-') or name_value.endswith('-'):
                    return False, f"Name '{name_value}' cannot start or end with hyphen"
                if '--' in name_value:
                    return False, f"Name '{name_value}' cannot contain consecutive hyphens"
                break
        
    except Exception as e:
        return False, f"Error reading SKILL.md: {e}"
    
    return True, f"Skill '{skill_path.name}' is valid!"

def validate_skill_file(skill_file: Path) -> tuple[bool, str]:
    """
    Validate a .skill file.
    Returns (is_valid, message)
    """
    if not skill_file.exists():
        return False, f"File does not exist: {skill_file}"
    
    if skill_file.suffix != ".skill":
        return False, f"File must have .skill extension: {skill_file}"
    
    # Check if it's a valid zip file
    try:
        with zipfile.ZipFile(skill_file, 'r') as zipf:
            # Check for SKILL.md in the zip
            skill_files = [f for f in zipf.namelist() if f.endswith('SKILL.md')]
            if not skill_files:
                return False, "No SKILL.md found in .skill file"
            
            # Extract to temp directory for validation
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                zipf.extractall(temp_path)
                
        # Find the skill directory
        items = list(temp_path.iterdir())
        skill_dir = None
        
        # Look for a directory first
        for item in items:
            if item.is_dir():
                skill_dir = item
                break
        
        # If no directory found, check if files are at root (including SKILL.md)
        if not skill_dir:
            # Check if SKILL.md exists at root
            if (temp_path / "SKILL.md").exists():
                skill_dir = temp_path
            else:
                return False, "No skill directory or SKILL.md found in .skill file"
                
                # Validate the extracted directory
                return validate_skill_directory(skill_dir)
                
    except zipfile.BadZipFile:
        return False, f"Invalid .skill file (not a valid zip): {skill_file}"
    except Exception as e:
        return False, f"Error validating .skill file: {e}"

def main():
    parser = argparse.ArgumentParser(description="Validate a skill directory or .skill file")
    parser.add_argument("skill_path", help="Path to skill directory or .skill file")
    
    args = parser.parse_args()
    
    skill_path = Path(args.skill_path)
    
    if not skill_path.exists():
        print(f"❌ Error: Path does not exist: {skill_path}")
        return 1
    
    # Determine if it's a directory or file
    if skill_path.is_dir():
        valid, message = validate_skill_directory(skill_path)
    elif skill_path.is_file() and skill_path.suffix == ".skill":
        valid, message = validate_skill_file(skill_path)
    else:
        print(f"❌ Error: Path must be a directory or .skill file: {skill_path}")
        return 1
    
    if valid:
        print(f"✅ {message}")
        return 0
    else:
        print(f"❌ Validation failed: {message}")
        return 1

if __name__ == "__main__":
    sys.exit(main())