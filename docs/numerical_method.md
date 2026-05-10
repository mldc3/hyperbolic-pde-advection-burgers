# Numerical Method

## Spatial-temporal discretization
The project uses explicit finite-difference updates on a uniform one-dimensional grid with timestep selected from a CFL criterion.

## Advection methods included
- FTCS (centered difference advection update),
- upwind method,
- downwind method,
- Lax-Friedrichs method.

These methods are compared through direct time evolution, error-versus-$\Delta t$ studies, and runtime-versus-$\Delta t$ studies.

## Burgers methods included
- centered explicit Burgers update,
- upwind-type Burgers update,
- classic loop implementation versus matrix-based implementation.

## Metrics and diagnostics
The numerical analysis includes:
- $L_2$ error calculations,
- error versus timestep sweeps,
- runtime versus timestep sweeps,
- qualitative diffusion behavior checks,
- boundary-condition comparisons (Dirichlet/Neumann/periodic),
- GIF animations for visual evolution.
