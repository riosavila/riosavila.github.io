* Analysis of Apple vs SP500 Returns 2010-2020
clear all
set more off

* Load and prepare data
use stock_apple.dta, clear
merge 1:1 date using stock_sp500.dta, keep(3)
keep if year(date)>=2010 & year(date)<=2020

* Generate monthly returns
gen month = mofd(date)
format month %tm

* Calculate returns
sort date
by month: egen apple_price = lastof(price)
by month: egen sp500_price = lastof(sp500)

sort month
gen apple_ret = (apple_price/apple_price[_n-1] - 1)*100 if month>month[_n-1]
gen sp500_ret = (sp500_price/sp500_price[_n-1] - 1)*100 if month>month[_n-1]

* Keep only month-end data
by month: keep if _n==_N
drop if missing(apple_ret, sp500_ret)

* Summary Statistics
tabstat apple_ret sp500_ret, stats(n mean sd min max) col(stat)

* Regression Analysis
reg apple_ret sp500_ret, robust

* Visualizations

* Time series plot of returns
twoway (line apple_ret month, lcolor(blue)) ///
       (line sp500_ret month, lcolor(green)), ///
       title("Stock and Market Returns over Time") ///
       ytitle("Monthly returns (percent)") ///
       legend(label(1 "Apple") label(2 "S&P500"))
graph export returns_time.png, replace

* Scatter plot with regression line
twoway (scatter apple_ret sp500_ret) ///
       (lfit apple_ret sp500_ret) ///
       (function y = x, range(sp500_ret)), ///
       title("Returns on Apple and Market Returns") ///
       xtitle("S&P 500 index monthly returns (percent)") ///
       ytitle("Apple stock monthly returns (percent)") ///
       legend(label(1 "Monthly returns") ///
              label(2 "reg line") ///
              label(3 "45 degree line"))
graph export returns_scatter.png, replace
