# ReactorD

![logo](https://raw.githubusercontent.com/SalvadorBrandolin/ReactorD/readthedocs/logo.png)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/SalvadorBrandolin/ReactorD/HEAD)

<a href="https://github.com/SalvadorBrandolin/ReactorD/actions/workflows/ci.yml">
<img src="https://github.com/SalvadorBrandolin/ReactorD/actions/workflows/ci.yml/badge.svg">
</a> 
<a href='https://reactord.readthedocs.io/en/latest/?badge=latest'>
<img src='https://readthedocs.org/projects/reactord/badge/?version=latest'
alt='Documentation Status'/></a> <a href="https://github.com/leliel12/diseno_sci_sfw">
<img src="https://camo.githubusercontent.com/69644832889fa9dfcdb974614129be2fda8e4591989fd713a983a21e7fd8d1ad/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4469536f6674436f6d7043692d46414d41462d666664613030"></a>
<a href='https://pypi.org/project/reactord/'>
<img src='https://img.shields.io/pypi/v/reactord'>
</a>

ReactorD (Reactor Design) is a python package whose proposal is to simulate and design reactors for multiple-reaction systems.Two models of reactors are solved: plug flow (PFR) or stirred tank (STR) in stationary or non-stationary conditions. 
According to requirements, the operation settings can change as follows; 

-Energy Balance
 -Isothermic
 -Non-isothermic
 -Adiabatic 
 
-Mas Balance
 -Homogeneous 
 -Heterogeneous 
 -Continuous 
 -Discontinuous 
 
-Pressure Balance
 -Isobaric
 -Non - isobaric

## Available in version 0.0.1a
- Stationary PFR Isothermic - Isobaric Operation 


## Motivation
While nowadays there are a lot of tools for calculation of thermodynamic
properties of fluids, most of them either are hard to mantain and don't have an
integrated testing system or are embeded to other softwares (as spredsheat
software) limiting the things that can be done to that enviroment.

PyForFluids aims to be a tool:

- With high performance, since most of it's calculations are done in Fortran
- Easy to scale due to it's modular design using the power of Python objects.
- Continuosly tested (at every `push`)to spot any problems as soon as possible.

## Instalation
For installing _ReactorD_ you just need to:

```sh
pip install reactord
```

Make sure to check the requirements first!

### Requirements

## Authors
Brandolín, Salvador Eduardo 
(<a href=salvadorbrandolin@mi.unc.edu.ar>salvadorbrandolin@mi.unc.edu.ar</a>)
Parodi, Adrián
(<a href=adrian.parodi@mi.unc.edu.ar>adrian.parodi@mi.unc.edu.ar</a>)
Rovezzi, Juan Pablo
(<a href=juan.rovezzi@mi.unc.edu.ar>juan.rovezzi@mi.unc.edu.ar</a>)
Santos, Maricel Del Valle
(<a href=maricel.santos@mi.unc.edu.ar>maricel.santos@mi.unc.edu.ar</a>)
Scilipoti, José Antonio
(<a href=jscilipoti@mi.unc.edu.ar>jscilipoti@mi.unc.edu.ar</a>)














