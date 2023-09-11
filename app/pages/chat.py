import streamlit as st
import openai

openai.api_type = "azure"
# openai.api_key = st.secrets['API_KEY']
openai.api_key = st.session_state.key
openai.api_base = "https://oai-oaichat-sbx-eus-001.openai.azure.com"
openai.api_version = "2023-03-15-preview"

if "chat_started" not in st.session_state:
    st.session_state.chat_started = False

def reset_conversation():
  st.session_state.messages = []
  st.session_state.chat_started = False

st.button('Reset Chat', on_click=reset_conversation)

st.title('Persona bot')

prompt_init = f"""
Context:
I am going to send you a profile of an individual, then I am going to ask you a 
series of survey questions. You must create a persona based on the provided 
profile and respond to the survey questions using that persona's perspective and
tone of voice. Avoid providing answers based on common interests, cliches and 
racial or gender stereotypes. Instead cater your responses to the persona 
specifically. Keep your responses in the style of a conversational interview.

The profile of the individual:
{st.session_state.persona}
"""

st.session_state.messages.append({"init": True, "role": "user", "content": prompt_init})

for message in st.session_state.messages:
    if not message["init"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

prompt = st.chat_input("Ask me stuff")

if not st.session_state.chat_started:
    greet = "Ok I'm ready"
    with st.chat_message("ai"):
        st.markdown(greet)
    st.session_state.messages.append({"init": False, "role": "assistant", "content": greet})
    st.session_state.chat_started = True

if prompt:
    st.session_state.messages.append({"init": False, "role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("ai"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            engine=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"init": False, "role": "assistant", "content": full_response})