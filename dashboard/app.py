import streamlit as st
import subprocess
import threading
import queue
import sys
import time
from pathlib import Path
from streamlit_ace import st_ace

# ── Paths ─────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent

VENV_PYTHON = PROJECT_ROOT / "venv" / "Scripts" / "python.exe"

PYTHON_BIN = str(VENV_PYTHON) if VENV_PYTHON.exists() else sys.executable

# ── Streamlit Config ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SpecForge",
    page_icon="⚙️",
    layout="wide",
)

# ── Session State ─────────────────────────────────────────────────────────────
if "process" not in st.session_state:
    st.session_state.process = None

if "output_queue" not in st.session_state:
    st.session_state.output_queue = queue.Queue()

if "terminal_output" not in st.session_state:
    st.session_state.terminal_output = ""

# ── Output Reader ─────────────────────────────────────────────────────────────
def read_output(process, q):

    while True:

        line = process.stdout.readline()

        if not line:
            break

        q.put(line)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:

    st.title("⚙️ SpecForge")

    st.markdown("### Python Binary")

    st.code(PYTHON_BIN)

    st.divider()

    if st.session_state.process:

        if st.session_state.process.poll() is None:

            st.success("Pipeline Running")

        else:

            st.info("Pipeline Finished")

# ── Main UI ───────────────────────────────────────────────────────────────────
st.title("SpecForge Pipeline")

spec_path = st.text_input(
    "Spec File Path",
    value="specs/example_feature.yaml"
)

# ── Run Pipeline ──────────────────────────────────────────────────────────────
if st.button("▶ Run Pipeline"):

    st.session_state.terminal_output = ""

    process = subprocess.Popen(
        [PYTHON_BIN, "-m", "pipeline.main", spec_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdin=subprocess.PIPE,
        text=True,
        bufsize=1,
        cwd=str(PROJECT_ROOT),
    )

    st.session_state.process = process

    thread = threading.Thread(
        target=read_output,
        args=(process, st.session_state.output_queue),
        daemon=True,
    )

    thread.start()

# ── Read Queue ────────────────────────────────────────────────────────────────
while not st.session_state.output_queue.empty():

    line = st.session_state.output_queue.get_nowait()

    st.session_state.terminal_output += line

# ── Terminal Display ──────────────────────────────────────────────────────────
st.subheader("Integrated Terminal")

st_ace(
    value=st.session_state.terminal_output,
    language="sh",
    theme="monokai",
    readonly=True,
    height=600,
    wrap=True,
)

# ── Terminal Input ────────────────────────────────────────────────────────────
st.subheader("Terminal Input")

col1, col2 = st.columns([5, 1])

with col1:

    terminal_input = st.text_input(
        "Input",
        placeholder="Type y or n and press Send...",
        label_visibility="collapsed",
    )

with col2:

    send_clicked = st.button(
        "Send",
        use_container_width=True,
    )

# ── Send Input ────────────────────────────────────────────────────────────────
if send_clicked:

    process = st.session_state.process

    if process and process.stdin:

        process.stdin.write(terminal_input + "\n")

        process.stdin.flush()

        st.session_state.terminal_output += f"\n> {terminal_input}\n"

# ── Process Status ────────────────────────────────────────────────────────────
process = st.session_state.process

if process:

    if process.poll() is None:

        st.warning("Pipeline Running...")

        time.sleep(1)

        st.rerun()

    else:

        if process.returncode == 0:

            st.success("✅ Pipeline Completed")

        else:

            st.error(
                f"❌ Pipeline Failed (Exit Code {process.returncode})"
            )