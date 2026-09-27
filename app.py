import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/ask"


st.set_page_config(
    page_title="InterviewIQ",
    page_icon="🤖",
    layout="centered"
)


st.title("🤖 InterviewIQ")
st.subheader("AI Engineer Knowledge Assistant")

st.write(
    "Ask questions about Python, DSA, Machine Learning, "
    "RAG, Databases, and AI Engineering."
)


question = st.text_input(
    "Ask your question:",
    placeholder="e.g. How does gradient descent update model weights?"
)


if st.button("Ask InterviewIQ"):

    if not question.strip():
        st.warning("Please enter a question.")

    else:
        with st.spinner("Thinking..."):

            response = requests.post(
                API_URL,
                json={"question": question}
            )

        if response.status_code == 200:

            data = response.json()

            st.markdown("### 💡 Answer")
            st.write(data["answer"])

            st.markdown("### 📚 Sources")

            for source in data["sources"]:
                st.write(f"- {source}")

        else:
            st.error("Something went wrong with the API.")