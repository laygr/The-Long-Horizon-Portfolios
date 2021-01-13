Descripción
Horizonte de los retornos: 1 semanas
periodo: todo
Combinadas las series altamente correlacionadas: No

# Dbs construction

python remove_repeated_prices.py ^
    --prices            ../input_data/todas.xlsx ^
    --minimum_repeated  4 ^
    --output            ../data/todas

python extract_days_every_n_weeks.py ^
    --rf     ../input_data/Cetes.xlsx ^
    --n      1 ^
    --output ../data/days_every_1_weeks

python build_n_week_returns.py ^
    --funds                ../data/todas.csv ^
    --index                ../input_data/Naftrac.xlsx ^
    --n                    1 ^
    --rf                   ../input_data/Cetes.xlsx ^
    --dates_every_n_week   ../data/days_every_1_weeks.csv ^
    --funds_output         ../data/funds_1_weeks_returns ^
    --index_output         ../data/index_1_weeks_returns ^
    --rf_output            ../data/risk_free_1_weeks_returns

python only_dates_in_range.py ^
    --funds          ../data/funds_1_weeks_returns.csv ^
    --index          ../data/index_1_weeks_returns.csv ^
    --rf             ../data/risk_free_1_weeks_returns.csv ^
    --first_date     2000-01-01 ^
    --last_date      2021-01-01 ^
    --output_suffix  2

# Methodology

python first_regressions.py ^
    --funds  ../data/funds_1_weeks_returns_2.csv ^
    --index  ../data/index_1_weeks_returns_2.csv ^
    --rf     ../data/risk_free_1_weeks_returns_2.csv ^
    --output ../data/regressions_1_weeks

python filter_regressions.py ^
    --regressions          ../data/regressions_1_weeks.csv ^
    --minimum              48 ^
    --filtered_by_metadata ../data/filtered_by_metadata.csv ^
    --filtered_output      ../data/filtered_regressions_1_weeks ^
    --eliminated_output    ../data/eliminated_regressions_1_weeks

python winsorize.py ^
    --regressions ../data/filtered_regressions_1_weeks.csv ^
    --lower 10 ^
    --upper 90

python modified_LL.py ^
    --regressions ../data/filtered_regressions_1_weeks_w_10_90.csv ^
    --N           52 ^
    --S           1000

python modified_LL.py ^
    --regressions ../data/filtered_regressions_1_weeks_w_10_90.csv ^
    --N           520 ^
    --S           1000

python modified_LL.py ^
    --regressions ../data/filtered_regressions_1_weeks_w_10_90.csv ^
    --N           0 ^
    --S           1000

# Tables

python categorias_tickers.py ^
    --filtered_by_metadata   ../data/filtered_by_metadata.csv ^
    --funds                  ../data/todas.csv ^
    --filtered_regs          ../data/filtered_regressions_1_weeks.csv ^
    --rejected_regs          ../data/eliminated_regressions_1_weeks.csv ^
    --output                 ../output/3/Categorias

python table1.py ^
    --funds        ../data/funds_1_weeks_returns_2.csv ^
    --index        ../data/index_1_weeks_returns_2.csv ^
    --rf           ../data/risk_free_1_weeks_returns_2.csv ^
    --regs         ../data/filtered_regressions_1_weeks.csv  ^
    --output       ../output/3/Table1.xlsx

python table2.py ^
    --funds                 ../data/funds_1_weeks_returns_2.csv ^
    --index                 ../data/index_1_weeks_returns_2.csv ^
    --rf                    ../data/risk_free_1_weeks_returns_2.csv ^
    --filtered_regressions  ../data/filtered_regressions_1_weeks.csv ^
    --weeks                 1 ^
    --output                ../output/3/Table2.xlsx

python table3.py ^
    --regs_year         ../data/filtered_regressions_1_weeks_w_10_90_52.csv ^
    --regs_decade       ../data/filtered_regressions_1_weeks_w_10_90_520.csv ^
    --regs_lifetime     ../data/filtered_regressions_1_weeks_w_10_90_0.csv ^
    --output            ../output/3/Table3.xlsx

python table4.py ^
    --regs_year ../data/filtered_regressions_1_weeks_w_10_90_52.csv ^
    --h         52 ^
    --funds     ../data/funds_1_weeks_returns_2.csv ^
    --rf        ../data/risk_free_1_weeks_returns_2.csv ^
    --index     ../data/index_1_weeks_returns.csv ^
    --output    ../output/3/Table4.xlsx

python table5.py ^
    --data           ../data/filtered_regressions_1_weeks_w_10_90.csv ^
    --data_year      ../data/filtered_regressions_1_weeks_w_10_90_52.csv ^
    --data_decade    ../data/filtered_regressions_1_weeks_w_10_90_520.csv ^
    --data_lifetime  ../data/filtered_regressions_1_weeks_w_10_90_0.csv ^
    --output         ../output/3/Table5.xlsx

python table6.py ^
    --data_year      ../data/filtered_regressions_1_weeks_w_10_90_52.csv ^
    --data_decade    ../data/filtered_regressions_1_weeks_w_10_90_520.csv ^
    --data_lifetime  ../data/filtered_regressions_1_weeks_w_10_90_0.csv ^
    --weeks          1 ^
    --output         ../output/3/Table6.xlsx

python table7I.py ^
    --data           ../data/filtered_regressions_1_weeks_w_10_90.csv ^
    --data_year      ../data/filtered_regressions_1_weeks_w_10_90_52.csv ^
    --data_decade    ../data/filtered_regressions_1_weeks_w_10_90_520.csv ^
    --data_lifetime  ../data/filtered_regressions_1_weeks_w_10_90_0.csv ^
    --weeks          1 ^
    --output         ../output/3/Table7_I.xlsx

python table7II.py ^
    --data           ../data/filtered_regressions_1_weeks_w_10_90.csv ^
    --data_year      ../data/filtered_regressions_1_weeks_w_10_90_52.csv ^
    --data_decade    ../data/filtered_regressions_1_weeks_w_10_90_520.csv ^
    --data_lifetime  ../data/filtered_regressions_1_weeks_w_10_90_0.csv ^
    --weeks          1 ^
    --output         ../output/3/Table7_II.xlsx
