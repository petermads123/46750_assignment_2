"""Main script to run the optimization models."""

from assignment_2.model1.data import test_data_model1
from assignment_2.model1.model1 import LCOEOptimizationModel
from assignment_2.model2.data import DataModel2
from assignment_2.model2.model2 import IntertemporalExpansionModel

# Model 1
model = LCOEOptimizationModel()
data = test_data_model1["test1"]
model.define_model(
    load=data["load"], gen_data=data["gen_data"], co2_price=data["co2_price"]
)
model.optimize()
results1 = model.get_results()
print(results1)

# Model 2
model2 = IntertemporalExpansionModel()
data_model2 = DataModel2()
data_model2.test_1()
model2.define_model(data=data_model2)
model2.optimize()
results2 = model2.get_results()
print(results2)
