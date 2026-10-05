# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo>=0.24.0",
#     "matplotlib>=3.8.0",
#     "numpy>=2.0.0",
# ]
# ///

"""Interactive companion to the two-period cake-eating lecture

Run from the course workspace with

    .venv/Scripts/marimo run Topics/03-Frictionless-Markets/01_CakeEating_2periods_marimo.py
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    plt.style.use("seaborn-v0_8-whitegrid")
    return mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Cake eating in two periods

    A person begins with $K_0>0$ units of cake and chooses consumption today,
    $C_0$, and tomorrow, $C_1$. Cake does not grow or depreciate, and no cake
    is valuable after tomorrow, so

    $$
    C_0+C_1=K_0
    $$

    Lifetime utility is

    $$
    U(C_0,C_1)=\log C_0+\beta\log C_1,
    \qquad 0<\beta\leq 1
    $$

    Use the controls to connect the allocation, preferences, and tangency
    condition
    """)
    return


@app.cell
def _(np):
    def allocation(beta, k0):
        """Return the analytical optimum (C0*, C1*)"""
        return k0 / (1 + beta), beta * k0 / (1 + beta)

    def utility(c0, c1, beta):
        """Return lifetime utility under log preferences"""
        return np.log(c0) + beta * np.log(c1)

    def indifference_c1(c0, utility_level, beta):
        """Return C1 on the indifference curve indexed by utility_level"""
        return np.exp((utility_level - np.log(c0)) / beta)

    return allocation, indifference_c1, utility


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Divide the cake

    Select **Choose $C_0$ manually** to divide the cake yourself. Under a
    manual allocation, choose whether to hold $C_0$ fixed in units or as a
    share of $K_0$ as you change the initial cake. Select **Use the optimal
    split** to let the model apply the first-order condition $C_1/C_0=\beta$
    """)
    return


@app.cell
def _(mo):
    split_rule = mo.ui.radio(
        options={
            "Choose C₀ manually": "manual",
            "Use the optimal split": "optimal",
        },
        value="Choose C₀ manually",
        label="How should the cake be divided",
    )
    initial_cake = mo.ui.slider(
        start=2,
        stop=40,
        step=1,
        value=20,
        label=r"Initial cake $K_0$",
        show_value=True,
        full_width=True,
    )
    beta_input = mo.ui.number(
        start=0.05,
        stop=1.0,
        step=0.05,
        value=0.9,
        label=r"Discount factor $\beta$",
    )
    manual_allocation_rule = mo.ui.radio(
        options={
            "Hold C₀ fixed in units": "units",
            "Hold C₀ fixed as a share of K₀": "share",
        },
        value="Hold C₀ fixed in units",
        label="When K₀ changes, manual allocation",
    )
    c0_units = mo.ui.slider(
        start=0.5,
        stop=39.5,
        step=0.5,
        value=11,
        label=r"Consumption today $C_0$ (units)",
        show_value=True,
        full_width=True,
    )
    today_share = mo.ui.slider(
        start=5,
        stop=95,
        step=1,
        value=55,
        label=r"Share consumed today $100C_0/K_0$",
        show_value=True,
        full_width=True,
    )
    return (
        beta_input,
        c0_units,
        initial_cake,
        manual_allocation_rule,
        split_rule,
        today_share,
    )


@app.cell(hide_code=True)
def _(
    allocation,
    beta_input,
    c0_units,
    initial_cake,
    manual_allocation_rule,
    mo,
    np,
    plt,
    split_rule,
    today_share,
    utility,
):
    _beta = float(beta_input.value)
    _k0 = float(initial_cake.value)
    if split_rule.value == "optimal":
        _c0, _c1 = allocation(_beta, _k0)
        _rule_note = r"The first-order condition determines the split"
    elif manual_allocation_rule.value == "units":
        _c0 = min(float(c0_units.value), _k0 - 0.1)
        _c1 = _k0 - _c0
        _rule_note = r"$C_0$ is held fixed in units while feasible"
    else:
        _c0 = _k0 * today_share.value / 100
        _c1 = _k0 - _c0
        _rule_note = r"The share of $K_0$ consumed today is held fixed"

    _u0 = np.log(_c0)
    _u1 = np.log(_c1)
    _lifetime_u = utility(_c0, _c1, _beta)

    _fig, _ax = plt.subplots(figsize=(6.3, 5.2))
    _wedges, _texts, _autotexts = _ax.pie(
        [_c0, _c1],
        labels=[r"Today  $C_0$", r"Tomorrow  $C_1$"],
        autopct="%1.1f%%",
        startangle=90,
        colors=["#006298", "#e57200"],
        wedgeprops={"edgecolor": "white", "linewidth": 2},
        textprops={"fontsize": 11},
    )
    _ax.set_title(fr"Dividing $K_0={_k0:g}$ units of cake")
    _fig.tight_layout()

    _readout = mo.vstack(
        [
            mo.md("### Controls"),
            split_rule,
            initial_cake,
            beta_input,
            manual_allocation_rule,
            c0_units,
            today_share,
            mo.md(
                rf"""
                ### Utility readout

                - Today: $C_0={_c0:.2f}$ units, which is $100C_0/K_0={100 * _c0 / _k0:.1f}\%$
                - Tomorrow: $C_1={_c1:.2f}$ units, which is $100C_1/K_0={100 * _c1 / _k0:.1f}\%$
                - Utility today: $\log C_0=\log({_c0:.2f})={_u0:.3f}$
                - Utility tomorrow: $\log C_1=\log({_c1:.2f})={_u1:.3f}$
                - Aggregate: $U=\log C_0+\beta\log C_1$
                - Numerically: $U={_u0:.3f}+({_beta:.2f})({_u1:.3f})={_lifetime_u:.3f}$

                {_rule_note}
                """
            ),
        ],
        gap=0.8,
    )
    mo.hstack([_fig, _readout], widths=[1.35, 1], align="start", gap=2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Indifference curves

    Holding lifetime utility at $\bar U$ gives

    $$
    C_1=\exp\left(\frac{\bar U-\log C_0}{\beta}\right)
    $$

    Every point on a curve gives the same lifetime utility. Higher curves are
    preferred because they correspond to higher values of $\bar U$
    """)
    return


@app.cell
def _(mo):
    ubar_control = mo.ui.slider(
        start=-1,
        stop=6,
        step=0.1,
        value=3,
        label=r"Central utility level $\bar U$",
        show_value=True,
        full_width=True,
    )
    beta_curves = mo.ui.slider(
        start=0.1,
        stop=1.0,
        step=0.05,
        value=0.9,
        label=r"Discount factor $\beta$",
        show_value=True,
        full_width=True,
    )
    curve_range = mo.ui.slider(
        start=5,
        stop=40,
        step=1,
        value=20,
        label="Axis maximum",
        show_value=True,
        full_width=True,
    )
    return beta_curves, curve_range, ubar_control


@app.cell(hide_code=True)
def _(beta_curves, curve_range, indifference_c1, mo, np, plt, ubar_control):
    _beta = float(beta_curves.value)
    _ubar = float(ubar_control.value)
    _axis_max = float(curve_range.value)
    _c0_grid = np.linspace(0.05, _axis_max, 800)
    _levels = [_ubar - 1, _ubar, _ubar + 1]

    _fig, _ax = plt.subplots(figsize=(7.2, 5.2))
    for _level, _color, _width in zip(
        _levels,
        ["#7f8c8d", "#006298", "#e57200"],
        [1.8, 3.0, 1.8],
    ):
        _c1_curve = indifference_c1(_c0_grid, _level, _beta)
        _visible = _c1_curve <= _axis_max * 1.2
        _ax.plot(
            _c0_grid[_visible],
            _c1_curve[_visible],
            color=_color,
            linewidth=_width,
            label=fr"$\bar U={_level:.1f}$",
        )
    _ax.set(
        xlim=(0, _axis_max),
        ylim=(0, _axis_max),
        xlabel=r"Consumption today $C_0$",
        ylabel=r"Consumption tomorrow $C_1$",
        title=fr"Indifference curves when $\beta={_beta:.2f}$",
    )
    _ax.legend()
    _ax.grid(alpha=0.25)
    _fig.tight_layout()

    _panel = mo.vstack(
        [
            mo.md("### Controls"),
            ubar_control,
            beta_curves,
            curve_range,
            mo.md(
                rf"""
                ### Current curve

                - Central level: $\bar U={_ubar:.2f}$
                - Discount factor: $\beta={_beta:.2f}$
                - Slope: $\dfrac{{dC_1}}{{dC_0}}=-\dfrac{{C_1}}{{\beta C_0}}$
                - A larger $\beta$ places more weight on tomorrow's consumption
                """
            ),
        ],
        gap=1,
    )
    mo.hstack([_fig, _panel], widths=[1.45, 1], align="start", gap=2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Budget constraint and tangency

    The budget line is $C_1=K_0-C_0$, with slope $-1$. At the interior optimum,
    the indifference curve has the same slope

    $$
    -\frac{C_1^*}{\beta C_0^*}=-1
    \qquad\Longleftrightarrow\qquad
    \frac{C_1^*}{C_0^*}=\beta
    $$
    """)
    return


@app.cell
def _(mo):
    k0_tangency = mo.ui.slider(
        start=2,
        stop=40,
        step=1,
        value=20,
        label=r"Initial cake $K_0$",
        show_value=True,
        full_width=True,
    )
    beta_tangency = mo.ui.slider(
        start=0.1,
        stop=1.0,
        step=0.05,
        value=0.9,
        label=r"Discount factor $\beta$",
        show_value=True,
        full_width=True,
    )
    axis_max_tangency = mo.ui.slider(
        start=5,
        stop=50,
        step=1,
        value=25,
        label="Axis maximum",
        show_value=True,
        full_width=True,
    )
    show_neighboring_curves = mo.ui.switch(
        value=True,
        label="Show neighboring indifference curves",
    )
    return (
        axis_max_tangency,
        beta_tangency,
        k0_tangency,
        show_neighboring_curves,
    )


@app.cell(hide_code=True)
def _(
    allocation,
    axis_max_tangency,
    beta_tangency,
    indifference_c1,
    k0_tangency,
    mo,
    np,
    plt,
    show_neighboring_curves,
    utility,
):
    _beta = float(beta_tangency.value)
    _k0 = float(k0_tangency.value)
    _axis_max = float(axis_max_tangency.value)
    _c0_star, _c1_star = allocation(_beta, _k0)
    _u_star = utility(_c0_star, _c1_star, _beta)
    _c0_grid = np.linspace(0.01, _axis_max, 900)

    _fig, _ax = plt.subplots(figsize=(7.2, 5.5))
    _ax.plot(
        [0, _k0],
        [_k0, 0],
        color="black",
        linewidth=2.4,
        label=r"Budget line $C_0+C_1=K_0$",
    )

    if show_neighboring_curves.value:
        for _shift, _style in [(-0.7, "--"), (0.7, ":")]:
            _curve = indifference_c1(_c0_grid, _u_star + _shift, _beta)
            _visible = _curve <= _axis_max * 1.2
            _ax.plot(
                _c0_grid[_visible],
                _curve[_visible],
                color="#9aa0a6",
                linestyle=_style,
                linewidth=1.5,
                label=fr"$\bar U=U^*{_shift:+.1f}$",
            )

    _tangent_curve = indifference_c1(_c0_grid, _u_star, _beta)
    _visible = _tangent_curve <= _axis_max * 1.2
    _ax.plot(
        _c0_grid[_visible],
        _tangent_curve[_visible],
        color="#006298",
        linewidth=3,
        label=r"Tangent curve $\bar U=U^*$",
    )
    _ax.scatter(
        [_c0_star],
        [_c1_star],
        s=95,
        color="#e57200",
        edgecolor="white",
        linewidth=1.4,
        zorder=5,
        label="Optimal allocation",
    )
    _ax.annotate(
        fr"$({ _c0_star:.2f},\ {_c1_star:.2f})$",
        xy=(_c0_star, _c1_star),
        xytext=(10, 12),
        textcoords="offset points",
        fontsize=11,
    )
    _ax.set(
        xlim=(0, _axis_max),
        ylim=(0, _axis_max),
        xlabel=r"Consumption today $C_0$",
        ylabel=r"Consumption tomorrow $C_1$",
        title="Feasibility and the utility-maximizing tangency",
    )
    _ax.legend(fontsize=9, loc="upper right")
    _ax.grid(alpha=0.25)
    _ax.set_aspect("equal", adjustable="box")
    _fig.tight_layout()

    _mrs = _c1_star / (_beta * _c0_star)
    _panel = mo.vstack(
        [
            mo.md("### Controls"),
            k0_tangency,
            beta_tangency,
            axis_max_tangency,
            show_neighboring_curves,
            mo.md(
                rf"""
                ### Optimal allocation

                - $C_0^*=\dfrac{{K_0}}{{1+\beta}}={_c0_star:.3f}$
                - $C_1^*=\dfrac{{\beta K_0}}{{1+\beta}}={_c1_star:.3f}$
                - $U^*=\log C_0^*+\beta\log C_1^*={_u_star:.3f}$
                - Budget slope: $-1$
                - Indifference-curve slope at the optimum: $-{_mrs:.3f}$

                The two slopes coincide, so the highest attainable
                indifference curve is tangent to the budget line
                """
            ),
        ],
        gap=1,
    )
    mo.hstack([_fig, _panel], widths=[1.45, 1], align="start", gap=2)
    return


if __name__ == "__main__":
    app.run()
