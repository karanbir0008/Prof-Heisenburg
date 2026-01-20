# Prof. Heisenburg – AI-Based Study Assistant

## Problem Statement

Most of the students in the secondary education level cannot get personal assistance in academics outside the class. Traditional modes of study rely mainly on textbooks, static notes, and limited availability of teachers, which makes concept clarification, revision, and understanding of documents pretty difficult.

There are online resources, but they are disjointed, very overwhelming, and many times unrelated to the official syllabus. Moreover, students also lack intelligent tools that can analyze academic documents, summarize content, and answer questions in a reliable and context-aware manner.

The challenge that has to be addressed in this project is designing an AI-based study assistant that can provide structured explanations, syllabus-restricted answers, and document analysis while maintaining clarity, correctness, and usability for students.

---

## Solution

For this purpose, I created **Prof. Heisenburg**, which is a study assistant based on artificial intelligence and incorporates large language models with information retrieval systems and database systems. The tool has been designed to be used as a smart educational companion instead of a universal chatter bot.

The system is equipped with:
- An interactive AI teacher for explanation of concepts  
- A syllabus-restricted answering facility for NCERT-based questions  
- A document analysis facility for answering questions and generating summaries from academic documents  

The chat history and uploaded documents are retained using database systems.

---

## System Overview

The application has been developed as a **multi-page web application** using the Streamlit platform, with the following well-defined modules:

1. AI Teacher (General Mode)  
2. NCERT-Specific Question Answering  
3. AI Assistant for Searching Educational Videos  
4. Document Analyzer for Academic Documents  

Each module has been designed with controlled execution flow and session management to ensure correct behavior during user interactions.

---

## Application Screenshots

### HOME PAGE
![Home Page](assets/Home%20Page.png)
### AI TEACHER
![AI Teacher](assets/AI%20teacher.png)
### DOCUMENT ANALYZER
![Document Analyzer](assets/Document%20Analyzer.png)
### YOUTUBE SEARCHER
![YouTube Search](assets/Youtube%20video%20finder.png)


## Methodology and Implementation

### AI Teacher Module (General Mode)

The AI Teacher allows students to submit questions related to science subjects. The general mode of the AI uses a large language model to provide precise explanations in simple and easy language. Chat history is recorded using MongoDB, ensuring continuity of conversations.

---

### NCERT-Specific Mode (RAG-Based)

For syllabus-based responses, NCERT textbooks are ingested in PDF format and processed by splitting them into smaller chunks, which are stored in a vector database.

When a question is asked, relevant content is retrieved from the NCERT textbooks and provided as input to the language model. This approach ensures that answers are strictly confined to NCERT content and are supported by retrieved references.

---

### Document Analyzer

The document analyzer allows users to upload academic documents in PDF or image formats.

Workflow:
- Uploaded files are stored using MongoDB GridFS  
- PDF files are converted into images using Poppler  
- Text is extracted using Tesseract OCR  
- Extracted text is passed to the language model to:
  - Answer questions related to the document, or  
  - Generate a concise summary  

The interaction is displayed in a chat-style interface showing both uploaded documents and AI responses.

---

### State and Execution Control

Special care is taken to manage Streamlit’s rerun behavior using session state. Database write operations and document processing steps are guarded to prevent duplicate inserts or repeated execution during reruns.

---

## Technologies Used

- Python  
- Streamlit  
- MongoDB and GridFS  
- LangChain  
- Chroma Vector Database  
- Groq Large Language Models  
- Tesseract OCR  
- Poppler (PDF to Image Conversion)  
- Pillow (PIL)  

---

## Demo Video

A short working demonstration of the project is available here:  
🔗 *(Add your demo video link here)*
