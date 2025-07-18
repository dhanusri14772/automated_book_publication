# 📘 Automated Book Publication 

This project implements an AI-powered system to automate the rewriting, reviewing, voice-interacting, and publishing of book chapters. It integrates LLMs, speech recognition, reinforcement-based feedback, and semantic search to deliver a human-in-the-loop authoring pipeline.

---

## 🎯 Objective

To create a seamless workflow that:

1. Scrapes chapter content from a URL.
2. Applies an AI-powered rewrite (spin).
3. Enables human-in-the-loop iteration via feedback and voice commands.
4. Implements a reward mechanism for learning from user ratings.
5. Supports semantic search over rewritten content.
6. Exports finalized content as a PDF.

---



## 🛠️ Tech Stack

| Component            | Tool / Library Used             |
|----------------------|---------------------------------|
| Web Scraping         | Playwright (Python)             |
| LLM Integration      | Falcon-7B-Instruct (via Ollama) |
| Voice Support        | pyttsx3, SpeechRecognition      |
| Vector Store         | ChromaDB                        |
| UI                   | Streamlit                       |
| PDF Export           | FPDF                            |
| Feedback System      | Custom logging (Reward loop)    |

---



## 🧱 Project Modules

### 1. `scraper.py` – Chapter Fetcher
- Scrapes text and screenshots from the source URL.
- Saves cleaned text into `data/Chapter_1.txt`.
- Screenshot saved in `screenshots/chapter_1.png`.

### 2. `writer_agent.py` – AI Rewriter
- Uses an LLM (Falcon-7B) to rewrite/spin the content.
- Generates new versions stored as `versions/Chapter_1/version_x.txt`.

### 3. `reviewer_agent.py` – AI Reviewer
- Evaluates the rewritten text.
- Suggests improvements based on coherence, grammar, etc.

### 4. `reward_system.py` – Feedback Logger
- Accepts user rating and decision (accepted/rejected).
- Stores reward signals for reinforcement learning loops.

### 5. `voice.py` – Voice Interaction
- Summarizes, accepts, or revises content using speech input.
- Converts speech to text and vice versa.

### 6. `index_with_chromadb.py` – Semantic Search
- Embeds rewritten content into ChromaDB.
- Enables retrieval based on natural language queries.

### 7. `app.py` – Streamlit Dashboard
- Central dashboard for interaction.
- Displays original and rewritten text.
- Integrates AI feedback, voice, semantic search, feedback form, and PDF download.

---

## How to Run

1. Setup Environment
```bash
git clone https://github.com/dhanusri14772/automated-book-publication
cd automated-book-publication
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**2.Run the Scraper**
```bash
python scraper.py
```
This command will:

> Fetch the chapter text from a predefined URL , 
> Save it to data/Chapter_1.txt then 
> Capture and store a screenshot in screenshots/Chapter_1.png

**Step 3: Launch the Streamlit dashboard**
```bash
streamlit run app.py
```
This will:

> Open a web-based interactive interface and 
> Guide you through rewriting, reviewing, voice commands, semantic search, feedback, and PDF download then
> Seamlessly connect all agents in the workflow




📂 Output Example


1. versions/Chapter_1/v1.txt – Rewritten text
2. versions/Chapter_1/v1.pdf – Downloadable version
3. screenshots/Chapter_1.png – Chapter screenshot




🔐 License


This repository is shared for educational and evaluation purposes only. All AI content and workflows were built independently. No part of this system is intended for commercial use or replication. 


