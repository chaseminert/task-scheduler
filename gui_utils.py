from datetime import datetime, timedelta
from task_scheduler import Task
from task_scheduler import TaskScheduler

import customtkinter as ctk
import tkinter as tk
import messages
import globals

BUTTON_FONT = ("Arial", 12)
BUTTON_FONT_UNDERLINE = ("Arial", 12, "underline")

TEXT_FONT = ("Roboto", 14)
TEXT_FONT_BOLD = ("Roboto", 14, "bold")
NO_TASKS_FONT = ("Roboto", 30, "bold")

TITLE_FONT = ("Arial", 45, "bold")


def update_gui(main_frame, root, task_scheduler, sort=True):
    if sort:
        task_scheduler.sort_tasks()

    # Clear all existing frames in main_frame
    main_frame: ctk.CTkFrame
    for widget in main_frame.winfo_children():
        widget.grid_forget()

    main_frame.grid()

    # Redraw items
    display_tasks(root, main_frame, task_scheduler)


def on_checkbox_click(checkbox_var, task_scheduler: TaskScheduler, task: Task):
    if checkbox_var.get() == 1:
        # print("Checkbox is checked.")
        task.set_as_complete()

    else:
        task.set_as_incomplete()
    task_scheduler.save_to_file()


def on_hover(widget, enter=True):
    if enter:
        widget.configure(font=BUTTON_FONT_UNDERLINE)
        widget.configure(fg_color="gray14")
    else:
        widget.configure(font=BUTTON_FONT)
        widget.configure(fg_color="transparent")


def on_delete(main_frame, root, task_scheduler: TaskScheduler, task: Task):
    task_scheduler.delete_task_obj(task)
    task_scheduler.save_to_file()
    update_gui(main_frame, root, task_scheduler)


def display_header_buttons(root, all_tasks_frame, task_scheduler: TaskScheduler):
    # all_tasks_frame.grid_rowconfigure(1, weight=1)

    header_buttons_frame = ctk.CTkFrame(root, fg_color="transparent", width=633, height=57)
    header_buttons_frame.grid(row=1, column=0, pady=(40, 20), padx=(5, 0))
    header_buttons_frame.grid_propagate(False)

    header_buttons_frame.columnconfigure(0, weight=1)
    header_buttons_frame.columnconfigure(1, weight=1)
    header_buttons_frame.columnconfigure(2, weight=1)

    new_task_button = ctk.CTkButton(header_buttons_frame, text="New Task", width=160,
                                    command=lambda: new_task(all_tasks_frame, task_scheduler, root), text_color="white",
                                    font=TEXT_FONT_BOLD)
    new_task_button.grid(row=1, column=0, sticky='WS')

    options = ["Name", "Due Date", "Order Added"]

    menu_frame = ctk.CTkFrame(header_buttons_frame, fg_color="transparent")
    menu_frame.grid(row=1, column=1)

    sort_menu = globals.sort_menu = ctk.CTkOptionMenu(menu_frame, values=options,
                                                      command=lambda option: change_sort(option, all_tasks_frame, root,
                                                                                         task_scheduler),
                                                      text_color="white", anchor="center", width=160,
                                                      font=TEXT_FONT_BOLD)
    task_scheduler.sort_tasks()
    sort_menu.set(task_scheduler.get_sort_type)
    sort_menu.grid(row=1, column=0)

    sort_label = ctk.CTkLabel(menu_frame, text="Sort By")
    sort_label.grid(row=0, column=0, padx=(0, 25))

    reverse_label = ctk.CTkLabel(menu_frame, text="Reverse")
    reverse_label.grid(row=0, column=1, padx=(0, 0))

    checkbox_wrapper = ctk.CTkFrame(menu_frame, width=24, height=24, fg_color="transparent")
    checkbox_wrapper.grid_propagate(False)
    checkbox_wrapper.grid(row=1, column=1, padx=(10, 0), sticky='W')

    reverse_val = task_scheduler.is_reverse

    reverse_checkbox = globals.reverse_checkbox = ctk.CTkCheckBox(checkbox_wrapper, width=24, text="",
                                                                  command=lambda: reverse_tasks(all_tasks_frame, root,
                                                                                                task_scheduler),
                                                                  text_color_disabled="white")
    if reverse_val:
        reverse_checkbox.select()
    reverse_checkbox.grid(row=0, column=0, padx=0)

    delete_complete_button = ctk.CTkButton(header_buttons_frame, text="Delete Completed Tasks", width=160,
                                           command=lambda: delete_completed_tasks(all_tasks_frame, root,
                                                                                  task_scheduler),
                                           text_color="white", font=TEXT_FONT_BOLD)
    delete_complete_button.grid(row=1, column=2, sticky="ES")


def get_due_date_color(date):
    if date == "":
        return "red"

    # Get today's date without the time component
    today = datetime.now().date()

    # Construct the date for the given mm/dd for the current year without the time component
    target_date = datetime.strptime(f"{date}/{today.year}", "%m/%d/%Y").date()

    # Check if the target date is today or 1 day after
    if today == target_date or today + timedelta(days=1) == target_date:
        return "yellow"
    elif today < target_date:
        return "lime green"
    else:
        return "red"


def disable_widget(*args):
    for arg in args:
        arg.configure(state=tk.DISABLED)


def enable_widget(*args, task_scheduler):
    if task_scheduler.can_enable_widgets():
        for arg in args:
            arg.configure(state=tk.NORMAL)


def display_tasks(root, all_tasks_frame, task_scheduler: TaskScheduler):
    if task_scheduler.num_tasks == 0:
        no_tasks = globals.no_tasks_label = ctk.CTkLabel(all_tasks_frame, text="No Tasks", width=632,
                                                         font=NO_TASKS_FONT, bg_color="transparent")
        no_tasks.grid(row=2, column=0, columnspan=100, pady=30, padx=15)
    for index, task in enumerate(task_scheduler, start=2):
        display_task(root, all_tasks_frame, task_scheduler, task, index)


def display_task(root, all_tasks_frame, task_scheduler: TaskScheduler, task: Task, index):
    checkbox_var = ctk.IntVar()
    if task.is_complete_bool:
        checkbox_var.set(1)
    else:
        checkbox_var.set(0)
    root: ctk.windows.ctk_tk.CTk

    task_name = task.name
    task_due_date = task.due_date

    task_frame = ctk.CTkFrame(all_tasks_frame, corner_radius=10, fg_color="gray20")  # frame for the whole task
    task_frame.grid(row=index, column=0, pady=15, padx=15)

    task_frame.grid_rowconfigure(2, weight=1)  # Make row 0 expandable
    task_frame.grid_columnconfigure(0, weight=1)

    checkbox = ctk.CTkCheckBox(task_frame, variable=checkbox_var, text="", width=1,
                               command=lambda: on_checkbox_click(checkbox_var, task_scheduler, task))
    checkbox.grid(row=0, column=2, padx=(5, 9), sticky="N", pady=15)

    task_name_entry = ctk.CTkEntry(task_frame, width=553, placeholder_text="Enter Task Name")
    due_date_entry = ctk.CTkEntry(task_frame, width=60, placeholder_text="mm/dd")

    task_label = ctk.CTkLabel(task_frame, text=task_name, wraplength=550, justify="left", text_color="white", width=550,
                              anchor="nw")

    due_date_label = ctk.CTkLabel(task_frame, text="Due:", font=TEXT_FONT, anchor='w')
    due_date_label.grid(row=1, column=0, columnspan=1, sticky="W", padx=(18, 0), pady=0)

    due_date_color = get_due_date_color(task_due_date)
    due_date = ctk.CTkLabel(task_frame, text=task_due_date, text_color=due_date_color, font=TEXT_FONT_BOLD, anchor='w',
                            width=480)

    show_labels(task_label, due_date)

    buttons_frame = ctk.CTkFrame(task_frame, fg_color="transparent", corner_radius=20)
    buttons_frame.grid(row=2, column=0, columnspan=100, sticky="EW", pady=10)

    buttons_frame.columnconfigure(0, weight=1)
    buttons_frame.columnconfigure(1, weight=1)

    edit_button = ctk.CTkButton(buttons_frame, text="Edit", fg_color="#1a4c85", hover_color="#0f2b4c", corner_radius=15)
    edit_button.grid(row=0, column=0, sticky="EW", padx=30)

    delete_button = ctk.CTkButton(buttons_frame, text="Delete", fg_color="#851a22", hover_color="#721616",
                                  corner_radius=15)
    delete_button.grid(row=0, column=1, sticky="EW", padx=30)

    edit_button.bind("<Button-1>", lambda _event: on_task_edit(task_label, task_name_entry, due_date,
                                                               due_date_entry, edit_button, delete_button, task,
                                                               all_tasks_frame, root, task_scheduler))

    delete_button.bind("<Button-1>", lambda _event: on_delete(all_tasks_frame, root, task_scheduler, task))

    if task.is_editing:
        root.after(1, lambda: on_task_edit(task_label, task_name_entry, due_date, due_date_entry, edit_button,
                                           delete_button, task, all_tasks_frame, root, task_scheduler))


def on_task_edit(task_name_label, task_name_entry, due_date_label, due_date_entry, edit_button, delete_button,
                 task: Task, all_tasks_frame, root, task_scheduler, edit_now=False):
    # Hide the labels and show the entry widgets with the current text
    task.set_editing(True)
    disable_widget(globals.reverse_checkbox, globals.sort_menu)

    task_name_label.grid_remove()
    due_date_label.grid_remove()

    if not edit_now:
        task_name_entry.insert(0, task.name)
        due_date_entry.insert(0, task.due_date)
    task_name_entry.grid(row=0, column=0, pady=15, padx=(15, 22), sticky='W')
    root.after(10, task_name_entry.focus_set)

    due_date_entry.grid(row=1, column=0, padx=55, sticky="W")
    root.after(10, due_date_entry.focus_set)
    root.after(10, root.focus_set)

    edit_button.configure(text="Save")
    edit_button.unbind("<Button-1>")
    edit_button.bind("<Button-1>",
                     lambda _event: save_changes(task_name_label, task_name_entry, due_date_label,
                                                 due_date_entry,
                                                 task,
                                                 edit_button, delete_button, all_tasks_frame, root, task_scheduler))

    delete_button.configure(text="Cancel")
    delete_button.unbind("<Button-1>")
    delete_button.bind("<Button-1>",
                       lambda _event: save_changes(task_name_label, task_name_entry, due_date_label,
                                                   due_date_entry, task, edit_button, delete_button,
                                                   all_tasks_frame, root, task_scheduler, cancel=True))


def save_changes(task_name_label, task_name_entry, due_date_label, due_date_entry, task: Task, edit_button,
                 delete_button, all_tasks_frame,
                 root, task_scheduler, cancel=False):
    task.set_editing(False)

    # Update the labels with the text from the entry widgets
    if cancel:
        if task.is_blank:
            task_scheduler.delete_task_obj(task)
            update_gui(all_tasks_frame, root, task_scheduler, )
        task_name_label.configure(text=task.name)
        due_date_label.configure(text=task.due_date)
    else:

        new_name = task_name_entry.get().strip()
        new_due_date = due_date_entry.get().strip()

        valid_date = Task.is_valid_date(new_due_date)

        if not valid_date and new_name == "":
            messages.no_name()
            messages.invalid_date()
            return

        if new_name == "":
            messages.no_name()
            return

        if not valid_date:
            messages.invalid_date()
            return

        task_name_label.configure(text=new_name)
        due_date_label.configure(text=new_due_date, text_color=get_due_date_color(new_due_date))

        task.set_name(new_name)
        task.set_date(new_due_date)
        task.set_not_blank()
        task_scheduler.save_to_file()
        update_gui(all_tasks_frame, root, task_scheduler)

    # Hide the entry widgets and show the labels
    task_name_entry.grid_remove()
    task_name_entry.delete(0, tk.END)
    due_date_entry.grid_remove()
    due_date_entry.delete(0, tk.END)

    show_labels(task_name_label, due_date_label)
    reset_buttons(task_name_label, task_name_entry, due_date_entry, task, edit_button, delete_button,
                  all_tasks_frame, root, task_scheduler, due_date_label)
    enable_widget(globals.reverse_checkbox, globals.sort_menu, task_scheduler=task_scheduler)


def reset_buttons(task_name_label, task_name_entry, due_date_entry, task: Task, edit_button, delete_button,
                  all_tasks_frame, root, task_scheduler, due_date_label):
    edit_button: ctk.CTkLabel
    delete_button: ctk.CTkLabel
    edit_button.configure(text="Edit")
    delete_button.configure(text="Delete")

    edit_button.unbind("<Button-1>")
    delete_button.unbind("<Button-1>")

    edit_button.bind("<Button-1>",
                     lambda _event: on_task_edit(task_name_label, task_name_entry, due_date_label,
                                                 due_date_entry,
                                                 edit_button,
                                                 delete_button, task, all_tasks_frame, root, task_scheduler))
    delete_button.bind("<Button-1>", lambda _event: on_delete(all_tasks_frame, root, task_scheduler, task))


def new_task(all_tasks_frame, task_scheduler: TaskScheduler, root):
    task_scheduler.add_task(Task(number=task_scheduler.max_num))
    update_gui(all_tasks_frame, root, task_scheduler, sort=False)


def show_labels(name_label, date_label):
    date_label.grid(row=1, column=0, sticky='E', padx=55)
    name_label.grid(row=0, column=0, pady=15, padx=(18, 0), sticky="W", columnspan=1)


def delete_completed_tasks(main_frame, root, task_scheduler: TaskScheduler):
    task_scheduler.delete_complete_tasks()
    task_scheduler.save_to_file()
    update_gui(main_frame, root, task_scheduler)


def change_sort(option, main_frame, root, task_scheduler: TaskScheduler):
    task_scheduler.set_sort_type(option)

    if task_scheduler.num_tasks == 1:
        return

    task_scheduler.sort_tasks()
    task_scheduler.save_to_file()
    update_gui(main_frame, root, task_scheduler)


def reverse_tasks(all_tasks_frame, root, task_scheduler: TaskScheduler):
    task_scheduler.flip_reverse()
    if task_scheduler.num_tasks == 1:
        return
    task_scheduler.sort_tasks()
    task_scheduler.save_to_file()
    update_gui(all_tasks_frame, root, task_scheduler)
