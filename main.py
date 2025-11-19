"""Main script to run the optimization models."""

from assignment_2.model1.data import test_data_model1
from assignment_2.model1.model1 import LCOEOptimizationModel

model = LCOEOptimizationModel()
data = test_data_model1["test1"]
load: float = data["load"]
co2_price: float = data["co2_price"]
gen_data: dict[str, dict[str, float]] = data["gen_data"]
model.define_model(load=load, gen_data=gen_data, co2_price=co2_price)
model.optimize()
results = model.get_results()
print("Done!")
