import streamlit as st

# setting page config
st.set_page_config(
    page_title="Home",
    page_icon="icon.png",
    layout = "centered"
)
st.markdown(
    """
    <h1 style='text-align: center;'>👨‍🏫 Prof. Heisenburg</h1>
    <h4 style='text-align: center; color: grey;'>
    Your AI-powered science teacher for clear, syllabus-aligned learning
    </h4>
    """,
    unsafe_allow_html=True
)
st.video("science video.mp4",autoplay=True)


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🧠 AI Teacher")
    st.write("Ask questions, learn concepts, and understand science step by step.")

with col2:
    st.markdown("### 📘 NCERT Mode")
    st.write("Get syllabus-aligned, exam-safe answers grounded in NCERT textbooks.")

with col3:
    st.markdown("### 🎥 YouTube Agent")
    st.write("Discover high-quality video explanations for any topic.")

st.markdown("## 🔍 How It Works")

st.markdown("""
1. Ask a question  
2. Choose **General** or **NCERT-specific** mode  
3. Get clear explanations or verified textbook answers  
4. Explore videos for deeper understanding  
""")

st.markdown("## 🌍 Built for Curious Minds")

st.write(
    "This platform is designed to promote clear thinking, scientific reasoning, "
    "and responsible use of artificial intelligence in education."
)

st.success("👉 Start learning by selecting **AI Teacher** from the sidebar.")

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)
