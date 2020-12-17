"""
Mac Cormack Scheme realization on python for
the two dimensional Navier-Stokes equation
with compressible fluid (or ideal gas, air).
"""

import matplotlib.pyplot as plt # noqa
import matplotlib.animation as animation # noqa: unused import
import matplotlib.cm as cm # noqa

n = 50
dx = 10**-5 / n
dy = 10**-5 / n
dt = dx ** 2 * 0.1
eps = 10**-8  # accuracy coefficient
max_diff = eps + 1
max_iters = 200  # break if # of iterations exceed it
print_period = 200  # print the max_diff every * iteration
iters = 0  # counter

# All constant coefficients
# R = 8.31  # universal gas constant
R = 286.9  # gas constant for the air

c_p = 1003.5  # mass heat capacity of the air
P_norm = 10**5  # pressure at the normal condition of the air
Pr = 0.71  # Prandtl coefficient
T_0 = 273  # reference temperature
T_w = 288
mu_0 = 1.716 * 10**-5  # viscosity at the reference temperature
c_v = 717.25  # molar heat capacity of the air
S = 110  # Sutherland temperature

U_init = 100

"""
U1 = Rho[]   - continuity           | we need three lists: old, pred, new
Ux = Rho * U[] - x component        | we need three lists: old, pred, new
Uy = Rho * V[] - y component        | we need three lists: old, pred, new
U5 = Et[]    - energy conservation  | we need three lists: old, pred, new
P = []
U = []
V = []
T = []
"""


# Note: if we write all E and F components
#       as a functions of the U's components
#       then we could store only U's components.
#       In other words, we will compute E and F at the current
#       time n on the fly.


"""
pseudo-code:

while max_diff > eps:
    1. predictor step (Explicit method) for all U components:
        rho
        rho*u
        rho*v
        E_t
    2. computing bar variables:
        we know rho, compute u, v, e, T = f(rho, e), P = f(rho, e),
            compute mu, k again
    3. corrector step:
        use computed values in the predictor, construct U_new using
        U_old, U_bar E_bar, F_bar.
    4. computing n+1 variables:
        we know rho, compute u, v, e, T = f(rho, e), P = f(rho, e).
            compute mu, k last time
    ---------------------------------------------------------------------------
    Here we know all components of  U_n+1, E_n+1, F_n+1
    ---------------------------------------------------------------------------

    5. compute max difference
    6. copy U_new to U_old
    7. if max differenc < eps, break, otherwise repeat 1 - 7
"""


def rho_u_u(rho_u, rho):
    return rho_u * rho_u / rho


def rho_u_v(rho_u, rho_v, rho):
    return rho_u * rho_v / rho


def tau_xx(U, V, mu, i, j, step='pred'):
    if step == 'pred':
        f = 2 * mu / dx * (U[i][j] - U[i - 1][j])
        f += - (2 / 3) * mu * (1 / dx * (U[i][j] - U[i - 1][j]) +
                               1 / 2 / dy * (V[i][j + 1] - V[i][j - 1]))
    else:
        f = 2 * mu / dx * (U[i + 1][j] - U[i][j])
        f += - (2 / 3) * mu * (1 / dx * (U[i + 1][j] - U[i][j]) +
                               1 / 2 / dy * (V[i][j + 1] - V[i][j - 1]))
    return f


def tau_yy(U, V, mu, i, j, step='pred'):
    if step == 'pred':
        f = 2 * mu / dy * (V[i][j] - V[i][j - 1])
        f += - (2 / 3) * mu * (1 / 2 / dx * (U[i + 1][j] - U[i - 1][j]) +
                               1 / dy * (V[i][j] - V[i][j - 1]))
    else:
        f = 2 * mu / dy * (V[i][j + 1] - V[i][j])
        f += - (2 / 3) * mu * (1 / 2 / dx * (U[i + 1][j] - U[i - 1][j]) +
                               1 / dy * (V[i][j + 1] - V[i][j]))
    return f


def E_x_pred(Rho, U, V, P, mu, i, j):
    return (Rho[i][j] * U[i][j]**2) + P[i][j] -\
        tau_xx(U, V, mu, i, j, step='pred')


def F_x_pred(Rho, U, V, mu, i, j):
    return (Rho[i][j] * U[i][j] * V[i][j]) -\
        mu * ((U[i][j] - U[i][j - 1]) / (dy) +
              (V[i + 1][j] - V[i - 1][j]) / (2 * dx))


def E_y_pred(Rho, U, V, mu, i, j):
    return (Rho[i][j] * U[i][j] * V[i][j]) -\
        mu * ((U[i][j + 1] - U[i][j - 1]) / (2 * dy) +
              (V[i][j] - V[i - 1][j]) / (dx))


def F_y_pred(Rho, U, V, P, mu, i, j):
    return (Rho[i][j] * V[i][j]**2) + P[i][j] -\
        tau_yy(U, V, mu, i, j, step='pred')


def E_x_corr(Rho, U, V, P, mu, i, j):
    return (Rho[i][j] * U[i][j]**2) + P[i][j] -\
        tau_xx(U, V, mu, i, j, step='corr')


def F_x_corr(Rho, U, V, mu, i, j):
    return (Rho[i][j] * U[i][j] * V[i][j]) -\
        mu * ((U[i][j + 1] - U[i][j]) / (dy) +
              (V[i + 1][j] - V[i - 1][j]) / (2 * dx))


def E_y_corr(Rho, U, V, mu, i, j):
    return (Rho[i][j] * U[i][j] * V[i][j]) -\
        mu * ((U[i][j + 1] - U[i][j - 1]) / (2 * dy) +
              (V[i + 1][j] - V[i][j]) / (dx))


def F_y_corr(Rho, U, V, P, mu, i, j):
    return (Rho[i][j] * V[i][j]**2) + P[i][j] -\
        tau_yy(U, V, mu, i, j, step='corr')


def E_5_pred(E_t, P, U, V, T, mu, i, j):
    return (E_t[i][j] + P[i][j]) * U[i][j] -\
        U[i][j] * tau_xx(U, V, mu, i, j, step='pred') -\
        V[i][j] * (mu * ((U[i][j + 1] - U[i][j - 1]) / (2 * dy) +
                         (V[i][j] - V[i - 1][j]) / (dx))) -\
        k_(mu) * (T[i][j] - T[i - 1][j]) / (dx)


def F_5_pred(E_t, P, U, V, T, mu, i, j):
    return (E_t[i][j] + P[i][j]) * V[i][j] -\
        U[i][j] * (mu * ((U[i][j] - U[i][j - 1]) / (dy) +
                         (V[i + 1][j] - V[i - 1][j]) / (2 * dx))) -\
        V[i][j] * tau_yy(U, V, mu, i, j, step='pred') -\
        k_(mu) * (T[i][j] - T[i][j - 1]) / (dy)


def E_5_corr(E_t, P, U, V, T, mu, i, j):
    return (E_t[i][j] + P[i][j]) * U[i][j] -\
        U[i][j] * tau_xx(U, V, mu, i, j, step='corr') -\
        V[i][j] * (mu * ((U[i][j + 1] - U[i][j - 1]) / (2 * dy) +
                         (V[i + 1][j] - V[i][j]) / (dx))) -\
        k_(mu) * (T[i + 1][j] - T[i][j]) / (dx)


def F_5_corr(E_t, P, U, V, T, mu, i, j):
    return (E_t[i][j] + P[i][j]) * V[i][j] -\
        U[i][j] * (mu * ((U[i][j + 1] - U[i][j]) / (dy) +
                         (V[i + 1][j] - V[i - 1][j]) / (2 * dx))) -\
        V[i][j] * tau_yy(U, V, mu, i, j, step='corr') -\
        k_(mu) * (T[i][j + 1] - T[i][j]) / (dy)


def mu_(T):
    return mu_0 * ((T / T_0)**(1.5)) * (T_0 + S) / (T + S)


def k_(mu):
    return mu * c_p / Pr


def e_(E_t, rho, u, v):
    return E_t / rho - ((u)**2 + (v)**2) / 2


def temperature(e):
    return e / c_v


def pressure(rho, e):
    return rho * R * e / c_v


U1 = [[0 for j in range(n)] for i in range(n)]
Ux = [[0 for j in range(n)] for i in range(n)]
Uy = [[0 for j in range(n)] for i in range(n)]
U5 = [[0 for j in range(n)] for i in range(n)]
P = [[0 for j in range(n)] for i in range(n)]
U = [[0 for j in range(n)] for i in range(n)]
V = [[0 for j in range(n)] for i in range(n)]
T = [[0 for j in range(n)] for i in range(n)]
for i in range(n):
    for j in range(n):
        P[i][j] = P_norm
        V[i][j] = 0
        T[i][j] = T_w
        U[i][j] = U_init if i == 0 or j == n - 1 else 0
        U1[i][j] = P[i][j] / (R * T[i][j])
        Ux[i][j] = U1[i][j] * U[i][j]
        Uy[i][j] = U1[i][j] * V[i][j]
        U5[i][j] = U1[i][j] * (c_v * T[i][j] + (U[i][j]**2) / 2)

U1_bar = [[U1[i][j] for j in range(n)] for i in range(n)]
Ux_bar = [[Ux[i][j] for j in range(n)] for i in range(n)]
Uy_bar = [[Uy[i][j] for j in range(n)] for i in range(n)]
U5_bar = [[U5[i][j] for j in range(n)] for i in range(n)]

U1_new = [[U1[i][j] for j in range(n)] for i in range(n)]
Ux_new = [[Ux[i][j] for j in range(n)] for i in range(n)]
Uy_new = [[Uy[i][j] for j in range(n)] for i in range(n)]
U5_new = [[U5[i][j] for j in range(n)] for i in range(n)]


def boundaries(F, var):
    if var == "V":
        for i in range(n):
            for j in range(n):
                if i == 0:
                    F[i][j] = 0
                if j == 0:
                    F[i][j] = 0
                if i == n - 1:
                    F[i][j] = F[i - 1][j]
                if j == n - 1:
                    F[i][j] = 0

    elif var == "U":
        for i in range(n):
            for j in range(n):
                if i == 0:
                    F[i][j] = U_init
                elif i == n - 1:
                    F[i][j] = F[i - 1][j]
                elif j == 0:
                    F[i][j] = 0
                elif j == n - 1:
                    F[i][j] = U_init

    elif var == "P":
        for i in range(n):
            for j in range(n):
                if i == 0:
                    F[i][j] = P_norm
                elif i == n - 1:
                    F[i][j] = F[i - 1][j]
                elif j == 0:
                    F[i][j] = F[i][j + 1]
                elif j == n - 1:
                    F[i][j] = P_norm

    elif var == 'T':
        for i in range(n):
            for j in range(n):
                if i == 0:
                    F[i][j] = T_w
                elif i == n - 1:
                    F[i][j] = F[i - 1][j]
                elif j == 0:
                    F[i][j] = T_w
                elif j == n - 1:
                    F[i][j] = T_w

    return F


graph = []
while max_diff > eps:

    for i in range(n):
        for j in range(n):
            U[i][j] = Ux[i][j] / U1[i][j]
            V[i][j] = Uy[i][j] / U1[i][j]

            e = e_(U5[i][j], U1[i][j], U[i][j], V[i][j])
            T[i][j] = temperature(e)
            P[i][j] = pressure(U1[i][j], e)
    for i in range(n):
        for j in range(n):
            U1[i][j] = P[i][j] / (R * T[i][j])
            Ux[i][j] = U1[i][j] * U[i][j]
            Uy[i][j] = U1[i][j] * V[i][j]
            U5[i][j] = U1[i][j] * (c_v * T[i][j] +
                                   (U[i][j]**2 + V[i][j]**2) / 2)

            U1_bar[i][j] = U1[i][j]
            U1_new[i][j] = U1[i][j]
            Ux_bar[i][j] = Ux[i][j]
            Ux_new[i][j] = Ux[i][j]
            Uy_bar[i][j] = Uy[i][j]
            Uy_new[i][j] = Uy[i][j]
            U5_bar[i][j] = U5[i][j]
            U5_new[i][j] = U5[i][j]

    for i in range(1, n - 1):
        for j in range(1, n - 1):
            mu = mu_(T[i][j])
            U1_bar[i][j] = U1[i][j] - dt / dx * (Ux[i + 1][j] - Ux[i][j]) -\
                dt / dy * (Uy[i][j + 1] - Uy[i][j])
            Ux_bar[i][j] = Ux[i][j] - dt / dx * (E_x_pred(U1, U, V, P,
                                                          mu, i + 1, j) -
                                                 E_x_pred(U1, U, V, P,
                                                          mu, i, j)) -\
                dt / dy * (F_x_pred(U1, U, V, mu, i, j + 1) -
                           F_x_pred(U1, U, V, mu, i, j))
            Uy_bar[i][j] = Uy[i][j] - dt / dx * (E_y_pred(U1, U, V,
                                                          mu, i + 1, j) -
                                                 E_y_pred(U1, U, V,
                                                          mu, i, j)) -\
                dt / dy * (F_y_pred(U1, U, V, P, mu, i, j + 1) -
                           F_y_pred(U1, U, V, P, mu, i, j))
            U5_bar[i][j] = U5[i][j] - dt / dx * (E_5_pred(U5, P, U, V, T,
                                                          mu, i + 1, j) -
                                                 E_5_pred(U5, P, U, V, T,
                                                          mu, i, j)) -\
                dt / dy * (F_5_pred(U5, P, U, V, T, mu, i, j + 1) -
                           F_5_pred(U5, P, U, V, T, mu, i, j))

    # computing variables
    for i in range(n):
        for j in range(n):
            U[i][j] = Ux_bar[i][j] / U1_bar[i][j]
            V[i][j] = Uy_bar[i][j] / U1_bar[i][j]

            e = e_(U5_bar[i][j], U1_bar[i][j], U[i][j], V[i][j])
            T[i][j] = temperature(e)
            P[i][j] = pressure(U1_bar[i][j], e)

    T = boundaries(T, var='T')
    P = boundaries(P, var='P')
    U = boundaries(U, var='U')
    V = boundaries(V, var='V')

    for i in range(n):
        for j in range(n):
            U1_bar[i][j] = P[i][j] / (R * T[i][j])
            Ux_bar[i][j] = U1_bar[i][j] * U[i][j]
            Uy_bar[i][j] = U1_bar[i][j] * V[i][j]
            U5_bar[i][j] = U1_bar[i][j] * (c_v * T[i][j] +
                                           (U[i][j]**2 + V[i][j]**2) / 2)

    for i in range(1, n - 1):
        for j in range(1, n - 1):
            mu = mu_(T[i][j])
            U1_new[i][j] = U1[i][j] + U1_bar[i][j] -\
                dt / dx * (Ux_bar[i][j] - Ux_bar[i - 1][j]) -\
                dt / dy * (Uy_bar[i][j] - Uy_bar[i][j - 1])
            U1_new[i][j] = U1_new[i][j] * 0.5
            Ux_new[i][j] = Ux[i][j] + Ux_bar[i][j] -\
                dt / dx * (E_x_corr(U1_bar, U, V, P,
                                    mu, i, j) -
                           E_x_corr(U1_bar, U, V, P,
                                    mu, i - 1, j)) -\
                dt / dy * (F_x_corr(U1_bar, U, V, mu, i, j) -
                           F_x_corr(U1_bar, U, V, mu, i, j - 1))
            Ux_new[i][j] = Ux_new[i][j] * 0.5
            Uy_new[i][j] = Uy[i][j] + Uy_bar[i][j] -\
                dt / dx * (E_y_corr(U1_bar, U, V,
                                    mu, i, j) -
                           E_y_corr(U1_bar, U, V,
                                    mu, i - 1, j)) -\
                dt / dy * (F_y_corr(U1_bar, U, V, P, mu, i, j) -
                           F_y_corr(U1_bar, U, V, P, mu, i, j - 1))
            Uy_new[i][j] = Uy_new[i][j] * 0.5
            U5_new[i][j] = U5[i][j] + U5_bar[i][j] -\
                dt / dx * (E_5_corr(U5_bar, P, U, V, T,
                                    mu, i, j) -
                           E_5_corr(U5_bar, P, U, V, T,
                                    mu, i - 1, j)) -\
                dt / dy * (F_5_corr(U5_bar, P, U, V, T, mu, i, j) -
                           F_5_corr(U5_bar, P, U, V, T, mu, i, j - 1))
            U5_new[i][j] = U5_new[i][j] * 0.5

    T = boundaries(T, var='T')
    P = boundaries(P, var='P')
    U = boundaries(U, var='U')
    V = boundaries(V, var='V')

    max_diff = 0
    for i in range(n):
        for j in range(n):
            diff = abs(U1_new[i][j] - U1[i][j])
            if diff > max_diff:
                max_diff = diff

    for i in range(n):
        for j in range(n):
            U[i][j] = Ux_new[i][j] / U1_new[i][j]
            V[i][j] = Uy_new[i][j] / U1_new[i][j]

            e = e_(U5_new[i][j], U1_new[i][j], U[i][j], V[i][j])
            T[i][j] = temperature(e)
            P[i][j] = pressure(U1_new[i][j], e)

    for i in range(n):
        for j in range(n):
            U1_new[i][j] = P[i][j] / (R * T[i][j])
            Ux_new[i][j] = U1_new[i][j] * U[i][j]
            Uy_new[i][j] = U1_new[i][j] * V[i][j]
            U5_new[i][j] = U1_new[i][j] * (c_v * T[i][j] +
                                           (U[i][j]**2 + V[i][j]**2) / 2)

    U1_bar = [[U1_new[i][j] for j in range(n)] for i in range(n)]
    Ux_bar = [[Ux_new[i][j] for j in range(n)] for i in range(n)]
    Uy_bar = [[Uy_new[i][j] for j in range(n)] for i in range(n)]
    U5_bar = [[U5_new[i][j] for j in range(n)] for i in range(n)]

    U1 = [[U1_new[i][j] for j in range(n)] for i in range(n)]
    Ux = [[Ux_new[i][j] for j in range(n)] for i in range(n)]
    Uy = [[Uy_new[i][j] for j in range(n)] for i in range(n)]
    U5 = [[U5_new[i][j] for j in range(n)] for i in range(n)]

    # if iters % print_period == 0:
    print(iters, max_diff)

    iters += 1
    if iters == max_iters or max_diff > 1000:
        break

    # if iters % 20 == 0:
    #     graph += [T]
print(iters)

plt.pcolormesh(T)
# plt.pcolormesh(U1)

# def animate(i):
#     ax1.clear()
#     ax1.pcolormesh(graph[i], cmap=cm.jet)


# fig = plt.figure(figsize=(11, 7), dpi=50)

# ax1 = fig.add_subplot(1, 1, 1)
# ani = animation.FuncAnimation(fig, animate, interval=50, frames=len(graph))


plt.show()

# print(T)
