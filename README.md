Return Horizon and Mutual Fund Performance In Mexico

*Example on how to remove repeated values:*

> python3 quitar_repetidos.py --filepath todas.xlsx --minimum_repeated 4 --output_csv_name sin_repetidos


*Example on how to clean the database:*

> python3 limpieza.py --metadatos data/metadatos.xlsx --quitados_manualmente data/eliminados_manualmente.xlsx --sin_repetidos data/sin_repetidos.csv --output_csv_name data/limpiados --output_eliminated_csv_name data/eliminados


*Example on how to compute returns:*

> python3 retornos_simples.py --precios data/limpiados.csv --diarios_csv_name data/daily_returns --mensuales_csv_name data/monthly_returns