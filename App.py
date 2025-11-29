import os
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Smart Reply — Search", layout="wide")

# ----------------------
# CONFIG: API key
# ----------------------
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    st.error("OpenAI API key missing! Add it in Streamlit → Secrets.")
    st.stop()

client = OpenAI(api_key=API_KEY)

# ----------------------
# UI
# ----------------------
st.markdown("<h1 style='color:#0b69ff;margin:0'>💬 Smart Reply — AI Assistant</h1>", unsafe_allow_html=True)
st.write("Ask anything + Choose tone. Powered by OpenAI 🤖✨")

col1, col2 = st.columns([3,1])
with col1:
    query = st.text_input("Your message:", "", placeholder="e.g. Where are you?")
with col2:
    tone = st.selectbox("Tone", ["friendly","professional","funny","romantic","angry"])
    run = st.button("Generate Reply")

result_area = st.empty()

# ----------------------
# Call OpenAI
# ----------------------
def ask_openai(prompt, model="gpt-4o-mini"):
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role":"user","content": prompt}]
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"[ERROR] {e}"

if run:
    if not query.strip():
        st.warning("Please enter a message first!")
    else:
        prompt = f"Reply to this message in a {tone} tone: {query}"
        with st.spinner("AI thinking..."):
            answer = ask_openai(prompt)

        card_html = f"""
        <div style="background:#fff;border-radius:12px;padding:16px;margin-top:10px;
                    box-shadow:0 6px 18px rgba(11,105,255,0.06);">
          <div style="font-weight:700;color:#111;margin-bottom:8px;">Tone: {tone.title()}</div>
          <div style="color:#222;font-size:15px;margin-bottom:10px">User: {query}</div>
          <hr>
          <div style="font-size:15px;color:#111;white-space:pre-wrap"><b>AI:</b> {answer}</div>
        </div>
        """
        result_area.markdown(card_html, unsafe_allow_html=True)
