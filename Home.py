import streamlit as st  
from utils.loader import download_model



def main():
    st.header("Expansion Dev Tool")
    download_model() 
















if __name__ == "__main__":
    st.set_page_config(page_title="Expansion Dev Tool", page_icon="📈", layout="wide")
    main()