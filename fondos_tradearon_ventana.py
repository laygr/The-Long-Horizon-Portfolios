import datetime
import pandas as pd

def fondos_que_tradearon_en_ventana(df, tamanio_ventana, minimo=0.99):
    base_date = df.index[0]
    dias_totales = len(df)
    acum = []
    for offset in range(0, dias_totales - tamanio_ventana):
        start_date = base_date + datetime.timedelta(days=offset)
        end_date = start_date + datetime.timedelta(days=tamanio_ventana)
        mask = (df.index >= pd.to_datetime(start_date)) & (df.index <= pd.to_datetime(end_date))
        ventana_df = df[mask]
        filas = len(ventana_df)
        count = (ventana_df.count(axis=0) >= filas * minimo).sum()
        acum.append([start_date, count])
    result = pd.DataFrame(acum, columns=['Date', 'Fondos'])
    result = result.set_index('Date')
    return result