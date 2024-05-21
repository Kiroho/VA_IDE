from timeit import default_timer as timer
from nltk.stem.snowball import SnowballStemmer
import re

jump_to_keywords = ['navigi', 'wegehr', 'kavigi', 'verrigi', 'regi', 'karri', 'spring', 'bring', 'dringend', 'ring', 'kling']

copy_keywords = ['kopi', 'pir', 'pier', 'vier']

paste_keywords = ['einfug', 'klug', 'zug', 'schug', 'reinfug', 'einfuhr', 'fug']

delete_keywords = ['schutt', 'schutz', 'losch', 'entfern', 'fern', 'fernezeil', 'fernzeil']

if_keywords = ['ifanweis', 'if', 'anweis', 'abfrag', 'hilfeanweis', 'elfanweis', 'stiftanweis', 'veranweis', 'ifoption', 'tiefabfrag', 'ifabfragezeil', 'abfragezeil']

for_keywords = ['vorschleif', 'vorschlaf', 'vorschneif', 'vorschrift', 'bohrschleif', 'for']

while_keywords = ['weilschleif', 'wildschleif', 'waldschleif', 'whileschleif', 'wireschraub', 'weilschlauf', 'wireschleif', 'waltschleif', 'while', 'forschleife']

switch_keywords = ['switch', 'witch', 'wich', 'hitch', 'match', 'cas']

exception_keywords = ['exception', 'ausnahm', 'final', 'expression']

endless_keywords = ['endoschleif', 'endlosschleif', 'endlos', 'infinity', 'infinity loop']

timer_keywords = ['tim', 'daima']

thread_keywords = ['thread', 'wett', 'thwett', 'sweat']

print_keywords = ['print', 'prund', 'trint', 'kind', 'printbefehl']

input_keywords = ['input', 'eingab']

zeile_keywords = ['zeil', 'teil', 'silo', 'seil', 'zeit', 'zell', 'sail']

snowball = SnowballStemmer("german")


def preprocess_text(text):
    #lowercasing
    text = text.lower()
    # print(text)
    #remove special chars
    regex = r"(?<!\d)[.,;:!?_\-\(\)\"\'](?!\d)"
    text = re.sub(regex, "", text, 0)
    # print(text)
    #tokenize
    text_list = text.split(" ")
    #stemming
    text_list = [snowball.stem(word) for word in text_list]
    print(text_list)
    return text_list

def classify_text(text):
    text_list = preprocess_text(text)

    print("Result is:")
    if any(word in text_list for word in jump_to_keywords):
        print("jump_to_keywords ")
    elif any(word in text_list for word in copy_keywords):
        print("copy_keywords")
    elif any(word in text_list for word in paste_keywords):
        print("paste_keywords")
    elif any(word in text_list for word in delete_keywords):
        print("delete_keywords")
    elif any(word in text_list for word in if_keywords):
        print("if_keywords")
    elif any(word in text_list for word in for_keywords):
        print("for_keywords")
    elif any(word in text_list for word in while_keywords):
        print("while_keywords ")
    elif any(word in text_list for word in switch_keywords):
        print("switch_keywords")
    elif any(word in text_list for word in exception_keywords):
        print("exception_keywords")
    elif any(word in text_list for word in endless_keywords):
        print("endless_keywords")
    elif any(word in text_list for word in timer_keywords):
        print("timer_keywords")
    elif any(word in text_list for word in thread_keywords):
        print("thread_keywords")
    elif any(word in text_list for word in print_keywords):
        print("print_keywords")
    elif any(word in text_list for word in input_keywords):
        print("input_keywords")
    else:
        print("Not Found")




























