import pandas as pd

def aggregate_date(df):
    
    df['date'] = pd.to_datetime(df['date'])
    
    pub_list = df['publication'].unique()
    
    df_distrib = resample(df,pub_list)

    df_distrib = df_distrib.rename(columns={"publication": "value"})
    df_distrib = df_distrib.reset_index(level=['date', 'publication'])
    df_distrib = df_distrib.drop_duplicates()
    df_distrib['date'] = df_distrib['date'].apply(lambda x: x.strftime("%Y-%m-%d"))

    return df_distrib



def resample(df,pub_list):

  df_main = pd.DataFrame()

  for publication in pub_list:

    df_year = df.set_index(['date']).groupby([pd.Grouper(freq='Y'), 'publication']).count()
    df_year['agg'] = 'year'
    
    df_month = df.set_index(['date']).groupby([pd.Grouper(freq='M'), 'publication']).count()
    df_month['agg'] = 'month'

    df_day = df.set_index(['date']).groupby([pd.Grouper(freq='D'), 'publication']).count()
    df_day['agg'] = 'day'

    df_main = pd.concat([df_main, df_year,df_month,df_day])
    print(df_main)
  
  return df_main
  





