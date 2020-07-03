import pandas as pd


# wrangling functions

def merge_tables_from_db(lst):
    # ----- Merge tables from databse -----
    print('Merging tables...')
    merge_1 = pd.merge(lst[0], lst[1], how='inner', on='uuid')
    merge_2 = pd.merge(merge_1, lst[2], how='inner', on='uuid')
    tables_merged_raw = pd.merge(merge_2, lst[3], how='inner', on='uuid')
    tables_merged_raw.rename(columns={'age': 'Age (years)'}, inplace=True)

    # ----- Filter only rows with job -----
    filter_jobs = ~tables_merged_raw['normalized_job_code'].isnull()
    table_merged_raw = tables_merged_raw[filter_jobs].reset_index()

    # ----- Clean Age column -----
    for i in range(len(table_merged_raw)):
        if 'years' in table_merged_raw.loc[i, 'Age (years)']:
            table_merged_raw.loc[i, 'Age (years)'] = int(table_merged_raw.loc[i, 'Age (years)'].replace(' years old', ''))
        else:
            table_merged_raw.loc[i, 'Age (years)'] = 2016 - int(table_merged_raw.loc[i, 'Age (years)'])

    # ----- Export table merged to CSV -----
    table_merged_raw.to_csv(f'data/processed/01_table_from_db.csv')

    return table_merged_raw

def final_table (lst, table_2, dic):
    # ----- Merging table from database with table from API -----
    table_final_merge = pd.merge(merge_tables_from_db(lst), table_2, how='left', left_on='normalized_job_code', right_on='job_uuid')

    # ----- New column Country with the name of the country according the code -----
    table_final_merge['Country'] = [dic[f'{country}'] for country in table_final_merge['country_code']]
    print('Merging completed')

    # ----- Final table with desired columns -----
    table = table_final_merge[['Country', 'title', 'Age (years)']]

    # ----- Export table clean to CSV -----
    table.to_csv(f'data/processed/02_table_merged_clean.csv')

    return table
