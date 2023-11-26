DATA_DIR = './datasets'
EXTERNAL_STYLESHEETS = ['/assets/home.css']

DELIMITER_OPTIONS={
    ';':';',
    ',':',',
    "' '":""
}

DECIMAL_OPTIONS={
    ',':',',
    '.':'.'
}

ENCODING_OPTIONS={
    'Latin 1':'latin-1',
    'UTF-8':'utf-8'
}

DATASET_MENU_DROPDOWN=[
    {
        "title": "Delimiter",
        "options": DELIMITER_OPTIONS,
        "placeholder": "Select a delimiter",
        "id":"delimiter-list"
    },
    {
        "title": "Decimal",
        "options": DECIMAL_OPTIONS,
        "placeholder": "Select a decimal",
        "id":"decimal-list"
    },
    {
        "title": "Encoding",
        "options":ENCODING_OPTIONS,
        "placeholder": "Select a encoding",
        "id":"encoding-list"
    }
]