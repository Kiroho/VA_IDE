from tkinter import *

import numpy as np
from timeit import default_timer as timer


def get_cursor_position(editor):
    position = editor.index(INSERT)
    print(f'Cursor Position: {position}')
    return position


def get_cursor_row(editor):
    current_row = editor.index(INSERT).split(".")[0]
    print(f'Cursor Row: {current_row}')
    return current_row


def get_selected_text(editor):
    selection = ""
    try:
        selection = editor.get(SEL_FIRST, SEL_LAST)
        print(f'Selected Text: {selection}')
    except TclError:
        print(f'Selected Text:')
    finally:
        return selection


def jump_to_row(editor, row=None):
    if row and isinstance(row, str):
        val = row.split(".")[0] + ".0"
        editor.mark_set("insert", val)
        print(f'Jumped To: {val}')
    else:
        print("Jumped To: Error. No Row Recognized.")


def copy(editor, row_start=None, row_end=None):
    if row_start and row_end:
        if isinstance(row_start, str) and isinstance(row_end, str):
            val_start = row_start.split(".")[0] + ".0"
            val_end = row_end.split(".")[0] + ".0"
            print(f'Rows to copy are: {val_start} to {val_end}')
            print(f'Copied text: {editor.get(val_start, val_end)}')
            editor.clipboard_append(editor.get(val_start + " linestart", val_end + " lineend"))
    else:
        print("Copied: No Rows selected. Copy marked instead.")
        if not get_selected_text(editor) == "":
            editor.clipboard_append(get_selected_text(editor))


def paste(editor, row=None):
    if row and isinstance(row, str):
        val = row.split(".")[0] + ".0"
    else:
        val = get_cursor_position(editor)
    try:
        print(f'Inserted at: {val}')
        editor.insert(val, editor.clipboard_get())
    except (TclError, Exception):
        print("Inserted at: Error, nothing to insert")


def delete(editor, row_start=None, row_end=None):
    if row_start and row_end:
        if isinstance(row_start, str) and isinstance(row_end, str):
            val_start = row_start.split(".")[0] + ".0"
            val_end = row_end.split(".")[0] + ".0"
            print(f'Rows to delete are: {val_start} to {val_end}')
            print(f'Deleted text: {editor.get(val_start, val_end)}')
            editor.delete(val_start + " linestart", val_end + " lineend")
    elif row_start:
        if isinstance(row_start, str):
            val_start = row_start.split(".")[0] + ".0"
            print(f'Rows to delete are: {val_start}')
            print(f'Deleted text: {editor.get(val_start)}')
            editor.delete(val_start + " linestart", val_start + " lineend")
    else:
        print("Deleted: No Rows selected. Delete marked instead.")
        if not get_selected_text(editor) == "":
            try:
                editor.delete(SEL_FIRST, SEL_LAST)
            except (TclError, Exception):
                print(f'Deleted Text:')


def check_tabs(editor, row):
    count = 0
    new_row = row.split(".")[0] + ".0"
    text = editor.get(new_row + " linestart", new_row + " lineend")
    text_array = np.fromiter(text, (np.str_, 1))
    # print(text_array)
    for i in text_array:
        if i == "\t":
            count += 1
            # print(f'output: {i}')
        else:
            break
    print(f'Tabs: {count}')
    return count


def get_previous_row(row):
    print(f'input Row: {row}')
    try:
        pre_row = row.split(".")[0] + ".0"
        pre_row = float(pre_row) - 1
        if pre_row < 1:
            pre_row = 1.0
        print(f'ounput Row: {pre_row}')
        return str(pre_row)
    except Exception:
        print(f'outnput Row: nope')
        return "1.0"


def remove_comment(text):
    text_array = np.fromiter(text, (np.str_, 1))
    start = timer()
    print(f'Text Array size: {text_array.size}')
    for c in range(len(text_array) - 1, -1, -1):
        if text_array[c] == "#":
            print(f'Is Comment: {c}')
            text_array = text_array[0:c]
            print(f'New Array: {text_array}')
            break
    print(f'time: {timer() - start}')
    return text_array


def check_for_function(text):
    text_array = remove_comment(text)
    for c in range(len(text_array) - 1, -1, -1):
        if text_array[c] == " " or text_array[c] == "\t":
            pass
        elif text_array[c] == ":":
            print("It's a Function")
            return True
        else:
            print("It's no Function")
            return False
    print("It's no Function")
    return False


def formate_function(editor, row, function_text):
    if row and isinstance(row, str):
        val = row.split(".")[0] + ".0"
        print("yay")
    else:
        val = get_cursor_position(editor)
        print(f'val: {val}')
    prev_row = get_previous_row(val)
    prev_row_text = editor.get(prev_row + " linestart", prev_row + " lineend")
    text = function_text + "\n\t"
    tabs_prev = check_tabs(editor, prev_row)
    print(f'tabs_prev: {tabs_prev}')
    for i in range(0, tabs_prev):
        text = "\t" + text + "\t"
    if check_for_function(prev_row_text):
        text = "\t" + text + "\t"
    text = "\n" + text
    return text


def insert_if_statement(editor, row=None, is_not="", x="x", y="", o="", then=True):
    val = adjust_row(editor, row)
    command = "if " + is_not + " " + x + o + y + ":"
    command = formate_function(editor, row, command)
    if then:
        else_command = "else:"
        else_command = formate_function(editor, row, else_command)
        command = command + else_command
    editor.insert(val + " lineend", command)


def insert_loop(editor, row=None, range_s="1", range_e=None, range_o=None, in_each=None):
    val = adjust_row(editor, row)

    command = "for i in range(" + range_s + "):"
    if in_each:
        in_each = 0  # for each loop
    elif range_e:
        range_e = 0  # in range zwei Attribute
        if range_o:
            range_o = 0  # in range drei Attribute

    command = formate_function(editor, row, command)
    editor.insert(val + " lineend", command)


def insert_while(editor, row=None, is_not="", x="x", y="y", o="=="):
    val = adjust_row(editor, row)
    command = "while " + is_not + " " + x + o + y + ":"
    command = formate_function(editor, row, command)
    editor.insert(val + " lineend", command)


def insert_match(editor, row=None, status="status", *args):
    val = adjust_row(editor, row)

    command = "match " + status + ":"
    command = formate_function(editor, row, command)
    for arg in args:
        case_command = "case " + arg + ":"
        case_command = formate_function(editor, row, case_command)
        command = command + case_command
    end_command = "case _:"
    end_command = formate_function(editor, row, command)
    command = command + end_command
    editor.insert(val + " lineend", command)


def insert_try(editor, row=None, excep="Exception"):
    val = adjust_row(editor, row)

    command = "try:"
    command = formate_function(editor, row, command)
    excep_command = "except " + excep + ":"
    excep_command = formate_function(editor, row, excep_command)
    command = command + excep_command
    final_command = "finally:"
    final_command = formate_function(editor, row, final_command)
    command = command + final_command
    editor.insert(val + " lineend", command)


def insert_infinite_loop(editor, row=None, excep="Exception"):
    val = adjust_row(editor, row)
    command = "while True:"
    command = formate_function(editor, row, command)
    editor.insert(val + " lineend", command)


def insert_print(editor, row=None, text="Hello World"):
    val = adjust_row(editor, row)
    command = "print(\"" + text + "\")"
    command = formate_function(editor, row, command)
    editor.insert(val + " lineend", command)

def insert_input(editor, row=None, variable="input_val", text="Input:"):
    val = adjust_row(editor, row)
    command = variable + " = input(\"" + text + "\")"
    command = formate_function(editor, row, command)
    editor.insert(val + " lineend", command)



def adjust_row(editor, row):    #Testen
    if row and isinstance(row, str):
        val = row.split(".")[0] + ".0"
        print("yay")
    else:
        val = get_cursor_position(editor)
        print(f'val: {val}')
    return val
