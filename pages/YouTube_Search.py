import streamlit as st
from youtube_utility import make_mongo_db_collection, get_dict, getting_ai_agent

st.set_page_config(
    page_title="YouTube search",
    page_icon="icon.png",
    layout="centered"
)

st.title("🔍 YouTube Video Searcher")

# load MongoDB collection
if "youtube_collection" not in st.session_state:
    st.session_state["youtube_collection"] = make_mongo_db_collection()

# user input
topic_name = st.text_input("Enter topic name...")

if st.button("Search"):
    if topic_name.strip() == "":
        st.warning("Please enter a topic")
    else:
        # save user query
        st.session_state["youtube_collection"].insert_one(
            get_dict(topic_name, "user")
        )

        agent = getting_ai_agent()
        response = agent.run_sync(
            topic_name
        ).output

        # save assistant response
        st.session_state["youtube_collection"].insert_one(
            get_dict([v.model_dump() for v in response], "assistant")
        )

        # display results
        for video in response:
            st.subheader(video.video_name)
            st.write(f"📌 Topic: {video.Topic}")
            st.markdown(f"[▶ Watch Video]({video.link})")
            st.divider()
