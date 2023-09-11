import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title='Digital twin skeleton',
    initial_sidebar_state='collapsed'
)
chatgpt_model_name = "chat"

if 'openai_model' not in st.session_state:
    st.session_state.openai_model = chatgpt_model_name

if "messages" not in st.session_state:
    st.session_state.messages = []

if "persona" not in st.session_state:
    st.session_state.persona = None

if "key" not in st.session_state:
    st.session_state.key = None

st.title('Persona constructor')

placeholder = '''
Age: 32
Gender: male 
Ethnicity: caucasian 
Income: NZD120,000 
Source of income: full time employee 
Job: auditor
Marital status: married
Orientation: straight
Family: 1 boy aged 9, 1 girl aged 5
Employer: kpmg 
Nationality: new zealand 
Country of residence: new zealand 
Prior foreign countries visited: australia, united kingdom 
Hobbies: hiking 
'''

st.session_state.key = st.text_input('API key')

st.session_state.persona = st.text_area('Persona input', 
                                        placeholder=placeholder, height=500)

launch_chat = st.button('Launch persona')

if launch_chat:
    if st.session_state.persona is None or st.session_state.persona == '':
        st.text('Give me some persona details doofus')
    else:
        switch_page('chat')
