"""Model 2 main script."""

import matplotlib.pyplot as plt
import numpy as np
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


# CO2 price sensitivy analysis
co2_prices = np.arange(0, 100000000, 1000000)
obj_values = []
for price in tqdm(co2_prices):
    data.add_co2_price(price)
    model.define_model(data=data, discount_factor=0.05)
    model.optimize()
    _, obj_val = model.get_results()
    obj_values.append(obj_val)

plt.figure(figsize=(6, 3))
plt.plot(co2_prices, obj_values)
plt.xlabel("CO2 Price [DKK/ton]")
plt.ylabel("Objective Value [DKK]")
plt.title("CO2 Price Sensitivity Analysis")
plt.tight_layout()
plt.show()
