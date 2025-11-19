"""Model 1 main script."""

from assignment_2.model1 import DataModel1, LCOEModel

# test 1
model = LCOEModel()
data = DataModel1()
data.test_1()
model.define_model(data=data)
model.optimize()
results = model.get_results()
print(results)
