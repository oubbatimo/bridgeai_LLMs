#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 17:14:52 2022

@author: mohamedoubbati
"""

import streamlit as st
import os
import replicate


st.title('bridgeai')
st.subheader('Large Language Model Llama 2 7b')

#For more information, please visit my website: https://www.bridgeai.de/


#Put here your personal Replicate API
your_replicate_api='r8_    '

#------------------
#LLM CONFIGURATION

#llm model
llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'

#llm parameters
temperature=0.5 
top_p=0.7
max_length=512

#--------------------


os.environ['REPLICATE_API_TOKEN']=your_replicate_api

st.session_state.messages=[{"role": "assistant", "content":"How may I assist you today?"}]


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Create a Function to generate the Llama 2 Response
def generate_llama2_response(prompt_input):
    default_system_prompt="You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for data in st.session_state.messages:
        print("Data:", data)
        if data["role"]=="user":
            default_system_prompt+="User: " + data["content"] + "\n\n"
        else:
            default_system_prompt+="Assistant" + data["content"] + "\n\n"
    
    output=replicate.run(llm, input={"prompt": f"{default_system_prompt} {prompt_input} Assistant: ",
                                     "temperature": temperature, "top_p":top_p, "max_length": max_length, "repititon_penalty":1})

    return output


#User -Provided Prompt

if prompt := st.chat_input(disabled=not your_replicate_api):
    st.session_state.messages.append({"role": "user", "content":prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a Response from the User-Provided Prompt (if the last message is not from the asssistant)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response=generate_llama2_response(prompt)
            placeholder=st.empty()
            full_response=''
            for item in response:
                full_response+=item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)

    message= {"role":"assistant", "content":full_response}
    st.session_state.messages.append(message)
