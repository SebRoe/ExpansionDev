import streamlit as st 
from streamlit_extras.add_vertical_space import add_vertical_space
import pandas as pd
from .DataValidator import DataValidator 
import copy 
from io import BytesIO
from bol.LogisticsEstimator import LogisticsEstimator
from bol.CommissionEstimator import CommissionEstimator
from bol.Storage import Storage
from bol.Product import Product
from bol.enums import LogisticMessages, CommissionMessages, ValidationMessages, DestinationCountry
from .DataEditor import DataEditor
from .helper import show_logistics, show_product_informations, show_commissions, show_costs_overview

class DataHandler():
    
    """Schnittstelle zwischen Streamlit und Busisness-Logik"""
    def __init__(self):
        self._set_class_variables()

    def _set_class_variables(self):
        
        if not "uploaded_df" in st.session_state:
            st.session_state.uploaded_df = None
            
        if not "processed_df" in st.session_state:
            st.session_state.processed_df = None
            
        if not "updated_rows" in st.session_state:
            st.session_state.updated_rows = None
            
        if not "excluded_rows" in st.session_state:
            st.session_state.excluded_rows = []
            
    def _unset_class_variables(self):
        if "uploaded_df" in st.session_state:
            del st.session_state.uploaded_df
            
        if "processed_df" in st.session_state:
            del st.session_state.processed_df
            
        if "updated_rows" in st.session_state:
            del st.session_state.updated_rows
            
        if "excluded_rows" in st.session_state:
            del st.session_state.excluded_rows
            
    def process_uploaded_file(self, uploaded_file):
        try:
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        except Exception as e:
            st.error("Error: {}".format(e))
        else:   
            
            if st.session_state.uploaded_df is None:
                st.write("Log: st.session_state.uploaded_df is None")
                self._validate_uploaded_file(df)
                
            else:
                if df.equals(st.session_state.uploaded_df):
                    pass
                else:
                    self._unset_class_variables()
                    self._validate_uploaded_file(df)            
            
    def _validate_uploaded_file(self, df:pd.DataFrame):
        """Validiert den hochgeladenen Datensatz"""

        with st.spinner("Validating File..."):
            st.subheader("File Format Validation")
            validator = DataValidator()
            
            cDf, logs = validator.validate_uploaded_file(copy.deepcopy(df)) 
            
            critical_error = False 
            fixable_error = False

            
            # General Error Discovery
            if len(logs["column_not_found"]) > 0 or len(logs["column_not_transformable"]) > 0 or len(logs["excluded_rows"]) == len(df):
                critical_error = True 
                
            if len(logs["changes"].keys()) > 0 or len(logs["attr_mismatch"]) > 0:
                fixable_error = True
                
            self._render_validation_summary(critical_error, fixable_error, df, logs)
            
            # New Uploaded File. 
            if not critical_error:
                st.session_state.uploaded_df = df
                st.session_state.processed_df = cDf         
                st.session_state.excluded_rows = logs["excluded_rows"]
                self._calculate_all_costs()
            else:
                pass
        
 
    def _add_meta_columns(self):
        
        st.session_state.processed_df["logistic validity attr"] = None                          
        st.session_state.processed_df["logistic message attr"] = None
        st.session_state.processed_df["logistic validity logistics"] = None
        st.session_state.processed_df["logistic message logistics"] = None
        st.session_state.processed_df["format"] = None


        st.session_state.processed_df["fee per article"] = None
        st.session_state.processed_df["fee per delivery"] = None
        st.session_state.processed_df["fee fragile"] = None
        st.session_state.processed_df["fee perishable"] = None
        st.session_state.processed_df["fee labeling"] = None
        st.session_state.processed_df["fee storage"] = None
        st.session_state.processed_df["total logistics fee"] = None        
        
        st.session_state.processed_df["commission validity attr"] = None
        st.session_state.processed_df["commission message attr"] = None
        st.session_state.processed_df["commission validity commission"] = None
        st.session_state.processed_df["commission message commission"] = None

        st.session_state.processed_df["fee fixed"] = None
        st.session_state.processed_df["fee percentage"] = None
        st.session_state.processed_df["fee surcharge"] = None
        st.session_state.processed_df["total commissions fee"] = None
        
        st.session_state.processed_df["selling price excl. vat"] = None
        
        st.session_state.processed_df["margin excl. VAT"] = None 
        st.session_state.processed_df["% margin excl. VAT"] = None 

    def _calc_per_product(self, id, row):
        
        product = Product(
            length=row["length"],
            width=row["width"],
            height=row["height"],
            weight=row["weight"],
            perishable=row["perishable"],
            fragile=row["fragile"],
            labeling=row["labeling"],
            price=row["selling price incl. vat"],
            vat=row["vat"],
            productName=row["product name"],
            productGroup=row["product group"],
        )
    
        storage = Storage(
            winter=row["storage winter"],
            duration=row["storage duration"],
        )


        # Calculate the costs.
        logistic = LogisticsEstimator(product, storage, DestinationCountry.from_string(row["delivery destination"]))
        commission = CommissionEstimator(product)

        cost_logistics:dict = logistic.get_logistic_fees()
        cost_commissions:dict = commission.get_commission_fees()

        for column, value in cost_logistics.items():
            st.session_state.processed_df.at[id, column] = value
        
        for column, value in cost_commissions.items():
            st.session_state.processed_df.at[id, column] = value
            
        # Calculate Margins
        
        st.session_state.processed_df.at[id, "selling price excl. vat"] = row["selling price incl. vat"] / (1 + row["vat"] / 100)
        
        
        
        marge_excl_vat = st.session_state.processed_df.at[id, "selling price excl. vat"] - st.session_state.processed_df.at[id, "buying price excl. vat"]
        marge_excl_vat -= cost_logistics["total logistics fee"] if cost_logistics["total logistics fee"] is not None else 0
        marge_excl_vat -= cost_commissions["total commissions fee"] if cost_commissions["total commissions fee"] is not None else 0
        
        st.session_state.processed_df.at[id, "margin excl. VAT"] = marge_excl_vat
        st.session_state.processed_df.at[id, "% margin excl. VAT"] = marge_excl_vat /  st.session_state.processed_df.at[id,"selling price excl. vat"] * 100
                
                
                
                
                
    def _calculate_all_costs(self):
        
        self._add_meta_columns()
        
        # Iterate over all rows and calculate the costs. 
        for id, row in st.session_state.processed_df.iterrows():
            self._calc_per_product(id, row)

    def process_updated_rows(self):
        for key, updates in st.session_state.updated_rows.items():
            for column, value in updates.items():
                st.session_state.processed_df.at[key, column] = value
            self._calc_per_product(key, st.session_state.processed_df.loc[key])
            
            

    #### RENDER METHODS ####
    def _render_validation_summary(self, critical_error, fixable_error, original_df, logs):
        if critical_error:
            st.error("Please fix the errors and try again.")
            
        if not critical_error and fixable_error:
            st.warning("We have made some changes to your inputs. Either they were wrong or we are just curious if you have made a mistake. Please review those changes, however the file is usable.")

        if not critical_error and not fixable_error:
            st.success("The file is valid.")
        
        with st.expander("Show first Validation Logs"):
                
            if logs["column_not_found"] == []:
                pass 
            else:
                st.error(f"The following columns are missing: {logs['column_not_found']}")
                
            if logs["changes"] == {}:
                pass 
            else:
                st.info(f"The following changes were made to the uploaded file: {logs['changes']}")
                
            if logs["attr_mismatch"] == []:
                pass
            else:
                st.error(f"The following attributes mismatched: {logs['attr_mismatch']}")
                
            
            if logs["excluded_rows"] == set():
                pass
            else:
                st.warning("The following rows were excluded: {}".format(logs["excluded_rows"]))
            
            if logs["column_not_transformable"] == []:
                pass
            else:
                st.error(f"The following columns could not be transformed: {logs['column_not_transformable']}")
            
            if len(logs["excluded_rows"]) == len(original_df):
                st.error("All rows were excluded, please check your file.")


    def render_results(self):
        if "processed_df" in st.session_state and st.session_state.processed_df is not None:
            add_vertical_space(2)
            show_product_informations(st.session_state.processed_df)
            add_vertical_space(2)
            st.subheader("Change Product Group here:")
            editor = DataEditor(st.session_state.processed_df, "updated_rows")
            editor.render("updated_rows")
            add_vertical_space(2)
            show_logistics(st.session_state.processed_df)
            add_vertical_space(2)
            show_commissions(st.session_state.processed_df)
            add_vertical_space(2)
            show_costs_overview(st.session_state.processed_df)
            add_vertical_space(2)
            
            st.download_button(
                label="Download the processed file",
                data=self.get_processed_df_as_excel(),
                file_name='processed_data.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                
            )
        

    def get_processed_df_as_excel(self):
        
        output = BytesIO()
        column_order = [
            "product name",
            "product group",
            "buying price excl. vat",
            "selling price incl. vat",
            "vat",
            "length",
            "width",
            "height", 
            "weight",
            "perishable",
            "fragile",
            "labeling",
            "storage winter",
            "storage duration",
            "delivery destination",                
        ]
        
        
        column_order.extend(
            [
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
        )
        
        column_order.extend(
            [
                "commission validity attr",
                "commission message attr",
                "commission validity commission",
                "commission message commission",
                "fee fixed",
                "fee percentage",
                "fee surcharge",
                "total commissions fee",
            ]
        )
        
        
        column_order.extend(
            [
                "margin excl. VAT",
                "% margin excl. VAT",
            ]
        )
        
        cDf = st.session_state.processed_df[column_order]
        
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            cDf.to_excel(writer, sheet_name='Sheet1', index=True)
        return output.getvalue()
            
            
        
        
        
        