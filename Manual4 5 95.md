Descripción
Horizonte de los retornos: 1 semanas
periodo: 01-01-2010 en adelante
Combinadas las series altamente correlacionadas: No


# Dbs construction

python remove_repeated_prices.py ^
    --prices            ../input_data/todas.xlsx ^
    --minimum_repeated  4 ^
    --output            ../data_4/todas

python extract_days_every_n_weeks.py ^
    --rf     ../input_data/Cetes.xlsx ^
    --n      1 ^
    --output ../data_4/days_every_1_weeks

python build_n_week_returns.py ^
    --funds                ../data_4/todas.csv ^
    --index                ../input_data/Naftrac.xlsx ^
    --n                    1 ^
    --rf                   ../input_data/Cetes.xlsx ^
    --dates_every_n_week   ../data_4/days_every_1_weeks.csv ^
    --funds_output         ../data_4/funds_1_weeks_returns ^
    --index_output         ../data_4/index_1_weeks_returns ^
    --rf_output            ../data_4/risk_free_1_weeks_returns

python only_dates_in_range.py ^
    --funds          ../data_4/funds_1_weeks_returns.csv ^
    --index          ../data_4/index_1_weeks_returns.csv ^
    --rf             ../data_4/risk_free_1_weeks_returns.csv ^
    --first_date     2010-01-01 ^
    --last_date      2021-01-01 ^
    --output_suffix  2

# Methodology

python first_regressions.py ^
    --funds  ../data_4/funds_1_weeks_returns_2.csv ^
    --index  ../data_4/index_1_weeks_returns_2.csv ^
    --rf     ../data_4/risk_free_1_weeks_returns_2.csv ^
    --output ../data_4/regressions_1_weeks

python filter_regressions.py ^
    --regressions          ../data_4/regressions_1_weeks.csv ^
    --minimum              52 ^
    --filtered_by_metadata ../data_4/filtered_by_metadata.csv ^
    --filtered_output      ../data_4/filtered_regressions_1_weeks ^
    --eliminated_output    ../data_4/eliminated_regressions_1_weeks

python winsorize.py ^
    --regressions ../data_4/filtered_regressions_1_weeks.csv ^
    --lower 5 ^
    --upper 95

python modified_LL.py ^
    --regressions ../data_4/filtered_regressions_1_weeks_w_5_95.csv ^
    --N           52 ^
    --S           1000

python modified_LL.py ^
    --regressions ../data_4/filtered_regressions_1_weeks_w_5_95.csv ^
    --N           520 ^
    --S           1000

python modified_LL.py ^
    --regressions ../data_4/filtered_regressions_1_weeks_w_5_95.csv ^
    --N           0 ^
    --S           1000

# Tables

python categorias_tickers.py ^
    --filtered_by_metadata   ../data_4/filtered_by_metadata.csv ^
    --funds                  ../data_4/todas.csv ^
    --filtered_regs          ../data_4/filtered_regressions_1_weeks.csv ^
    --rejected_regs          ../data_4/eliminated_regressions_1_weeks.csv ^
    --output                 ../output/4/Categorias

python table1.py ^
    --funds        ../data_4/funds_1_weeks_returns_2.csv ^
    --index        ../data_4/index_1_weeks_returns_2.csv ^
    --rf           ../data_4/risk_free_1_weeks_returns_2.csv ^
    --regs         ../data_4/filtered_regressions_1_weeks.csv  ^
    --output       ../output/4/Table1.xlsx

python table2.py ^
    --funds                 ../data_4/funds_1_weeks_returns_2.csv ^
    --index                 ../data_4/index_1_weeks_returns_2.csv ^
    --rf                    ../data_4/risk_free_1_weeks_returns_2.csv ^
    --filtered_regressions  ../data_4/filtered_regressions_1_weeks.csv ^
    --weeks                 1 ^
    --output                ../output/4/Table2.xlsx

python table3.py ^
    --regs_year         ../data_4/filtered_regressions_1_weeks_w_5_95_52.csv ^
    --regs_decade       ../data_4/filtered_regressions_1_weeks_w_5_95_520.csv ^
    --regs_lifetime     ../data_4/filtered_regressions_1_weeks_w_5_95_0.csv ^
    --output            ../output/4/Table3.xlsx


python table5.py ^
    --data           ../data_4/filtered_regressions_1_weeks_w_5_95.csv ^
    --data_year      ../data_4/filtered_regressions_1_weeks_w_5_95_52.csv ^
    --data_decade    ../data_4/filtered_regressions_1_weeks_w_5_95_520.csv ^
    --data_lifetime  ../data_4/filtered_regressions_1_weeks_w_5_95_0.csv ^
    --output         ../output/4/Table5.xlsx

python table6.py ^
    --data_year      ../data_4/filtered_regressions_1_weeks_w_5_95_52.csv ^
    --data_decade    ../data_4/filtered_regressions_1_weeks_w_5_95_520.csv ^
    --data_lifetime  ../data_4/filtered_regressions_1_weeks_w_5_95_0.csv ^
    --weeks          1 ^
    --output         ../output/4/Table6.xlsx

python table7I.py ^
    --data           ../data_4/filtered_regressions_1_weeks_w_5_95.csv ^
    --data_year      ../data_4/filtered_regressions_1_weeks_w_5_95_52.csv ^
    --data_decade    ../data_4/filtered_regressions_1_weeks_w_5_95_520.csv ^
    --data_lifetime  ../data_4/filtered_regressions_1_weeks_w_5_95_0.csv ^
    --weeks          1 ^
    --output         ../output/4/Table7_I.xlsx

python table7II.py ^
    --data           ../data_4/filtered_regressions_1_weeks_w_5_95.csv ^
    --data_year      ../data_4/filtered_regressions_1_weeks_w_5_95_52.csv ^
    --data_decade    ../data_4/filtered_regressions_1_weeks_w_5_95_520.csv ^
    --data_lifetime  ../data_4/filtered_regressions_1_weeks_w_5_95_0.csv ^
    --weeks          1 ^
    --output         ../output/4/Table7_II.xlsx