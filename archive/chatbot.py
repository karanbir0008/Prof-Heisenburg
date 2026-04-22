# loading necessary modules and packages
from dotenv import load_dotenv #to get access of hidden api key
from langchain_groq import ChatGroq #to access llms on groq
import streamlit as st #for gui

# loading the api key
load_dotenv()

# page layout
st.set_page_config(
    page_title = "Chatbot",
    page_icon = "assets/icon.png",
    layout = "centered"
)

# main title of page
st.title("Karan's chatbot")

# to add a selectbox for different models of llm
selected_model = st.sidebar.selectbox(
    "choose model",
    ["llama-3.1-8b-instant","llama-3.3-70b-versatile","meta-llama/llama-guard-4-12b"
     ,"openai/gpt-oss-120b","openai/gpt-oss-20b"]
)

# initialize the chat history ---- > session state = {chat_history = [{},{}]}
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [{"role":"system","content":"your name is heisenburg .you are an expert AI assistant and science teacher. you have vast knowledge of science in every ascpect. always give answer as if teaching to a student of 3rd grade. do not forget to add daily life examples to understand better."}]

#showing the chat history---> this code part do not work for first chat given by user
for message in st.session_state["chat_history"]:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#input box
user_prompt = st.chat_input("ask chatbot......")

#after taking input from the user
if user_prompt:
    st.session_state["chat_history"].append({"role":"user","content":user_prompt})
    st.chat_message("user").markdown(user_prompt)
    #initializing llm remote control---> this code is placed here as if user do not enter any prompt then initialization of llm is useless
    if "llm" not in st.session_state:
        st.session_state["llm"] = ChatGroq(
            model=f"{selected_model}",
            temperature=0.3
        )

    llm = st.session_state["llm"]

    response = llm.invoke(st.session_state["chat_history"])
    #append response to chat_history
    st.session_state["chat_history"].append({"role":"assistant","content":response.content})
    st.chat_message("assistant").markdown(response.content)






