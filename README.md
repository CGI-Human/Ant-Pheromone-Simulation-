# Ant Pheromone Simulation

This project simulates the behavior of ants using pheromones to find the shortest path to food sources.

## Requirements

- **Python**: Ensure that you have Python 3.7 or later installed on your system.
- **Dependencies**: This simulation requires several Python libraries that need to be installed.

## Setup Instructions

Follow these steps to set up and run the simulation:

### 1. Download the Repository

You can download the files directly from GitHub:

- Navigate to the repository: [Ant Pheromone Simulation](https://github.com/CGI-Human/Ant-Pheromone-Simulation-).
- Click on the "Code" button and select **Download ZIP**.
- Extract the files to a folder on your computer.

### 2. Install Python

Make sure Python 3.7 or later is installed on your system. You can download it from the official website:

- [Python Official Download Page](https://www.python.org/downloads/)

To verify Python is installed correctly, run this in your terminal:

```bash
python --version
or if using Python 3 specifically:

python3 --version
3. Install Dependencies
Open a terminal (or command prompt) in the directory where you downloaded the repository.

To install the required libraries, you’ll need to create a virtual environment and install the dependencies listed in the requirements.txt file.

Create a Virtual Environment:

python3 -m venv venv
Activate the Virtual Environment:

For macOS/Linux:
source venv/bin/activate
For Windows:
.\venv\Scripts\activate
Install the Required Libraries:

Once the virtual environment is active, install the required libraries by running:

pip install -r requirements.txt
If there is no requirements.txt file, you can manually install dependencies like this:

pip install <library_name>
For example, if the project uses numpy, matplotlib, etc., you can install them individually:

pip install numpy matplotlib
4. Run the Simulation
After installing all the dependencies, you can start the simulation.

Run the following command:

python simulation.py
This should start the simulation, and you can observe the behavior of the ants as they find the shortest path to the food source.

Troubleshooting

If you run into issues:

Ensure that you're using the correct version of Python.
Make sure all dependencies are installed properly by checking the output of pip list.
If the simulation doesn't run as expected, try checking for any missing libraries and install them manually.
Additional Notes

Feel free to contribute to this project by forking the repository and submitting a pull request.
If you have suggestions or feedback, open an issue in the GitHub repository.
