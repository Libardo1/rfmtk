# rfmtk.py: Python RMF analytics toolkit
import pandas as pd

def rfm(df, today, date, checkout_id, price, user_id='member_id'):
    """
    Args:
        df: DataFrame with columns: user_id, date, checkout_id, price.
        today: E.g. '2016/04/01'.
        user_id: User ID column for group-by aggregation.
        date: Date column for calculating recency.
        checkout_id: Checkout column for calculating frequency.
        price: Proce column for calculating monetary.
    
    Returns:
        rfm_df: DataFrame with columns user_id, recency, frequency and monetary.
    """
    
    df1 = df.loc[:, [user_id, date, checkout_id, price]]
    df1.columns = ['user_id', 'date', 'checkout_id', 'price']
    
    today = pd.to_datetime(today)
    
    recency_df = (df1[df1.user_id.notnull()]
                  .groupby('user_id')['date']
                  .agg([('recency', lambda x: (today - pd.to_datetime(x).max()).days)])
                  .reset_index())
    
    frequency_df = (df1[df1.user_id.notnull()]
                    .groupby('user_id')['checkout_id']
                    .agg([('frequency', 'nunique')])
                    .reset_index())

    monetary_df = (df1[df1.user_id.notnull()]
                   .groupby('user_id')['price']
                   .agg([('monetary', lambda x: x.sum())])
                   .reset_index())
    
    rfm_df0 = pd.merge(recency_df, frequency_df, on='user_id')
    rfm_df = pd.merge(rfm_df0, monetary_df, on='user_id')
    
    return(rfm_df)

