import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Auto-load variables from .env (e.g., OPENAI_API_KEY)
load_dotenv()

# ========= 1) Initialize OpenAI Client =========
# macOS/Linux: export OPENAI_API_KEY="your_key"
# Windows PowerShell: setx OPENAI_API_KEY "your_key"
# pip install streamlit openai python-dotenv
# Run: streamlit run survey.py
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_completion(prompt, model="gpt-4o", temperature=0):
    """
    Helper to call Chat Completions API and return the text content.
    """
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature  # 0 = most deterministic
    )
    return response.choices[0].message.content

# ========= 2) Streamlit UI =========
st.set_page_config(page_title="Perfume Talent Test (Lite)", page_icon="🧪")
st.title("Perfume Talent Test (Lite)")

st.markdown("Please answer the questions below, then click the button to generate results via the LLM.")

# Q1: Concentration (select box)
q1 = st.selectbox(
    "Q1: What concentration do you want to blend?",
    [
        "Parfum (Extrait)",
        "Eau de Parfum (EDP)",
        "Perfume (Eau de Parfum/Toilette)",
        "Eau de Toilette (EDT)",
        "Eau de Cologne (EDC)"
    ],
    index=1
)

# Q2/Q3/Q4: Free text inputs
q2_text = st.text_area(
    "Q2: What do you want for the top notes? (free text)",
    placeholder="Examples: citrus (lemon, sweet orange, yuzu), aromatic herbs (lavender, clary sage, mint), or anything else..."
)

q3_text = st.text_area(
    "Q3: What do you want for the heart/middle notes? (free text)",
    placeholder="Examples: floral (rose, jasmine, mimosa), spicy (pepper, clove, cinnamon), or anything else..."
)

q4_text = st.text_area(
    "Q4: What do you want for the base notes? (free text)",
    placeholder="Examples: woody (cedar, sandalwood), balsamic (labdanum, vanilla), animalic (ambergris), etc."
)

# ========= 3) Generate & Call the LLM =========
if st.button("Evaluate"):
    # Build prompt from the questionnaire
    prompt = f"""
You are a highly professional master perfumer who is strict with apprentices. The user, however, is not your apprentice, so address them politely as “you”.

Based on the user's choices of concentration and their selected notes, give a bold, first-sentence verdict on whether they have a perfume-blending talent, with one of these ratings: 
“Extremely Talented”, “Very Talented”, “Some Talent”, “No Talent”, or “Extremely Untalented”. 
Briefly justify the verdict in that same opening sentence.

Then provide your expert guidance. Use your professional knowledge (for example: making a tea-centered theme as an EDP or Parfum can be quite challenging and often unsuitable—overly high concentration may cause a cloying ‘tea dizziness’ effect) to critique their selections and propose improvements.

Here is the user input:
1) Concentration: {q1}
2) Top notes (user free text): {q2_text.strip() if q2_text.strip() else "Not provided"}
3) Middle notes (user free text): {q3_text.strip() if q3_text.strip() else "Not provided"}
4) Base notes (user free text): {q4_text.strip() if q4_text.strip() else "Not provided"}

Output requirements:
- Start with the bold verdict sentence (rating + reason).
- Follow with concise, expert advice: balance, diffusion, longevity, seasonality, and potential substitutions.
- End with a sample formula sketch (top/middle/base in % totals summing to 100%), aligned with the chosen concentration.
"""

    with st.spinner("Generating suggestions..."):
        try:
            result = get_completion(prompt, model="gpt-4o", temperature=0.7)
        except Exception as e:
            result = f"LLM call failed: {e}"

    st.subheader("Model Suggestions")
    st.write(result)
