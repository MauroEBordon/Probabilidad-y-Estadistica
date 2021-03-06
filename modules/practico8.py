import math
from scipy import integrate
from pynverse import inversefunc
from definiciones import *

def ej1():
	print("a) R1, estamos haciendo una prueba bilateral")
	print("b) X~B(25, 0.5)")
	pt, ct, e, _, _ = binomial_dist(25, 0.5)
	err1 = ct[7] + 1 - ct[18]
	err2 = ct[18] - ct[7]
	print("   err1 =", "%.3f"%err1)
	print("c)")
	pt, ct, _, _, _ = binomial_dist(25, 0.3)
	err2 = ct[18] - ct[7]
	print("   if p = 0.3: err2 =", "%.3f"%err2)
	pt, ct, _,_,_ = binomial_dist(25, 0.4)
	err2 = ct[18] - ct[7]
	print("   if p = 0.4: err2 =", "%.3f"%err2)
	pt, ct, _,_,_ = binomial_dist(25, 0.6)
	err2 = ct[18] - ct[7]
	print("   if p = 0.6: err2 =", "%.3f"%err2)
	
	pt, ct, _,_,_ = binomial_dist(25, 0.7)
	err2 = ct[18] - ct[7]
	print("   if p = 0.7: err2 =", "%.3f"%err2)
	
	print("d)")
	print("   Como 6 pertenece a la región de rechazo, rechazamos la hipótesis nula.")

def ej2():
	print("a) Hipotesis alternativa del tipo bilateral:")
	print("   H0: μ = 10")
	print("   Ha: μ != 10")
	print("   estadístico de prueba: Z")
	izq = 9.8968  
	der = 10.1032
	e = 10
	d = 0.2
	n = 25
	err1 = ph_mean_err1(e,d,n,izq,der,case='A', hip='equal')
	print("b) P(revisar en vano) =", "%.4f"%err1)
	x = 10.1
	err2 = ph_mean_err2(x,d,n,e,err1,case='A', hip='equal')
	print("c) P(rechazar revision con μ = 10.1) =", "%.3f"%err2)
	x = 9.8
	err2 = ph_mean_err2(x,d,n,e, err1,case='A', hip='equal')
	print("   P(rechazar revision con μ = 9.8) =", "%.3f"%err2)

	zde = math.sqrt(n) * (der-10)/d
	print("d) c =", "%.2f"%zde)

def ej3():
	ans = z_prob(a=1.88)
	print("a)", "%.4f"%ans)
	ans = z_prob(b=-2.75)
	print("b)", "%.3f"%ans)
	ans = 1 - z_prob(a=-2.88, b=2.88)
	print("c)", "%.3f"%ans)

def ej4():
	x = 94.32
	d = 1.2
	n = 16
	e = 95
	a = 0.01
	if ph_mean_result(x,d,n,e,a,hip='equal', case='A'):
		print("a) La hipotesis nula se rechaza")
	else:
		print("a) No se rechaza la hipótesis nula porque x no cayó en el RR")
	x = 94
	b = ph_mean_err2(x, d, n, e, a, hip='equal', case='A')
	print("b)", "%.3f"%b)
	b = 0.1
	c = ph_mean_n(x,d,e,a, b, hip='equal')
	print("c)", "%.3f"%c)

def ej5():
	print("a) P(tobs fuera del RR) =", "%.3f"%t.cdf(1.6, 12))
	print("Prevalece la hipótesis nula. Personalmente me parece que al estar a 0.043 de ser rechazada se debería retomar la prueba\n")
	print("b) misma conclución que en el inciso b).\n")
	print("c) P(tobs fuera del RR) =", "%.3f"%t.cdf(2.6, 24))
	print("   la observacion está en el RR, se rechaza H0.")

def ej6():
	x = 370.69
	d = 24.26
	n = 26
	e = 360
	a = ph_mean_err1(x, d, n, e, 1, hip='less', case='C')
	print("Hay una probabilidad de", "%.3f"%a, "de que dada una media de 360 la media muestral haya resultado 370.69.\n")
	print("Con un nivel de significación de 0.05 se rechazaría la hipótesis nula.")

def ej7():
	x = 73.1
	s = 5.9
	n = 42
	e = 75
	a = 0.01
	if ph_mean_result(x,s,n,e,a,hip='less', case='B'):
		print("a) La hipotesis nula se rechaza")
	else:
		print("a) La hipotesis nula prevalece")
	x = 70
	b = ph_mean_err2(x,s,n,e,a,hip='less', case='B')
	print("b)  β(70) =", "%.4f"%b)

def ej8():
	x = 3.72
	s = 1.25
	n = 8
	e = 3.5
	a = 0.05
	if ph_mean_result(x,s,n,e,a,hip='greater', case='C'):
		print("a) La hipotesis nula se rechaza")
	else:
		print("a) La hipotesis nula prevalece")
	x = 4
	b = ph_mean_err2(x,s,n,e,a,hip='greater', case='A')
	print("b) error tipo II =", "%.3f"%b)

def ej9():
	n = 150
	x = 92/150
	p = 0.4
	a = 0.01
	if ph_prop_result(x,p,n,a,hip='equal'):
		print("nivel de significancia 0.01: La hipotesis nula se rechaza")
	else:
		print("nivel de significancia 0.01: La hipotesis nula prevalece")

	a = 0.05
	if ph_prop_result(x,p,n,a,hip='equal'):
		print("nivel de significancia 0.05: La hipotesis nula se rechaza")
	else:
		print("nivel de significancia 0.05: La hipotesis nula prevalece")

def ej10():
	x = 5/500
	n = 500
	p = 0.03
	a = 0.01
	d = math.sqrt(p * (1-p))
	pv = p_value(x,d,n,p,est='Z', hip='less')
	print("los robots siempre nos van a ganar")
	if ph_prop_result(x,p,n,a,hip='less'):
		print("con un p-valor de", "%.4f"%pv," La hipotesis nula se rechaza")
	else:
		print("con un p-valor de", "%.4f"%pv," La hipotesis nula prevalece")

def ej11():
	x = 2.72
	s = 0.41
	n = 16
	e = 2.5
	a = 0.05
	pv = p_value(x,s,n,e,est='T', hip='greater')
	if ph_mean_result(x,s,n,e,a,hip='greater', case='C'):
		print("con un p-valor de", "%.3f"%pv, "el implante de hormonas es exitoso")
	else:
		print("con un p-valor de", "%.3f"%pv, "el implante de hormonas es innecesario")

def ej12():
	print("a) H0 prevalece")
	print("b) H0 prevalece")
	print("c) H0 prevalece")
	print("d) H0 se rechaza")
	print("e) H0 prevalece")
	print("f) H0 prevalece")

def ej13():
	a = 0.05
	n = 1
	d = 1
	x = 1.42
	za = norm.ppf(a)
	za2 = norm.ppf(a/2)
	pv = 1 - norm.cdf(x)
	print("a)")
	if pv < a:
		print("   i) con un p-valor de", "%.4f"%pv, "se rechaza la hipótesis nula")
	else:
		print("   i) con un p-valor de", "%.4f"%pv, "prevalece la hipótesis nula")
	x = 2.48
	pv = 1 - norm.cdf(x)
	if pv < a:
		print("   ii) con un p-valor de", "%.4f"%pv, "se rechaza la hipótesis nula")
	else:
		print("   ii) con un p-valor de", "%.4f"%pv, "prevalece la hipótesis nula")
	
	x = -1.96
	pv = norm.cdf(x)
	print("b)")
	if pv <= a:
		print("   i) con un p-valor de", "%.4f"%pv, "se rechaza la hipótesis nula")
	else:
		print("   i) con un p-valor de", "%.4f"%pv, "prevalece la hipótesis nula")
	x = -0.11
	pv = norm.cdf(x)
	if pv <= a:
		print("   ii) con un p-valor de", "%.4f"%pv, "se rechaza la hipótesis nula")
	else:
		print("   ii) con un p-valor de", "%.4f"%pv, "prevalece la hipótesis nula")
	
	x = 2.10
	pv = 2*(1-norm.cdf(abs(x)))
	print("c)")
	if pv <= a:
		print("   i) con un p-valor de", "%.4f"%pv, "se rechaza la hipótesis nula")
	else:
		print("   i) con un p-valor de", "%.4f"%pv, "prevalece la hipótesis nula")
	x = -1.75
	pv = 2*(1-norm.cdf(abs(x)))
	if pv <= a:
		print("   ii) con un p-valor de", "%.4f"%pv, "se rechaza la hipótesis nula")
	else:
		print("   ii) con un p-valor de", "%.4f"%pv, "prevalece la hipótesis nula")
	
def ej14():
	a = 0.02
	gr = 8
	tobs = 2
	pv = 1-t.cdf(tobs,gr)
	if pv <= a:
		print("a) con un p-valor de", "%.4f"%pv, "se rechaza la hipótesis nula")
	else:
		print("a) con un p-valor de", "%.4f"%pv, "prevalece la hipótesis nula")
	gr = 811
	tobs = -2.4
	pv = t.cdf(tobs,gr)
	if pv <= a:
		print("b) con un p-valor de", "%.4f"%pv, "se rechaza la hipótesis nula")
	else:
		print("b) con un p-valor de", "%.4f"%pv, "prevalece la hipótesis nula")
	gr = 16
	tobs = -1.6
	pv = 2*(1-t.cdf(abs(tobs),gr))
	if pv <= a:
		print("c) con un p-valor de", "%.4f"%pv, "se rechaza la hipótesis nula")
	else:
		print("c) con un p-valor de", "%.4f"%pv, "prevalece la hipótesis nula")
