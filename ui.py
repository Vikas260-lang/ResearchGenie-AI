import streamlit as st
from app import run_pipeline
import networkx as nx
import matplotlib.pyplot as plt

# ---------------- CACHE ----------------
@st.cache_data(show_spinner=False)
def cached_pipeline(task, use_sc):
    return run_pipeline(task, use_sc)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ResearchGenie AI",
    layout="wide",
    page_icon="🤖"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

/* ---------------- MAIN APP ---------------- */
.stApp {
    background: linear-gradient(
        135deg,
        #020617 0%,
        #0f172a 40%,
        #111827 100%
    );
    color: white;
}

/* ---------------- HEADER ---------------- */
.main-title {
    text-align:center;
    font-size:4rem;
    font-weight:900;
    background: linear-gradient(90deg,#38bdf8,#818cf8,#c084fc);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    margin-bottom:0;
}

.sub-title {
    text-align:center;
    color:#cbd5e1;
    font-size:1.2rem;
    margin-bottom:2rem;
}

/* ---------------- HERO SECTION ---------------- */
.hero-box {
    padding:35px;
    border-radius:28px;
    background: linear-gradient(
    135deg,
    rgba(37,99,235,0.25),
    rgba(124,58,237,0.25),
    rgba(6,182,212,0.18)
    );
    border:1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(18px);
    margin-bottom:25px;
    box-shadow:0 0 40px rgba(99,102,241,0.25);
}

/* ---------------- METRIC CARDS ---------------- */
.metric-card {
    background: rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:22px;
    padding:22px;
    text-align:center;
    backdrop-filter: blur(14px);
    box-shadow:0 0 25px rgba(59,130,246,0.18);
    transition:0.3s;
}

.metric-card:hover {
    transform: translateY(-6px);
    box-shadow:0 0 35px rgba(99,102,241,0.4);
}

/* ---------------- BUTTON ---------------- */
.stButton button {
    background: linear-gradient(90deg,#2563eb,#7c3aed);
    color:white;
    border:none;
    border-radius:14px;
    font-size:1rem;
    font-weight:700;
    padding:0.8rem 2rem;
    width:100%;
    box-shadow:0 0 20px rgba(99,102,241,0.35);
    transition:0.3s;
}

.stButton button:hover {
    transform: scale(1.03);
    box-shadow:0 0 30px rgba(59,130,246,0.6);
}

/* ---------------- TABS ---------------- */
.stTabs [data-baseweb="tab-list"] {
    gap:18px;
    background: rgba(255,255,255,0.04);
    border-radius:18px;
    padding:10px;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.05);
    border-radius:14px;
    color:white;
    font-weight:700;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg,#2563eb,#7c3aed);
}

/* ---------------- FINAL ANSWER ---------------- */
.answer-box {
    background: linear-gradient(145deg,#052e16,#064e3b);
    border:1px solid rgba(34,197,94,0.3);
    border-radius:22px;
    padding:24px;
    color:#dcfce7;
    line-height:1.8;
    font-size:1.05rem;
    box-shadow:0 0 25px rgba(34,197,94,0.15);
}

/* ---------------- PRO CON ---------------- */
.pro-card {
    background: rgba(34,197,94,0.12);
    border-left:5px solid #22c55e;
    padding:18px;
    border-radius:14px;
    margin-bottom:12px;
}

.con-card {
    background: rgba(239,68,68,0.12);
    border-left:5px solid #ef4444;
    padding:18px;
    border-radius:14px;
    margin-bottom:12px;
}

/* ---------------- SIDEBAR ---------------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#020617,#111827);
}

/* ---------------- INPUT ---------------- */
textarea, input {
    border-radius:16px !important;
    background:#0f172a !important;
    color:white !important;
}

/* ---------------- SUCCESS ---------------- */
.stSuccess {
    border-radius:18px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(
    '<div class="main-title">🧠 ResearchGenie AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Agentic AI Research Assistant for Structured Reasoning, Debate & Explainability</div>',
    unsafe_allow_html=True
)

# ---------------- HERO SECTION ----------------
st.markdown("""
<div class="hero-box">

<h1 style="
font-size:3rem;
font-weight:900;
margin-bottom:10px;
">
🚀 Next-Generation Agentic AI Research Platform
</h1>

<p style="
font-size:1.2rem;
color:#cbd5e1;
line-height:1.8;
">
Multi-Agent Reasoning • Explainable AI • Debate Intelligence • Trust Evaluation • Knowledge Graphs
</p>

</div>
""", unsafe_allow_html=True)

st.divider()

# ---------------- INPUT ----------------
with st.container():

    st.markdown("### 🔍 Enter your research query")

    task = st.text_input(
        "Enter your research query",
        placeholder="e.g., How do LLMs work?",
        label_visibility="collapsed"
    )

    level = st.select_slider(
        "Explanation Level",
        options=["Simple", "Standard", "Detailed"],
        value="Standard"
    )

    st.caption("Simple = short summary | Standard = balanced | Detailed = full reasoning")

    use_sc = st.checkbox("Enable Self-Consistency")

    run = st.button("🚀 Run Analysis")

# ---------------- SIMPLIFY ----------------
def simplify(text, lvl, claims=None, debates=None, verdicts=None):

    if lvl == "Simple":

        short = text.split("Key Insights:")[0]

        return "🔹 **Simple Explanation:**\n\n" + short[:200] + "..."

    elif lvl == "Standard":

        return text

    else:

        detailed = text + "\n\n---\n### 🔍 Detailed Reasoning:\n"

        if claims and debates and verdicts:

            for i in range(len(claims)):

                c = claims[i]
                d = debates[i] if i < len(debates) else {}
                v = verdicts[i] if i < len(verdicts) else {}

                detailed += f"\n**Claim {i+1}:** {c.get('statement','')}\n"

                for arg in d.get("arguments", []):

                    detailed += f"- {arg.get('side','').upper()}: {arg.get('reasoning','')}\n"

                detailed += f"➡ Verdict: {v.get('verdict','')} ({v.get('confidence_score',50)}%)\n"

        return detailed

# ---------------- MAIN ----------------
if run and task.strip():

    progress = st.progress(0)
    status = st.empty()

    try:

        for i in range(100):

            progress.progress(i + 1)

            if i < 30:
                status.info("🧠 Initializing AI Agents...")

            elif i < 60:
                status.info("⚖️ Running Multi-Agent Debate...")

            elif i < 85:
                status.info("🌐 Building Knowledge Graph...")

            else:
                status.info("🔒 Computing Trust & Reliability...")

        result = cached_pipeline(task, use_sc)

        progress.empty()
        status.empty()

    except Exception as e:

        st.error(f"❌ Error: {str(e)}")
        st.stop()

    st.success("✅ Analysis Complete")

    st.divider()

    # ---------------- SAFE DATA EXTRACTION ----------------
    debate_data = result.get("debate", {})
    debates = debate_data.get("debates", [])
    verdicts = debate_data.get("verdicts", [])
    claims = result.get("claims", [])

    trust_obj = result.get("trust_score", None)

    if isinstance(trust_obj, dict):
        trust_value = trust_obj.get("trust_score", 0)
    else:
        trust_value = getattr(trust_obj, "trust_score", 0)

    num_claims = len(claims)

    avg_conf = int(
        sum([v.get("confidence_score", 50) for v in verdicts]) /
        max(len(verdicts), 1)
    )

    agreement = result.get("agreement_score", 1.0)

    plag = result.get("plagiarism", 0)

    # ---------------- METRICS ----------------
    st.markdown("## 📊 Overview")

    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        ("📌 Claims", num_claims),
        ("📊 Confidence", f"{avg_conf}%"),
        ("🔒 Trust Score", f"{round(trust_value * 100)}%"),
        ("⚖️ Agreement", f"{round(agreement * 100)}%")
    ]

    for col, metric in zip([col1, col2, col3, col4], metrics):

        with col:
            st.markdown(f'''
            <div class="metric-card">
                <h4>{metric[0]}</h4>
                <h1>{metric[1]}</h1>
            </div>
            ''', unsafe_allow_html=True)

    st.divider()

    # ---------------- TABS ----------------
    tab1, tab2, tab3, tab4 = st.tabs([
        "🧠 Final Answer",
        "⚖️ Perspectives",
        "🧩 Knowledge Graph",
        "📊 Analysis"
    ])

    # ---------------- TAB 1 ----------------
    with tab1:

        st.markdown("## 🧠 Final Answer")

        st.markdown(
            f'''
            <div class="answer-box">
            {simplify(
                result.get("answer", "No answer"),
                level,
                result.get("claims"),
                result.get("debates"),
                result.get("verdicts")
            ).replace(chr(10), "<br>")}
            </div>
            ''',
            unsafe_allow_html=True
        )

    # ---------------- TAB 2 ----------------
    with tab2:

        st.markdown("### ⚖️ Multi-Perspective Reasoning")

        if debates:

            for debate in debates:

                st.markdown(f"#### 🧾 Claim: {debate.get('claim_id', '')}")

                for arg in debate.get("arguments", []):

                    if arg.get("side") == "pro":

                        st.markdown(
                            f'<div class="pro-card">✅ <b>PRO:</b> {arg.get("reasoning","")}</div>',
                            unsafe_allow_html=True
                        )

                    else:

                        st.markdown(
                            f'<div class="con-card">❌ <b>CON:</b> {arg.get("reasoning","")}</div>',
                            unsafe_allow_html=True
                        )

        else:
            st.warning("No debate data available")

    # ---------------- TAB 3 ----------------
    with tab3:

        st.markdown("### 🧩 Explainable Knowledge Graph")

        graph_data = result.get("graph", {})

        if graph_data and len(graph_data.get("nodes", [])) > 0:

            G = nx.DiGraph()

            for edge in graph_data["edges"]:

                source = str(edge.get("source", ""))[:30]
                target = str(edge.get("target", ""))[:30]

                G.add_edge(source, target)

            if len(G.nodes) > 0:

                pos = nx.spring_layout(G, k=2)

                fig, ax = plt.subplots(figsize=(12, 8))

                fig.patch.set_facecolor('#0f172a')
                ax.set_facecolor('#0f172a')

                nx.draw_networkx_nodes(
                    G,
                    pos,
                    node_color="#7c3aed",
                    node_size=4200,
                    alpha=0.95
                )

                nx.draw_networkx_edges(
                    G,
                    pos,
                    edge_color="#38bdf8",
                    width=3,
                    arrows=True,
                    arrowsize=22
                )

                nx.draw_networkx_labels(
                    G,
                    pos,
                    font_color="white",
                    font_size=10,
                    font_weight="bold"
                )

                plt.axis('off')

                st.pyplot(fig)

            else:
                st.warning("Graph is empty")

        else:
            st.warning("No graph data available")

    # ---------------- TAB 4 ----------------
    with tab4:

        st.markdown("### 📊 Confidence & Reliability")

        st.subheader("📊 Confidence Analysis")
        st.json(result.get("uncertainty", {}))

        st.subheader("🔒 Trust Score")

        if trust_obj:

            try:

                if isinstance(trust_obj, dict):

                    st.write(f"Score: {round(trust_obj.get('trust_score', 0) * 100)}%")
                    st.write(f"Confidence: {trust_obj.get('confidence_level', 'N/A')}")
                    st.write(f"Explanation: {trust_obj.get('explanation', '')}")

                else:

                    st.write(f"Score: {round(trust_obj.trust_score * 100)}%")
                    st.write(f"Confidence: {trust_obj.confidence_level}")
                    st.write(f"Explanation: {trust_obj.explanation}")

            except:
                st.write("Trust score format error")

        st.subheader("📄 Plagiarism Check")

        if isinstance(plag, float):

            st.write(f"Plagiarism Score: {round(plag * 100)}%")

        else:

            st.write(plag or "Not available")

    # ---------------- DEBUG ----------------
    with st.expander("🔍 Debug Data"):
        st.json(result)