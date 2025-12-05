"""Model 1 main script."""

import matplotlib.pyplot as plt

from assignment_2.model1 import DataModel1, LCOEModel

# test 1
model = LCOEModel()
data = DataModel1()
data.freja()
model.define_model(data=data)
model.optimize()
results = model.get_results()
generation: dict[str, float] = results["generation"]  # type: ignore
print(results)


### Plotting ###
labels_values = sorted(generation.items(), key=lambda kv: kv[1], reverse=True)
labels = [k for k, _ in labels_values]
values = [v for _, v in labels_values]

# Use a professional, colorblind-friendly palette
base_colors = list(plt.get_cmap("tab20").colors)
colors = [model.colors.get(label) for label in labels]


def _autopct(pct: float) -> str:
    return f"{pct:.1f}%" if pct >= 3 else ""


fig, ax = plt.subplots(figsize=(10, 5), constrained_layout=True)
wedges, texts, autotexts = ax.pie(
    values,
    labels=None,
    colors=colors,
    startangle=90,
    counterclock=False,
    autopct=_autopct,
    pctdistance=0.75,
    wedgeprops={"width": 0.4, "edgecolor": "white", "linewidth": 1},
)

for t in autotexts:
    t.set_color("white")
    t.set_fontsize(9)
    t.set_weight("bold")

ax.set_aspect("equal")

total = sum(values) if values else 0.0
percentages = [(v / total * 100) if total else 0.0 for v in values]
legend_labels = [
    f"{lab} — {p:.1f}%" for lab, p, v in zip(labels, percentages, values, strict=True)
]
ax.legend(
    wedges,
    legend_labels,
    title="Sources",
    loc="center left",
    bbox_to_anchor=(1.02, 0.5),
    frameon=False,
)

ax.set_title("Generation Mix", pad=12)
plt.show()
