import openai
from utils import * 
from constants import *
import streamlit as st
from io import StringIO
from PIL import Image

# Create an OpenAI client instance using the API key
client = openai.OpenAI(api_key=OPENAIKEY)

def general_corrector(prompt, temperature, model=OPENAIMODEL, max_tokens=20):
    try:
        # Using the client instance to create a completion
        res = client.completions.create(model=model, prompt=prompt, temperature=temperature, max_tokens=max_tokens)
        return res.choices[0].text
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return ""

def single_experience_corrector(experience_text):
    correct_text = general_corrector(prompt=EXPERIENCE_PROMPT_CONVERT + experience_text, temperature=0.4, max_tokens=200)
    st.markdown("<span style='color:navy'>" + experience_text + "</span>", unsafe_allow_html=True)
    st.markdown("The AI suggests the following summary instead: \n", unsafe_allow_html=True)
    st.markdown("<span style='color:red'>" + correct_text + "</span>", unsafe_allow_html=True)
    return correct_text

def summary_corrector(summary_text):
    st.markdown("The AI is rephrasing the text (if necessary):", unsafe_allow_html=True)
    first_correction = general_corrector(prompt=SUMMARY_PROMPT_CONVERT + summary_text, temperature=TEMPERATURE_SUMMARY_PROMPT_CONVERT, max_tokens=200)
    st.markdown("The AI is improving the rephrased summary", unsafe_allow_html=True)
    final_correction = general_corrector(prompt=SUMMARY_PROMPT_IMPROVER + first_correction, temperature=TEMPERATURE_SUMMARY_PROMPT_IMPROVER, max_tokens=200)
    st.markdown("The summary section of your CV is the following one:", unsafe_allow_html=True)
    st.markdown("<span style='color:navy'>" + summary_text + "</span>", unsafe_allow_html=True)
    st.markdown("The AI suggests the following summary instead:", unsafe_allow_html=True)
    st.markdown("<span style='color:red'>" + final_correction + "</span>", unsafe_allow_html=True)
    return final_correction

def summary_corrector_main(summary_text):
    first_correction = general_corrector(prompt=SUMMARY_PROMPT_CONVERT + summary_text, temperature=TEMPERATURE_SUMMARY_PROMPT_CONVERT, max_tokens=200)
    final_correction = general_corrector(prompt=SUMMARY_PROMPT_IMPROVER + first_correction, temperature=TEMPERATURE_SUMMARY_PROMPT_IMPROVER, max_tokens=200)
    return final_correction

def single_experience_corrector_main(experience_text):
    correct_text = general_corrector(prompt=EXPERIENCE_PROMPT_CONVERT + experience_text, temperature=0.4, max_tokens=200)
    return correct_text
