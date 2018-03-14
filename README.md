# CMPUT 291 Project 1
This is a system to handle a waste management companies database. Employees are able to maintain their records on this program and also get information about their shifts or records of customer accounts.

###### * For Developers
If your wish to extend the functionality, please read the documentation as it will help break down the process behind the program. We divided the functionalities into modules which organizes and allows for easier scalability if there is intention to create extensions to this program.

#### Installation

Requirements: Python3.6, pip3

##### 1. Create a virtual environment (Optional)

Goto the directory you want to store your virtualenv
```
virtualenv ENV_NAME

cd ENV_NAME
```

##### 2. Activate your environment

###### For OSX

```
source bin/activate
```

###### For Windows

```
.\Scripts\activate
```

##### 3. Clone repository to virtual environment and import dependencies
```
git clone https://github.com/ThomasChuDesigns/CMPUT291_Project_1.git
cd CMPUT291_Project_1
pip3 install -r requirements.txt
```

##### 4. Run Program
In your terminal, change to this repository folder and run this command:
```
python3 main.py
```