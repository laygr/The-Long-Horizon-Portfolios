import retornos_simples as rs
import pandas as pd
import argparse

def main(filepath, output_csv_name):
    index_df = pd.read_excel(filepath, parse_dates=['Dates'], index_col=0)
    index_df = rs.compute_end_of_month_returns(index_df)
    index_df.to_csv(output_csv_name + '.csv', index=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Transform daily anual rates to monthly rates')
    parser.add_argument('--prices', help='the path to the excel file with the rates')
    parser.add_argument('--output', help='the path to the excel file with the rates')
    args = parser.parse_args()
    main(args.prices, args.output)