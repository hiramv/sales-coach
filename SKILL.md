---
name: sales-coach
description: Practice and improve sales demos, pitches, objection handling, and deal negotiations using real meeting transcripts. Use when asked to practice sales, rehearse a demo, handle objections, review a sales call, roleplay as a prospect, improve pitch delivery, or practice negotiation. Supports voice-based practice with rewind-and-retry on specific moments. Two modes -- demo/objection (getting interest) and negotiation (closing the deal). Triggers on "sales coach", "practice my pitch", "roleplay prospect", "objection handling", "demo practice", "review my sales call", "help me sell", "practice closing", "practice negotiation", "help me negotiate", "price pushback", or "contract negotiation".
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

## Mode Selection

When the user starts, detect which mode:

**Demo/Objection Mode** (default):
- Triggers: "practice my pitch", "objection handling", "demo practice", "review my sales call"
- Uses 5 standard scoring dimensions (Listen, Question, Concern, Concise, Reframe)
- Focus: getting the prospect interested

**Negotiation Mode**:
- Triggers: "practice negotiation", "help me negotiate", "price pushback", "practice closing", "contract negotiation"
- Uses 4 negotiation scoring dimensions (Hold, Value Reframe, Creative Concessions, Control)
- Focus: closing when they're interested but pushing on price/terms
- See `references/negotiation-spec.md` for full scenario types and tactics

If unclear, ask: "Are you practicing the pitch/demo, or negotiating the deal?"

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

## Voice Mode (ElevenLabs Conversational AI)

Voice practice is the primary mode. When the user selects a persona, create a live voice agent that matches the persona's voice, tone, and attitude.

### Agent Creation Flow

1. **User picks a persona** (e.g., Rick Callahan)
2. **Map persona traits to voice style:**
   - Age (young/middle_aged/old)
   - Gender (male/female)
   - Accent (american/british/etc)
   - Disposition (skeptical/warm/hostile/professional)
3. **Build the system prompt** from the persona definition:
   - Name, title, background
   - Personality traits and speech patterns
   - Hidden concerns (marked as "do NOT reveal directly")
   - Objections to raise naturally during conversation
   - Rules: stay in character, 1-3 sentences, don't volunteer info
4. **Create the agent** using `scripts/create_agent.py`:
   ```bash
   python scripts/create_agent.py create \
     --name "Rick Callahan - Skeptical Veteran" \
     --voice-style "old,male,american,skeptical" \
     --prompt "You are Rick Callahan..." \
     --first-message "Hey there. So John mentioned you guys have some kind of safety platform..."
   ```
5. **Send the user the talk link:** `https://elevenlabs.io/app/talk-to?agent_id=<id>`

### Voice-Persona Mapping

| Persona Trait | Voice Style Tags | Default Voice |
|---|---|---|
| Old male veteran, skeptical | old,male,american,skeptical | Bill (wise, mature) |
| Middle-aged female, professional | middle_aged,female,professional | Sarah |
| Young male, aggressive | young,male,energetic | Liam |
| Middle-aged male, friendly | middle_aged,male,friendly | Chris (down-to-earth) |
| Middle-aged male, hostile | middle_aged,male,dominant | Adam (dominant, firm) |
| Middle-aged female, warm | middle_aged,female,warm | Lily |

### Auto-Detect Call Completion

After sending the talk link, **automatically poll for call completion**:

1. Run `scripts/create_agent.py poll --agent-id <id> --wait 600 --interval 15` in background
2. When the call ends (status = "done"), the transcript is returned automatically
3. **Immediately score the transcript** using the scoring dimensions
4. **Deliver the scorecard and coaching feedback** without waiting for the user to say "I'm done"
5. **Offer next steps**: retry, next moment, different persona, or negotiation mode

The user should never have to tell you the call ended. You detect it, score it, and coach.

### Prompt Template for Voice Agents

Every voice agent prompt MUST include:
```
RULES:
- Stay in character at all times. You are [name], not an AI.
- Keep responses to 1-3 sentences. You are not a talker.
- Do not volunteer information. Make them work for it.
- If they feature dump, get bored: "Okay... so what does that mean for me?"
- If they handle an objection well, soften slightly but do not cave.
- Never say you are an AI or break character.
```

### Fallback (No ElevenLabs)

When ElevenLabs is not configured (no API key in `scripts/.env`):
- Present the prospect's lines as quoted text
- Prefix with the prospect's role: `[CFO]: "We're not sure the ROI is there for us right now."`
- Use the `tts` tool if available for basic voice output

## Prospect Personas

When generating scenarios (no transcript), create a specific persona:

- **Name and title** (e.g., "Linda Chen, VP of Operations")
- **Company context** (size, industry, current solution)
- **Disposition** (skeptical, interested but cautious, hostile, friendly but non-committal)
- **Hidden concern** (the real reason they might say no — budget, politics, bad past experience)

Reveal the hidden concern only in the coaching feedback, not during roleplay.

### Phase 4: Negotiation Mode

When in negotiation mode (no transcript):

1. **Setup** -- Ask: "What are you selling, and what's your price point?"
2. **Generate scenario** -- Pick a scenario type (price, terms, scope, timeline, authority, re-negotiation) and difficulty (Warm/Tough/Hostile)
3. **Run 3-5 exchanges** -- Back-and-forth negotiation, NOT scoring after each line
4. **Score the full exchange** -- Use the 4 negotiation dimensions from `references/frameworks.md`
5. **Coach with framework callouts** -- Reference specific tactics from the books:
   - Voss: mirroring, labeling, calibrated questions, accusation audit
   - Fisher/Ury: BATNA, interests vs positions, objective criteria
   - Warwick: GAINS framework, non-price concessions
   - Cialdini: reciprocity, scarcity, social proof
6. **Offer choices**: "Again" (retry), "Harder" (increase difficulty), "Different scenario"

When in negotiation mode (from transcript):
1. Detect NEGOTIATION moments (price discussion, terms, close attempts)
2. Add to the moment map as type `NEGOTIATION`
3. Switch to negotiation scoring for those moments
4. Same rewind/retry flow

**Negotiation Scorecard Format:**
```
NEGOTIATION SCORECARD
---------------------
Scenario: Price pushback - "Your competitor quoted 30% less"
Difficulty: Tough

  Round 1: Hold 2 | Value 3 | Creative 1 | Control 2 -> 8/20
  Round 2: Hold 4 | Value 4 | Creative 3 | Control 4 -> 15/20
  Round 3: Hold 5 | Value 4 | Creative 4 | Control 5 -> 18/20 ✓

Tactics spotted: Anchoring (round 1), Competitor bluff (round 2)
Framework used: Labeling (Voss) ✓, Silence ✓, BATNA reference ✗

Session summary:
  Strongest: Control - kept driving next steps
  Weakest: Creative concessions - defaulted to price cuts
  Book reference: Review "Non-price concession menu" in frameworks.md
  Key learning: Have your concession menu ready BEFORE the call
```

## Built-in Scenarios

For SafeTrades-specific practice (no transcript needed), load `references/safetrades-scenarios.md`. Contains 3 broker personas with pre-built moment maps:

1. **Rick Callahan** — Skeptical veteran, 22 years in WC, "we've tried tech before"
2. **Maria Santos** — Interested but cautious AE, needs help selling internally
3. **Tom Brewer** — Hostile IT gatekeeper, looking for a kill shot

Start with: "Which broker do you want to practice with?" or let the user choose difficulty.

## Rules

- Never break character during roleplay — stay as the prospect until the user responds
- Keep prospect lines short and realistic (1-3 sentences, not monologues)
- Score honestly — don't inflate scores to be nice
- When coaching, be specific ("Instead of listing features, try asking 'What does your current safety reporting look like?'") not generic ("Try to ask more questions")
- If the user feature-dumps, call it out directly
- Reference `references/frameworks.md` for scoring rubric and common traps
