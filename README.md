# Prof. Heisenburg

Prof. Heisenburg is a Streamlit-based study assistant built to make science learning feel clearer and more approachable. I wanted this project to do more than answer questions, so I combined a few different AI workflows in one place: a classroom-style teacher, an NCERT-grounded retrieval mode, a document analyzer, and a YouTube topic finder.

The idea behind the project is simple. Students often have to switch between textbooks, notes, videos, and search engines just to understand one topic well. This app tries to reduce that friction by giving them a single place where they can ask, read, analyze, and explore.

## Demo Video

A short working demonstration of the project is available here:  
https://youtu.be/Ky5na9nUf-4

## What the project does

- `AI Teacher` explains science concepts in a simple classroom-style way.
- `NCERT mode` uses retrieval over textbook content stored in a vector database.
- `Document Analyzer` extracts text from PDFs and images, then answers questions or summarizes the content.
- `YouTube Search` finds topic-relevant videos for revision and deeper understanding.
- `MongoDB storage` keeps chat and interaction history across the different tools.

## Why I built it

Many students do not get personal academic help outside the classroom. Even when good resources exist online, they are often scattered, overwhelming, or not aligned with the syllabus. I built Prof. Heisenburg as a practical educational companion that can explain concepts clearly, stay grounded in NCERT material when needed, and help students work through their own documents.

## How it works

The project is built as a multi-page Streamlit application.

- `Home.py` is the landing page.
- `pages/AI_Teacher.py` handles the main teaching experience.
- `pages/Document_Analyzer.py` supports OCR-based document analysis.
- `pages/YouTube_Search.py` finds educational videos related to a topic.
- `prof_heisenburg/` contains the utility modules used by the app logic.

Behind the interface, the project uses LangChain-based workflows for retrieval and LLM interaction, ChromaDB for vector storage, MongoDB for chat and document history, Tesseract OCR for extracting text from files, and the YouTube Data API for topic-based video search.

## Application Screenshots

### Home Page
![Home Page](assets/Home%20Page.png)

### AI Teacher
![AI Teacher](assets/AI%20teacher.png)

### Document Analyzer
![Document Analyzer](assets/Document%20Analyzer.png)

### YouTube Search
![YouTube Search](assets/Youtube%20video%20finder.png)

## Running it locally

1. Create and activate a virtual environment.
2. Install the dependencies with `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and add your keys and local paths.
4. Add `.streamlit/secrets.toml` with your `POPPLER_PATH`.
5. Start the app with `streamlit run Home.py`.

## Repository notes

Some parts of the project are intentionally not included in Git, such as secrets, local vector database files, NCERT source PDFs, and other machine-specific files. That keeps the repository cleaner and safer to share publicly.

This project is still evolving, but the current version reflects the direction I care about most: building educational tools that are practical, understandable, and genuinely helpful to students.
