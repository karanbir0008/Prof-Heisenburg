import streamlit as st
from analyzer_utility import extract_text_of_file,create_collection,store_user,store_assistant,get_file_from_gridfs,db
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

POPPLER_PATH = st.secrets["POPPLER_PATH"]

# page layout
st.set_page_config(
    page_title = "Test Checker",
    page_icon = "icon.png",
    layout = "centered"
)


# main title of page
st.title("📝✔️ Document Analyzer")

if st.sidebar.button("🔄 NEW UPLOAD"):
    st.session_state.pop("mode_radio",None)
    st.session_state.pop("history_radio",None)
    st.session_state.pop("uploaded_option",None)
    st.rerun()



mode = st.sidebar.radio(
    "Select Mode", ["Answer Questions","Summerize"],index=None,key = "mode_radio"
)



document_hostory = st.sidebar.radio("Do you want to see history?",["Yes","No"],index = None,key = "history_radio")
if document_hostory == "Yes":
    collection = create_collection()
    history = list(
        collection.find({},{"_id":0}).sort("timestamp",1)

    )
    for msg in history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                file_bytes, content_type, filename = get_file_from_gridfs(
                    db,
                    msg["file_id"]
                )

                st.markdown(f"📄 **Uploaded file:** `{filename}`")

                if content_type == "application/pdf":
                    st.download_button(
                        "View PDF",
                        data=file_bytes,
                        file_name=filename,
                        mime="application/pdf",
                        key=f"pdf_{msg['file_id']}"
                    )

                elif content_type.startswith("image/"):
                    st.image(file_bytes, caption=filename)

        elif msg["role"] == "assistant":
            with st.chat_message("assistant"):
                st.markdown(msg["content"])


else:
    #loading llm and selected model from AI Teacher 
    if "analyzer_llm" not in st.session_state:
        st.session_state["analyzer_llm"] = ChatGroq(model = "openai/gpt-oss-120b",temperature=0.2)
    llm = st.session_state["analyzer_llm"]



    # only specific types of files are allowed

    uploaded_file = st.file_uploader("upload file (pdf,png,jpeg)",type = ["pdf", "png", "jpeg"],key="uploaded_option")
    if uploaded_file:
        st.markdown(f"**Detected type : {uploaded_file.type}**")
        if uploaded_file.type not in [
            "application/pdf",
            "image/png",
            "image/jpeg"
            ]:
            st.error("Unsupported file type")
            st.stop()
        else:
            st.success("File accepted")

    #initialization of collection
    if "document_collection" not in st.session_state:
        st.session_state["document_collection"] = create_collection()

    if uploaded_file:
        
        file_bytes = uploaded_file.read()
        content_type = uploaded_file.type
        filename = uploaded_file.name
            #now we need to insert user uploaded document to mongodb collection document
        if "inserted_document" not in st.session_state or st.session_state["inserted_document"]!=filename:
            st.session_state["inserted_document"] = filename


            st.session_state["document_collection"].insert_one(store_user(file_bytes,content_type,filename))

            #now we need to convert  document into text and pass to llm
        text = extract_text_of_file(file_bytes,content_type)
        if mode:
            if mode == "Answer Questions":
                prompt = f"""
            You are an intelligent document assistant.

            Below is the content of a document.
            Read it carefully and answer the questions found in the document
            in a clear, detailed, and easy-to-understand manner.

            DOCUMENT CONTENT:
            {text}
            """
            elif mode == "Summerize":
                prompt = f"""
            You are a document analysis assistant.

            Summarize the following document in a clear, simple, and concise manner.
            Use easy language.
            Focus only on the main ideas and important points.
            Avoid unnecessary details.

            DOCUMENT CONTENT:
            {text}
            """
            with st.spinner("wait for a moment"):  
                response = llm.invoke(prompt)
                answer = response.content
                # now we need to store the response of assistant 
                st.session_state["document_collection"].insert_one(store_assistant(answer))
                st.markdown(response.content)
        else:
            st.warning("Please select a valid mode")
    else:
        st.warning("Please upload a text document")