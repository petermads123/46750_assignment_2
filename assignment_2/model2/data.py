"""Data class for the optimization intertemporal expansion model."""

import numpy as np


class DataModel:
    """Class for holding data for the intertemporal expansion model."""

    def __init__(self) -> None:
        """Initialize instance."""
        self.load_series: list[float]
        self.co2_price: float
        self.gen_data: dict[str, dict[str, float]] = {}
        self.cf_data: dict[str, dict[str, list[float]]] = {}
        self.T: int
        self.gen_names: list[str] = []
        self.prev_load_factor: float = 1.0
        self.scenario_weights: list[float] = []
        self.cfs: list[dict[str, float | list[float]]] = []
        self.load_factors: list[float] = []

    def add_load_series(self, load_series: list[float]) -> None:
        """Add load series to the instance.

        Args:
            load_series (list[float]): Load series to be added.
        """
        self.load_series = load_series
        self.T = len(load_series)

    def add_co2_price(self, co2_price: float) -> None:
        """Add CO2 price to the instance.

        Args:
            co2_price (float): CO2 price to be added.
        """
        self.co2_price = co2_price

    def add_generator(
        self,
        gen_name: str,
        capex: float = 0,
        fixed_opex: float = 0,
        var_opex: float = 0,
        decex: float = 0,
        initial_capacity: float = 0,
        max_capacity: float = 0,
        max_cf: list[float] | float = 1,
        min_cf: list[float] | float = 0,
        co2: float = 0,
    ) -> None:
        """Add generator data to the instance.

        Args:
            gen_name (str): Name of the generator.
            capex (float, optional): Capital expenditure. Defaults to 0.
            fixed_opex (float, optional): Fixed operational expenditure. Defaults to 0.
            var_opex (float, optional): Variable operational expenditure. Defaults to 0.
            decex (float, optional): Decommissioning expenditure. Defaults to 0.
            initial_capacity (float, optional): Initial capacity. Defaults to 0.
            max_capacity (float, optional): Maximum capacity. Defaults to 0.
            max_cf (list[float] | float, optional): Maximum capacity factor. Defaults to 1.
                If list, must match length of load_series.
            min_cf (list[float] | float, optional): Minimum capacity factor. Defaults to 0.
                If list, must match length of load_series.
            co2 (float, optional): CO2 emissions unit generated. Defaults to 0.
        """
        if not isinstance(max_cf, list):
            max_cf = [max_cf] * self.T
        if not isinstance(min_cf, list):
            min_cf = [min_cf] * self.T

        self.gen_data[gen_name] = {
            "capex": capex,
            "fixed_opex": fixed_opex,
            "var_opex": var_opex,
            "decex": decex,
            "initial_capacity": initial_capacity,
            "max_capacity": max_capacity,
            "co2": co2,
        }
        self.cf_data[gen_name] = {
            "max_cf": max_cf,
            "min_cf": min_cf,
        }

        self.gen_names.append(gen_name)

    def set_cf(self, cf: dict[str, float | list[float]]) -> None:
        """Set a factor to scale all renewable generators' capacity factors.

        Args:
            cf (dict[str, float | list[float]]): Scaling factors for renewable generators.
        """
        for gen in self.gen_names:
            if gen in cf:
                cf_new = cf[gen]
                if isinstance(cf_new, float | int):
                    new_cf = [cf_new] * self.T
                elif isinstance(cf_new, list):
                    new_cf = cf_new

                self.cf_data[gen]["max_cf"] = new_cf

    def scale_load(self, factor: float) -> None:
        """Set a factor to scale the load series.

        Args:
            factor (float): Scaling factor for the load series.
        """
        self.load_series = [
            load / self.prev_load_factor * factor for load in self.load_series
        ]
        self.prev_load_factor = factor

    def set_scenario_factors(
        self,
        scenario_weights: list[float],
        cfs: list[dict[str, float | list[float]]],
        load_factors: list[float],
    ) -> None:
        """Set scenario factors for uncertainty modeling.

        Args:
            scenario_weights (list[float]): Weights for each uncertainty scenario.
            cfs (list[dict[str, float | list[float]]]): New CFs for each scenario to adjust renewable generation.
            load_factors (list[float]): Factors to adjust load series.
        """
        self.scenario_weights = scenario_weights
        self.cfs = cfs
        self.load_factors = load_factors

    def jonas(self) -> None:
        """Predefined test data jonas."""
        load = np.array(
            [
                36,
                37.1,
                38.2,
                39.3,
                40.4,
                41.5,
                42.6,
                43.7,
                44.8,
                45.9,
                47,
                48.2,
                49.4,
                50.6,
                51.8,
                53,
                54.2,
                55.4,
                56.6,
                57.8,
                59,
            ]
        )
        self.add_load_series((load / 10**6).tolist())
        self.add_co2_price(32.6)
        self.add_generator(
            gen_name="Offshore_Wind",
            capex=0,  # TBD
            fixed_opex=0,  # TBD
            var_opex=0,  # TBD
            decex=0,  # TBD
            initial_capacity=0,  # TBD
            max_capacity=0,  # TBD
            max_cf=1,
            min_cf=0,
            co2=0,
        )
        self.add_generator(
            gen_name="Onshore_Wind",
            capex=0,  # TBD
            fixed_opex=0,  # TBD
            var_opex=0,  # TBD
            decex=0,  # TBD
            initial_capacity=0,  # TBD
            max_capacity=0,  # TBD
            max_cf=1,
            min_cf=0,
            co2=0,
        )
        self.add_generator(
            gen_name="Solar_PV",
            capex=0,  # TBD
            fixed_opex=0,  # TBD
            var_opex=0,  # TBD
            decex=0,  # TBD
            initial_capacity=0,  # TBD
            max_capacity=0,  # TBD
            max_cf=1,
            min_cf=0,
            co2=0,
        )
        self.add_generator(
            gen_name="Conventional",
            capex=0,  # TBD
            fixed_opex=0,  # TBD
            var_opex=0,  # TBD
            decex=0,  # TBD
            initial_capacity=0,  # TBD
            max_capacity=0,  # TBD
            max_cf=1,
            min_cf=0,
            co2=0,  # TBD
        )
        self.set_scenario_factors(
            scenario_weights=[
                0.027583,
                0.069542,
                0.139083,
                0.069542,
                0.027583,
                0.027583,
                0.069542,
                0.139083,
                0.069542,
                0.027583,
                0.027583,
                0.069542,
                0.139083,
                0.069542,
                0.027583,
            ],
            cfs=[
                {
                    "Offshore_Wind": 0.530145459,
                    "Onshore_Wind": 0.370145459,
                    "Solar_PV": 0.15043685,
                },
                {
                    "Offshore_Wind": 0.473233414,
                    "Onshore_Wind": 0.313233414,
                    "Solar_PV": 0.136019132,
                },
                {"Offshore_Wind": 0.41, "Onshore_Wind": 0.25, "Solar_PV": 0.12},
                {
                    "Offshore_Wind": 0.346766586,
                    "Onshore_Wind": 0.186766586,
                    "Solar_PV": 0.103980868,
                },
                {
                    "Offshore_Wind": 0.289854541,
                    "Onshore_Wind": 0.129854541,
                    "Solar_PV": 0.08956315,
                },
                {
                    "Offshore_Wind": 0.530145459,
                    "Onshore_Wind": 0.370145459,
                    "Solar_PV": 0.15043685,
                },
                {
                    "Offshore_Wind": 0.473233414,
                    "Onshore_Wind": 0.313233414,
                    "Solar_PV": 0.136019132,
                },
                {"Offshore_Wind": 0.41, "Onshore_Wind": 0.25, "Solar_PV": 0.12},
                {
                    "Offshore_Wind": 0.346766586,
                    "Onshore_Wind": 0.186766586,
                    "Solar_PV": 0.103980868,
                },
                {
                    "Offshore_Wind": 0.289854541,
                    "Onshore_Wind": 0.129854541,
                    "Solar_PV": 0.08956315,
                },
                {
                    "Offshore_Wind": 0.530145459,
                    "Onshore_Wind": 0.370145459,
                    "Solar_PV": 0.15043685,
                },
                {
                    "Offshore_Wind": 0.473233414,
                    "Onshore_Wind": 0.313233414,
                    "Solar_PV": 0.136019132,
                },
                {"Offshore_Wind": 0.41, "Onshore_Wind": 0.25, "Solar_PV": 0.12},
                {
                    "Offshore_Wind": 0.346766586,
                    "Onshore_Wind": 0.186766586,
                    "Solar_PV": 0.103980868,
                },
                {
                    "Offshore_Wind": 0.289854541,
                    "Onshore_Wind": 0.129854541,
                    "Solar_PV": 0.08956315,
                },
            ],
            load_factors=[
                0.916969697,
                0.916969697,
                0.916969697,
                0.916969697,
                0.916969697,
                1,
                1,
                1,
                1,
                1,
                1.082415531,
                1.082415531,
                1.082415531,
                1.082415531,
                1.082415531,
            ],
        )
