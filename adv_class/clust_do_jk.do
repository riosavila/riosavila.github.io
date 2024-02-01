gen n=_n
*sort idcode
mata
	y = st_data(.,"ln_wage"); n=rows(y)
	x = st_data(.,"race msp union "),J(n,1,1)
	cv = st_data(.,"n") 
	info = panelsetup(cv,1);kcv = rows(info)
	xx = cross(x,x); xy = cross(x,y)
	bb = J(kcv,rank(xx),0)
	for(i=1;i<=kcv;i++){
		sx = panelsubmatrix(x,i,info)
		sy = panelsubmatrix(y,i,info)
		sbb = invsym(xx-cross(sx,sx))*(xy-cross(sx,sy))
		bb[i,]=sbb'
	}
	bt = invsym(xx)*xy
	rbb=bb:-bt'
	//bt'
	bt,sqrt(diagonal(cross(rbb,rbb)))
end
