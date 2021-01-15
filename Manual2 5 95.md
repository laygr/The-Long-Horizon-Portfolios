Descripción
Horizonte de los retornos: 4 semanas
periodo: todo
Combinadas las series altamente correlacionadas: Sí

# Dbs construction

python remove_repeated_prices.py ^
    --prices            ../input_data/todas.xlsx ^
    --minimum_repeated  4 ^
    --output            ../data_2/todas

python extract_days_every_n_weeks.py ^
    --rf     ../input_data/Cetes.xlsx ^
    --n      4 ^
    --output ../data_2/days_every_4_weeks

python build_n_week_returns.py ^
    --funds                ../data_2/todas.csv ^
    --index                ../input_data/Naftrac.xlsx ^
    --n                    4 ^
    --rf                   ../input_data/Cetes.xlsx ^
    --dates_every_n_week   ../data_2/days_every_4_weeks.csv ^
    --funds_output         ../data_2/funds_4_weeks_returns ^
    --index_output         ../data_2/index_4_weeks_returns ^
    --rf_output            ../data_2/risk_free_4_weeks_returns

python combine_highly_correlated.py ^
    --funds                 ../data_2/funds_4_weeks_returns.csv ^
    --filtered_by_metadata  ../data_2/filtered_by_metadata.csv ^
    --threshold             0.9999

python only_dates_in_common.py ^
    --funds          ../data_2/funds_4_weeks_returns_c.csv ^
    --index          ../data_2/index_4_weeks_returns.csv ^
    --rf             ../data_2/risk_free_4_weeks_returns.csv ^
    --output_sufix   2

# Methodology

python first_regressions.py ^
    --funds  ../data_2/funds_4_weeks_returns_c_2.csv ^
    --index  ../data_2/index_4_weeks_returns_2.csv ^
    --rf     ../data_2/risk_free_4_weeks_returns_2.csv ^
    --output ../data_2/regressions_4_weeks_c

python filter_regressions.py ^
    --regressions          ../data_2/regressions_4_weeks_c.csv ^
    --minimum              13 ^
    --filtered_by_metadata ../data_2/filtered_by_metadata.csv ^
    --filtered_output      ../data_2/filtered_regressions_4_weeks_c ^
    --eliminated_output    ../data_2/eliminated_regressions_4_weeks_c

python winsorize.py ^
    --regressions ../data_2/filtered_regressions_4_weeks_c.csv ^
    --lower 5 ^
    --upper 95

python modified_LL.py ^
    --regressions ../data_2/filtered_regressions_4_weeks_c_w_5_95.csv ^
    --N 13 ^
    --S 1000

python modified_LL.py ^
    --regressions ../data_2/filtered_regressions_4_weeks_c_w_5_95.csv ^
    --N 130 ^
    --S 1000

python modified_LL.py ^
    --regressions ../data_2/filtered_regressions_4_weeks_c_w_5_95.csv ^
    --N 0 ^
    --S 1000

# tables

python categorias_tickers.py ^
    --filtered_by_metadata   ../data_2/filtered_by_metadata.csv ^
    --funds                  ../data_2/todas.csv ^
    --filtered_regs          ../data_2/filtered_regressions_4_weeks_c.csv ^
    --rejected_regs          ../data_2/eliminated_regressions_4_weeks_c.csv ^
    --output                 ../output/2/Categorias

python table1.py ^
    --funds        ../data_2/funds_4_weeks_returns_c_2.csv ^
    --index        ../data_2/index_4_weeks_returns_2.csv ^
    --rf           ../data_2/risk_free_4_weeks_returns_2.csv ^
    --regs         ../data_2/filtered_regressions_4_weeks_c.csv  ^
    --output       ../output/2/Table1.xlsx

python table2.py ^
    --funds                 ../data_2/funds_4_weeks_returns_c_2.csv ^
    --index                 ../data_2/index_4_weeks_returns_2.csv ^
    --rf                    ../data_2/risk_free_4_weeks_returns_2.csv ^
    --filtered_regressions  ../data_2/filtered_regressions_4_weeks_c.csv ^
    --weeks                 4^
    --output                ../output/2/Table2.xlsx

python table3.py ^
    --regs_year         ../data_2/filtered_regressions_4_weeks_c_w_5_95_13.csv ^
    --regs_decade       ../data_2/filtered_regressions_4_weeks_c_w_5_95_130.csv ^
    --regs_lifetime     ../data_2/filtered_regressions_4_weeks_c_w_5_95_0.csv ^
    --output            ../output/2/Table3.xlsx

python table4.py ^
    --regs_year ../data_2/filtered_regressions_4_weeks_c_w_5_95_13.csv ^
    --h         13 ^
    --funds     ../data_2/funds_4_weeks_returns_c_2.csv ^
    --rf        ../data_2/risk_free_4_weeks_returns_2.csv ^
    --index     ../data_2/index_4_weeks_returns.csv ^
    --output    ../output/2/Table4.xlsx

python table5.py ^
    --data           ../data_2/filtered_regressions_4_weeks_c_w_5_95.csv ^
    --data_year      ../data_2/filtered_regressions_4_weeks_c_w_5_95_13.csv ^
    --data_decade    ../data_2/filtered_regressions_4_weeks_c_w_5_95_130.csv ^
    --data_lifetime  ../data_2/filtered_regressions_4_weeks_c_w_5_95_0.csv ^
    --output         ../output/2/Table5.xlsx

python table6.py ^
    --data_year      ../data_2/filtered_regressions_4_weeks_c_w_5_95_13.csv ^
    --data_decade    ../data_2/filtered_regressions_4_weeks_c_w_5_95_130.csv ^
    --data_lifetime  ../data_2/filtered_regressions_4_weeks_c_w_5_95_0.csv ^
    --weeks          4 ^
    --output         ../output/2/Table6.xlsx

python table7I.py ^
    --data           ../data_2/filtered_regressions_4_weeks_c_w_5_95.csv ^
    --data_year      ../data_2/filtered_regressions_4_weeks_c_w_5_95_13.csv ^
    --data_decade    ../data_2/filtered_regressions_4_weeks_c_w_5_95_130.csv ^
    --data_lifetime  ../data_2/filtered_regressions_4_weeks_c_w_5_95_0.csv ^
    --weeks          4 ^
    --output         ../output/2/Table7_I.xlsx

python table7II.py ^
    --data           ../data_2/filtered_regressions_4_weeks_c_w_5_95.csv ^
    --data_year      ../data_2/filtered_regressions_4_weeks_c_w_5_95_13.csv ^
    --data_decade    ../data_2/filtered_regressions_4_weeks_c_w_5_95_130.csv ^
    --data_lifetime  ../data_2/filtered_regressions_4_weeks_c_w_5_95_0.csv ^
    --weeks          4 ^
    --output         ../output/2/Table7_II.xlsx