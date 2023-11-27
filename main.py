from bs4 import BeautifulSoup
import os
import re
from gen_func_util import generate_function
import traceback


# file name for debug
def parse_html(html, file_name):
    def table_to_markdown(table):
        data = [[td.get_text(strip=True) for td in tr.find_all('td')] for tr in table.find_all('tr')]

        # Remove any empty first item
        if not data[0]:
            data = data[1:]

        lines = [' - '.join(row) + ',' for row in data]
        return '\n'.join(lines)

    soup = BeautifulSoup(html, 'lxml')

    brief_desc = soup.find(class_="refnamediv").find('p').get_text().strip()

    # Get all C Specifications
    c_specs = soup.select(".refsynopsisdiv > .funcsynopsis > .funcprototype-table")

    # function names to specs
    func_dict = {}

    for spec in c_specs:
        spec_text = spec.get_text().strip()
        spec_text = ' '.join(spec_text.split())

        func_dict[spec.find(class_="fsfunc").text] = spec_text

    parameters = {}

    param_elem = None
    if soup.find('h2', string='Parameters') is not None:
        param_elem = soup.find('h2', string='Parameters').parent

    if param_elem is not None:
        if len(param_elem.find_all('math')) > 0:
            print(f"Warning: {file_name} has math elements. The docs may be poorly formatted")

        var_list = param_elem.find(class_="variablelist")

        dt_elements = var_list.find_all('dt')
        dd_elements = var_list.find_all('dd')

        for dt, dd in zip(dt_elements, dd_elements):
            # Get parameter names. There might be multiple parameters for one description.
            parameter_names = [em.get_text() for em in dt.find_all('em', class_='parameter')]
            # Get description
            description = dd.p.get_text()
            description = ' '.join(description.split())

            table = dd.find(class_="informaltable")

            if table is not None:
                description += "\n\n"
                description += table_to_markdown(table)

            for name in parameter_names:
                parameters[name] = description

    return func_dict, brief_desc, parameters


# without file extensions
def get_filenames_in_dir(directory):
    list = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            list.append(os.path.splitext(filename)[0])

    list.sort()
    return list


# should always end with slash
PARSE_DIR = "htdocs/gl4/"

fnames = get_filenames_in_dir(PARSE_DIR)
# fnames = ["glBindBuffer"]

print("Number of files to process: ", len(fnames))

if not os.path.exists("out/"):
    os.makedirs("out/")

# Write to file
with open('out/opengl_documentation.h', 'w') as f:
    undefs = []
    functions = ""

    for file_name in fnames:
        path = f"{PARSE_DIR}{file_name}"

        with open(path, 'r') as file:
            html = file.read()

            try:
                func_dict, brief_desc, parameters = parse_html(html, file_name)

                for function_name, c_spec in func_dict.items():
                    output = generate_function(function_name, brief_desc, c_spec, parameters)
                    functions += output
                    undefs.append(function_name)
            except Exception as e:
                # print(f"Error on {file_name}: {traceback.format_exc()}")
                print(f"Error on {file_name}")

    for function_name in undefs:
        f.write(f"#undef {function_name}\n")
    f.write(functions)

print("Wrote generated files to:", os.path.abspath("out/"))
