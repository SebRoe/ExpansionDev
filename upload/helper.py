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
        "selling price",
        "buying price",
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
    st.dataframe(cDf)




def show_logistics(df):
    
    columns = [
        "product name",
        "logistic validity attr",
        "logistic message attr",
        "logistic validity logistics",
        "logistic message logistics",
        "format",

        "fee storage per month",
        "fee fragile",
        "fee perishalbe",
        "fee labeling",
        
        "cost per article",
        "cost per delivery",
        "cost fragile",
        "cost perishable",
        "cost labeling",
        "cost storage",
        "total logistics costs",
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
        "fee fixed excl. vat.",
        "fee percentage excl. vat",
        "cost fixed fee incl. vat",
        "cost percentage fee incl. vat",
        "cost surcharge",
        "total commissions costs",
    ]
    cDf = copy.deepcopy(df)
    cDf = cDf[columns]
    st.subheader("Commissions")
    st.dataframe(cDf)


def show_costs_overview(df):
    columns = [
        "product name",
        "total logistics costs",
        "total commissions costs",
        "buying price",
        "selling price",
        "brutto margin",
        "% margin",
    ]
    cDf = copy.deepcopy(df)
    cDf = cDf[columns]
    st.subheader("Overview Costs and Margin")
    st.dataframe(cDf)
    
    