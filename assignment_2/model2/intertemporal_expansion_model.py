"""Implementation of optimization model 2."""

from gurobipy import GRB, Model, quicksum

from assignment_2.model2.data import DataModel


class IntertemporalExpansionModel:
    """Intertemporal expansion optimization model.

    Including multiple time periods and investment decisions.
    """

    def __init__(self) -> None:
        """Initialize instance."""

    def define_model(
        self, data: DataModel, model_id: int = 0, weigth: float = 1.0
    ) -> None:
        """Define the optimization model and its parameters.

        Args:
            data (DataModel): Data for the optimization model.
            model_id (int, optional): Identifier for the model instance
                if multiple models are created together. Defaults to 0.
                Leave blank if objective should be defined in this method.
            weigth (float, optional): Weight of the objective if multiple
        """
        # Create gurobi model
        if model_id == 0:
            self.model = Model("IntertemporalExpansionModel")

        self.gen_names = data.gen_names
        self.T = data.T

        # Define variables
        self.vars = {}

        for t in range(data.T):
            for gen in data.gen_names:
                # Capacity at each time period for each generator
                self.vars[f"{gen}_cap_{t}"] = self.model.addVar(
                    name=f"{gen}_cap_{t}",
                    lb=0,
                    ub=data.gen_data[gen]["max_capacity"],
                )

                # Investment decision at each time period for each generator
                self.vars[f"{gen}_inv_{t}"] = self.model.addVar(
                    name=f"{gen}_inv_{t}", lb=0, ub=GRB.INFINITY
                )

                # Decommissioning decision at each time period for each generator
                self.vars[f"{gen}_dec_{t}"] = self.model.addVar(
                    name=f"{gen}_dec_{t}", lb=0, ub=GRB.INFINITY
                )

                # Generation at each time period for each generator
                self.vars[f"{gen}_gen_{t}_{model_id}"] = self.model.addVar(
                    name=f"{gen}_gen_{t}_{model_id}",
                    lb=0,
                )

        # Define objective
        self.model.ModelSense = GRB.MINIMIZE
        self.model.setObjectiveN(
            quicksum(
                self.vars[f"{gen}_gen_{t}_{model_id}"]
                * (
                    data.gen_data[gen]["var_opex"]
                    + data.co2_price * data.gen_data[gen]["co2"]
                )
                + data.gen_data[gen]["fixed_opex"] * self.vars[f"{gen}_cap_{t}"]
                + self.vars[f"{gen}_inv_{t}"] * data.gen_data[gen]["capex"]
                + self.vars[f"{gen}_dec_{t}"] * data.gen_data[gen]["decex"]
                for gen in data.gen_names
                for t in range(data.T)
            ),
            index=model_id,
            weight=weigth,
        )

        # Define constraints
        self.constr = {}
        for t in range(data.T):
            # Energy balance constraint
            self.constr[f"energy_balance_{t}_{model_id}"] = self.model.addConstr(
                quicksum(
                    self.vars[f"{gen}_gen_{t}_{model_id}"] for gen in data.gen_names
                )
                >= data.load_series[t],
                name=f"energy_balance_{t}_{model_id}",
            )

            for gen in data.gen_names:
                # Generation constraints
                self.constr[f"gen_max_{gen}_{t}_{model_id}"] = self.model.addConstr(
                    self.vars[f"{gen}_gen_{t}_{model_id}"]
                    <= self.vars[f"{gen}_cap_{t}"] * data.cf_data[gen]["max_cf"][t],
                    name=f"gen_max_{gen}_{t}_{model_id}",
                )

                self.constr[f"gen_min_{gen}_{t}_{model_id}"] = self.model.addConstr(
                    self.vars[f"{gen}_gen_{t}_{model_id}"]
                    >= self.vars[f"{gen}_cap_{t}"] * data.cf_data[gen]["min_cf"][t],
                    name=f"gen_min_{gen}_{t}_{model_id}",
                )

                # Generation capacity evolution constraints
                if t == 0:
                    self.constr[f"cap_evol_{gen}_{t}"] = self.model.addConstr(
                        self.vars[f"{gen}_cap_{t}"]
                        == data.gen_data[gen]["initial_capacity"]
                        + self.vars[f"{gen}_inv_{t}"]
                        - self.vars[f"{gen}_dec_{t}"],
                        name=f"cap_evol_{gen}_{t}",
                    )
                else:
                    self.constr[f"cap_evol_{gen}_{t}"] = self.model.addConstr(
                        self.vars[f"{gen}_cap_{t}"]
                        == self.vars[f"{gen}_cap_{t - 1}"]
                        + self.vars[f"{gen}_inv_{t}"]
                        - self.vars[f"{gen}_dec_{t}"],
                        name=f"cap_evol_{gen}_{t}",
                    )

        self.model.update()

    def optimize(self) -> None:
        """Optimize the model."""
        self.model.optimize()

    def get_results(self) -> dict[str, float | dict[str, list[float]]]:
        """Get optimization results.

        Returns:
            dict[str, float | dict[str, list[float]]]: Dictionary with results.
        """
        if self.model.getAttr("Status") != GRB.OPTIMAL:
            raise Exception("Optimization was not successful.")

        results = {}
        results["objective_value"] = self.model.objVal
        results["capacities"] = {}
        results["generation"] = {}
        results["investments"] = {}
        results["decommissions"] = {}

        for gen in self.gen_names:
            # Capacities per timestamp
            results["capacities"][gen] = [
                self.vars[f"{gen}_cap_{t}"].X for t in range(self.T)
            ]

            # Investments per timestamp
            results["investments"][gen] = [
                self.vars[f"{gen}_inv_{t}"].X for t in range(self.T)
            ]

            # Decommissions per timestamp
            results["decommissions"][gen] = [
                self.vars[f"{gen}_dec_{t}"].X for t in range(self.T)
            ]

        return results
