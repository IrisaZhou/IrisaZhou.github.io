"""Interactive illustrations of the bisection and Newton–Raphson methods.

Run from the workspace root with:

    .venv/bin/marimo run Topics/02-Growth/Numerical_Functions_Illustrations.py
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="full")


@app.cell
def _():
    import ast
    import matplotlib.pyplot as plt
    import marimo as mo
    import numpy as np

    def make_expression(expression):
        allowed_functions = {"abs", "cos", "exp", "log", "sin", "sqrt", "tan"}
        allowed_constants = {"pi"}

        class SafeExpression(ast.NodeVisitor):
            def visit_Expression(self, node): self.visit(node.body)
            def visit_BinOp(self, node):
                if not isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow)):
                    raise ValueError("Use only +, -, *, /, and ** operators")
                self.visit(node.left); self.visit(node.right)
            def visit_UnaryOp(self, node):
                if not isinstance(node.op, (ast.UAdd, ast.USub)):
                    raise ValueError("Use only unary + and - operators")
                self.visit(node.operand)
            def visit_Name(self, node):
                if node.id not in {"x", "np"}: raise ValueError("The expression may use only x and np")
            def visit_Constant(self, node):
                if not isinstance(node.value, (int, float)): raise ValueError("Use numeric constants only")
            def visit_Attribute(self, node):
                if not isinstance(node.value, ast.Name) or node.value.id != "np":
                    raise ValueError("Use NumPy functions as np.function(x)")
                if node.attr not in allowed_functions | allowed_constants:
                    raise ValueError("Allowed NumPy names: " + ", ".join(sorted(allowed_functions | allowed_constants)))
            def visit_Call(self, node):
                if not isinstance(node.func, ast.Attribute) or node.keywords:
                    raise ValueError("Use NumPy functions such as np.sin(x), without keyword arguments")
                self.visit(node.func)
                for argument in node.args: self.visit(argument)
            def generic_visit(self, node):
                raise ValueError(f"Unsupported expression element: {type(node).__name__}")

        tree = ast.parse(expression, mode="eval")
        SafeExpression().visit(tree)
        compiled = compile(tree, "<function input>", "eval")
        return lambda x: eval(compiled, {"__builtins__": {}, "np": np}, {"x": x})

    return make_expression, mo, np, plt


@app.cell
def _(mo):
    mo.md(r"""
    # Numerical functions illustrations

    ## Bisection method

    Bisection starts with an interval whose endpoint values have opposite signs. It evaluates the midpoint, then keeps the half that still contains a sign change. Drag the step control: earlier midpoint evaluations are blue and the current midpoint is orange.
    """)
    return


@app.cell
def _(mo):
    function_input = mo.ui.text(value="np.sin(4 * (x - 1/4)) + x + x**20 - 1", label="Function f(x)", full_width=True)
    left_endpoint = mo.ui.number(value=0, step=0.1, label="Left endpoint a")
    right_endpoint = mo.ui.number(value=1, step=0.1, label="Right endpoint b")
    bisection_step_slider = mo.ui.slider(start=1, stop=24, step=1, value=1, label="Bisection step", show_value=True, full_width=True)
    mo.vstack([function_input, mo.hstack([left_endpoint, right_endpoint], widths="equal"), bisection_step_slider], gap=1)
    return bisection_step_slider, function_input, left_endpoint, right_endpoint


@app.cell
def _(function_input, make_expression):
    function_error = None
    try:
        f = make_expression(function_input.value)
    except (SyntaxError, TypeError, ValueError, OverflowError) as error:
        f = None
        function_error = str(error)
    return f, function_error


@app.cell
def _(f, function_error, left_endpoint, np, right_endpoint):
    bisection_error, bisection_records = function_error, []
    if bisection_error is None:
        try:
            a, b = float(left_endpoint.value), float(right_endpoint.value)
            if not np.isfinite(a) or not np.isfinite(b) or a >= b: raise ValueError("The left endpoint must be smaller than the right endpoint")
            fa, fb = float(f(a)), float(f(b))
            if not np.isfinite(fa) or not np.isfinite(fb): raise ValueError("The function must be finite at both endpoints")
            if fa == 0 or fb == 0 or np.sign(fa) == np.sign(fb): raise ValueError("f(a) and f(b) must be nonzero and have opposite signs")
            for iteration in range(1, 25):
                midpoint = (a + b) / 2
                f_midpoint = float(f(midpoint))
                if not np.isfinite(f_midpoint): raise ValueError("The function became non-finite inside the interval")
                bisection_records.append({"iteration": iteration, "left": a, "right": b, "f_left": fa, "midpoint": midpoint, "f_midpoint": f_midpoint})
                if f_midpoint == 0: break
                if np.sign(fa) != np.sign(f_midpoint): b, fb = midpoint, f_midpoint
                else: a, fa = midpoint, f_midpoint
        except (TypeError, ValueError, OverflowError, FloatingPointError) as error:
            bisection_error, bisection_records = str(error), []
    return bisection_error, bisection_records


@app.cell
def _(bisection_error, bisection_records, mo):
    if bisection_error:
        _notice = mo.callout(mo.md(f"**Choose a valid bisection problem:** {bisection_error}"), kind="danger")
    elif len(bisection_records) < 24:
        _notice = mo.callout(mo.md("**An exact root was reached.** There are no later bisection steps."), kind="success")
    else:
        _notice = mo.md("")
    _notice
    return


@app.cell
def _(
    bisection_error,
    bisection_records,
    bisection_step_slider,
    f,
    mo,
    np,
    plt,
):
    if bisection_error is None:
        shown_bisection_step = min(bisection_step_slider.value, len(bisection_records))
        current_bisection = bisection_records[shown_bisection_step - 1]
        previous_midpoints = [row["midpoint"] for row in bisection_records[:shown_bisection_step - 1]]
        plot_a, plot_b = bisection_records[0]["left"], bisection_records[0]["right"]
        padding = max((plot_b - plot_a) * 0.12, 0.05)
        bisection_grid = np.linspace(plot_a - padding, plot_b + padding, 800)
        with np.errstate(all="ignore"): bisection_values = np.asarray(f(bisection_grid), dtype=float)
        bisection_figure, (function_axis, interval_axis) = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={"height_ratios": [3, 1]}, sharex=True)
        function_axis.plot(bisection_grid, bisection_values, color="#263238", linewidth=2.3, label="f(x)")
        function_axis.axhline(0, color="#455a64", linestyle="--", linewidth=1.2)
        function_axis.axvspan(current_bisection["left"], current_bisection["right"], color="#90caf9", alpha=0.22, label="Current interval")
        function_axis.axvline(current_bisection["left"], color="#c62828", linestyle=":")
        function_axis.axvline(current_bisection["right"], color="#2e7d32", linestyle=":")
        if previous_midpoints:
            function_axis.scatter(previous_midpoints, [float(f(x)) for x in previous_midpoints], color="#1976d2", s=58, zorder=5, label="Earlier midpoints")
        function_axis.scatter([current_bisection["midpoint"]], [current_bisection["f_midpoint"]], color="#f57c00", edgecolor="white", linewidth=1.2, s=110, zorder=6, label="Current midpoint")
        function_axis.set_ylabel("f(x)"); function_axis.set_title("Bisection repeatedly halves a sign-changing interval"); function_axis.grid(alpha=0.22); function_axis.legend(loc="best")
        interval_axis.axhline(0, color="#455a64", linewidth=1)
        interval_axis.plot([current_bisection["left"], current_bisection["right"]], [0, 0], color="#90caf9", linewidth=12, solid_capstyle="butt")
        interval_axis.scatter([current_bisection["left"], current_bisection["right"]], [0, 0], color=["#c62828", "#2e7d32"], s=75, zorder=4)
        if previous_midpoints: interval_axis.scatter(previous_midpoints, [0] * len(previous_midpoints), color="#1976d2", s=52, zorder=5)
        interval_axis.scatter([current_bisection["midpoint"]], [0], color="#f57c00", edgecolor="white", linewidth=1.2, s=110, zorder=6)
        interval_axis.set_yticks([]); interval_axis.set_xlabel("x"); interval_axis.set_title("Current interval and midpoint history", loc="left", fontsize=11); interval_axis.grid(axis="x", alpha=0.22)
        bisection_figure.tight_layout()
        retained_side = "left half" if np.sign(current_bisection["f_left"]) != np.sign(current_bisection["f_midpoint"]) else "right half"
        _result = mo.vstack([mo.md(f"""**Step {shown_bisection_step} of {len(bisection_records)}**

    Current interval: `[{current_bisection['left']:.8f}, {current_bisection['right']:.8f}]`

    Midpoint: `x = {current_bisection['midpoint']:.8f}` and `f(x) = {current_bisection['f_midpoint']:.8f}`

    The sign change is in the **{retained_side}**"""), bisection_figure])
    else:
        _result = mo.md("Fix the function or endpoints above to display bisection steps")
    _result
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Newton–Raphson method

    Newton–Raphson follows the tangent line at the current guess. It computes `x_(k+1) = x_k - f(x_k) / f'(x_k)`. It can converge much faster than bisection, but it needs a derivative and does not keep a root bracketed.
    """)
    return


@app.cell
def _(mo):
    derivative_input = mo.ui.text(value="4 * np.cos(4 * (x - 1/4)) + 1 + 20 * x**19", label="Derivative f'(x)", full_width=True)
    initial_guess = mo.ui.number(value=0.5, step=0.1, label="Initial guess x_0")
    newton_step_slider = mo.ui.slider(start=0, stop=12, step=1, value=0, label="Newton–Raphson step", show_value=True, full_width=True)
    mo.vstack([derivative_input, initial_guess, newton_step_slider], gap=1)
    return derivative_input, initial_guess, newton_step_slider


@app.cell
def _(derivative_input, make_expression):
    derivative_error = None
    try:
        fprime = make_expression(derivative_input.value)
    except (SyntaxError, TypeError, ValueError, OverflowError) as error:
        fprime, derivative_error = None, str(error)
    return derivative_error, fprime


@app.cell
def _(derivative_error, f, fprime, function_error, initial_guess, np):
    newton_error, newton_records = function_error or derivative_error, []
    if newton_error is None:
        try:
            newton_x = float(initial_guess.value)
            if not np.isfinite(newton_x): raise ValueError("The initial guess must be finite")
            for newton_step in range(13):
                with np.errstate(all="ignore"):
                    newton_value, newton_slope = float(f(newton_x)), float(fprime(newton_x))
                if not np.isfinite(newton_value) or not np.isfinite(newton_slope): raise ValueError("The function or derivative became non-finite")
                next_newton_x = None
                if abs(newton_value) > 1e-12:
                    if abs(newton_slope) < 1e-12: raise ValueError("The derivative is too close to zero for a Newton step")
                    next_newton_x = newton_x - newton_value / newton_slope
                    if not np.isfinite(next_newton_x): raise ValueError("The next Newton iterate is not finite")
                newton_records.append({"step": newton_step, "x": newton_x, "value": newton_value, "slope": newton_slope, "next_x": next_newton_x})
                if next_newton_x is None: break
                newton_x = next_newton_x
        except (TypeError, ValueError, OverflowError, FloatingPointError) as error:
            newton_error, newton_records = str(error), []
    return newton_error, newton_records


@app.cell
def _(f, mo, newton_error, newton_records, newton_step_slider, np, plt):
    if newton_error is None:
        shown_newton_step = min(newton_step_slider.value, len(newton_records) - 1)
        current_newton = newton_records[shown_newton_step]
        earlier_newton_points = [row["x"] for row in newton_records[:shown_newton_step]]
        all_newton_points = np.asarray([row["x"] for row in newton_records])
        newton_centre = (np.min(all_newton_points) + np.max(all_newton_points)) / 2
        newton_half_width = max((np.max(all_newton_points) - np.min(all_newton_points)) * 0.7, 0.55)
        newton_grid = np.linspace(newton_centre - newton_half_width, newton_centre + newton_half_width, 800)
        with np.errstate(all="ignore"): newton_values = np.asarray(f(newton_grid), dtype=float)
        newton_figure, newton_axis = plt.subplots(figsize=(10, 5.6))
        newton_axis.plot(newton_grid, newton_values, color="#263238", linewidth=2.3, label="f(x)")
        newton_axis.axhline(0, color="#455a64", linestyle="--", linewidth=1.2)
        if earlier_newton_points:
            newton_axis.scatter(earlier_newton_points, [float(f(x)) for x in earlier_newton_points], color="#1976d2", s=60, zorder=5, label="Earlier guesses")
        if current_newton["next_x"] is not None:
            tangent_x = np.linspace(min(current_newton["x"], current_newton["next_x"]), max(current_newton["x"], current_newton["next_x"]), 100)
            tangent_y = current_newton["value"] + current_newton["slope"] * (tangent_x - current_newton["x"])
            newton_axis.plot(tangent_x, tangent_y, color="#7b1fa2", linestyle="--", linewidth=1.8, label="Tangent line")
            newton_axis.scatter([current_newton["next_x"]], [0], color="#7b1fa2", marker="x", s=85, zorder=5, label="Tangent intercept")
        newton_axis.scatter([current_newton["x"]], [current_newton["value"]], color="#f57c00", edgecolor="white", linewidth=1.2, s=125, zorder=6, label="Current guess")
        newton_axis.axvline(current_newton["x"], color="#f57c00", linestyle=":", linewidth=1.3)
        newton_axis.set_title("Newton–Raphson follows the tangent to its horizontal-axis intercept")
        newton_axis.set_xlabel("x"); newton_axis.set_ylabel("f(x)"); newton_axis.grid(alpha=0.22); newton_axis.legend(loc="best")
        newton_figure.tight_layout()
        if current_newton["next_x"] is None: next_newton_text = "The current value is already an approximate root"
        else: next_newton_text = f"The tangent intercept gives `x_{shown_newton_step + 1} = {current_newton['next_x']:.8f}`"
        _result = mo.vstack([mo.md(f"""**Step {shown_newton_step} of {len(newton_records) - 1}**

    Current guess: `x_{shown_newton_step} = {current_newton['x']:.8f}`

    `f(x_{shown_newton_step}) = {current_newton['value']:.8f}` and `f'(x_{shown_newton_step}) = {current_newton['slope']:.8f}`

    {next_newton_text}"""), newton_figure])
    else:
        _result = mo.md("Fix the function, derivative, or initial guess above to display Newton–Raphson steps")
    _result
    return


if __name__ == "__main__":
    app.run()
