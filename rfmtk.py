# rfmtk.py: Python RMF analytics toolkit
def rfm(data, user_id, today, date, checkout_id, price):
    # user_id: User ID column for group-by aggregation
    # today: E.g. '2016/04/01'
    # date: Date column for calculating recency
    # checkout_id: Checkout column for calculating frequency
    # price: Proce column for calculating monetary
    import pandas as pd

    today = pd.to_datetime(today)
    
    recency_df = (data[data[user_id].notnull()]
                  .groupby(user_id)[date]
                  .agg([('recency', lambda x: (today - pd.to_datetime(x).max()).days)])
                  .reset_index())
    
    frequency_df = (data[data[user_id].notnull()]
                    .groupby(user_id)[checkout_id]
                    .agg([('frequency', 'nunique')])
                    .reset_index())

    monetary_df = (data[data[user_id].notnull()]
                   .groupby(user_id)[price]
                   .agg([('monetary', lambda x: x.sum())])
                   .reset_index())
    
    rfm_df0 = pd.merge(recency_df, frequency_df, on=user_id)
    rfm_df = pd.merge(rfm_df0, monetary_df, on=user_id)
    
    return(rfm_df)

