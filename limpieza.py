import tipos_filtros as filtros
import pandas as pd

def limpiar(metadatos_df, quitados_manualmente_df, sin_repetidos_df):
    tickers_originales = set(metadatos_df['TICKER'])
    # APLICAR FILTROS A METADATOS
    #   Rellenar vacios
    metadatos_df['FUND_ASSET_ALLOC_GOVT'] = metadatos_df['FUND_ASSET_ALLOC_GOVT'].fillna(0.0)
    metadatos_df = metadatos_df.fillna('Faltante')
    #   Crear columnas auxiliares
    metadatos_df['Coincide focus y region'] = (metadatos_df['FUND_GEO_FOCUS'] == metadatos_df['GEO_FOCUS_REGION'])
    metadatos_df['Coincide focus y country y no mexico'] = (metadatos_df['FUND_GEO_FOCUS'] == metadatos_df['GEO_FOCUS_COUNTRY']) \
                                                           & (metadatos_df['HB_GEOGRAPHIC_FOCUS'] != 'Mexico')

    # filtrar por metadatos
    metadatos_df = filtros.quitar_si_columna_en_lista(metadatos_df, 'GEO_FOCUS_COUNTRY', ['brazil', 'spain', 'us'])
    metadatos_df = filtros.quitar_si_columna_contiene(metadatos_df, 'GEO_FOCUS_REGION', 'bric')
    metadatos_df = filtros.quitar_si_condicion_y_columna_en_lista(metadatos_df, 'Coincide focus y region', 'FUND_GEO_FOCUS', ['european region', 'asian pacific region ex japan', 'asian pacific region', 'eurozone'])
    metadatos_df = filtros.quitar_si_condicion_y_columna_en_lista(metadatos_df, 'Coincide focus y country y no mexico', 'FUND_GEO_FOCUS', ['u.s.'])
    metadatos_df = filtros.quitar_si_columna_en_lista(metadatos_df, 'HB_GEOGRAPHIC_FOCUS', ['u.s.', 'asia pacific', 'western europe'])
    metadatos_df = filtros.quitar_si_columna_contiene(metadatos_df, 'TICKER', 'fib')
    #Pendiente
    #metadatos_df = quitar_si_columna_contiene(metadatos_df, 'TICKER', 'ind')
    metadatos_df = filtros.quitar_si_columna_contiene(metadatos_df, 'TICKER', 'ret')
    metadatos_df = filtros.quitar_si_columna_contiene(metadatos_df, 'FUND_INDUSTRY_FOCUS', 'real estate')
    metadatos_df = filtros.quitar_si_columna_mayor_a(metadatos_df, 'FUND_ASSET_ALLOC_GOVT', 80)
    metadatos_df = filtros.quitar_si_columna_contiene(metadatos_df, 'CIE_DES', 'msci')
    metadatos_df = filtros.quitar_si_columna_contiene(metadatos_df, 'CIE_DES', 'morgan stanley capital internationl all country world index')
    metadatos_df = filtros.quitar_si_columna_contiene(metadatos_df, 'CIE_DES', 'commodities')

    # QUITAR FILTRADOS MANUALMENTE
    quitados_manualmente_df = quitados_manualmente_df[['TICKER', 'Dudoso']]
    combinado_df = metadatos_df.merge(quitados_manualmente_df, on='TICKER', how='left')
    combinado_df = combinado_df[~(combinado_df['Dudoso'] == False)]
    tickers_sobrevivientes = set(combinado_df['TICKER'])
    tickers_eliminados = tickers_originales - tickers_sobrevivientes
    
    eliminated_df = pd.DataFrame(tickers_eliminados, columns=['Eliminated'])
    filtered_df = sin_repetidos_df[combinado_df['TICKER']]
    return filtered_df, eliminated_df

import argparse
def main(metadatos, quitados_manualmente, sin_repetidos, output_csv_name, output_eliminated_csv_name):
    metadatos_df = pd.read_excel(metadatos)
    quitados_manualmente_df = pd.read_excel(quitados_manualmente)
    sin_repetidos_df = pd.read_csv(sin_repetidos, index_col=0)
    limpiados_df, eliminados_df = limpiar(metadatos_df, quitados_manualmente_df, sin_repetidos_df)
    limpiados_df.to_csv(output_csv_name + '.csv')
    eliminados_df.to_csv(output_eliminated_csv_name+'.csv')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cleans the database')
    parser.add_argument('--metadatos', help='file with the metadata')
    parser.add_argument('--quitados_manualmente', help='file that contains the tickers eliminated manually')
    parser.add_argument('--sin_repetidos', help='file without repeated prices')
    parser.add_argument('--output_csv_name', help='name of the csv where the processed table will be saved')
    parser.add_argument('--output_eliminated_csv_name', help='name of the csv where the eliminated tickers will be saved')
    args = parser.parse_args()
    main(args.metadatos, args.quitados_manualmente, args.sin_repetidos, \
        args.output_csv_name, args.output_eliminated_csv_name)