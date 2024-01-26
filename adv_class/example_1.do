***************
*** PART I: ***
***************
*** Example for the estimation of Robust and Clustered Standard errors

** Load Data

frause wage2, clear

** Define your model Dependent and Independent variables 

global yvar wage
global xvar hours educ exper age married black south urban

** baseline model 

reg $yvar $xvar
est sto m_homosk

** Estimation of the model using Mata:

mata
	// Load data for Y in Mata, and define N of observations
	y = st_data(.,"$yvar"); n = rows(y)
	// Load Xvars, and add a constant with J(n,1,1)
	x = st_data(.,"$xvar"), J(n,1,1)
	// create relevant matrixes: X'X and X'y
	xx = cross(x,x); xy = cross(x,y);  ixx = invsym(xx)
	// define number of columns in X, as well as number of linearly independent variables
	// kx and krank will include the constant
	kx = cols(x); krank = rank(xx)
	// estimate beta = (X'X)^-1 X'y
	beta = ixx * xy
	// residuals
	res  = y:-x*beta
	// Now Consider the Robust Variance Formula = (X'X)^-1 X S X  (X'X)^-1
	// Where S is the variance covariance matrix.
	// A way to estimate the White Robust variance is to get the Influence functions defined as
	iff  = (x:*res) * ixx * n
	// Finally the variance covariance matrix is given by:
	vcv_0 = cross(iff,iff) /n^2
end

** Lets now put it all in a way that Stata can produce the nicely formated tables

// transfer a matrix from mata to Stata
mata: st_matrix("b", beta')
mata: st_matrix("V", vcv_0)

// add the following program 
capture {
program adde, eclass
	ereturn `0'
end
}
// The matrixes are unlabeled, so lets fix that
// I will get the names from the earlier regression:

qui:reg $yvar $xvar
global bname `:colname e(b)'

// rename all matrixes 
matrix colname b = $bname
matrix colname V = $bname
matrix rowname V = $bname

// Now we put everything into a format Stata understand:

// First we "post" results
adde post b V
// and store information for the "name" of the command that create this
adde local cmd myreg

// you could now store it as usual for later work, or just display it
est sto m_robust
ereturn display

esttab  m_homosk m_robust, se 

//// Now for Clustered Standard errors:

mata:
	// load variale for cluster. In this case iq
	cvar = st_data(.,"iq")
	// we need to sort data based on cvar (or more specifically create a variable that will sort the data)
	orden = order(cvar,1)
	// now sort the Cluster variable, and the Influence function
	cvar = cvar[orden,]
	iff  = iff[orden,]
	// set data as panel in mata
	info = panelsetup(cvar,1)
	// and "sum" all IFFs within cluster
	siff = panelsum(iff,info)
	// the rest is like before
	vcv_cl = cross(siff,siff)/n^2
	st_matrix("b", beta')
	st_matrix("V", vcv_cl)
	
end

// Rename
matrix colname b = $bname
matrix colname V = $bname
matrix rowname V = $bname
// we "post" results
adde post b V
// and store information for the "name" of the command that create this
adde local cmd myreg2
est sto m_cluster

esttab  m_homosk m_robust m_cluster, se 

// There will be a small difference in SE because of Degrees of freedom Adjusment
// Nevertheless, while not exact, this is what Stata does on the background

////////////////////////////////////////////////////////////////////////////////
// Part II: Cross validation

// the following is an example of how one could implement a k-fold cross validation

// Number of "folds"

global kf = 3

// creation of samples into kf random groups

xtile qkf = runiform(), n($kf)

// estimation of the model and prediction excluding 1 fold.
gen cv_yhat=.
forvalues i = 1  / $kf {
	qui:reg $yvar $xvar if qkf!=`i'  // This indicates to exclude group `i', 
	capture drop aux
	predict aux    
	replace cv_yhat = aux if qkf==`i' // Here we use the previous model to make predictions for the excluded group
}

// Estimation of RMSE (root of mean squared error) and MAE (mean of absolute error)

egen rmse = mean(($yvar-cv_yhat)^2)
replace rmse =sqrt(rmse )
egen mae = mean(abs($yvar-cv_yhat))

sum rmse mae

// You can repeat the process with different groups, or different specifications

////////////////////////////////////////////////////////////////////////////////
// Part III: Robinson Estimator
// The idea of Robinson estimator is in principle similar to the FWL theorem. 
// If you run a regression with the partialed out data, it would be the same as running the model with the full specification
// This is done commonly with Fixed Effects (Dummies), but Robinson proposes doing 
// the same with non-paramatric models
////////
// Same example as before, but now using experience as the nonparametric model:

// First Redefine the variables for the model: (exclude experience from xvar)

global yvar wage
global xvar hours educ age married black south urban
global zvar exper

// For the partialling out, we first make predictions with a non-parametric model 

foreach i in $yvar $xvar {
	lpoly `i' $zvar, degree(1) nograph gen(po_`i') at($zvar)
}

// then get the partiallout variables:
foreach i in $yvar $xvar {
	gen po2_`i' = `i'-po_`i'
}

// estimate the model as usual.

reg po2_wage po2_hours po2_educ po2_age po2_married po2_black po2_south po2_urban
// This is in essence the Robinson estimator.
est sto m1

// you can compare it with the standard one
reg $yvar $xvar $zvar
est sto m2

esttab m1 m2
// Estimating the nonparametric component
// first we get redisuals
qui:reg po2_wage po2_hours po2_educ po2_age po2_married po2_black po2_south po2_urban
predict res2,res
gen res = $yvar - ( hours*_b[po2_hours] + educ*_b[po2_educ]+age*_b[po2_age]+married*_b[po2_married]+black*_b[po2_black] + south*_b[po2_south]+urban*_b[po2_urban] )

// finally we can plot res vs experience

two lpolyci res $zvar if inrange($zvar,5,20), degree(1)

// Alternative, although SE are not obtained
gen nonpar = res - res2

two lpolyci res $zvar if inrange($zvar,5,20), degree(1) || scatter nonpar $zvar if inrange($zvar,5,20), connect(l) sort