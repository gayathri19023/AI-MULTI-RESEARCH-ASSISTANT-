"""Streamlit entry point for the AI Multi-Agent Research Assistant."""
import streamlit as st
import pandas as pd
import plotly.express as px
from config import DEFAULT_DEMO_MODE, OPENAI_API_KEY
from database import init_db, get_session
from database.models import ResearchSession, Source
from services.document_parser import extract_document
from services.report_generator import make_docx, make_pdf
from utils.validators import validate_upload
from workflows import run_research
from pages.dashboard import render_dashboard

st.set_page_config(page_title="AI Multi-Agent Research Assistant", page_icon="🔬", layout="wide")
init_db()
SAMPLES=["Impact of Generative AI on Higher Education", "Artificial Intelligence in Healthcare", "Electric Vehicle Adoption in India", "Cybersecurity Challenges in Cloud Computing", "AI and Future Employment", "Machine Learning in Agriculture"]

def sidebar():
    st.sidebar.title("AI Research Assistant")
    page=st.sidebar.radio("Navigate", ["Dashboard", "New Research", "Document Analysis", "Research Results", "Research History", "Reports", "Settings"], key="nav_page")
    st.sidebar.caption("One Question. Multiple AI Agents. One Research Report.")
    return page

def show_results(state):
    if not state: st.info("Run research to see results."); return
    if state.get("demo"): st.warning("DEMO MODE - Results are based on sample research data, not live web research.")
    for warning in state.get("warnings", []): st.warning(warning)
    st.subheader(state["topic"]); st.write(state.get("summary", ""))
    metrics=st.columns(5); metrics[0].metric("Sources",len(state.get("sources",[]))); metrics[1].metric("Academic papers",sum(s.get("type")=="academic" for s in state.get("sources",[]))); metrics[2].metric("Documents",len(state.get("documents",[]))); metrics[3].metric("Claims checked",len(state.get("claims",[]))); metrics[4].metric("Potential gaps",len(state.get("gaps",[])))
    st.subheader("Agent activity")
    for name,result in state.get("agent_results",{}).items(): st.success(f"{name}: {result}")
    st.subheader("Key sources")
    for src in state.get("sources",[]):
        with st.expander(src.get("title","Untitled")):
            st.write(src.get("abstract") or src.get("snippet") or "No description available.")
            if src.get("url"): st.link_button("Open source",src["url"])
    if state.get("sources"):
        df=pd.DataFrame(state["sources"]); st.plotly_chart(px.bar(df, x="type", title="Sources collected by type"), use_container_width=True)
    st.subheader("Fact checking")
    st.dataframe(pd.DataFrame(state.get("claims",[])), use_container_width=True)
    st.subheader("Source comparison")
    st.dataframe(pd.DataFrame(state.get("comparison",[])), use_container_width=True)
    st.subheader("Potential research gaps")
    for gap in state.get("gaps",[]): st.warning(f"Potential gap: {gap['gap']}\n\nFuture research: {gap['future']}")
    st.subheader("Citations")
    for c in state.get("citations",[]): st.caption(c)
    st.download_button("Download PDF report", make_pdf(state), "research_report.pdf", "application/pdf")
    st.download_button("Download DOCX report", make_docx(state), "research_report.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")

page=sidebar()
if page=="Dashboard":
    render_dashboard()
elif page=="New Research":
    st.title("New Research")
    question=st.text_area("Research question", value=st.session_state.get("question", ""), placeholder="For example: What is the impact of generative AI on higher education?")
    st.caption("Sample topics: " + " | ".join(SAMPLES))
    col1,col2,col3=st.columns(3)
    demo=col1.toggle("Demo mode", value=DEFAULT_DEMO_MODE)
    style=col2.selectbox("Citation style",["APA","MLA","IEEE"])
    limit=col3.select_slider("Research depth",options=[3,5,8],value=5,format_func=lambda x:{3:"Basic",5:"Standard",8:"Deep"}[x])
    uploads=st.file_uploader("Optional supporting documents",type=["pdf","docx","txt"],accept_multiple_files=True)
    if st.button("Start Research",type="primary"):
        docs=[]
        for file in uploads:
            problem=validate_upload(file.name,file.size)
            if problem: st.error(f"{file.name}: {problem}"); continue
            try: docs.append(extract_document(file.name,file.getvalue()))
            except Exception as exc: st.error(f"{file.name}: {exc}")
        with st.spinner("Specialized agents are researching and analyzing evidence..."):
            try:
                state=run_research(question,demo=demo,source_limit=limit,citation_style=style,documents=docs); st.session_state["result"]=state; st.session_state["question"]=question
                from database.database import save_research
                st.session_state["session_id"]=save_research(state); st.success("Research complete. Open Research Results to review and download the report.")
            except Exception as exc: st.error(f"Research could not be completed: {exc}")
elif page=="Document Analysis":
    st.title("Document Analysis")
    files=st.file_uploader("Upload PDF, DOCX, or TXT documents",type=["pdf","docx","txt"],accept_multiple_files=True)
    for file in files or []:
        try:
            d=extract_document(file.name,file.getvalue()); st.success(f"{d['filename']} | {d['type']} | {d['pages']} pages"); st.write(d["text"][:1000])
        except Exception as exc: st.error(str(exc))
elif page=="Research Results": show_results(st.session_state.get("result"))
elif page=="Research History":
    st.title("Research History")
    with get_session() as db: rows=db.query(ResearchSession).order_by(ResearchSession.created_at.desc()).all()
    st.dataframe(pd.DataFrame([{"ID":r.id,"Topic":r.topic,"Question":r.question,"Status":r.status,"Date":r.created_at} for r in rows]),use_container_width=True)
elif page=="Reports":
    st.title("Reports"); st.write("Reports are generated with each research session. Open Research Results to download PDF or DOCX.")
elif page=="Settings":
    st.title("Settings"); st.write("API keys are read only from a local `.env` file and are never stored in the database.")
    st.code("OPENAI_API_KEY=\nSEARCH_API_KEY=\nDEMO_MODE=true",language="text")
    st.write("OpenAI key configured:" , "Yes" if OPENAI_API_KEY else "No - demo mode remains available.")
