** HW3
** P1

frause labsup, clear

* q11.
reg hours kids educ age c.age#c.age hispan black nonmomi
est sto m0
* q12. Discussion

qui:ivregress 2sls hours educ age c.age#c.age hispan black nonmomi (kids = samesex)
est sto m1
qui:ivregress 2sls hours educ age c.age#c.age hispan black nonmomi (kids = multi2nd)
est sto m2
qui:ivregress 2sls hours educ age c.age#c.age hispan black nonmomi (kids = samesex multi2nd)
est sto m3

esttab m0 m1 m2 m3

** Instrument strength

qui:reg  kids samesex educ age c.age#c.age hispan black nonmomi 
predict res1, res
test samesex
qui:reg  kids multi2nd educ age c.age#c.age hispan black nonmomi 
predict res2, res
test multi2nd 
qui:reg  kids samesex multi2nd educ age c.age#c.age hispan black nonmomi 
predict res3, res
test samesex  multi2nd , 

** THey are strong, but Multi is stronger than "same sex"
**
**q132: effects do change

esttab m0 m1 m2 m3, keep(kids) se
** far less precise, and Same sex is stronger (yet non significant)

** Are #kids Endogenous? Endogeneity test
reg hours kids educ age c.age#c.age hispan black nonmomi res1
est sto m1b
reg hours kids educ age c.age#c.age hispan black nonmomi res2
est sto m2b
reg hours kids educ age c.age#c.age hispan black nonmomi res3
est sto m3b

esttab m1b m2b m3b, keep(res*) se

** No, in all cases we cannot reject the Null of no endogeneity


* P2.

frause smoke, clear

gen smoker = cigs>0
** agesq may be excluded
reg smoker educ white age c.age#c.age lincome  lcigpric restaurn
est sto m1
probit smoker educ white age c.age#c.age lincome  lcigpric restaurn
est sto m2
margins, dydx(*) post
est sto m3
esttab m1 m2 m3, mtitle(lpm probit mfx_probit) se

** Both models provide remarkably similar results. The ban reduced the probability of smoking (among those affected by the ban) of about 10%

*q22

poisson cigs educ white age c.age#c.age lincome  lcigpric restaurn, 
margins, dydx(*) post
est sto m1
tobit cigs educ white age c.age#c.age lincome  lcigpric restaurn, ll(0) 
margins, dydx(*) post predict(ystar(0,.))
est sto m2
esttab m1 m2 , mtitle(poisson tobit) se

** Both predict very similar impacts of the ban. A reduction of just over 3 cigs per day.
** in terms of Cig Prices. This variable is non significant, and has a very small impact on #cig. 
** a 10% increase would reduce # of cigs in 0.09 (poisson) or 0.13 (cigs). Or about 1 fewer cigarate every 10 individuals.

** Something to note. POisson and Tobit have very different significance levels. This should make you suspect on the results.
** If you add Robust to poisson (and vce(robust) to tobit), you should be able to see the results are comparable

poisson cigs educ white age c.age#c.age lincome  lcigpric restaurn,  robust
margins, dydx(*) post
est sto m1
tobit cigs educ white age c.age#c.age lincome  lcigpric restaurn, ll(0)  vce(robust)
margins, dydx(*) post predict(ystar(0,.))
est sto m2
esttab m1 m2 , mtitle(poisson tobit) se

*q23

qui:tobit cigs educ white age c.age#c.age lincome  lcigpric restaurn, ll(0)  
margins, dydx(*) post predict(pr(0,.))
est sto m3

qui:reg smoker educ white age c.age#c.age lincome  lcigpric restaurn
margins, dydx(*) post

est sto m1
qui:probit smoker educ white age c.age#c.age lincome  lcigpric restaurn
margins, dydx(*) post
est sto m2

esttab m1 m2 m3, mtitle(LPM probit tobit_pr) se

** Tobit assumes that the same coefficients affects intensity and probability . Which can be strong.
** Here, however, they seem reasonable, as we would reach the same conclusion regardless of the model. A decline in the P of smoking of around 10%

***
**Q3

frause driving, clear
reg totfatrte i.seatbelt minage zerotol unem perc14_24 vehicmiles
** Weird conclusion. Seatbelt increases fatality rate!
** potential heterogeneity bias

* RE FE CRE
xtset state year 
xtreg totfatrte i.seatbelt minage zerotol unem perc14_24 vehicmiles, re
est sto re
xtreg totfatrte i.seatbelt minage zerotol unem perc14_24 vehicmiles, fe
est sto fe
**
fra install cre
cre, abs(state) keep: xtreg totfatrte i.seatbelt minage zerotol unem perc14_24 vehicmiles, re
est sto cre

esttab re fe cre, se mtitle(RE FE CRE)

** Controling for FE makes a huge difference. Seatbleats actually reduced fatality rate. 

** For choosing between RE and FE: Hausman test

 hausman fe re
 ** wil give you -17.22 Error!

 ** Better approach CRE
 
cre, abs(state) keep: xtreg totfatrte i.seatbelt minage zerotol unem perc14_24 vehicmiles, re 
test m1__1_seatbelt m1__2_seatbelt m1_minage m1_zerotol m1_unem m1_perc14_24 m1_vehicmiles

** the Null is rejected. So FE is prefered over RE (mostly because of Unemployment)




