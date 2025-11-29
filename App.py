# App.py
import streamlit as st
import openai

st.set_page_config(page_title="Smart Reply — AI Assistant", layout="centered")

st.title("💬 Smart Reply — AI Assistant")
st.write("Ask anything + Choose tone. Powered by OpenAI")

# API key from Streamlit secrets
if "OPENAI_API_KEY" not in st.secrets:
    st.error("OPENAI_API_KEY missing. Go to Settings → Secrets and add it.")
    st.stop()

openai.api_key = st.secrets["OPENAI_API_KEY"]

message = st.text_input("Your message:", placeholder="e.g. Where are you?")
tone = st.selectbox("Tone", ["friendly", "angry", "funny", "professional", "sad", "excited"])

if st.button("Generate Reply"):
    if not message:
        st.warning("Please enter a message first.")
    else:
        with st.spinner("Generating..."):
            try:
                resp = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": f"Reply in a {tone} tone."},
                        {"role": "user", "content": message}
                    ],
                    max_tokens=200,
                    temperature=0.8,
                )
                reply = resp["choices"][0]["message"]["content"].strip()
            except Exception as e:
                st.error(f"API error: {e}")
                reply = None

        if reply:
            st.markdown("---")
            st.subheader(f"Tone: {tone.capitalize()}")
            st.write(f"**User:** {message}")
            st.write(f"**AI:** {reply}")
