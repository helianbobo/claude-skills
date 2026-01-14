# Spaced Repetition System (SRS)

## Table of Contents
- [Overview](#overview)
- [SM-2 Algorithm](#sm-2-algorithm)
- [Mastery Levels](#mastery-levels)
- [Review Scheduling](#review-scheduling)
- [Daily Word Selection](#daily-word-selection)

## Overview

The spaced repetition system ensures optimal vocabulary retention by:
1. Introducing new words at a manageable pace
2. Reviewing words at increasing intervals as mastery improves
3. Bringing back words when performance drops
4. Balancing new learning with review

## SM-2 Algorithm

Use the SuperMemo SM-2 algorithm adapted for children:

### Core Formula

```
next_interval = previous_interval * ease_factor

where:
- ease_factor starts at 2.5 (range: 1.3 to 2.5)
- ease_factor adjusts based on response quality
```

### Response Quality Scale (0-5)

| Score | Description | Child-Friendly Meaning |
|-------|-------------|------------------------|
| 5 | Perfect response | Knew it instantly, used it correctly |
| 4 | Correct after hesitation | Got it right after thinking |
| 3 | Correct with difficulty | Needed a hint but remembered |
| 2 | Incorrect, but recognized | Said "oh yeah!" when shown answer |
| 1 | Incorrect, vaguely familiar | Remembered seeing it before |
| 0 | Complete blackout | No memory at all |

### Ease Factor Update

```
new_EF = old_EF + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))

Constraints:
- Minimum EF: 1.3
- Maximum EF: 2.5
```

### Interval Calculation

| Quality | Action |
|---------|--------|
| 0-2 | Reset to 1 day, reduce EF |
| 3 | Keep current interval, slight EF decrease |
| 4-5 | Multiply interval by EF, increase EF |

**Initial intervals:**
- First review: 1 day
- Second review: 3 days
- Third+ review: previous_interval * EF

## Mastery Levels

Track each word's mastery status:

| Level | Name | Criteria | Review Interval |
|-------|------|----------|-----------------|
| 0 | New | Just introduced | Same session |
| 1 | Learning | 1-2 correct responses | 1 day |
| 2 | Familiar | 3-4 correct responses | 3 days |
| 3 | Known | 5-7 correct responses | 1 week |
| 4 | Mastered | 8+ correct, EF > 2.0 | 2-4 weeks |
| 5 | Permanent | Mastered for 3+ months | Monthly check |

### Promotion Criteria
- Consecutive correct answers: 2+ at quality 4-5
- Minimum time at current level before promotion
- No "0" responses in last 5 reviews

### Demotion Triggers
- Quality 0-1 response: drop 1-2 levels
- Quality 2 response: drop 1 level
- 2+ consecutive quality ≤3: drop 1 level

## Review Scheduling

### Daily Review Queue Priority

1. **Overdue words** (missed scheduled review date)
   - Sort by days overdue (most overdue first)
   - Limit: include all overdue

2. **Due today** (scheduled for today)
   - Sort by mastery level (lower first)
   - Include all due

3. **New words** (from recommendation pool)
   - Based on level assessment
   - Daily limit: 3-5 new words

### Maximum Daily Load

| Learner Type | Review Words | New Words | Total |
|--------------|--------------|-----------|-------|
| Light | 10-15 | 3 | 13-18 |
| Standard | 15-20 | 5 | 20-25 |
| Intensive | 20-30 | 7 | 27-37 |

Default to "Standard" for children aged 8-12.

## Daily Word Selection

### Algorithm for 5 Focus Words

```
1. Get all words due for review today
2. Sort by priority:
   a. Overdue words (highest priority)
   b. Low mastery level words
   c. Words with declining performance
3. Select up to 3 review words
4. Fill remaining slots (2-3) with new words from level-appropriate pool
5. Ensure thematic coherence when possible
```

### New Word Selection Criteria

From the learner's current level word pool:
1. Not yet introduced to this learner
2. Matches learner's assessed vocabulary level
3. Useful for upcoming content/themes
4. Builds on previously learned words (word families, related concepts)

### Example Selection

```
Learner: Level 2, 150 words learned, 3 due for review

Review words (due today):
- "beautiful" (mastery 2, last seen 3 days ago)
- "different" (mastery 1, struggling)
- "remember" (mastery 3, due for 1-week check)

New words (from Level 2 pool):
- "excited" (connects to emotion words learned)
- "discover" (useful action verb)

Final 5: beautiful, different, remember, excited, discover
```

## Data Structure for Word Tracking

```json
{
  "word": "beautiful",
  "level": 2,
  "introduced_date": "2024-01-15",
  "mastery_level": 2,
  "ease_factor": 2.3,
  "interval_days": 3,
  "next_review": "2024-01-20",
  "review_history": [
    {"date": "2024-01-15", "quality": 4},
    {"date": "2024-01-16", "quality": 5},
    {"date": "2024-01-17", "quality": 3}
  ],
  "total_reviews": 3,
  "correct_streak": 2
}
```
