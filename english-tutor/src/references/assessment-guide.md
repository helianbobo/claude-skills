# Vocabulary Assessment Guide

## Table of Contents
- [Overview](#overview)
- [Initial Assessment Protocol](#initial-assessment-protocol)
- [Adaptive Testing Algorithm](#adaptive-testing-algorithm)
- [Level Estimation](#level-estimation)
- [Periodic Re-assessment](#periodic-re-assessment)

## Overview

Assessment serves three purposes:
1. **Initial placement**: Determine starting vocabulary level
2. **Progress tracking**: Measure growth over time
3. **Level adjustment**: Ensure appropriate difficulty

## Initial Assessment Protocol

### Assessment Structure

Total: 25-30 words across all levels (5-6 per level)
Time: 10-15 minutes
Format: Adaptive (adjusts based on responses)

### Word Selection for Assessment

Select test words that are:
- Representative of each level
- Unambiguous in meaning
- Testable through multiple methods

**Sample assessment words by level:**

| Level | Test Words |
|-------|------------|
| 1 | happy, water, jump, mother, blue, eat |
| 2 | excited, discover, different, neighbor, decide, remember |
| 3 | conclude, evidence, similar, process, analyze, describe |
| 4 | interpret, significant, contemporary, hypothesis, perspective, synthesize |
| 5 | ambiguous, comprehensive, implication, methodology, nuance, synthesize |

### Assessment Methods

Use 2-3 methods per word to get accurate picture:

**1. Recognition (Receptive)**
- "Which picture shows 'excited'?"
- "What does 'discover' mean?"
- Multiple choice with 4 options

**2. Production (Expressive)**
- "Use 'different' in a sentence"
- "Tell me a word that means the opposite of 'happy'"
- "What do you call someone who lives next to you?"

**3. Contextual Understanding**
- "The scientist made an important _____" (discovery)
- Read sentence, identify underlined word's meaning

### Scoring Criteria

| Response | Score | Interpretation |
|----------|-------|----------------|
| Instant correct | 2 | Fully knows word |
| Correct after thinking | 1.5 | Knows word |
| Partially correct | 1 | Familiar with word |
| Incorrect but close | 0.5 | Seen word before |
| No idea | 0 | Unknown word |

## Adaptive Testing Algorithm

### Start Point
Begin at estimated level based on age:
- Age 8: Start at Level 1
- Age 9: Start at Level 1-2
- Age 10: Start at Level 2
- Age 11: Start at Level 2-3
- Age 12: Start at Level 3

### Adaptation Rules

```
After each 3-word block:
- If 3/3 correct (score ≥ 5): Move up one level
- If 2/3 correct (score 3-5): Stay at current level
- If 0-1/3 correct (score < 3): Move down one level

Stop conditions:
- Tested all 5 levels, OR
- Two consecutive level drops, OR
- Reached ceiling (2 levels above consistent success)
```

### Example Adaptive Flow

```
Child: 10 years old, start at Level 2

Block 1 (Level 2): excited, discover, different
- Scores: 2, 1.5, 2 = 5.5 → Move to Level 3

Block 2 (Level 3): evidence, similar, analyze
- Scores: 1, 1.5, 0.5 = 3 → Stay at Level 3

Block 3 (Level 3): conclude, process, describe
- Scores: 1.5, 1, 1.5 = 4 → Stay at Level 3

Block 4 (Level 4): interpret, significant, perspective
- Scores: 0.5, 0, 0.5 = 1 → Move to Level 2

Block 5 (Level 2): remember, neighbor, decide
- Scores: 2, 2, 1.5 = 5.5 → Confirm Level 2

Result: Assigned Level 2 (solid at 2, struggling at 3)
```

## Level Estimation

### Calculation Formula

```
estimated_level = weighted_average(level_scores)

where:
- level_scores[i] = (correct_at_level[i] / tested_at_level[i]) * level_weight[i]
- level_weight = [1.0, 1.2, 1.4, 1.6, 1.8] (higher levels weighted more)
```

### Vocabulary Size Estimation

```
estimated_vocabulary = base_vocab + (level * growth_factor)

Approximate vocabulary sizes:
- Level 1: 300-500 words
- Level 2: 500-1000 words
- Level 3: 1000-1500 words
- Level 4: 1500-2500 words
- Level 5: 2500-3500+ words
```

### Confidence Scoring

Report confidence based on assessment consistency:
- High confidence: Clear pattern, consistent responses
- Medium confidence: Some inconsistency, borderline scores
- Low confidence: Erratic responses, need more data

## Periodic Re-assessment

### When to Re-assess

| Trigger | Assessment Type |
|---------|-----------------|
| Every 4 weeks | Mini-assessment (10 words) |
| Every 12 weeks | Full assessment (25-30 words) |
| After mastering 50 new words | Level-up check |
| Performance drop detected | Diagnostic assessment |

### Mini-Assessment Protocol

Quick 5-minute check:
1. 5 words from current level (should know)
2. 3 words from next level (stretch)
3. 2 words from previous assessments (retention check)

### Level Adjustment Criteria

**Move up one level if:**
- 90%+ accuracy on current level words
- 70%+ accuracy on next level test words
- Consistent performance over 2+ weeks

**Move down one level if:**
- Below 60% accuracy on current level words
- Struggling with previously mastered words
- Consistent difficulty over 1+ week

### Progress Report Metrics

Track and report:
```json
{
  "learner_name": "Zishen",
  "current_level": 2,
  "vocabulary_size_estimated": 750,
  "words_learned_total": 180,
  "words_mastered": 95,
  "words_in_progress": 85,
  "average_mastery_level": 2.8,
  "weekly_new_words": 25,
  "retention_rate": 0.88,
  "sessions_completed": 28,
  "last_assessment_date": "2024-01-15",
  "level_progress": 0.65
}
```

## Child-Friendly Assessment Tips

### Make it Fun
- Frame as a "word adventure" not a "test"
- Use encouraging language: "Let's see which words you already know!"
- Celebrate known words: "Wow, you know that one!"

### Reduce Anxiety
- Allow "I'm not sure" as valid response
- Don't rush - give thinking time
- Mix easy and hard words to build confidence

### Gather Accurate Data
- Note hesitation time (instant vs. thought about it)
- Watch for guessing patterns
- Ask follow-up: "Can you use it in a sentence?"
