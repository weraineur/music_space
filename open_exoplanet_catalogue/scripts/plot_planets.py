from pathlib import Path
import math

import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
INPUT_CSV = BASE_DIR / "planets.csv"
OUTPUT_PNG = BASE_DIR / "planets_positions.png"


def parse_right_ascension(value):
    if pd.isna(value):
        return None

    parts = str(value).replace(":", " ").split()
    if len(parts) < 3:
        return None

    hours = float(parts[0])
    minutes = float(parts[1])
    seconds = float(parts[2])

    return 15.0 * (hours + minutes / 60.0 + seconds / 3600.0)


def parse_declination(value):
    if pd.isna(value):
        return None

    parts = str(value).replace(":", " ").split()
    if len(parts) < 3:
        return None

    degrees_text = parts[0]
    sign = -1.0 if degrees_text.startswith("-") else 1.0

    degrees = abs(float(degrees_text))
    minutes = float(parts[1])
    seconds = float(parts[2])

    return sign * (degrees + minutes / 60.0 + seconds / 3600.0)


def build_positions(dataframe):
    positions = dataframe.copy()
    positions["distance"] = pd.to_numeric(positions["distance"], errors="coerce")
    positions["ra_deg"] = positions["ascension_droite"].apply(parse_right_ascension)
    positions["dec_deg"] = positions["declinaison"].apply(parse_declination)
    positions["masse"] = pd.to_numeric(positions["masse"], errors="coerce")
    positions["temperature"] = pd.to_numeric(positions["temperature"], errors="coerce")

    positions = positions.dropna(subset=["distance", "ra_deg", "dec_deg"]).copy()

    ra_rad = positions["ra_deg"].apply(math.radians)
    dec_rad = positions["dec_deg"].apply(math.radians)

    positions["x"] = positions["distance"] * dec_rad.apply(math.cos) * ra_rad.apply(math.cos)
    positions["y"] = positions["distance"] * dec_rad.apply(math.cos) * ra_rad.apply(math.sin)
    positions["z"] = positions["distance"] * dec_rad.apply(math.sin)

    return positions


def marker_sizes(series):
    filled = series.fillna(series.median())
    if filled.isna().all():
        return [18] * len(series)

    clipped = filled.clip(lower=filled.quantile(0.1), upper=filled.quantile(0.9))
    minimum = clipped.min()
    maximum = clipped.max()

    if minimum == maximum:
        return [22] * len(series)

    normalized = (clipped - minimum) / (maximum - minimum)
    return 12 + normalized * 48


def plot_positions(positions):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)
    fig.suptitle("Position des exoplanetes par rapport au Soleil", fontsize=16)

    scatter_kwargs = {
        "c": positions["temperature"],
        "cmap": "plasma",
        "s": marker_sizes(positions["masse"]),
        "alpha": 0.75,
        "edgecolors": "none",
    }

    axes[0].scatter(positions["x"], positions["y"], **scatter_kwargs)
    axes[0].scatter([0], [0], color="gold", s=140, marker="*", label="Soleil")
    axes[0].set_title("Vue XY")
    axes[0].set_xlabel("x (parsecs)")
    axes[0].set_ylabel("y (parsecs)")
    axes[0].legend(loc="upper right")
    axes[0].grid(alpha=0.25)

    scatter = axes[1].scatter(positions["x"], positions["z"], **scatter_kwargs)
    axes[1].scatter([0], [0], color="gold", s=140, marker="*", label="Soleil")
    axes[1].set_title("Vue XZ")
    axes[1].set_xlabel("x (parsecs)")
    axes[1].set_ylabel("z (parsecs)")
    axes[1].legend(loc="upper right")
    axes[1].grid(alpha=0.25)

    colorbar = fig.colorbar(scatter, ax=axes, shrink=0.92)
    colorbar.set_label("Temperature de la planete (K)")

    fig.savefig(OUTPUT_PNG, dpi=200, bbox_inches="tight")
    plt.show()


def main():
    planets = pd.read_csv(INPUT_CSV)
    positions = build_positions(planets)
    plot_positions(positions)
    print(f"Image creee : {OUTPUT_PNG}")
    print(f"Planetes affichees : {len(positions)}")


if __name__ == "__main__":
    main()
