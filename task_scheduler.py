from datetime import datetime
import ast

TODAY_DATE = datetime.now()
FORMAT_STR = "<15"
INVALID_INPUT_ERROR = "Error: Input is invalid!"
INVALID_DATE_ERROR = "Error: Date is invalid!"


class Task:
    def __init__(self, name="", due_date="", completed=False, number=-1, blank=True, is_editing=True):
        self._name = name
        self._completed = completed
        whole_date = due_date + "/" + TODAY_DATE.strftime("%y")
        if due_date == "":
            self._due_date = ""
        else:
            self._due_date: datetime = datetime.strptime(whole_date, "%m/%d/%y")
        self._number = number
        self._blank = blank
        self._is_editing = is_editing

    def to_string_file(self) -> str:
        return f"{self.name}::{self.due_date}::{self.is_complete_bool}"

    @staticmethod
    def from_string_file(task_str: str, index=0) -> "Task":
        name, due_date, is_complete = task_str.strip().split("::")
        is_complete_bool = is_complete.strip() == "True"
        return Task(name, due_date, is_complete_bool, index - 1, blank=False, is_editing=False)

    @property
    def name(self) -> str:
        return self._name

    @property
    def number(self) -> int:
        return self._number

    @property
    def due_date(self):
        if self._due_date == "":
            return self._due_date
        else:
            return self._due_date.strftime("%#m/%#d")

    @property
    def due_date_obj(self) -> datetime:
        return self._due_date

    @property
    def is_editing(self) -> bool:
        return self._is_editing

    @property
    def is_complete_str(self) -> str:
        if self._completed:
            return "Yes"
        else:
            return "No"

    @property
    def is_complete_bool(self) -> bool:
        return self._completed

    @property
    def is_blank(self) -> bool:
        return self._blank

    def flip_status(self):
        old_status = self._completed
        self._completed = not old_status

    def set_blank(self):
        self._blank = True

    def set_not_blank(self):
        self._blank = False

    def set_as_complete(self):
        self._completed = True

    def set_as_incomplete(self):
        self._completed = False

    def set_editing(self, val: bool):
        self._is_editing = val

    def set_name(self, name):
        self._name = name

    def set_number(self, new_number: int):
        self._number = new_number

    def set_date(self, date_str):
        whole_date = date_str + "/" + TODAY_DATE.strftime("%y")
        self._due_date: datetime = datetime.strptime(whole_date, "%m/%d/%y")

    @staticmethod
    def is_valid_date(date_str):
        try:
            # Try to parse the date string as MM/DD format
            date_obj = datetime.strptime(date_str, "%m/%d")

            # Check if the day and month components are within valid ranges
            if 1 <= date_obj.month <= 12 and 1 <= date_obj.day <= 31:
                return True
        except ValueError:
            return False


class TaskScheduler:
    FILE_PATH = "data.txt"
    DATE = "Due Date"
    NAME = "Name"
    ORDER_ADDED = "Order Added"

    def __init__(self, sort_type=DATE, max_num=0, reverse=False):
        self._sort_type = sort_type
        self._tasks = []
        self._max_num = max_num
        self._reverse = reverse

    def __iter__(self):
        return iter(self._tasks)

    def __getitem__(self, index):
        return self._tasks[index]

    def __len__(self):
        return len(self._tasks)

    def __str__(self):
        string = ""
        for task in self._tasks:
            string += task.debug_str() + "\n\n"
        return string

    def add_task(self, task):
        self._tasks.insert(0, task)
        self.inc_max_num()

    def any_editing(self):  # returns if any tasks are currently being edited
        for task in self:
            if task.is_editing:
                return True
        return False

    def can_enable_widgets(self):  # returns whether you can enable the drop-down menu and the checkbox
        for task in self._tasks:
            if task.is_editing:
                return False
        return True

    def delete_task_obj(self, task: Task):
        index = self._tasks.index(task)
        del self._tasks[index]

    def delete_blank_tasks(self):
        new_list = []
        for index, task in enumerate(self._tasks, start=1):
            if not task.is_blank:
                new_list.append(task)
        self._tasks = new_list

    def sort_tasks(self):
        if self.any_editing():
            return
        sort_type = self.get_sort_type
        reverse = self.is_reverse
        if sort_type == self.DATE:
            self.sort_by_date(reverse)
        elif sort_type == self.NAME:
            self.sort_by_name(reverse)
        else:
            self.sort_by_added(reverse)

    def save_to_file(self) -> None:
        if self.any_editing():
            return

        self.sort_by_added(reverse=False)
        with open(TaskScheduler.FILE_PATH, "w") as file:
            sort_type = self.get_sort_type
            reverse = str(self.is_reverse)
            file.write(reverse + "\n")
            file.write(sort_type + "\n")

            for task in self._tasks:
                file.write(task.to_string_file() + "\n")

    @staticmethod
    def _create_file() -> None:
        with open(TaskScheduler.FILE_PATH, "w") as file:
            file.write("False\n")
            file.write(f"{TaskScheduler.ORDER_ADDED}\n")

    @staticmethod
    def load_from_file() -> "TaskScheduler":
        tasks_from_file = []
        if not TaskScheduler._file_exists():
            TaskScheduler._create_file()
        with open(TaskScheduler.FILE_PATH, "r") as file:
            for line_num, line in enumerate(file):
                if line_num == 0:
                    reverse = ast.literal_eval(line.strip())
                elif line_num == 1:
                    sort_type = line.strip()
                else:
                    tasks_from_file.append(Task.from_string_file(line, line_num))
            max_num = len(tasks_from_file)
            task_scheduler = TaskScheduler(sort_type, max_num, reverse)
            task_scheduler._tasks = tasks_from_file
            return task_scheduler

    @staticmethod
    def _file_exists() -> bool:
        try:
            with open(TaskScheduler.FILE_PATH, "r"):
                return True
        except FileNotFoundError:
            return False

    def replace_task(self, index: int, task: "Task"):
        self._tasks[index - 1] = task

    def sort_by_date(self, reverse=False):
        self._tasks.sort(key=lambda obj: obj.due_date_obj, reverse=reverse)

    def sort_by_added(self, reverse=True):
        self._tasks.sort(key=lambda obj: obj.number, reverse=not reverse)

    def sort_by_name(self, reverse=False):
        self._tasks.sort(key=lambda obj: obj.name.lower(), reverse=reverse)

    def set_sort_type(self, new_type):
        self._sort_type = new_type

    @property
    def num_tasks(self) -> int:
        return len(self._tasks)

    @property
    def get_sort_type(self) -> str:
        return self._sort_type

    @property
    def max_num(self) -> int:
        return self._max_num

    @property
    def is_reverse(self) -> bool:
        return self._reverse

    def get_task(self, index: int) -> "Task":
        return self._tasks[index - 1]

    def delete_task(self, index: int):
        del self._tasks[index - 1]

    def inc_max_num(self):
        self._max_num += 1

    def set_max_num(self, new_max: int):
        self._max_num = new_max

    def flip_reverse(self):
        self._reverse = not self.is_reverse

    def delete_complete_tasks(self):
        indexes = []
        tasks = self._tasks
        for index, element in enumerate(tasks):
            if element.is_complete_bool:
                indexes.append(index)
        indexes_reverse = sorted(indexes, reverse=True)
        for index_element in indexes_reverse:
            del tasks[index_element]

    def change_all_tasks(self, user_input: int):
        tasks = self._tasks
        if user_input == 1:
            for index, element in enumerate(tasks):
                tasks[index] = element.set_as_complete()
        else:
            for index, element in enumerate(tasks):
                tasks[index] = element.set_as_incomplete()
