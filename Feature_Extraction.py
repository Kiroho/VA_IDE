import re

zeile_keywords = ['zeil', 'teil', 'silo', 'seil', 'zeit', 'zell', 'sail', 'reih', 'seit']

if_operator_keywords = ['klein', 'gleich', 'gross']
if_operator_symbols = {'gross gleich': '>=', 'klein gleich': '<=', 'klein': '<', 'gleich': '==', 'gross': '>'}
if_not_keyword = ["nicht", "not"]


def find_rows(text_list):
    text = " ".join(text_list)
    # print(text)

    #"zeile" word correction
    for word in zeile_keywords:
        text = text.replace(word, "zeile")
    # print(text)

    if " zeile " in text:
        rows = re.findall(r'\d+', text)
        # print(rows)

        rows_f = []
        for numbers in rows:
            rows_f.append(numbers)
            # print(numbers)
        # print(f'rows{rows_f}')
        return rows_f
    else:
        # print("no rows")
        return []


def find_one_row(text_list):
    text = " ".join(text_list)
    # print(text)
    #"zeile" word correction
    for word in zeile_keywords:
        text = text.replace(word, " zeile ")
    if " zeile " in text:
        rows = re.findall(r'\d+', text)
        text = text.split(" zeile ")[1]
        text = text.split(" ")
        for word in text:
            if word.isdigit():
                print(f'Zeile: {word}')
                return word
        else:
            print("No Number")
            return None
    else:
        print("No Zeile")
        return None


def remove_stopwords(text_tuple_list):
    stopwords = ["nicht", "not", "ist", "als", "mit", "für", "fur", "der", "die", "das", "des", "dessen", "dies",
                 "dieses", "diesen", "diesem", "ein", "einer", "eine", "eines", "sein", "ihr",
                 "unser", "euer", "mein", "dein", "er", "sie", "es", "wir", "ihr", "noch", "so"]
    forbidden_chars = [".", ",", ";", ":", "!", "?", "_",
                       "-", "(", ")", "\"", "\'"]
    for word in stopwords:
        for i in range(0, len(text_tuple_list) - 1):
            if text_tuple_list[i][0] == word:
                text_tuple_list.pop(i)
            else:
                for char in forbidden_chars:
                    original = text_tuple_list[i][0]
                    original = original.replace(char, "")
                    text_tuple_list[i] = (original, text_tuple_list[i][1])
    print(f'Text without Stopwords: {text_tuple_list}')
    return text_tuple_list


def extract_if_operators(text_tuple_list):
    variable_a = None
    variable_b = None
    operator = None
    for i in range(0, len(text_tuple_list) - 1):
        for keyword in if_operator_keywords:
            if keyword == text_tuple_list[i][1]:
                if keyword == "gross" or keyword == "klein":
                    if text_tuple_list[i + 1][1] == "gleich":
                        variable_a = text_tuple_list[i - 1][0]
                        operator = text_tuple_list[i][1] + " gleich"
                        variable_b = text_tuple_list[i + 2][0]
                        return [variable_a, variable_b, operator]
                variable_a = text_tuple_list[i - 1][0]
                operator = text_tuple_list[i][1]
                variable_b = text_tuple_list[i + 1][0]
                return [variable_a, variable_b, operator]
    return [variable_a, variable_b, operator]


def extract_not(text_tuple_list):
    for keyword in if_not_keyword:
        for i in range(0, len(text_tuple_list) - 1):
            if keyword == text_tuple_list[i][1]:
                return True
    return False


def if_extraction(text_tuple_list):
    variable_a = None
    variable_b = None
    is_not = False
    operator = None
    is_not = extract_not(text_tuple_list)
    text_tuple_list = remove_stopwords(text_tuple_list)
    variable_a, variable_b, operator = extract_if_operators(text_tuple_list)
    if operator:
        operator = if_operator_symbols[operator]

    print(f'Variable a: {variable_a}')
    print(f'Variable b: {variable_b}')
    print(f'Operator: {operator}')
    print(f'is not?: {is_not}')
    return [variable_a, variable_b, operator, is_not]

#

# if __name__ == '__main__':
#     find_one_row("ein fabfrag in zeil 3.".split())
