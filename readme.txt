Application 1 : Rule Engine with AST

Overview

The Rule Engine Project is designed to evaluate and combine rules based on various criteria such as age, department, salary, and experience.
This application provides an intuitive interface for users to create, evaluate, and combine rules, facilitating decision-making processes in various applications.



Features
- Create custom rules using various parameters.
- Evaluate rules against input data.
- Combine multiple rules for complex evaluations.
- User-friendly web interface.

 Installation
To set up the project on your local machine, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/aswaniramachandran/Weather_Projects.git
   cd rule_engine
2. Install dependencies: Ensure you have Python and pip installed, then run:
   pip install Flask
   pip install -r requirements.txt

3.To start the application, execute the following command in your terminal:
  python app.py
  The application will be accessible at http://localhost:5000.

4. Create_Rule
   You should give input in this format : ((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)

5. Combine_Rule 
   You should give input in this format :(age > 30 AND department = 'Sales') 
                         (age < 25 AND department = 'Marketing') 
                         (salary > 50000 OR experience > 5)

6. Evaluate Rule
   You should give input in this format : 
{
    "age": 30,
    "department": "Marketing",
    "salary": 50000,
    "experience": 5
  }