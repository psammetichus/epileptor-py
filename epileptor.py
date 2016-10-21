from scipy import integrate
from numpy import exp, arange
import sdeint

def epifun(y,t ):
  """
  Function defining the system of ODEs in the epileptor model. The variables in
  the published model x1, y1, x2, y2, z, u are respectively renamed y[0] through
  y[5]. The helper functions f1, f2 are defined in nested scope.

  This version does not introduce additive normal noise.
  """

  #parameters

  Irest1, Irest2 = 3.1, 0.45

  y0 = [-1.6, 1.0]

  tau0, tau1, tau2 = 2857., 1., 10.

  gamma = 0.01

  def f1(a,b):
    return a**3 - 3*a**2 if a < 0 else (b - 0.6*(y[4] - 4)**2)*a 

  def f2(a,b):
    return 0 if b < -0.25 else 6*(b + 0.25)

  return [
      y[1] - f1(y[0],y[2]) - z + Irest1,
      y0[1] - 5*y[0]**2 - y[1],
      -y[3] + y[2] - y[2]**3 + Irest2 + 0.002*g(y[0]) - 0.3*(y[4]-3.5),
      (1/tau2) * (-y[3] + f2(y[0], y[2])),
      (1/tau0) * (4*(y[0] - y0[0]) - y[4]),
      -gamma*(y[5] - 0.1*y[0])
      ]

initconds = [0, -5, 0, 0, 3, 0]

def main():
  tspan = arange(0,200.0,0.005)
  eqtype = 'ito'
  if eqtype == 'ode':
    ans = integrate.odeint(epifun, initconds, tspan)
  elif eqtype == 'ito':
    ans = sdeint.itoEuler(epifun, [0,0,0,0,0] initconds, tspan

