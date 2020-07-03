# Data Project README file

This is the first project, corresponding to module 1 of the Data Analytics Bootcamp at Ironhack Madrid.

It is a project focused on the acquisition, clean and merge of data.
The data is acquired from diferents places:
- Databases.
- Web APIs.
- Web scraping.

## **Requirements**

`python==3.7`
`pandas`
`requests`
`sqlalchemy`
`beautiful soup 4`
`argparse`


## **Data**

- **Tables (.db).** [Here](http://www.potacho.com/files/ironhack/raw_data_project_m1.db) you can find the `.db` file with the main dataset.

- **API.** API from the [Open Skills Project](http://dataatwork.org/data/).  

- **Web Scraping.** Information about country codes from [Eurostat](https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Country_codes) website.


## **How to run it**

The script `main_script.py` has 2 parameters to play with:
	
	("-c", "--country", type=str, default='All', help="Introduce the name of the country or All for all countries...")
    ("-up", "--updt", type=str, help="True to update jobs information from api")
	
To run the script for the first time it is highly recommended `-up True` to get the jobs information updated from the API.




## **Start writing ASAP:**
*Last but not least, by writing your README soon you give yourself some pretty significant advantages. Most importantly, you’re giving yourself a chance to think through the project without the overhead of having to change code every time you change your mind about how something should be organized or what should be included.*


### :file_folder: **Folder structure**
```
└── project
    ├── __trash__
    ├── .gitignore
    ├── .env
    ├── requeriments.txt
    ├── README.md
    ├── main_script.py
    ├── notebooks
    │   └── test_main_code.ipynb
    ├── p.acquisition
    │   ├── __init__.py
    │   └── m.acquisition.py
    ├── p.analysis
    │   ├── __init__.py
    │   └── m.analysis.py
    ├── p.reporting (developing...)
    │   ├── __init__.py
    │   └── m.reporting.py
    ├── p.wrangling
    │   ├── __init__.py
    │   └── m.wrangling.py
    └── data
        ├── raw
        ├── processed
        └── results
```

