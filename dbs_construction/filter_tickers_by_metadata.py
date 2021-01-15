import tipos_filtros as filtros
import pandas as pd

def limpiar(metadatos_df, quitados_manualmente_df):
    tickers_originales = set(metadatos_df['TICKER'])

    # APLICAR FILTROS A METADATOS
    removed_acum = []
    #   Rellenar vacios
    metadatos_df['FUND_ASSET_ALLOC_GOVT'] = metadatos_df['FUND_ASSET_ALLOC_GOVT'].fillna(0.0)
    metadatos_df = metadatos_df.fillna('Faltante')
    #   Crear columnas auxiliares
    metadatos_df['Coincide focus y region'] = (metadatos_df['FUND_GEO_FOCUS'] == metadatos_df['GEO_FOCUS_REGION'])
    metadatos_df['Coincide focus y country y no mexico'] = (metadatos_df['FUND_GEO_FOCUS'] == metadatos_df['GEO_FOCUS_COUNTRY']) \
                                                           & (metadatos_df['HB_GEOGRAPHIC_FOCUS'] != 'Mexico')

    #    filtrar por metadatos
    metadatos_df = filtros.quitar_si_condicion_y_columna_en_lista(metadatos_df, 'Coincide focus y region', 'FUND_GEO_FOCUS', ['european region', 'asian pacific region ex japan', 'asian pacific region', 'eurozone', 'global'], 'no mexico', removed_acum)
    metadatos_df = filtros.quitar_si_condicion_y_columna_en_lista(metadatos_df, 'Coincide focus y country y no mexico', 'FUND_GEO_FOCUS', ['u.s.'], 'no mexico', removed_acum)

    metadatos_df = filtros.quitar_si_columna_en_lista(metadatos_df, 'GEO_FOCUS_COUNTRY', ['brazil', 'spain', 'us'], 'no mexico', removed_acum)
    metadatos_df = filtros.quitar_si_columna_contiene(metadatos_df, 'GEO_FOCUS_REGION', 'bric', 'no mexico', removed_acum)
    metadatos_df = filtros.quitar_si_columna_en_lista(metadatos_df, 'HB_GEOGRAPHIC_FOCUS', ['u.s.', 'asia pacific', 'western europe'], 'no mexico', removed_acum)
    metadatos_df = filtros.quitar_si_columna_contiene(metadatos_df, 'TICKER', 'fib', 'fib en ticker', removed_acum)
    metadatos_df = filtros.quitar_si_columna_contiene(metadatos_df, 'TICKER', 'glob', 'glob en ticker', removed_acum)
    metadatos_df = filtros.quitar_si_columna_contiene(metadatos_df, 'TICKER', 'ret', 'ret en ticker', removed_acum)
    metadatos_df = filtros.quitar_si_columna_contiene(metadatos_df, 'FUND_INDUSTRY_FOCUS', 'real estate', 'real estate', removed_acum)
    metadatos_df = filtros.quitar_si_columna_mayor_a(metadatos_df, 'FUND_ASSET_ALLOC_GOVT', 80, 'muchos bonos', removed_acum)
    metadatos_df = filtros.quitar_si_columna_contiene(metadatos_df, 'CIE_DES', 'msci', 'msci en descripción', removed_acum)
    metadatos_df = filtros.quitar_si_columna_contiene(metadatos_df, 'CIE_DES', 'morgan stanley capital internationl all country world index', 'morgan stanley capital internationl all country world index en des', removed_acum)
    metadatos_df = filtros.quitar_si_columna_contiene(metadatos_df, 'CIE_DES', 'commodities', 'commodities en des', removed_acum)

    # QUITAR FILTRADOS MANUALMENTE
    metadatos_df = filtros.quitar_seleccionados_manualmente(metadatos_df, quitados_manualmente_df, removed_acum)
    eliminated_df = pd.DataFrame(removed_acum, columns=['Ticker', 'Reason'])

    print('# de Tickers al principio: ', len(tickers_originales))
    print('# de Tickers después de filtrar: ', len(metadatos_df))
    print('# de Tickers eliminados: ', len(eliminated_df))
    
    return metadatos_df, eliminated_df




##### Para correrlo desde la línea de comandos #####
import argparse
def main(metadatos, quitados_manualmente, output_csv_name, output_eliminated_csv_name):
    metadatos_df = pd.read_excel(metadatos)
    quitados_manualmente_df = pd.read_excel(quitados_manualmente)
    limpiados_df, eliminados_df = limpiar(metadatos_df, quitados_manualmente_df)
    limpiados_df.to_csv(output_csv_name + '.csv', index=False)
    eliminados_df.to_csv(output_eliminated_csv_name+'.csv', index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cleans the database')
    parser.add_argument('--metadatos', help='file with the metadata')
    parser.add_argument('--quitados_manualmente', help='file that contains the tickers eliminated manually')
    parser.add_argument('--output', help='name of the csv where the processed table will be saved')
    parser.add_argument('--output_eliminated', help='name of the csv where the eliminated tickers will be saved')
    args = parser.parse_args()
    main(args.metadatos, args.quitados_manualmente, args.output, args.output_eliminated)