FORMATS = {
    "XXXS": {
        "length": 25.5,
        "width": 16.5,
        "height": 3,
        "weight": 1,
    },
    "XXS": {
        "length": 37.5,
        "width": 26,
        "height": 3,
        "weight": 2,
    },
    "XS": {
        "length": 37.5,
        "width": 26,
        "height": 5,
        "weight": 5,
    },
    "S": {
        "length": 45,
        "width": 30,
        "height": 8,
        "weight": 5,
    },
    "M": {
        "length": 55,
        "width": 35,
        "height": 20,
        "weight": 8,
    },
    "L": {
        "length": 72,
        "width": 50,
        "height": 41,
        "weight": 15,
    },
}

COSTS_PER_FORMAT = {
    "XXXS": {
        "cost_per_article": 1.3,
        "cost_per_delivery": 1.07,
        "total_cost": 2.37,
        "storage_cost_per_month": 0.13,
    },
    "XXS": {
        "cost_per_article": 1.39,
        "cost_per_delivery": 1.63,
        "total_cost": 3.02,
        "storage_cost_per_month": 0.14,
    },
    "XS": {
        "cost_per_article": 1.58,
        "cost_per_delivery": 2.92,
        "total_cost": 4.5,
        "storage_cost_per_month": 0.23,
    },
    "S": {
        "cost_per_article": 1.99,
        "cost_per_delivery": 3.38,
        "total_cost": 5.37,
        "storage_cost_per_month": 0.45,
    },
    "M": {
        "cost_per_article": 2.1,
        "cost_per_delivery": 3.42,
        "total_cost": 5.52,
        "storage_cost_per_month": 0.6,
    },
    "L": {
        "cost_per_article": 2.81,
        "cost_per_delivery": 3.73,
        "total_cost": 6.54,
        "storage_cost_per_month": 0.9,
    },
}

STORAGE_COSTS_WINTER_HOLIDAYS = {
    "XXXS": 0.18,
    "XXS": 0.20,
    "XS": 0.32,
    "S": 0.63,
    "M": 0.84,
    "L": 1.26,
    "XL": 3.36,
    "XXL": 3.89,
}

ADDITIONAL_COSTS = {
    "fragile": 0.35,
    "perishable": 0.35,
    "label": 0.18,
    "label_unordered": 0.23,
    "recall": 0.4,
    "destruction": 0.4,
}


RETRIEVAL_AND_SHIPPING_COSTS = {
    "shipping_costs": {
        "Netherlands": {
            "5kg": 4.6,
            "10kg": 5.6,
            "20kg": 6.6,
            "25kg": 7.6,
        },
        "Belgium": {
            "5kg": 4.6,
            "10kg": 5.6,
            "20kg": 6.6,
            "25kg": 7.6,
        },
    },
    "bulk_shipping_costs": {
        "Netherlands": {
            "1": 40.0,
            "2": 32.0,
            "3": 30.0,
            "4_and_more": 28.0,
        },
        "Belgium": {
            "1": 46.0,
            "2": 46.0,
            "3": 46.0,
            "4_and_more": 46.0,
        },
    },
}