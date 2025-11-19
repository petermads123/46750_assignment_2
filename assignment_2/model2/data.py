"""Data dictionaries for the optimization model."""


class DataModel2:
    """Class for holding data for model 2."""

    def __init__(self) -> None:
        """Initialize instance."""
        self.load_series: list[float]
        self.co2_price: float
        self.gen_data: dict[str, dict[str, float]] = {}
        self.cf_data: dict[str, dict[str, list[float]]] = {}
        self.T: int
        self.gen_names: list[str] = []

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
        if isinstance(max_cf, float):
            max_cf = [max_cf] * self.T
        if isinstance(min_cf, float):
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

    def test_1(self) -> None:
        """Predefined test data 1."""
        self.add_load_series([400, 500, 600, 700])
        self.add_co2_price(20.0)
        self.add_generator(
            gen_name="Wind",
            capex=50.0,
            fixed_opex=5.0,
            var_opex=0.0,
            decex=25.0,
            initial_capacity=300.0,
            max_capacity=800.0,
            max_cf=[0.4, 0.5, 0.6, 0.5],
            min_cf=[0, 0, 0, 0],
            co2=0,
        )
        self.add_generator(
            gen_name="Solar",
            capex=40.0,
            fixed_opex=1.0,
            var_opex=0.0,
            decex=20.0,
            initial_capacity=100.0,
            max_capacity=800.0,
            max_cf=[0.8, 0.5, 0.3, 0.2],
            min_cf=[0.0, 0.0, 0.0, 0.0],
            co2=0.0,
        )
        self.add_generator(
            gen_name="Conv",
            capex=20.0,
            fixed_opex=5.0,
            var_opex=5.0,
            decex=10.0,
            initial_capacity=500.0,
            max_capacity=10000.0,
            max_cf=[1.0, 1.0, 1.0, 1.0],
            min_cf=[0.1, 0.1, 0.1, 0.1],
            co2=10.0,
        )
