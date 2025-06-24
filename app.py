
from fpdf import FPDF
import os
import io
import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd
from dotenv import load_dotenv
from fpdf import FPDF
from Utils.Agent import Cardiologist, Psychologist, Pulmonologist, MultidisciplinaryTeam, Dietician, PreventiveSpecialist
from Utils.Chatbot import get_bot_response
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
load_dotenv()

st.set_page_config(page_title="MediScan AI", layout="wide")

st.title("🩺 MediScan AI")
st.subheader("Smart Medical Report Analyzer")

# Function to extract text from image or text file
# Extract section by matching a single heading
def extract_section(text, header):
    if not text:  # check for None or empty string
        return []
    lines = text.splitlines()
    start_idx = None
    end_headers = ["Disease Predictions", "Diet Recommendations", "Precautionary Measures", "Personalized Diet Recommendations", "Appropriate Precautionary Measures"]

    # Normalize headers for comparison
    normalized_lines = [line.strip().lower() for line in lines]
    header = header.lower()

    # Find start of the section
    for i, line in enumerate(normalized_lines):
        if header in line:
            start_idx = i
            break

    if start_idx is None:
        return []

    section = []
    for line in lines[start_idx + 1:]:
        # Stop if a new top-level section starts
        if any(h.lower() in line.lower() for h in end_headers if h.lower() != header):
            break
        section.append(line.strip())

    return [line for line in section if line]  # remove empty lines


# Tries multiple possible headers
def extract_any_section(text, headers):
    for h in headers:
        result = extract_section(text, h)
        if result:
            return result
    return []
# Function to extract text from image or text file
def extract_text(uploaded_file):
    if uploaded_file.name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")
    else:
        image = Image.open(uploaded_file)
        return pytesseract.image_to_string(image)


# Upload medical report
uploaded_file = st.file_uploader("Upload your medical report (.txt or image)", type=["txt", "png", "jpg", "jpeg"])

if uploaded_file:
    medical_report = extract_text(uploaded_file)
    st.success("Medical report uploaded successfully.")
    
    if st.button("Analyze Report"):
        with st.spinner("Processing..."):

            # Step 1: Specialist Agents
            cardiologist = Cardiologist(medical_report)
            cardiologist_response = cardiologist.run()

            psychologist = Psychologist(medical_report)
            psychologist_response = psychologist.run()

            pulmonologist = Pulmonologist(medical_report)
            pulmonologist_response = pulmonologist.run()

            # Step 2: Multidisciplinary Analysis
            mdt = MultidisciplinaryTeam(
                cardiologist_report=cardiologist_response,
                psychologist_report=psychologist_response,
                pulmonologist_report=pulmonologist_response
            )
            final_diagnosis = mdt.run()

            # Step 3: Diet & Precaution
            diet_agent = Dietician(medical_report)
            diet_response = diet_agent.run()

            precaution_agent = PreventiveSpecialist(medical_report)
            precaution_response = precaution_agent.run()
        

        # Display three-column layout
        # Debug print to inspect agent outputs
        # st.subheader("🛠 Debug: Raw Agent Outputs")
        # st.code(final_diagnosis, language="markdown")
        # st.code(diet_response, language="markdown")
        # st.code(precaution_response, language="markdown")



        table_data = {
    "🧬 Final Diagnosis": extract_any_section(final_diagnosis, ["Disease Predictions", "Final Diagnosis"]) or ["No diagnosis available."],
    "🥗 Diet Recommendations": extract_any_section(diet_response, ["Diet Recommendations", "Personalized Diet", "Diet Plan"]) or ["No diet suggestions found."],
    "🛡️ Precautionary Measures": extract_any_section(precaution_response, ["Precautionary Measures", "Precaution Tips", "Recommendations"]) or ["No precautions found."]
}


                # Display structured output in a more readable layout
        st.markdown("## 🧠 Final Diagnosis Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("🧬 Final Diagnosis")
            for item in table_data["🧬 Final Diagnosis"]:
                if item.strip():
                    st.markdown(f"- {item}")


        with col2:
            st.subheader("🥗 Diet Recommendations")
            for item in table_data["🥗 Diet Recommendations"]:
                if item.strip():
                    st.markdown(f"- {item}")

        with col3:
            st.subheader("🛡️ Precautionary Measures")
            for item in table_data["🛡️ Precautionary Measures"]:
                if item.strip():
                    st.markdown(f"- {item}")

        st.markdown("---")
        st.success("✅ By following the personalized diagnosis, dietary advice, and precautionary measures, users can better manage their health and enhance their quality of life.")

       

        # # Create a dynamic table with extracted agent outputs
        # table_data = {
        #     "🧬 Final Diagnosis": final_diagnosis.split("\n") if final_diagnosis else ["No diagnosis available."],
        #     "🥗 Diet Recommendations": diet_response.split("\n") if diet_response else ["No diet suggestions found."],
        #     "🛡️ Precautionary Measures": precaution_response.split("\n") if precaution_response else ["No precautions found."]
        # }

        # # Make sure all columns have equal number of rows
        # max_len = max(len(table_data[col]) for col in table_data)
        # for col in table_data:
        #     table_data[col] += [""] * (max_len - len(table_data[col]))

        # df = pd.DataFrame(table_data)

        # # Render the table
        # st.markdown("### 🧠 Final Diagnosis Summary (Structured Table)")
        # st.table(df)
st.markdown("## 💬 Chat with MediScan Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.form("chat_form"):
    user_input = st.text_input("Ask a question about your diagnosis, diet, or precautions", key="chat_input")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    bot_response = get_bot_response(user_input)
    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})

# Display chat history
for msg in st.session_state.chat_history:
    role = "🧑 You" if msg["role"] == "user" else "🤖 Assistant"
    st.markdown(f"**{role}:** {msg['content']}")


def download_chat_as_pdf(history):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for msg in history:
        role = "You" if msg["role"] == "user" else "Assistant"
        pdf.multi_cell(0, 10, f"{role}: {msg['content']}\n")

    # Fix: Write to BytesIO using dest="S"
    pdf_output = pdf.output(dest='S').encode('latin-1')  # Encode for binary
    return io.BytesIO(pdf_output)


if st.button("📄 Download Chat as PDF"):
    if st.session_state.chat_history:
        pdf_data = download_chat_as_pdf(st.session_state.chat_history)
        st.download_button("Download", data=pdf_data, file_name="chat_summary.pdf", mime="application/pdf")
    else:
        st.warning("💬 No chat history to save yet.")

