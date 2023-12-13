import streamlit as st
from main_self_improve_Class import GPT4AutoCoder
import os
import openai
# from dotenv import load_dotenv

# load_dotenv()
logo_url = "https://yt3.googleusercontent.com/OR2aEA7-LvbSLdyfow5tjPFSpBvWqJ_aq-laCk0DVUeEf6w9NEDeuqQQlCrW-_DuCVkHATrdvA=s176-c-k-c0x00ffffff-no-rj"
st.set_page_config(page_title="GPT-4 Auto Coder", layout="wide")

col1, col2 = st.columns((1,4))
with col1:
    st.image(logo_url, width=100)
with col2:
    st.title("Automation AI Assistant🤖")

# Sidebar
with st.sidebar:
    st.title("Models:")

    # API key input
    api_key =  "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" or os.environ['OPENAI_API_KEY']
    # api_key = st.text_input("Enter your OpenAI API key:", type="password", placeholder="OpenAI API key here")

    if api_key:
        st.session_state["OPENAI_API_KEY"] = api_key

    # GPT Engine choice
    gpt_engine_choice = st.radio(
        "Choose GPT engine:",
        ("gpt-4-1106-preview", "gpt-4", "gpt-3.5-turbo")
    )

auto_coder = GPT4AutoCoder(api_key, gpt_engine_choice)

user_input = st.text_area("Enter the lib discription you want to create or add exiting lib to improve:", height=300,
 help="enter a descripton of your task here and then select the number of iterations for improvement. Then click on the 'Generate Code' button to get the code.")

# code_input = st.text_area("OR paste your existing code here if you want to improve it:", height=300, help="type or paste your existing code here and then select the number of iterations for improvement. Then click on the 'Generate Code' button to get the code improved.")
option = st.selectbox(
    'How would you like to do?',
    ('Create New Lib', 'Improve Existing Lib', 'Create Test Case'))

match option:
    case 'Create New Lib':
        code_input = None
    case 'Improve Existing Lib':
        code_input = user_input
    case 'Create Test Case':
        st.text('We do not support this yet!')
        user_input = None



num_attempts = st.number_input("Enter the number of iterations for improvement:", min_value=0, value=1, step=1, help="GPT will try to improve the code this many times. GPT will add new features, error catching, bug fixing, etc. to the code.")

if st.button("Generate Code"):
    if not st.session_state.get("OPENAI_API_KEY"):
        st.title("Please enter your OpenAI API key in the sidebar first!")
    with st.spinner("Generating code..."):
        if code_input:
            existing_code = code_input

            for attempt in range(1, num_attempts + 1):
                gpt3_question = f"The current code is:\n```\n{existing_code}\n``` Improve the following Python code (implement new ideas if necessary) based on the discription as a cisco automation engineer and based on how our codebase looks like, including error catching and bug fixing. Write the entire code from scratch while implementing the improvements. Start the code block with a simple 'python' word. Comment about the changes you are making."
                response = GPT4AutoCoder(api_key, gpt_engine_choice).ask_gpt3(gpt3_question)
                existing_code = response
                st.write("Iteration", attempt, "of", num_attempts, "code improvements completed.")
                st.code(response, language="python")
        elif user_input:
            gpt3_question = GPT4AutoCoder(api_key, gpt_engine_choice).get_project_idea(user_input)

            response = GPT4AutoCoder(api_key, gpt_engine_choice).ask_gpt3(gpt3_question)

            st.code(response, language="python")

            for attempt in range(1, num_attempts + 1):
                gpt3_question = f"The current code is:\n```\n{response}\n``` Improve the following Python code (implement new ideas if necessary), including error catching and bug fixing. Write the entire code from scratch while implementing the improvements. Start the code block with a simple 'python' word. Comment about the changes you are making."
                response = GPT4AutoCoder(api_key, gpt_engine_choice).ask_gpt3(gpt3_question)
                st.code(response, language="python")
