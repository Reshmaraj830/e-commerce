import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import os
from io import BytesIO

# Initialize Gemini API
genai.configure(api_key="AIzaSyADh8pKp_qFmoJxh53JHU7MfiFkBDwwiRU")  # <-- Replace with your Gemini API Key

model = genai.GenerativeModel('gemini-2.0-flash')

# App Configuration
st.set_page_config(page_title="AI Email Generator", layout="centered")

st.title("📧 AI-Powered Email Generator")
st.write("Enter your message and choose the email format and tone. Then generate and download your email!")

# --- INPUT SECTION ---
prompt = st.text_area("✍️ Enter your message or context for the email:", height=150)

col1, col2 = st.columns(2)

with col1:
    email_format = st.selectbox("📂 Select Email Format", ["Formal", "Informal", "Business", "Thank You", "Apology"])
with col2:
    email_tone = st.selectbox("🎭 Select Tone", ["Professional", "Friendly", "Assertive", "Empathetic"])

# Session State Setup
if "generated_email" not in st.session_state:
    st.session_state["generated_email"] = ""

# --- GENERATE EMAIL FUNCTION ---
def generate_email(prompt, email_format, email_tone):
    full_prompt = f"""
    Generate an email based on the following input:
    - Message/Content: {prompt}
    - Format: {email_format}
    - Tone: {email_tone}
    
    The email should be well-structured, appropriate to the selected tone, and formatted accordingly.
    """
    response = model.generate_content(full_prompt)
    return response.text.strip()

# --- GENERATE BUTTON ---
if st.button("🔍 Generate Email"):
    if prompt.strip():
        email_output = generate_email(prompt, email_format, email_tone)
        st.session_state["generated_email"] = email_output
    else:
        st.warning("Please enter your message to generate an email.")

# --- DISPLAY GENERATED EMAIL ---
if st.session_state["generated_email"]:
    st.subheader("📨 Generated Email")
    st.write(st.session_state["generated_email"])

    # --- PDF DOWNLOAD FUNCTION ---
    def create_pdf(text):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        for line in text.split('\n'):
            pdf.multi_cell(0, 10, line)
        pdf_output = BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)
        return pdf_output

    # Download Button
    pdf_file = create_pdf(st.session_state["generated_email"])
    st.download_button(
        label="📥 Download Email as PDF",
        data=pdf_file,
        file_name="generated_email.pdf",
        mime="application/pdf"
    )

    # --- Regenerate Button ---
    if st.button("🔁 Regenerate with new Format/Tone"):
        if prompt.strip():
            new_output = generate_email(prompt, email_format, email_tone)
            st.session_state["generated_email"] = new_output
        else:
            st.warning("Please enter your message again.")

