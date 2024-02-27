# Task Scheduler

## Overview
Task Scheduler is an open-source task management application with a graphical user interface (GUI) designed to help users organize their tasks efficiently. Users can input tasks, set due dates, mark tasks as complete, and more, all within a user-friendly interface.

## Key Features
- **Graphical User Interface (GUI)**: Modern GUI powered by CustomTkinter for a seamless user experience.
- **Task Management**: Add, edit, delete, and prioritize tasks with ease.
- **Sorting Options**: Sort tasks by due date, name (alphabetically), or order added. Reverse sorting is also supported.
- **Data Persistence**: All task data is automatically saved when the user exits the program and restored upon reopening.
- **Real-time Updates**: Changes made to tasks are automatically reflected in the GUI, ensuring a seamless user experience.

## Technologies Used
- **Python**: Core programming language for application logic.
- **CustomTkinter**: Modern Python GUI library for building the graphical interface.

## Installation and Usage
1. **Clone the Repository**: Clone the repository to your local machine:
   ```bash
   git clone https://github.com/chaseminert/task-scheduler.git
   cd task-scheduler
2. **Install Dependencies**: Ensure you have Python installed on your system. Install the required dependencies using:
   ```bash
   pip install -r requirements.txt
3. **Run the Application**: Execute the main Python script to launch the program:
4. ```bash
   python main.py
  **Usage**: Use the GUI to manage tasks, set due dates, mark tasks as complete, and more. Changes are automatically saved and reflected open closing the program.

## Visual
<img width="800" alt="image" src="https://github.com/chaseminert/task-scheduler/assets/155914646/80aebab1-e651-4f9b-99dd-7021e71edfee">


## Challenges Faced
### Backend Development
Addressing backend challenges involved determining the data storage structure and handling user data persistence. This was resolved by creating a `Task` class to encapsulate task objects and a `TaskScheduler` class to manage task collections.

### Frontend GUI Design
Developing an intuitive GUI presented challenges in representing task objects visually and ensuring real-time updates. Overcoming this involved learning about Tkinter's frame and grid geometry manager, enabling dynamic task display updates upon user actions.

### Task Editing and Maintenance
Enabling seamless task editing posed a significant challenge. This was addressed by implementing robust error handling and dynamic data updates to reflect changes instantly, enhancing user experience and program stability.

## Contributing
Contributions to enhance the functionality, usability, or documentation of Task Scheduler are welcome. To contribute:
- Fork the repository
- Create a new branch for your feature or fix
- Commit your changes
- Push your changes to your fork
- Submit a pull request

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
  
