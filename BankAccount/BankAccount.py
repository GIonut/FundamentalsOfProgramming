import datetime
import re
from get_set import get_day, get_trans, get_value, get_type, get_descr, set_value
from functions import create_storage, create_df_storage, add, insert, remove, remove_to, remove_type, replace, write, type_sum, sum_type, max_tr, filter_type, filter, add_stack, undo
from tests import all_tests
import copy
################################################################################       
#********************************* VALIDATION *********************************
################################################################################

def validate_cmd(cmd):
    commands = { 1:"add", 2:"insert", 3:"remove", 4:"replace", 5:"list", 6: "exit", 7:"sum", 8:"max", 9:"filter", 10:"undo" }
    while True:
        if(cmd[0] == "print" or cmd[0] == "add" or cmd[0] == "insert" or cmd[0] == "remove" or cmd[0] == "replace" or cmd[0] == "list" or cmd[0] == "default" or cmd[0] == "exit" or cmd[0] == "sum" or cmd[0] == "max" or cmd[0] == "filter" or cmd[0] == "undo"):
            break
        else:
            print("invalid command!\n")
            cmd = ui_read_command()
            
    if(cmd[0] == "add"):
        cmd = validate_add(cmd)
    elif(cmd[0] == "insert"):
        cmd = validate_insert(cmd)
    elif(cmd[0] == "remove"):
        cmd = validate_remove(cmd)
    elif(cmd[0] == "replace"):
        cmd = validate_replace(cmd)
    elif(cmd[0] == "list"):
        cmd = validate_list(cmd)
    elif(cmd[0] == "default"):
        pass
    elif(cmd[0] == "exit"):
        pass
    elif(cmd[0] == "sum"):
        cmd = validate_sum(cmd)
    elif(cmd[0] == "max"):
        cmd = validate_max(cmd)
    elif(cmd[0] == "filter"):
        cmd = validate_filter(cmd)
    #elif(cmd[0] == "undo"):
        #cmd = validate_undo(cmd)
    return cmd

def validate_add(cmd):
    while True:
        try:
            int(cmd[1])
            if(len(cmd) != 4 or (cmd[2] != "in" and cmd[2] != "out") ):
                raise Exception
            return cmd
        except:
            print("add command must be : add <value> <type> <description>")
            cmd = ui_read_command()
                
def validate_insert(cmd):
     while True:
        try:
            int(cmd[1])
            int(cmd[2])
            if(len(cmd)!= 5 or int(cmd[1])<0 or int(cmd[1])>30 or (cmd[3] != "in" and cmd[3] != "out")):
                raise Exception
            return cmd
        except:
                print("insert command must be : insert <day> <value> <type> <description>")
                cmd = ui_read_command()

def validate_remove(cmd):
    l = len(cmd)
    while True:
        try:
            if(l != 2 and l != 4):
                raise Exception
            break
        except:
            print("remove command must be : remove <day> or\n"
              "                         remove <type> or\n"
              "                         remove <start day> to <end day> or")
            cmd = ui_read_command()
            l = len(cmd)
    if(l == 2):
        while True:
            try:
                if(not(cmd[1] == "in" or cmd[1] == "out")):
                    int(cmd[1])
                    if(int(cmd[1])<0 or int(cmd[1])>30):
                        raise Exception
                return cmd
            except Exception:
                print("remove command must be : remove <day> or\n"
                      "                         remove <type> or\n"
                      "                         remove <start day> to <end day> or")
                cmd = ui_read_command()
    elif(l == 4):
        while True:
            try:
                if(not(cmd[2] == "to" and int(cmd[1]) and int(cmd[1])>=0 and int(cmd[1])<=30 and int(cmd[3]) and int(cmd[3])>=0 and int(cmd[3])<=30)):
                    raise Exception
                return cmd
            except Exception:
                print("remove command must be : remove <day> or\n"
                      "                         remove <type> or\n"
                      "                         remove <start day> to <end day> or")
                cmd = ui_read_command()
        
def validate_replace(cmd):
    while True:
        try:
            int(cmd[1])
            if(not(len(cmd) == 6 and int(cmd[1])>=0 and int(cmd[1])<=30 and (cmd[2] == "in" or cmd[2] == "out") and cmd[4] == "with" and int(cmd[5]))):
                raise Exception
            return cmd
        except Exception:
            print("replace command must be : replace <day> <type> <description> with <value>")
            cmd = ui_read_command()

def validate_list(cmd):
    l = len(cmd)
    if(l == 1):
        return cmd
    elif(l == 2):
        while True:
            try:
                if(not(cmd[1] == "in" or cmd[1] == "out")):
                    raise Exception
                return cmd
            except Exception:
                print("list command must be : list or\n"
                      "                       list <type> or\n"
                      "                       list [ < | = | > ] <value> or\n"
                      "                       list balance <day>")
                cmd = ui_read_command()
    elif(l == 3 and cmd[1] == "balance"):
        while True:
            try:
                int(cmd[2])
                if(not(int(cmd[2])>=0 and int(cmd[2])<=30)):
                    raise Exception
                return cmd
            except Exception:
                print("list command must be : list or\n"
                      "                       list <type> or\n"
                      "                       list [ < | = | > ] <value> or\n"
                      "                       list balance <day>")
                cmd = ui_read_command()
    elif(l == 3):
        while True:
            try:
                int(cmd[2])
                if(not((cmd[1] == "<" or cmd[1] == ">" or cmd[1] == "="))):
                    raise Exception
                return cmd       
            except Exception:
                print("list command must be : list or\n"
                      "                       list <type> or\n"
                      "                       list [ < | = | > ] <value> or\n"
                      "                       list balance <day>")
                cmd = ui_read_command()
            
def validate_sum(cmd):
    while True:
        try:
            if(not(len(cmd) == 2 and (cmd[1] == "in" or cmd[1] == "out"))):
                raise Exception
            return cmd
        except Exception:
            print("sum command must be : sum <type>")
            cmd = ui_read_command()

def validate_max(cmd):
    while True:
        try:
            if(not(len(cmd) == 3 and (cmd[1] == "out" or cmd[1] == "in") and int(cmd[2]) and int(cmd[2]) >= 0 and int(cmd[2]) <= 30)):
                raise Exception
            return cmd
        except Exception:
            print("max command must be : max <type> <day>")
            cmd = ui_read_command()

def validate_filter(cmd):
    l = len(cmd)
    while True:
        try:
            if(l != 2 and l != 3):
                raise Exception
            break
        except Exception:
            print("filter command must be : filter <type> or\n"
                  "                         filter <type> <value>")
            cmd = ui_read_command()
            l = len(cmd)
    if(l == 2):
        while True:
            try:
                if(not(cmd[1] == "in" or cmd[1] == "out")):
                    raise Exception
                return cmd
            except Exception:
                print("filter command must be : filter <type> or\n"
                      "                         filter <type> <value>")
                cmd = ui_read_command()
    if(l == 3):
        while True:
            try:
                if(not((cmd[1] == "out" or cmd[1] == "in") and int(cmd[2]))):
                    raise Exception
                return cmd
            except Exception:
                print("filter command must be : filter <type> or\n"
                      "                         filter <type> <value>")
                cmd = ui_read_command()
        
################################################################################                                        
#************************************* ui_functions *****************************
################################################################################
    
def ui_read_command():
    comm = input("get command: ")
    cmd = re.split("\s", comm)
    return cmd

def ui_list_balance(storage, day):
    in_tr = type_sum(storage, day, "in")
    out_tr = type_sum(storage, day, "out")
    print(in_tr - out_tr)

def ui_list_less_value(storage, value):
    for i in range(31):
        ok = 1
        for j in range(len(get_day(storage, i))):
               if(get_value(storage, i, j) < value):
                   if(ok):
                       print("\nday ", i, "\n---------------------------------------------------")
                       ok = 0
                   print(write(storage, i, j))
        if(not ok):
            print("\n")

def ui_list_more_value(storage, value):
    for i in range(31):
        ok = 1
        for j in range(len(get_day(storage, i))):
               if(get_value(storage, i, j) > value):
                   if(ok):
                       print("\nday ", i, "\n---------------------------------------------------")
                       ok = 0
                   print(write(storage, i, j))
        if(not ok):
            print("\n")

def ui_list_equal_value(storage, value):
    for i in range(31):
        ok = 1
        for j in range(len(get_day(storage, i))):
               if(get_value(storage, i, j) == value):
                   if(ok):
                       print("\nday ", i, "\n---------------------------------------------------")
                       ok = 0
                   print(write(storage, i, j))
        if(not ok):
            print("\n")
            
def ui_list(storage):
    for i in range(31):
        ok = 1
        for j in range(len(get_day(storage, i))):
              if(ok):
                   print("\nday ", i, "\n---------------------------------------------------")
                   ok = 0
              print(write(storage, i, j))
        if(not ok):
            print("\n")

def ui_list_type(storage, tr_type):
    for i in range(31):
        ok = 1
        for j in range(len(get_day(storage, i))):
               if(get_type(storage, i ,j) == tr_type):
                   if(ok):
                       print("\nday ", i, "\n---------------------------------------------------")
                       ok = 0
                   print(write(storage, i, j))
        if(not ok):
            print("\n")

def ui_list_value(storage, sign, value):
     if(sign == "<"):
         ui_list_less_value(storage, value)
     elif(sign == ">"):
         ui_list_more_value(storage, value)
     else:
         ui_list_equal_value(storage, value)         

def ui_add(storage, cmd):
    value = int(cmd[1])
    tr_type = cmd[2]
    description = cmd[3]
    add(storage, value, tr_type, description)

def ui_insert(storage, cmd):
    day = int(cmd[1])
    value = int(cmd[2])
    tr_type = cmd[3]
    description = cmd[4]
    insert(storage, day, value, tr_type, description)
            
def ui_menu():
    cmd = ui_read_command()
    cmd = validate_cmd(cmd)
    if(cmd[0] == "add"):
        ui_add(storage, cmd)
        add_stack(stack, storage)
        ui_menu()
    if(cmd[0] == "insert"):
        ui_insert(storage, cmd)
        add_stack(stack, storage)
        ui_menu()
    if(cmd[0] == "remove"):
        if(len(cmd) == 4):
                remove_to(storage, int(cmd[1]), int(cmd[3]))
        elif(cmd[1] == "in" or cmd[1] == "out"):
             remove_type(storage, cmd[1])
        else:
            remove(storage, int(cmd[1]))
        add_stack(stack, storage)
        ui_menu()
    if(cmd[0] == "replace"):
        replace(storage, cmd)
        add_stack(stack, storage)
        ui_menu()
    if(cmd[0] == "default"):
        create_df_storage(storage)
        add_stack(stack, storage)
        ui_menu()
    if(cmd[0] == "list"):
        if(len(cmd)==1):
            ui_list(storage)
        elif(len(cmd) == 2):
            ui_list_type(storage, cmd[1])
        elif(cmd[1] == "balance"):
            ui_list_balance(storage, int(cmd[2]))
        else:
            ui_list_value(storage, cmd[1], int(cmd[2]))
        ui_menu()
    if(cmd[0] == "exit"):
        exit()
    if(cmd[0] == "sum"):
        sum_type(storage, cmd[1])
        ui_menu()
    if(cmd[0] == "max"):
        max_tr(storage, cmd[1], int(cmd[2]))
        ui_menu()
    if(cmd[0] == "filter"):
        l = len(cmd)
        if(l == 2):
            filter_type(storage, cmd[1])
            ui_list(storage)
        if(l == 3):
            filter(storage, cmd[1], int(cmd[2]))
            ui_list(storage)
        add_stack(stack, storage)
        ui_menu()
    if(cmd[0] == "undo"):
        storage.clear()
        storage.update(undo(stack,storage))
        ui_menu()





################################################################################       
#********************************* menu_based_app *********************************
################################################################################

def ui_read_comm(menu):
    comm = str(input("get command: "))
    cmd = re.split("\s", comm)
    return cmd
          
def ui_menu1():
    print("\nTo exit the application input 9\n"
          "To add a new transaction in the current day input 0\n"
          "To insert a new transaction in a certain day input  1\n"
          "To remove transactions input 2\n"
          "To replace a transaction input 3\n"
          "To list the transactions input 4\n"
          "To sum the transaction considering their type input 5\n"
          "To get the maximum value of a transaction considering its type input 6\n"
          "To undo an operation input 7\n"
          "To get a default account input 8\n")
    menu = int(input())
    cmd = ui_read_comm(menu)
    cmd = validate_cmd(cmd)
    if(cmd[0] == "add"):
        ui_add(storage, cmd)
        add_stack(stack, storage)
        ui_menu1()
    if(cmd[0] == "insert"):
        ui_insert(storage, cmd)
        add_stack(stack, storage)
        ui_menu1()
    if(cmd[0] == "remove"):
        if(len(cmd) == 4):
                remove_to(storage, int(cmd[1]), int(cmd[3]))
        elif(cmd[1] == "in" or cmd[1] == "out"):
             remove_type(storage, cmd[1])
        else:
            remove(storage, int(cmd[1]))
        add_stack(stack, storage)
        ui_menu1()
    if(cmd[0] == "replace"):
        replace(storage, cmd)
        add_stack(stack, storage)
        ui_menu()
    if(cmd[0] == "default"):
        create_df_storage(storage)
        add_stack(stack, storage)
        ui_menu1()
    if(cmd[0] == "list"):
        if(len(cmd)==1):
            ui_list(storage)
        elif(len(cmd) == 2):
            ui_list_type(storage, cmd[1])
        elif(cmd[1] == "balance"):
            ui_list_balance(storage, int(cmd[2]))
        else:
            ui_list_value(storage, cmd[1], int(cmd[2]))
        ui_menu1()
    if(cmd[0] == "exit"):
        exit()
    if(cmd[0] == "sum"):
        sum_type(storage, cmd[1])
        ui_menu1()
    if(cmd[0] == "max"):
        max_tr(storage, cmd[1], int(cmd[2]))
        ui_menu()
    if(cmd[0] == "filter"):
        l = len(cmd)
        if(l == 2):
            filter_type(storage, cmd[1])
            ui_list(storage)
        if(l == 3):
            filter(storage, cmd[1], int(cmd[2]))
            ui_list(storage)
        add_stack(stack, storage)
        ui_menu1()
    if(cmd[0] == "undo"):
        storage.clear()
        storage.update(undo(stack,storage))
        ui_menu1()

################################################################################       
#********************************* main_function *********************************
################################################################################

if __name__ == "__main__":
    stack = []
    storage = {}
    create_storage(storage)
    stack.append(copy.deepcopy(storage))
    all_tests()
    a = int(input("continue with menu interface?\nPress 1 for 'yes' or 0 for 'no'\n"))
    if( a == 0):
        ui_menu()
    else:
        ui_menu1()
    
