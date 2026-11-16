# /// script
# requires-python = ">=3.11"
# dependencies = ["marimo>=0.24.0", "matplotlib>=3.8", "numpy>=2.0", "scipy>=1.12"]
# ///

"""Interactive McCall search model based on 03_mccall_model.ipynb.

Run with:
.venv/bin/marimo run Topics/04-Frictional-Market/mccall_model.py
"""

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy.stats import betabinom

    plt.style.use("seaborn-v0_8-whitegrid")
    return betabinom, mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # A simple McCall search model

    ## 1 · Setup

    | Time $t-1$ | Time $t$ | Time $t+1$ and onward |
    |---|---|---|
    | Unemployed, waiting for an offer | Receives wage offer $W_t$ | Follows the branch selected at time $t$ |

    At time $t$, the worker chooses one of two actions:

    $$
    \begin{array}{rcl}
    \text{Accept } W_t &\longrightarrow& \text{Employed permanently at wage } W_t \\
    \text{Reject } W_t &\longrightarrow& \text{Unemployed at } t+1,\text{ receives benefits } b,\text{ and draws a new offer} \\
    \end{array}
    $$

    In other words, computatioally:

    An unemployed worker observes an IID wage offer $w \in \{w_0,\ldots,w_n\}$ and either accepts it forever or rejects it, receives $b$, and draws again next period. If the distribution of wage offers is $\phi(w)$, the worker's problem is to choose a policy $\sigma(w)\in\{0,1\}$ that maximizes expected discounted income:

    $$
    v^*(w)=\max\left\{\frac{w}{1-\beta},\; b+\beta\sum_{w'}v^*(w')\phi(w')\right\}
    $$

    The implied reservation wage $\bar w$ is the lowest wage that the worker will accept, and the optimal policy is to accept any offer above this threshold:
    $$
    \bar w=(1-\beta)\left[b+\beta\sum_{w'}v^*(w')\phi(w')\right],
    \qquad \sigma(w)=\mathbf 1\{w\geq \bar w\}
    $$

    For this example, the wage probabilities follow a beta-binomial distribution with shape parameters $BB_a$ and $BB_b$
    """)
    return


@app.cell
def _(mo):
    benefit_input = mo.ui.number(
        start=0, stop=100, step=1, value=25,
        label="Unemployment benefit b",
    )
    beta_input = mo.ui.number(
        start=0.50, stop=0.999, step=0.001, value=0.99,
        label="Discount factor β",
    )
    tolerance_input = mo.ui.dropdown(
        options={"Quick · 1e-4": 1e-4, "Precise · 1e-6": 1e-6, "Very precise · 1e-8": 1e-8},
        value="Precise · 1e-6",
        label="Convergence tolerance",
    )
    mo.hstack(
        [benefit_input, beta_input, tolerance_input],
        widths="equal",
        gap=2,
    )
    return benefit_input, beta_input, tolerance_input


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2 · Wage-offer distribution

    Use the entry boxes to reshape the discrete offer distribution and its wage support
    """)
    return


@app.cell
def _(mo):
    support_input = mo.ui.number(
        start=5, stop=150, step=1, value=50,
        label="Number of beta-binomial trials n",
    )
    shape_a_input = mo.ui.number(
        start=0.1, stop=500, step=1, value=200,
        label="First shape BB_a",
    )
    shape_b_input = mo.ui.number(
        start=0.1, stop=500, step=1, value=100,
        label="Second shape BB_b",
    )
    wage_min_input = mo.ui.number(
        start=0, stop=100, step=1, value=10,
        label="Minimum wage offer",
    )
    wage_max_input = mo.ui.number(
        start=1, stop=200, step=1, value=60,
        label="Maximum wage offer",
    )
    mo.vstack([
        mo.hstack([support_input, shape_a_input, shape_b_input], widths="equal", gap=2),
        mo.hstack([wage_min_input, wage_max_input], widths="equal", gap=2),
    ])
    return (
        shape_a_input,
        shape_b_input,
        support_input,
        wage_max_input,
        wage_min_input,
    )


@app.cell
def _(
    betabinom,
    mo,
    np,
    shape_a_input,
    shape_b_input,
    support_input,
    wage_max_input,
    wage_min_input,
):
    trial_count = int(support_input.value)
    shape_a = float(shape_a_input.value)
    shape_b = float(shape_b_input.value)
    wage_min = float(wage_min_input.value)
    wage_max = float(wage_max_input.value)

    invalid_support = wage_max <= wage_min
    mo.stop(
        invalid_support,
        mo.callout("Maximum wage must be larger than minimum wage", kind="danger"),
    )

    wage_grid = np.linspace(wage_min, wage_max, trial_count + 1)
    offer_probabilities = betabinom.pmf(
        np.arange(trial_count + 1), trial_count, shape_a, shape_b
    )
    offer_probabilities = offer_probabilities / offer_probabilities.sum()
    expected_offer = float(offer_probabilities @ wage_grid)
    probability_peak = float(wage_grid[int(np.argmax(offer_probabilities))])
    return (
        expected_offer,
        offer_probabilities,
        probability_peak,
        shape_a,
        shape_b,
        trial_count,
        wage_grid,
    )


@app.cell(hide_code=True)
def _(
    expected_offer,
    mo,
    offer_probabilities,
    plt,
    probability_peak,
    shape_a,
    shape_b,
    trial_count,
    wage_grid,
):
    distribution_figure, distribution_axis = plt.subplots(figsize=(10, 4.2))
    markerline, stemlines, baseline = distribution_axis.stem(
        wage_grid, offer_probabilities, linefmt="#0072B2", markerfmt="o", basefmt=" "
    )
    plt.setp(markerline, markersize=4, markerfacecolor="#0072B2")
    plt.setp(stemlines, linewidth=1.4, alpha=0.8)
    distribution_axis.axvline(
        expected_offer, color="#D55E00", linestyle="--", linewidth=2,
        label=f"Mean offer = {expected_offer:.2f}",
    )
    distribution_axis.set(
        title=f"Beta-binomial wage offers · n={trial_count}, BB_a={shape_a:g}, BB_b={shape_b:g}",
        xlabel="Wage offer",
        ylabel="Probability",
    )
    distribution_axis.legend(frameon=True)
    distribution_figure.tight_layout()

    mo.vstack([
        distribution_figure,
        mo.callout(
            f"Expected offer: **{expected_offer:.2f}**  ·  "
            f"Most likely grid wage: **{probability_peak:.2f}**  ·  "
            f"Probabilities sum to **{offer_probabilities.sum():.6f}**",
            kind="info",
        ),
    ])
    return


@app.cell
def _(np):
    def bellman_path(wages, probabilities, benefit, discount, tolerance, max_steps=20_000):
        """Return successive value functions and implied reservation wages."""
        current_value = wages / (1.0 - discount)
        value_history = [current_value.copy()]
        reservation_history = [
            (1.0 - discount)
            * (benefit + discount * float(probabilities @ current_value))
        ]
        errors = []

        for _step in range(max_steps):
            continuation = benefit + discount * float(probabilities @ current_value)
            next_value = np.maximum(wages / (1.0 - discount), continuation)
            error = float(np.max(np.abs(next_value - current_value)))
            errors.append(error)
            value_history.append(next_value.copy())
            reservation_history.append(
                (1.0 - discount)
                * (benefit + discount * float(probabilities @ next_value))
            )
            current_value = next_value
            if error <= tolerance:
                break

        return (
            np.asarray(value_history),
            np.asarray(reservation_history),
            np.asarray(errors),
        )

    def reservation_wage(wages, probabilities, benefit, discount, tolerance=1e-7):
        """Solve the scalar continuation-value fixed point."""
        continuation = benefit + discount * float(probabilities @ (wages / (1.0 - discount)))
        for _step in range(20_000):
            updated = benefit + discount * float(
                probabilities @ np.maximum(wages / (1.0 - discount), continuation)
            )
            if abs(updated - continuation) <= tolerance:
                continuation = updated
                break
            continuation = updated
        return (1.0 - discount) * continuation

    return bellman_path, reservation_wage


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3 · Value-function iteration

    The graphical demonstration begins at $n=1$

    The summary reports the optimal threshold $w^*$ and the number of Bellman updates needed to reach it, while the stepper shows one $n\rightarrow n+1$ update at a time
    """)
    return


@app.cell
def _(
    bellman_path,
    benefit_input,
    beta_input,
    offer_probabilities,
    tolerance_input,
    wage_grid,
):
    model_benefit = float(benefit_input.value)
    model_beta = float(beta_input.value)
    model_tolerance = float(tolerance_input.value)
    value_path, reservation_path, iteration_errors = bellman_path(
        wage_grid,
        offer_probabilities,
        model_benefit,
        model_beta,
        model_tolerance,
    )
    final_update_index = len(value_path) - 2
    return (
        final_update_index,
        iteration_errors,
        model_benefit,
        model_beta,
        model_tolerance,
        reservation_path,
        value_path,
    )


@app.cell
def _(final_update_index, mo, reservation_path):
    first_displayed_iteration = min(1, final_update_index)
    updates_to_convergence = final_update_index + 1
    optimal_threshold = float(reservation_path[-1])
    iteration_input = mo.ui.number(
        start=first_displayed_iteration,
        stop=final_update_index,
        step=1,
        value=first_displayed_iteration,
        label="Bellman update n → n+1",
    )
    comparison_toggle = mo.ui.switch(
        value=True,
        label="Show the n+1 update",
    )
    mo.vstack([
        mo.callout(
            f"Optimal reservation threshold: **w* = {optimal_threshold:.3f}**  ·  "
            f"Updates to convergence: **{updates_to_convergence}**",
            kind="success",
        ),
        mo.hstack([iteration_input, comparison_toggle], justify="start", gap=3),
    ])
    return comparison_toggle, iteration_input


@app.cell(hide_code=True)
def _(
    comparison_toggle,
    final_update_index,
    iteration_errors,
    iteration_input,
    mo,
    model_tolerance,
    plt,
    reservation_path,
    value_path,
    wage_grid,
):
    selected_iteration = min(int(iteration_input.value), final_update_index)
    next_iteration = selected_iteration + 1
    has_converged = selected_iteration == final_update_index

    value_figure, value_axis = plt.subplots(figsize=(10.5, 5.2))
    value_axis.plot(
        wage_grid,
        value_path[selected_iteration],
        color="#0072B2",
        linewidth=2.6,
        label=f"v{selected_iteration}",
    )
    value_axis.axvline(
        reservation_path[selected_iteration],
        color="#0072B2",
        linestyle=":",
        linewidth=2,
        label=f"w{selected_iteration} = {reservation_path[selected_iteration]:.3f}",
    )

    if comparison_toggle.value:
        final_label = "v*" if has_converged else f"v{next_iteration}"
        final_wage_label = "w*" if has_converged else f"w{next_iteration}"
        value_axis.plot(
            wage_grid,
            value_path[next_iteration],
            color="#D55E00",
            linewidth=2.6,
            linestyle="--",
            label=final_label,
        )
        value_axis.axvline(
            reservation_path[next_iteration],
            color="#D55E00",
            linestyle="--",
            linewidth=2,
            label=f"{final_wage_label} = {reservation_path[next_iteration]:.3f}",
        )

    value_axis.set(
        title=(
            "Converged value function and reservation wage"
            if has_converged
            else f"One update only · iteration {selected_iteration} → {next_iteration}"
        ),
        xlabel="Wage offered",
        ylabel="Lifetime value",
    )
    value_axis.legend(frameon=True, loc="best", ncol=2)
    value_figure.tight_layout()

    value_change = iteration_errors[selected_iteration]
    wage_change = reservation_path[next_iteration] - reservation_path[selected_iteration]
    status_kind = "success" if has_converged else "info"
    status_text = (
        f"**Converged:** max value change = **{value_change:.3g}** ≤ "
        f"tolerance **{model_tolerance:g}**  ·  "
        f"$w^*$ = **{reservation_path[next_iteration]:.3f}**"
        if has_converged
        else f"Max value change: **{value_change:.3f}**  ·  "
        f"Reservation-wage change: **{wage_change:+.4f}**  ·  "
        f"Current threshold: **{reservation_path[next_iteration]:.3f}**"
    )
    mo.vstack([value_figure, mo.callout(status_text, kind=status_kind)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4 · Comparative statics

    Choose two different parameters for the heatmap axes

    The other two parameters stay at their current values from Sections 1 and 2
    """)
    return


@app.cell
def _(mo):
    parameter_options = {
        "Unemployment benefit b": "b",
        "Discount factor β": "beta",
        "First shape BB_a": "BB_a",
        "Second shape BB_b": "BB_b",
    }
    x_parameter_input = mo.ui.dropdown(
        options=parameter_options,
        value="Unemployment benefit b",
        label="Horizontal parameter",
    )
    y_parameter_input = mo.ui.dropdown(
        options=parameter_options,
        value="Discount factor β",
        label="Vertical parameter",
    )
    mo.hstack([x_parameter_input, y_parameter_input], widths="equal", gap=2)
    return x_parameter_input, y_parameter_input


@app.cell
def _(
    betabinom,
    mo,
    model_benefit,
    model_beta,
    np,
    reservation_wage,
    shape_a,
    shape_b,
    trial_count,
    wage_grid,
    x_parameter_input,
    y_parameter_input,
):
    x_parameter = x_parameter_input.value
    y_parameter = y_parameter_input.value
    mo.stop(
        x_parameter == y_parameter,
        mo.callout("Choose two different parameters for the heatmap", kind="warn"),
    )

    comparative_grids = {
        "b": np.linspace(10.0, 40.0, 25),
        "beta": np.linspace(0.90, 0.995, 25),
        "BB_a": np.linspace(40.0, 300.0, 25),
        "BB_b": np.linspace(40.0, 300.0, 25),
    }
    comparative_labels = {
        "b": "Unemployment benefit b",
        "beta": "Discount factor β",
        "BB_a": "First shape BB_a",
        "BB_b": "Second shape BB_b",
    }
    comparative_defaults = {
        "b": model_benefit,
        "beta": model_beta,
        "BB_a": shape_a,
        "BB_b": shape_b,
    }
    x_grid = comparative_grids[x_parameter]
    y_grid = comparative_grids[y_parameter]
    reservation_surface = np.empty((len(y_grid), len(x_grid)))

    for y_index, y_value in enumerate(y_grid):
        for x_index, x_value in enumerate(x_grid):
            local_parameters = comparative_defaults.copy()
            local_parameters[x_parameter] = float(x_value)
            local_parameters[y_parameter] = float(y_value)
            local_probabilities = betabinom.pmf(
                np.arange(trial_count + 1),
                trial_count,
                local_parameters["BB_a"],
                local_parameters["BB_b"],
            )
            local_probabilities = local_probabilities / local_probabilities.sum()
            reservation_surface[y_index, x_index] = reservation_wage(
                wage_grid,
                local_probabilities,
                local_parameters["b"],
                local_parameters["beta"],
            )
    return (
        comparative_defaults,
        comparative_labels,
        reservation_surface,
        x_grid,
        x_parameter,
        y_grid,
        y_parameter,
    )


@app.cell(hide_code=True)
def _(
    comparative_defaults,
    comparative_labels,
    mo,
    plt,
    reservation_surface,
    x_grid,
    x_parameter,
    y_grid,
    y_parameter,
):
    heatmap_figure, heatmap_axis = plt.subplots(figsize=(10, 6))
    heatmap = heatmap_axis.pcolormesh(
        x_grid,
        y_grid,
        reservation_surface,
        shading="auto",
        cmap="viridis",
    )
    contour = heatmap_axis.contour(
        x_grid,
        y_grid,
        reservation_surface,
        levels=7,
        colors="white",
        linewidths=0.7,
        alpha=0.75,
    )
    heatmap_axis.clabel(contour, inline=True, fontsize=8, fmt="%.1f")
    colorbar = heatmap_figure.colorbar(heatmap, ax=heatmap_axis)
    colorbar.set_label("Reservation wage w*")
    heatmap_axis.set(
        title="Reservation-wage comparative statics",
        xlabel=comparative_labels[x_parameter],
        ylabel=comparative_labels[y_parameter],
    )
    heatmap_figure.tight_layout()

    held_fixed = [
        f"{comparative_labels[name]} = {value:g}"
        for name, value in comparative_defaults.items()
        if name not in (x_parameter, y_parameter)
    ]
    mo.vstack([
        heatmap_figure,
        mo.callout(
            "Held fixed: **" + "**  ·  **".join(held_fixed) + "**  ·  "
            f"Displayed $w^*$ range: **{reservation_surface.min():.2f}–{reservation_surface.max():.2f}**",
            kind="info",
        ),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5 · Unemployment duration simulation

    This experiment is independent of Sections 1–4 and resets the model to the original notebook defaults

    $T$ counts the wage-offer period in which the worker accepts, while $T-1$ counts completed periods of unemployment before acceptance
    """)
    return


@app.cell
def _(mo):
    duration_repetitions_input = mo.ui.number(
        start=100,
        stop=1_000_000,
        step=100,
        value=10_000,
        label="Number of simulation repetitions",
    )
    mo.vstack([
        mo.callout(
            "Fixed defaults: **b = 25**  ·  **β = 0.99**  ·  **n = 50**  ·  "
            "**BB_a = 200**  ·  **BB_b = 100**  ·  **wages = 10–60**",
            kind="info",
        ),
        duration_repetitions_input,
    ])
    return (duration_repetitions_input,)


@app.cell
def _(betabinom, duration_repetitions_input, np, reservation_wage):
    duration_default_b = 25.0
    duration_default_beta = 0.99
    duration_default_n = 50
    duration_default_BB_a = 200.0
    duration_default_BB_b = 100.0
    duration_default_wages = np.linspace(10.0, 60.0, duration_default_n + 1)
    duration_default_probabilities = betabinom.pmf(
        np.arange(duration_default_n + 1),
        duration_default_n,
        duration_default_BB_a,
        duration_default_BB_b,
    )
    duration_default_probabilities /= duration_default_probabilities.sum()

    duration_threshold = reservation_wage(
        duration_default_wages,
        duration_default_probabilities,
        duration_default_b,
        duration_default_beta,
    )
    duration_acceptance_probability = float(
        duration_default_probabilities[
            duration_default_wages >= duration_threshold
        ].sum()
    )
    duration_repetitions = int(duration_repetitions_input.value)
    duration_rng = np.random.default_rng(402)
    duration_stopping_times = duration_rng.geometric(
        duration_acceptance_probability,
        size=duration_repetitions,
    )
    duration_unemployment_periods = duration_stopping_times - 1

    duration_average_stop = float(duration_stopping_times.mean())
    duration_average_unemployment = float(duration_unemployment_periods.mean())
    duration_exact_stop = 1.0 / duration_acceptance_probability
    duration_exact_unemployment = duration_exact_stop - 1.0
    return (
        duration_acceptance_probability,
        duration_average_stop,
        duration_average_unemployment,
        duration_exact_stop,
        duration_exact_unemployment,
        duration_repetitions,
        duration_stopping_times,
        duration_threshold,
    )


@app.cell(hide_code=True)
def _(
    duration_acceptance_probability,
    duration_average_stop,
    duration_average_unemployment,
    duration_exact_stop,
    duration_exact_unemployment,
    duration_repetitions,
    duration_stopping_times,
    duration_threshold,
    mo,
    np,
    plt,
):
    duration_figure, duration_axis = plt.subplots(figsize=(10, 4.8))
    duration_display_limit = max(
        5,
        int(np.quantile(duration_stopping_times, 0.99)),
    )
    duration_bins = np.arange(0.5, duration_display_limit + 1.5, 1.0)
    duration_axis.hist(
        duration_stopping_times[duration_stopping_times <= duration_display_limit],
        bins=duration_bins,
        color="#0072B2",
        edgecolor="white",
        alpha=0.9,
    )
    duration_axis.axvline(
        duration_average_stop,
        color="#D55E00",
        linestyle="--",
        linewidth=2.5,
        label=f"Simulated mean T = {duration_average_stop:.2f}",
    )
    duration_axis.set(
        title=f"Stopping times across {duration_repetitions:,} simulated workers",
        xlabel="Periods until an offer is accepted, T",
        ylabel="Number of workers",
    )
    duration_axis.legend(frameon=True)
    duration_figure.tight_layout()

    mo.vstack([
        mo.hstack(
            [
                mo.callout(
                    f"Average unemployment duration, $T-1$\n\n"
                    f"**{duration_average_unemployment:.3f} periods**\n\n"
                    f"Exact benchmark: {duration_exact_unemployment:.3f}",
                    kind="success",
                ),
                mo.callout(
                    f"Average stopping time, $T$\n\n"
                    f"**{duration_average_stop:.3f} periods**\n\n"
                    f"Exact benchmark: {duration_exact_stop:.3f}",
                    kind="success",
                ),
            ],
            widths="equal",
            gap=2,
        ),
        duration_figure,
        mo.callout(
            f"Reservation threshold: **w* = {duration_threshold:.3f}**  ·  "
            f"Acceptance probability per offer: **{duration_acceptance_probability:.3%}**  ·  "
            "Simulation seed: **402**",
            kind="info",
        ),
    ])
    return


if __name__ == "__main__":
    app.run()
