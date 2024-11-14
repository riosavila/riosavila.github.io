** Shane Test
use "C:/Users/Fernando/Documents/GitHub/riosavila/rm-data/hhprice_train.dta", clear

ssc install cv_kfold
ssc install cv_regress
ssc install geodist

gen ln_price = log(price)
summarize bathroom
local mid_bath = (r(min) + r(max)) / 2
gen bath_distance = abs(bathroom - `mid_bath')
gen bath_adj = 1 / (1 + bath_distance)
summarize bedroom2
local mid_bed = (r(min) + r(max)) / 2
gen bed_distance = abs(bedroom2 - `mid_bath')
gen bed_adj = 1 / (1 + bed_distance)
summarize longitud, detail
local longitud_median = r(p50)
gen longitud_distance = abs(longitud - `longitud_median')
gen lon_prox = 1 / (1 + longitud_distance)
summarize latitud
scalar mean_lat = r(mean)
gen closeness_to_mean_lat = abs(latitud - mean_lat)
gen lat_prox = 1 / (1 + closeness_to_mean_lat)
geodist latitud longitud -37.8136 144.9631, generate(dist_cbd)
gen dist_cbd_car = dist_cbd * car
gen ln_area = log(buildingarea)
gen area_sq = buildingarea^2
gen dist_sq = distance^2
gen ln_dist = log(distance)
gen dist_car = distance * car
gen cbd_car2 = log(dist_cbd) * car
gen bath_sq = bathroom^2
gen bed_sq = bedroom2^2
gen lat2 = latitud^2
gen lon2 = longitud^2
gen lat3 = latitud^3
gen lon3 = longitud^3
gen latlon = latitud * longitud
gen bedroom3 = bedroom2^3
gen bedroom4 = bedroom2^4
gen ln_land = log(landsize)
gen land_area = ln_land * ln_area
geodist latitud longitud -37.8  145, generate(dist_center)
gen ln_dist_center = log(dist_center)
gen sqrt_dist_center = sqrt(dist_center)
gen sq_dist_center = dist_center^2
gen bed_spline1 = bedroom2 if bedroom2 <= 5
replace bed_spline1 = 5 if bedroom2 > 5
gen bed_spline2 = 0 if bedroom2 <= 5
replace bed_spline2 = bedroom2 - 5 if bedroom2 > 5
mkspline latspline = latitud, knots(-38, -37.8, -37.6) cubic 
mkspline lonspline = longitud, knots(144.8, 145, 145.2) cubic

* NO NEED TO RUN PAST THIS 

** estra No year
replace yearbuilt = 99 if yearbuilt==.
gen dln_area = ln_area==.
replace ln_area = 0 if ln_area==.

reg ln_price i.suburb i.region i.type i.bedroom2 i.bathroom i.car i.region#i.bed_spline* ln_area i.yearbuilt ln_land c.ln_area#c.ln_land sq_dist_center dist_cbd_car date c.date#c.ln_area c.date#i.bedroom2 c.date#c.ln_land c.date#c.cbd_car2 dln_area


use "C:/Users/Fernando/Documents/GitHub/riosavila/rm-data/hhprice_test.dta", clear
 sum latitud
replace latitud = r(mean) if latitud==.
sum longitud
replace longitud= r(mean) if longitud==.
gen target = log(price)

gen ln_price = log(price)
summarize bathroom
local mid_bath = (r(min) + r(max)) / 2
gen bath_distance = abs(bathroom - `mid_bath')
gen bath_adj = 1 / (1 + bath_distance)
summarize bedroom2
local mid_bed = (r(min) + r(max)) / 2
gen bed_distance = abs(bedroom2 - `mid_bath')
gen bed_adj = 1 / (1 + bed_distance)
summarize longitud, detail
local longitud_median = r(p50)
gen longitud_distance = abs(longitud - `longitud_median')
gen lon_prox = 1 / (1 + longitud_distance)
summarize latitud
scalar mean_lat = r(mean)
gen closeness_to_mean_lat = abs(latitud - mean_lat)
gen lat_prox = 1 / (1 + closeness_to_mean_lat)
geodist latitud longitud -37.8136 144.9631, generate(dist_cbd)
gen dist_cbd_car = dist_cbd * car
gen ln_area = log(buildingarea)
gen area_sq = buildingarea^2
gen dist_sq = distance^2
gen ln_dist = log(distance)
gen dist_car = distance * car
gen cbd_car2 = log(dist_cbd) * car
gen bath_sq = bathroom^2
gen bed_sq = bedroom2^2
gen lat2 = latitud^2
gen lon2 = longitud^2
gen lat3 = latitud^3
gen lon3 = longitud^3
gen latlon = latitud * longitud
gen bedroom3 = bedroom2^3
gen bedroom4 = bedroom2^4
gen ln_land = log(landsize)
gen land_area = ln_land * ln_area
geodist latitud longitud -37.8  145, generate(dist_center)
gen ln_dist_center = log(dist_center)
gen sqrt_dist_center = sqrt(dist_center)
gen sq_dist_center = dist_center^2
gen bed_spline1 = bedroom2 if bedroom2 <= 5
replace bed_spline1 = 5 if bedroom2 > 5
gen bed_spline2 = 0 if bedroom2 <= 5
replace bed_spline2 = bedroom2 - 5 if bedroom2 > 5
mkspline latspline = latitud, knots(-38, -37.8, -37.6) cubic 
mkspline lonspline = longitud, knots(144.8, 145, 145.2) cubic

replace yearbuilt = 99 if yearbuilt==.
gen dln_area = ln_area==.
replace ln_area = 0 if ln_area==.

predict target_hat

gen mse = (ln(price)-target_hat)^2
total mse

