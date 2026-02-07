"""Plotting helpers for streaming/interactive visualizations.

This module provides a minimal plotting function used by the demo pipeline.
It produces a simple aggregated signal plot. `plt.show()` is used which may
block depending on the matplotlib backend; that is acceptable for a demo.
"""

import matplotlib.pyplot as plt
import numpy as np


def streaming_plot(signal):
    """Render a running-average aggregated signal plot.

    Args:
        signal (array-like): 1D numeric sequence representing the signal.
    """
    plt.plot(np.cumsum(signal) / np.arange(1, len(signal) + 1))
    plt.title("Aggregated Market Signal")
    plt.xlabel("Feature index (aggregated)")
    plt.ylabel("Mean activation")
    plt.grid(True)
    plt.show()