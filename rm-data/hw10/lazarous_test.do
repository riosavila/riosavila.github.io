** Lazarous
* Disqualified
use "C:/Users/Fernando/Documents/GitHub/riosavila/rm-data/hhprice_train.dta", clear


*Models

* Model 1: distance and distance squared
gen distance_squared = distance^2

* Model 2: Adds rooms, bathroom, car, and landsize

* Model 3: Adds interactions with distance for all variables in Model 2

gen distance_rooms = distance * rooms
gen distance_bathroom = distance * bathroom
gen distance_car = distance * car
gen distance_buildingarea = distance * buildingarea
gen distance_yearbuilt = distance * yearbuilt 

regress price distance rooms bathroom car buildingarea yearbuilt distance_squared distance_rooms distance_bathroom distance_car distance_yearbuilt distance_buildingarea


use "C:/Users/Fernando/Documents/GitHub/riosavila/rm-data/hhprice_test.dta", clear


*Models

* Model 1: distance and distance squared
gen distance_squared = distance^2

* Model 2: Adds rooms, bathroom, car, and landsize

* Model 3: Adds interactions with distance for all variables in Model 2

gen distance_rooms = distance * rooms
gen distance_bathroom = distance * bathroom
gen distance_car = distance * car
gen distance_buildingarea = distance * buildingarea
gen distance_yearbuilt = distance * yearbuilt 

predict price_hat

gen mse = (price-price_hat)^2
sum mse
display sqrt(`r(mean)')


