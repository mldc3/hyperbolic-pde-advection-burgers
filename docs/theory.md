# Theory

## Linear advection equation
The linear advection model
$$
\frac{\partial u}{\partial t} + c\frac{\partial u}{\partial x}=0
$$
propagates profiles at constant speed $c$ without changing shape in the exact continuous solution.

## Inviscid Burgers equation
The inviscid Burgers equation
$$
\frac{\partial u}{\partial t} + u\frac{\partial u}{\partial x}=0
$$
introduces nonlinear wave speed, since local propagation depends on the state $u$ itself. This causes steepening and sensitivity to discretization choices.

## Initial and boundary conditions
The practice combines:
- square-pulse initialization for linear advection,
- sinusoidal initialization for Burgers,
- periodic boundaries as the baseline treatment,
- additional Dirichlet and Neumann comparisons in boundary-condition studies.

## Stability perspective
For explicit schemes, stability is constrained by a CFL condition of the form
$$
\Delta t \propto \frac{\Delta x}{\text{characteristic speed}}
$$
which controls numerical propagation relative to the spatial mesh.
