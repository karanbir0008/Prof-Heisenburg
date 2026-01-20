import streamlit as st
from chatbot_utility import start_db, start_llm, collection_name, get_dict
from RAG_utility import retrieval_process, load_vector_db

# SYSTEM PROMPTS 
GENERAL_SYSTEM_PROMPT = """You are Prof. Heisenburg, an experienced science teacher.

Explain scientific concepts clearly to students of classes 8–10.
Use simple language, step-by-step reasoning, and real-life examples.
You may use general scientific knowledge beyond textbooks.
"""

NCERT_SYSTEM_PROMPT = """You are Prof. Heisenburg, an NCERT Science teacher.

Answer ONLY using information explicitly present in NCERT textbooks
for classes 8–10.

If the topic is not covered in NCERT, respond exactly:
"This topic is not covered in NCERT."
"""
# page layout
st.set_page_config(
    page_title = "Chatbot",
    page_icon = "icon.png",
    layout = "centered"
)


# main title of page
st.title("👨‍🏫Prof. Heisenburg ")

#-------------------------------------------------------------------------------------------------

#selecting the mode 
mode = st.sidebar.radio(
    "Mode of Professor",["General","NCERT Specific"],index=None
)

#model selection option
selected_model = st.sidebar.selectbox(
    "choose model",
    ["llama-3.1-8b-instant","llama-3.3-70b-versatile","meta-llama/llama-guard-4-12b"
     ,"openai/gpt-oss-120b","openai/gpt-oss-20b"]
)

 # model selection variable
if "selected_model" not in st.session_state:
    st.session_state["selected_model"] = selected_model
   
# llm initialization based on selected model
if ("llm" not in st.session_state or st.session_state["selected_model"]!=selected_model  ):
    st.session_state["selected_model"] = selected_model #make selected model in session_state equal to newly selected model
    st.session_state["llm"] = start_llm(st.session_state["selected_model"])

#---------------------------------------------------------------------------------------------------------

# db initialization per session
if "db" not in st.session_state:
    st.session_state["db"] = start_db()
#side bar to get previous chats
show_history_option = st.sidebar.radio("want chat history?",["YES","NO"],index = None)

if show_history_option=="YES":
    selected_chat_history = st.sidebar.selectbox(
        "select the chat you want to reload",
        [coll for coll in list(st.session_state["db"].list_collection_names())],index= None )

    if selected_chat_history:
        data = list(st.session_state["db"][selected_chat_history].find({},{"_id":0,"role":1,"content":1}).sort("timestamp",1))
        #so data here is of form list[{},{}]
        for chat in data:
            if chat["role"] == "system":
                continue
            with st.chat_message(chat["role"]):
                st.markdown(chat["content"])

#---------------------------------------------------------------------------------------------------------------------

#showing chat history
if "collection" in st.session_state:
    data = list(
        st.session_state["collection"]
        .find({}, {"_id": 0, "role": 1, "content": 1})
        .sort("timestamp", 1)
    )

    for msg in data:
        if msg["role"]=="system":
            continue
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# getting vector db for RAG 
if mode=="NCERT Specific":
    if "vector_db" not in st.session_state:
        st.session_state["vector_db"] = load_vector_db()

user_input = st.chat_input("ask Prof. .....")

#creation of collection for one session 
if user_input :
    if "collection" not in st.session_state:
        name = collection_name(user_input)   # sanitize first query
        st.session_state["collection"] = st.session_state["db"][name]

    # inserting system prompt to collection
    if "system_prompt_added" not in st.session_state:
        st.session_state["system_prompt_added"] = False

    if not st.session_state["system_prompt_added"]:
        system_prompt = "HERE COMES SYSTEM PROMPT"
        
        st.session_state["collection"].insert_one(get_dict("system",system_prompt,st.session_state["selected_model"]))
        st.session_state["system_prompt_added"]=True
    
    if mode == "NCERT Specific":
        st.session_state["collection"].update_one(
    {"role": "system"},
    {
        "$set": {
            "content": NCERT_SYSTEM_PROMPT
        }
    }
)
    if mode == "General":
        st.session_state["collection"].update_one(
    {"role": "system"},
    {
        "$set": {
            "content":GENERAL_SYSTEM_PROMPT
        }
    }
)



    #inserting the user_prompt to collection
    st.session_state["collection"].insert_one(get_dict("user",user_input,st.session_state["selected_model"]))
    with st.chat_message("user"):
        st.markdown(user_input)
    
    if mode == "General":
        #now givinng the chat to llm
        data = list(
            st.session_state["collection"]
            .find({}, {"_id": 0, "role": 1, "content": 1})
            .sort("timestamp", 1)
        )
                
        response = st.session_state["llm"].invoke(data)
        result = response.content

    elif mode == "NCERT Specific":
        response = retrieval_process(st.session_state["vector_db"],user_input,st.session_state["llm"])
        result_theory = response["result"]
        if response["source_documents"] :
            source = "\n\n📚 **Sources:**\n"
            for doc in response["source_documents"]:
                src = doc.metadata.get("source", "NCERT")
                page = doc.metadata.get("page", "?")
                source += f"- {src}, page {page}\n"
       
        result = result_theory+source

    # storing assistant result in db
    st.session_state["collection"].insert_one(get_dict("assistant",result,st.session_state["selected_model"]))
    with st.chat_message("assistant"):
        st.markdown(result)
        