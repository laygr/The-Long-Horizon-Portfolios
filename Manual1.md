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

python only_dates_in_common.py ^
    --funds          ../data/funds_4_weeks_returns.csv ^
    --index          ../data/index_4_weeks_returns.csv ^
    --rf             ../data/risk_free_4_weeks_returns.csv ^
    --output_sufix   2

# Methodology

python first_regressions.py ^
    --funds  ../data/funds_4_weeks_returns_2.csv ^
    --index  ../data/index_4_weeks_returns_2.csv ^
    --rf     ../data/risk_free_4_weeks_returns_2.csv ^
    --output ../data/regressions_4_weeks

python filter_regressions.py ^
    --regressions          ../data/regressions_4_weeks.csv ^
    --minimum              12 ^
    --filtered_by_metadata ../data/filtered_by_metadata.csv ^
    --filtered_output      ../data/filtered_regressions_4_weeks ^
    --eliminated_output    ../data/eliminated_regressions_4_weeks

python winsorize.py ^
    --regressions ../data/filtered_regressions_4_weeks.csv ^
    --lower 10 ^
    --upper 90

python modified_LL.py ^
    --regressions ../data/filtered_regressions_4_weeks_w_10_90.csv ^
    --N 13 ^
    --S 1000

python modified_LL.py ^
    --regressions ../data/filtered_regressions_4_weeks_w_10_90.csv ^
    --N 130 ^
    --S 1000

python modified_LL.py ^
    --regressions ../data/filtered_regressions_4_weeks_w_10_90.csv ^
    --N 0 ^
    --S 1000

# tables

python table1.py ^
    --funds        ../data/funds_4_weeks_returns_2.csv ^
    --index        ../data/index_4_weeks_returns_2.csv ^
    --rf           ../data/risk_free_4_weeks_returns_2.csv ^
    --regs         ../data/filtered_regressions_4_weeks.csv  ^
    --output       ../output/1/Table1.xlsx

python table2.py ^
    --funds                 ../data/funds_4_weeks_returns_2.csv ^
    --index                 ../data/index_4_weeks_returns_2.csv ^
    --rf                    ../data/risk_free_4_weeks_returns_2.csv ^
    --filtered_regressions  ../data/filtered_regressions_4_weeks.csv
    --output                ../output/1/Table2.xlsx

python table3.py ^
    --regs_year         ../data/filtered_regressions_4_weeks_w_10_90_13.csv ^
    --regs_decade       ../data/filtered_regressions_4_weeks_w_10_90_130.csv ^
    --regs_lifetime     ../data/filtered_regressions_4_weeks_w_10_90_0.csv ^
    --output            ../output/1/Table3.xlsx

python table4.py ^
    --regs_year ../data/filtered_regressions_4_weeks_w_10_90_13.csv ^
    --h         13 ^
    --funds     ../data/funds_4_weeks_returns_2.csv ^
    --rf        ../data/risk_free_4_weeks_returns_2.csv ^
    --index     ../data/index_4_weeks_returns.csv ^
    --output    ../output/1/Table4.xlsx

python table5.py ^
    --data           ../data/filtered_regressions_4_weeks_w_10_90.csv ^
    --data_year      ../data/filtered_regressions_4_weeks_w_10_90_13.csv ^
    --data_decade    ../data/filtered_regressions_4_weeks_w_10_90_130.csv ^
    --data_lifetime  ../data/filtered_regressions_4_weeks_w_10_90_0.csv ^
    --output         ../output/1/Table5.xlsx

python table6.py ^
    --data_year      ../data/filtered_regressions_4_weeks_w_10_90_13.csv ^
    --data_decade    ../data/filtered_regressions_4_weeks_w_10_90_130.csv ^
    --data_lifetime  ../data/filtered_regressions_4_weeks_w_10_90_0.csv ^
    --weeks          4 ^
    --output         ../output/1/Table6.xlsx

python table7I.py ^
    --data           ../data/filtered_regressions_4_weeks_w_10_90.csv ^
    --data_year      ../data/filtered_regressions_4_weeks_w_10_90_13.csv ^
    --data_decade    ../data/filtered_regressions_4_weeks_w_10_90_130.csv ^
    --data_lifetime  ../data/filtered_regressions_4_weeks_w_10_90_0.csv ^
    --weeks          4 ^
    --output         ../output/1/Table7_I.xlsx

python table7II.py ^
    --data           ../data/filtered_regressions_4_weeks_w_10_90.csv ^
    --data_year      ../data/filtered_regressions_4_weeks_w_10_90_13.csv ^
    --data_decade    ../data/filtered_regressions_4_weeks_w_10_90_130.csv ^
    --data_lifetime  ../data/filtered_regressions_4_weeks_w_10_90_0.csv ^
    --weeks          4 ^
    --output         ../output/1/Table7_II.xlsx