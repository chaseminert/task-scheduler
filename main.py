import customtkinter as ctk

import globals
import gui_utils
import messages
from task_scheduler import TaskScheduler

MIN_WIDTH = 1200
MIN_HEIGHT = 375

STARTING_HEIGHT = 800


def run_gui(task_scheduler: TaskScheduler) -> None:
    root = ctk.CTk()
    root.geometry(f"{MIN_WIDTH}x{STARTING_HEIGHT}")
    root.minsize(MIN_WIDTH, MIN_HEIGHT)

    root.grid_columnconfigure(0, weight=1)

    program_label = ctk.CTkLabel(root, text="Task Scheduler", font=gui_utils.TITLE_FONT)
    program_label.grid(row=0, column=0, columnspan=100, pady=(20, 0))

    all_tasks_frame = ctk.CTkScrollableFrame(root, fg_color="transparent", width=900, height=675)
    all_tasks_frame.grid(row=2, padx=(250, 0))

    gui_utils.display_header_buttons(root, all_tasks_frame, task_scheduler)
    task_scheduler.sort_tasks()
    gui_utils.display_tasks(root, all_tasks_frame, task_scheduler)

    root.protocol("WM_DELETE_WINDOW", lambda: on_close(task_scheduler, root))
    # root.bind("<d>", lambda event: task_scheduler.print_ts(event))

    root.mainloop()


def on_close(task_scheduler: TaskScheduler, root: ctk.windows.ctk_tk.CTk):
    if task_scheduler.any_editing():
        if not messages.currently_editing():  # aka if they clicked the "NO" button
            return
    task_scheduler.delete_blank_tasks()
    task_scheduler.save_to_file()
    root.destroy()
    exit()


def main():
    task_scheduler = TaskScheduler.load_from_file()
    # for task in task_scheduler:
    # print(task)
    run_gui(task_scheduler)


if __name__ == "__main__":
    globals.init()
    main()
