def quitar_si_columna_en_lista(df, columna, lista):
    print('quitar_si_columna_en_lista', columna, lista)
    mask = ~df[columna].str.lower().isin(lista)
    df = df[mask]
    print('Quedan: ', len(df))
    return df

def quitar_si_condicion_y_columna_en_lista(df, columna_condicion, columna, lista):
    print('quitar_si_condicion_y_columna_en_lista', columna_condicion, columna, lista)
    estan_en_lista = df[columna].str.lower().isin(lista)
    y_cumplen_condicion = (estan_en_lista) & (df[columna_condicion])
    df = df[~y_cumplen_condicion]
    print('Quedan: ', len(df))
    return df

def quitar_si_columna_contiene(df, columna, patron):
    print('quitar_si_columna_contiene', columna, patron)
    df = df[~df[columna].str.lower().str.contains(patron)]
    print('Quedan: ', len(df))
    return df

def quitar_si_columna_mayor_a(df, columna, valor):
    print('quitar_si_columna_mayor_a', columna, valor)
    df = df[~(df[columna] > valor)]
    print('Quedan: ', len(df))
    return df