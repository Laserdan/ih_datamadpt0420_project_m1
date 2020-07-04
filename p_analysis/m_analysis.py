import pandas as pd

# analysis functions

def quant(table):
    # ----- Aggrupation and count of same values -----
    table_qt = pd.DataFrame(table.groupby(['Country', 'title', 'Age (years)']).size()).reset_index().set_index('Country')
    table_qt.rename(columns={'title': 'Job Title', 0: 'Quantity'}, inplace=True)
    return table_qt

def perc(table):
    # ----- New column with the % of quantity -----
    table_perc = table
    table_perc['Percentage'] = 100 * table_perc['Quantity'] / len(table_perc)
    return table_perc

def analyze(table, country):
    # ----- Add quantity and % to the table -----
    table_qt = quant(table)
    table_to_analyze = perc(table_qt)
    countries = list(table_to_analyze.index.unique())

    # ----- Filter by country or all -----
    if country in countries:
        table_to_analyze.loc[country].to_csv(f'data/results/results_{country}.csv') # ----- Export results as CSV -----
        return table_to_analyze.loc[country]
    elif country == 'All':
        table_to_analyze.to_csv(f'data/results/results.csv')  # ----- Export results as CSV -----
        return table_to_analyze
    else:
        return f'\nCountry not recognized\n\nIntroduce one of these countries: {countries}'
