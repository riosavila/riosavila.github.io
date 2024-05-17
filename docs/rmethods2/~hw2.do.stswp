//// HW2 Dofile
/// Part I: Testing

/// Drop mymtesting so the program can be run all at once
capture program drop mymtesting
program mymtesting, eclass
    syntax, [ n(int 100) k(int 1)]
	/// clear all data
	clear
	/// set number of observations. 
	set obs `n'
	/// create random variables (see help forvalues to go over more variable creation)
	forvalues i = 1/`k' {
		gen x`i'=rnormal()
	}
	/// tests for **all** X's if they have mean equal to zero or not
	/// here only 1
	
	
	/// test for each X
	
	/// Simple test
	local cnt_sng1 =0
	// notice im using a 5% significance level
	forvalues i = 1/`k' {
        mean x`i' 
		test x`i'
		if `r(p)'<=0.05 local cnt_sng1=1
	}
	
	/// bonferroni Correction
	local cnt_sng2 =0
	// Correction not implemented, since there is only 1 variable in this example
	forvalues i = 1/`k' {
        mean x`i'
		test x`i'
		if `r(p)'<=(0.05/`k') local cnt_sng2=1
	}
	
	/// Joint test: In this case, will be the same as before, because im ony using 1 variable. need to add more
	local cnt_jnt =0
    local allx
    forvalues i = 1/`k' {
        local allx `allx' x`i'
	}
    mean `allx'
	test `allx'
	if `r(p)'<=0.05 local cnt_jnt =1
	
	/// we put everything together in a matrix
	
	matrix b = `cnt_sng1', `cnt_sng2', `cnt_jnt'
	matrix colname b = mul_test, benf_test, joint_test
	ereturn post b
	
end

/// Now the simulation


simulate, reps(1000) dots(100): mymtesting, k(2) n(100)

/// the outcome is a dataset with all the "counts"
//  make summary of the data

sum


// Recommendation. Run the above command modifying K and N