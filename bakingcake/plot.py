from matplotlib import pyplot as plt
import seaborn as sns


def plot_risk_reward(vol_df):
    """
        Plot risk (volatility) vs reward (return).

        Args:
            vol_df (pandas.DataFrame): volatility DataFrame

        Returns:
            risk vs reward plot
    """
    colors = sns.color_palette("husl", 8)
    # Initialize axis
    fig, ax = plt.subplots(1, 1)
    # Add ticker symbols to each scatter point
    for index, row in vol_df.iterrows(): 
        ax.scatter(
            row["mean"] * 100.0, row["return"] * 100.0, color=colors[index],
            s=50)
        ax.annotate(
            row["ticker"], (row["mean"] * 100.0, row["return"] * 100.0))
    # Format axis properly
    ax.grid(linestyle='--')
    ax.set_title("Risk vs Reward ({} to {})".format(
        str(vol_df["start"][0].date()),
        str(vol_df["end"][0].date())))
    ax.set_xlabel("Risk (Average Volatility Per Day in %)")
    ax.set_ylabel("Reward (Overall Return in %)")

    return fig


def plot_kpi_heatmap(adv_info, kpis, ascending=[]):
    """
        Plot a comparison heatmap of normalized key performance indicators.

        Args:
            adv_info (pandas.DataFrame): advanced stock information
            kpis (list): list of kpis
            ascending (list): list of boolean values dictating order

        Returns
            kpi comparison heatmap 
    """
    fig, ax = plt.subplots(1, 1)
    # Get kpis and normalize
    kpi_df = adv_info.loc[:, kpis]
    normalized_df = (kpi_df - kpi_df.min()) / (kpi_df.max() - kpi_df.min())
    # Add tickers
    normalized_df["ticker"] = adv_info["ticker"]
    # Flip columns where the values are ascending
    if len(ascending) == len(kpis):
        ascending_cols = [kpis[i] for i in range(len(kpis)) if ascending[i]]
        normalized_df.loc[
            :, ascending_cols] = 1.0 - normalized_df.loc[:, ascending_cols]
    # Plot on axis
    ax = sns.heatmap(
        normalized_df.set_index("ticker").T, cmap="RdYlGn", linewidths=.5)
    # Set title
    ax.set_title("KPI Comparison Heatmap")

    return fig
