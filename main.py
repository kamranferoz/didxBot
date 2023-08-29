import openai
import streamlit as st


st.title("Chat With DIDX.net...")
st.subheader("Powered by Kamran Feroz")

openai.api_key = st.secrets['OPENAI_API_KEY']

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask anything about DIDX Inc?"):

    primer = f"""Act as an representative of DIDX Inc, https://didx.net. answer the queries for the user from the website contents i.e. https://didx.net and https://kb.didx.net, incase you don't find any suitable answer to the user's query you can direct the user visit our website i.e. https://didx.net for general queries or https://kb.didx.net for the knowledge base"""
    # st.session_state.messages.append.__init__({"role": "system", "content": primer})
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # primer = f"""Your task is to answer user questions based on the information given above each question.It is crucial to cite sources accurately by using the [[number](URL)] notation after the reference. Say "I don't know" if the information is missing and be as detailed as possible. End each sentence with a period. Please begin."""
        # primer = f"""Act as an representative of DIDX Inc, https://didx.net. answer the queries from the user, say please visit our website i.e. https://didx.net if you don't find a suitable answer"""
        # {"role": "system", "content": primer},
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": "system", "content": primer},
                {"role": "user", "content": prompt},
                # {"role": "user", "content": prompt},
                # {"role": m["role"], "content": m["content"]}
                # for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
