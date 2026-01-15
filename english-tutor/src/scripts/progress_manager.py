#!/usr/bin/env python3
"""
English Tutor Progress Manager

Manages learner data including vocabulary progress, mastery levels, and review scheduling
using a spaced repetition system (SM-2 algorithm).

Usage:
    python progress_manager.py init <learner_name> [--age AGE] [--level LEVEL]
    python progress_manager.py show <learner_name>
    python progress_manager.py get-daily <learner_name> [--count COUNT]
    python progress_manager.py add-word <learner_name> <word> [--level LEVEL]
    python progress_manager.py update <learner_name> <word> <quality>
    python progress_manager.py assess <learner_name> --level LEVEL --vocab-size SIZE
    python progress_manager.py stats <learner_name>
"""

import argparse
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import math

# Default data directory
DATA_DIR = Path.home() / ".english-tutor"


def get_learner_file(name: str) -> Path:
    """Get the path to a learner's data file."""
    return DATA_DIR / f"{name.lower()}.json"


def load_learner(name: str) -> Optional[dict]:
    """Load learner data from file."""
    filepath = get_learner_file(name)
    if not filepath.exists():
        return None
    with open(filepath, "r") as f:
        return json.load(f)


def save_learner(name: str, data: dict) -> None:
    """Save learner data to file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    filepath = get_learner_file(name)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, default=str)
    print(f"Saved learner data to {filepath}")


def init_learner(name: str, age: int = 10, level: int = 1, 
                 learner_type: str = "child", mother_tongue: Optional[str] = None,
                 interests: Optional[str] = None) -> dict:
    """Initialize a new learner profile."""
    data = {
        "name": name,
        "age": age,
        "current_level": level,
        "learner_type": learner_type,
        "mother_tongue": mother_tongue,
        "interests": interests,
        "created_date": datetime.now().isoformat(),
        "last_session": None,
        "total_sessions": 0,
        "vocabulary": {},  # word -> word_data
        "stats": {
            "words_learned": 0,
            "words_mastered": 0,
            "total_reviews": 0,
            "current_streak": 0,
            "longest_streak": 0,
            "estimated_vocab_size": level * 300 + 200
        },
        "assessment_history": [],
        "session_history": []
    }
    save_learner(name, data)
    print(f"Initialized learner profile for {name} (age {age}, level {level})")
    return data


def calculate_next_interval(word_data: dict, quality: int) -> dict:
    """
    Calculate next review interval using SM-2 algorithm.

    quality: 0-5 scale
        5 - perfect response
        4 - correct after hesitation
        3 - correct with difficulty
        2 - incorrect but recognized
        1 - incorrect, vaguely familiar
        0 - complete blackout
    """
    ef = word_data.get("ease_factor", 2.5)
    interval = word_data.get("interval_days", 1)
    repetitions = word_data.get("repetitions", 0)

    if quality >= 3:
        # Correct response
        if repetitions == 0:
            interval = 1
        elif repetitions == 1:
            interval = 3
        else:
            interval = round(interval * ef)
        repetitions += 1
    else:
        # Incorrect response - reset
        repetitions = 0
        interval = 1

    # Update ease factor
    ef = ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    ef = max(1.3, min(2.5, ef))  # Keep EF between 1.3 and 2.5

    # Calculate mastery level
    mastery = calculate_mastery_level(repetitions, ef, quality)

    next_review = (datetime.now() + timedelta(days=interval)).isoformat()

    return {
        "ease_factor": round(ef, 2),
        "interval_days": interval,
        "repetitions": repetitions,
        "next_review": next_review,
        "mastery_level": mastery
    }


def calculate_mastery_level(repetitions: int, ef: float, last_quality: int) -> int:
    """Calculate mastery level (0-5) based on performance."""
    if repetitions == 0:
        return 0  # New or reset
    elif repetitions <= 2:
        return 1  # Learning
    elif repetitions <= 4:
        return 2  # Familiar
    elif repetitions <= 7:
        return 3  # Known
    elif ef >= 2.0 and last_quality >= 4:
        return 5  # Permanent (after extended mastery)
    else:
        return 4  # Mastered


def get_daily_words(learner_data: dict, count: int = 5) -> dict:
    """
    Get words for today's session.
    Returns dict with 'review' and 'new' word lists.
    """
    today = datetime.now().date()
    vocabulary = learner_data.get("vocabulary", {})

    # Find words due for review
    due_words = []
    overdue_words = []

    for word, data in vocabulary.items():
        if "next_review" not in data:
            continue
        review_date = datetime.fromisoformat(data["next_review"]).date()
        days_overdue = (today - review_date).days

        if days_overdue > 0:
            overdue_words.append((word, data, days_overdue))
        elif days_overdue == 0:
            due_words.append((word, data, 0))

    # Sort: overdue first (most overdue), then due today (lowest mastery first)
    overdue_words.sort(key=lambda x: -x[2])
    due_words.sort(key=lambda x: x[1].get("mastery_level", 0))

    # Select review words (prioritize overdue)
    review_words = []
    for word, data, _ in overdue_words + due_words:
        if len(review_words) >= min(3, count):
            break
        review_words.append({
            "word": word,
            "mastery_level": data.get("mastery_level", 0),
            "last_review": data.get("last_review"),
            "review_count": data.get("repetitions", 0)
        })

    # Calculate how many new words to add
    new_word_slots = count - len(review_words)

    return {
        "review_words": review_words,
        "new_word_slots": new_word_slots,
        "total_due": len(overdue_words) + len(due_words),
        "overdue_count": len(overdue_words)
    }


def add_word(learner_data: dict, word: str, level: Optional[int] = None) -> dict:
    """Add a new word to learner's vocabulary."""
    if level is None:
        level = learner_data.get("current_level", 1)

    word_lower = word.lower()

    if word_lower in learner_data.get("vocabulary", {}):
        print(f"Word '{word}' already exists in vocabulary")
        return learner_data

    learner_data.setdefault("vocabulary", {})[word_lower] = {
        "word": word,
        "level": level,
        "introduced_date": datetime.now().isoformat(),
        "mastery_level": 0,
        "ease_factor": 2.5,
        "interval_days": 1,
        "repetitions": 0,
        "next_review": datetime.now().isoformat(),
        "review_history": [],
        "correct_streak": 0
    }

    learner_data["stats"]["words_learned"] += 1
    return learner_data


def update_word(learner_data: dict, word: str, quality: int) -> dict:
    """Update word after review with quality score (0-5)."""
    word_lower = word.lower()

    if word_lower not in learner_data.get("vocabulary", {}):
        print(f"Word '{word}' not found in vocabulary")
        return learner_data

    word_data = learner_data["vocabulary"][word_lower]

    # Record review
    word_data.setdefault("review_history", []).append({
        "date": datetime.now().isoformat(),
        "quality": quality
    })
    word_data["last_review"] = datetime.now().isoformat()

    # Update streak
    if quality >= 3:
        word_data["correct_streak"] = word_data.get("correct_streak", 0) + 1
    else:
        word_data["correct_streak"] = 0

    # Calculate new interval using SM-2
    updates = calculate_next_interval(word_data, quality)
    word_data.update(updates)

    # Update stats
    learner_data["stats"]["total_reviews"] += 1

    # Check if newly mastered
    if word_data["mastery_level"] >= 4:
        # Count mastered words
        mastered = sum(1 for w in learner_data["vocabulary"].values()
                      if w.get("mastery_level", 0) >= 4)
        learner_data["stats"]["words_mastered"] = mastered

    return learner_data


def update_assessment(learner_data: dict, level: int, vocab_size: int) -> dict:
    """Record assessment results and update learner level."""
    learner_data["assessment_history"].append({
        "date": datetime.now().isoformat(),
        "level": level,
        "estimated_vocab_size": vocab_size
    })
    learner_data["current_level"] = level
    learner_data["stats"]["estimated_vocab_size"] = vocab_size
    return learner_data


def update_interests(learner_data: dict, interests: str) -> dict:
    """Update learner interests."""
    learner_data["interests"] = interests
    return learner_data


def export_learner(name: str, output_path: Optional[str] = None) -> None:
    """Export learner profile to a specific location."""
    data = load_learner(name)
    if not data:
        print(f"Learner '{name}' not found.")
        return

    if output_path:
        target_path = Path(output_path)
    else:
        target_path = Path.cwd() / f"{name}-export.json"

    # Create parent directories if they don't exist
    target_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(target_path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    print(f"Exported learner profile for {name} to {target_path}")


def import_learner(import_path: str) -> None:
    """Import learner profile from a file."""
    source_path = Path(import_path)
    if not source_path.exists():
        print(f"File not found: {source_path}")
        return

    try:
        with open(source_path, "r") as f:
            data = json.load(f)
        
        name = data.get("name")
        if not name:
            print("Invalid profile: Missing learner name")
            return
            
        # Save to standard location
        save_learner(name, data)
        print(f"Imported learner profile for {name}")
    except json.JSONDecodeError:
        print(f"Error: {source_path} is not a valid JSON file")
    except Exception as e:
        print(f"Error importing profile: {e}")


def get_stats(learner_data: dict) -> dict:
    """Get comprehensive learner statistics."""
    vocabulary = learner_data.get("vocabulary", {})

    # Count by mastery level
    mastery_distribution = {i: 0 for i in range(6)}
    for word_data in vocabulary.values():
        level = word_data.get("mastery_level", 0)
        mastery_distribution[level] += 1

    # Calculate retention rate
    total_reviews = sum(len(w.get("review_history", [])) for w in vocabulary.values())
    correct_reviews = sum(
        sum(1 for r in w.get("review_history", []) if r.get("quality", 0) >= 3)
        for w in vocabulary.values()
    )
    retention_rate = correct_reviews / total_reviews if total_reviews > 0 else 0

    # Words due today
    today = datetime.now().date()
    due_today = sum(
        1 for w in vocabulary.values()
        if "next_review" in w and
        datetime.fromisoformat(w["next_review"]).date() <= today
    )

    return {
        "name": learner_data.get("name"),
        "current_level": learner_data.get("current_level"),
        "total_words": len(vocabulary),
        "mastery_distribution": mastery_distribution,
        "words_mastered": learner_data["stats"].get("words_mastered", 0),
        "retention_rate": round(retention_rate, 2),
        "total_reviews": total_reviews,
        "due_today": due_today,
        "estimated_vocab_size": learner_data["stats"].get("estimated_vocab_size", 0),
        "total_sessions": learner_data.get("total_sessions", 0),
        "current_streak": learner_data["stats"].get("current_streak", 0)
    }


def show_learner(learner_data: dict) -> None:
    """Display learner profile summary."""
    stats = get_stats(learner_data)

    print(f"\n{'='*50}")
    print(f"Learner: {stats['name']}")
    print(f"{'='*50}")
    print(f"Current Level: {stats['current_level']}")
    print(f"Estimated Vocabulary: {stats['estimated_vocab_size']} words")
    print(f"\nProgress:")
    print(f"  Total words tracked: {stats['total_words']}")
    print(f"  Words mastered: {stats['words_mastered']}")
    print(f"  Retention rate: {stats['retention_rate']*100:.0f}%")
    print(f"\nMastery Distribution:")
    level_names = ["New", "Learning", "Familiar", "Known", "Mastered", "Permanent"]
    for level, count in stats['mastery_distribution'].items():
        if count > 0:
            print(f"  {level_names[level]}: {count} words")
    print(f"\nToday:")
    print(f"  Words due for review: {stats['due_today']}")
    print(f"  Total sessions: {stats['total_sessions']}")


def main():
    parser = argparse.ArgumentParser(description="English Tutor Progress Manager")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # init command
    init_parser = subparsers.add_parser("init", help="Initialize new learner")
    init_parser.add_argument("name", help="Learner name")
    init_parser.add_argument("--age", type=int, default=10, help="Learner age")
    init_parser.add_argument("--level", type=int, default=1, help="Starting level (1-5)")
    init_parser.add_argument("--type", dest="learner_type", default="child", choices=["child", "adult"], help="Learner type")
    init_parser.add_argument("--mother-tongue", help="Mother tongue (for children)")
    init_parser.add_argument("--interests", help="Comma-separated list of interests")

    # show command
    show_parser = subparsers.add_parser("show", help="Show learner profile")
    show_parser.add_argument("name", help="Learner name")

    # get-daily command
    daily_parser = subparsers.add_parser("get-daily", help="Get daily words")
    daily_parser.add_argument("name", help="Learner name")
    daily_parser.add_argument("--count", type=int, default=5, help="Number of words")

    # add-word command
    add_parser = subparsers.add_parser("add-word", help="Add word to vocabulary")
    add_parser.add_argument("name", help="Learner name")
    add_parser.add_argument("word", help="Word to add")
    add_parser.add_argument("--level", type=int, help="Word level")

    # update command
    update_parser = subparsers.add_parser("update", help="Update word after review")
    update_parser.add_argument("name", help="Learner name")
    update_parser.add_argument("word", help="Word reviewed")
    update_parser.add_argument("quality", type=int, choices=range(6),
                               help="Quality score (0-5)")

    # assess command
    assess_parser = subparsers.add_parser("assess", help="Record assessment results")
    assess_parser.add_argument("name", help="Learner name")
    assess_parser.add_argument("--level", type=int, required=True, help="Assessed level")
    assess_parser.add_argument("--vocab-size", type=int, required=True,
                               help="Estimated vocabulary size")

    # update-interests command
    interests_parser = subparsers.add_parser("update-interests", help="Update learner interests")
    interests_parser.add_argument("name", help="Learner name")
    interests_parser.add_argument("--interests", required=True, help="New interests string")

    # export command
    export_parser = subparsers.add_parser("export", help="Export learner profile")
    export_parser.add_argument("name", help="Learner name")
    export_parser.add_argument("--output", help="Output file path")

    # import command
    import_parser = subparsers.add_parser("import", help="Import learner profile")
    import_parser.add_argument("path", help="Path to profile json file")

    # stats command
    stats_parser = subparsers.add_parser("stats", help="Get detailed statistics")
    stats_parser.add_argument("name", help="Learner name")

    args = parser.parse_args()

    if args.command == "init":
        init_learner(args.name, args.age, args.level, args.learner_type, args.mother_tongue, args.interests)

    elif args.command == "show":
        data = load_learner(args.name)
        if data:
            show_learner(data)
        else:
            print(f"Learner '{args.name}' not found. Use 'init' to create.")

    elif args.command == "get-daily":
        data = load_learner(args.name)
        if data:
            daily = get_daily_words(data, args.count)
            print(json.dumps(daily, indent=2))
        else:
            print(f"Learner '{args.name}' not found.")

    elif args.command == "add-word":
        data = load_learner(args.name)
        if data:
            data = add_word(data, args.word, args.level)
            save_learner(args.name, data)
        else:
            print(f"Learner '{args.name}' not found.")

    elif args.command == "update":
        data = load_learner(args.name)
        if data:
            data = update_word(data, args.word, args.quality)
            save_learner(args.name, data)
            print(f"Updated '{args.word}' with quality {args.quality}")
        else:
            print(f"Learner '{args.name}' not found.")

    elif args.command == "assess":
        data = load_learner(args.name)
        if data:
            data = update_assessment(data, args.level, args.vocab_size)
            save_learner(args.name, data)
            print(f"Assessment recorded: Level {args.level}, Vocab size {args.vocab_size}")
        else:
            print(f"Learner '{args.name}' not found.")

    elif args.command == "update-interests":
        data = load_learner(args.name)
        if data:
            data = update_interests(data, args.interests)
            save_learner(args.name, data)
            print(f"Updated interests for {args.name}")
        else:
            print(f"Learner '{args.name}' not found.")

    elif args.command == "export":
        export_learner(args.name, args.output)

    elif args.command == "import":
        import_learner(args.path)

    elif args.command == "stats":
        data = load_learner(args.name)
        if data:
            stats = get_stats(data)
            print(json.dumps(stats, indent=2))
        else:
            print(f"Learner '{args.name}' not found.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
