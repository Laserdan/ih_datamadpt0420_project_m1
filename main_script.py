import argparse

from p_acquisition import m_acquisition
from p_wrangling import m_wrangling
from p_analysis import m_analysis
from p_reporting import m_reporting

def argument_parser():
    parser = argparse.ArgumentParser(description = 'Specify country, path, url to scrap, api and update jobs information')
    parser.add_argument("-c", "--country", type=str, default='All', help="Introduce the name of the country or All for all countries...")
    parser.add_argument("-p", "--path", type=str, default='data/raw/raw_data_project_m1.db' , help="specify .db database path")
    parser.add_argument("-u", "--url", type=str, default='https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Country_codes', help="specify url of web to be scraped")
    parser.add_argument("-a", "--api", type=str, default='http://api.dataatwork.org/v1/jobs?offset=0&limit=1', help="specify url of API")
    parser.add_argument("-up", "--updt", type=str, help="True to update jobs information from api")
    args = parser.parse_args()
    return args


def main(args):
    print('starting pipeline...\n---------------------')
    tables_from_db = m_acquisition.get_tables(args.path)
    jobs_api = m_acquisition.get_jobs(args.api, args.updt)
    country_codes_dic = m_acquisition.get_countries(args.url)
    final = m_wrangling.final_table(tables_from_db, jobs_api, country_codes_dic)
    analysis = m_analysis.analyze(final, args.country)
    print('\n',analysis)
    print('\n========================= Pipeline is complete. You may find the results in the folder ./data/results =========================')


if __name__ == '__main__':
    arguments = argument_parser()
    main(arguments)