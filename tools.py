import json
import re


def cal(text):
    """
    :param text: a string of response from GPT-3
    :return: a string of the calculation result
    """
    print("- Use Calculator -")
    # get formula
    i = 1
    while i <= len(text) and text[-i] != "\n":
        i += 1
    formula = text[-i + 1 : -2]
    print("input:", formula)

    # calculate
    formula = formula.replace("x", "*")
    output = eval(formula)

    # if the output is an integer, then convert it to int
    # else, round it to 2 decimal places
    output = int(output) if output == int(output) else round(float(output), 2)
    print("output:", output)
    return str(output)


def crp(text):
    """
    :param text: a string of response from GPT-3
    :return: a string of the chemical reaction
    """
    print("- Use Chemical reaction predictor -")
    # get products
    i = 1
    while i <= len(text) and text[-i] != "\n":
        i += 1

    products = text[-i + 1 :].replace(",", "").split()[1:]

    # get reactants
    j = i + 1
    while j <= len(text) and text[-j] != "\n":
        j += 1
    reactants = text[-j + 1 : -i].replace(",", "").split()[1:]
    print("input:", reactants, "=>", products)

    # if there is a question mark in the reactants,
    # then the reaction is reversed temporarily
    if any("?" in s for s in reactants):
        inv = True
        reactants, products = products, reactants
    else:
        inv = False

    # get atoms in reactants and add them to atoms_d
    atoms_d = {}
    for reactant in reactants:
        # get the number before the product
        num_idx = 0
        while reactant[num_idx].isdigit():
            num_idx += 1
        num = 1 if num_idx == 0 else int(reactant[:num_idx])

        reactant = reactant[num_idx:]
        for key, value in _count_atom(reactant).items():
            if key in atoms_d:
                atoms_d[key] += value * num
            else:
                atoms_d[key] = value * num

    # get atoms in products and subtract them from atoms_d
    for idx, product in enumerate(products):
        if product[0] == "?":
            mask_formula = product[1:]
            mask_idx = idx
            continue
        # get the number before the product
        num_idx = 0
        while product[num_idx].isdigit():
            num_idx += 1
        num = 1 if num_idx == 0 else int(product[:num_idx])

        product = product[num_idx:]
        for key, value in _count_atom(product).items():
            atoms_d[key] -= value * num

    # calculate the mask (question mark)
    mask_d = _count_atom(mask_formula)
    mask = -1
    for key, value in mask_d.items():
        if mask == -1:
            mask = atoms_d[key] / value
        # if the mask is not an integer, return ""
        elif mask != atoms_d[key] / value:
            return ""

    # replace the mask with the calculated number
    products[mask_idx] = str(int(mask)) + mask_formula

    # reverse the reaction if necessary
    if inv:
        reactants, products = products, reactants

    output = " + ".join(reactants) + " → " + " + ".join(products)
    print("output:", output)

    return output


def mml(text):
    """
    :param text: a string of response from GPT-3
    :return: a string of the molecular mass
    """
    print("- Use Molecular mass calculator -")
    # get chemical formula
    i = 1
    while i <= len(text) and text[-i] != "\n":
        i += 1
    formula = text[-i + 1 :]
    print("input:", formula)

    # get the dictionary of the chemical formula
    formula_d = _count_atom(formula)

    # get the atomic weight dictionary
    with open("atomic_weight.json", "r") as f:
        atomic_weight = json.load(f)

    # calculate the molecular mass
    molecular_mass = 0
    for key, value in formula_d.items():
        molecular_mass += atomic_weight[key] * value

    print("output:", molecular_mass, "g/mol")
    return str(molecular_mass) + " g/mol"


def _count_atom(formula):
    """
    :param formula: a string of chemical formula
    :return: a dictionary of the chemical formula
    """
    # if there is a bracket in formula
    if "(" in formula:
        # get the content in the bracket
        in_bracket = formula[formula.find("(") + 1 : formula.find(")")]
        # get the number after the bracket
        num_idx_start = formula.find(")") + 1
        num_idx_end = num_idx_start
        while num_idx_end < len(formula) and formula[num_idx_end].isdigit():
            num_idx_end += 1
        num = int(formula[num_idx_start : num_idx_end])
        # get the dictionary of the content in the bracket * num
        formula_d = {key: value * num for key, value in _count_atom(in_bracket).items()}
        # remove the content in the bracket
        formula = formula[: formula.find("(")] + formula[num_idx_end:]
    else:
        formula_d = {}

    # get the dictionary of the content outside the bracket
    for i in re.findall(r"[A-Z][^A-Z]*", formula):
        elem = re.match(r"\D+", i).group()
        num = i.replace(elem, "")
        num = 1 if num == "" else int(num)
        if elem in formula_d:
            formula_d[elem] += num
        else:
            formula_d[elem] = num

    return formula_d
