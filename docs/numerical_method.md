# Numerical Method

This document explains the implementation strategy used in the code. The goal is to connect the finite-difference formulas with the structure of the Python implementation while keeping the notation readable in GitHub Markdown.

---

## 1. Linear advection setup

The code first solves the one-dimensional linear advection equation:

$$
\frac{\partial u}{\partial t}+c\frac{\partial u}{\partial x}=0.
$$

The propagation speed is `c = 2`. The spatial domain is `x in [0, 5]`, and the grid contains 100 points.

The timestep is chosen as:

$$
\Delta t = 0.98\frac{\Delta x}{c}.
$$

The factor 0.98 keeps the Courant number just below the CFL limit.

The initial condition is a square pulse equal to 1 between `x = 1` and `x = 2`, and zero elsewhere.

---

## 2. Advection methods implemented

The code implements four main explicit schemes: upwind, downwind, centered / FTCS, and Lax-Friedrichs.

### Upwind scheme

For positive velocity, the upwind method uses information from the left neighbour:

$$
\begin{aligned}
u_j^{n+1}
&=
u_j^n
-\frac{c\Delta t}{\Delta x}
\left(
u_j^n-\nu_{j-1}^n\right).
\end{aligned}
$$

This is the correct directional stencil for positive advection speed. Since the wave travels to the right, the value at grid point $j$ must be updated using information from the upstream side, which is the left neighbour.

### Downwind scheme

The downwind method uses the downstream point:

$$
\begin{aligned}
u_j^{n+1}
&=\nu_j^n
-\frac{c\Delta t}{\Delta x}
\left(\nu_{j+1}^n-\nu_j^n\right).
\end{aligned}
$$

For positive advection speed, this is the wrong propagation direction. The method uses information from the side where the wave is going, not from where it is coming. It is therefore expected to be unstable or strongly distorted.

### Centered / FTCS scheme

The centered method uses a symmetric spatial derivative:

$$
\begin{aligned}
u_j^{n+1}
&=\nu_j^n
-\frac{c\Delta t}{2\Delta x}
\left(\nu_{j+1}^n-\nu_{j-1}^n\right).
\end{aligned}
$$

Although this scheme is formally consistent, it is not stable for pure advection with forward time integration. It does not respect the one-sided propagation direction of the hyperbolic equation.

### Lax-Friedrichs scheme

The Lax-Friedrichs method adds neighbour averaging:

$$
\begin{aligned}
u_j^{n+1}
&=\frac{\nu_{j+1}^n+\nu_{j-1}^n}{2}
-\frac{c\Delta t}{2\Delta x}
\left(\nu_{j+1}^n-\nu_{j-1}^n\right).
\end{aligned}
$$

The averaging term stabilizes the method but introduces artificial diffusion. This makes the method more robust than FTCS, but it also smooths sharp features such as the edges of a square pulse.

---

## 3. GIF generation

The code uses Matplotlib animation tools to visualize the time evolution. GIFs are important because they show the propagation process directly rather than only a final profile.

The animations show:

- the full advection-method comparison,
- the individual upwind method,
- the individual downwind method,
- the individual FTCS method,
- the individual Lax-Friedrichs method,
- Burgers upwind evolution,
- Burgers centered evolution,
- Burgers classic-versus-matrix comparison.

The repository stores selected GIFs in `figures/animations/`.

These animations should be treated as scientific outputs, not as decorative media. For hyperbolic PDEs, the time evolution is often more informative than a single final-time plot because it shows whether the method transports, diffuses, oscillates or becomes unstable.

---

## 4. Periodic boundary conditions

The main advection and Burgers simulations use periodic boundary conditions. Periodicity means that the computational domain behaves like a closed loop:

$$
u(x+L,t)=\nu(x,t).$$

If a pulse exits through the right boundary, it re-enters through the left boundary. This is useful for advection tests because the exact solution should keep circulating through the domain without changing shape.

In the code, periodicity is implemented through index wrapping. The left neighbour of the first grid point is the last grid point, and the right neighbour of the last grid point is the first grid point.

This boundary condition avoids artificial boundary losses. If the pulse changes shape under periodic conditions, the change is due to the numerical method rather than to the pulse leaving the domain.

---

## 5. CFL condition in the implementation

For linear advection, the Courant number is:

$$
\alpha = \frac{c\Delta t}{\Delta x}.
$$

The code chooses:

$$
\Delta t = 0.98\frac{\Delta x}{c},
$$

so that:

$$
\alpha \approx 0.98.
$$

This is slightly below the stability threshold for standard explicit upwind advection. The factor 0.98 acts as a safety margin.

The CFL condition expresses numerical causality: during one timestep, the physical signal should not move farther than the numerical stencil can represent.

For Burgers equation, the local propagation speed is the solution itself. A typical stability requirement is:

$$
\Delta t \lesssim \frac{\Delta x}{\max |u|}.
$$

This is why nonlinear hyperbolic equations require more care than constant-speed advection.

---

## 6. Burgers equation setup

The code also solves the inviscid Burgers equation:

$$
\frac{\partial u}{\partial t}+u\frac{\partial u}{\partial x}=0.
$$

This equation is nonlinear because the propagation speed is the field itself. A point with larger value of $u$ moves faster than a point with smaller value of $u$.

The initial condition used in the code is:

$$

u(x,0)=2+0.5\sin(2\pi x).
$$

This profile is positive everywhere, so the characteristic velocity is positive throughout the domain at the beginning of the simulation. The maximum of the wave moves faster than the minimum, which produces nonlinear steepening.

---

## 7. Centered Burgers method

The centered Burgers scheme uses a symmetric finite-difference approximation:

$$
\begin{aligned}
u_j^{n+1}
&=\nu_j^n
-\nu_j^n
\frac{\Delta t}{2\Delta x}
\left(\nu_{j+1}^n-\nu_{j-1}^n\right).
\end{aligned}
$$

This scheme is easy to implement and follows directly from the differential form of Burgers equation. However, it does not include directional bias or numerical dissipation. As the solution steepens, it can develop nonphysical oscillations.

---

## 8. Upwind Burgers method

For Burgers equation, the local characteristic speed is $u_j$. Therefore, the direction of information flow depends on the sign of $u_j$.

If $u_j>0$, information travels to the right and the derivative should use the left neighbour:

$$
\frac{\partial u}{\partial x}\approx \frac{u_j-u_{j-1}}{\Delta x}.
$$

If $u_j<0$, information travels to the left and the derivative should use the right neighbour:

$$
\frac{\partial u}{\partial x}\approx \frac{u_{j+1}-u_j}{\Delta x}.
$$

The code implements this sign-dependent upwind idea. For the chosen initial condition, $u$ is positive, so the backward/upwind direction dominates.

---

## 9. Classic versus matrix implementation

The project also compares two implementation styles for Burgers equation:

1. a classic loop-based implementation,
2. a matrix/operator-based implementation.

The classic implementation updates the solution directly using explicit loops. The matrix implementation represents the finite-difference derivative through a discrete operator.

The purpose of comparing both is verification. If both implementations represent the same finite-difference method, they should produce very similar results.

---

## 10. Error norm

The code uses an $L^2$-type error norm:


$$
E_2 =
\sqrt{
\frac{1}{N}
\sum_{j=0}^{N-1}
\left(
 u_j^{\mathrm{num}}
- u_j^{\mathrm{ref}}
\right)^2
}.
$$

This measures the root-mean-square difference between a numerical solution and a reference solution.

For the advection problem, the reference can be the expected transported profile after a given propagation time. Under periodic boundary conditions, if the pulse completes an integer number of domain crossings, the exact solution should match the initial profile.

For Burgers equation, error interpretation is more delicate because the solution is nonlinear. Nevertheless, the error norm is still useful for comparing trends as timestep, spatial resolution or implementation style changes.

---

## 11. Error versus timestep

The code studies how the numerical error changes when $\Delta t$ is varied.

For explicit hyperbolic schemes, increasing $\Delta t$ increases the Courant number:

$$
\alpha=\frac{c\Delta t}{\Delta x}.
$$

For Burgers equation, the relevant speed is local and depends on the solution itself:

$$
\Delta t \lesssim \frac{\Delta x}{\max |u|}.
$$

The error-versus-timestep analysis shows how numerical reliability depends on timestep selection.

---

## 12. Runtime versus timestep

The runtime analysis measures the computational cost of reaching a fixed final time. The number of timesteps is approximately:

$$
N_t \approx \frac{T}{\Delta t}.
$$

Smaller $\Delta t$ means more timesteps and larger runtime. This is why runtime must be analysed together with error.

---

## 13. Spatial resolution study

The code also studies the effect of changing the number of grid points. Increasing the number of points decreases $\Delta x$, so the solution can resolve sharper structures.

For the square-pulse advection problem, higher resolution represents the discontinuities more accurately. For Burgers equation, higher resolution helps capture steepening gradients.

However, increasing resolution also increases cost. More grid points require more operations per timestep, and if the CFL condition is enforced, smaller $\Delta x$ usually requires smaller $\Delta t$.

---

## 14. Artificial diffusion analysis

Artificial diffusion is smoothing introduced by the numerical method, not by the physical PDE.

For the linear advection equation, the exact solution should preserve the shape of the square pulse. Therefore, any rounding of the pulse edges is numerical diffusion.

Upwind introduces moderate numerical diffusion. Lax-Friedrichs introduces stronger diffusion because of its neighbour-averaging term. FTCS may produce oscillations instead of clean diffusion. Downwind can behave like anti-diffusion and become unstable.

---

## 15. Boundary-condition comparison

The code compares three types of boundary conditions:

- periodic,
- Dirichlet,
- Neumann.

Periodic boundaries make the domain behave like a loop:

$$
u(0,t)=\nu(L,t).$$

Dirichlet boundaries prescribe the value of the solution at the boundary:

$$
u(0,t)=0.$$

Neumann boundaries prescribe the derivative at the boundary:

$$
\frac{\partial u}{\partial x}=0.
$$

In the implementation, a homogeneous Neumann condition can be approximated by copying the adjacent value:

$$

u_0=\nu_1.
$$

The comparison shows that boundary conditions are part of the physical problem. Changing the boundary condition changes the behaviour of the solution, even if the PDE and numerical method remain the same.

---

## 16. Static figures and animation outputs

The repository contains both static figures and GIF animations.

The static figures are used for quantitative diagnostics:

- error versus timestep,
- runtime versus timestep,
- error versus runtime,
- classic-versus-matrix snapshot.

The GIF animations are used for qualitative diagnosis:

- advection method comparison,
- individual upwind/downwind/FTCS/Lax-Friedrichs behaviour,
- Burgers upwind evolution,
- Burgers centered evolution,
- Burgers classic-versus-matrix evolution.

Both types of output are important. Static plots quantify trends, while GIFs show how the numerical behaviour develops in time.

---

## 17. Implementation style

The implementation is intentionally educational. Many updates are written in a direct form so that the code remains close to the finite-difference equations.

This style is useful because it makes the numerical method readable. Each update formula can be traced back to the corresponding mathematical discretization.

For larger simulations, the same methods could be vectorized, written in conservative flux form or implemented with sparse matrices. However, for this project, clarity and connection to the theory are the main priorities.

---

## 18. Summary of implemented components

The code demonstrates:

- explicit time marching,
- finite-difference spatial derivatives,
- CFL-based timestep selection,
- periodic boundary conditions,
- Dirichlet boundary conditions,
- Neumann boundary conditions,
- upwind advection,
- downwind advection,
- FTCS advection,
- Lax-Friedrichs advection,
- inviscid Burgers dynamics,
- centered Burgers update,
- upwind Burgers update,
- classic versus matrix implementation comparison,
- error diagnostics,
- runtime diagnostics,
- GIF animation generation.

Overall, the implementation connects the mathematical theory of hyperbolic PDEs with visible numerical behaviour.
