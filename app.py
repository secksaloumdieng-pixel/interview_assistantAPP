import streamlit as st
from dotenv import load_dotenv
from utils.cv_parser import extract_cv_text
from utils.JD_parser import parse_jd_text
from models.question_generator import generate_questions
from models.answer_evaluator import evaluate_answers
from models.resource_recommender import recommend_resources

load_dotenv()

st.set_page_config(
    page_title="Interview Assistant",
    page_icon="IA",
    layout="wide"
)

st.markdown("""
<style>
    :root {
        --bg: #f4f1ea;
        --card: #fbf8f2;
        --paper: #fffdf8;
        --ink: #1d1d1b;
        --muted: #6b665c;
        --line: #d8d0c2;
        --accent: #c66a3d;
        --accent-deep: #9f4d27;
        --accent-soft: #f3dfd2;
        --accent-hover: #a94f28;
        --panel: #f8f1e6;
        --panel-strong: #f2e6d6;
        --green-soft: #dfe9d8;
        --shadow: 0 18px 40px rgba(77, 56, 35, 0.08);
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(198,106,61,0.10), transparent 30%),
            radial-gradient(circle at top right, rgba(119,140,99,0.10), transparent 28%),
            linear-gradient(180deg, #f8f5ef 0%, #f1ede5 100%);
        color: var(--ink);
    }

    .block-container {
        padding-top: 2.2rem;
        padding-bottom: 3rem;
        max-width: 1280px;
    }

    .hero {
        background: linear-gradient(135deg, #2f241f 0%, #4c3529 55%, #7a4a33 100%);
        color: #fff8ef;
        border-radius: 28px;
        padding: 2.2rem 2.3rem;
        box-shadow: 0 22px 50px rgba(65, 41, 26, 0.18);
        position: relative;
        overflow: hidden;
        margin-bottom: 1.4rem;
    }

    .hero:before {
        content: "";
        position: absolute;
        width: 260px;
        height: 260px;
        right: -60px;
        top: -80px;
        border-radius: 999px;
        background: rgba(255,255,255,0.07);
    }

    .hero-kicker {
        display: inline-block;
        padding: 0.35rem 0.8rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.12);
        font-size: 0.8rem;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 0.9rem;
        font-weight: 700;
    }

    .hero-title {
        font-size: 3rem;
        line-height: 1.02;
        font-weight: 800;
        margin-bottom: 0.7rem;
        max-width: 760px;
    }

    .hero-subtitle {
        font-size: 1.02rem;
        line-height: 1.7;
        color: #f3e7db;
        max-width: 760px;
    }

    .surface {
        background: rgba(255,253,248,0.88);
        border: 1px solid rgba(216,208,194,0.85);
        border-radius: 22px;
        padding: 1.2rem 1.2rem 1rem 1.2rem;
        box-shadow: var(--shadow);
        backdrop-filter: blur(6px);
        margin-bottom: 1rem;
    }

    .section-title {
        font-size: 1.15rem;
        font-weight: 800;
        color: var(--ink);
        margin-bottom: 0.3rem;
    }

    .section-copy {
        color: var(--muted);
        font-size: 0.95rem;
        line-height: 1.55;
        margin-bottom: 1rem;
    }

    .score-card {
        background: linear-gradient(135deg, #fff8ef 0%, #f4e8d6 100%);
        border: 1px solid #ead9bf;
        border-radius: 22px;
        padding: 1.25rem;
        min-height: 170px;
        box-shadow: var(--shadow);
    }

    .score-label {
        color: #745f4d;
        font-size: 0.92rem;
        margin-bottom: 0.55rem;
    }

    .score-value {
        font-size: 3rem;
        font-weight: 800;
        color: #8f4826;
        line-height: 1;
        margin-bottom: 0.5rem;
    }

    .score-copy {
        color: #6e6258;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .mini-card {
        background: linear-gradient(180deg, #fcfaf6 0%, #f6f1e8 100%);
        border: 1px solid #e8dece;
        border-radius: 22px;
        padding: 1rem 1.1rem;
        min-height: 170px;
        box-shadow: var(--shadow);
    }

    .mini-title {
        color: #6e5a48;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        font-weight: 700;
        margin-bottom: 0.65rem;
    }

    .mini-value {
        color: #1d1d1b;
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.45rem;
    }

    .mini-copy {
        color: #6f675d;
        line-height: 1.55;
        font-size: 0.94rem;
    }

    .resource-card {
        background: linear-gradient(180deg, #fffdfa 0%, #f8f3eb 100%);
        border: 1px solid #e6dbc8;
        border-radius: 22px;
        padding: 1.05rem;
        box-shadow: var(--shadow);
        margin-bottom: 1rem;
        height: 100%;
    }

    .badge {
        display: inline-block;
        padding: 0.28rem 0.7rem;
        border-radius: 999px;
        background: var(--accent-soft);
        color: var(--accent-deep);
        font-size: 0.78rem;
        font-weight: 800;
        margin-bottom: 0.8rem;
    }

    .resource-title {
        font-size: 1.05rem;
        font-weight: 800;
        color: #2e261f;
        margin-bottom: 0.5rem;
    }

    .resource-meta {
        font-size: 0.92rem;
        color: #5e574f;
        margin-bottom: 0.38rem;
        line-height: 1.5;
    }

    .resource-desc {
        font-size: 0.94rem;
        color: #5f594f;
        line-height: 1.6;
        margin-top: 0.7rem;
    }

    div[data-testid="stButton"] > button {
        border-radius: 999px;
        border: none;
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-deep) 100%);
        color: white;
        font-weight: 700;
        min-height: 2.7rem;
        padding: 0.35rem 1rem;
        box-shadow: 0 10px 20px rgba(159, 77, 39, 0.18);
        transition: all 0.2s ease;
    }

    div[data-testid="stButton"] > button[kind="secondary"] {
        background: linear-gradient(135deg, #efe4d6 0%, #e5d5c1 100%);
        color: #5a4334;
        border: 1px solid #d5bea2;
        box-shadow: 0 10px 22px rgba(113, 87, 62, 0.12);
    }

    div[data-testid="stButton"] > button:disabled {
        background: linear-gradient(135deg, #c6beb3 0%, #aba195 100%) !important;
        color: #f8f4ef !important;
        box-shadow: none !important;
        transform: none !important;
        cursor: not-allowed !important;
        opacity: 1 !important;
    }

    div[data-testid="stButton"] > button:hover {
        background: linear-gradient(135deg, #d87745 0%, var(--accent-hover) 100%);
        color: #fffaf4;
        box-shadow: 0 18px 34px rgba(159, 77, 39, 0.32);
        transform: translateY(-1px);
    }

    div[data-testid="stButton"] > button[kind="secondary"]:hover {
        background: linear-gradient(135deg, #ead9c6 0%, #dcc4a7 100%);
        color: #4a3529;
        box-shadow: 0 14px 28px rgba(113, 87, 62, 0.18);
    }

    div[data-testid="stButton"] > button:active {
        background: linear-gradient(135deg, #b8afa3 0%, #9f9487 100%) !important;
        color: #fffaf4 !important;
        box-shadow: inset 0 3px 10px rgba(63, 51, 41, 0.22) !important;
        transform: translateY(1px) !important;
    }

    div[data-testid="stButton"] > button[kind="secondary"]:active {
        background: linear-gradient(135deg, #d8c1a7 0%, #ccb391 100%) !important;
        color: #3f2d24 !important;
        box-shadow: inset 0 3px 10px rgba(91, 67, 49, 0.18) !important;
    }

    div[data-testid="stButton"] > button p {
        font-size: 0.96rem;
        letter-spacing: 0.01em;
    }

    div[data-testid="stButton"] > button:focus,
    div[data-testid="stButton"] > button:focus-visible {
        outline: none !important;
        border: 2px solid #ffd7bf !important;
        box-shadow: 0 0 0 0.24rem rgba(198,106,61,0.30) !important;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f7f2e8 0%, #efe8dc 100%);
        border-right: 1px solid #ddd0bc;
    }

    .sidebar-box {
        background: rgba(255,255,255,0.5);
        border: 1px solid #ddd0bc;
        border-radius: 18px;
        padding: 1rem;
        margin-top: 0.8rem;
    }

    .sidebar-spacer {
        height: 1.2rem;
    }

    .question-label {
        font-size: 1rem;
        font-weight: 800;
        color: #2a231d;
        margin-bottom: 0.3rem;
    }

    .status-row {
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
        margin: 0.35rem 0 1rem 0;
    }

    .status-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        padding: 0.55rem 0.9rem;
        border-radius: 999px;
        background: rgba(223, 233, 216, 0.9);
        border: 1px solid #bfd0b4;
        color: #36523a;
        font-weight: 700;
        font-size: 0.92rem;
        box-shadow: 0 8px 18px rgba(91, 120, 80, 0.08);
    }

    div[data-testid="stFileUploaderDropzone"] {
        background: linear-gradient(180deg, var(--panel) 0%, var(--panel-strong) 100%);
        border: 1.5px dashed #d1b796;
        border-radius: 18px;
    }

    div[data-testid="stFileUploaderDropzone"]:hover {
        background: linear-gradient(180deg, #f6eadb 0%, #eedcc7 100%);
        border-color: #c66a3d;
    }

    div[data-testid="stFileUploaderDropzone"] * {
        color: #493a2f !important;
    }

    div[data-testid="stTextArea"] {
        border-radius: 20px !important;
    }

    div[data-baseweb="textarea"] {
        border-radius: 20px !important;
        overflow: hidden !important;
        background: transparent !important;
    }

    div[data-baseweb="textarea"] > div {
        border: none !important;
        background: transparent !important;
    }

    div[data-testid="stTextArea"] textarea {
        background: linear-gradient(180deg, var(--panel) 0%, #fbf4ea 100%) !important;
        border: 1.5px solid #d8c4a8 !important;
        color: #2d241f !important;
        border-radius: 20px !important;
        padding: 1rem !important;
        box-shadow: none !important;
        outline: none !important;
        resize: vertical !important;
    }

    div[data-testid="stTextArea"] textarea:hover {
        border-color: #cda67d !important;
    }

    div[data-testid="stTextArea"] textarea:focus,
    div[data-testid="stTextArea"] textarea:focus-visible {
        border: 1.5px solid #c66a3d !important;
        box-shadow: 0 0 0 0.24rem rgba(198,106,61,0.16) !important;
        outline: none !important;
    }

    label, .stTextArea label, .stFileUploader label {
        color: #3a2f28 !important;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

if "questions" not in st.session_state:
    st.session_state.questions = []

if "evaluation" not in st.session_state:
    st.session_state.evaluation = None

if "is_generating" not in st.session_state:
    st.session_state.is_generating = False

if "is_evaluating" not in st.session_state:
    st.session_state.is_evaluating = False

if "questions_generated" not in st.session_state:
    st.session_state.questions_generated = False

st.sidebar.markdown("## Interview Assistant")
st.sidebar.markdown("A focused workflow for interview preparation.")

st.sidebar.markdown("""
<div class="sidebar-box">
<strong>Flow</strong><br><br>
1. Upload CV<br>
2. Paste job description<br>
3. Generate questions<br>
4. Write answers<br>
5. Evaluate performance<br>
6. Review resources
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-spacer"></div>', unsafe_allow_html=True)

if st.sidebar.button("Reset Session", use_container_width=True, type="secondary"):
    st.session_state.questions = []
    st.session_state.evaluation = None
    st.session_state.questions_generated = False
    for key in list(st.session_state.keys()):
        if key.startswith("answer_"):
            del st.session_state[key]
    st.rerun()

st.sidebar.markdown("""
<div class="sidebar-box">
<strong>Testing Tip</strong><br><br>
Keep the question count low while iterating on the experience.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-kicker">AI Interview Prep</div>
    <div class="hero-title">Prepare like the interview already matters.</div>
    <div class="hero-subtitle">
        Turn a CV and job description into a focused mock interview, get structured scoring,
        and receive next-step learning recommendations from both a local library and AI.
    </div>
</div>
""", unsafe_allow_html=True)

top_left, top_right = st.columns([1, 1])

with top_left:
    st.markdown('<div class="surface">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Candidate Profile</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-copy">Upload a PDF CV to extract the professional context used for question generation.</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload your CV (PDF)", type=["pdf"])
    st.markdown("</div>", unsafe_allow_html=True)

with top_right:
    st.markdown('<div class="surface">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Role Brief</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-copy">Paste the target job description so the interview can be shaped around the role.</div>', unsafe_allow_html=True)
    jd_input = st.text_area("Paste the Job Description", height=220)
    st.markdown("</div>", unsafe_allow_html=True)

cv_text = ""
jd_text = ""
status_chips = []

if uploaded_file is not None:
    cv_text = extract_cv_text(uploaded_file)
    status_chips.append("CV parsed")

if jd_input:
    jd_text = parse_jd_text(jd_input)
    status_chips.append("Job description ready")

if status_chips:
    chips_html = "".join(
        f'<div class="status-chip">{chip}</div>'
        for chip in status_chips
    )
    st.markdown(f'<div class="status-row">{chips_html}</div>', unsafe_allow_html=True)

st.markdown('<div class="surface">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Interview Setup</div>', unsafe_allow_html=True)
st.markdown('<div class="section-copy">Generate a tailored mock interview once both the CV and the job description are ready.</div>', unsafe_allow_html=True)

if cv_text and jd_text:
    generate_button = st.empty()
    if st.session_state.is_generating:
        generate_label = "Generating..."
    elif st.session_state.questions_generated:
        generate_label = "Questions Generated"
    else:
        generate_label = "Generate Questions"

    generate_clicked = generate_button.button(
        generate_label,
        use_container_width=True,
        disabled=st.session_state.is_generating or st.session_state.questions_generated
    )
    if generate_clicked:
        st.session_state.is_generating = True
        generate_button.button("Generating...", use_container_width=True, disabled=True)
        try:
            with st.spinner("Generating questions..."):
                st.session_state.questions = generate_questions(cv_text, jd_text)
                st.session_state.evaluation = None
                st.session_state.questions_generated = True
        except Exception as e:
            st.error(f"Error while generating questions: {e}")
        finally:
            st.session_state.is_generating = False
else:
    st.info("Upload a CV and paste a job description to unlock question generation.")

st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.questions:
    st.markdown('<div class="surface">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Interview Questions</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-copy">Write your answers directly below each question, then run the evaluation.</div>', unsafe_allow_html=True)

    answers = []
    for i, question in enumerate(st.session_state.questions, start=1):
        st.markdown(f'<div class="question-label">Question {i}</div>', unsafe_allow_html=True)
        st.write(question)
        answer = st.text_area(
            f"Your answer to question {i}",
            key=f"answer_{i}",
            height=150,
            label_visibility="collapsed"
        )
        answers.append(answer)

    evaluate_button = st.empty()
    evaluate_label = "Evaluating..." if st.session_state.is_evaluating else "Evaluate Answers"
    evaluate_clicked = evaluate_button.button(
        evaluate_label,
        use_container_width=True,
        disabled=st.session_state.is_evaluating
    )
    if evaluate_clicked:
        if not any(answer.strip() for answer in answers):
            st.warning("Please write at least one answer before evaluation.")
        else:
            st.session_state.is_evaluating = True
            evaluate_button.button("Evaluating...", use_container_width=True, disabled=True)
            try:
                qa_list = []
                for question, answer in zip(st.session_state.questions, answers):
                    qa_list.append({
                        "question": question,
                        "answer": answer
                    })

                with st.spinner("Evaluating answers..."):
                    st.session_state.evaluation = evaluate_answers(qa_list)
            except Exception as e:
                st.error(f"Error while evaluating answers: {e}")
            finally:
                st.session_state.is_evaluating = False

    st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.evaluation:
    evaluation = st.session_state.evaluation
    answer_count = len(evaluation.get("answers", []))
    low_scores = sum(1 for item in evaluation.get("answers", []) if item.get("score", 0) < 75)

    st.markdown('<div class="surface">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Performance Snapshot</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-copy">A quick dashboard view of your current interview performance.</div>', unsafe_allow_html=True)

    dash1, dash2, dash3 = st.columns([1.2, 1, 1])

    with dash1:
        st.markdown(f"""
        <div class="score-card">
            <div class="score-label">Overall Score</div>
            <div class="score-value">{evaluation["overall_score"]}</div>
            <div class="score-copy">
                Use this as a directional benchmark, then review the detailed feedback below to improve your next attempt.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with dash2:
        st.markdown(f"""
        <div class="mini-card">
            <div class="mini-title">Answers Reviewed</div>
            <div class="mini-value">{answer_count}</div>
            <div class="mini-copy">
                Total responses included in this evaluation cycle.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with dash3:
        st.markdown(f"""
        <div class="mini-card">
            <div class="mini-title">Needs Work</div>
            <div class="mini-value">{low_scores}</div>
            <div class="mini-copy">
                Answers that likely need another pass or more specific examples.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Detailed Feedback</div>', unsafe_allow_html=True)

    for item in evaluation["answers"]:
        with st.expander(item["q"]):
            st.write(f"**Answer:** {item['a']}")
            st.write(f"**Score:** {item['score']}")
            st.write(f"**Feedback:** {item['feedback']}")

    st.markdown("</div>", unsafe_allow_html=True)

    try:
        with st.spinner("Finding recommended resources..."):
            resources = recommend_resources(evaluation)

        st.markdown('<div class="surface">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Recommended Resources</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-copy">A mix of trusted local references and AI-generated suggestions based on weak areas.</div>', unsafe_allow_html=True)

        if resources:
            for i in range(0, len(resources), 2):
                cols = st.columns(2)
                batch = resources[i:i + 2]

                for col, resource in zip(cols, batch):
                    with col:
                        source_label = "Local Library" if resource["source"] == "local_library" else "AI Suggestion"
                        st.markdown(f"""
                        <div class="resource-card">
                            <div class="badge">{source_label}</div>
                            <div class="resource-title">{resource['title']}</div>
                            <div class="resource-meta"><strong>Topic:</strong> {resource['topic']}</div>
                            <div class="resource-meta"><strong>Link:</strong> <a href="{resource['url']}" target="_blank">Open resource</a></div>
                            <div class="resource-desc">{resource['description']}</div>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("No resources were returned for this evaluation.")

        st.markdown("</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error while getting resources: {e}")
