# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo>=0.25.1",
#     "matplotlib>=3.8.0",
#     "numpy>=2.0.0",
# ]
# ///

"""Interactive companion to Lecture 8: the baseline New Keynesian model

Published as an interactive page on the teaching website.
"""

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="full")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.patches import ConnectionPatch
    from matplotlib.ticker import PercentFormatter

    plt.style.use("seaborn-v0_8-whitegrid")
    return ConnectionPatch, PercentFormatter, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # The baseline New Keynesian model

    ## 1 Full model

    The complete equilibrium system in Lecture 8 is

    $$
    \begin{aligned}
    x_t
    &=E_tx_{t+1}-(r_t-\bar r)+g_t
    &&\text{Dynamic IS}\\
    i_t
    &=r_t+E_t\pi_{t+1}
    &&\text{Fisher equation}\\
    i_t
    &=\bar r+\pi^T+\phi_{\pi}(\pi_t-\pi^T)+\phi_yx_t+v_t
    &&\text{Policy rule}\\
    \pi_t-\pi^T
    &=\beta E_t(\pi_{t+1}-\pi^T)+\kappa x_t+u_t
    &&\text{Phillips curve}
    \end{aligned}
    $$

    Here $x_t$ is the output gap, $r_t$ is the real interest rate, $i_t$ is
    the nominal interest rate, and $\pi_t$ is inflation. The parameters
    $\bar r$ and $\pi^T$ are the natural real rate and inflation target.
    The disturbances $g_t$, $v_t$, and $u_t$ are demand, monetary-policy,
    and cost-push shocks.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2 A household chooses optimally as income changes

    The lecture begins with a two-period household. With log utility, its
    problem is

    $$
    \max_{C_0,C_1,S_1}\;\log C_0+\beta\log C_1
    $$

    subject to

    $$
    C_0=Y_0-S_1,
    \qquad
    C_1=Y_1+(1+r_0)S_1
    $$

    The Euler equation $1/C_0=\beta(1+r_0)/C_1$ and the lifetime budget
    constraint determine the optimum. Change current income $Y_0$ below.
    Future income and the real interest rate remain fixed so the income
    effect is visible by itself.
    """)
    return


@app.cell(hide_code=True)
def _(np):
    def household_optimum(y0, y1, real_rate, discount_factor):
        """Return optimal consumption, saving, and lifetime utility."""
        c0 = (y0 + y1 / (1 + real_rate)) / (1 + discount_factor)
        c1 = discount_factor * (1 + real_rate) * c0
        saving = y0 - c0
        lifetime_utility = np.log(c0) + discount_factor * np.log(c1)
        return c0, c1, saving, lifetime_utility

    def indifference_curve(c0, utility_level, discount_factor):
        """Return C1 on a log-utility indifference curve."""
        return np.exp((utility_level - np.log(c0)) / discount_factor)

    return household_optimum, indifference_curve


@app.cell(hide_code=True)
def _(mo):
    income_today = mo.ui.slider(
        start=2,
        stop=18,
        step=0.5,
        value=10,
        label=r"Current income $Y_0$",
        show_value=True,
        full_width=True,
    )
    return (income_today,)


@app.cell(hide_code=True)
def _(household_optimum, income_today, indifference_curve, mo, np, plt):
    _y0 = float(income_today.value)
    _y1 = 10.0
    _real_rate = 0.04
    _beta = 0.96
    _c0_star, _c1_star, _saving, _utility = household_optimum(
        _y0, _y1, _real_rate, _beta
    )

    _wealth = _y0 + _y1 / (1 + _real_rate)
    _c0_grid = np.linspace(0.08, _wealth - 0.02, 800)
    _budget_c1 = _y1 + (1 + _real_rate) * (_y0 - _c0_grid)
    _indifference_c1 = indifference_curve(_c0_grid, _utility, _beta)
    _axis_max = max(20.0, 1.12 * _wealth * (1 + _real_rate))
    _visible = (_indifference_c1 > 0) & (_indifference_c1 < _axis_max)

    _fig, _ax = plt.subplots(figsize=(7.2, 5.6))
    _ax.plot(
        _c0_grid,
        _budget_c1,
        color="#006298",
        linewidth=2.6,
        label="Lifetime budget constraint",
    )
    _ax.plot(
        _c0_grid[_visible],
        _indifference_c1[_visible],
        color="#e57200",
        linewidth=2.6,
        label="Indifference curve through optimum",
    )
    _ax.scatter(
        [_y0],
        [_y1],
        marker="s",
        s=75,
        color="#6c757d",
        zorder=4,
        label=r"Income point $(Y_0,Y_1)$",
    )
    _ax.scatter(
        [_c0_star],
        [_c1_star],
        s=95,
        color="#990000",
        zorder=5,
        label=r"Optimum $(C_0^*,C_1^*)$",
    )
    _ax.plot(
        [_y0, _c0_star],
        [_y1, _c1_star],
        color="#990000",
        linestyle=":",
        linewidth=1.8,
    )
    _ax.set(
        xlim=(0, _axis_max),
        ylim=(0, _axis_max),
        xlabel=r"Current consumption $C_0$",
        ylabel=r"Future consumption $C_1$",
        title=fr"Optimal household choice when $Y_0={_y0:.1f}$",
    )
    _ax.legend(loc="upper right", fontsize=9)
    _ax.grid(alpha=0.25)
    _fig.tight_layout()

    if _saving > 1e-8:
        _choice = "saves"
    elif _saving < -1e-8:
        _choice = "borrows"
    else:
        _choice = "neither borrows nor saves"

    _readout = mo.vstack(
        [
            mo.md("### Change income"),
            income_today,
            mo.md(
                rf"""
                ### Optimal choice

                With $Y_1={_y1:.0f}$, $r_0={100 * _real_rate:.0f}\%$, and
                $\beta={_beta:.2f}$,

                $$
                C_0^*={_c0_star:.2f},
                \qquad
                C_1^*={_c1_star:.2f},
                \qquad
                S_1^*=Y_0-C_0^*={_saving:.2f}
                $$

                The household **{_choice}**. Moving $Y_0$ shifts the budget
                line and the tangency, so the optimal allocation updates
                rather than remaining at the old point.
                """
            ),
        ],
        gap=0.8,
    )
    mo.hstack([_fig, _readout], widths=[1.55, 1], align="start", gap=2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3 Connect IS, Fisher and monetary policy, and the Phillips curve

    Choose which interest rate to set. With expected inflation anchored at
    $\pi^T$, the other rate follows from the Fisher equation:

    - Setting $i_t$ determines $r_t=i_t-\pi^T$
    - Setting $r_t$ determines $i_t=r_t+\pi^T$
    - $E_tx_{t+1}$ shifts the dynamic IS curve

    To isolate these channels, expected inflation is anchored at $\pi^T$ and
    the current demand and cost-push shocks are zero. The left panel computes
    the current output gap from IS. The panel below it carries that same
    output gap to the Phillips curve to compute inflation. The panel on the
    upper right shows the Fisher-consistent rate pair and compares the
    nominal rate with the systematic policy rule.

    The readout shows the monetary-policy shock $v_t$ needed to reconcile
    the selected nominal rate with the systematic policy rule.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    rate_mode = mo.ui.radio(
        options={"Set nominal rate $i_t$": "nominal", "Set real rate $r_t$": "real"},
        value="Set nominal rate $i_t$",
        inline=True,
        label="Interest-rate input",
    )
    real_rate_control = mo.ui.slider(
        start=-0.02,
        stop=0.08,
        step=0.0025,
        value=0.005,
        label=r"Current real rate $r_t$",
        show_value=True,
        full_width=True,
    )
    nominal_rate_control = mo.ui.slider(
        start=-0.015,
        stop=0.085,
        step=0.0025,
        value=0.01,
        label=r"Current nominal rate $i_t$",
        show_value=True,
        full_width=True,
    )
    expected_output_control = mo.ui.slider(
        start=-0.04,
        stop=0.04,
        step=0.0025,
        value=0.0,
        label=r"Expected future output gap $E_tx_{t+1}$",
        show_value=True,
        full_width=True,
    )
    return (
        expected_output_control,
        nominal_rate_control,
        rate_mode,
        real_rate_control,
    )


@app.cell(hide_code=True)
def _(
    ConnectionPatch,
    PercentFormatter,
    expected_output_control,
    mo,
    nominal_rate_control,
    np,
    plt,
    rate_mode,
    real_rate_control,
):
    _beta = 0.995
    _r_bar = -np.log(_beta)
    _pi_target = 0.02 / 4
    _kappa = 0.25
    _phi_pi = 1.5
    _phi_y = 0.5 / 4

    _expected_y = float(expected_output_control.value)
    _expected_pi = _pi_target
    if rate_mode.value == "nominal":
        _i = float(nominal_rate_control.value)
        _r = _i - _expected_pi
        _active_rate_control = nominal_rate_control
    else:
        _r = float(real_rate_control.value)
        _i = _r + _expected_pi
        _active_rate_control = real_rate_control

    # With g_t = u_t = 0 and expected inflation anchored at the target
    _output_gap = _expected_y - (_r - _r_bar)
    _inflation = _pi_target + _kappa * _output_gap
    _nominal_rule_no_shock = (
        _r_bar
        + _pi_target
        + _phi_pi * (_inflation - _pi_target)
        + _phi_y * _output_gap
    )
    _implied_policy_shock = _i - _nominal_rule_no_shock

    # These bounds keep every outcome from the active rate and output sliders visible
    _x_limits = (-0.125, 0.075)
    _x_grid = np.linspace(*_x_limits, 500)
    _is_real_rate = _r_bar + _expected_y - _x_grid
    _r_grid = np.linspace(-0.035, 0.095, 500)
    _fisher_nominal_rate = _r_grid + _expected_pi
    _phillips_inflation = _pi_target + _kappa * _x_grid

    _fig = plt.figure(figsize=(11.8, 8.4))
    _grid = _fig.add_gridspec(2, 2, width_ratios=[1.1, 1], hspace=0.48, wspace=0.4)
    _is_ax = _fig.add_subplot(_grid[0, 0])
    _pc_ax = _fig.add_subplot(_grid[1, 0], sharex=_is_ax)
    _fisher_ax = _fig.add_subplot(_grid[0, 1], sharey=_is_ax)
    _axes = (_is_ax, _fisher_ax, _pc_ax)

    _is_ax.plot(
        _x_grid,
        _is_real_rate,
        color="#006298",
        linewidth=2.7,
        label="Dynamic IS",
    )
    _is_ax.axhline(_r_bar, color="#6c757d", linestyle="--", linewidth=1.2)
    _is_ax.scatter([_output_gap], [_r], color="#990000", s=80, zorder=5)
    _is_ax.axvline(_output_gap, color="#990000", linestyle=":", linewidth=1.4)
    _is_ax.set(
        xlim=_x_limits,
        ylim=(-0.035, 0.095),
        ylabel=r"Real interest rate $r_t$",
        title="IS",
    )
    _is_ax.legend(loc="upper right", fontsize=9)

    _fisher_ax.plot(
        _fisher_nominal_rate,
        _r_grid,
        color="#e57200",
        linewidth=2.7,
        label=r"Fisher $i_t=r_t+E_t\pi_{t+1}$",
    )
    _fisher_ax.axvline(
        _nominal_rule_no_shock,
        color="#5b2c83",
        linewidth=2.4,
        label=r"Policy rule with $v_t=0$",
    )
    _fisher_ax.scatter(
        [_i], [_r], color="#990000", s=80, zorder=5, label="Selected rate pair"
    )
    _fisher_ax.plot(
        [_nominal_rule_no_shock, _i],
        [_r, _r],
        color="#990000",
        linestyle=":",
        linewidth=1.6,
    )
    _fisher_ax.set(
        xlim=(-0.055, 0.105),
        ylim=(-0.035, 0.095),
        xlabel=r"Nominal interest rate $i_t$",
        ylabel=r"Real interest rate $r_t$",
        title="Fisher and policy rule",
    )
    _fisher_ax.yaxis.tick_right()
    _fisher_ax.yaxis.set_label_position("right")
    _fisher_ax.legend(loc="lower right", fontsize=8)

    _pc_ax.plot(
        _x_grid,
        _phillips_inflation,
        color="#008542",
        linewidth=2.7,
        label="Phillips curve",
    )
    _pc_ax.axhline(
        _pi_target,
        color="#6c757d",
        linestyle="--",
        linewidth=1.2,
        label=r"Inflation target $\pi^T$",
    )
    _pc_ax.scatter([_output_gap], [_inflation], color="#990000", s=80, zorder=5)
    _pc_ax.axvline(_output_gap, color="#990000", linestyle=":", linewidth=1.4)
    _pc_ax.set(
        xlim=_x_limits,
        ylim=(-0.025, 0.035),
        xlabel=r"Output gap $x_t$",
        ylabel=r"Inflation $\pi_t$",
    )
    _pc_ax.set_title("Phillips curve", loc="left")
    _pc_ax.legend(loc="upper left", fontsize=9)

    for _ax in _axes:
        _ax.xaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=1))
        _ax.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=1))
        _ax.grid(alpha=0.22)

    _is_to_fisher = ConnectionPatch(
        xyA=(_output_gap, _r),
        coordsA=_is_ax.transData,
        xyB=(_i, _r),
        coordsB=_fisher_ax.transData,
        arrowstyle="-|>",
        mutation_scale=12,
        color="#990000",
        linestyle=":",
        linewidth=1.7,
        clip_on=False,
    )
    _is_to_pc = ConnectionPatch(
        xyA=(_output_gap, _is_ax.get_ylim()[0]),
        coordsA=_is_ax.transData,
        xyB=(_output_gap, _pc_ax.get_ylim()[1]),
        coordsB=_pc_ax.transData,
        arrowstyle="-|>",
        mutation_scale=12,
        color="#990000",
        linestyle=":",
        linewidth=1.7,
        clip_on=False,
    )
    _fig.add_artist(_is_to_fisher)
    _fig.add_artist(_is_to_pc)
    _fig.suptitle("A connected New Keynesian accounting diagram", fontsize=15)
    _fig.subplots_adjust(left=0.09, right=0.9, bottom=0.09, top=0.91)

    _policy_description = (
        "contractionary" if _implied_policy_shock > 1e-8 else "expansionary"
    )
    if abs(_implied_policy_shock) <= 1e-8:
        _policy_description = "zero"

    _controls = mo.vstack(
        [
            mo.md("### Controls"),
            rate_mode,
            _active_rate_control,
            expected_output_control,
            mo.md(
                rf"""
                ### Linked outcome

                - IS output gap: $x_t={100 * _output_gap:.2f}\%$
                - Phillips inflation: $\pi_t={100 * _inflation:.2f}\%$
                - Real rate: $r_t={100 * _r:.2f}\%$
                - Nominal rate: $i_t={100 * _i:.2f}\%$
                - Systematic policy rate: ${100 * _nominal_rule_no_shock:.2f}\%$
                - Implied policy shock: $v_t={100 * _implied_policy_shock:.2f}\%$

                The implied policy shock is **{_policy_description}**. It is
                the horizontal dotted gap between the selected nominal rate
                and the purple policy-rule line. When the gap is zero, the
                policy rule holds without a monetary-policy shock.
                """
            ),
        ],
        gap=0.8,
    )
    mo.vstack([mo.hstack([_controls], widths=[1]), _fig], gap=1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Reading the connected panels

    1. Start with the chosen $r_t$ on the vertical axis of IS
    2. Read the implied current output gap where it meets the shifted IS curve
    3. Carry the same $x_t$ straight down to the Phillips curve to obtain current inflation
    4. Carry $r_t$ to the Fisher panel to read the Fisher-consistent $i_t$
    5. Compare that nominal rate with the policy rule
    """)
    return


if __name__ == "__main__":
    app.run()
