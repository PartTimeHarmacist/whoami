import streamlit as st
from sqlalchemy import text
from collections.abc import Sequence


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

@st.cache_data(ttl=3600)
@st.fragment
def retrieve_qanda() -> Sequence:
    with conn.session as s:
        rtn = s.execute(
            text('SELECT question, answer FROM whoami_qa WHERE answer IS NOT NULL;')
        )
        s.commit()
    return rtn.fetchall()

@st.cache_data(ttl=3600)
@st.fragment
def retrieve_headers() -> Sequence:
    with conn.session as s:
        rtn = s.execute(
            text('SELECT * FROM whoami_headers;')
        )
        s.commit()
    return rtn.fetchall()

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
    example_projects_blurb = """
    I've always struggled with example or portfolio projects.  
    Most of the projects I work on for work are tucked away under Intellectual Property in some manner or another, 
    which usually means I can talk in broad strokes about the technologies and methodologies used, but actual source 
    code is something I can't readily share.
    
    Couple that with the fact that I don't like working on projects that seemingly have no purpose, and you get a fairly
    sparse professional portfolio that I can share elsewhere.  With that said, I've come up with a few projects that I
     actually get some use from and I can share here, which you'll find below.
     
    - [Warframe Drops Application](https://warframe.datadumplings.cloud) - [[source]]()
        - This is at the top of the list, because it's fully functional and useful to me and some friends.
        It's a simple data powered application, utilizing a data pipeline I set up in my Apache Airflow instance,
        that offers a way to quickly and easily track down what in-game items (Warframes, Items, etc) I want to locate,
        and how to best acquire them.
    - [Apache Airflow Deployment](https://airflow.datadumplings.cloud)
        - My own personal Apache Airflow instance.  It gets some use mainly because I know how Airflow works already,
        so I can further my knowledge with Kubernetes easily by tinkering with this deployment.  At the time of writing,
        it also serves to run the only personal ETL I have set up, which powers the above Streamlit application.
        [[source]](https://github.com/PartTimeHarmacist/datadumplings_dags)
        - The instance is visible, but restricted to try and avoid anything crazy.  If you'd like to view source code
        or more details than just the list of dags, you can sign in with github powered OAuth2 if you'd like.
    - [Apache Superset Deployment](https://superset.datadumplings.cloud)
        - This is a technology I'm just starting to learn, so there's not much to show yet.  I'll put some metrics up
        on the Warframe data when I get a chance; but for now it's a blank canvas, ready for some charts.
    - Teamcity Deployment
        - This is my personal CI/CD pipeline I use to manage my custom airflow image.  Whenever I want to make a change
        to the image, it automatically builds said image on one of three automatically provisioned workers, all hosted
        on my own hardware.  I could've probably gone with something more familiar, like Jenkins, Github Actions or 
        the like, but I use TeamCity personally and professionally, and I'm just a big fan of how their stuff works.
    - Private Gitea Deployment
        - If you take a look at my github, you'll notice that, aside from the _very professional_ username choice,
        there's not a lot of code out there.  I prefer to host my code on my own infrastructure, and I like having
        alternatives to big sites like github.  If anything, it's part of my ever-growing list of homelab deployed
        services.
    - Private Minio (S3) Deployment
        - This doesn't serve much use right now, but I do have functioning connections in Airflow to it.  I want to 
        learn how to use Minio as a base for Apache Iceberg and thus, Apache Spark; but that is going to take some time.
        My learning process tends to be a bit slower for big projects like these - I want to know how all the bits fit
        together and how they all work with each other.  Sure I could use a helm chart or something like that, but then
        how would I know how to fix it if something went wrong?
     """
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