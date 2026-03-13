# Supported Transcript Formats

## Auto-Detection

Parse transcripts from any of these common formats:

### Fireflies.ai
```
Speaker Name (HH:MM:SS):
Text content here
```

### Zoom
```
HH:MM:SS Speaker Name
Text content here
```

### Otter.ai
```
Speaker Name  HH:MM:SS
Text content here
```

### Gong
```
[HH:MM:SS] Speaker Name: Text content here
```

### Google Meet (manual export)
```
Speaker Name
HH:MM:SS
Text content here
```

### Plain text / Custom
```
Name: Text content here
```

## Extraction Rules

When parsing a transcript:

1. Identify all unique speakers
2. Ask the user which speaker is the **seller** (the one practicing)
3. All other speakers are prospects/buyers
4. Extract turns with timestamps where available
5. Identify and tag key moments (see below)

## Key Moment Types

Tag each significant moment in the transcript:

- **OBJECTION**: Prospect raises a concern, pushback, or reason not to buy
- **BUYING_SIGNAL**: Prospect shows interest ("that's interesting", "how would that work for us", asking about pricing/timeline)
- **MISSED_OPPORTUNITY**: Seller could have asked a question or gone deeper but didn't
- **FEATURE_DUMP**: Seller listed multiple features without connecting to prospect's problem
- **GOOD_MOVE**: Seller did something effective (good question, reframe, storytelling)
- **AWKWARD_PAUSE**: Conversation stalled or went off track
- **CLOSE_ATTEMPT**: Either side moved toward next steps or commitment
