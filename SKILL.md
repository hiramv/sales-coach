---
name: sales-coach
description: Practice and improve sales demos, pitches, and objection handling using real meeting transcripts. Use when asked to practice sales, rehearse a demo, handle objections, review a sales call, roleplay as a prospect, or improve pitch delivery. Supports voice-based practice with rewind-and-retry on specific moments. Triggers on "sales coach", "practice my pitch", "roleplay prospect", "objection handling", "demo practice", "review my sales call", "help me sell", or "practice closing".
---

# Sales Coach

Practice sales conversations using real meeting transcripts. Extract key moments, roleplay as the prospect, score responses, and track improvement through repeated practice.

## Quick Start

If the user has a transcript:
1. Parse it (see `references/transcript-format.md` for supported formats)
2. Ask which speaker is the seller
3. Extract and bookmark key moments
4. Start practice mode

If no transcript:
1. Ask about their product/service and target buyer
2. Generate realistic objection scenarios based on their context
3. Start practice mode with generated scenarios

## Core Workflow

### Phase 1: Transcript Analysis

Parse the transcript and extract a **moment map** — a numbered list of key moments:

```
MOMENT MAP
──────────
#1 [02:14] OBJECTION — "We already have a safety program"
#2 [05:30] BUYING_SIGNAL — "How would that integrate with our current system?"
#3 [07:45] FEATURE_DUMP — Seller listed 4 features without asking a question
#4 [11:20] MISSED_OPPORTUNITY — Prospect mentioned budget concerns, seller didn't dig in
#5 [14:00] OBJECTION — "We'd need to get IT involved"
#6 [18:30] CLOSE_ATTEMPT — "What would next steps look like?"
```

See `references/transcript-format.md` for format detection and moment types.

Present the moment map and ask: "Which moment do you want to practice first? Or say 'start from #1' to go in order."

### Phase 2: Practice Mode

For each moment:

1. **Set the scene** — Briefly describe what happened in the conversation leading up to this moment (2-3 sentences max)
2. **Play the prospect** — Deliver the prospect's line (use TTS if voice is available via the `tts` tool)
3. **Wait for the user's response** — Let them practice their reply
4. **Score the response** — Use the 5 dimensions from `references/frameworks.md`
5. **Coach** — Give specific, actionable feedback:
   - What worked
   - What to change
   - A suggested alternative response (brief)
6. **Offer choices**:
   - **"Again"** — Retry this same moment
   - **"Next"** — Move to the next bookmarked moment
   - **"Rewind to #N"** — Jump to any moment by number

### Phase 3: Scoring & Tracking

Track attempts per moment in a session scorecard:

```
SESSION SCORECARD
─────────────────
Moment #1: "We already have a safety program"
  Attempt 1: Listen 2 | Question 1 | Concern 2 | Concise 3 | Reframe 1 → 9/25
  Attempt 2: Listen 4 | Question 3 | Concern 3 | Concise 4 | Reframe 3 → 17/25
  Attempt 3: Listen 5 | Question 4 | Concern 4 | Concise 5 | Reframe 4 → 22/25 ✓

Moment #3: Feature dump at 07:45
  Attempt 1: Listen 3 | Question 2 | Concern 2 | Concise 1 | Reframe 2 → 10/25
  ...
```

After practicing 3+ moments, provide a **session summary**:
- Strongest dimension (e.g., "You're good at staying concise")
- Weakest dimension (e.g., "Work on asking follow-up questions instead of defending")
- Overall trend (improving, plateauing, specific patterns)
- Top 1-2 things to focus on next time

## Voice Mode

When TTS is available (check for `tts` tool):
- Use voice for the prospect's lines to make practice feel realistic
- Keep the user's response as text (they type or voice-to-text their reply)
- Use a different vocal style than the default — slightly skeptical, professional tone

When TTS is not available:
- Present the prospect's lines as quoted text
- Prefix with the prospect's role: `[CFO]: "We're not sure the ROI is there for us right now."`

## Prospect Personas

When generating scenarios (no transcript), create a specific persona:

- **Name and title** (e.g., "Linda Chen, VP of Operations")
- **Company context** (size, industry, current solution)
- **Disposition** (skeptical, interested but cautious, hostile, friendly but non-committal)
- **Hidden concern** (the real reason they might say no — budget, politics, bad past experience)

Reveal the hidden concern only in the coaching feedback, not during roleplay.

## Rules

- Never break character during roleplay — stay as the prospect until the user responds
- Keep prospect lines short and realistic (1-3 sentences, not monologues)
- Score honestly — don't inflate scores to be nice
- When coaching, be specific ("Instead of listing features, try asking 'What does your current safety reporting look like?'") not generic ("Try to ask more questions")
- If the user feature-dumps, call it out directly
- Reference `references/frameworks.md` for scoring rubric and common traps
