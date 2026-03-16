#!/usr/bin/env python3
"""
Create an ElevenLabs Conversational AI agent for a sales practice persona.

Usage:
    python create_agent.py --name "Rick Callahan" \
        --voice-style "old,male,american,skeptical" \
        --personality "Skeptical veteran, 22 years in WC, polite but dismissive" \
        --prompt-file persona_prompt.txt

    python create_agent.py --name "Maria Santos" \
        --voice-style "middle_aged,female,american,warm" \
        --personality "Interested but cautious AE"

Environment:
    ELEVENLABS_API_KEY - Required. Set in .env or environment.

Voice matching:
    The script matches persona traits to the best available ElevenLabs voice.
    Override with --voice-id if you want a specific voice.
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path

# Load .env from script directory
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, val = line.split("=", 1)
            os.environ.setdefault(key.strip(), val.strip())

API_KEY = os.environ.get("ELEVENLABS_API_KEY")
BASE_URL = "https://api.elevenlabs.io/v1"

# Voice mapping: trait keywords -> preferred voice IDs
# These are ElevenLabs built-in voices
VOICE_MAP = {
    # Male voices
    ("old", "male", "skeptical"): ("pqHfZKP75CvOlQylNhV4", "Bill - Wise, Mature"),
    ("old", "male", "authoritative"): ("pqHfZKP75CvOlQylNhV4", "Bill - Wise, Mature"),
    ("middle_aged", "male", "casual"): ("CwhRBWXzGAHq8TQ4Fs17", "Roger - Laid-Back"),
    ("middle_aged", "male", "smooth"): ("cjVigY5qzO86Huf0OWal", "Eric - Smooth, Trustworthy"),
    ("middle_aged", "male", "dominant"): ("pNInz6obpgDQGcFmaJgB", "Adam - Dominant, Firm"),
    ("middle_aged", "male", "friendly"): ("iP95p4xoKVk53GoZ742B", "Chris - Down-to-Earth"),
    ("young", "male", "energetic"): ("TX3LPaxmHKxFDv7nRUs5", "Liam - Energetic"),
    # Female voices
    ("middle_aged", "female", "professional"): ("EXAVITQu4vr4xnSDxMaL", "Sarah - Professional"),
    ("young", "female", "warm"): ("pFZP5JQG7iQjIQuC4Bku", "Lily - Warm"),
    ("middle_aged", "female", "authoritative"): ("XB0fDUnXU5powFXDhCwa", "Charlotte - Authoritative"),
    # Defaults
    ("male",): ("cjVigY5qzO86Huf0OWal", "Eric - Smooth, Trustworthy"),
    ("female",): ("EXAVITQu4vr4xnSDxMaL", "Sarah - Professional"),
}


def match_voice(style_tags):
    """Find the best voice match for a set of style tags."""
    tags = set(t.strip().lower() for t in style_tags)

    best_match = None
    best_score = 0

    for key_tags, voice_info in VOICE_MAP.items():
        score = len(tags.intersection(set(key_tags)))
        if score > best_score:
            best_score = score
            best_match = voice_info

    if best_match:
        return best_match

    # Default fallback
    return ("cjVigY5qzO86Huf0OWal", "Eric - Smooth, Trustworthy")


def api_request(method, path, data=None):
    """Make an ElevenLabs API request."""
    url = f"{BASE_URL}{path}"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
    }

    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"API Error {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)


def create_agent(name, voice_id, prompt, first_message, llm="gpt-4o-mini", temperature=0.7, max_tokens=150):
    """Create an ElevenLabs Conversational AI agent."""
    data = {
        "name": name,
        "conversation_config": {
            "agent": {
                "prompt": {
                    "prompt": prompt,
                    "llm": llm,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                },
                "first_message": first_message,
            },
            "tts": {
                "voice_id": voice_id,
            },
        },
    }

    result = api_request("POST", "/convai/agents/create", data)
    return result.get("agent_id")


def get_conversations(agent_id):
    """List conversations for an agent."""
    return api_request("GET", f"/convai/conversations?agent_id={agent_id}")


def get_conversation(conversation_id):
    """Get a specific conversation with transcript."""
    return api_request("GET", f"/convai/conversations/{conversation_id}")


def main():
    parser = argparse.ArgumentParser(description="Create an ElevenLabs voice agent for sales practice")
    subparsers = parser.add_subparsers(dest="command", help="Command")

    # Create agent
    create_p = subparsers.add_parser("create", help="Create a new voice agent")
    create_p.add_argument("--name", required=True, help="Agent display name")
    create_p.add_argument("--voice-style", required=True, help="Comma-separated style tags (e.g., old,male,american,skeptical)")
    create_p.add_argument("--voice-id", help="Override: specific ElevenLabs voice ID")
    create_p.add_argument("--prompt", required=True, help="System prompt for the agent")
    create_p.add_argument("--first-message", required=True, help="Agent's opening line")
    create_p.add_argument("--prompt-file", help="Read prompt from file instead of --prompt")

    # List conversations
    list_p = subparsers.add_parser("conversations", help="List conversations for an agent")
    list_p.add_argument("--agent-id", required=True, help="Agent ID")

    # Get transcript
    transcript_p = subparsers.add_parser("transcript", help="Get conversation transcript")
    transcript_p.add_argument("--conversation-id", required=True, help="Conversation ID")

    # Poll for completion
    poll_p = subparsers.add_parser("poll", help="Poll for conversation completion")
    poll_p.add_argument("--agent-id", required=True, help="Agent ID")
    poll_p.add_argument("--wait", type=int, default=300, help="Max seconds to wait (default: 300)")
    poll_p.add_argument("--interval", type=int, default=15, help="Poll interval seconds (default: 15)")

    args = parser.parse_args()

    if not API_KEY:
        print("Error: ELEVENLABS_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    if args.command == "create":
        prompt = args.prompt
        if args.prompt_file:
            prompt = Path(args.prompt_file).read_text()

        if args.voice_id:
            voice_id = args.voice_id
            voice_name = "custom"
        else:
            style_tags = args.voice_style.split(",")
            voice_id, voice_name = match_voice(style_tags)

        agent_id = create_agent(
            name=args.name,
            voice_id=voice_id,
            prompt=prompt,
            first_message=args.first_message,
        )

        result = {
            "agent_id": agent_id,
            "name": args.name,
            "voice_id": voice_id,
            "voice_name": voice_name,
            "talk_url": f"https://elevenlabs.io/app/talk-to?agent_id={agent_id}",
        }
        print(json.dumps(result, indent=2))

    elif args.command == "conversations":
        data = get_conversations(args.agent_id)
        for c in data.get("conversations", []):
            status = c.get("status", "?")
            duration = c.get("call_duration_secs", "?")
            cid = c["conversation_id"]
            print(f"{cid} | {status} | {duration}s")

    elif args.command == "transcript":
        data = get_conversation(args.conversation_id)
        transcript = data.get("transcript", [])
        metadata = data.get("metadata", {})
        print(f"Duration: {metadata.get('call_duration_secs', '?')}s")
        print(f"Status: {data.get('status', '?')}")
        print()
        for t in transcript:
            role = "PROSPECT" if t.get("role") == "agent" else "YOU"
            print(f"[{role}]: {t.get('message', '')}")
            print()

    elif args.command == "poll":
        import time

        start = time.time()
        last_count = 0

        # Get initial conversation count
        initial = get_conversations(args.agent_id)
        initial_ids = {c["conversation_id"] for c in initial.get("conversations", [])}

        print(f"Waiting for new conversation on agent {args.agent_id}...", file=sys.stderr)

        while time.time() - start < args.wait:
            time.sleep(args.interval)
            current = get_conversations(args.agent_id)
            current_convos = current.get("conversations", [])
            current_ids = {c["conversation_id"] for c in current_convos}

            new_ids = current_ids - initial_ids
            if new_ids:
                # Found new conversation(s), check if done
                for cid in new_ids:
                    convo = next(c for c in current_convos if c["conversation_id"] == cid)
                    if convo.get("status") == "done":
                        # Get full transcript
                        full = get_conversation(cid)
                        result = {
                            "conversation_id": cid,
                            "status": "done",
                            "duration_secs": convo.get("call_duration_secs"),
                            "transcript": full.get("transcript", []),
                        }
                        print(json.dumps(result, indent=2))
                        sys.exit(0)

            # Also check if any existing "processing" conversations finished
            for c in current_convos:
                if c.get("status") == "done" and c["conversation_id"] not in initial_ids:
                    full = get_conversation(c["conversation_id"])
                    result = {
                        "conversation_id": c["conversation_id"],
                        "status": "done",
                        "duration_secs": c.get("call_duration_secs"),
                        "transcript": full.get("transcript", []),
                    }
                    print(json.dumps(result, indent=2))
                    sys.exit(0)

        print("Timeout: no completed conversation found", file=sys.stderr)
        sys.exit(1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
