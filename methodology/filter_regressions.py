import pandas as pd

def main(regressions, filtered_by_metadata, minimum):
    print('Número de regresiones:', len(regressions))

    filtered_regressions = regressions.loc[filtered_by_metadata.index]
    print('Después de aplicar filtros por metadatos:', len(filtered_regressions))
    filtered_regressions = filtered_regressions[filtered_regressions['M'] >= minimum]
    print('Después de eliminar fondos con menos de 11 retornos mensuales:', len(filtered_regressions))

    eliminated_regressions = regressions.loc[regressions.index.difference(filtered_by_metadata.index)]
    print('Número de regresiones rechazadas por los metadatos:', len(eliminated_regressions))
    eliminated_regressions = eliminated_regressions[eliminated_regressions['M'] >= minimum]
    print('Después de eliminar fondos con menos de 11 retornos mensuales:', len(eliminated_regressions))

    return filtered_regressions, eliminated_regressions



import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Splits the regressions in filtered and eliminated')
    parser.add_argument('--regressions')
    parser.add_argument('--minimum', type=int)
    parser.add_argument('--filtered_by_metadata')
    parser.add_argument('--filtered_output')
    parser.add_argument('--eliminated_output')
    args = parser.parse_args()
    
    regressions          = pd.read_csv(args.regressions,          index_col=0)
    filtered_by_metadata = pd.read_csv(args.filtered_by_metadata, index_col=0)

    filtered_regressions, eliminated_regressions = main(regressions, filtered_by_metadata, args.minimum)

    filtered_regressions.to_csv(args.filtered_output + '.csv')
    eliminated_regressions.to_csv(args.eliminated_output + '.csv')