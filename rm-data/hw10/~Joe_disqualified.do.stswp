** JOE
** Disqualified

use "C:/Users/Fernando/Documents/GitHub/riosavila/rm-data/hhprice_train.dta", clear
drop latitud

drop longitud

* Model 1 - Is Price dependant upon Bed+Bathrooms?

gen bedbath =bathroom + bedroom2

regress price bedbath

* Model 2 - Aggregate of positive factors impact on price 

gen aggregate = bedbath + buildingarea + car + rooms + landsize

regress price aggregate

gen log_aggregate = log(aggregate)

regress price log_aggregate

* Model 3 -

gen distance_date= distance * date

gen distance_yb = distance* yearbuilt

gen distance_bb= distance * bedbath

regress price distance_date distance_yb distance_bb

use "C:/Users/Fernando/Documents/GitHub/riosavila/rm-data/hhprice_test.dta", clear

gen bedbath =bathroom + bedroom2

gen aggregate = bedbath + buildingarea + car + rooms + landsize

gen log_aggregate = log(aggregate)


* Model 3 -

gen distance_date= distance * date

gen distance_yb = distance* yearbuilt

gen distance_bb= distance * bedbath

predict price_hat

gen mse = (price-price_hat)^2
sum mse
display sqrt(`r(mean)')