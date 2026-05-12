# Theory Background: Hyperbolic PDEs, Advection and Burgers Equation

This document develops the theoretical background behind the simulations in this repository. The project studies one-dimensional hyperbolic partial differential equations, focusing on the linear advection equation and the inviscid Burgers equation.

The key physical idea is finite propagation speed. Hyperbolic equations describe systems where information travels through the domain along characteristic directions. For this reason, numerical methods for hyperbolic equations must respect the direction of propagation. A method that uses information from the wrong side of the grid may become unstable even if the finite-difference formula looks reasonable.

The project combines static plots and GIF animations because hyperbolic PDEs are fundamentally dynamical. The animations show the time evolution directly: propagation, smoothing, steepening, oscillation and instability.

---

## 1. Hyperbolic PDEs

Partial differential equations can be broadly classified into elliptic, parabolic and hyperbolic equations.

Elliptic equations describe stationary equilibrium. They do not contain time evolution and the solution is determined globally by boundary conditions and sources.

Parabolic equations describe diffusion or relaxation. They contain first-order time derivatives and second-order spatial derivatives. Their solutions tend to smooth out over time.

Hyperbolic equations describe propagation. They appear in waves, transport, acoustics, electromagnetism and fluid dynamics. Their defining property is finite-speed propagation.

This finite propagation speed imposes a numerical requirement: the numerical domain of dependence must include the physical domain of dependence. This is the origin of the CFL condition.

---

## 2. Linear advection equation

The linear advection equation is:

$$
\frac{\partial u}{\partial t}+ c \frac{\partial u}{\partial x} = 0.
$$

Here $u(x,t)$ is a transported scalar quantity and $c$ is the constant advection speed.

The exact solution is:

$$
u(x,t)=u_0(x-ct).
$$

Therefore, the initial condition should translate without changing shape. This makes linear advection a very clean numerical benchmark.

In this project, the initial condition is a square pulse:

$$
u(x,0)=
\begin{cases}
1, & 1\leq x \leq 2,\\
0, & \text{otherwise}.
\end{cases}
$$

Because the square pulse contains discontinuities, it is a demanding test. Discontinuities reveal numerical diffusion, oscillations and instability more clearly than smooth functions.

---

## 3. Discretization and CFL condition

The grid is defined by:

$$
x_j=x_{\min}+j\Delta x,
$$

and time levels are:

$$
t^n=n\Delta t.
$$

The numerical solution is:

$$
u_j^n \approx u(x_j,t^n).
$$

The Courant number is:

$$
\alpha=\frac{c\Delta t}{\Delta x}.
$$

It measures how many grid cells the physical wave travels in one timestep. For explicit advection schemes, the CFL condition is:

$$
|\alpha|\leq 1.
$$

If this condition is violated, the numerical method attempts to propagate information faster than its stencil allows.

---

## 4. FTCS scheme

The FTCS scheme uses forward time and centered space:

$$
u_j^{n+1} = u_j^n - \frac{c\Delta t}{2\Delta x}
\left( u_{j+1}^n-u_{j-1}^n
\right).
$$

Although this scheme is consistent, it is unstable for pure advection. It does not respect the one-sided propagation direction of the equation.

This shows that consistency is not sufficient. A numerical scheme must also be stable and physically compatible with the PDE type.

---

## 5. Upwind scheme

For $c>0$, information comes from the left. The upwind method uses:

$$
u_j^{n+1} = u_j^n - \frac{c\Delta t}{\Delta x}
\left(
u_j^n-u_{j-1}^n
\right).
$$

This respects the physical direction of propagation. It is stable under the CFL condition.

However, upwind is first-order accurate and introduces numerical diffusion. The square pulse becomes smoother as it propagates.

---

## 6. Downwind scheme

The downwind method for $c>0$ uses:

$$
u_j^{n+1} = u_j^n -
\frac{c\Delta t}{\Delta x}
\left(
u_{j+1}^n-u_j^n
\right).
$$

This uses information from the wrong side of the grid. For positive advection speed, the downstream point should not determine the upstream update.

The method therefore behaves like anti-diffusion and becomes unstable.

---

## 7. Lax-Friedrichs scheme

Lax-Friedrichs is:

$$
u_j^{n+1} = \frac{u_{j+1}^n+u_{j-1}^n}{2} -
\frac{c\Delta t}{2\Delta x}
\left(
u_{j+1}^n-u_{j-1}^n
\right).
$$

The neighbour average stabilizes the method by adding artificial diffusion. This avoids instability but smooths the solution.

Thus, Lax-Friedrichs demonstrates the trade-off between stability and resolution.

---

## 8. Numerical diffusion

Numerical diffusion is artificial smoothing introduced by the discretization. A numerical scheme may behave as if it were solving:

$$
\frac{\partial u}{\partial t} + c \frac{\partial u}{\partial x} =
\nu_{\mathrm{num}}
\frac{\partial^2 u}{\partial x^2}.
$$

The original advection equation has no diffusion term. Therefore, any smoothing of the square pulse is numerical, not physical.

Numerical diffusion is not always bad. It can stabilize solutions and suppress oscillations. However, excessive diffusion destroys sharp features.

---

## 9. Burgers equation

The inviscid Burgers equation is:

$$
\frac{\partial u}{\partial t} + u \frac{\partial u}{\partial x} = 0.
$$

It can also be written in conservative form:

$$
\frac{\partial u}{\partial t} + \frac{\partial}{\partial x}
\left(
\frac{u^2}{2}
\right) =
0.
$$

Burgers equation is nonlinear because the propagation speed is $u$ itself. Larger values travel faster than smaller values. This causes wave steepening.

The initial condition used is:

$$
u(x,0)=2+0.5\sin(2\pi x).
$$

Since $u$ is positive, the wave propagates mainly to the right, but different parts of the wave propagate at different speeds.

---

## 10. Upwind and centered Burgers schemes

The centered Burgers update is:

$$
u_j^{n+1} = u_j^n -
u_j^n
\frac{\Delta t}{2\Delta x}
\left(
u_{j+1}^n-u_{j-1}^n
\right).
$$

It is simple, but fragile when gradients steepen.

The upwind Burgers update chooses the stencil according to the sign of $u_j$. If $u_j>0$, it uses a backward difference. If $u_j<0$, it uses a forward difference.

This is more physically appropriate because the characteristic speed is local.

---

## 11. Role of GIF animations

GIF animations are particularly useful for this project because the equations describe time evolution. Static plots can show a final state, but they cannot show how the solution became stable, diffusive or unstable.

The animations reveal:

- whether the pulse moves in the correct direction,
- how quickly discontinuities smear,
- whether oscillations grow,
- whether a method becomes unstable,
- how Burgers nonlinear steepening develops,
- whether two implementations produce the same dynamic evolution.

For this reason, the GIFs are part of the scientific interpretation, not only visual decoration.

---

## 12. Error and runtime

The project uses an $L^2$-type error:

$$
E_2=
\sqrt{
\frac{1}{N}
\sum_j
\left(
u_j^{\mathrm{num}}-u_j^{\mathrm{ref}}
\right)^2
}.
$$

Runtime is analysed together with error because computational modelling always involves a compromise. Smaller timesteps usually improve stability and accuracy, but require more iterations.

A good method must therefore be evaluated by both accuracy and cost.

---

## 13. Main conclusions

The theoretical conclusions are:

1. Hyperbolic PDEs require direction-aware discretizations.
2. The CFL condition expresses numerical causality.
3. FTCS is unstable for pure advection.
4. Upwind is stable but numerically diffusive.
5. Downwind fails for the wrong propagation direction.
6. Lax-Friedrichs stabilizes through artificial diffusion.
7. Burgers equation is nonlinear and can steepen smooth data.
8. Centered schemes are fragile for nonlinear hyperbolic dynamics.
9. GIF animations are essential for interpreting propagation problems.
10. Error and runtime must be studied together.
