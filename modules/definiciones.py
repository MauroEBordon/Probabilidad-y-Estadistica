from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from scipy.stats import lognorm
from scipy import special
from scipy import integrate
from pynverse import inversefunc
from scipy.stats import t, chi2, norm
import math

MAX_POISSON = 28

def mediana(x, cont=False):
	if len(x)%2==0:
		i = int(len(x)/2)
		return (x[i]+x[i-1])/2
	else:
		i = int(len(x)/2)
		return x[i]


def desvio(x, a=None, b=None, continuous=False, modify=False):
	return math.sqrt(V(x, a, b, continuous, modify))

def E(x, a=None, b=None, continuous=False, modify=False):
	if modify:
		return a * E(x) - b
	if continuous:
		return integrate.quad(lambda y:y*x(y),a,b)[0]
	if isinstance(x, dict):
		ans = 0
		num = 0
		for k in x.keys():
			ans += k * x[k]
			num += x[k]
	else:
		return sum(x)/len(x)
	return ans/num

def E2(x, a, b):	
	return integrate.quad(lambda y:y*y*x(y),a,b)[0]

def V(x, a=None, b=None, est=False, continuous=False, modify=False):
	if modify:
		return a**2 * V(x)
	if continuous:
		return E2(x, a, b) - E(x,a,b, True)**2
	if isinstance(x, dict):
		esqared = 0
		num = 0
		for k in x.keys():
			esqared += k**2 * x[k]
			num += x[k]
		ans = esqared - E(x)**2 
	else:
		ans = 0
		e = E(x)
		for i in x:
			ans += (i - e)**2
		if est:
			return ans/(len(x)-1)
	return ans

def fact(n):
	ans = 1
	for i in range(1, n+1):
		ans *= i
	return ans

def nCr(n, m):
	ans = fact(n) / (fact(m) * fact(n-m))
	return ans

def binomial_probt(ensayos, p_exito, acumulada=False):
	ans = [0] * (ensayos+1)
	acum = 0
	for i in range(0,ensayos+1):
		if acumulada:
			acum += nCr(ensayos,i) * p_exito**i * (1-p_exito)**(ensayos-i)
			ans[i] = acum
		else: 
			ans[i] = nCr(ensayos,i) * p_exito**i * (1-p_exito)**(ensayos-i)
	ans = dict(zip(range(0,ensayos+1),ans))
	return ans

def hypergeo_probt(muestra, num_exitos, total, acumulada=False):
	ans = [0] * (num_exitos+1)
	fracasos = total - num_exitos
	acum = 0
	for i in range(0, num_exitos+1):
		if acumulada:
			if fracasos < (muestra-i):
				acum += 0
				ans[i] = acum
			else:
				acum += nCr(num_exitos,i)*nCr(fracasos,(muestra-i))/nCr(total,muestra)
				ans[i] = acum
		else: 
			if fracasos < (muestra-i):
				ans[i] = 0
			else:
				ans[i] = nCr(num_exitos,i)*nCr(fracasos,(muestra-i))/nCr(total,muestra)
	ans = dict(zip(range(0,num_exitos+1),ans))
	return ans

def BN_probt(num_exitos, prob, max_cases = 100, acumulada=False):
	ans = [0] * (max_cases+1)
	acum = 0
	for i in range(0,max_cases+1):
		if acumulada:
			acum += nCr(num_exitos+i-1, num_exitos-1) * prob**num_exitos * (1-prob)**i
			ans[i] = acum
		else: 
			ans[i] = nCr(num_exitos+i-1, num_exitos-1) * prob**num_exitos * (1-prob)**i
	ans = dict(zip(range(0,max_cases+1),ans))
	return ans

def poisson_probt(lam, acumulada=False):
	ans = [0] * MAX_POISSON
	acum = 0
	for i in range (0, MAX_POISSON):
		if acumulada:
			acum += math.e**-lam * lam**i / fact(i)
			ans[i] = acum
		else: 
			ans[i] = math.e**-lam * lam**i / fact(i)
	ans = dict(zip(range(0,MAX_POISSON), ans))
	return ans


def binomial_dist(n, p):
	prob_table = binomial_probt(n, p, False)
	cumulative_table = binomial_probt(n, p, True)
	e = n*p
	v = n*p*(1-p)
	return prob_table, cumulative_table, e, v, math.sqrt(v)

def hypergeo_dist(n, M, N):
	prob_table = hypergeo_probt(M, N, n, False)
	cumulative_table = hypergeo_probt(M, N, n, True)
	e = n * M / N
	v = n*M/N * (1 - M/N) * (N-n)/(N-1)
	des = math.sqrt(v)
	return prob_table, cumulative_table, e, v, des

def BN_dist(r, p, max_cases=100):
	prob_table = BN_probt(r, p, False)
	cumulative_table = BN_probt(r, p, True)
	e = r * (1-p) / p
	v = r * (1-p) / p**2
	des = math.sqrt(v)
	return prob_table, cumulative_table, e, v, des

def poisson_dist(lam):
	prob_table = binomial_probt(lam, False)
	cumulative_table = binomial_probt(lam, True)
	e = lam
	v = lam
	return prob_table, cumulative_table, e, v, math.sqrt(v)

def uniform_dist(a, b):
	fda = lambda x: (x-a)/(b-a)
	f = lambda x: 1/(b-a)
	e = (a+b) / 2
	v = (b-a)**2 / 12
	return f, fda, e, v

def normal_dist(e=None, v=None):
	std = lambda x: (math.e**((x**2 / 2)*(-1))) / math.sqrt(2*math.pi) 
	if e != None:
		f = lambda x: (math.e**(((x-e)**2 / (2*v)) * (-1))) / math.sqrt(2*math.pi*v)
		fda = lambda x: integrate.quad(f, -math.inf, x)[0]
		return f, fda	
	else:
		return std

STD = normal_dist()

def gamma_dist(a, b):
	f = lambda x: x**(a-1.) * np.e**(-x/b) / (b**a * special.gamma(a))
	e = a * b
	v = a * b**2
	fda = lambda x: integrate.quad(f, 0., x)[0]
	return f, fda, e, v

def exp_dist(lam):
	f, fda, e, v = gamma_dist(1.,1./lam)
	e = 1 / lam
	v = 1 / lam**2
	fda = lambda x: 1.-math.e**(-lam*x)
	return f, fda, e, v

def chi2_dist(k):
	f, fda, e, v = gamma_dist(int(k)/2,2)
	e = k
	v = 2*k
	return f, fda, e, v

def weibull_dist(a, b):
	f = lambda x: a * x**(a-1.) * np.e**(-((x/b)**a)) / (b**a)
	e = b * special.gamma(1+1/a)
	v =  b**2 * (special.gamma(1+2/a) - special.gamma(1+1/a)**2)
	fda = lambda x: integrate.quad(f, 0., x)[0]
	return f, fda, e, v

def lognormal_dist(e, v):
	f = lambda x:lognorm.pdf(x,math.sqrt(v))
	fda = lambda x: lognorm.cdf(x,math.sqrt(v))
	e = math.e**(e+v/2)
	v = np.exp(2*e+v) * (np.exp(v) - 1)
	return f, fda, e, v

def cov(f, a, b):
	px = lambda x: integrate.quad(lambda y:f(x,y),0,10)[0]
	py = lambda y: integrate.quad(lambda x:f(x,y),0,10)[0]
	dob = integrate.dblquad(lambda x,y: x*y*f(x,y), 0, 10, lambda x: 0, lambda x: 10)[0]
	return dob - E(px, a, b, continuous=True)*E(py, a, b, continuous=True)

def corr(f, a, b):
	px = lambda x: integrate.quad(lambda y:f(x,y),0,10)[0]
	py = lambda y: integrate.quad(lambda x:f(x,y),0,10)[0]
	dx = desvio(px, a, b, continuous=True)
	dy = desvio(py, a, b, continuous=True)
	co = cov(f, a, b)
	return co/(dx*dy)

def show_conjunta(f, a, b):
	fig = plt.figure(figsize=(9, 6))
	ax = fig.gca(projection='3d')

	# Make data.
	X = np.arange(a, b, (a+b)/200)
	Y = np.arange(a, b, (a+b)/200)
	X, Y = np.meshgrid(X, Y)
	Z = f(X,Y)

	ax.contourf(X, Y, Z, zdir='x', offset=-(b-a)/10, cmap=cm.copper, alpha=0.3)
	ax.contourf(X, Y, Z, zdir='y', offset=b+(b-a)/10, cmap=cm.copper, alpha=0.3)
	surf = ax.plot_surface(X, Y, Z, cmap=cm.copper, rstride=8, cstride=8, alpha=0.8)
	ax.set_xlabel('X')
	ax.set_ylabel('Y')

	fig.colorbar(surf, shrink=0.5, aspect=5)

	plt.show()

def Zvalue(x, e, d):
	return (x-e)/d

def prob_norm(a=-math.inf, b=math.inf):
	std = normal_dist()
	return integrate.quad(std, a, b)[0]

def z_prob(a=-math.inf, b=math.inf):
	return integrate.quad(STD, a, b)[0]

def aprox_prob(e, d, n, a=-math.inf, b=math.inf):
	std = normal_dist()
	aa = Zvalue(a, e, d) * math.sqrt(n)
	ab = Zvalue(b, e, d) * math.sqrt(n)
	return integrate.quad(std, aa, ab)[0]

def t_dist(v):
	f = lambda x: special.gamma((v+1)/2) * (1 + x**2 / v)**((-v-1)/2) / (math.sqrt(v*math.pi)/special.gamma(v/2))
	e = 0
	va = v/(v-2)
	fda = lambda x: integrate.quad(f, 0., x)[0]
	return f, fda, e, va

def auxz(b):
	return integrate.quad(STD, -b, b)[0]
	
def int_conf(x, d, n, conf):
	a = (1 + conf)/2
	invz = inversefunc(auxz)
	z = invz(a)
	izq = "%.3f"%(x - z * d/math.sqrt(n))
	der = "%.3f"%(x + z * d/math.sqrt(n))
	ic = (float(izq), float(der))
	lon = ic[1] - ic[0]
	return ic, lon

def ic_getN(x, d, om, conf):
	a = (1 + conf)/2
	invz = inversefunc(auxz)
	z = invz(a)
	n = (2*z*d/om)**2
	return math.ceil(n)

def ic_mean(x, d, n, conf, normal=False):
	if not normal and n < 30:
		a = (1 + conf)/2
		tv = t.ppf(a, n-1)
		izq = "%.3f"%(x - tv * d/math.sqrt(n))
		der = "%.3f"%(x + tv * d/math.sqrt(n))
		ic = (float(izq), float(der))
		lon = ic[1] - ic[0]
		return ic, lon
	else:
		return int_conf(x, d, n, conf)

def ic_var(d, n, conf):
	a = (1 - conf)/2
	xi = chi2.ppf(a, n-1)
	xd = chi2.ppf(1- a, n-1)
	izq = "%.3f"%((n-1) * d**2 / xd)
	der = "%.3f"%((n-1) * d**2 / xi)
	ic = (float(izq), float(der))
	lon = ic[1] - ic[0]
	return ic, lon		

def ic_dev(d, n, conf):
	a = (1 - conf)/2
	xi = chi2.ppf(a, n-1)
	xd = chi2.ppf(1- a, n-1)
	izq = "%.3f"%(math.sqrt((n-1) * d**2 / xd))
	der = "%.3f"%(math.sqrt((n-1) * d**2 / xi))
	ic = (float(izq), float(der))
	lon = ic[1] - ic[0]
	return ic, lon		

def ic_getdev(x, der, n, conf):
	a = (1 + conf)/2
	tv = t.ppf(a, n-1)
	d = (der - x)/tv * math.sqrt(n)
	return d

#entra en zona de rechazo?
def ph_mean_result(x,d,n,e,a, hip=None, case=None):
	if case == 'A' or (case == 'B' and n>29):
		z = math.sqrt(n)*(x - e)/d
		if hip == 'equal':
			c = norm.ppf(a/2)
			return abs(c) <= abs(z)  
		elif hip == 'less':
			c = norm.ppf(a)
			return -z <= c
		elif hip == 'greater':
			c = norm.ppf(a)
			return c <= z
	if case == 'C':
		ta = math.sqrt(n)*(x - e)/d
		if hip == 'equal':
			c = t.ppf(a/2, n-1)
			return abs(c) < abs(ta)
		elif hip == 'less':
			c = t.ppf(a, n-1)
			return -ta <= c
		elif hip == 'greater':
			c = t.ppf(a, n-1)
			return c <= ta

def ph_mean_err1(x, d, n, izq, der, hip=None, case=None):
	if case == 'A' or (case == 'B' and n>29):
		less = norm.cdf(math.sqrt(n)*(izq-x)/d)
		greater = norm.cdf(math.sqrt(n)*(der-x)/d)
		if hip == 'equal':
			return less+1-greater
		elif hip == 'less':
			return less
		elif hip == 'greater':
			return 1-greater
	if case == 'C':
		less = t.cdf(math.sqrt(n)*(izq-x)/d, n-1)
		greater = t.cdf(math.sqrt(n)*(der-x)/d, n-1)
		if hip == 'equal':
			return less+1-greater
		elif hip == 'less':
			return less
		elif hip == 'greater':
			return 1-greater

def ph_mean_err2(x, d, n, e, a, hip=None, case=None):
	if case == 'A' or (case == 'B' and n>29):
		if hip == 'equal':
			c = abs(norm.ppf(a/2))
			der = c + (math.sqrt(n)*(e - x)/d)
			izq = -c + (math.sqrt(n)*(e - x)/d)
			ans = norm.cdf(der) - norm.cdf(izq)
			return ans
		elif hip == 'less':
			c = abs(norm.ppf(a))
			izq = -c + (math.sqrt(n)*(e - x)/d)
			return 1 - norm.cdf(izq)
		elif hip == 'greater':
			c = abs(norm.ppf(a))
			der = c + (math.sqrt(n)*(e - x)/d)
			return norm.cdf(der)

def ph_mean_n(x, d, e, a, b,  hip=None):
	if hip == 'equal':
		za = abs(norm.ppf(a/2))
	else:
		za = abs(norm.ppf(a))
	zb = abs(norm.ppf(b))
	n = ((za+zb)*d/(x-e))**2
	return math.ceil(n)
	
#se fija si entra en la zona de rechazo
def ph_prop_result(x,p,n,a,hip=None):
	if n*p >= 10 and n*(1-p) >= 10:
		z = (x-p)/math.sqrt(p*(1-p)/n)
		if hip == 'equal':
			c = norm.ppf(a/2)
			return abs(c) <= abs(z)  
		elif hip == 'less':
			c = norm.ppf(a)
			return z <= c
		elif hip == 'greater':
			c = norm.ppf(a)
			return -c <= z

def ph_prop_err1(x,y,p,n, hip=None):
	if n*p >= 10 and n*(1-p) >= 10:
		less = norm.cdf((x-p)/math.sqrt(p*(1-p)/n))
		greater = norm.cdf((y-p)/math.sqrt(p*(1-p)/n))
		if hip == 'equal':
			return less+1-greater
		elif hip == 'less':
			return less
		elif hip == 'greater':
			return 1-greater

def ph_prop_err2(x,p,n,a, hip=None):
	if n*p >= 10 and n*(1-p) >= 10:
		if hip == 'equal':
			c = abs(norm.ppf(a/2))
			der = c*math.sqrt((p*(1-p))/x*(1-x)) + ((p-x)/math.sqrt(p*(1-p)/n))
			izq = -c*math.sqrt((p*(1-p))/x*(1-x)) + ((p-x)/math.sqrt(p*(1-p)/n))
			ans = norm.cdf(der) - norm.cdf(izq)
			return ans
		elif hip == 'less':
			c = abs(norm.ppf(a))
			izq = -c*math.sqrt((p*(1-p))/x*(1-x)) + ((p-x)/math.sqrt(p*(1-p)/n))
			return 1 - norm.cdf(izq)
		elif hip == 'greater':
			c = abs(norm.ppf(a))
			der = c*math.sqrt((p*(1-p))/x*(1-x)) + ((p-x)/math.sqrt(p*(1-p)/n))
			return norm.cdf(der)

def ph_prop_n(x, p, a, b,  hip=None):
	if hip == 'equal':
		za = abs(norm.ppf(a/2))
	else:
		za = abs(norm.ppf(a))
	zb = abs(norm.ppf(b))
	n = ((zb*math.sqrt(x*(1-x))+za*math.sqrt(p*(1-p)))/(p-x))**2
	return math.ceil(n)

def p_value(obs,d,n,e,est=None, hip=None):
	if est=='Z':
		z = math.sqrt(n)*(obs - e)/d
		if hip == 'equal':
			return 2*(1 - norm.cdf(z))
		elif hip == 'less':
			return norm.cdf(z)
		elif hip == 'greater':
			return 1 - norm.cdf(z)
	elif est=='T':
		tv = math.sqrt(n)*(obs - e)/d
		if hip == 'equal':
			return 2*(1 - t.cdf(abs(tv), n-1))
		elif hip == 'less':
			return t.cdf(tv, n-1)
		elif hip == 'greater':
			return 1 - t.cdf(tv, n-1)




"""
def test():
	bi_prob = binomial_probt(20, 0.2)
	bit, bict, bie, biv, bid = binomial_dist(20, 0.2)
	print("binomial:")
	print("E(X) =", "%.3f"%E(bi_prob),"y V(X) =", "%.3f"%V(bi_prob))
	print("E(X) =", "%.3f"%bie,"y V(X) =", "%.3f"%biv)

	hg_prob = hypergeo_probt(6, 7, 10)
	hgt, hgct, hge, hgv, hgd = hypergeo_dist(6, 7, 10)
	print("hipergeometrica:")
	print("E(X) =", "%.3f"%E(hg_prob),"y V(X) =", "%.3f"%V(hg_prob))
	print("E(X) =", "%.3f"%hge,"y V(X) =", "%.3f"%hgv)


	bn_prob = BN_probt(4, 0.3)
	bnt, bnct, bne, bnv, bnd = BN_dist(4, 0.3)
	print("binomial negativa:")
	print("E(X) =", "%.3f"%E(bn_prob),"y V(X) =", "%.3f"%V(bn_prob))
	print("E(X) =", "%.3f"%bne,"y V(X) =", "%.3f"%bnv)

	po_prob = poisson_probt(5)
	pot, poct, poe, pov, pod = poisson_dist(5)
	print("poisson:")
	print("E(X) =", "%.3f"%E(po_prob),"y V(X) =", "%.3f"%V(po_prob))
	print("E(X) =", "%.3f"%poe,"y V(X) =", "%.3f"%pov)

	unif,unie,univ = uniform_dist(0,1)
	print("uniforme:")
	print("E(X) =", "%.3f"%E(unif,0,1,True),"y V(X) =", "%.3f"%V(unif,0,1,True))
	print("E(X) =", "%.3f"%unie,"y V(X) =", "%.3f"%univ)
"""
