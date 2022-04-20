import ast
import json
# import test im

MAIN_CLASS = 'Schematic'
INPUT_FILE = 'test.py'
OUTPUT_FILE = 'out.md'


def parse_classes(file):

    with open(file, "r") as f:
        p = ast.parse(f.read())

    # get all classes from the given python file.
    classes = [c for c in ast.walk(p) if isinstance(c, ast.ClassDef)]

    classesDict = dict()
    for x in classes:
        class_name = x.name

        for ib in x.body:
            if isinstance(ib, ast.FunctionDef):
                init_body = ib
                break

        init_args = []
        for init_arg in init_body.args.args:
            init_args.append(init_arg.arg)

        init_vars = []
        for init_var in init_body.body:
            if isinstance(init_var, ast.Assign):
                if hasattr(init_var.targets[0], 'attr'):
                    # self variable
                    var_name = init_var.targets[0].attr
                    var_cname = init_var.targets[0].value.id

                else:
                    # normal variable
                    var_name = init_var.targets[0].id
                    var_cname = None

                var_value_class_type = None
                var_value_type = None
                if hasattr(init_var.value, 'value'):
                    var_value = init_var.value.value
                elif hasattr(init_var.value, 'id'):
                    var_value = init_var.value.id
                else:
                    print("unknown values")

            elif isinstance(init_var, ast.AnnAssign):
                if hasattr(init_var.target, 'attr'):
                    # self variable
                    var_name = init_var.target.attr
                    var_cname = init_var.target.value.id

                else:
                    # normal variable
                    var_name = init_var.target.id
                    var_cname = None

                # one or multiple object types typed
                if hasattr(init_var.annotation.slice, 'id'):
                    var_value_class_type = init_var.annotation.slice.id
                else:
                    types = init_var.annotation.slice.elts
                    types = [t.id for t in types]
                    var_value_class_type = types

                var_value_type = init_var.annotation.value.id
                var_value = None

            varDict = {
                'var_name': var_name,
                'var_cname': var_cname,
                'var_value': var_value,
                'var_value_class_type': var_value_class_type,
                'var_value_type': var_value_type
            }

            init_vars.append(varDict)

        classDict = {
            'init_args': init_args,
            'init_vars': init_vars
        }

        classesDict[class_name] = classDict

    return classesDict

def generate_map(classesDict, main_class):
    # print(json.dumps(classesDict, sort_keys=True, indent=4))
    td = classesDict[main_class]
    print(td)

classesDict = parse_classes(INPUT_FILE)
generate_map(classesDict, MAIN_CLASS)


print('break')
