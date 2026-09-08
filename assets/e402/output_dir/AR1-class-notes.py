# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo>=0.15.0",
#     "matplotlib>=3.8.0",
#     "numpy>=2.0.0",
#     "pandas>=2.2.0",
#     "statsmodels>=0.14.0",
# ]
# ///

import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # Forecasting with AR and MA Models

    We first use a simulation to build intuition for persistence and mean
    reversion. We then apply the four steps from the **Estimating an AR(1)**
    slide to annual GDP growth.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note: This notebook is in **Marimo** format. Variables beginning with an
    underscore are local to their cell and are not saved in the notebook's
    namespace.
    """)
    return


@app.cell
def _():
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from statsmodels.graphics.tsaplots import plot_acf
    from statsmodels.tsa.stattools import adfuller

    plt.style.use("seaborn-v0_8-whitegrid")
    return adfuller, np, pd, plot_acf, plt


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. AR and MA models: persistence and mean reversion

    The first-order autoregressive model is the special case $p=1$ of

    $$
    Y_t = c + \sum_{j=1}^{p}\frac{\phi}{p}Y_{t-j} + \varepsilon_t,
    \qquad E(\varepsilon_t\mid\mathcal I_{t-1})=0.
    $$

    Set $p=1$ to recover the usual AR(1). The lag control below illustrates
    an AR($p$) extension in which the total lag weight remains $\phi$.
    When $|\phi|<1$, its long-run mean is $\mu=c/(1-\phi)$.
    """)
    return


@app.cell
def _(mo):
    phi_slider = mo.ui.slider(
        start=-1.5, stop=1.50, step=0.05, value=0.75,
        label=r"Persistence $\phi$", show_value=True,
    )
    ar_lags_slider = mo.ui.slider(
        start=1, stop=5, step=1, value=1,
        label=r"Number of lags of $Y_t$ ($p$)", show_value=True,
    )
    mo.hstack([phi_slider, ar_lags_slider])
    return ar_lags_slider, phi_slider


@app.cell
def _(ar_lags_slider, np, phi_slider, plt):
    _rng = np.random.default_rng(402)
    _periods = 120
    _burn_in = 100
    _c = 0.5
    _phi = phi_slider.value
    _p = ar_lags_slider.value
    _simulated = np.empty(_periods + _burn_in + _p)
    _simulated[:_p] = _c / (1 - _phi)
    _shocks = _rng.normal(0, 1, size=_periods + _burn_in)
    for _t in range(_p, len(_simulated)):
        _simulated[_t] = _c + (_phi / _p) * _simulated[_t - _p:_t].sum() + _shocks[_t - _p]

    _sample = _simulated[_burn_in + _p:]
    _mean = _c / (1 - _phi)
    _fig, _ax = plt.subplots(figsize=(10, 3.6))
    _ax.plot(_sample, color="#006298", linewidth=1.4)
    _ax.axhline(_mean, color="#990000", linestyle="--", label=f"Long-run mean = {_mean:.2f}")
    _ax.set(title=f"Simulated AR({_p}), phi = {_phi:.2f}", xlabel="Period", ylabel="$Y_t$")
    _ax.legend()
    _fig.tight_layout()
    _fig
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(
            "Move the sliders. Set $p=1$ for the usual AR(1); larger values "
            "include additional lags of $Y_t$. Positive values produce "
            "persistence, while negative values produce alternating movements."
        ),
        kind="info",
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### MA(1): temporary effects of an innovation

    A moving-average model expresses $Y_t$ as a function of current and past
    innovations:

    $$
    Y_t = \mu + \varepsilon_t + \theta\sum_{j=1}^{q}\varepsilon_{t-j}.
    $$

    Set $q=1$ to obtain the standard MA(1). Unlike an AR model, the effect of
    a shock disappears after the selected number of innovation lags.
    """)
    return


@app.cell
def _(mo):
    theta_slider = mo.ui.slider(
        start=-1.5, stop=1.5, step=0.05, value=0.75,
        label=r"Innovation coefficient $\theta$", show_value=True,
    )
    ma_lags_slider = mo.ui.slider(
        start=1, stop=5, step=1, value=1,
        label=r"Number of lags of $\varepsilon_t$ ($q$)", show_value=True,
    )
    mo.hstack([theta_slider, ma_lags_slider])
    return ma_lags_slider, theta_slider


@app.cell
def _(ma_lags_slider, np, plt, theta_slider):
    _rng = np.random.default_rng(402)
    _periods = 120
    _burn_in = 10
    _mu = 0.0
    _theta = theta_slider.value
    _q = ma_lags_slider.value
    _shocks = _rng.normal(0, 1, size=_periods + _burn_in + _q)
    _simulated = np.empty(_periods + _burn_in)
    for _t in range(_periods + _burn_in):
        _simulated[_t] = _mu + _shocks[_t + _q] + _theta * _shocks[_t:_t + _q].sum()

    _sample = _simulated[_burn_in:]
    _fig, _ax = plt.subplots(figsize=(10, 3.6))
    _ax.plot(_sample, color="#006298", linewidth=1.4)
    _ax.axhline(_mu, color="#990000", linestyle="--", label=f"Mean = {_mu:.2f}")
    _ax.set(title=f"Simulated MA({_q}), theta = {_theta:.2f}", xlabel="Period", ylabel="$Y_t$")
    _ax.legend()
    _fig.tight_layout()
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 2. GDP levels versus annual GDP growth

    We use the annual `FYGDP` series in `FYGDP.csv`. The GDP level trends over
    time, so we study its annual log growth rate:

    $$
    y_t = 100\,[\log(FYGDP_t)-\log(FYGDP_{t-1})].
    $$
    """)
    return


@app.cell
def _(mo, pd):
    data_path = mo.notebook_location() / "public" / "FYGDP.csv"
    gdp = pd.read_csv(str(data_path), parse_dates=["observation_date"])
    gdp = gdp.rename(columns={"observation_date": "date"}).sort_values("date")
    gdp = gdp.reset_index(drop=True)
    gdp
    return (gdp,)


@app.cell
def _(gdp, np, plt):
    gdp_analysis = gdp.assign(y=100 * np.log(gdp["FYGDP"]).diff())

    _fig, (_ax1, _ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    _ax1.plot(gdp_analysis["date"], gdp_analysis["FYGDP"], color="#006298")
    _ax1.set(title="Annual GDP level", ylabel="FYGDP")
    _ax2.axhline(0, color="black", linewidth=0.8)
    _ax2.plot(gdp_analysis["date"], gdp_analysis["y"], color="#990000", linewidth=1.1)
    _ax2.set(title="Annual GDP growth", ylabel="Percent per year", xlabel="Year")
    _fig.tight_layout()
    _fig
    return (gdp_analysis,)


@app.cell
def _(mo):
    mo.md(r"""
    ### Estimate AR(1)
    """)
    return


@app.cell
def _(gdp_analysis):
    # Step 1: Create the lagged variable y_{t-1}.
    ar1_data_with_lag = gdp_analysis.assign(y_lag=gdp_analysis["y"].shift(1))
    return (ar1_data_with_lag,)


@app.cell
def _(ar1_data_with_lag):
    # Step 2: Align each current observation y_t with its lag y_{t-1}.
    ar1_data = ar1_data_with_lag[["date", "y", "y_lag"]].dropna().reset_index(drop=True)
    ar1_data
    return (ar1_data,)


@app.cell
def _(ar1_data, np, pd):
    # Step 3: Estimate c and phi by regressing y_t on a constant and y_{t-1}.
    X = np.column_stack((np.ones(len(ar1_data)), ar1_data["y_lag"]))
    y = ar1_data["y"].to_numpy()
    c_hat, phi_hat = np.linalg.lstsq(X, y, rcond=None)[0]
    ar1_results = pd.DataFrame(
        {"estimate": [c_hat, phi_hat, c_hat / (1 - phi_hat)]},
        index=["intercept c", "persistence phi", "implied mean c/(1-phi)"],
    )
    ar1_results
    return c_hat, phi_hat


@app.cell
def _(c_hat, mo, phi_hat):
    stationarity_text = "meets" if abs(phi_hat) < 1 else "does not meet"
    inequality = "<" if abs(phi_hat) < 1 else "\\geq"
    mo.md(
        rf"""
        The estimated model is

        $$
        y_t = {c_hat:.3f} + {phi_hat:.3f}y_{{t-1}} + \widehat{{\varepsilon}}_t.
        $$

        The estimate $\hat\phi={phi_hat:.3f}$ measures the predictive association
        between last year's GDP growth and this year's GDP growth. Since
        $|\hat\phi|{inequality}1$, the fitted AR(1) {stationarity_text} the usual
        stationarity condition.
        """
    )
    return


@app.cell
def _(ar1_data, c_hat, mo, phi_hat):
    # Step 4: Use the final observed y_T as the forecast origin.
    y_T = float(ar1_data["y"].iloc[-1])
    y_forecast = c_hat + phi_hat * y_T
    mo.md(
        rf"""
        The final observed value is $y_T={y_T:.3f}$. Therefore the one-year-ahead
        forecast is

        $$
        \widehat{{y}}_{{T+1\mid T}} = \hat c + \hat\phi y_T
        = {c_hat:.3f} + ({phi_hat:.3f})({y_T:.3f})
        = {y_forecast:.3f}\ \text{{percent}}.
        $$
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Step 5. Perform an augmented Dickey–Fuller (ADF) test

    The ADF test helps us assess whether the growth series behaves as if it has
    a unit root. A unit root means shocks may have permanent effects, which is
    inconsistent with the usual stationary AR(1) interpretation.

    The null hypothesis is that the series has a unit root. A small p-value is
    evidence against the null; a large p-value means that we do not have enough
    evidence to reject it. A large p-value is not proof that a unit root exists.

    We include a constant but no deterministic trend because this test is for
    the annual growth rate, not the trending GDP level. The result depends on
    the deterministic terms, lag selection, sample period, structural breaks,
    and data vintage, so use it together with the plot and the ACF.
    """)
    return


@app.cell
def _(adfuller, gdp_analysis, pd):

    _statistic, _p_value, _used_lags, _nobs, *_ = adfuller(
        gdp_analysis["y"].dropna(), regression="c", autolag="AIC", result_object=False
    )
    adf_results = pd.DataFrame(
        {"result": [_statistic, _p_value, _used_lags, _nobs]},
        index=["ADF statistic", "p-value", "lags used", "observations"],
    )
    adf_results
    return


@app.cell
def _(gdp_analysis, mo, plot_acf, plt):
    mo.md(r"""
    ## Final diagnostic: the annual GDP-growth ACF

    The lag-$k$ autocorrelation compares $y_t$ with $y_{t-k}$. Each bar is the
    sample correlation between annual GDP growth and growth $k$ years earlier.
    A bar outside the shaded bands is evidence that the correlation at that lag
    differs from zero in this sample. For a stationary AR(1), the population
    autocorrelation is $\rho_k=\phi^k$, so the ACF often decays toward zero. The
    ACF is descriptive evidence, not proof that an AR(1) is the correct model.
    """)
    _fig, _ax = plt.subplots(figsize=(10, 4))
    plot_acf(gdp_analysis["y"].dropna(), lags=20, zero=False, ax=_ax, color="#990000")
    _ax.set(title="ACF: annual GDP growth", xlabel="Lag (years)", ylabel="Sample autocorrelation")
    _fig.tight_layout()
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Conclusion

    We estimated an AR(1) for annual GDP growth, checked the growth series with
    an ADF test, and inspected its autocorrelation pattern.
    """)
    return


if __name__ == "__main__":
    app.run()
