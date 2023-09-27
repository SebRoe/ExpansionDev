
import streamlit as st
from ml.SimplifiedBertClassifier import SimplifiedBertClassifier
import os
import json
import requests 
import gdown
import subprocess

@st.cache_data
def load_classes():
    with open(os.path.join("ml", "classes.json"), "r") as f:
        classes = json.load(f)

    return classes

@st.cache_resource
def load_model():
    
    classes = load_classes()
    classifier = SimplifiedBertClassifier(
        os.path.join("ml", "model"), os.path.join("ml", "model"), classes
    )
    return classifier


@st.cache_resource(show_spinner=True)
def download_model():
    
    file_path = os.path.join("ml", "model", "pytorch_model.bin")
    url = "https://drive.google.com/file/d/1ovZfQVMkHwC_STQAHxa9wPBcFJStCwef/view?usp=sharing"
    file_id = "1ovZfQVMkHwC_STQAHxa9wPBcFJStCwef"
    if os.path.exists(file_path):
        return
    else:  
        command = f'gdown --id {file_id} --output {file_path} --quiet'
        subprocess.run(command, shell=True, check=True)