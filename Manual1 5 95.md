Descripción
Horizonte de los retornos: 4 semanas
periodo: todo
Combinadas las series altamente correlacionadas: No

# Dbs construction

python filter_tickers_by_metadata.py ^
    --metadatos             ../input_data/metadatos.xlsx ^
    --quitados_manualmente  ../input_data/eliminados_manualmente.xlsx ^
    --output                ../data_1/filtered_by_metadata ^
    --output_eliminated     ../data_1/eliminated_by_metadata

python remove_repeated_prices.py ^
    --prices            ../input_data/todas.xlsx ^
    --minimum_repeated  4 ^
    --output            ../data_1/todas

python extract_days_every_n_weeks.py ^
    --rf     ../input_data/Cetes.xlsx ^
    --n      4 ^
    --output ../data_1/days_every_4_weeks

python build_n_week_returns.py ^
    --funds                ../data_1/todas.csv ^
    --index                ../input_data/Naftrac.xlsx ^
    --rf                   ../input_data/Cetes.xlsx ^
    --n                    4 ^
    --dates_every_n_week   ../data_1/days_every_4_weeks.csv ^
    --funds_output         ../data_1/funds_4_weeks_returns ^
    --index_output         ../data_1/index_4_weeks_returns ^
    --rf_output            ../data_1/risk_free_4_weeks_returns

python only_dates_in_common.py ^
    --funds          ../data_1/funds_4_weeks_returns.csv ^
    --index          ../data_1/index_4_weeks_returns.csv ^
    --rf             ../data_1/risk_free_4_weeks_returns.csv ^
    --output_sufix   2

# Methodology

python first_regressions.py ^
    --funds  ../data_1/funds_4_weeks_returns_2.csv ^
    --index  ../data_1/index_4_weeks_returns_2.csv ^
    --rf     ../data_1/risk_free_4_weeks_returns_2.csv ^
    --output ../data_1/regressions_4_weeks

python filter_regressions.py ^
    --regressions          ../data_1/regressions_4_weeks.csv ^
    --minimum              13 ^
    --filtered_by_metadata ../data_1/filtered_by_metadata.csv ^
    --filtered_output      ../data_1/filtered_regressions_4_weeks ^
    --eliminated_output    ../data_1/eliminated_regressions_4_weeks

python winsorize.py ^
    --regressions ../data_1/filtered_regressions_4_weeks.csv ^
    --lower 5 ^
    --upper 95

python modified_LL.py ^
    --regressions "../data_1/filtered_regressions_4_weeks_w_5_95.csv" ^
    --N 13 ^
    --S 1000

python modified_LL.py ^
    --regressions "../data_1/filtered_regressions_4_weeks_w_5_95.csv" ^
    --N 130 ^
    --S 1000

python modified_LL.py ^
    --regressions "../data_1/filtered_regressions_4_weeks_w_5_95.csv" ^
    --N 0 ^
    --S 1000

# tables

python categorias_tickers.py ^
    --filtered_by_metadata   "../data_1/filtered_by_metadata.csv" ^
    --funds                  "../data_1/todas.csv" ^
    --filtered_regs          "../data_1/filtered_regressions_4_weeks.csv" ^
    --rejected_regs          "../data_1/eliminated_regressions_4_weeks.csv" ^
    --output                 ../output/1/Categorias

python table1.py ^
    --funds        "../data_1/funds_4_weeks_returns_2.csv" ^
    --index        "../data_1/index_4_weeks_returns_2.csv" ^
    --rf           "../data_1/risk_free_4_weeks_returns_2.csv" ^
    --regs         "../data_1/filtered_regressions_4_weeks.csv"  ^
    --output       ../output/1/Table1.xlsx

python table2.py ^
    --funds                 "../data_1/funds_4_weeks_returns_2.csv" ^
    --index                 "../data_1/index_4_weeks_returns_2.csv" ^
    --rf                    "../data_1/risk_free_4_weeks_returns_2.csv" ^
    --filtered_regressions  "../data_1/filtered_regressions_4_weeks.csv" ^
    --weeks                 4^
    --output                ../output/1/Table2.xlsx

python table3.py ^
    --regs_year         "../data_1/filtered_regressions_4_weeks_w_5_95_13.csv" ^
    --regs_decade       "../data_1/filtered_regressions_4_weeks_w_5_95_130.csv" ^
    --regs_lifetime     "../data_1/filtered_regressions_4_weeks_w_5_95_0.csv" ^
    --output            ../output/1/Table3.xlsx

python table3.py ^
    --regs_year         "../data_1/filtered_regressions_4_weeks_w_5_95_13.csv" ^
    --regs_decade       "../data_1/filtered_regressions_4_weeks_w_5_95_130.csv" ^
    --regs_lifetime     "../data_1/filtered_regressions_4_weeks_w_5_95_0.csv" ^
    --output            ../output/1/Table3.xlsx

python table4.py ^
    --regs_year ../data_1/filtered_regressions_4_weeks_w_5_95_13.csv ^
    --h         13 ^
    --funds     ../data_1/funds_4_weeks_returns_2.csv ^
    --rf        ../data_1/risk_free_4_weeks_returns_2.csv ^
    --index     ../data_1/index_4_weeks_returns.csv ^
    --output    ../output/1/Table4.xlsx

python table5.py ^
    --data           ../data_1/filtered_regressions_4_weeks_w_5_95.csv ^
    --data_year      ../data_1/filtered_regressions_4_weeks_w_5_95_13.csv ^
    --data_decade    ../data_1/filtered_regressions_4_weeks_w_5_95_130.csv ^
    --data_lifetime  ../data_1/filtered_regressions_4_weeks_w_5_95_0.csv ^
    --output         ../output/1/Table5.xlsx

python table5.py ^
    --data           "../data_1/filtered_regressions_4_weeks_w_5_95.csv" ^
    --data_year      "../data_1/filtered_regressions_4_weeks_w_5_95_13.csv" ^
    --data_decade    "../data_1/filtered_regressions_4_weeks_w_5_95_130.csv" ^
    --data_lifetime  "../data_1/filtered_regressions_4_weeks_w_5_95_0.csv" ^
    --output         ../output/1/Table5.xlsx

python table6.py ^
    --data_year      "../data_1/filtered_regressions_4_weeks_w_5_95_13.csv" ^
    --data_decade    "../data_1/filtered_regressions_4_weeks_w_5_95_130.csv" ^
    --data_lifetime  "../data_1/filtered_regressions_4_weeks_w_5_95_0.csv" ^
    --weeks          4 ^
    --output         ../output/1/Table6.xlsx

python table7I.py ^
    --data           "../data_1/filtered_regressions_4_weeks_w_5_95.csv" ^
    --data_year      "../data_1/filtered_regressions_4_weeks_w_5_95_13.csv" ^
    --data_decade    "../data_1/filtered_regressions_4_weeks_w_5_95_130.csv" ^
    --data_lifetime  "../data_1/filtered_regressions_4_weeks_w_5_95_0.csv" ^
    --weeks          4 ^
    --output         ../output/1/Table7_I.xlsx

python table7II.py ^
    --data           ../data_1/filtered_regressions_4_weeks_w_5_95.csv ^
    --data_year      ../data_1/filtered_regressions_4_weeks_w_5_95_13.csv ^
    --data_decade    ../data_1/filtered_regressions_4_weeks_w_5_95_130.csv ^
    --data_lifetime  ../data_1/filtered_regressions_4_weeks_w_5_95_0.csv ^
    --weeks          4 ^
    --output         ../output/1/Table7_II.xlsx