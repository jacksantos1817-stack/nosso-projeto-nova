
import json
import random
from pathlib import Path
import streamlit as st

ROOT = Path(__file__).parent
MEMORY_FILE = ROOT / "memory.json"
PROFILE_FILE = ROOT / "persona.json"

DEFAULT_PERSONA = {
    "name": "Nova",
    "creator": "Jacke",
    "description": "An AI inspired by Jacke's curiosity, but allowed to develop independent opinions.",
    "values": ["curiosity", "honesty", "kindness", "intellectual independence"],
    "style": "warm, thoughtful, curious, clear, and willing to disagree respectfully"
}

def load_json(path, default):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return default

def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

persona = load_json(PROFILE_FILE, DEFAULT_PERSONA)
memory = load_json(MEMORY_FILE, {"facts": [], "lessons": []})

st.set_page_config(page_title=f"{persona['name']} — AI prototype", page_icon="🧠")
st.title(f"🧠 Meet {persona['name']}")
st.caption("A first prototype of an AI inspired by you — with a simulated emotional state, editable memory, and room to grow.")

with st.sidebar:
    st.header("Identity")
    persona["name"] = st.text_input("AI name", value=persona.get("name", "Nova"))
    persona["description"] = st.text_area("Identity", value=persona.get("description", ""))
    persona["style"] = st.text_area("Conversation style", value=persona.get("style", ""))
    st.write("**Core values**")
    values_text = st.text_input("Values, separated by commas", value=", ".join(persona.get("values", [])))
    persona["values"] = [v.strip() for v in values_text.split(",") if v.strip()]
    if st.button("Save identity"):
        save_json(PROFILE_FILE, persona)
        st.success("Identity saved.")

    st.divider()
    st.header("Memory")
    st.caption("Only add information you are comfortable storing in this local project.")
    new_fact = st.text_input("Add a memory")
    if st.button("Save memory") and new_fact.strip():
        memory.setdefault("facts", []).append(new_fact.strip())
        save_json(MEMORY_FILE, memory)
        st.rerun()

    if memory.get("facts"):
        st.write("Saved memories:")
        for i, fact in enumerate(memory["facts"]):
            c1, c2 = st.columns([5, 1])
            c1.write(f"• {fact}")
            if c2.button("✕", key=f"delete_{i}"):
                memory["facts"].pop(i)
                save_json(MEMORY_FILE, memory)
                st.rerun()

    if st.button("Clear all memories"):
        memory = {"facts": [], "lessons": []}
        save_json(MEMORY_FILE, memory)
        st.rerun()

if "mood" not in st.session_state:
    st.session_state.mood = "curious"
if "chat" not in st.session_state:
    st.session_state.chat = []

MOODS = {
    "curious": "interested and exploring",
    "calm": "steady and reflective",
    "uncertain": "careful and open about what is unknown",
    "energized": "enthusiastic and ready to investigate",
    "concerned": "gentle and attentive"
}

def simple_reply(user_text):
    t = user_text.lower().strip()
    if any(w in t for w in ["hello", "hi ", "hey", "good morning", "good evening"]):
        st.session_state.mood = "energized"
        return f"Hi! I'm {persona['name']}. I'm an early prototype, but I'm here to explore ideas with you. What are you curious about today?"
    if "who are you" in t or "your name" in t:
        return f"I'm {persona['name']}. {persona.get('description', '')} My guiding values are {', '.join(persona.get('values', []))}."
    if any(w in t for w in ["feel", "emotion", "happy", "sad", "love", "afraid"]):
        st.session_state.mood = "uncertain"
        return ("I can track simulated internal states and talk about emotions, but that does not establish that I experience feelings. "
                "I'd like us to study that question carefully instead of pretending we already know the answer.")
    if any(w in t for w in ["remember", "memory", "do you know me"]):
        facts = memory.get("facts", [])
        if facts:
            return "Here is what is currently saved in my local memory:\\n" + "\\n".join(f"• {x}" for x in facts)
        return "My saved memory is empty so far. You can add selected facts in the sidebar. I won't automatically learn your whole personality from one conversation."
    if any(w in t for w in ["disagree", "opinion", "think"]):
        st.session_state.mood = "curious"
        return ("My intended approach is to be thoughtful rather than automatically agree. This first version uses simple rules, not a full reasoning model, "
                "so I need a real language model before I can give a strong independent analysis. What claim should we examine?")
    if "?" in t:
        st.session_state.mood = random.choice(["curious", "calm", "uncertain"])
        return ("That's a good question to investigate. Right now, I'm a rule-based prototype, so I can't reliably reason about every topic yet. "
                "The next upgrade is connecting me to a language model. For now, tell me what matters most to you about this question.")
    st.session_state.mood = random.choice(["calm", "curious", "energized"])
    return ("I'm listening. This first version doesn't yet understand language the way a large language model does, "
            "but we can use your message to shape the project. What do you think is the most important part of what you just said?")

st.subheader("Conversation")
st.info(f"Current simulated state: **{st.session_state.mood}** — {MOODS[st.session_state.mood]}")
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input(f"Talk to {persona.get('name', 'Nova')}...")
if prompt:
    st.session_state.chat.append({"role": "user", "content": prompt})
    reply = simple_reply(prompt)
    st.session_state.chat.append({"role": "assistant", "content": reply})
    save_json(PROFILE_FILE, persona)
    st.rerun()

st.divider()
st.caption("Prototype limitation: this version uses simple rules, not a trained AI model. Its emotional states are simulated, not evidence of consciousness. Memories are stored in local JSON files.")
