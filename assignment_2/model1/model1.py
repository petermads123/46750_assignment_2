"""Implementation of optimization model 1."""

from gurobipy import GRB, Model, quicksum


class LCOEOptimizationModel:
    """Optimization model minimizing system LCOE."""

    def __init__(self) -> None:
        """Initialize instance."""

    def define_model(
        self,
        load: float,
        gen_data: dict[str, dict[str, float]],
        co2_price: float = 0.0,
    ) -> None:
        """Define the optimization model and its parameters.

        Args:
            load (float): Required load to be fullfilled.
            gen_data (dict[str, dict[str, float]]): Generator data including
                'lcoe', 'max_capacity', 'min_capacity', 'cf' and 'co2' for each generator.
            co2_price (float, optional): CO2 price. Defaults to 0.0.
        """
        # Create gurobi model
        self.model = Model("Model1")
        gen_names = list(gen_data.keys())

        # Define variables
        self.vars = {}
        for gen in gen_names:
            self.vars[gen] = self.model.addVar(
                name=f"capacity_{gen}",
                lb=gen_data[gen]["min_capacity"],
                ub=gen_data[gen]["max_capacity"],
            )

        # Define objective
        self.model.setObjective(
            quicksum(
                (gen_data[gen]["lcoe"] + gen_data[gen]["co2"] * co2_price)
                * self.vars[gen]
                * gen_data[gen]["cf"]
                for gen in gen_names
            ),
            GRB.MINIMIZE,
        )

        # Define constraints
        self.constr = {}
        # Energy balance constraint
        self.constr["energy_balance"] = self.model.addConstr(
            quicksum(self.vars[gen] * gen_data[gen]["cf"] for gen in gen_names) == load
        )

        self.model.update()

    def optimize(self) -> None:
        """Optimize the model."""
        self.model.optimize()

    def get_results(self) -> dict[str, float]:
        """Get the optimization results.

        Returns:
            dict[str, float]: Dictionary with generator names as keys and optimized capacities as values.
        """
        results = {}
        for var in self.model.getVars():
            results[var.VarName] = var.x
        return results
