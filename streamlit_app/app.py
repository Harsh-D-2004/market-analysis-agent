import streamlit as st
import requests

st.set_page_config(page_title="Market Analysis Agent", page_icon="📈")

st.title("Market Analysis Agent")
st.markdown("Upload an audio file (WAV, MP3) and get a market-related insight generated from your voice query.")

st.markdown("---")

audio_file = st.file_uploader("Upload your audio query", type=["wav", "mp3"])

if audio_file is not None:
    with st.spinner("Analayzing..."):
        files = {"file": (audio_file.name, audio_file, audio_file.type)}
        response = requests.post("http://localhost:8000/response", files=files)

    st.markdown("---")

    if response.status_code == 200:
        data = response.json()

        if "result" in data:
            st.success("Query processed successfully!")

            with st.expander("Query"):
                st.code(data.get("query", "No query available."), language="markdown")

            with st.expander("Response"):
                st.markdown(f"**{data.get('result', 'No response available.')}**")

        else:
            st.warning("⚠️ No valid result received.")
    else:
        st.error("Request failed.")
        st.markdown("Please try again.")

