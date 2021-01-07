def quitar_si_columna_en_lista(df, columna, lista, short_description, removed_acum):
    print('quitar_si_columna_en_lista', columna, lista)
    mask = ~df[columna].str.lower().isin(lista)

    removed = [[ticker, short_description] for ticker in df[~mask]['TICKER'].values]
    removed_acum.extend(removed)

    df = df[mask]
    print('Quedan: ', len(df))
    return df

def quitar_si_condicion_y_columna_en_lista(df, columna_condicion, columna, lista, short_description, removed_acum):
    print('quitar_si_condicion_y_columna_en_lista', columna_condicion, columna, lista)
    estan_en_lista = df[columna].str.lower().isin(lista)
    mask = ~((estan_en_lista) & (df[columna_condicion]))
    
    removed = [[ticker, short_description] for ticker in df[~mask]['TICKER'].values]
    removed_acum.extend(removed)

    df = df[mask]
    print('Quedan: ', len(df))
    return df

def quitar_si_columna_contiene(df, columna, patron, short_description, removed_acum):
    print('quitar_si_columna_contiene', columna, patron)
    mask = ~df[columna].str.lower().str.contains(patron)

    removed = [[ticker, short_description] for ticker in df[~mask]['TICKER'].values]
    removed_acum.extend(removed)

    df = df[mask]
    print('Quedan: ', len(df))    
    return df

def quitar_si_columna_mayor_a(df, columna, valor, short_description, removed_acum):
    print('quitar_si_columna_mayor_a', columna, valor)
    mask = ~(df[columna] > valor)

    removed = [[ticker, short_description] for ticker in df[~mask]['TICKER'].values]
    removed_acum.extend(removed)

    df = df[mask]
    print('Quedan: ', len(df))
    return df

def quitar_seleccionados_manualmente(df, df_seleccion, removed_acum):
    df = df.set_index('TICKER')
    df_seleccion = df_seleccion[df_seleccion['Dudoso'] == False]
    df_seleccion = df_seleccion.loc[df_seleccion.index.intersection(df.index)]
    df_seleccion['Justificación'] = df_seleccion['Justificación'].fillna('No especificado')
    df_seleccion = df_seleccion.set_index('TICKER')
    filtered_tickers = df.index.difference(df_seleccion.index)
    df = df.loc[filtered_tickers]
    removed = [[ticker, row['Justificación']] for ticker, row in df_seleccion.iterrows()]
    removed_acum.extend(removed)
    return df.reset_index()