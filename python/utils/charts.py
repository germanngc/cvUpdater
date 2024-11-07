import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def radar_chart(labels, values, plot_color=[0, 200, 200]):
    percentages = [f"{v}%" for v in values]

    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]
    percentages += percentages[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color=(plot_color[0]/255, plot_color[1]/255, plot_color[2]/255), alpha=0.3)
    ax.plot(angles, values, color=(plot_color[0]/255, plot_color[1]/255, plot_color[2]/255), linewidth=4)

    for angle, value, percentage in zip(angles, values, percentages):
        ax.text(angle, value * 0.7, percentage, ha='center', va='center', fontsize=16, color='black')

    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=18)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Save the radar chart
    radar_chart_path = f"utils/charts/radar_chart_{timestamp}.png"
    plt.savefig(radar_chart_path)
    plt.close(fig)

    return radar_chart_path