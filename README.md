
# 🩺 MediScan AI

**Smart Medical Report Analyzer with AI Diagnosis, Diet, and Precaution Guidance**

---

## 📌 Overview

MediScan AI is an intelligent healthcare assistant that analyzes uploaded medical reports (text or image), performs disease predictions, recommends personalized diets, and provides precautionary measures — all powered by LLMs (Groq/OpenAI) and OCR.

---

## 🚀 Features

- 🧠 Final diagnosis prediction using multi-specialist AI agents
- 🥗 Diet recommendations tailored to medical context
- 🛡️ Precautionary measures to reduce health risk
- 🖼️ OCR for image-based reports using Tesseract
- 💬 Integrated chat assistant to ask follow-up health questions
- 📄 Downloadable PDF summary of chat
- 📦 Easily extensible with more specialists or LLMs

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Tesseract OCR
- LangChain + Groq LLM (`llama3-70b-8192`)
- dotenv
- FPDF (for PDF chat export)

---

## 📁 Folder Structure

MediScan-AI/
│
├── Utils/
│   └── Agent.py
│
├── .env
├── app.py                 # Streamlit UI
├── main.py                # Command-line interface for testing agents
├── requirements.txt
├── results/
│   └── final_diagnosis.txt  # Output from CLI
└── README.md

````

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/MediScan-AI.git
cd MediScan-AI
````

### 2. Create a Virtual Environment

```bash
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup `.env`

Create a `.env` file in the root folder and add your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the App

```bash
streamlit run app.py
```

---

## 🧪 Sample Use

1. Upload a `.txt` or `.jpg/.png` medical report.
2. Click **Analyze Report**.
3. View:

   * Final Diagnosis
   * Diet Recommendations
   * Precautionary Measures
4. Ask questions to the chatbot.
5. Download the chat as PDF.



## 💡 Future Improvements

* Voice input/output integration
* Integration with hospital EHRs
* Doctor login dashboard
* Medical PDF parsing

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.
