import streamlit as st 
from upload.DataHandler import DataHandler
import warnings



def upload_section():
    st.subheader("Upload Excel File")
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"], key="data_file")
    datahandler = DataHandler()
    
    if uploaded_file:    
        datahandler.process_uploaded_file(uploaded_file)
        
    if "updated_rows" in st.session_state and st.session_state.updated_rows is not None:
        datahandler.process_updated_rows()
        
    datahandler.render_results()
        
    
def main():
    upload_section()
    
    
    
    
    
    
if __name__ == "__main__":
    warnings.simplefilter(action='ignore', category=FutureWarning)
    st.set_page_config(page_title="Bol Estimator", layout="wide")
    main() 