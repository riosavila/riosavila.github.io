
/****************
# FOR I-O TABLE

k-sectors -> Number of Sectors
+1 for Households <- Balancing

mmax and mmin <- Max a Min dependence

p <-- P of 0 
******************/

mata
mata clear
class iodata {
    real scalar ksectors
    real scalar mmax
    real scalar mmin
    real scalar p
    real matrix data_gen()
}

real matrix iodata::data_gen(){
    real matrix iomatrix, hhfd, tprod
    real scalar good

    
    good = 0
    for(good=0;good<=0;good){
        iomatrix = runiformint(ksectors,ksectors,mmin,mmax)
        prob0    = rbinomial(ksectors,ksectors,1,p)
        iomatrix = iomatrix :* (1:-prob0)
        hhfd     = runiformint(ksectors,1,mmin,mmax)
        tprod    = rowsum((iomatrix,hhfd))
        tdemand  = tprod':-colsum(iomatrix)

        if (min(tdemand)>0) good=1
    }   
    return ((iomatrix,hhfd,tprod)\(tdemand,0,sum( tdemand)) \ (tprod',sum(hhfd),sum(tprod)+sum(hhfd)))
}
    
end

mata:io=iodata()
mata:io.ksectors=3
mata:io.p=0.01
mata:io.mmin=50
mata:io.mmax=200
mata:iodata=io.data_gen()
mata:iodata
sss
mata:tx = iodata[,6]
mata:ty = iodata[,5]
mata:fct = iodata:/iodata[6,];  