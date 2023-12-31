*program drop _parse_smqreg 
program _parse_smqreg , rclass
	syntax anything
	
	gettoken p1 p2:0, parse("()")
	gettoken y   x :p1 
	local p2 `=subinstr("`p2'","(","",.)'
	local p2 `=subinstr("`p2'",")","",.)'
	gettoken y1  z :p2 , parse("=")
	local z  `=subinstr("`z'","=","",.)'
	return local yvar   `y'
	return local xvar   `x'
	if "`y1'"!="" return local y1var  `y1'
	if "`z'"!="" return local zvar   `z'
end
*program drop smqreg
program smqreg,
        if replay() {
                if `"`e(cmd)'"' != "smqreg" { 
                        error 301
                }
                else {
                        ereturn display
                }
                exit
        }
		else {
			smqreg_wh `0'
		}
	
end

program smqreg_wh, eclass
syntax anything [if] [in] [aw pw iw fw], [Quantile(str) * kernel(str) bw(str) from(str)]
	** Stripdown variables
	if "`quantile'"=="" local quantile 50
	numlist "`quantile'" , range(>0 <100)
	if `quantile'<1 {
		local q = `quantile'
	}
	else {  
		local q = `quantile'/100
	}
	_parse_smqreg `anything'
	local y   `r(yvar)'
	local x   `r(xvar)'
	if "r(y1var)"!=""	local y1   `r(y1var)'
	if "r(zvar)"!=""    local z    `r(zvar)'
 	marksample touse, novar
	
	markout    `touse' `y' `x' `y1' `z'
 	**get Initial values
	tempname bini
	qui:reg `y' `x' `y1' if `touse' [`weight'`exp']
	matrix `bini'=e(b)
	tempvar res
	qui:predict `res', res
	if "`bw'"=="" {
		if "`weight'"!="" local wwgt  aw 
		qui:kdensity `res' [`wwgt'`exp'], nograph kernel(gaussian)
		local bw = `=r(bwidth)'
	}
	else {
		numlist "`bw'" , range(>0)
	}
	**estimate Smooth GMM
	
	if "`from'"!="" local bini `from'
	
	if "`from'"=="" | "`z'`y1'"=="" {
		gmm ( normal( ({q: `x' `y1' _cons}-`y')/`bw' ) - `q' ) if `touse' [`weight'`exp'], ///
			instruments(`x' `y1') `options' from(`bini')  derivative(/q =1/`bw'*normalden ( ({q:}-`y')/`bw' ))
		tempname bini
		matrix `bini'=e(b)
	}
	**estimate IV
	if "`z'`y1'"!="" {
		gmm ( normal( ({q: `x' `y1' _cons}-`y')/`bw' ) - `q' ) if `touse' [`weight'`exp'], ///
			instruments(`x' `z')  `options' from(`bini')   derivative(/q =1/`bw'*normalden ( ({q:}-`y')/`bw' ))
	}
	
	ereturn local cmd smqreg
	ereturn local cmdline smqreg `0'
	ereturn local bw `bw'
end