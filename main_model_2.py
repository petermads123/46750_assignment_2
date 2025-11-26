"""Model 2 main script."""

from assignment_2.model2 import DataModel, IntertemporalExpansionModel

# test 1
model = IntertemporalExpansionModel()
data = DataModel()
data.jonas()
model.define_model(data=data)
model.optimize()
results = model.get_results()
print(results)
