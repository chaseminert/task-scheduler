from tkinter import messagebox


def invalid_date():
    messagebox.showerror("Error", "Invalid Date (must be mm/dd)")


def no_name():
    messagebox.showerror("Error", "Invalid Name (cannot be blank)")


def currently_editing():
    return messagebox.askyesno("Quit", "An edit is currently in progress. Are you sure you want to quit?")
