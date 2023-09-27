import streamlit as st
import copy 
from bol.constants.commissions import PRODUCT_GROUPS

class DataEditor:
    
    
    def __init__(self, df, mimic:str) -> None:
        
        self.df = copy.deepcopy(df)
        self.mimic = mimic
        
        self.columns_to_show = [
            "product name",
            "product group",
        ]
        
        self.columns_changable = [
            "product group",
        ]
        
        
    
    
    def callback(self, key):
        st.session_state[self.mimic] = st.session_state["data_editor_{}".format(key)]["edited_rows"]
    
    def render(self, key:str):
        st.data_editor(
            self.df[self.columns_to_show],
    
            column_config={
                "product group": st.column_config.SelectboxColumn(
                    "product group",
                    help="Update the product group of the product",
                    options=PRODUCT_GROUPS,
                )
            },
            
            key="data_editor_{}".format(key),
            on_change=self.callback,
            args=(key,),
            disabled=list(set(self.columns_to_show) - set(self.columns_changable)),
            use_container_width=True,
            hide_index=True,
        )
    
    
    