# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo>=0.23.3",
#     "matplotlib>=3.8.0",
#     "numpy>=2.0.0",
# ]
# ///

"""Interactive Solow growth model demonstration.

Run with::

    marimo run Solow_demonstrate.py

The notation is written with words rather than Greek symbols so that the
equations and code use the same names throughout the demonstration.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="full")


@app.cell
def _():
    import matplotlib.pyplot as plt
    import numpy as np
    import marimo as mo

    return mo, np, plt


@app.cell
def _(mo):
    mo.md(r"""
    # Solow Growth Model

    Let $k_t$ denote capital per worker in period $t$. Its law of motion is

    $$
    k_{t+1}
    = \frac{s A k_t^{\alpha} + (1-\delta)k_t}{1+n},
    $$

    where $s$ is the saving rate, $A$ is productivity, $\alpha$ is capital's
    share of income, $\delta$ is the depreciation rate, and $n$ is the
    population growth rate. Output per worker is

    $$
    y_t = A k_t^{\alpha}.
    $$

    At the steady state $k^\ast$, capital per worker is constant. Therefore,

    $$
    s A (k^\ast)^{\alpha} = (\delta+n)k^\ast,
    $$

    which implies

    $$
    k^\ast
    = \left(\frac{sA}{\delta+n}\right)^{\frac{1}{1-\alpha}}.
    $$
    """)
    return


@app.cell
def _(mo):
    saving_rate_slider = mo.ui.slider(
        start=5, stop=80, step=1, value=40, label="saving rate (%)",    show_value=True,
    )
    depreciation_rate_slider = mo.ui.slider(
        start=1, stop=15, step=0.5, value=5, label="depreciation rate (% per year)",    show_value=True,
    )
    population_growth_slider = mo.ui.slider(
        start=0, stop=8, step=0.5, value=1.5, label="population growth rate (% per year)",    show_value=True,
    )
    capital_share_slider = mo.ui.slider(
        start=10, stop=90, step=1, value=30, label="capital share (%)",    show_value=True,
    )
    productivity_slider = mo.ui.slider(
        start=0.5, stop=4, step=0.1, value=2, label="productivity",    show_value=True,

    )

    controls = mo.vstack(
        [
            saving_rate_slider,
            depreciation_rate_slider,
            population_growth_slider,
            capital_share_slider,
            productivity_slider,
        ],
        gap=1,
    )
    controls
    return (
        capital_share_slider,
        depreciation_rate_slider,
        population_growth_slider,
        productivity_slider,
        saving_rate_slider,
    )


@app.cell
def _(
    capital_share_slider,
    depreciation_rate_slider,
    mo,
    np,
    plt,
    population_growth_slider,
    productivity_slider,
    saving_rate_slider,
):
    saving_rate = saving_rate_slider.value / 100
    depreciation_rate = depreciation_rate_slider.value / 100
    population_growth_rate = population_growth_slider.value / 100
    capital_share = capital_share_slider.value / 100
    productivity = productivity_slider.value

    capital_star = (
        saving_rate * productivity / (depreciation_rate + population_growth_rate)
    ) ** (1 / (1 - capital_share))
    output_star = productivity * capital_star**capital_share

    capital_grid = np.linspace(0.01, max(25, capital_star * 2.2), 400)
    output = productivity * capital_grid**capital_share
    investment = saving_rate * output
    break_even = (depreciation_rate + population_growth_rate) * capital_grid

    _fig_curves, _ax_curves = plt.subplots(figsize=(8, 5))
    _ax_curves.plot(capital_grid, output, color="#4caf50", linewidth=2.5, label="Output")
    _ax_curves.plot(capital_grid, investment, color="#3478eb", linewidth=2.5, label="Investment")
    _ax_curves.plot(
        capital_grid,
        break_even,
        color="black",
        linestyle="--",
        linewidth=1.8,
        label="Break-even investment",
    )
    _ax_curves.scatter([capital_star], [investment[np.argmin(abs(capital_grid - capital_star))]], color="#3478eb", zorder=4)
    _ax_curves.axvline(capital_star, color="#3478eb", linestyle=":", linewidth=1.2)
    _ax_curves.set_title("Output, investment, and break-even investment")
    _ax_curves.set_xlabel("Capital per worker")
    _ax_curves.set_ylabel("Per-worker value")
    _ax_curves.grid(alpha=0.25)
    _ax_curves.legend()
    _ax_curves.set_xlim(0, 80)
    _ax_curves.set_ylim(0, 8)

    _fig_curves.tight_layout()

    mo.hstack(
        [
            mo.md(
                rf"""
                **Steady-state values**

                $$
                k^\ast = {capital_star:.2f},
                \qquad
                y^\ast = {output_star:.2f}.
                $$

                At $k^\ast$, investment equals break-even investment:

                $$
                sA(k^\ast)^\alpha = (\delta+n)k^\ast.
                $$
                """
            ),
            _fig_curves,
        ],
        widths=[1, 2],
    )
    return (
        capital_share,
        capital_star,
        depreciation_rate,
        output_star,
        population_growth_rate,
        productivity,
        saving_rate,
    )


@app.cell
def _(mo):
    mo.md(r"""
    ## Capital transitions

    The plots below start one economy below the steady state and another
    above it. Both use the same parameters and converge toward the same
    steady-state capital per worker, $k^\ast$, and its associated output
    per worker, $y^\ast$.
    """)
    return


@app.cell
def _(capital_star, mo):
    below_initial_slider = mo.ui.slider(
        start=0.1, stop=max(1, capital_star * 1.5), step=0.1,
        value=max(0.1, round(capital_star * 0.5, 1)), label="initial capital below steady state",    show_value=True,
    )
    above_initial_slider = mo.ui.slider(
        start=0.1, stop=max(2, capital_star * 2.5), step=0.1,
        value=max(0.2, round(capital_star * 1.5, 1)), label="initial capital above steady state",    show_value=True,
    )
    periods_slider = mo.ui.slider(start=10, stop=150, step=5, value=60, label="number of periods",    show_value=True,
    )
    mo.vstack([below_initial_slider, above_initial_slider, periods_slider])
    return above_initial_slider, below_initial_slider, periods_slider


@app.cell
def _(
    above_initial_slider,
    below_initial_slider,
    capital_share,
    capital_star,
    depreciation_rate,
    mo,
    np,
    output_star,
    periods_slider,
    plt,
    population_growth_rate,
    productivity,
    saving_rate,
):
    def capital_update(capital):
        return (
            saving_rate * productivity * capital**capital_share
            + (1 - depreciation_rate) * capital
        ) / (1 + population_growth_rate)

    def path_from(initial_capital, periods):
        path = [initial_capital]
        for _ in range(periods):
            path.append(capital_update(path[-1]))
        return np.asarray(path)

    _periods_transition = periods_slider.value
    below_path = path_from(below_initial_slider.value, _periods_transition)
    above_path = path_from(above_initial_slider.value, _periods_transition)
    below_output_path = productivity * below_path**capital_share
    above_output_path = productivity * above_path**capital_share
    time = np.arange(_periods_transition + 1)

    _fig_transition, (_ax_capital, _ax_output) = plt.subplots(1, 2, figsize=(13, 5))

    _ax_capital.plot(
        time, below_path, color="#3478eb", linewidth=2, label="Below steady state"
    )
    _ax_capital.plot(
        time, above_path, color="#d95f02", linewidth=2, label="Above steady state"
    )
    _ax_capital.axhline(
        capital_star,
        color="black",
        linestyle="--",
        linewidth=1.5,
        label="Steady state",
    )
    _ax_capital.set_title("Capital per worker over time")
    _ax_capital.set_xlabel("Time")
    _ax_capital.set_ylabel("Capital per worker")
    _ax_capital.set_xlim(0, _periods_transition + 5)
    _ax_capital.set_ylim(bottom=0)
    _ax_capital.grid(alpha=0.25)
    _ax_capital.legend()

    _ax_output.plot(
        time,
        below_output_path,
        color="#3478eb",
        linewidth=2,
        label="Below steady state",
    )
    _ax_output.plot(
        time,
        above_output_path,
        color="#d95f02",
        linewidth=2,
        label="Above steady state",
    )
    _ax_output.axhline(
        output_star,
        color="black",
        linestyle="--",
        linewidth=1.5,
        label="Steady state",
    )
    _ax_output.set_title("Output per worker over time")
    _ax_output.set_xlabel("Time")
    _ax_output.set_ylabel("Output per worker")
    _ax_output.set_xlim(0, _periods_transition + 5)
    _ax_output.set_ylim(bottom=0)
    _ax_output.grid(alpha=0.25)
    _ax_output.legend()

    _fig_transition.tight_layout()

    mo.vstack(
        [
            _fig_transition,
            mo.md("The output paths are calculated from $y_t = A k_t^\\alpha$."),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
