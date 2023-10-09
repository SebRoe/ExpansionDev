import pandas as pd
from bol.constants.commissions import PRODUCT_GROUPS
from bol.enums import ValidationMessages, DestinationCountry
from utils.loader import load_model

class DataValidator:
    def __init__(self):
        self.columns = [
            # Column Name, Type, Required, Default,
            ("length", float, True, None),
            ("width", float, True, None),
            ("height", float, True, None),
            ("weight", float, True, None),
            ("selling price incl. vat", float, True, None),
            ("buying price excl. vat", float, True, None),
            ("vat", float, False, 21.0),
            ("perishable", bool, False, False),
            ("fragile", bool, False, False),
            ("labeling", bool, False, False),
            ("storage winter", bool, False, False),
            ("storage duration", int, False, 1),
            ("delivery destination", DestinationCountry, False, "NL")
        ]

        self.special_treatment = [
            ("product group", "product name"),
        ]

        self.excluded_ids = []

    def validate_uploaded_file(self, df: pd.DataFrame):
        df.columns = df.columns.str.lower()

        
        change_log = {}
        attr_mismatch= []
        column_not_found = []
        column_not_transformable = []
        
        excluded_rows = set()

        for name, type, required, default in self.columns:
            
            
            
            # Check if column exists and set if default is given
            if required and name not in df.columns:
                column_not_found.append(name)
                continue

            elif not required and name not in df.columns:
                df[name] = default
                change_log[name] = f"Column {name} not found, filled with default value {default}."


            # Check for None Values and fill with default if given
            if df[name].isnull().values.any():
                nan_indices = df[df[name].isnull()].index

                if default is None:
                    excluded_rows.update(nan_indices)
                    attr_mismatch.extend(
                        [
                            (name, i, ValidationMessages.NONE_VALUE.value)
                            for i in nan_indices
                        ]
                    )
                else:
                    df.loc[nan_indices, name] = default
                    change_log[name] = f"Column {name} contains None Values, rows with None Values are filled with default value {default}."


            # Check if column can be transformed to given type
            try:
                if type == bool:
                    df[name] = df[name].astype(int).astype(bool)
                elif type == DestinationCountry:
                    # Check if all are convertable
                    df[name] = df[name].apply(lambda x: DestinationCountry.from_string(x.strip()).value[1])
                else:
                    df[name] = df[name].astype(type)
            except Exception as e:
                column_not_transformable.append((name, e))
                continue

            # Check for negative values in numeric columns
            if type in [int, float]:
                invalid_indices = df[df[name] < 0].index.tolist()
                if invalid_indices:
                    attr_mismatch.extend(
                        [
                            (name, i, ValidationMessages.NEGATIVE_VALUE.value)
                            for i in invalid_indices
                        ]
                    )
                    excluded_rows.update(invalid_indices)
                    
                    
                        
            if name == "vat":
                
                if df[name].between(0, 1).all():
                    df[name] = df[name] * 100
                    change_log[name + "_range"] = f"VAT Range (0, 1) found. Values were multiplied by 100."
                
                elif df[name].between(0,0.999).any() and df[name].between(1,100).any():
                    change_log[name + "_range"] = f"Found VAT Range (0, 1) and (1, 100). Please check if this is correct."


                invalid_indices = df[~df[name].between(0, 100)].index.tolist()
                if invalid_indices:
                    attr_mismatch.extend(
                        [
                            (name, i, ValidationMessages.INVALID_VAT_RANGE.value)
                            for i in invalid_indices
                        ]
                    )
                    excluded_rows.update(invalid_indices)
                        
                    

        return self._validate_special_columns(
            df,
            {
                "changes": change_log,
                "attr_mismatch": attr_mismatch,
                "column_not_found": column_not_found,
                "column_not_transformable": column_not_transformable,
                "excluded_rows": excluded_rows,
            },
        )

    def _validate_special_columns(self, df: pd.DataFrame, log: dict):
        
        if "product group" in df.columns:
            df["product group"] = df["product group"].astype(str).str.strip()
            # iterate over the whole column: id, value
            for id, value in df["product group"].items():
                if value in PRODUCT_GROUPS:
                    pass
                else:
                    log["attr_mismatch"].append(
                        ("product group", id, ValidationMessages.INVALID_PRODUCT_GROUP.value)
                    )
                    log["excluded_rows"].add(id)

        elif "product name" in df.columns and not "product group" in df.columns:
            classifier = load_model()

            # Predict the whole column
            df["product name"] = df["product name"].astype(str).str.strip()
            names = df["product name"].values.tolist()
            groups = []
            for name in names:
                label, proba, top4_labels, top4_probas = classifier.predict(name)
                groups.append(label)

            df["product group"] = groups

        else:
            log["column_not_found"].append("product group")
            log["column_not_found"].append("product name")
            
            
        if "selling price" in df.columns and "buying price" in df.columns:
            # Check if selling price is lower than buying price 
            invalid_indices = df[df["selling price"] < df["buying price"]].index.tolist()
            if invalid_indices:
                log["attr_mismatch"].extend(
                    [
                        ("selling price", i, ValidationMessages.INVALID_SELLING_PRICE.value)
                        for i in invalid_indices
                    ]
                )
                log["excluded_rows"].update(invalid_indices)
            
            
            
        

        return self._finalize_validation(df, log)

    def _finalize_validation(self, df: pd.DataFrame, logs: dict):
        """Drop excluded rows and return the final dataframe"""
        df.drop(index=logs["excluded_rows"], inplace=True)
        return df, logs
