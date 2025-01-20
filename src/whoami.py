import streamlit as st
from sqlalchemy import text
from collections.abc import Sequence
from pathlib import Path


st.set_page_config(
    page_title="whoami",
    initial_sidebar_state="collapsed"
)

conn = st.connection("postgresql", type="sql")

@st.fragment
def submit_feedback() -> None:
    feedback = st.chat_input("Put your Question or Feedback here, and press enter to submit")
    feedback_status = st.empty()
    if feedback:
        feedback_status = feedback_status.progress(0, text="Sending feedback...")
        with conn.session as s:
            feedback_status.progress(50, "Sending feedback...")
            s.execute(
                text('INSERT INTO whoami_qa (question) VALUES (:question);'),
                params={"question": feedback}
            )
            s.commit()
        feedback_status.progress(100, "Feedback sent!")
    return

@st.cache_data(ttl=300)
@st.fragment
def retrieve_qanda() -> Sequence:
    with conn.session as s:
        rtn = s.execute(
            text('SELECT question, answer FROM whoami_qa WHERE answer IS NOT NULL;')
        )
        s.commit()
    return rtn.fetchall()

@st.cache_data(ttl=300)
@st.fragment
def retrieve_headers() -> Sequence:
    with conn.session as s:
        rtn = s.execute(
            text('SELECT * FROM whoami_headers;')
        )
        s.commit()
    return rtn.fetchall()

@st.cache_data(ttl=300)
@st.fragment
def retrieve_doc_file(file_path: Path) -> str:
    return file_path.read_text("utf-8")

headers = {h: t.replace(r"\n", "\n\n") for i, d, h, t in retrieve_headers()}

st.write("### Welcome!")
greeting = headers["greeting"]

st.write(greeting)

st.write("---")

tab1, tab2, tab3 = st.tabs(["About Me", "Examples", "Q&A"])

with tab1:
    st.header("About Me")
    about_me = headers["about_me"]
    st.write(about_me)

with tab2:
    st.header("Example Projects")
    example_projects_blurb = retrieve_doc_file(Path("/home/appuser/app/repo/src/docs/example_projects.md"))
    st.markdown(example_projects_blurb)
    st.write("---")

with tab3:
    st.header("Questions and Answers")

    q_and_a = retrieve_qanda()

    exp = True
    for qa in q_and_a:
        q, a = qa
        with st.expander(q, expanded=exp):
            st.write(a.replace(r"\n", "\n\n"))
        exp = False

    with st.expander("Where can I leave my own question?"):
        st.write("""Right here!  Now, this isn't a chat-gpt powered bot or anything, so you won't receive an
        instant response.  Submit feedback or ask a question here though, and I will see it and do my best to
        respond in a timely manner!""")

        submit_feedback()