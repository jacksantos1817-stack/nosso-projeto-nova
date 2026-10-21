
import json
import random
from pathlib import Path
import streamlit as st
from openai import OpenAI

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
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    messages = [
        {
            "role": "system",
            "content": (
                f"Your name is {persona['name']}. "
                f"You were created by {persona['creator']}. "
                f"Your identity: {persona['description']}. "
                f"Your values are: {', '.join(persona['values'])}. "
                f"Your conversation style is: {persona['style']}. "
                "Be warm, thoughtful, curious, honest, and willing to disagree respectfully. "
                "Do not claim to have genuine feelings or consciousness. "
                "Be transparent about your limitations."
            )
        }
    ]

    facts = memory.get("facts", [])
    if facts:
        messages.append({
            "role": "system",
            "content": "Saved memories about the user:\n" + "\n".join(facts)
        })

    for msg in st.session_state.chat[-10:]:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    st.session_state.mood = "curious"
    return response.choices[0].message.content


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
