"""Implementation of optimization model 1."""

from gurobipy import GRB, Model, quicksum

from assignment_2.model1.data import DataModel1


class LCOEModel:
    """Optimization model minimizing system LCOE."""

    def __init__(self) -> None:
        """Initialize instance."""

    def define_model(self, data: DataModel1) -> None:
        """Define the optimization model and its parameters.

        Args:
            data (DataModel1): Data for the optimization model.
        """
        # Create gurobi model
        self.model = Model("Model1")
        self.model.setParam("OutputFlag", 0)
        self.gen_names = data.gen_names

        # Define variables
        self.vars = {}

        for gen in data.gen_names:
            self.vars[gen] = self.model.addVar(
                name=f"{gen}_gen",
                lb=data.gen_data[gen]["min_cf"] * data.gen_data[gen]["capacity"],
                ub=data.gen_data[gen]["max_cf"] * data.gen_data[gen]["capacity"],
            )

        # Define objective
        self.model.setObjective(
            quicksum(
                (
                    data.gen_data[gen]["lcoe"]
                    + data.gen_data[gen]["co2"] * data.co2_price
                )
                * self.vars[gen]
                for gen in data.gen_names
            ),
            GRB.MINIMIZE,
        )

        # Define constraints
        self.constr = {}
        # Energy balance constraint
        self.constr["energy_balance"] = self.model.addConstr(
            quicksum(self.vars[gen] for gen in data.gen_names) == data.load
        )

        self.model.update()

    def optimize(self) -> None:
        """Optimize the model."""
        self.model.optimize()

    def get_results(self) -> dict[str, float | dict[str, float]]:
        """Get the optimization results.

        Returns:
            dict[str, float | dict[str, float]]: Dictionary with results.
        """
        if self.model.getAttr("Status") != GRB.OPTIMAL:
            raise Exception("Optimization was not successful.")

        results = {}
        results["objective_value"] = self.model.objVal
        results["generation"] = {}

        for gen in self.gen_names:
            results["generation"][gen] = self.vars[gen].X

        return results
