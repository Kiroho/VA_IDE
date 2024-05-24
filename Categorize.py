from timeit import default_timer as timer
from tkinter import Text

from nltk.stem.snowball import SnowballStemmer
import re
import Editor_Commands as e
import Feature_Extraction as f

jump_to_keywords = ['navigi', 'wegehr', 'kavigi', 'verrigi', 'regi', 'karri', 'spring', 'bring', 'dringend', 'ring',
                    'kling']

copy_keywords = ['kopi', 'pir', 'pier', 'vier']

paste_keywords = ['einfug', 'klug', 'zug', 'schug', 'reinfug', 'einfuhr', 'fug']

delete_keywords = ['schutt', 'schutz', 'losch', 'entfern', 'fern', 'fernezeil', 'fernzeil']

if_keywords = ['ifanweis', 'if', 'anweis', 'abfrag', 'fabfrag', 'ifabfrag', 'efabfrag' 'hilfeanweis', 'fabfrag',
               'elfanweis', 'stiftanweis', 'veranweis', 'ifoption', 'tiefabfrag', 'ifabfragezeil', 'abfragezeil']

for_keywords = ['vorschleif', 'vorschlaf', 'vorschneif', 'vorschrift', 'bohrschleif', 'for', 'forschleife']

while_keywords = ['weilschleif', 'wildschleif', 'waldschleif', 'whileschleif', 'wireschraub', 'weilschlauf',
                  'wireschleif', 'waltschleif', 'while']

switch_keywords = ['switch', 'switchcas', 'witch', 'wich', 'hitch', 'match', 'cas', 'status']

exception_keywords = ['exception', 'ausnahm', 'final', 'expression']

endless_keywords = ['endoschleif', 'endlosschleif', 'endlossleif', 'luftschleif', 'endlos', 'infinity', 'infinity loop']

timer_keywords = ['tim', 'daima']

thread_keywords = ['thread', 'wett', 'thwett', 'sweat']

print_keywords = ['print', 'prund', 'trint', 'kind', 'printbefehl']

input_keywords = ['input', 'eingab']

snowball = SnowballStemmer("german")


def preprocess_text(owner, text):
    #lowercasing
    text = text.lower()
    # print(text)
    # text = "erstelle eine if-abfrage in seite 3? "
    #remove special chars and tokenize
    forbidden_end_of_line_chars = [".", ",", ";", ":", "!", "?", "_", "\-", "\(", "\)", "\"", "\'"]
    regex = r"(?<!\d)[.,;:!?_\-\(\)\"\'](?!\d)"
    text = re.sub(regex, "", text)
    # print(text)
    text_list = text.split()
    try:
        if text_list[-1][-1] in forbidden_end_of_line_chars:
            text_list[-1] = text_list[-1][:-1]
        # print(text)
    except Exception:
        owner.create_error_info("Command not found.", color="orange", timer=2000)

    #stemming
    text_list = [snowball.stem(word) for word in text_list]
    # print(text_list)

    return text_list


def classify_text(owner, editor, text):
    text_list = preprocess_text(owner, text)

    # print("Result is:")
    if any(word in text_list for word in jump_to_keywords):
        # print("jump_to_keywords ")
        row = f.find_one_row(text_list)
        e.jump_to_row(editor, row=row)
    elif any(word in text_list for word in copy_keywords):
        # print("copy_keywords")
        rows = f.find_rows(text_list)
        row_a = None
        row_b = None
        if rows[0]:
            row_a = rows[0]
        if rows[1]:
            row_b = rows[1]
        e.copy(editor, row_start=row_a, row_end=row_b)
    elif any(word in text_list for word in paste_keywords):
        # print("paste_keywords")
        row = f.find_one_row(text_list)
        e.paste(owner, editor, row=row)
    elif any(word in text_list for word in delete_keywords):
        # print("delete_keywords")
        rows = f.find_rows(text_list)
        row_a = None
        row_b = None
        try:
            row_a = rows[0]
            row_b = rows[1]
        except Exception:
            pass
        e.delete(owner, editor, row_start=row_a, row_end=row_b)
    elif any(word in text_list for word in if_keywords):
        # print("if_keywords")
        row = f.find_one_row(text_list)
        # print(f'if-row: {row}')
        e.insert_if_statement(editor, row=row)
    elif any(word in text_list for word in for_keywords):
        # print("for_keywords")
        row = f.find_one_row(text_list)
        e.insert_for(editor, row=row)
    elif any(word in text_list for word in while_keywords):
        # print("while_keywords ")
        row = f.find_one_row(text_list)
        e.insert_while(editor, row=row)
    elif any(word in text_list for word in switch_keywords):
        # print("switch_keywords")
        row = f.find_one_row(text_list)
        e.insert_match(editor, row=row)
    elif any(word in text_list for word in exception_keywords):
        # print("exception_keywords")
        row = f.find_one_row(text_list)
        e.insert_try(editor, row=row)
    elif any(word in text_list for word in endless_keywords):
        # print("endless_keywords")
        row = f.find_one_row(text_list)
        e.insert_infinite_loop(editor, row=row)
    elif any(word in text_list for word in timer_keywords):
        # print("timer_keywords")
        row = f.find_one_row(text_list)
        e.insert_timer(editor, row=row)
    elif any(word in text_list for word in thread_keywords):
        # print("thread_keywords")
        row = f.find_one_row(text_list)
        e.insert_thread(editor, row=row)
    elif any(word in text_list for word in print_keywords):
        # print("print_keywords")
        row = f.find_one_row(text_list)
        e.insert_print(editor, row=row)
    elif any(word in text_list for word in input_keywords):
        # print("input_keywords")
        row = f.find_one_row(text_list)
        e.insert_input(editor, row=row)
    else:
        print("Category Not Found")
        owner.create_error_info("Command not found.", color="orange", timer=2000)

# editor  = Text()
#
# if __name__ == '__main__':
#     classify_text(editor, "ein fabfrag in zeile 3.")
