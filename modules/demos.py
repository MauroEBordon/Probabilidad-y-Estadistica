import matplotlib.pylab as plt
import numpy as np
import matplotlib as mpl
from scipy import integrate
from scipy import special
from definiciones import *

def exp_demo():
	ranx = list(np.linspace(0.1, 5, 1000))
	mpl.style.use('seaborn')
	fig1, ax1 = plt.subplots(figsize=(7, 6))
	f1, fda1, e1, v1 = exp_dist(0.5)
	f2, fda2, e2, v2 = exp_dist(1)
	f3, fda3, e3, v3 = exp_dist(1.5)
	f4, fda4, e4, v4 = exp_dist(2)
	f5, fda5, e5, v5 = exp_dist(0.75)
	ax1.set_title('X~exp(λ) - funcion de densidad', color='C0', fontsize=24)
	ax1.plot(ranx, list(map(f1,ranx)), 'C1', label='λ = 0.5',)
	ax1.plot(ranx, list(map(f5,ranx)), 'C5', label='λ = 0.75',)
	ax1.plot(ranx, list(map(f2,ranx)), 'C2', label='λ = 1')
	ax1.plot(ranx, list(map(f3,ranx)), 'C3', label='λ = 1.5')
	ax1.plot(ranx, list(map(f4,ranx)), 'C4', label='λ = 2')
	ax1.set_ylim(0,1)
	ax1.set_xlim(0,5)
	ax1.set_xlabel('x')
	ax1.set_ylabel('P(x)')
	ax1.set_xticks(np.arange(0,6,1))
	ax1.set_yticks(np.arange(0,1.2,0.1))
	ax1.legend(prop={'size': 16})

	fig2, ax2 = plt.subplots(figsize=(7, 6))
	ax2.set_title('X~exp(λ) -funcion de densidad acumulada', color='C0', fontsize=24)
	ax2.plot(ranx, list(map(fda1,ranx)), 'C1', label='λ = 0.5',)
	ax2.plot(ranx, list(map(fda5,ranx)), 'C5', label='λ = 0.75',)
	ax2.plot(ranx, list(map(fda2,ranx)), 'C2', label='λ = 1')
	ax2.plot(ranx, list(map(fda3,ranx)), 'C3', label='λ = 1.5')
	ax2.plot(ranx, list(map(fda4,ranx)), 'C4', label='λ = 2')
	ax1.set_ylim(0,1)
	ax1.set_xlim(0,5)
	ax2.set_xlabel('x')
	ax2.set_ylabel('P(X <= x)')
	ax2.set_xticks(np.arange(0,6,1))
	ax2.set_yticks(np.arange(0,1.2,0.1))
	ax2.legend(prop={'size': 16})

def chi2_demo():
	ranx = list(np.linspace(0.01, 8, 1000))
	mpl.style.use('seaborn')
	fig1, ax1 = plt.subplots(figsize=(7, 6))
	f1, fda1, e1, v1 = chi2_dist(1)
	f2, fda2, e2, v2 = chi2_dist(2)
	f3, fda3, e3, v3 = chi2_dist(3)
	f4, fda4, e4, v4 = chi2_dist(4)
	f5, fda5, e5, v5 = chi2_dist(6)
	f6, fda6, e6, v6 = chi2_dist(9)
	ax1.set_title('X~chi2(k) - funcion de densidad', color='C0', fontsize=24)
	ax1.plot(ranx, list(map(f1,ranx)), 'C1', label='k = 1')
	ax1.plot(ranx, list(map(f2,ranx)), 'C2', label='k = 2')
	ax1.plot(ranx, list(map(f3,ranx)), 'C3', label='k = 3')
	ax1.plot(ranx, list(map(f4,ranx)), 'C4', label='k = 4')
	ax1.plot(ranx, list(map(f5,ranx)), 'C5', label='k = 6')
	ax1.plot(ranx, list(map(f6,ranx)), 'C6', label='k = 9')
	ax1.set_ylim(0,1)
	ax1.set_xlim(0,8)
	ax1.set_xlabel('x')
	ax1.set_ylabel('P(x)')
	ax1.set_xticks(np.arange(0,9,1))
	ax1.set_yticks(np.arange(0,1.1,0.1))
	ax1.legend(prop={'size': 16})
	ranx = list(np.linspace(0.01, 15, 1000))
	fig2, ax2 = plt.subplots(figsize=(7, 6))
	ax2.set_title('X~chi2(k) -funcion de densidad acumulada', color='C0', fontsize=24)
	ax2.plot(ranx, list(map(fda1,ranx)), 'C1', label='k = 1')
	ax2.plot(ranx, list(map(fda2,ranx)), 'C2', label='k = 2')
	ax2.plot(ranx, list(map(fda3,ranx)), 'C3', label='k = 3')
	ax2.plot(ranx, list(map(fda4,ranx)), 'C4', label='k = 4')
	ax2.plot(ranx, list(map(fda5,ranx)), 'C5', label='k = 6')
	ax2.plot(ranx, list(map(fda6,ranx)), 'C6', label='k = 9')
	ax2.set_ylim(0,1)
	ax2.set_xlabel('x')
	ax2.set_ylabel('P(X <= x)')
	ax2.set_xticks(np.arange(0,16,1))
	ax2.set_yticks(np.arange(0,1.1,0.1))
	ax2.legend(prop={'size': 16})

def gamma_demo2():
	mpl.style.use('seaborn')
	ax = [None]*4
	f = [None]*24
	fda = [None]*24
	e = [None]*24
	v = [None]*24
	ran = list(np.linspace(0.01, 20, 1000))
	alfa = [1,2,3,5,9,15]
	beta = [0.5,1,1.5,2]
	
	for i in range (0,3):
		fig1, ax[i] = plt.subplots(figsize=(7, 6))
		ax[i].set_title('X~Г(a, b) - funcion de densidad', color='C0', fontsize=24)
		for j in range(0,6):
			f[5*i+j], fda[5*i+j], e[5*i+j], v[5*i+j] = gamma_dist(alfa[j], beta[i])
			ax[i].plot(ran, list(map(f[5*i+j],ran)), label=('a='+str(alfa[j])+',b='+str(beta[i])))
		ax[i].set_ylim(0,1)
		ax[i].set_xlim(0,20)
		ax[i].set_xlabel('x')
		ax[i].set_ylabel('P(x)')
		ax[i].set_xticks(np.arange(0,20,1))
		ax[i].set_yticks(np.arange(0,1.1,0.1))
		ax[i].legend()

	for i in range (0,3):
		fig1, ax[i] = plt.subplots(figsize=(7, 6))
		ax[i].set_title('X~Г(a, b) - funcion de densidad acumulada', color='C0', fontsize=24)
		for j in range(0,6):
			f[5*i+j], fda[5*i+j], e[5*i+j], v[5*i+j] = gamma_dist(alfa[j], beta[i])
			ax[i].plot(ran, list(map(fda[5*i+j],ran)), label=('a='+str(alfa[j])+',b='+str(beta[i])))
		ax[i].set_ylim(0,1)
		ax[i].set_xlim(0,20)
		ax[i].set_xlabel('x')
		ax[i].set_ylabel('P(X <= x)')
		ax[i].set_xticks(np.arange(0,20,1))
		ax[i].set_yticks(np.arange(0,1.1,0.1))
		ax[i].legend()

def gamma_demo():
	mpl.style.use('seaborn')

	f = [None]*24
	fda = [None]*24
	e = [None]*24
	v = [None]*24
	ran = list(np.linspace(0.01, 20, 1000))
	alfa = [1,2,3,5,9]
	beta = [0.5,1,1.5,2]
	fig1, ax = plt.subplots(3, 2, figsize=(15, 20))
	for i in range (0,3):
		ax[i, 0].set_title('X~Г(a, b) - funcion de densidad', color='C0', fontsize=24)
		for j in range(0,5):
			f[5*i+j], fda[5*i+j], e[5*i+j], v[5*i+j] = gamma_dist(alfa[j], beta[i])
			ax[i,0].plot(ran, list(map(f[5*i+j],ran)), label=('a='+str(alfa[j])+',b='+str(beta[i])))
			ax[i,1].plot(ran, list(map(fda[5*i+j],ran)), label=('a='+str(alfa[j])+',b='+str(beta[i])))
		ax[i,0].set_ylim(0,0.8)
		ax[i,0].set_xlim(0,2.5)
		ax[i,0].set_xlabel('x')
		ax[i,0].set_ylabel('P(x)')
		ax[i,0].set_xticks(np.arange(0,20,1))
		ax[i,0].set_yticks(np.arange(0,0.9,0.1))
		ax[i,0].legend()

		ax[i,1].set_title('X~Г(a, b) - funcion de densidad acumulada', color='C0', fontsize=24)
		ax[i,1].set_ylim(0,1.1)
		ax[i,1].set_xlim(0,2.5)
		ax[i,1].set_xlabel('x')
		ax[i,1].set_ylabel('P(X <= x)')
		ax[i,1].set_xticks(np.arange(0,20,1))
		ax[i,1].set_yticks(np.arange(0,1.1,0.1))
		ax[i,1].legend()

def weibull_demo():
	mpl.style.use('seaborn')

	f = [None]*24
	fda = [None]*24
	e = [None]*24
	v = [None]*24
	ran = list(np.linspace(0.01, 2.5, 1000))
	alfa = [1,2,3,5,9]
	beta = [0.5,1,1.5,2]
	fig1, ax = plt.subplots(4, 2, figsize=(10, 24))
	for i in range (0,4):
		ax[i, 0].set_title('X~W(a, b) - funcion de densidad', color='C0')
		for j in range(0,5):
			f[5*i+j], fda[5*i+j], e[5*i+j], v[5*i+j] = weibull_dist(alfa[j], beta[i])
			ax[i,0].plot(ran, list(map(f[5*i+j],ran)), label=('a='+str(alfa[j])+',b='+str(beta[i])))
		ax[i,0].set_ylim(0,3)
		ax[i,0].set_xlim(0,2.5)
		ax[i,0].set_xlabel('x')
		ax[i,0].set_ylabel('P(x)')
		ax[i,0].set_xticks(np.arange(0,2.5,0.2))
		ax[i,0].set_yticks(np.arange(0,3.1,0.2))
		ax[i,0].legend()

		ax[i,1].set_title('X~W(a, b) - funcion de densidad acumulada', color='C0')
		for j in range(0,5):
			ax[i,1].plot(ran, list(map(fda[5*i+j],ran)), label=('a='+str(alfa[j])+',b='+str(beta[i])))
		ax[i,1].set_ylim(0,1.1)
		ax[i,1].set_xlim(0,2.5)
		ax[i,1].set_xlabel('x')
		ax[i,1].set_ylabel('P(X <= x)')
		ax[i,1].set_xticks(np.arange(0,2.5,0.2))
		ax[i,1].set_yticks(np.arange(0,1.1,0.2))
		ax[i,1].legend()

def lognormal_demo():
	mpl.style.use('seaborn')

	f = [None]*24
	fda = [None]*24
	e = [None]*24
	v = [None]*24
	ran = list(np.linspace(0.01, 2.5, 1000))
	desvio = [0.0025, 0.125**2,0.25**2, 0.5**2, 1**2, 2.25]
	label = [0.05,0.125,0.25, 0.5, 1, 1.5]
	fig1, ax1 = plt.subplots()
	ax1.set_title('X~lognormal(μ, σ2) - funcion de densidad', color='C0', fontsize=24)

	fig2, ax2 = plt.subplots()

	for j in range(0,6):
		f[j], fda[j], e[j], v[j] = lognormal_dist(0,desvio[j])
		ax1.plot(ran, list(map(f[j],ran)), label=('μ = '+str(0)+', σ2 ='+str(label[j])))
		ax2.plot(ran, list(map(fda[j],ran)), label=('μ = '+str(0)+', σ2 ='+str(label[j])))
	ax1.set_ylim(0,1.5)
	ax1.set_xlim(0,2.5)
	ax1.set_xlabel('x')
	ax1.set_ylabel('P(x)')
	ax1.set_xticks(np.arange(0,2.5,0.25))
	ax1.set_yticks(np.arange(0,1.6,0.1))
	ax1.legend()

	ax2.set_title('X~lognormal(μ, σ2) - fda', color='C0', fontsize=24)
	ax2.set_ylim(0,1.1)
	ax2.set_xlim(0,2.5)
	ax2.set_xlabel('x')
	ax2.set_ylabel('P(X <= x)')
	ax2.set_xticks(np.arange(0,2.5,0.25))
	ax2.set_yticks(np.arange(0,1.1,0.1))
	ax2.legend()

def normal_demo():
	mpl.style.use('seaborn')

	f = [None]*24
	fda = [None]*24
	ran = list(np.linspace(-2.5, 2.5, 1000))
	desvio = [0.125**2,0.25**2,0.333**2, 0.5**2, 1**2, 2.25]
	label = [0.125,0.25, 0.333, 0.5, 1, 1.5]
	media = [-1, 0.5, 0, 0, -0.5, 1]
	fig1, ax1 = plt.subplots()
	ax1.set_title('X~N(μ, v) - funcion de densidad', color='C0', fontsize=24)

	fig2, ax2 = plt.subplots()

	for j in range(0,6):
		f[j], _ = normal_dist(media[j],desvio[j])
		_, fda[j] = normal_dist(0,desvio[j])
		ax1.plot(ran, list(map(f[j],ran)), label=('μ = '+str(media[j])+', σ2 = '+str(label[j])))
		ax2.plot(ran, list(map(fda[j],ran)), label=('μ = '+str(0)+', σ2 = '+str(label[j])))
	ax1.set_ylim(0,1.5)
	ax1.set_xlim(-2.5,2.5)
	ax1.set_xlabel('x')
	ax1.set_ylabel('P(x)')
	ax1.set_xticks(np.arange(-2.5,2.5,0.25))
	ax1.set_yticks(np.arange(0,1.6,0.1))
	ax1.legend()

	ax2.set_title('X~N(μ, σ2) - fda', color='C0', fontsize=24)
	ax2.set_ylim(0,1.1)
	ax2.set_xlim(-1,1)
	ax2.set_xlabel('x')
	ax2.set_ylabel('P(X <= x)')
	ax2.set_xticks(np.arange(-1,1,0.25))
	ax2.set_yticks(np.arange(0,1.1,0.1))
	ax2.legend()

def uniforme_demo():
	mpl.style.use('seaborn')
	ran1 = list(np.linspace(1, 5, 1000))
	ran2 = list(np.linspace(2, 3, 1000))
	ran3 = list(np.linspace(0.5, 1, 1000))
	fig1, ax1 = plt.subplots()
	fig1, ax2 = plt.subplots()

	f1, fda1, e1, v1 = uniform_dist(1, 5)
	ax1.plot(ran1, list(map(f1,ran1)), label=('a = '+str(1)+', b = '+str(5)))
	ax2.plot(ran1, list(map(fda1,ran1)), label=('a = '+str(1)+', b = '+str(5)))
	ax1.set_title('X~U(a, b) - funcion de densidad', color='C0', fontsize=24)
	ax2.set_title('X~U(a, b) - fda', color='C0', fontsize=24)
	f1, fda1, e1, v1 = uniform_dist(2, 3)
	ax1.plot(ran2, list(map(f1,ran2)), label=('a = '+str(2)+', b = '+str(3)))
	ax2.plot(ran2, list(map(fda1,ran2)), label=('a = '+str(2)+', b = '+str(3)))
	f1, fda1, e1, v1 = uniform_dist(0.5, 1)
	ax1.plot(ran3, list(map(f1,ran3)), label=('a = '+str(0.5)+', b = '+str(1)))
	ax2.plot(ran3, list(map(fda1,ran3)), label=('a = '+str(0.5)+', b = '+str(1)))
	ran = list(np.linspace(2.5, 3.833333, 1000))
	f1, fda1, e1, v1 = uniform_dist(2.5, 3.833333)
	ax1.plot(ran, list(map(f1,ran)), label=('a = '+str(2.5)+', b = '+str(3.833)))
	ax2.plot(ran, list(map(fda1,ran)), label=('a = '+str(2.5)+', b = '+str(3.833)))
	ax1.legend()
	ax2.legend()
