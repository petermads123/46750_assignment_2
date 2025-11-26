"""Model 2 main script."""

from assignment_2.model2 import DataModel
from assignment_2.model3 import UncertaintyModel

model = UncertaintyModel()
data = DataModel()
data.jonas()
model.define_uncertainty_model(data)
model.optimize()
results, obj_val = model.get_results()
print(results)
print("Objective value:", obj_val)
model.plot_results(scale_factor=365 * 24)
