import streamlit as st
from tutor import get_response
from tracker import update_patterns, get_summary

PATTERNS_FILE = "patterns.json"

st.set_page_config(page_title="Leeter")
st.title("Leeter")
st.caption("Socratic competitive programming tutor")

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "session_active" not in st.session_state:
    st.session_state.session_active = False

# --- Input Section ---
problem = st.text_area("Paste the problem statement here", height=200)
code = st.text_area("Paste your code attempt here", height=200)

col1, col2, col3, col4 = st.columns(4)
with col1:
    submit = st.button("Submit")
with col2:
    hint = st.button("Hint")
with col3:
    give_up = st.button("Give Up")
with col4:
    solved = st.button("Solved It ✓")

# --- Chat History ---
st.divider()
for message in st.session_state.conversation_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- User Follow Up ---
user_reply = st.chat_input("Reply to the tutor...")

# --- Weakness Summary Sidebar ---
with st.sidebar:
    st.header("My Weaknesses")
    summary = get_summary(PATTERNS_FILE)
    if summary:
        for pattern, counts in summary.items():
            total = counts["solved"] + counts["struggled"]
            rate = int((counts["solved"] / total) * 100)
            st.metric(label=pattern, value=f"{rate}% success", delta=f"{counts['struggled']} struggled")
    else:
        st.write("No data yet. Start a session!")

# --- Button Logic ---
if submit:
    if problem and code:
        user_message = f"Problem:\n{problem}\n\nMy code:\n{code}"
        response, st.session_state.conversation_history = get_response(
            st.session_state.conversation_history,
            user_message
        )
        st.session_state.session_active = True
        st.rerun()

if hint:
    response, st.session_state.conversation_history = get_response(
        st.session_state.conversation_history,
        "hint"
    )
    st.rerun()

if give_up:
    response, st.session_state.conversation_history = get_response(
        st.session_state.conversation_history,
        "give up"
    )
    pattern_response, _ = get_response(
        st.session_state.conversation_history,
        "List only the algorithmic patterns involved in this problem from the list in your instructions. Comma separated, nothing else."
    )
    patterns_found = [p.strip().lower() for p in pattern_response.split(",")]
    for pattern in patterns_found:
        update_patterns(PATTERNS_FILE, pattern, "struggled")
    st.session_state.conversation_history = []
    st.session_state.session_active = False
    st.rerun()

if solved:
    pattern_response, _ = get_response(
        st.session_state.conversation_history,
        "List only the algorithmic patterns involved in this problem from the list in your instructions. Comma separated, nothing else."
    )
    patterns_found = [p.strip().lower() for p in pattern_response.split(",")]
    for pattern in patterns_found:
        update_patterns(PATTERNS_FILE, pattern, "solved")
    st.session_state.conversation_history = []
    st.session_state.session_active = False
    st.rerun()

# --- User Reply ---
if user_reply:
    response, st.session_state.conversation_history = get_response(
        st.session_state.conversation_history,
        user_reply
    )
    st.rerun()