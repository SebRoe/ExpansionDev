import pandas as pd
import streamlit as st 
import copy

def show_product_informations(df):
    columns = [
        "product name",
        "length",
        "width",
        "height",
        "weight",
        "selling price incl. vat",
        "buying price excl. vat",
        "vat",
        "perishable",
        "fragile",
        "labeling",
        "storage winter",
        "storage duration",
        "delivery destination",
    ]
    cDf = copy.deepcopy(df)
    cDf = cDf[columns]
    st.subheader("Product Overview")
    st.dataframe(cDf, use_container_width=True)




def show_logistics(df):
    
    columns = [
        "product name",
        "logistic validity attr",
        "logistic message attr",
        "logistic validity logistics",
        "logistic message logistics",
        "format",

        
        "fee per article",
        "fee per delivery",
        "fee fragile",
        "fee perishable",
        "fee labeling",
        "fee storage",
        "total logistics fee",
    ]
    cDf = copy.deepcopy(df)
    cDf = cDf[columns]
    st.subheader("Logistics")
    st.dataframe(cDf)


def show_commissions(df):
    
    columns = [
        "product name",
        "commission validity attr",
        "commission message attr",
        "commission validity commission",
        "commission message commission",

        "fee fixed",
        "fee percentage",
        "fee surcharge",
        "total commissions fee",
    ]
    cDf = copy.deepcopy(df)
    cDf = cDf[columns]
    st.subheader("Commissions")
    st.dataframe(cDf)


def show_costs_overview(df):
    columns = [
        "product name",
        "total logistics fee",
        "total commissions fee",
        "buying price excl. vat",
        "selling price incl. vat",
        "margin excl. VAT",
        "% margin excl. VAT",
    ]
    cDf = copy.deepcopy(df)
    cDf = cDf[columns]
    st.subheader("Overview Costs and Margin")
    st.dataframe(cDf)
    
    