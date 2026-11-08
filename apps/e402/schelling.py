# /// script
# requires-python = ">=3.11"
# dependencies = ["marimo>=0.24.0", "matplotlib>=3.8", "numpy>=2.0"]
# ///

"""Interactive Schelling model based on material/10_schelling.ipynb.

Run from the repository root with: uvx marimo run apps/e402/schelling.py
"""

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    return mo, np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <!-- # Schelling's segregation model -->
    This simple model shows that even a small **preference** for neighbors of similar race can lead to high levels of segregation.

    ## Set Up
    Suppose we have two types of people: orange people and green people. we will assume there are 250 of each type.

    These agents all live on a single unit square.

    The location of an agent is just a point $ (x, y) $,  where $ 0 < x < 1 $ and $ 0 < y < 1 $.


    ## Preferences
    An agent is happy if M (Minimum) of her N nearest neighbors are of the same type as her. Otherwise, she is unhappy.

    Nearest = 'Euclidean distance' in the unit square.

    ## Initialization
    These 500 agents are initially randomly mixed together: each agent independently and randomly draws a location from a bivariate uniform distribution S = (0,1) x (0,1).
    """)
    return


@app.cell
def _(mo):
    neighbors_input = mo.ui.slider(
        start=2, stop=20, step=1, value=10,
        label="Number of nearest neighbors", show_value=True,
    )
    return (neighbors_input,)


@app.cell
def _(mo, neighbors_input):
    required_input = mo.ui.slider(
        start=1, stop=neighbors_input.value, step=1,
        value=min(5, neighbors_input.value),
        label="Minimum same-type neighbors to stay", show_value=True,
    )
    return (required_input,)


@app.cell
def _(mo, neighbors_input, required_input):
    mo.hstack([neighbors_input, required_input], widths="equal", gap=2)
    return


@app.cell
def _(mo):
    seed_input = mo.ui.number(
        start=0, stop=999999, step=1, value=402,
        label="Random seed",
    )
    seed_input
    return (seed_input,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## How the model works
    At each round (time period), each agent can either stay or move to a random location in the unit square.

    An agent stays if the agent is happy. The algorith for moving is as follows:
    1. Draw a random location in $ S $
    1. If happy at new location, move there
    1. Else, go to step 1

    We cycle through all agents in one round, in a fixed order.

    We continue to cycle until no one wishes to move.
    """)
    return


@app.cell
def _(np):
    N_PER_TYPE = 250
    MAX_ROUNDS = 25

    def neighbor_count(positions, types, agent_index, num_neighbors, candidate=None):
        """Count same-type agents among the nearest other agents."""
        location = positions[agent_index] if candidate is None else candidate
        distances = np.sum((positions - location) ** 2, axis=1)
        distances[agent_index] = np.inf
        nearest = np.argpartition(distances, num_neighbors - 1)[:num_neighbors]
        return int(np.count_nonzero(types[nearest] == types[agent_index]))

    def summarize(positions, types, num_neighbors, required_same):
        counts = np.fromiter(
            (neighbor_count(positions, types, i, num_neighbors) for i in range(len(types))),
            dtype=int,
            count=len(types),
        )
        return int(np.count_nonzero(counts < required_same)), float(np.mean(counts / num_neighbors))

    def simulate(
        num_neighbors, required_same, seed, num_types=2,
        agent_counts=None, capture_agent_steps=False,
    ):
        rng = np.random.default_rng(seed)
        if agent_counts is None:
            total_agents = 2 * N_PER_TYPE
            counts = np.full(num_types, total_agents // num_types)
            counts[:total_agents % num_types] += 1
        else:
            counts = np.asarray(agent_counts, dtype=int)
        types = np.repeat(np.arange(num_types), counts)
        positions = rng.random((len(types), 2))
        snapshots = [positions.copy()]
        statistics = [summarize(positions, types, num_neighbors, required_same)]
        moves = [0]
        stop_message = None
        round_histories = []

        for _round in range(MAX_ROUNDS):
            round_start = positions.copy()
            agent_positions = np.empty_like(positions) if capture_agent_steps else None
            moved = 0
            for i in range(len(types)):
                if neighbor_count(positions, types, i, num_neighbors) < required_same:
                    # Match the source notebook: keep drawing until the agent is content.
                    for _draw in range(2000):
                        candidate = rng.random(2)
                        if neighbor_count(positions, types, i, num_neighbors, candidate) >= required_same:
                            positions[i] = candidate
                            moved += 1
                            break
                    else:
                        positions[:] = round_start
                        stop_message = (
                            f"Stopped during round {_round + 1}: an agent could not find "
                            "an acceptable location in 2,000 draws. Try a lower M "
                            "or another seed."
                        )
                        break
                if capture_agent_steps:
                    agent_positions[i] = positions[i]
            if stop_message is not None:
                break
            if capture_agent_steps:
                round_histories.append((round_start, agent_positions))
            snapshots.append(positions.copy())
            statistics.append(summarize(positions, types, num_neighbors, required_same))
            moves.append(moved)
            if moved == 0:
                break

        last_completed_round = len(snapshots) - 1
        # Keep the last completed state available at every remaining slider value.
        while len(snapshots) <= MAX_ROUNDS:
            snapshots.append(snapshots[-1].copy())
            statistics.append(statistics[-1])
            moves.append(0)

        return (
            types, snapshots, statistics, moves, stop_message,
            last_completed_round, round_histories,
        )

    return (simulate,)


@app.cell
def _(neighbors_input, required_input, seed_input, simulate):
    types, snapshots, statistics, moves, stop_message, last_completed_round, round_histories = simulate(
        neighbors_input.value, required_input.value, int(seed_input.value),
        capture_agent_steps=True,
    )
    return (
        last_completed_round,
        moves,
        round_histories,
        snapshots,
        statistics,
        stop_message,
        types,
    )


@app.cell
def _(mo, snapshots):
    round_slider = mo.ui.slider(
        start=0,
        stop=len(snapshots) - 1,
        step=1,
        value=0,
        label="Complete rounds, t",
        show_value=True,
        full_width=True,
    )

    round_slider
    # mo.vstack([round_slider, mo.md("At $t=0$, no agent has moved")])
    return (round_slider,)


@app.cell(hide_code=True)
def _(
    last_completed_round,
    mo,
    moves,
    plt,
    round_slider,
    snapshots,
    statistics,
    stop_message,
    types,
):
    t = round_slider.value
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.2), sharex=True, sharey=True)
    colors = ("#e68613", "#16845b")

    for ax, positions, title in zip(
        axes,
        (snapshots[0], snapshots[t]),
        ("Random start, t = 0", f"After {min(t, last_completed_round)} completed rounds"),
    ):
        for kind, color in ((0, colors[0]), (1, colors[1])):
            selected = types == kind
            ax.scatter(
                positions[selected, 0],
                positions[selected, 1],
                c=color,
                s=16,
                alpha=0.8,
                edgecolors="none",
            )
        ax.set(xlim=(0, 1), ylim=(0, 1), aspect="equal", title=title,
               xlabel="x position", ylabel="y position")
    fig.tight_layout()

    unhappy, same_share = statistics[t]
    status = "All agents are happy" if unhappy == 0 else f"{unhappy} agents are currently unhappy"
    equilibrium_round = (
        next((i for i in range(1, len(moves)) if moves[i] == 0), None)
        if stop_message is None else None
    )
    equilibrium_note = (
        f"**No movement from round {equilibrium_round} onward:** later slider positions show the same state"
        if equilibrium_round is not None and t >= equilibrium_round
        else stop_message or ""
    )
    mo.vstack([
        fig,
        mo.md(
            f"**Round {t}:** {moves[t]} moves during this round  \n"
            f"{status}  \n"
            f"Mean same-type share among nearest neighbors: "
            f"{same_share:.1%}"
        ),
        mo.md(equilibrium_note)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What is striking about the pictures is how rapidly racial integration breaks down.

    This is despite the fact that people in the model don’t actually mind living mixed with the other type.

    Even with these preferences, the outcome is a high degree of segregation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Watch agents move one by one

    This walkthrough uses the orange and green simulation above. Each row is
    one complete round, starting from the positions at the end of the previous
    round. Agents are visited in order: all 250 orange agents, then all 250
    green agents. Move the orange slider first. Once it reaches 250, the green
    slider advances through the green agents. The buttons beside either slider
    move one agent at a time. A ring marks the last agent
    visited, and an arrow shows its move, if it moved. A flat step means that
    agent was already happy and stayed put.
    """)
    return


@app.cell
def _(last_completed_round, mo):
    _round_count = max(1, last_completed_round)
    get_orange_steps, set_orange_steps = mo.state((0,) * _round_count)
    get_green_steps, set_green_steps = mo.state((0,) * _round_count)
    return get_green_steps, get_orange_steps, set_green_steps, set_orange_steps


@app.cell
def _(get_green_steps, get_orange_steps, mo, set_green_steps, set_orange_steps):
    orange_step_inputs = mo.ui.array([
        mo.ui.slider(
            start=0, stop=250, step=1, value=get_orange_steps()[i],
            label=f"Round {i + 1}: orange agents visited", show_value=True,
            on_change=lambda value, i=i: set_orange_steps(
                lambda old: old[:i] + (int(value),) + old[i + 1:]
            ),
        )
        for i in range(len(get_orange_steps()))
    ])
    green_step_inputs = mo.ui.array([
        mo.ui.slider(
            start=0, stop=250, step=1, value=get_green_steps()[i],
            label=f"Round {i + 1}: green agents visited", show_value=True,
            on_change=lambda value, i=i: set_green_steps(
                lambda old: old[:i] + (int(value),) + old[i + 1:]
            ),
        )
        for i in range(len(get_green_steps()))
    ])
    return green_step_inputs, orange_step_inputs


@app.cell
def _(last_completed_round, mo, set_green_steps, set_orange_steps):
    def _step(values, index, amount):
        updated = list(values)
        updated[index] = max(0, min(250, updated[index] + amount))
        return tuple(updated)

    orange_minus_buttons = mo.ui.array([
        mo.ui.button(
            label="−1", tooltip=f"Previous orange agent in round {i + 1}",
            on_click=lambda _value, i=i: set_orange_steps(
                lambda old: _step(old, i, -1)
            ),
        )
        for i in range(max(1, last_completed_round))
    ])
    orange_plus_buttons = mo.ui.array([
        mo.ui.button(
            label="+1", tooltip=f"Next orange agent in round {i + 1}",
            on_click=lambda _value, i=i: set_orange_steps(
                lambda old: _step(old, i, 1)
            ),
        )
        for i in range(max(1, last_completed_round))
    ])
    green_minus_buttons = mo.ui.array([
        mo.ui.button(
            label="−1", tooltip=f"Previous green agent in round {i + 1}",
            on_click=lambda _value, i=i: set_green_steps(
                lambda old: _step(old, i, -1)
            ),
        )
        for i in range(max(1, last_completed_round))
    ])
    green_plus_buttons = mo.ui.array([
        mo.ui.button(
            label="+1", tooltip=f"Next green agent in round {i + 1}",
            on_click=lambda _value, i=i: set_green_steps(
                lambda old: _step(old, i, 1)
            ),
        )
        for i in range(max(1, last_completed_round))
    ])
    return (
        green_minus_buttons, green_plus_buttons,
        orange_minus_buttons, orange_plus_buttons,
    )


@app.cell(hide_code=True)
def _(
    get_green_steps, get_orange_steps,
    green_minus_buttons, green_plus_buttons, green_step_inputs,
    mo, np, orange_minus_buttons, orange_plus_buttons, orange_step_inputs,
    plt, round_histories, stop_message,
):
    _rows = []
    _orange_values = get_orange_steps()
    _green_values = get_green_steps()

    for _round_index, (_start, _after_each_agent) in enumerate(round_histories):
        _orange_count = _orange_values[_round_index]
        _green_count = _green_values[_round_index] if _orange_count == 250 else 0
        _positions = _start.copy()
        _positions[:_orange_count] = _after_each_agent[:_orange_count]
        _positions[250:250 + _green_count] = _after_each_agent[250:250 + _green_count]

        _fig, _ax = plt.subplots(figsize=(5.2, 5.2))
        for _kind, _color in ((0, "#e68613"), (1, "#16845b")):
            _mask = np.arange(500) < 250 if _kind == 0 else np.arange(500) >= 250
            _ax.scatter(
                _positions[_mask, 0], _positions[_mask, 1],
                c=_color, s=17, alpha=0.8, edgecolors="none",
            )

        _current = (
            250 + _green_count - 1 if _green_count > 0
            else _orange_count - 1 if _orange_count > 0 else None
        )
        if _current is not None:
            _old = _start[_current]
            _new = _after_each_agent[_current]
            _ax.scatter([_new[0]], [_new[1]], s=125, facecolors="none",
                        edgecolors="black", linewidths=1.5, zorder=4)
            _did_move = not np.array_equal(_old, _new)
            if _did_move:
                _ax.annotate(
                    "", xy=_new, xytext=_old,
                    arrowprops={"arrowstyle": "->", "color": "black", "lw": 1.7},
                )
            _agent_type = "orange" if _current < 250 else "green"
            _agent_number = _current + 1 if _current < 250 else _current - 249
            _action = "moved" if _did_move else "stayed"
            _agent_note = f"Agent {_agent_number} ({_agent_type}) {_action}"
        else:
            _agent_note = "Start of round: no agent has been visited yet"

        _ax.set(
            xlim=(0, 1), ylim=(0, 1), aspect="equal",
            title=f"Round {_round_index + 1}", xlabel="x position", ylabel="y position",
        )
        _fig.tight_layout()
        _controls = mo.vstack([
            mo.hstack([
                orange_minus_buttons[_round_index],
                orange_step_inputs[_round_index],
                orange_plus_buttons[_round_index],
            ], widths=[0.2, 1, 0.2], align="center", gap=0.5),
            mo.hstack([
                green_minus_buttons[_round_index],
                green_step_inputs[_round_index],
                green_plus_buttons[_round_index],
            ], widths=[0.2, 1, 0.2], align="center", gap=0.5),
            mo.md(
                f"**{_agent_note}**  \n"
                f"Showing {_orange_count} orange and {_green_count} green updates"
            ),
            mo.md("Finish orange first to activate the green slider")
            if _orange_count < 250 else mo.md("Green agents are now visited in order"),
        ], gap=1)
        _rows.append(mo.hstack([_fig, _controls], widths=[1.15, 1], align="start", gap=2))

    _output = (
        mo.vstack(_rows, gap=2) if _rows
        else mo.md(stop_message or "No round has completed yet for these settings")
    )
    _output
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## More than two types

    Choose 2 to 10 types, then enter the number of agents in each type. The
    boxes begin blank and have no upper limit. Decimal entries are rounded to
    the nearest whole agent, with halves rounded up. This section has its own
    nearest neighbor count $N$, minimum same-type count $M$, and random seed.
    Each type has a distinct color. The slider again shows the initial state
    and every later round, including unchanged rounds after equilibrium.
    """)
    return


@app.cell
def _(mo):
    type_count_input = mo.ui.slider(
        start=2, stop=10, step=1, value=3,
        label="Number of types", show_value=True,
    )
    multi_neighbors_input = mo.ui.slider(
        start=2, stop=20, step=1, value=8,
        label="Nearest neighbors (N)", show_value=True,
    )
    multi_seed_input = mo.ui.number(
        start=0, stop=999999, step=1, value=403,
        label="Random seed for this section",
    )
    return multi_neighbors_input, multi_seed_input, type_count_input


@app.cell
def _(mo, multi_neighbors_input):
    multi_required_input = mo.ui.slider(
        start=1, stop=multi_neighbors_input.value, step=1,
        value=min(3, multi_neighbors_input.value),
        label="Minimum same-type neighbors (M)", show_value=True,
    )
    return (multi_required_input,)


@app.cell
def _(
    mo,
    multi_neighbors_input,
    multi_required_input,
    multi_seed_input,
    type_count_input,
):
    mo.vstack([
        mo.hstack([type_count_input, multi_seed_input], widths="equal", gap=2),
        mo.hstack([multi_neighbors_input, multi_required_input], widths="equal", gap=2),
    ])
    return


@app.cell
def _(mo, type_count_input):
    agent_count_inputs = mo.ui.array(
        [
            mo.ui.text(value="", placeholder="Enter a number", label=f"Type {i + 1}")
            for i in range(type_count_input.value)
        ],
        label="Number of agents in each type",
    )
    agent_count_inputs
    return (agent_count_inputs,)


@app.cell
def _(agent_count_inputs, mo, multi_neighbors_input):
    from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

    _raw_counts = agent_count_inputs.value
    mo.stop(
        any(not value.strip() for value in _raw_counts),
        mo.md("Enter a number for every type to show the simulation"),
    )
    try:
        multi_agent_counts = tuple(
            int(Decimal(value.strip()).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
            for value in _raw_counts
        )
    except (InvalidOperation, ValueError, OverflowError):
        mo.stop(True, mo.md("Enter a finite number in each box"))
    mo.stop(
        any(count < 1 for count in multi_agent_counts),
        mo.md("Each type needs at least one agent after rounding"),
    )
    mo.stop(
        sum(multi_agent_counts) <= multi_neighbors_input.value,
        mo.md("The total number of agents must exceed the number of nearest neighbors $N$"),
    )
    mo.md(
        "Using rounded counts: "
        + ", ".join(f"Type {i + 1}: {count}" for i, count in enumerate(multi_agent_counts))
    )
    return (multi_agent_counts,)


@app.cell
def _(
    multi_agent_counts,
    multi_neighbors_input,
    multi_required_input,
    multi_seed_input,
    simulate,
    type_count_input,
):
    (
        multi_types, multi_snapshots, multi_statistics, multi_moves,
        multi_stop_message, multi_last_completed_round, _multi_round_histories,
    ) = simulate(
        multi_neighbors_input.value,
        multi_required_input.value,
        int(multi_seed_input.value),
        num_types=type_count_input.value,
        agent_counts=multi_agent_counts,
    )
    return (
        multi_last_completed_round,
        multi_moves,
        multi_snapshots,
        multi_statistics,
        multi_stop_message,
        multi_types,
    )


@app.cell
def _(mo, multi_snapshots):
    multi_round_slider = mo.ui.slider(
        start=0, stop=len(multi_snapshots) - 1, step=1, value=0,
        label="Complete rounds, t", show_value=True, full_width=True,
    )
    multi_round_slider
    return (multi_round_slider,)


@app.cell(hide_code=True)
def _(
    mo,
    multi_last_completed_round,
    multi_moves,
    multi_round_slider,
    multi_snapshots,
    multi_statistics,
    multi_stop_message,
    multi_types,
    plt,
):
    _t = multi_round_slider.value
    _fig, _axes = plt.subplots(1, 2, figsize=(11, 5.2), sharex=True, sharey=True)
    _palette = plt.get_cmap("tab10")
    for _ax, _positions, _title in zip(
        _axes,
        (multi_snapshots[0], multi_snapshots[_t]),
        ("Random start, t = 0", f"After {min(_t, multi_last_completed_round)} completed rounds"),
    ):
        for _kind in range(int(multi_types.max()) + 1):
            _selected = multi_types == _kind
            _ax.scatter(
                _positions[_selected, 0], _positions[_selected, 1],
                color=_palette(_kind), s=16, alpha=0.8,
                edgecolors="none",
            )
        _ax.set(
            xlim=(0, 1), ylim=(0, 1), aspect="equal", title=_title,
            xlabel="x position", ylabel="y position",
        )
    _fig.tight_layout()

    _unhappy, _same_share = multi_statistics[_t]
    _equilibrium_round = (
        next((i for i in range(1, len(multi_moves)) if multi_moves[i] == 0), None)
        if multi_stop_message is None else None
    )
    _note = multi_stop_message or (
        f"No movement from round {_equilibrium_round} onward; later positions are unchanged"
        if _equilibrium_round is not None and _t >= _equilibrium_round else ""
    )
    mo.vstack([
        _fig,
        mo.md(
            f"**Round {_t}:** {multi_moves[_t]} moves · {_unhappy} unhappy agents · "
            f"Mean same-type share among nearest neighbors: {_same_share:.1%}"
        ),
        mo.md(_note),
    ])
    return


if __name__ == "__main__":
    app.run()
