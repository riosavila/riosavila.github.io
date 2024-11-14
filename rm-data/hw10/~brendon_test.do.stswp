** Brandon
use "C:/Users/Fernando/Documents/GitHub/riosavila/rm-data/hhprice_train.dta", clear

gen log_price = log(price)
gen log_land = log(landsize)
gen log_dis = log(distance)
gen log_ba = log(building area)
gen log_pc = log(prop_count)


gen manyb_room =.
replace manyb_room =0 if bathroom<2
replace manyb_room =1 if bathroom>1

gen goodagent =0
replace goodagent =1 if inlist(sellerg2, 3, 19, 33, 45, 50, 77, 88, 95, 100, 104, 126, 127, 151, 155, 227)
*the agents that have the highest significent coefficent when regressing with log_price

gen goodsuburb =0
replace goodsuburb =1 if inlist(suburb, 5, 12, 14, 22, 23, 27, 42, 43, 59, 61, 62, 63, 109, 138, 146, 150, 163, 172, 173, 185, 186, 197, 200, 273, 278)

gen best_date = inlist(month(date), 10, 11, 12)
*some research indicates last 3 months of the year have higher sell prices 

keep if inrange(price, 30000, 400000)
*removing outlier properties because their price likely reflects qualities that are not captured by any of the variables
drop if yearbuilt<1900
*removing houses where extreme age likely effects price in a way not captured by current variables, such as historic value. 


summarize price buildingarea landsize rooms bathroom car yearbuilt price1000 distance

histogram price
histogram rooms
histogram bathroom
histogram bedroom2
histogram yearbuilt
histogram prop_count

*** Model 1: House Characteristics ***
reg log_price rooms manyb_room car yearbuilt type_h, robust
estat ic
*car spots does not have a statistically significent impact in this model
*year build is only measured for half the sample

*** Model 2: Area and Agent Characteristics  *** 
reg log_price distance log_land goodagent goodsuburb prop_count, robust
estat ic
*building area is only measured for about half of the sample
*prop_count has a low impact and t value

*** Model 3: Combined Model ***
reg log_price rooms manyb_room type_h distance goodagent goodsuburb, robust
estat ic
*kept best variables from previous model, each remaining variable has a statistically significent meaningful impact on price, with a relatively high robust r-squared and lower BIC then previous regressions 

use "C:/Users/Fernando/Documents/GitHub/riosavila/rm-data/hhprice_test.dta", clear

gen log_price = log(price)
gen log_land = log(landsize)
gen log_dis = log(distance)
gen log_ba = log(building area)
gen log_pc = log(prop_count)


gen manyb_room =.
replace manyb_room =0 if bathroom<2
replace manyb_room =1 if bathroom>1

gen goodagent =0
replace goodagent =1 if inlist(sellerg2, 3, 19, 33, 45, 50, 77, 88, 95, 100, 104, 126, 127, 151, 155, 227)
*the agents that have the highest significent coefficent when regressing with log_price

gen goodsuburb =0
replace goodsuburb =1 if inlist(suburb, 5, 12, 14, 22, 23, 27, 42, 43, 59, 61, 62, 63, 109, 138, 146, 150, 163, 172, 173, 185, 186, 197, 200, 273, 278)

gen best_date = inlist(month(date), 10, 11, 12)
*some research indicates last 3 months of the year have higher sell prices 

 *removing outlier properties because their price likely reflects qualities that are not captured by any of the variables
 *removing houses where extreme age likely effects price in a way not captured by current variables, such as historic value. 


summarize price buildingarea landsize rooms bathroom car yearbuilt price1000 distance

predict target_hat


gen mse = (ln(price)-target_hat)^2
total mse

