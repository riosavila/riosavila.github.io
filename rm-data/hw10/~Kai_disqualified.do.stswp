*KaiLin

** load data
use "C:/Users/Fernando/Documents/GitHub/riosavila/rm-data/hhprice_train.dta", clear

** inspect data
describe
summarize

** run a simple regression
regress price rooms distance
** here is what i learned: R-squard is 0.3091, 31% of variability is explained by rooms and distance. both number of rooms and distance are signficant predictors but need to add other variables. more rooms = greater price, greater distance = lower price

** look at AIC and BIC
estat ic
** AIC=203799 BIC=203820.1

** create training and test samples 
set seed 12345
gen rand = runiform()
gen train = rand < 0.8

** rerun with training data 
regress price rooms distance if train == 1

** predictions on test data
predict yhat if train == 0

** calculate prediction error
gen error = (price - yhat)^2 if train == 0
summarize error, meanonly

** assess model performance
display sqrt(r(mean))
** 52064.576. oops too high. lets try again

clear 

** TEST MODEL TWO

** load data
use "C:/Users/Fernando/Documents/GitHub/riosavila/rm-data/hhprice_train.dta", clear

** inspect data
describe
summarize

** run regression. this time with more variables. also include bathrooms, car space, land size, building area, and the year built
regress price rooms distance bathroom car landsiz buildingarea yearbuilt 

** look at AIC and BIC
estat ic
**AIC=96868.54 BIC=96918.87

** create training and test samples
set seed 12345
gen rand = runiform()
gen train = rand < 0.8

** rerun with training data 
regress price rooms distance bathroom car landsiz buildingarea yearbuilt if train == 1

** predictions on test data
predict yhat if train == 0

** calculate prediction error
gen error = (price - yhat)^2 if train == 0
summarize error, meanonly

**assess model performance
display sqrt(r(mean))
**43718.453. slightly better. need to figure out how to compare AIC and BIC

clear 

** TEST MODEL THREE 

**load data
use "C:/Users/Fernando/Documents/GitHub/riosavila/rm-data/hhprice_train.dta", clear

** create squared terms
gen rooms_squared = rooms^2
gen landsize_squared = landsiz^2

** run new regression
regress price rooms rooms_squared distance bathroom car landsize landsize_squared buildingarea yearbuilt

** look at AIC and BIC
estat ic
** AIC=96846 BIC=96908.92

** create training and test samples 
set seed 12345
gen rand = runiform()
gen train = rand < 0.8

** rerun with training data
regress price rooms rooms_squared distance bathroom car landsize landsize_squared buildingarea yearbuilt if train == 1

** predictions on test data
predict yhat if train == 0

** calculate prediction error 
gen error = (price - yhat)^2 if train == 0
summarize error, meanonly

** assess model performance
display sqrt(r(mean))
** 43635.011.. well thats a little better than the other two... 

** Final model based on Line 98
regress price rooms rooms_squared distance bathroom car landsize landsize_squared buildingarea yearbuilt

use "C:/Users/Fernando/Documents/GitHub/riosavila/rm-data/hhprice_test.dta", clear

** create squared terms
gen rooms_squared = rooms^2
gen landsize_squared = landsiz^2

** Final model based on Line 98
predict price_hat

gen mse = (price-price_hat)^2
sum mse
display sqrt(`r(mean)')


