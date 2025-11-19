"""Data class for the optimization model 1."""


class DataModel1:
    """Class for holding data for model 1."""

    def __init__(self) -> None:
        """Initialize instance."""
        self.load: float
        self.co2_price: float
        self.gen_data: dict[str, dict[str, float]] = {}
        self.gen_names: list[str] = []

    def add_load(self, load: float) -> None:
        """Add load to the instance.

        Args:
            load (float): Load to be added.
        """
        self.load = load

    def add_co2_price(self, co2_price: float) -> None:
        """Add CO2 price to the instance.

        Args:
            co2_price (float): CO2 price to be added.
        """
        self.co2_price = co2_price

    def add_generator(
        self,
        gen_name: str,
        lcoe: float = 0,
        capacity: float = 0,
        max_cf: float = 1,
        min_cf: float = 0,
        co2: float = 0,
    ) -> None:
        """Add generator data to the instance.

        Args:
            gen_name (str): Name of the generator.
            lcoe (float, optional): Levelized cost of energy. Defaults to 0.
            capacity (float, optional): Installed capacity. Defaults to 0.
            max_cf (float, optional): Maximum capacity factor. Defaults to 1.
            min_cf (float, optional): Minimum capacity factor. Defaults to 0.
            co2 (float, optional): CO2 emissions unit generated. Defaults to 0.
        """
        self.gen_data[gen_name] = {
            "lcoe": lcoe,
            "capacity": capacity,
            "max_cf": max_cf,
            "min_cf": min_cf,
            "co2": co2,
        }

        self.gen_names.append(gen_name)

    def test_1(self) -> None:
        """Predefined test data 1."""
        self.add_load(1100.0)
        self.add_co2_price(10.0)
        self.add_generator(
            gen_name="Wind",
            lcoe=50,
            capacity=800.0,
            max_cf=0.7,
            min_cf=0,
            co2=0,
        )
        self.add_generator(
            gen_name="Solar",
            lcoe=30,
            capacity=800.0,
            max_cf=0.3,
            min_cf=0,
            co2=0,
        )
        self.add_generator(
            gen_name="Conv",
            lcoe=40,
            capacity=800.0,
            max_cf=1,
            min_cf=0.1,
            co2=20.0,
        )
