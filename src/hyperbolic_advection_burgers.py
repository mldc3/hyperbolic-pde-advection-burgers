"""Numerical methods for 1D linear advection and inviscid Burgers equation.

This module keeps an educational, explicit implementation style that mirrors the
finite-difference formulas documented in this repository.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict

import numpy as np


# =============================================================================
# SECTION 1 — Grid and initial conditions
# =============================================================================


@dataclass(frozen=True)
class Grid1D:
    """Uniform 1D grid."""

    x_min: float = 0.0
    x_max: float = 5.0
    n_points: int = 100

    @property
    def x(self) -> np.ndarray:
        return np.linspace(self.x_min, self.x_max, self.n_points, endpoint=False)

    @property
    def dx(self) -> float:
        return (self.x_max - self.x_min) / self.n_points

    @property
    def length(self) -> float:
        return self.x_max - self.x_min


def advection_dt_cfl(dx: float, c: float, cfl: float = 0.98) -> float:
    """CFL-based timestep for linear advection."""

    return cfl * dx / c


def burgers_dt_cfl(dx: float, u: np.ndarray, cfl: float = 0.98) -> float:
    """CFL-like timestep for Burgers equation based on max local speed."""

    umax = max(float(np.max(np.abs(u))), 1e-12)
    return cfl * dx / umax


def initial_square_pulse(x: np.ndarray, left: float = 1.0, right: float = 2.0) -> np.ndarray:
    """Square pulse initial condition: 1 on [left, right], 0 elsewhere."""

    u0 = np.zeros_like(x)
    u0[(x >= left) & (x <= right)] = 1.0
    return u0


def initial_burgers_profile(x: np.ndarray) -> np.ndarray:
    """Initial condition u(x,0) = 2 + 0.5 sin(2 pi x)."""

    return 2.0 + 0.5 * np.sin(2.0 * np.pi * x)


# =============================================================================
# SECTION 2 — Boundary conditions
# =============================================================================


def apply_boundary(u: np.ndarray, bc: str, value: float = 0.0) -> np.ndarray:
    """Apply boundary condition in-place for non-periodic updates."""

    if bc == "periodic":
        return u
    if bc == "dirichlet":
        u[0] = value
        u[-1] = value
        return u
    if bc == "neumann":
        u[0] = u[1]
        u[-1] = u[-2]
        return u
    msg = f"Unsupported boundary condition: {bc}"
    raise ValueError(msg)


def _neighbors(u: np.ndarray, bc: str) -> tuple[np.ndarray, np.ndarray]:
    """Return left and right neighbor arrays under selected boundary condition."""

    if bc == "periodic":
        return np.roll(u, 1), np.roll(u, -1)

    left = np.empty_like(u)
    right = np.empty_like(u)

    left[1:] = u[:-1]
    right[:-1] = u[1:]

    if bc == "dirichlet":
        left[0] = 0.0
        right[-1] = 0.0
    elif bc == "neumann":
        left[0] = u[0]
        right[-1] = u[-1]
    else:
        msg = f"Unsupported boundary condition: {bc}"
        raise ValueError(msg)

    return left, right


# =============================================================================
# SECTION 3 — Linear advection explicit schemes
# =============================================================================


def advection_upwind(u: np.ndarray, c: float, dt: float, dx: float, bc: str = "periodic") -> np.ndarray:
    """Upwind update for positive advection speed c.

    u_j^{n+1} = u_j^n - (c dt/dx) (u_j^n - u_{j-1}^n)
    """

    alpha = c * dt / dx
    left, _ = _neighbors(u, bc)
    un = u - alpha * (u - left)
    return apply_boundary(un, bc)


def advection_downwind(u: np.ndarray, c: float, dt: float, dx: float, bc: str = "periodic") -> np.ndarray:
    """Downwind update.

    u_j^{n+1} = u_j^n - (c dt/dx) (u_{j+1}^n - u_j^n)
    """

    alpha = c * dt / dx
    _, right = _neighbors(u, bc)
    un = u - alpha * (right - u)
    return apply_boundary(un, bc)


def advection_ftcs(u: np.ndarray, c: float, dt: float, dx: float, bc: str = "periodic") -> np.ndarray:
    """Centered FTCS advection update."""

    alpha = c * dt / dx
    left, right = _neighbors(u, bc)
    un = u - 0.5 * alpha * (right - left)
    return apply_boundary(un, bc)


def advection_lax_friedrichs(
    u: np.ndarray,
    c: float,
    dt: float,
    dx: float,
    bc: str = "periodic",
) -> np.ndarray:
    """Lax-Friedrichs advection update."""

    alpha = c * dt / dx
    left, right = _neighbors(u, bc)
    un = 0.5 * (right + left) - 0.5 * alpha * (right - left)
    return apply_boundary(un, bc)


# =============================================================================
# SECTION 4 — Inviscid Burgers explicit schemes
# =============================================================================


def burgers_centered(u: np.ndarray, dt: float, dx: float, bc: str = "periodic") -> np.ndarray:
    """Centered Burgers update.

    u_j^{n+1} = u_j^n - u_j^n (dt/(2dx)) (u_{j+1}^n - u_{j-1}^n)
    """

    left, right = _neighbors(u, bc)
    un = u - u * (dt / (2.0 * dx)) * (right - left)
    return apply_boundary(un, bc)


def burgers_upwind(u: np.ndarray, dt: float, dx: float, bc: str = "periodic") -> np.ndarray:
    """Sign-dependent upwind Burgers update.

    If u_j > 0 use backward difference, else forward difference.
    """

    left, right = _neighbors(u, bc)
    dudx_backward = (u - left) / dx
    dudx_forward = (right - u) / dx
    dudx = np.where(u >= 0.0, dudx_backward, dudx_forward)
    un = u - u * dt * dudx
    return apply_boundary(un, bc)


def burgers_centered_matrix_operator(n_points: int, dx: float) -> np.ndarray:
    """Periodic centered-difference matrix operator D for du/dx."""

    d = np.zeros((n_points, n_points))
    for j in range(n_points):
        d[j, (j - 1) % n_points] = -1.0 / (2.0 * dx)
        d[j, (j + 1) % n_points] = 1.0 / (2.0 * dx)
    return d


def burgers_centered_matrix(u: np.ndarray, dt: float, d_dx: np.ndarray) -> np.ndarray:
    """Matrix/operator implementation equivalent to centered Burgers update."""

    dudx = d_dx @ u
    return u - dt * (u * dudx)


# =============================================================================
# SECTION 5 — Simulation drivers and diagnostics
# =============================================================================


AdvectionStepper = Callable[[np.ndarray, float, float, float, str], np.ndarray]
BurgersStepper = Callable[[np.ndarray, float, float, str], np.ndarray]


def run_advection(
    stepper: AdvectionStepper,
    u0: np.ndarray,
    c: float,
    dt: float,
    dx: float,
    n_steps: int,
    bc: str = "periodic",
) -> np.ndarray:
    """Run advection simulation with explicit time marching."""

    u = u0.copy()
    for _ in range(n_steps):
        u = stepper(u, c, dt, dx, bc)
    return u


def run_burgers(
    stepper: BurgersStepper,
    u0: np.ndarray,
    dt: float,
    dx: float,
    n_steps: int,
    bc: str = "periodic",
) -> np.ndarray:
    """Run Burgers simulation with explicit time marching."""

    u = u0.copy()
    for _ in range(n_steps):
        u = stepper(u, dt, dx, bc)
    return u


def advection_exact_periodic_square(
    x: np.ndarray,
    t: float,
    c: float,
    x_min: float,
    x_max: float,
    left: float = 1.0,
    right: float = 2.0,
) -> np.ndarray:
    """Exact periodic advection of the square pulse."""

    l = x_max - x_min
    x_shift = ((x - c * t - x_min) % l) + x_min
    return initial_square_pulse(x_shift, left=left, right=right)


def l2_error(u_num: np.ndarray, u_ref: np.ndarray) -> float:
    """RMS / L2-type discrete error norm."""

    return float(np.sqrt(np.mean((u_num - u_ref) ** 2)))


def available_advection_methods() -> Dict[str, AdvectionStepper]:
    """Named advection methods used in the project."""

    return {
        "upwind": advection_upwind,
        "downwind": advection_downwind,
        "ftcs": advection_ftcs,
        "lax_friedrichs": advection_lax_friedrichs,
    }


def available_burgers_methods() -> Dict[str, BurgersStepper]:
    """Named Burgers methods used in the project."""

    return {
        "upwind": burgers_upwind,
        "centered": burgers_centered,
    }


# =============================================================================
# SECTION 6 — Minimal executable demo
# =============================================================================


def _demo() -> None:
    """Run a short consistency demo without writing files."""

    grid = Grid1D(x_min=0.0, x_max=5.0, n_points=100)
    x = grid.x
    dx = grid.dx

    # Linear advection demo
    c = 2.0
    dt_adv = advection_dt_cfl(dx, c, cfl=0.98)
    # Keep demo horizon short to avoid nonlinear centered-scheme blow-up.
    t_final = 0.1
    n_steps = int(np.ceil(t_final / dt_adv))
    dt_adv = t_final / n_steps

    u0_adv = initial_square_pulse(x)
    u_adv = run_advection(advection_upwind, u0_adv, c, dt_adv, dx, n_steps)
    u_adv_ref = advection_exact_periodic_square(x, t_final, c, grid.x_min, grid.x_max)
    err_adv = l2_error(u_adv, u_adv_ref)

    # Burgers demo
    u0_b = initial_burgers_profile(x)
    dt_b = burgers_dt_cfl(dx, u0_b, cfl=0.98)
    n_steps_b = int(np.ceil(t_final / dt_b))
    dt_b = t_final / n_steps_b

    u_b_upwind = run_burgers(burgers_upwind, u0_b, dt_b, dx, n_steps_b)
    u_b_centered = run_burgers(burgers_centered, u0_b, dt_b, dx, n_steps_b)

    d = burgers_centered_matrix_operator(grid.n_points, dx)
    u_b_matrix = u0_b.copy()
    for _ in range(n_steps_b):
        u_b_matrix = burgers_centered_matrix(u_b_matrix, dt_b, d)

    print("Hyperbolic PDE demo complete")
    print(f"Advection L2 error (upwind vs exact): {err_adv:.6e}")
    print(f"Burgers means (upwind/centered/matrix): {u_b_upwind.mean():.6f}, {u_b_centered.mean():.6f}, {u_b_matrix.mean():.6f}")


if __name__ == "__main__":
    _demo()
