Return Horizon and Mutual Fund Performance In Mexico


> python remove_tickers_by_metadata.py  ^
    --metadatos ../input_data/metadatos.xlsx  ^
    --quitados_manualmente ../input_data/eliminados_manualmente.xlsx  ^
    --output ../data/filtered_by_metadata  ^
    --output_eliminated ../data/eliminated_by_metadata


    

python extract_last_days_months.py ^
    --prices ../input_data/todas.xlsx ^
    --output ../data/last_days_in_months

> python build_risk_free.py ^
    --rates             "../input_data/Cetes28 Tasa.xlsx" ^
    --col               1 ^
    --last_days_months  ../data/last_days_in_months.csv ^
    --output            ../data/risk_free

> python build_funds_monthly_returns.py ^
    --precios          ../input_data/todas.xlsx ^
    --minimum_repeated 4 ^
    --last_days_months ../data/last_days_in_months.csv ^
    --output           ../data/funds_returns

> python build_index.py ^
    --prices ../input_data/Naftrac.xlsx ^
    --output ../data/index_returns

> python only_dates_in_common.py ^
    --funds        ../data/funds_returns_combined.csv ^
    --index        ../data/index_returns.csv ^
    --rf           ../data/risk_free.csv ^
    --output_sufix 2





python extract_days_every_4_weeks.py ^
    --rf     ../input_data/Cetes.xlsx ^
    --output ../data/days_every_4_weeks

python build_risk_free_4_weeks.py ^
    --rates    ../input_data/Cetes.xlsx ^
    --output   ../data/risk_free_4_weeks

python build_funds_4_weeks.py ^
    --prices               ../input_data/todas.xlsx ^
    --minimum_repeated     4 ^
    --days_every_4_weeks   ../data/days_every_4_weeks.csv ^
    --output               ../data/funds_4_weeks_returns

python build_index_4_weeks.py ^
    --prices               ../input_data/Naftrac.xlsx ^
    --days_every_4_weeks   ../data/days_every_4_weeks.csv ^
    --output               ../data/index_4_weeks_returns

python only_dates_in_common.py ^
    --funds        ../data/funds_4_weeks_returns.csv ^
    --index        ../data/index_4_weeks_returns.csv ^
    --rf           ../data/risk_free_4_weeks.csv ^
    --output_sufix 2