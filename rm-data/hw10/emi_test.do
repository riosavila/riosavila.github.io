** EMI
*Data

use "C:/Users/Fernando/Documents/GitHub/riosavila/rm-data/hhprice_train.dta", clear

gen target = log(price)

levelsof suburb      , local(lcn3)
foreach i of local lcn3 {
      gen suburb_`i' = suburb==`i'

}

qui:reg target bedroom2 i.suburb
est sto m1
esttab m1, keep(bedroom2 _cons)

use "C:/Users/Fernando/Documents/GitHub/riosavila/rm-data/hhprice_test.dta", clear

gen target = log(price)

levelsof suburb      , local(lcn3)
foreach i of local lcn3 {
      gen suburb_`i' = suburb==`i'

}

predict target_hat


gen mse = (target-target_hat)^2
total mse