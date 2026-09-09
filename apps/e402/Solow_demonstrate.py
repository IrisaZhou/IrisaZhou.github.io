# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo>=0.24.0",
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

__generated_with = "0.24.0"
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
        population_growth_rate,
        productivity,
        saving_rate,
    )


@app.cell
def _(mo):
    mo.md(r"""
    ## Capital transitions

    The next plot starts one economy below the steady state and another
    above it. Both use the same parameters and converge toward the same
    steady-state capital per worker, $k^\ast$.
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
    time = np.arange(_periods_transition + 1)

    _fig_transition, _ax_transition = plt.subplots(figsize=(8, 5))
    _ax_transition.plot(time, below_path, color="#3478eb", linewidth=2, label="Below steady state")
    _ax_transition.plot(time, above_path, color="#d95f02", linewidth=2, label="Above steady state")
    _ax_transition.axhline(capital_star, color="black", linestyle="--", linewidth=1.5, label="Steady state")
    _ax_transition.set_title("Capital per worker over time")
    _ax_transition.set_xlabel("Time")
    _ax_transition.set_ylabel("Capital per worker")
    _ax_transition.grid(alpha=0.25)
    _ax_transition.legend()
    _ax_transition.set_xlim(0, _periods_transition+5)
    _ax_transition.set_ylim(0,80)

    _fig_transition.tight_layout()

    mo.vstack([_fig_transition, mo.md("Both paths use the same capital update rule")])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## The `Solow` class

    The class below follows the object-oriented implementation from the
    Jupyter notebook. Each object stores its current capital per worker,
    updates it one period at a time, and can generate a complete path.
    """)
    return


@app.class_definition
class Solow:
    """Solow growth model with a discrete capital update rule."""

    def __init__(
        self,
        population_growth_rate=0.05,
        saving_rate=0.25,
        depreciation_rate=0.1,
        capital_share=0.3,
        productivity=2.0,
        capital=1.0,
    ):
        self.population_growth_rate = population_growth_rate
        self.saving_rate = saving_rate
        self.depreciation_rate = depreciation_rate
        self.capital_share = capital_share
        self.productivity = productivity
        self.capital = capital

    def steady_state(self):
        """Return the steady-state capital per worker."""
        return (
            self.saving_rate * self.productivity
            / (self.population_growth_rate + self.depreciation_rate)
        ) ** (1 / (1 - self.capital_share))

    def output(self, capital=None):
        """Return output per worker at the supplied capital level."""
        if capital is None:
            capital = self.capital
        return self.productivity * capital**self.capital_share

    def investment(self, capital=None):
        """Return investment per worker at the supplied capital level."""
        return self.saving_rate * self.output(capital)

    def break_even_investment(self, capital=None):
        """Return investment needed to keep capital per worker constant."""
        if capital is None:
            capital = self.capital
        return (self.population_growth_rate + self.depreciation_rate) * capital

    def update(self):
        """Update capital per worker one period forward."""
        self.capital = (
            self.saving_rate * self.productivity * self.capital**self.capital_share
            + (1 - self.depreciation_rate) * self.capital
        ) / (1 + self.population_growth_rate)
        return self.capital

    def generate_sequence(self, periods):
        """Return a capital-per-worker path of the requested length."""
        path = []
        for _ in range(periods):
            path.append(self.capital)
            self.update()
        return path


@app.cell
def _(mo, plt):
    default_model = Solow()
    high_capital_model = Solow(capital=8.0)

    _class_periods = 60
    steady_state_path = [default_model.steady_state()] * _class_periods
    default_path = default_model.generate_sequence(_class_periods)
    high_capital_path = high_capital_model.generate_sequence(_class_periods)

    _fig_class, _ax_class = plt.subplots(figsize=(8, 5))
    _ax_class.plot(steady_state_path, color="black", linestyle="--", label="Steady state")

    # Show the steady-state value
    steady_state_value = steady_state_path[-1]
    _ax_class.text(
        len(steady_state_path) - 2,
        steady_state_value - 0.5,
        f"{steady_state_value:.2f}",
        ha="left",
        va="center"
    )


    # Plot the paths generated by each model
    _ax_class.plot(
        default_path,
        marker=".",
        markersize=3,
        label="Class path from initial capital 1.0",
    )
    _ax_class.plot(
        high_capital_path,
        marker=".",
        markersize=3,
        label="Class path from initial capital 8.0",
    )


    _ax_class.set_title("Time series generated by the Solow class")
    _ax_class.set_xlabel("Time")
    _ax_class.set_ylabel("Capital per worker")
    _ax_class.grid(alpha=0.25)
    _ax_class.legend()
    _fig_class.tight_layout()
    mo.vstack([_fig_class, mo.md("The two class objects share parameters but begin with different capital stocks")])
    return default_model, default_path, steady_state_path


@app.cell
def _(default_path, mo, plt, steady_state_path):
    _class_periods = 60
    # include the high capital share model (they have a different steady state)
    high_capital_share_model = Solow(capital_share=0.5)
    high_capital_share_steady_state = [high_capital_share_model.steady_state()] * _class_periods

    _fig_class, _ax_class = plt.subplots(figsize=(8, 5))
    _ax_class.plot(steady_state_path, color="black", linestyle="--", label="Steady state")
    _ax_class.plot(high_capital_share_steady_state, color="red", linestyle="-.", label="Steady state (high capital share)")

    # Show the steady-state value
    _steady_state_value = steady_state_path[-1]
    _ax_class.text(
        len(steady_state_path) - 2,
        _steady_state_value - 0.5,
        f"{_steady_state_value:.2f}",
        ha="left",
        va="center"
    )

    high_capital_share_steady_state_value = high_capital_share_steady_state[-1]
    _ax_class.text(
        len(high_capital_share_steady_state) - 2,
        high_capital_share_steady_state_value - 0.5,
        f"{high_capital_share_steady_state_value:.2f}",
        ha="left",
        va="center",
        color="red"
    )

    # Plot the paths generated by each model
    _ax_class.plot(
        default_path,
        marker=".",
        markersize=3,
        label="Class path from initial capital 1.0",
    )

    _ax_class.plot(
        high_capital_share_model.generate_sequence(_class_periods),
        marker=".",
        markersize=3,
        label="Class path from initial capital 1.0 with capital share 0.5",
    )

    _ax_class.set_title("Time series generated by the Solow class")
    _ax_class.set_xlabel("Time")
    _ax_class.set_ylabel("Capital per worker")
    _ax_class.grid(alpha=0.25)
    _ax_class.legend()
    _fig_class.tight_layout()
    mo.vstack([_fig_class, mo.md("The two class objects begin with same initial capital stocks, but have different capital shares.")])
    return


if __name__ == "__main__":
    app.run()
