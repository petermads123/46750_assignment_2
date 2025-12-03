"""Model 2 main script."""

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
