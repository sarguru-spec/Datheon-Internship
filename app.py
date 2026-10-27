import html
import time
import streamlit as st
from agent_core import get_agent_executor

# --- Helper function to match the UI's expected format ---
def format_history(turns, max_turns: int = 6) -> str:
    recent = turns[-max_turns * 2:]
    return "\n".join(f"{role}: {text}" for role, text in recent)

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
html, body, .stApp, button, textarea, [data-testid="stMarkdownContainer"] {font-family:'Inter',system-ui,sans-serif;}
.stApp {background:#0f172a;}
#MainMenu, footer, [data-testid="stDecoration"] {display:none;}
header[data-testid="stHeader"] {background:transparent;}
.block-container {max-width:820px; padding-top:2.5rem; padding-bottom:8rem;}

/* Header */
.hero-title {display:inline-block; margin:0; font-size:2.5rem; font-weight:700; letter-spacing:-0.025em;
  background:linear-gradient(90deg,#38bdf8,#c084fc); -webkit-background-clip:text; background-clip:text;
  -webkit-text-fill-color:transparent; color:transparent;}
.hero-sub {color:#94a3b8; font-size:1rem; margin:.4rem 0 2rem;}

/* Chat bubbles */
[data-testid^="stChatMessageAvatar"], [data-testid^="chatAvatarIcon"] {display:none;}
[data-testid="stChatMessage"] {width:fit-content; min-width:280px; max-width:92%; padding:16px 20px; margin:0 0 16px;
  background:#1e293b; border:1px solid #334155; border-radius:16px; box-shadow:0 10px 30px -12px rgba(0,0,0,.55);}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"], [data-testid="chatAvatarIcon-user"]) {
  min-width:0; max-width:80%; margin-left:auto; background:#2563eb; border-color:#2563eb;
  box-shadow:0 10px 30px -10px rgba(37,99,235,.55);}
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li {color:#f8fafc; line-height:1.65; font-size:.97rem;}
[data-testid="stChatMessage"] code {font-family:'JetBrains Mono',monospace; background:#0f172a; color:#7dd3fc; border-radius:6px; padding:2px 6px;}

/* Floating input */
[data-testid="stBottom"], [data-testid="stBottom"] > div {background:linear-gradient(180deg,rgba(15,23,42,0),#0f172a 45%) !important;}
[data-testid="stChatInput"] {background:#1e293b; border:1px solid #334155; border-radius:18px;
  box-shadow:0 16px 40px -14px rgba(0,0,0,.7); transition:border-color .2s, box-shadow .2s;}
[data-testid="stChatInput"] > div {background:transparent; border:none;}
[data-testid="stChatInput"]:focus-within {border-color:#38bdf8; box-shadow:0 0 0 3px rgba(56,189,248,.15), 0 16px 40px -14px rgba(0,0,0,.7);}
[data-testid="stChatInput"] textarea {color:#f8fafc; background:transparent;}
[data-testid="stChatInput"] textarea::placeholder {color:#64748b;}
[data-testid="stChatInputSubmitButton"] {background:#2563eb; color:#fff; border-radius:12px;}

/* Sidebar */
[data-testid="stSidebar"] {background:#0b1220; border-right:1px solid #1e293b;}
.side-brand {font-weight:600; font-size:1.05rem; color:#f8fafc; letter-spacing:-.01em;}
.side-label {text-transform:uppercase; letter-spacing:.12em; font-size:.68rem; color:#64748b; margin:1.6rem 0 .7rem;}
.tool-pill {display:flex; align-items:center; gap:8px; width:fit-content; margin-bottom:8px; padding:6px 14px;
  font-family:'JetBrains Mono',monospace; font-size:.78rem; color:#7dd3fc;
  background:rgba(56,189,248,.08); border:1px solid rgba(56,189,248,.25); border-radius:999px;}
.tool-pill::before {content:""; width:6px; height:6px; border-radius:50%; background:#34d399; box-shadow:0 0 8px #34d399;}

/* Buttons (clear + suggestions) */
.stButton > button {background:#1e293b; color:#e2e8f0; border:1px solid #334155; border-radius:14px;
  padding:.7rem 1rem; text-align:left; font-weight:500; transition:all .2s;}
.stButton > button:hover {border-color:#38bdf8; color:#fff; background:#243449; transform:translateY(-1px);}

/* Reasoning expander */
[data-testid="stExpander"] {background:#162032; border:1px solid #334155; border-radius:12px; margin-bottom:12px;}
[data-testid="stExpander"] summary {color:#94a3b8; font-size:.85rem;}

/* Thinking card */
.think-card {background:#162032; border:1px solid #334155; border-radius:14px; padding:14px 16px; margin-bottom:6px;}
.think-head {display:flex; align-items:center; gap:10px; color:#cbd5e1; font-size:.88rem; font-weight:500;}
.dots {display:inline-flex; gap:4px;}
.dots i {width:6px; height:6px; border-radius:50%; background:#38bdf8; animation:bounce 1.2s infinite ease-in-out;}
.dots i:nth-child(2) {animation-delay:.15s; background:#818cf8;}
.dots i:nth-child(3) {animation-delay:.3s; background:#c084fc;}
@keyframes bounce {0%,80%,100% {transform:translateY(0); opacity:.4;} 40% {transform:translateY(-5px); opacity:1;}}
.think-bar {height:2px; margin:12px 0 4px; border-radius:2px; background-size:200% 100%;
  background-image:linear-gradient(90deg,#1e293b 0%,#38bdf8 40%,#c084fc 60%,#1e293b 100%); animation:shimmer 1.6s linear infinite;}
@keyframes shimmer {0% {background-position:200% 0;} 100% {background-position:-200% 0;}}
.step {margin-top:12px; padding-top:12px; border-top:1px solid #243449;}
.step .pill {font-family:'JetBrains Mono',monospace; font-size:.72rem; color:#7dd3fc; background:rgba(56,189,248,.1);
  border:1px solid rgba(56,189,248,.25); border-radius:999px; padding:2px 10px; margin-right:8px;}
.step .step-in {font-family:'JetBrains Mono',monospace; font-size:.78rem; color:#cbd5e1; background:transparent;}
.step .step-obs {margin-top:6px; font-size:.8rem; color:#94a3b8; line-height:1.5;}
.step .step-obs.running {color:#64748b; font-style:italic;}
"""
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

TOOLS = ["web_search", "python_calculator", "read_local_file"]
EXAMPLES = [
    "🧮 What is (4829 * 17) + sqrt(2025)? Verify it with Python.",
    "🔍 Search the web for the latest news on open-source LLMs.",
    "📂 Read sample_resume.txt and list the key skills.",
]

@st.cache_resource
def get_agent():
    return get_agent_executor()

try:
    agent_executor = get_agent()
except Exception as e:
    st.error(f"Could not start the agent: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

def clean(text, limit):
    return html.escape(" ".join(str(text).split())[:limit]).replace("$", "&#36;")

def steps_html(steps):
    out = ""
    for s in steps:
        obs = (f'<div class="step-obs">{clean(s["observation"], 320)}</div>' if s.get("observation")
               else '<div class="step-obs running">running…</div>')
        out += (f'<div class="step"><span class="pill">{clean(s["tool"], 40)}</span>'
                f'<code class="step-in">{clean(s["input"], 200)}</code>{obs}</div>')
    return out

def think_card(steps):
    return ('<div class="think-card"><div class="think-head"><span class="dots"><i></i><i></i><i></i></span>'
            'Thinking…</div><div class="think-bar"></div>' + steps_html(steps) + '</div>')

def stream_words(text):
    words = text.split(" ")
    for i in range(0, len(words), 2):
        yield " ".join(words[i:i + 2]) + " "
        time.sleep(0.03)

# --- Sidebar ---
with st.sidebar:
    st.markdown('<div class="side-brand">✦ Agent Console</div>', unsafe_allow_html=True)
    st.markdown('<div class="side-label">Active tools</div>'
                + "".join(f'<div class="tool-pill">{t}</div>' for t in TOOLS), unsafe_allow_html=True)
    st.markdown('<div class="side-label">Session</div>', unsafe_allow_html=True)
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Header ---
st.markdown('<h1 class="hero-title">Multi-Tool AI Agent</h1>'
            '<div class="hero-sub">Reasons step by step, searches the web, runs Python and reads your files.</div>',
            unsafe_allow_html=True)

question = st.chat_input("Ask anything — I can search, calculate and read files…") \
    or st.session_state.pop("pending", None)

# --- Empty state ---
if not st.session_state.messages and not question:
    st.markdown('<div class="side-label" style="margin-top:0">Try one of these</div>', unsafe_allow_html=True)
    for ex in EXAMPLES:
        st.button(ex, key=ex, use_container_width=True,
                  on_click=lambda t=ex: st.session_state.update(pending=t[3:].strip()))

# --- History ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if m.get("steps"):
            with st.expander(f"Reasoning steps · {len(m['steps'])}"):
                st.markdown(steps_html(m["steps"]), unsafe_allow_html=True)
        st.markdown(m["content"])

# --- New turn ---
if question:
    history = format_history([("User" if m["role"] == "user" else "Assistant", m["content"])
                              for m in st.session_state.messages])
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        think = st.empty()
        think.markdown(think_card([]), unsafe_allow_html=True)
        steps, final = [], ""
        try:
            for chunk in agent_executor.stream({"input": question, "chat_history": history}):
                if "actions" in chunk:
                    for a in chunk["actions"]:
                        steps.append({"tool": a.tool, "input": a.tool_input, "observation": None})
                elif "steps" in chunk:
                    for s in chunk["steps"]:
                        for item in reversed(steps):
                            if item["observation"] is None and item["tool"] == s.action.tool:
                                item["observation"] = str(s.observation)
                                break
                elif "output" in chunk:
                    final = chunk["output"]
                think.markdown(think_card(steps), unsafe_allow_html=True)
        except Exception as e:
            final = f"❌ Something went wrong: {e}"

        think.empty()
        if steps:
            with st.expander(f"Reasoning steps · {len(steps)}"):
                st.markdown(steps_html(steps), unsafe_allow_html=True)
        st.write_stream(stream_words(final))

    st.session_state.messages.append({"role": "assistant", "content": final, "steps": steps})