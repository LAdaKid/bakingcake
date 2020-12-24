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
