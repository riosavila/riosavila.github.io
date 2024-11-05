foreach i in apple disney gmstop meta nvidia sp500 {
    import delimited "C:\Users\Fernando\Documents\GitHub\riosavila\rm-data\historical_data_`i'.csv", clear  varn(1) rowrange(4:2770)
    ren price date
    split date
    gen yd = date(date1,"YMD")
    drop date date1 date2
    keep yd close
    gen ticker = "`i'"
    format %td yd
    destring close, replace
    ren close `i'
    save stock_`i', replace
    
}

clear
use stock_sp500
merge 1:1 yd using stock_apple, nogen
merge 1:1 yd using stock_disney, nogen 
merge 1:1 yd using stock_gmstop, nogen
merge 1:1 yd using stock_meta, nogen
merge 1:1 yd using stock_nvidia, nogen

gen day=day(yd)
gen month=month(yd)
gen year =year(yd)
bysort year month:egen min=min(day)
keep if day==min
drop day month year min
gen ym = ym(year(yd),month(yd))
format %tm ym