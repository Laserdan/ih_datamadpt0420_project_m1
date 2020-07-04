import pandas as pd
import requests
import itertools
import re
from sqlalchemy import create_engine
from bs4 import BeautifulSoup


def acquire_db(path):
    # ----- Connection to database -----
    engine = create_engine(f'sqlite:///{path}')
    return engine


def get_table_from_db(table_name, path):
    # ----- Get tables from a database -----
    table_name = pd.read_sql_query(f'SELECT * FROM {table_name}', acquire_db(path))
    return table_name


def get_tables(path):
    print('Connecting to database...')
    # ----- Get the name of all the tables of the database -----
    db_tables_names = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name",
                                        acquire_db(path))

    # ----- Get all tables from database -----
    tables = [get_table_from_db(table, path) for table in db_tables_names['name']]

    # ----- Export tables as CSV -----
    name = 'name'
    [tables[i].to_csv(f'data/raw/00_{db_tables_names.loc[i, name]}.csv') for i in range(len(tables))]

    print('Acquisition completed')
    return tables


def get_jobs(api, updt):
    if updt == 'True':
        return get_jobs_api(api)
    else:
        return get_jobs_csv()


def get_jobs_csv():
    print('Reading jobs.csv from cache...')
    jobs_df = pd.read_csv(f'data/raw/jobs.csv')
    print('Jobs information acquired')
    return jobs_df


def get_jobs_api(api):
    print('Connecting to api.dataatwork.org...\nGetting jobs information...')

    # ----- Make API connection -----
    response = requests.get(api)

    # ----- Get number of jobs to automatize the request -----
    json_data = response.json()
    number_of_jobs = int(json_data[1]['links'][3]['href'].replace('/jobs?offset=', '').replace('&limit=1', ''))
    number_of_requests = number_of_jobs // 500
    last_request = number_of_jobs % 500

    # ----- Make the requests -----
    response_500s = [requests.get(f'http://api.dataatwork.org/v1/jobs?offset={500 * (request - 1)}&limit=500') for
                     request in range(number_of_requests)]
    response_last = requests.get(f'http://api.dataatwork.org/v1/jobs?offset={number_of_jobs - last_request}&limit=500')

    # ----- Get jsons from requests -----
    json_data_500s = [response.json()[:-1] for response in response_500s]
    json_data_last = response_last.json()[:-1]

    # ----- Flatten and join -----
    json_data_500s_flat = list(itertools.chain(*json_data_500s))
    json_data = json_data_500s_flat + json_data_last  # ---->  List of all jobs

    jobs_df = pd.DataFrame(json_data)
    jobs_df = jobs_df.rename(columns={'uuid': 'job_uuid'})

    # ----- Export df to CSV -----
    jobs_df.to_csv(f'data/raw/jobs.csv')

    print('Jobs information acquired')
    return jobs_df


def get_countries(url):
    print('Getting country codes...')

    # ----- Connection to web -----
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'lxml')

    # ----- Getting all tables from web -----
    tables = soup.find_all('table')

    # ----- Scraping country codes from web -----
    countries_raw = [table.find_all('td') for table in tables]
    countries_flatted = list(itertools.chain(*countries_raw))

    # ----- Cleaning the output -----
    countries = [country.text.replace('\n', '') for country in countries_flatted]
    countries_clean = [country for country in countries if country != '' and country != ' \xa0']
    countries_clean = [re.sub('\[[0-9]\]', '', country).replace('*', '') for country in countries_clean]

    # ----- Make a dict {country_code: country_name} -----
    countries_names = [country.strip() for country in countries_clean[::2]]
    countries_codes = [country.replace('(', '').replace(')', '').strip() for country in countries_clean[1::2]]
    countries_dict = {countries_codes[i]: countries_names[i] for i in range(len(countries_names))}

    # ----- Adding exceptions -----
    countries_dict['GB'] = countries_dict['UK']
    countries_dict['GR'] = countries_dict['EL']

    print('Country codes acquired')
    return countries_dict
