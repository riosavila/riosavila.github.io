clear
set obs 2000
gen r0 = runiform() 
gen r1 = 0.5*(runiform() +r0)
gen r2 = 0.5*(runiform() +r0)
scatter r1 r2, xlabel("",nogrid) ylabel("",nogrid) ///
               yscale(noline) xscale(noline)  ///
               ytitle("") xtitle("") aspect(1) ///
               ysize(6) xsize(6)
cluster kmeans r1 r2, k(100) name(qr0)
bysort qr0: gen sel2 = runiform()
bysort qr0: gen sel = sel2[1]<.1
drop sel2
                            
               
gen qr1 = floor(r1*10)+1
gen qr2 = floor(r2*10)+1
gen rx = runiform()
sort qr1 qr2 rx
by qr1 qr2 :gen sel2 = _n<=(0.1*_N)
by qr1 qr2 :replace sel2 = 1 if _n==1
set scheme white2
two (scatter r1 r2,  mcolor(%40)) (scatter r1 r2 if runiform()<.1, msize(2) mcolor(%70) ) ///
               , xlabel("",nogrid) ylabel("",nogrid) ///
               yscale(noline) xscale(noline)  ///
               ytitle("") xtitle("") aspect(1) ///
               ysize(6) xsize(6) legend(off)  xline(0(.1)1) yline(0(.1)1)            
graph export "C:\Users\Fernando\Documents\GitHub\rm-data-analysis\Slides\images\paste-1.png", replace        
two (scatter r1 r2,  mcolor(%40)) (scatter r1 r2 if sel, msize(2) mcolor(%70) ) ///
               , xlabel("",nogrid) ylabel("",nogrid) ///
               yscale(noline) xscale(noline)  ///
               ytitle("") xtitle("") aspect(1) ///
               ysize(6) xsize(6) legend(off)  xline(0(.1)1) yline(0(.1)1)
graph export "C:\Users\Fernando\Documents\GitHub\rm-data-analysis\Slides\images\paste-2.png", replace 
two (scatter r1 r2,  mcolor(%40)) (scatter r1 r2 if sel2, msize(2) mcolor(%70) ) ///
               , xlabel("",nogrid) ylabel("",nogrid) ///
               yscale(noline) xscale(noline)  ///
               ytitle("") xtitle("") aspect(1) ///
               ysize(6) xsize(6) legend(off) xline(0(.1)1) yline(0(.1)1)
graph export "C:\Users\Fernando\Documents\GitHub\rm-data-analysis\Slides\images\paste-3.png", replace                