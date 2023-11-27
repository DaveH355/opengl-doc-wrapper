import re
from collections import defaultdict


def generate_function(function_name, brief_desc, c_spec, parameters):
    def parse_c_prototype(function_name, c_prototype):
        pattern = r"(.+?)\s*" + re.escape(function_name) + r"\s*\((.*)\)\s*;"

        match = re.match(pattern, c_prototype.strip())
        if not match:
            raise ValueError(f"Invalid C prototype: {c_prototype}")

        return_type, params = match.groups()

        params = [p.strip().rstrip(';') for p in params.split(',')]
        return return_type, ', '.join(params)

    def parse_c_function_arguments(raw_params):
        # Split raw_params into individual parameters
        parameters = raw_params.split(',')
        param_names = []

        for param in parameters:
            param = param.strip()
            # Split by space and *, and consider the last word as the parameter name
            parts = re.split(r'\s+|\*', param)
            param_names.append(parts[-1])

        return param_names

    function_return_type, raw_function_params = parse_c_prototype(function_name, c_spec)

    # print("Function name: ", function_name)
    # print("C Prototype: ", c_spec)
    # print("Raw params: ", raw_function_params)

    function_has_params = True
    param_names = []
    if raw_function_params != "void":
        param_names = parse_c_function_arguments(raw_function_params)

    else:
        function_has_params = False

    output = f"/**\n * {brief_desc}\n"

    # Dict to map description to parameter names
    # For combining duplicate descriptions
    desc_dict = defaultdict(list)
    for param, desc in parameters.items():
        param = re.sub(r'\s+', ' ', param).strip()

        desc_dict[desc].append(param)

    for desc, params in desc_dict.items():
        desc = desc.strip().replace('\n', '\n * ')
        param_str = ', '.join(params)
        output += f" *\n * @param [{param_str}] {desc}\n"

    output += " */\n"

    output += f"static inline {c_spec.replace(";", "")} {{\n"
    if function_has_params:
        if function_return_type != "void":
            output += f"  return glad_{function_name}({', '.join(param_names)});\n"
        else:
            output += f"  glad_{function_name}({', '.join(param_names)});\n"
    else:
        output += f"  glad_{function_name}();\n"
    output += "}\n"

    return output
