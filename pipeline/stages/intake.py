import yaml
from pipeline.models import FeatureSpec


def load_spec(path: str) -> FeatureSpec:
    with open(path, "r") as file:
        data = yaml.safe_load(file)

    validated = FeatureSpec(**data)

    return validated