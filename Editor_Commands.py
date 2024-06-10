from tkinter import *

import numpy as np
from random import randrange


def get_cursor_position(editor):
    position = editor.index(INSERT)
    # print(f'Cursor Position: {position}')
    return position


def get_cursor_row(editor):
    current_row = editor.index(INSERT).split(".")[0]
    # print(f'Cursor Row: {current_row}')
    return current_row


def get_selected_text(editor):
    selection = ""
    try:
        selection = editor.get(SEL_FIRST, SEL_LAST)
        # print(f'Selected Text: {selection}')
    except TclError:
        # print(f'Selected Text:')
        pass
    finally:
        return selection


def check_tabs(editor, row):
    count = 0
    new_row = row.split(".")[0] + ".0"
    text = editor.get(new_row + " linestart", new_row + " lineend")
    text_array = np.fromiter(text, (np.str_, 1))
    for i in text_array:
        if i == "\t":
            count += 1
        else:
            break
    # print(f'Tabs: {count}')
    return count


def get_relative_row(editor, row, offset=-1):
    try:
        new_row = row.split(".")[0] + ".0"
        new_row = float(new_row) + offset
        if new_row < 1:
            new_row = 1.0
            print("it's before 1")
        total_rows = float(editor.index('end-1c').split('.')[0])
        if new_row > total_rows:
            new_row = total_rows
            print("it's beyond END")
        print(f'its: {new_row}')
        return str(new_row)
    except Exception:
        return "0.0"


def remove_comment(text):
    text_array = np.fromiter(text, (np.str_, 1))
    for c in range(len(text_array) - 1, -1, -1):
        if text_array[c] == "#":
            # print(f'Is Comment: {c}')
            text_array = text_array[0:c]
            # print(f'New Array: {text_array}')
            break
    return text_array


def check_for_function(text):
    text_array = remove_comment(text)
    for c in range(len(text_array) - 1, -1, -1):
        if text_array[c] == " " or text_array[c] == "\t":
            pass
        elif text_array[c] == ":":
            # print("It's a Function")
            return True
        else:
            # print("It's no Function")
            return False
    # print("It's no Function")
    return False


def formate_function(editor, row, function_text):
    val = adjust_row(editor, row=row)

    prev_row = get_relative_row(editor, val)
    prev_row_text = editor.get(prev_row + " linestart", prev_row + " lineend")
    text = function_text + "\n\t"
    tabs_prev = check_tabs(editor, prev_row)
    for i in range(0, tabs_prev):
        text = "\t" + text + "\t"
    if check_for_function(prev_row_text):
        text = "\t" + text + "\t"
    text = "\n" + text
    return text


def formate_non_function(editor, row, text):
    val = adjust_row(editor, row=row)

    prev_row = get_relative_row(editor, val)
    prev_row_text = editor.get(prev_row + " linestart", prev_row + " lineend")
    text = text
    tabs_prev = check_tabs(editor, prev_row)
    for i in range(0, tabs_prev):
        text = "\t" + text
    if check_for_function(prev_row_text):
        text = "\t" + text
    text = "\n" + text
    return text


# Editor Commands_________________________

def jump_to_row(editor, owner, row=None):
    if row and isinstance(row, str):
        val = row.split(".")[0] + ".0"
        editor.mark_set("insert", val)
        # print(f'Jumped To: {val}')
        owner.create_error_info("Command done", color="light green", timer=1000)
    else:
        # print("Jumped To: Error. No Row Recognized.")
        owner.create_error_info("No Row Recognized.", color="orange", timer=2000)


def copy(editor, owner, row_start=None, row_end=None):
    if row_start and row_end:
        if isinstance(row_start, str) and isinstance(row_end, str):
            val_start = row_start.split(".")[0] + ".0"
            val_end = row_end.split(".")[0] + ".0"
            # print(f'Rows to copy are: {val_start} to {val_end}')
            # print(f'Copied text: {editor.get(val_start, val_end)}')
            editor.clipboard_append(editor.get(val_start + " linestart", val_end + " lineend"))
    else:
        # print("Copied: No Rows selected. Copy marked instead.")
        if not get_selected_text(editor) == "":
            editor.clipboard_append(get_selected_text(editor))
    owner.create_error_info("Command done", color="light green", timer=1000)


def paste(owner, editor, row=None):
    if row and isinstance(row, str):
        val = row.split(".")[0] + ".0"
    else:
        val = get_cursor_position(editor)
    try:
        # print(f'Inserted at: {val}')
        editor.insert(val, editor.clipboard_get())
        owner.create_error_info("Command done", color="light green", timer=1000)
    except (TclError, Exception):
        # print("Inserted at: Error, nothing to insert")
        owner.create_error_info("Insert not possible. Clipboard is empty", color="orange", timer=2000)
        pass


def delete(owner, editor, row_start=None, row_end=None):
    if row_start and row_end:
        if isinstance(row_start, str) and isinstance(row_end, str):
            val_start = row_start.split(".")[0] + ".0"
            val_end = row_end.split(".")[0] + ".0"
            # print(f'Rows to delete are: {val_start} to {val_end}')
            # print(f'Deleted text: {editor.get(val_start, val_end)}')
            editor.delete(val_start + " linestart", val_end + " lineend")
            owner.create_error_info("Command done", color="light green", timer=1000)
            return
    if row_start:
        if isinstance(row_start, str):
            val_start = row_start.split(".")[0] + ".0"
            # print(f'Rows to delete are: {val_start}')
            # print(f'Deleted text: {editor.get(val_start)}')
            editor.delete(val_start + " linestart", val_start + " lineend")
            owner.create_error_info("Command done", color="light green", timer=1000)
            return
    # print("Deleted: No Rows selected. Delete marked instead.")
    if not get_selected_text(editor) == "":
        try:
            editor.delete(SEL_FIRST, SEL_LAST)
        except (TclError, Exception):
            # print(f'Deleted Text:')
            owner.create_error_info("Nothing marked for Deletion.", color="orange")
            pass


def insert_if_statement(editor, owner, row=None, is_not=False, x=None, y=None, o=None, then=True):
    val = adjust_row(editor, row)
    cursor = True
    if x or y or o:
        cursor = False
        no = ""
        if is_not:
            no = "not "
        if not x:
            x = "x"
        if not y:
            y = "y"
        if not o:
            o = "=="
        command = "if " + no + x + " " + o + " " + y + ":"
    else:
        command = "if  :"

    command = formate_function(editor, row, command)
    if then:
        else_command = "else:"
        else_command = formate_function(editor, row, else_command)
        command = command + else_command
    editor.insert(val + " lineend", command)
    if cursor:
        set_cursor_position(editor, command=command, row=val, offset=2)

    owner.create_error_info("Command done", color="light green", timer=1000)


def insert_for(editor, owner, row=None, range_s="1", range_e=None, range_o=None, in_each=None):
    val = adjust_row(editor, row)

    command = "for i in range(  ):"
    if in_each:
        command = "for i in " + in_each + ":"
    # elif range_e:
    #     command = "for i in range(" + range_s + ", " + range_e + "):"
    #     if range_o:
    #         command = "for i in range(" + range_s + ", " + range_e + ", " + range_o + "):"
    command = formate_function(editor, row, command)
    editor.insert(val + " lineend", command)
    set_cursor_position(editor, command=command, row=val, offset=3)
    owner.create_error_info("Command done", color="light green", timer=1000)


def insert_while(editor, owner, row=None, is_not=False, x=None, y=None, o=None):
    val = adjust_row(editor, row)
    cursor = True
    if x or y or o:
        cursor = False
        no = ""
        if is_not:
            no = "not "
        if not x:
            x = "x"
        if not y:
            y = "y"
        if not o:
            o = "=="
        command = "while " + no + x + " " + o + " " + y + ":"
    else:
        command = "while  :"
    command = formate_function(editor, row, command)
    editor.insert(val + " lineend", command)
    if cursor:
        set_cursor_position(editor, command=command, row=val, offset=2)

    owner.create_error_info("Command done", color="light green", timer=1000)


def insert_match(editor, owner, *args, row=None, status="status"):
    val = adjust_row(editor, row)

    command = "match " + status + " :"
    command = formate_function(editor, row, command)
    for arg in args:
        case_command = "case " + arg + ":"
        case_command = formate_function(editor, row, case_command)
        command = command + case_command
    end_command = "\tcase _:"
    end_command = formate_function(editor, row, end_command)
    command = command + end_command
    editor.insert(val + " lineend", command)
    owner.create_error_info("Command done", color="light green", timer=1000)


def insert_try(editor, owner, row=None, excep="Exception", final=False):
    val = adjust_row(editor, row)

    command = "try:"
    command = formate_function(editor, row, command)
    excep_command = "except " + excep + ":"
    excep_command = formate_function(editor, row, excep_command)
    command = command + excep_command
    if final:
        final_command = "finally:"
        final_command = formate_function(editor, row, final_command)
        command = command + final_command
    editor.insert(val + " lineend", command)
    owner.create_error_info("Command done", color="light green", timer=1000)


def insert_infinite_loop(editor, owner, row=None, ):
    val = adjust_row(editor, row)
    command = "while True:"
    command = formate_function(editor, row, command)
    editor.insert(val + " lineend", command)
    owner.create_error_info("Command done", color="light green", timer=1000)


def insert_print(editor, owner, row=None, text=""):
    val = adjust_row(editor, row)
    command = "print(\"" + text + "\")"
    command = formate_non_function(editor, row, command)
    editor.insert(val + " lineend", command)
    set_cursor_position(editor, command=command, row=val, offset=2, filter=")")
    owner.create_error_info("Command done", color="light green", timer=1000)


def insert_input(editor, owner, row=None, variable="input_val", text="Input: "):
    val = adjust_row(editor, row)
    command = variable + " = input(\"" + text + "\")"
    command = formate_non_function(editor, row, command)
    editor.insert(val + " lineend", command)
    set_cursor_position(editor, command=command, row=val, offset=2, filter=")")
    owner.create_error_info("Command done", color="light green", timer=1000)


def insert_timer(editor, owner, row=None):
    if not check_import(editor, "from timeit import default_timer as timer"):
        editor.insert("0.0", "from timeit import default_timer as timer\n")
    val = adjust_row(editor, row)
    number = randrange(1, 1000)
    command = "my_timer_" + str(number) + " = timer()\t\t#starts the timer"
    command = formate_non_function(editor, row, command)
    command_2 = "print(f\'time: {timer() - my_timer_" + str(number) + "}\')\t\t#stops the timer and prints the time"
    command_2 = formate_non_function(editor, row, command_2)
    command = command + command_2
    editor.insert(val + " lineend", command)
    owner.create_error_info("Command done", color="light green", timer=1000)


def insert_thread(editor, owner, row=None, target=""):
    if not check_import(editor, "import threading"):
        editor.insert("0.0", "import threading\n")
    val = adjust_row(editor, row)
    number = randrange(1, 1000)

    command = "my_thread_" + str(number) + " = threading.Thread(target=" + target + ")\t\t#initializes the thread"
    command = formate_non_function(editor, row, command)
    command_2 = "my_thread_" + str(
        number) + ".daemon = True\t\t#kills the thread automatically once the main program get closed"
    command_2 = formate_non_function(editor, row, command_2)
    command_3 = "my_thread_" + str(number) + ".start()\t\t#starts the thread"
    command_3 = formate_non_function(editor, row, command_3)
    command = command + command_2 + command_3
    editor.insert(val + " lineend", command)
    set_cursor_position(editor, command=command, row=val, offset=1, filter=")")
    owner.create_error_info("Command done", color="light green", timer=1000)


#internal functions________________________________________

def set_cursor_position(editor, command, row, offset, filter=":"):
    cursor_row = str(float(row) + 1)
    cursor_row = cursor_row.split(".")[0]
    cursor_pos = command.split(filter)[0]
    cursor_pos = str(len(cursor_pos) - offset)
    print(len(command))
    print(cursor_pos)
    editor.mark_set("insert", cursor_row + "." + cursor_pos)


def check_import(editor, wanted_import):
    text = get_imports(editor)
    for imports in text:
        if wanted_import in imports:
            # print(text)
            return True
    return False


def get_imports(editor):
    imports = []
    for row in editor.get(0.0, END).split("\n"):
        row = row.replace("\t", "")
        if row.startswith("import") or row.startswith("from"):
            imports.append(row)
    return imports


def adjust_row(editor, row):
    # print("inside adjust_row")
    # print(f'row is{row}')
    try:
        val = row.split(".")[0] + ".0"
    except Exception:
        val = get_cursor_position(editor)
        pass
    return val
