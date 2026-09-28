import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/ask"


st.set_page_config(
    page_title="InterviewIQ",
    page_icon="🤖",
    layout="centered"
)


st.title("🤖 InterviewIQ")
st.caption("AI Engineer Knowledge Assistant")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input
question = st.chat_input(
    "Ask something about Python, ML, RAG, DSA..."
)


if question:

    # Display user message
    with st.chat_message("user"):
        st.markdown(question)

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })


    # Call backend
    with st.chat_message("assistant"):

        with st.spinner("Searching knowledge base..."):

            try:

                response = requests.post(
                    API_URL,
                    json={"question": question},
                    timeout=60
                )

                response.raise_for_status()

                data = response.json()

                answer = data["answer"]
                sources = data["sources"]


                # Answer
                st.markdown(answer)


                # Sources
                if sources:

                    st.markdown("**Sources:**")

                    for source in sources:
                        st.caption(f"📄 {source}")


                # Save assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })


            except requests.exceptions.RequestException as e:

                st.error(
                    f"Could not connect to the RAG API: {e}"
                )