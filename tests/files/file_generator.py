import pandas as pd


# Valid Setup
df = pd.DataFrame(
    {
        "length": [1, 2, 3],
        "width": [1, 2, 3],
        "height": [1, 2, 3],
        "weight": [1, 2, 3],
        "selling price": [10, 20, 30],
        "buying price": [1, 2, 3],
        "vat": [1, 2, 3],
        "perishable": [True, False, True],
        "fragile": [True, False, True],
        "labeling": [True, False, True],
        "storage winter": [True, False, True],
        "storage duration": [1, 2, 3],
        "product name": "Television",
        "product group": "TV and Audio - Television",
    }
)   

df.to_excel("tests/files/valid_setup.xlsx", index=False)



# Missing length
df = pd.DataFrame(
    {
        #"length": [1, 2, 3],
        "width": [1, 2, 3],
        "height": [1, 2, 3],
        "weight": [1, 2, 3],
        "selling price": [10, 20, 30],
        "buying price": [1, 2, 3],
        "vat": [1, 2, 3],
        "perishable": [True, False, True],
        "fragile": [True, False, True],
        "labeling": [True, False, True],
        "storage winter": [True, False, True],
        "storage duration": [1, 2, 3],
        "product name": "Television",
        "product group": "TV and Audio - Television",
    }
)   

df.to_excel("tests/files/missing_length.xlsx", index=False)


# Missing length & Fragile
df = pd.DataFrame(
    {
        #"length": [1, 2, 3],
        "width": [1, 2, 3],
        "height": [1, 2, 3],
        "weight": [1, 2, 3],
        "selling price": [10, 20, 30],
        "buying price": [1, 2, 3],
        "vat": [1, 2, 3],
        "perishable": [True, False, True],
        #"fragile": [True, False, True],
        "labeling": [True, False, True],
        "storage winter": [True, False, True],
        "storage duration": [1, 2, 3],
        "product name": "Television",
        "product group": "TV and Audio - Television",
    }
)   

df.to_excel("tests/files/missing_length_and_fragile.xlsx", index=False)


# Missing length & Fragile & labeling
df = pd.DataFrame(
    {
        #"length": [1, 2, 3],
        "width": [1, 2, 3],
        "height": [1, 2, 3],
        "weight": [1, 2, 3],
        "selling price": [10, 20, 30],
        "buying price": [1, 2, 3],
        "vat": [1, 2, 3],
        "perishable": [True, False, True],
        #"fragile": [True, False, True],
        #"labeling": [True, False, True],
        "storage winter": [True, False, True],
        "storage duration": [1, 2, 3],
        "product name": "Television",
        "product group": "TV and Audio - Television",
    }
)   

df.to_excel("tests/files/missing_length_and_fragile_and_labeling.xlsx", index=False)


# Not transformable entry, excluding column?
df = pd.DataFrame(
    {
        "length": [1, 2, 3],
        "width": [1, 2, 3],
        "height": [1, 2, 3],
        "weight": [1, 2, 3],
        "selling price": [10, 20, 30],
        "buying price": [1, 2, 3],
        "vat": [1, 2, 3],
        "perishable": [True, False, True],
        "fragile": [True, False, True],
        "labeling": [True, False, True],
        "storage winter": [True, "Jey", True],
        "storage duration": [1, 2, 3],
        "product name": "Television",
        "product group": "TV and Audio - Television",
    }
)   

df.to_excel("tests/files/winter_storage_not_transformable.xlsx", index=False)



# Wrong Product Group 
df = pd.DataFrame(
    {
        "length": [1, 2, 3],
        "width": [1, 2, 3],
        "height": [1, 2, 3],
        "weight": [1, 2, 3],
        "selling price": [10, 20, 30],
        "buying price": [1, 2, 3],
        "vat": [1, 2, 3],
        "perishable": [True, False, True],
        "fragile": [True, False, True],
        "labeling": [True, False, True],
        "storage winter": [True, False, True],
        "storage duration": [1, 2, 3],
        "product name": "Television",
        "product group": ["TV and Audio - Television", "TV and Audio - Television", "TV and Audio - Television2"],
    }
)   

df.to_excel("tests/files/invalid_product_group.xlsx", index=False)


# Defaults
df = pd.DataFrame(
    {
        "length": [1, 2, 3],
        "width": [1, 2, 3],
        "height": [1, 2, 3],
        "weight": [1, 2, 3],
        "selling price": [10, 20, 30],
        "buying price": [1, 2, 3],
        "storage winter": [True, False, True],
        "storage duration": [1, 2, 3],
        "product name": "Television",
        "product group": ["TV and Audio - Television", "TV and Audio - Television", "TV and Audio - Television"],
    }
)   

df.to_excel("tests/files/defaults_missing.xlsx", index=False)


# Wrong VAT Range
df = pd.DataFrame(
    {
        "length": [1, 2, 3],
        "width": [1, 2, 3],
        "height": [1, 2, 3],
        "weight": [1, 2, 3],
        "selling price": [10, 20, 30],
        "buying price": [1, 2, 3],
        "vat": [0.1, 0.21, 0.19],
        "perishable": [True, False, True],
        "fragile": [True, False, True],
        "labeling": [True, False, True],
        "storage winter": [True, False, True],
        "storage duration": [1, 2, 3],
        "product name": "Television",
        "product group": "TV and Audio - Television",
    }
)   

df.to_excel("tests/files/vat_wrong_range.xlsx", index=False)


# Wrong VAT Range
df = pd.DataFrame(
    {
        "length": [1, 2, 3],
        "width": [1, 2, 3],
        "height": [1, 2, 3],
        "weight": [1, 2, 3],
        "selling price": [10, 20, 30],
        "buying price": [1, 2, 3],
        "vat": [0.1, 21, 0.19],
        "perishable": [True, False, True],
        "fragile": [True, False, True],
        "labeling": [True, False, True],
        "storage winter": [True, False, True],
        "storage duration": [1, 2, 3],
        "product name": "Television",
        "product group": "TV and Audio - Television",
    }
)   

df.to_excel("tests/files/vat_wrong_range2.xlsx", index=False)


# Correct VAT Range
df = pd.DataFrame(
    {
        "length": [1, 2, 3],
        "width": [1, 2, 3],
        "height": [1, 2, 3],
        "weight": [1, 2, 3],
        "selling price": [10, 20, 30],
        "buying price": [1, 2, 3],
        "vat": [21, 21, 19],
        "perishable": [True, False, True],
        "fragile": [True, False, True],
        "labeling": [True, False, True],
        "storage winter": [True, False, True],
        "storage duration": [1, 2, 3],
        "product name": "Television",
        "product group": "TV and Audio - Television",
    }
)   

df.to_excel("tests/files/correct_vat.xlsx", index=False)


# Exclude all
df = pd.DataFrame(
    {
        "length": [-1, 2, 3],
        "width": [1, -2, 3],
        "height": [1, 2, -3],
        "weight": [1, 2, 3],
        "selling price": [10, 20, 30],
        "buying price": [1, 2, 3],
        "vat": [21, 21, 19],
        "perishable": [True, False, True],
        "fragile": [True, False, True],
        "labeling": [True, False, True],
        "storage winter": [True, False, True],
        "storage duration": [1, 2, 3],
        "product name": "Television",
        "product group": "TV and Audio - Television",
    }
)   

df.to_excel("tests/files/exclude_all_entries.xlsx", index=False)


# No Product Group
df = pd.DataFrame(
    {
        "length": [1, 2, 3],
        "width": [1, 2, 3],
        "height": [1, 2, 3],
        "weight": [1, 2, 3],
        "selling price": [10, 20, 30],
        "buying price": [1, 2, 3],
        "vat": [1, 2, 3],
        "perishable": [True, False, True],
        "fragile": [True, False, True],
        "labeling": [True, False, True],
        "storage winter": [True, False, True],
        "storage duration": [1, 2, 3],
        "product name": ["baby phone 3000", "Soccer Ball", "Television"],
    }
)   

df.to_excel("tests/files/valid_without_product_group.xlsx", index=False)



