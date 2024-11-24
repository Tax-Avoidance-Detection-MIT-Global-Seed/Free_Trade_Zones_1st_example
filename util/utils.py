import importlib

# TODO The return is not an str, it is an actual python class. Therefore, instead of "-> str" it should be "-> type"
def import_function(fitness_function_str: str) -> str:
    module, method = fitness_function_str.rsplit(".", 1)
    fitness_function = importlib.import_module(module) # Dynamically imports the module which name corresponds to the value of the "module" variable
    method = getattr(fitness_function, method) # Dynamically retrieves the class which name corresponds to the value of the "method" variable and that it is within the module stored at "fitness_function"
    return method
