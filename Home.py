import streamlit as st  
from utils.loader import download_model
from bol.constants.commissions import PRODUCT_GROUPS
import pandas as pd 
import io 

def create_excel_data():
    df = pd.DataFrame(columns=[
        "product name", "length", "width", "height", "weight", "selling price",
        "buying price", "vat", "perishable", "fragile",
        "labeling", "storage winter", "storage duration",
        "delivery destination"
    ])
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return output.read()

def main():
    st.header("Dev Tool")
    st.subheader("This tool is still under construction..")
    download_model() 
    

    st.warning("When uploading a csv file certain columns are required. The columns are as follows:")

    data_instructions = [
        ("Column Name", "Data Type", "Required", "Default Value", "Additional Information"),
        ("length", "float", "Yes", "None", "Enter the length in cm."),
        ("width", "float", "Yes", "None", "Enter the width in cm."),
        ("height", "float", "Yes", "None", "Enter the height in cm."),
        ("weight", "float", "Yes", "None", "Enter the weight in kilograms."),
        ("selling price", "float", "Yes", "None", "Enter the selling price."),
        ("buying price", "float", "Yes", "None", "Enter the buying price."),
        ("vat", "float", "No", "21.0", "Enter the VAT percentage (0 to 100)."),
        ("perishable", "bool", "No", "False", "Set to 'True' if the item is perishable, otherwise 'False'."),
        ("fragile", "bool", "No", "False", "Set to 'True' if the item is fragile, otherwise 'False'."),
        ("labeling", "bool", "No", "False", "Set to 'True' if labeling is required, otherwise 'False'."),
        ("storage winter", "bool", "No", "False", "Set to 'True' if winter storage is needed, otherwise 'False'."),
        ("storage duration", "int", "No", "1", "Enter the storage duration in days."),
        ("delivery destination", "DestinationCountry", "No", "NL", "Enter the delivery destination."),
    ]

    df = pd.DataFrame(columns=[ "product name", 
        "length", "width", "height", "weight", "selling price",
        "buying price", "vat", "perishable", "fragile",
        "labeling", "storage winter", "storage duration",
        "delivery destination"
    ])



    st.write("### Detailed Data Entry Instructions:")
    st.table(data_instructions)
    st.download_button(
            label="Download Example File",
            data=create_excel_data(),
            file_name="example.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    
    st.write("### Special Treatment:")
    st.write("Some columns require special treatment. These columns are:")
    special_treatment = [
        ("product group", "product name"),
    ]
    st.table(special_treatment)
    st.write("If the product group column is not existent in the uploaded file, the product name column will be used to estimate the product group.")
    st.write("You will be able to tweak that estimations around.")

    st.write("### Product Groups:")
    with st.expander("Click here to see the product groups"):
        st.table(PRODUCT_GROUPS)
    














if __name__ == "__main__":
    st.set_page_config(page_title="Expansion Dev Tool", page_icon="📈", layout="wide")
    main()