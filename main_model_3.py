"""Model 2 main script."""

from assignment_2.model2 import DataModel
from assignment_2.model3 import UncertaintyModel

# test 1
model = UncertaintyModel()
data = DataModel()
data.jonas()
model.define_uncertainty_model(data)
model.optimize()
results = model.get_results()
print(results)
