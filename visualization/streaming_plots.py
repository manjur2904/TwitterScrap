import matplotlib.pyplot as plt
import numpy as np

def streaming_plot(signal):
    plt.plot(np.cumsum(signal)/np.arrange(1, len(signal)+1))
    plt.title("Aggregated Market Signal")
    plt.show()