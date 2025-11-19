"""Data dictionaries for the optimization models."""

test_data_model1 = {
    "test1": {
        "load": 1100.0,
        "co2_price": 10.0,
        "gen_data": {
            "Wind": {
                "lcoe": 50,
                "max_capacity": 800.0,
                "min_capacity": 0,
                "cf": 1,
                "co2": 0,
            },
            "Solar": {
                "lcoe": 30,
                "max_capacity": 800.0,
                "min_capacity": 0,
                "cf": 1,
                "co2": 0,
            },
            "Conv": {
                "lcoe": 40,
                "max_capacity": 800.0,
                "min_capacity": 100.0,
                "cf": 1,
                "co2": 20.0,
            },
        },
    }
}
