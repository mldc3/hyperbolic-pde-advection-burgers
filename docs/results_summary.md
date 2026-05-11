# Results Summary

This document analyses the static figures and GIF animations produced for the one-dimensional hyperbolic PDE simulations. The goal is not only to show that the code runs, but to interpret what each visual result says about stability, causality, numerical diffusion, nonlinear steepening and computational cost.

---

## 1. Why animations are important for hyperbolic PDEs

Hyperbolic equations describe propagation. For that reason, static plots only show part of the story. A single final-time profile can reveal distortion, but it does not show how that distortion developed.

The GIF animations are especially useful because they show the full time evolution. They make visible:

- the direction of propagation,
- whether the method respects causality,
- whether discontinuities are transported or smeared,
- whether oscillations grow with time,
- whether the solution becomes unstable,
- how nonlinear Burgers dynamics deform the initial profile,
- how matrix and loop implementations compare dynamically.

For this project, the animations are therefore not decorative. They are part of the numerical diagnosis.

---

## 2. Linear advection: full methods comparison

![Linear advection full methods comparison](../figures/animations/advection_methods_comparison.gif)

The full advection animation compares the explicit schemes on the same square-pulse initial condition. The exact advection equation should simply translate the pulse without changing its shape:

$$
u(x,t)=u_0(x-ct).
$$

Therefore, any visible deformation is numerical.

The upwind profile remains bounded and follows the correct propagation direction. Its main error is smoothing: the discontinuous edges of the pulse become rounded as the simulation advances. This is numerical diffusion.

The downwind profile is expected to behave poorly for positive velocity. Since information physically travels from left to right, the numerical method must look to the left. Downwind instead looks to the right. The animation makes this violation visible through distortion or instability.

The centered/FTCS profile is also problematic. It uses a symmetric stencil and does not respect the one-sided domain of dependence of the hyperbolic equation. This can lead to nonphysical oscillations.

Lax-Friedrichs is more stable because it adds averaging between neighbouring points. However, the animation shows that this stabilization comes from artificial diffusion, which smears the pulse.

The central conclusion is that stability and accuracy are controlled by the relationship between the numerical stencil and the physical direction of propagation.

---

## 3. Upwind animation

![Upwind advection animation](../figures/animations/advection_upwind.gif)

The upwind animation is the cleanest example of a stable directional method for positive advection speed. The update uses the previous grid point:

$$
u_j^{n+1}
=
u_j^n
-
\frac{c\Delta t}{\Delta x}
\left(
u_j^n-u_{j-1}^n\right).
$$

Since $c>0$, this is the correct side of the stencil. The solution remains stable because the numerical domain of dependence contains the physical domain of dependence.

The animation also shows the limitation of first-order upwind: the square pulse gradually loses its sharp corners. This is not physical diffusion. It is introduced by the discretization. In practical simulations, this is often acceptable if the goal is to avoid nonphysical oscillations, but it reduces resolution near discontinuities.

---

## 4. Downwind animation

![Downwind advection animation](../figures/animations/advection_downwind.gif)

The downwind animation is a useful negative example. For positive velocity, the scheme uses the downstream point:

$$
u_j^{n+1}
=
u_j^n
-
\frac{c\Delta t}{\Delta x}
\left(
u_{j+1}^n-u_j^n\right).
$$

This contradicts the direction of propagation. Instead of damping small numerical errors, the method amplifies them. In physical terms, the method asks the future direction of the wave to determine the present update.

This is why downwind is not just less accurate; it is structurally wrong for this sign of velocity. The animation should be interpreted as a demonstration of numerical anti-diffusion and loss of causality.

---

## 5. FTCS / centered advection animation

![FTCS centered advection animation](../figures/animations/advection_ftcs_centered.gif)

The centered animation shows why FTCS is not suitable for pure advection. The centered derivative,

$$
\frac{u_{j+1}^n-u_{j-1}^n}{2\Delta x},
$$

does not choose an upstream direction. It treats the left and right neighbours symmetrically.

For diffusion equations, centered spatial derivatives are often natural. For hyperbolic transport, the propagation direction matters. Without upwind bias or artificial diffusion, high-frequency components are not controlled.

The square pulse contains sharp discontinuities, which correspond to high-frequency Fourier components. These components are precisely the ones most likely to trigger visible oscillations or instability in centered advection.

---

## 6. Lax-Friedrichs animation

![Lax-Friedrichs advection animation](../figures/animations/advection_lax_friedrichs.gif)

The Lax-Friedrichs animation shows a stable but diffusive behaviour. The method is:

$$
u_j^{n+1}
=
\frac{u_{j+1}^n+u_{j-1}^n}{2}
-
\frac{c\Delta t}{2\Delta x}
\left(
u_{j+1}^n-u_{j-1}^n\right).
$$

The first term is an average of neighbouring values. This introduces artificial diffusion. The result is a solution that remains bounded, but smooths the pulse more strongly than the exact equation would.

This result is important because it separates two ideas: a stable solution is not necessarily a sharp or accurate solution. Lax-Friedrichs is robust, but it pays for robustness by dissipating structure.

---

## 7. Advection error versus timestep

![Advection error versus timestep](../figures/error_analysis/advection_error_vs_dt.png)

The error-versus-timestep figure quantifies what the animations show qualitatively. The Courant number,

$$
\alpha=\frac{c\Delta t}{\Delta x},
$$

controls the relation between physical propagation and numerical update.

For small enough $\Delta t$, upwind remains stable and the error is mainly due to numerical diffusion. As $\Delta t$ increases, the error increases because the method approximates the time evolution more coarsely.

Downwind and centered schemes are expected to show much worse behaviour because their instability is not only a timestep issue. It comes from an inappropriate stencil for the hyperbolic problem.

Lax-Friedrichs generally stays bounded but can show significant error because the artificial diffusion changes the shape of the transported pulse.

---

## 8. Advection runtime versus timestep

![Advection runtime versus timestep](../figures/runtime/advection_runtime_vs_dt.png)

The runtime plot shows the computational cost of reaching a fixed final time. Smaller timesteps require more time iterations:

$$
N_t \approx \frac{T}{\Delta t}.
$$

Therefore, runtime increases as $\Delta t$ decreases. This is the standard cost of explicit time integration.

The relevant interpretation is the compromise between accuracy and cost. Very small timesteps are safer and usually more accurate, but they are computationally more expensive. Larger timesteps are faster, but can push the simulation toward instability or excessive error.

---

## 9. Burgers methods comparison animation

![Burgers methods comparison animation](../figures/animations/burgers_methods_comparison.gif)

Burgers equation is nonlinear:

$$
\frac{\partial u}{\partial t}
+
u
\frac{\partial u}{\partial x}
=
0.
$$

The wave speed is now $u$ itself. Larger values of $u$ travel faster than smaller values. The animation therefore shows deformation of the initial sinusoidal profile.

This deformation is not only numerical: it is part of the physics of Burgers equation. The difficulty is to distinguish physical steepening from numerical artifacts.

The upwind Burgers method is more robust because it respects the local propagation direction. The centered method is less dissipative but more fragile, especially when the gradient becomes steep.

---

## 10. Burgers upwind animation

![Burgers upwind animation](../figures/animations/burgers_upwind.gif)

The upwind Burgers animation shows a stable evolution of the nonlinear profile. Since the initial condition is positive,

$$
u(x,0)=2+0.5\sin(2\pi x),
$$

the local velocity is positive over the whole domain. The backward/upwind stencil is therefore appropriate.

As the simulation evolves, the faster parts of the wave catch up with slower parts, causing steepening. The upwind method damps the sharpest gradients, which prevents strong oscillations but introduces numerical smoothing.

This is typical of robust first-order hyperbolic solvers.

---

## 11. Burgers centered animation

![Burgers centered animation](../figures/animations/burgers_centered.gif)

The centered Burgers animation is useful because it shows the limitation of non-dissipative centered schemes in nonlinear hyperbolic equations. The centered method can look acceptable at early times while the profile remains smooth. However, once gradients steepen, the method has no mechanism to control oscillations.

This is why high-resolution methods for nonlinear hyperbolic PDEs usually combine upwind fluxes, limiters or Riemann solvers rather than relying on purely centered differences.

---

## 12. Burgers classic versus matrix animation

![Burgers classic versus matrix animation](../figures/animations/burgers_classic_vs_matrix.gif)

The classic-versus-matrix animation compares two implementation styles. The classic approach uses explicit loops, while the matrix approach represents the discrete derivative operator algebraically.

The value of this comparison is methodological. If both implementations produce the same evolution, this validates the translation from finite-difference formulas to a matrix/operator representation.

If small differences appear, they should be interpreted carefully. They can arise from boundary handling, update ordering, matrix construction or floating-point roundoff. In nonlinear equations, even small numerical differences can become more visible over time.

---

## 13. Burgers error versus timestep

![Burgers error versus timestep](../figures/error_analysis/burgers_error_vs_dt.png)

The Burgers error plot shows how timestep affects a nonlinear hyperbolic equation. The relevant stability scale is controlled by the maximum local speed:

$$
\Delta t \lesssim \frac{\Delta x}{\max |u|}.
$$

Because $u$ changes during the simulation, Burgers equation is more delicate than linear advection. A timestep that seems acceptable initially may become less accurate as gradients steepen.

The upwind method usually behaves more robustly, while the centered method may show increasing error or oscillatory behaviour.

---

## 14. Burgers runtime versus timestep

![Burgers runtime versus timestep](../figures/runtime/burgers_runtime_vs_dt.png)

As in the advection case, runtime increases when $\Delta t$ decreases because more time steps are required.

For Burgers equation, this cost is especially relevant because stable simulations may require smaller timesteps when the local velocity is large. The plot therefore illustrates the practical cost of stability in nonlinear wave propagation.

---

## 15. Classic versus matrix snapshot

![Classic versus matrix snapshot](../figures/matrix_comparison/burgers_classic_vs_matrix_snapshot.png)

The static comparison complements the animation by showing a direct profile comparison at a representative time. Close agreement indicates that both implementations are solving the same discrete problem.

This is useful for portfolio purposes because it demonstrates not only physics knowledge, but also numerical verification: the same algorithmic idea has been checked through two equivalent computational formulations.

---

## 16. Classic versus matrix error and runtime

![Classic versus matrix error comparison](../figures/error_analysis/burgers_classic_vs_matrix_error_vs_dt.png)

The error comparison verifies whether the two implementations scale similarly as the timestep changes. Similar trends support the consistency of the two formulations.

![Classic versus matrix runtime comparison](../figures/runtime/burgers_classic_vs_matrix_runtime_vs_dt.png)

The runtime comparison shows that implementation style matters. For small 1D problems, explicit loops may be competitive. Matrix formulations can introduce overhead, especially if dense matrices are used. However, matrix representations become powerful in larger problems, sparse solvers and implicit methods.

---

## 17. Error versus runtime

![Error versus runtime](../figures/error_analysis/burgers_error_vs_runtime.png)

This plot combines accuracy and computational cost. It is often more informative than error or runtime alone.

A good method should not only be accurate; it should also be computationally efficient. Conversely, a very fast method is not useful if the error is too large or the solution is unstable.

This type of plot is important because real numerical modelling always involves a trade-off between reliability and cost.

---

## 18. Overall conclusions

The static figures and GIF animations support the following conclusions:

1. Hyperbolic PDEs require direction-aware schemes.
2. The CFL condition encodes numerical causality.
3. Upwind methods are stable for the correct propagation direction but introduce numerical diffusion.
4. Downwind methods fail when they use information from the wrong side.
5. FTCS is not appropriate for pure advection because it is unstable.
6. Lax-Friedrichs stabilizes the solution through artificial diffusion.
7. Burgers equation is more demanding because the wave speed depends on the solution.
8. Centered Burgers schemes can become fragile as gradients steepen.
9. GIF animations are essential for diagnosing propagation, diffusion and instability.
10. Error analysis must be interpreted together with runtime analysis.
11. Boundary conditions are part of the physical model.
12. Matrix and loop implementations provide complementary views of the same numerical method.

Overall, this project demonstrates the connection between mathematical PDE classification, physical propagation, numerical stability and scientific Python implementation.
