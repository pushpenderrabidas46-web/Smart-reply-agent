import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Smart Reply – AI Assistant", layout="centered")

st.title("💬 Smart Reply — AI Assistant")
st.write("Ask anything + Choose tone. Powered by OpenAI 🤖✨")

# Load API key from Streamlit Secret
if "OPENAI_API_KEY" not in st.secrets:
    st.error("OPENAI_API_KEY missing. Go to Settings → Secrets and add it.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

message = st.text_input("Your message:", placeholder="e.g. Where are you?")
tone = st.selectbox("Tone", ["friendly", "angry", "funny", "professional", "sad", "excited"])

if st.button("Generate Reply"):
    if not message:
        st.warning("Please enter a message first.")
    else:
        with st.spinner("Generating..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": f"Reply in a {tone} tone."},
                        {"role": "user", "content": message},
                    ],
                    max_tokens=200,
                    temperature=0.8
                )

                # FIXED LINE 👇  
                reply = response.choices[0].message.content

                st.subheader(f"Tone: {tone.capitalize()}")
                st.write(f"**AI:** {reply}")

            except Exception as e:
                st.error(f"API Error: {e}")
