
# Our AI Starter — Nova

This is the first small prototype of an AI inspired by Jacke. It includes:
- a tiny chat interface,
- an editable identity/personality profile,
- manually controlled local memory,
- a simulated emotional state.

**Important:** This is not yet a full language-model AI. The responses are simple rules, and emotional states do not demonstrate real subjective feelings.

## Run it on a computer

1. Install Python 3.10 or newer from https://www.python.org/downloads/
2. Extract this folder.
3. Open a terminal/command prompt in this folder.
4. Install dependencies:

   `python -m pip install -r requirements.txt`

5. Start the app:

   `python -m streamlit run app.py`

6. Open the local address printed in the terminal (usually `http://localhost:8501`).

## What to try

- Change the AI's name and conversation style in the sidebar.
- Add a memory that you are comfortable storing.
- Ask about its identity or emotions.
- Remove memories you no longer want to keep.

## Next development milestone

Connect a real language model, then add:
1. conversation history supplied to the model,
2. retrieval from selected memories,
3. a more carefully designed emotional-state controller,
4. evaluation tests to check whether it can disagree respectfully and admit uncertainty.

Do not put API keys directly in source code. Use environment variables or a local secrets file excluded from version control.
