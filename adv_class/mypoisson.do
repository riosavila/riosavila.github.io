clear
set obs 1000
gen r1 = rnormal()
gen x1 = 1+rnormal()+r1
gen x2 = 1+rnormal()+r1
gen  ey = exp(0.5+0.5*x1-0.5*x2)

gen  y = rpoisson(ey)

gen yc = max(3,y)

capture program drop mypoisson
program mypoisson
	args lnf lambda
	qui {
		replace `lnf' = $ML_y1* (`lambda')  - exp(`lambda') - lnfactorial($ML_y1)
	}
end

ml model lf mypoisson (y= x1 x2)
ml maximize

capture program drop mypoissonc
program mypoissonc
	args lnf lambda
	qui {
		// To be modified
	}
end