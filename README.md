# Sales Coach 🎙️

Practice sales demos with AI prospects that talk back. Built as an [OpenClaw](https://github.com/openclaw/openclaw) skill.

## What it does

- **Live voice practice** — AI plays your prospect on a real-time voice call (ElevenLabs Conversational AI)
- **Realistic pushback** — prospects push back on objections, call out feature dumps, and react naturally
- **Transcript analysis** — upload real meeting transcripts to practice with actual objections you've faced
- **Rewind & retry** — bookmark key moments and practice the same objection until your response is automatic
- **Performance tracking** — scored on 5 dimensions after each session, logged to Google Sheets for trend analysis

## Scoring Dimensions

Each practice attempt is scored 1-5 on:

- 🎧 **Listen vs. Defend** — did you acknowledge the concern or immediately justify?
- ❓ **Question Quality** — did you ask an open question that uncovered the real concern?
- 🎯 **Concern Addressed** — did you identify and address the underlying fear?
- ✂️ **Conciseness** — tight response or feature dump?
- 🔄 **Reframe Strength** — did you turn the objection into a reason to buy?

## Setup

### Prerequisites

- [OpenClaw](https://github.com/openclaw/openclaw) installed
- [ElevenLabs](https://elevenlabs.io) API key (free tier works)
- Python 3.9+ with `elevenlabs` and `python-dotenv` packages
- Google Sheet for performance tracking (optional but recommended)
- `gog` CLI configured for Google Sheets access ([gogcli.sh](https://gogcli.sh))

### Install

1. Copy the `sales-coach` folder to your OpenClaw skills directory:
   ```bash
   cp -r sales-coach ~/clawd/skills/
   ```

2. Create your config file:
   ```bash
   cat > ~/clawd/skills/sales-coach/scripts/.env << EOF
   ELEVENLABS_API_KEY=your_key_here
   ELEVENLABS_VOICE_ID=EXAVITQu4vr4xnSDxMaL
   EOF
   ```

3. Install Python dependencies:
   ```bash
   pip install elevenlabs python-dotenv
   ```

4. (Optional) Create a Google Sheet for tracking and add the sheet ID to your config:
   ```bash
   echo "GOOGLE_SHEET_ID=your_sheet_id_here" >> ~/clawd/skills/sales-coach/scripts/.env
   ```
   The agent will auto-create headers and log scores after each session.

## Usage

### Quick start (no transcript needed)

Tell your OpenClaw agent:

> "I want to practice my sales pitch. I sell [your product] to [your buyer persona]. Common objections are [list them]."

The agent will:
1. Create a voice prospect with realistic pushback
2. Give you a link to start a live voice call
3. Score your performance after the call
4. Track improvement over time

### With a real transcript

> "Here's a transcript from my last demo call. Help me practice the tough moments."

Paste or upload a transcript from any of these platforms:
- **Fireflies.ai**
- **Zoom**
- **Otter.ai**
- **Gong**
- **Google Meet**
- **Plain text / custom format**

The agent will:
1. Extract key moments (objections, buying signals, missed opportunities)
2. Build a practice session around those moments
3. Let you rewind and retry any moment

## Customization

### Voice selection

Change the voice in `.env` by setting `ELEVENLABS_VOICE_ID`. Browse voices at [ElevenLabs Voice Library](https://elevenlabs.io/voice-library).

### Prospect personas

Describe any buyer persona and the agent builds a practice scenario:
- Industry, role, years of experience
- Disposition (skeptical, friendly, hostile)
- Specific objections and hidden concerns

## File Structure

```
sales-coach/
├── SKILL.md                        — Core workflow and practice mode
├── README.md                       — This file
├── scripts/
│   └── speak.py                    — ElevenLabs TTS helper
└── references/
    ├── frameworks.md               — Scoring rubric, common traps, reframe patterns
    └── transcript-format.md        — Supported transcript formats
```

## Architecture Note

This skill works through your existing OpenClaw agent — no separate agent definitions needed. The AI prospect personas are created as ElevenLabs Conversational AI voice agents, not OpenClaw agents. Your main agent handles transcript analysis, scoring, and coaching.

## Privacy

Everything runs locally. No transcripts or recordings are uploaded to any server. ElevenLabs processes voice during live calls only (same as any voice API). Your sales conversations stay on your machine.

## License

MIT — do whatever you want with it.

## Author

Built by [Hiram Vazquez](https://linkedin.com/in/hiramv) because technical founders shouldn't have to wing it on sales calls.
