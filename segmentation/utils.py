import yaml


def getArgs(filename):
    with open(filename) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        args = yaml.load(file, Loader=yaml.FullLoader)
    return args
