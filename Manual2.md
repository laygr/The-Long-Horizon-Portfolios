Descripción
Horizonte de los retornos: 4 semanas
periodo: todo
Combinadas las series altamente correlacionadas: Sí

# Dbs construction

python remove_repeated_prices.py ^
    --prices            ../input_data/todas.xlsx ^
    --minimum_repeated  4 ^
    --output            ../data/todas

python extract_days_every_n_weeks.py ^
    --rf     ../input_data/Cetes.xlsx ^
    --n      4 ^
    --output ../data/days_every_4_weeks

python build_n_week_returns.py ^
    --funds                ../data/todas.csv ^
    --index                ../input_data/Naftrac.xlsx ^
    --n                    4 ^
    --rf                   ../input_data/Cetes.xlsx ^
    --dates_every_n_week   ../data/days_every_4_weeks.csv ^
    --funds_output         ../data/funds_4_weeks_returns ^
    --index_output         ../data/index_4_weeks_returns ^
    --rf_output            ../data/risk_free_4_weeks_returns

python combine_highly_correlated.py ^
    --funds                 ../data/funds_4_weeks_returns.csv ^
    --filtered_by_metadata  ../data/filtered_by_metadata.csv ^
    --threshold             0.9999

python only_dates_in_common.py ^
    --funds          ../data/funds_4_weeks_returns_c.csv ^
    --index          ../data/index_4_weeks_returns.csv ^
    --rf             ../data/risk_free_4_weeks_returns.csv ^
    --output_sufix   2

# Methodology

python first_regressions.py ^
    --funds  ../data/funds_4_weeks_returns_c_2.csv ^
    --index  ../data/index_4_weeks_returns_2.csv ^
    --rf     ../data/risk_free_4_weeks_returns_2.csv ^
    --output ../data/regressions_4_weeks_c

python filter_regressions.py ^
    --regressions          ../data/regressions_4_weeks_c.csv ^
    --minimum              13 ^
    --filtered_by_metadata ../data/filtered_by_metadata.csv ^
    --filtered_output      ../data/filtered_regressions_4_weeks_c ^
    --eliminated_output    ../data/eliminated_regressions_4_weeks_c

python winsorize.py ^
    --regressions ../data/filtered_regressions_4_weeks_c.csv ^
    --lower 10 ^
    --upper 90

python modified_LL.py ^
    --regressions ../data/filtered_regressions_4_weeks_c_w_10_90.csv ^
    --N 13 ^
    --S 1000

python modified_LL.py ^
    --regressions ../data/filtered_regressions_4_weeks_c_w_10_90.csv ^
    --N 130 ^
    --S 1000

python modified_LL.py ^
    --regressions ../data/filtered_regressions_4_weeks_c_w_10_90.csv ^
    --N 0 ^
    --S 1000

# tables

python categorias_tickers.py ^
    --filtered_by_metadata   ../data/filtered_by_metadata.csv ^
    --funds                  ../data/todas.csv ^
    --filtered_regs          ../data/filtered_regressions_4_weeks_c.csv ^
    --rejected_regs          ../data/eliminated_regressions_4_weeks_c.csv ^
    --output                 ../output/2/Categorias

python table1.py ^
    --funds        ../data/funds_4_weeks_returns_c_2.csv ^
    --index        ../data/index_4_weeks_returns_2.csv ^
    --rf           ../data/risk_free_4_weeks_returns_2.csv ^
    --regs         ../data/filtered_regressions_4_weeks_c.csv  ^
    --output       ../output/2/Table1.xlsx

python table2.py ^
    --funds                 ../data/funds_4_weeks_returns_c_2.csv ^
    --index                 ../data/index_4_weeks_returns_2.csv ^
    --rf                    ../data/risk_free_4_weeks_returns_2.csv ^
    --filtered_regressions  ../data/filtered_regressions_4_weeks_c.csv ^
    --weeks                 4^
    --output                ../output/2/Table2.xlsx

python table3.py ^
    --regs_year         ../data/filtered_regressions_4_weeks_c_w_10_90_13.csv ^
    --regs_decade       ../data/filtered_regressions_4_weeks_c_w_10_90_130.csv ^
    --regs_lifetime     ../data/filtered_regressions_4_weeks_c_w_10_90_0.csv ^
    --output            ../output/2/Table3.xlsx

python table4.py ^
    --regs_year ../data/filtered_regressions_4_weeks_c_w_10_90_13.csv ^
    --h         13 ^
    --funds     ../data/funds_4_weeks_returns_c_2.csv ^
    --rf        ../data/risk_free_4_weeks_returns_2.csv ^
    --index     ../data/index_4_weeks_returns.csv ^
    --output    ../output/2/Table4.xlsx

python table5.py ^
    --data           ../data/filtered_regressions_4_weeks_c_w_10_90.csv ^
    --data_year      ../data/filtered_regressions_4_weeks_c_w_10_90_13.csv ^
    --data_decade    ../data/filtered_regressions_4_weeks_c_w_10_90_130.csv ^
    --data_lifetime  ../data/filtered_regressions_4_weeks_c_w_10_90_0.csv ^
    --output         ../output/2/Table5.xlsx

python table6.py ^
    --data_year      ../data/filtered_regressions_4_weeks_c_w_10_90_13.csv ^
    --data_decade    ../data/filtered_regressions_4_weeks_c_w_10_90_130.csv ^
    --data_lifetime  ../data/filtered_regressions_4_weeks_c_w_10_90_0.csv ^
    --weeks          4 ^
    --output         ../output/2/Table6.xlsx

python table7I.py ^
    --data           ../data/filtered_regressions_4_weeks_c_w_10_90.csv ^
    --data_year      ../data/filtered_regressions_4_weeks_c_w_10_90_13.csv ^
    --data_decade    ../data/filtered_regressions_4_weeks_c_w_10_90_130.csv ^
    --data_lifetime  ../data/filtered_regressions_4_weeks_c_w_10_90_0.csv ^
    --weeks          4 ^
    --output         ../output/2/Table7_I.xlsx

python table7II.py ^
    --data           ../data/filtered_regressions_4_weeks_c_w_10_90.csv ^
    --data_year      ../data/filtered_regressions_4_weeks_c_w_10_90_13.csv ^
    --data_decade    ../data/filtered_regressions_4_weeks_c_w_10_90_130.csv ^
    --data_lifetime  ../data/filtered_regressions_4_weeks_c_w_10_90_0.csv ^
    --weeks          4 ^
    --output         ../output/2/Table7_II.xlsx