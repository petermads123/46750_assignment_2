"""Model 2 main script."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
from tqdm import tqdm

from assignment_2.model2 import DataModel, IntertemporalExpansionModel

model = IntertemporalExpansionModel()
data = DataModel()
data.jonas()
model.define_model(data=data, discount_factor=0.05)
model.optimize()
results, obj_val = model.get_results()
print(results)
print("Objective value:", obj_val)
model.plot_results(scale_factor=365 * 24)


scales = np.arange(0, 2, 0.01)
capacities: dict[str, list[float]] = {}
for conv_factor in tqdm(scales):
    data.jonas_max_capacity_change(conv_max_factor=float(conv_factor))
    model.define_model(data=data, discount_factor=0.05)
    model.optimize()
    results, obj_val = model.get_results()
    for gen in model.gen_names:
        if gen not in capacities:
            capacities[gen] = []
        capacities[gen].append(
            results["capacities"][gen][-1] / (365 * 24)
        )  # final time step

fig, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)

# Use a consistent, colorblind-friendly palette; fall back to model.colors if present
gen_order = sorted(
    capacities.keys(),
    key=lambda g: capacities[g][-1] if capacities[g] else 0,
    reverse=True,
)

for gen in gen_order:
    ax.plot(scales, capacities[gen], label=gen, color=model.colors[gen], linewidth=2.2)

ax.set_title("Generator capacities vs. conventional capacity scaling", pad=10)
ax.set_xlabel("Max conventional capacity scaling factor")
ax.set_ylabel("Final time step capacity (MW)")

# Grid and ticks for readability
ax.grid(True, which="major", linestyle="--", linewidth=0.7, alpha=0.6)
ax.grid(True, which="minor", linestyle=":", linewidth=0.5, alpha=0.4)
ax.minorticks_on()


# Format y-axis with thousands separator if large
def _fmt_thousands(x: float, _pos: int) -> str:
    return f"{x:,.0f}"


ax.yaxis.set_major_formatter(FuncFormatter(_fmt_thousands))

# Legend outside for clarity
legend = ax.legend(
    title="Generators", loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False
)
legend._legend_box.align = "left"

plt.show()
