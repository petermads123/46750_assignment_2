"""Implementation of optimization model 3."""

from assignment_2.model2.data import DataModel
from assignment_2.model2.intertemporal_expansion_model import (
    IntertemporalExpansionModel,
)


class UncertaintyModel(IntertemporalExpansionModel):
    """Uncertainty optimization model.

    Extending the intertemporal expansion model with uncertainty handling.
    """

    def __init__(self) -> None:
        """Initialize instance."""
        super().__init__()

    def define_uncertainty_model(
        self,
        data: DataModel,
        discount_factor: float = 1.0,
    ) -> None:
        """Define the optimization model and its parameters.

        Args:
            data (DataModel): Data for the optimization model.
            discount_factor (float, optional): Discount factor for future costs. Defaults to 1.0.
        """
        scenario_weights = data.scenario_weights
        cfs = data.cfs
        load_factors = data.load_factors

        for i in range(len(scenario_weights)):
            data.set_cf(cfs[i])
            data.scale_load(load_factors[i])
            super().define_model(
                data=data,
                discount_factor=discount_factor,
                model_id=i,
                weigth=scenario_weights[i],
            )
