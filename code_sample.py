import pandas as pd
import os
import datetime
import pandas_datareader.data as web
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import us

PATH = r'/Users/ally/Documents/GitHub/iija-on-unemployment-rate'

def iija_funding_summary():
    df_iija = pd.read_excel(os.path.join(PATH, 'iija_projects.xlsx'))
    df_iija['FUNDING'] = pd.to_numeric(df_iija['FUNDING'].replace('[\$,]', '', regex=True), errors='coerce')
    funding_summary = df_iija.groupby('STATE NAME')['FUNDING'].sum().reset_index()
    return funding_summary

# variable to toggle going on the web on and off (True = local, False: web)
USE_LOCAL_DATA = True

def abbr_to_name(abbr):
    state = us.states.lookup(abbr)
    return state.name if state else None

def find_ur_data(append, path, use_local=False):
    start = datetime.date(year=2021, month=1, day=1)
    end = datetime.date(year=2022, month=12, day=31)
    states = [state.abbr for state in us.states.STATES if state.abbr != "DC"]

    if use_local:
        df_ur = pd.read_csv(os.path.join(path, 'unemployment_21_22.csv'))
        df_ur['DATE'] = pd.to_datetime(df_ur['DATE'])
        df_ur = df_ur.query('@start <= DATE <= @end')
        df_ur['STATE'] = df_ur['STATE'].apply(abbr_to_name)
        return df_ur.dropna()
    else:
        states_appended = [f"{state}{append}" for state in states]
        all_states_df = web.DataReader(states_appended, 'fred', start, end)
        all_states_df = all_states_df.reset_index().melt(id_vars=['DATE'], var_name='STATE', value_name=append)
        all_states_df['STATE'] = all_states_df['STATE'].str.replace(append, '')
        all_states_df['STATE'] = all_states_df['STATE'].apply(abbr_to_name)
        return all_states_df.dropna()


def calculate_percentage_change(df, df2, state, rate, date):
    df[date] = pd.to_datetime(df[date])
    df['YEAR'] = df[date].dt.year
    annual_data = df.pivot_table(index=state, columns='YEAR', values=rate, aggfunc='mean')
    annual_data['2021_2022_Change'] = ((annual_data[2022] - annual_data[2021]) / annual_data[2021]) * 100
    annual_data.reset_index()
    merged_df = pd.merge(df2, annual_data, left_on='STATE NAME', right_on='STATE', how='inner')
    return merged_df.reset_index()

def regression(df, x_column, y_column):
    X = df[x_column]
    y = df[y_column]
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    return model

def plot_regression(df, x_column, y_column):
    sns.set_style('whitegrid')
    plt.figure(figsize=(8, 6))
    sns.regplot(x=x_column, y=y_column, data=df, scatter_kws={'alpha': 0.5}, line_kws={'color': 'red'})
    plt.xlabel('IIJA Funding ($)')
    plt.ylabel('Unemployment Rate Change 2021-2022 (%)')
    plt.title('Impact of IIJA Funding on Changes in Unemployment Rate')
    plt.savefig(os.path.join(PATH, 'iija_on_unemployment.png'))
    return plt

iija_by_state = iija_funding_summary()
df_ur = find_ur_data('UR', PATH, use_local=USE_LOCAL_DATA)
ur_change_iija = calculate_percentage_change(df_ur, iija_by_state, 'STATE', 'UR', 'DATE')
model_iija = regression(ur_change_iija, 'FUNDING', '2021_2022_Change')
print("\nRegression Statistics for Impact of IIJA Funding on Changes in Unemployment Rate:")
print(model_iija.summary())
plot_regression(ur_change_iija, 'FUNDING', '2021_2022_Change')
