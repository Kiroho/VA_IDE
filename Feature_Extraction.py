import re

zeile_keywords = ['zeil', 'teil', 'silo', 'seil', 'zeit', 'zell', 'sail', 'reih', 'seit']

if_operator_keywords = [' gross gleich ', ' klein gleich ', ' klein ', ' gleich ', ' gross ', ' in ']
if_operator_symbols = {' gross gleich ': '>=', ' klein gleich ': '<=', ' klein ': '<', ' gleich ': '==', ' gross ': '>',
                       ' in ': 'in'}
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


# def if_extraction(text_list):
#     row = find_one_row(text_list)
#     variable_a = ""
#     variable_b = ""
#     is_not = False
#     operator = ""
#     text = " ".join(text_list)
#     text = text.replace(" ist ", " ")
#     text = text.replace(" als ", " ")
#     for keyword in if_operator_keywords:
#         if keyword in text:
#             try:
#                 before_keyword, keyword, after_keyword = text.partition(keyword)
#                 operator = if_operator_symbols.get(keyword)
#                 variable_a = before_keyword.split()[-1]
#                 if variable_a in if_not_keyword:
#                     variable_a = before_keyword.split()[-2]
#                     is_not = True
#                 else:
#                     for word in if_not_keyword:
#                         if word in text:
#                             is_not = word
#                             break
#                 variable_b = after_keyword.split()[0]
#             except Exception:
#                 pass
#             finally:
#                 break
#     print(f'Variable a: {variable_a}')
#     print(f'Variable b: {variable_b}')
#     print(f'Operator: {operator}')
#     print(f'is not?: {is_not}')
#     return {"row": row, "variable_a": variable_a, "variable_b": variable_b, "operator": operator, "is_not": is_not}



# if __name__ == '__main__':
#     find_one_row("ein fabfrag in zeil 3.".split())
