"""Model 2 main script."""

from assignment_2.model2 import DataModel2, IntertemporalExpansionModel

# test 1
model = IntertemporalExpansionModel()
data = DataModel2()
data.test_1()
model.define_model(data=data)
model.optimize()
results = model.get_results()
print(results)
