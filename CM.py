import mysql.connector
from datetime import datetime

# MySQL connection parameters
db_params = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345',
    'database': 'company_management'
}

# Function to connect to MySQL
def connect_to_mysql():
    try:
        connection = mysql.connector.connect(**db_params)
        cursor = connection.cursor(buffered=True)
        return connection, cursor
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None, None

# Function to create tables if not exists
def create_tables(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            EMPNO INT PRIMARY KEY,
            ENAME VARCHAR(255),
            POST VARCHAR(255),
            SALARY INT,
            MGR INT,
            DEPTNO INT,
            DOJ DATE,
            DOB DATE,
            SEX VARCHAR(1)
        )
    """)

# Employee Management Section
def add_employee(cursor):
    print("Adding Employee:")
    emp_no = int(input("Enter Employee Number: "))
    ename = input("Enter Employee Name: ")
    post = input("Enter Employee Post: ")
    salary = int(input("Enter Salary: "))
    mgr = int(input("Enter Manager's Employee Number: "))
    dept_no = int(input("Enter Department Number: "))
    doj = input("Enter Date of Joining (YYYY-MM-DD): ")
    dob = input("Enter Date of Birth (YYYY-MM-DD): ")
    sex = input("Enter Gender (M/F): ")

    try:
        doj = datetime.strptime(doj, "%Y-%m-%d").date()
        dob = datetime.strptime(dob, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    cursor.execute("""
        INSERT INTO employees
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (emp_no, ename, post, salary, mgr, dept_no, doj, dob, sex))
    print(f"Employee {ename} added successfully.")

def fire_employee(cursor):
    print("Firing Employee:")
    emp_no = int(input("Enter Employee Number to be fired: "))
    cursor.execute("DELETE FROM employees WHERE EMPNO = %s", (emp_no,))
    if cursor.rowcount > 0:
        print(f"Employee with EMPNO {emp_no} has been fired.")
    else:
        print(f"Employee with EMPNO {emp_no} not found.")

def promote_employee(cursor):
    print("Promoting Employee:")
    emp_no = int(input("Enter Employee Number to promote: "))
    new_post = input("Enter New Post: ")
    cursor.execute("UPDATE employees SET POST = %s WHERE EMPNO = %s", (new_post, emp_no))
    if cursor.rowcount > 0:
        print(f"Employee with EMPNO {emp_no} has been promoted to {new_post}.")
    else:
        print(f"Employee with EMPNO {emp_no} not found.")

def give_raise(cursor):
    print("Giving Raise:")
    emp_no = int(input("Enter Employee Number to give a raise: "))
    raise_amount = int(input("Enter Raise Amount: "))
    cursor.execute("UPDATE employees SET SALARY = SALARY + %s WHERE EMPNO = %s", (raise_amount, emp_no))
    if cursor.rowcount > 0:
        print(f"Raise of {raise_amount} given to Employee with EMPNO {emp_no}.")
    else:
        print(f"Employee with EMPNO {emp_no} not found.")

def transfer_employee(cursor):
    print("Transferring Employee:")
    emp_no = int(input("Enter Employee Number to transfer: "))
    new_dept = int(input("Enter New Department Number: "))
    cursor.execute("UPDATE employees SET DEPTNO = %s WHERE EMPNO = %s", (new_dept, emp_no))
    if cursor.rowcount > 0:
        print(f"Employee with EMPNO {emp_no} has been transferred to Department {new_dept}.")
    else:
        print(f"Employee with EMPNO {emp_no} not found.")

# Reporting Section
def list_all_employees(cursor):
    try:
            print("Listing Employees :")
            cursor.execute("SELECT * FROM employees")
            employees = cursor.fetchall()
            if not employees:
                print("No matching records found.")
                return
            print("-" * 110)
            print("%10s%12s%20s%10s%08s%10s%12s%15s%10s" % ("EMPNO", "NAME", "POST", "SALARY", "MGR",\
                                                            "DEPTNO", "DOJ", "DOB", "Gender"))
            print("-" * 110)
            for row in employees:
                print("%10s%12s%20s%10s%08s%10s%12s%15s%10s" % (row[0], row[1], row[2], row[3], row[4],\
                                                                row[5], row[6], row[7], row[8]))
            print("-" * 110)
    except (mysql.connector.Error, ValueError) as err:
        print(f"Error displaying employees: {err}")
    
def list_employees_by_department(cursor):
    try:
            print("Listing Employees by Department:")
            dept_no = int(input("Enter Department Number: "))
            cursor.execute("SELECT * FROM employees WHERE DEPTNO = %s", (dept_no,))
            employees = cursor.fetchall()
            if not employees:
                print("No matching records found.")
                return
            print("-" * 110)
            print("%10s%12s%20s%10s%08s%10s%12s%15s%10s" % ("EMPNO", "NAME", "POST", "SALARY", "MGR",\
                                                            "DEPTNO", "DOJ", "DOB", "Gender"))
            print("-" * 110)
            for row in employees:
                print("%10s%12s%20s%10s%08s%10s%12s%15s%10s" % (row[0], row[1], row[2], row[3], row[4],\
                                                                row[5], row[6], row[7], row[8]))
            print("-" * 110)
    except (mysql.connector.Error, ValueError) as err:
        print(f"Error displaying employees: {err}")
def hierarchical_department_view(cursor):
    try:
        print("Hierarchical Department View:")
        cursor.execute("""
        SELECT D.DEPTNO, D.DEPTNAME, E.EMPNO, E.ENAME, E.POST
        FROM departments D
        LEFT JOIN employees E ON D.DEPTNO = E.DEPTNO
        ORDER BY D.DEPTNO, E.POST
        """)
        results = cursor.fetchall()
        current_dept = None

        for result in results:
             if result[0] != current_dept:
               print("-"*50)
               print(f"Department {result[0]} - {result[1]}:")
               print("-"*50)
               current_dept = result[0]

             if result[2] is not None:
               print(f"  {result[2]} - {result[3]} ({result[4]})")
    except (mysql.connector.Error, ValueError) as err:
        print(f"Error displaying employees: {err}")

def search_employee(cursor):
    print("Searching Employee:")
    emp_no = int(input("Enter Employee Number to search: "))
    cursor.execute("SELECT * FROM employees WHERE EMPNO = %s", (emp_no,))
    employee = cursor.fetchall()
    if employee:
        print("-" * 110)
        print("%10s%12s%20s%10s%08s%10s%12s%15s%10s" % ("EMPNO", "NAME", "POST", "SALARY", "MGR",\
                                                            "DEPTNO", "DOJ", "DOB", "Gender"))
        print("-" * 110)
        for row in employee:
            print("%10s%12s%20s%10s%08s%10s%12s%15s%10s" % (row[0], row[1], row[2], row[3], row[4],\
                                                                row[5], row[6], row[7], row[8]))
            print("-" * 110)
    else:
        print(f"Employee with EMPNO {emp_no} not found.")

# Performance Evaluation Section
def evaluate_performance(cursor):
    try:
        print("Evaluating Performance :")
        
        # Get user input for performance threshold
        performance_threshold = int(input("Enter Performance Threshold (Salary): "))

        # Execute SQL query to retrieve high-performing employees
        cursor.execute("SELECT * FROM employees WHERE SALARY >= %s", (performance_threshold,))
        high_performers = cursor.fetchall()

        # Display results
        if high_performers:
            print(f"\nHigh performers with salary greater than or equal to {performance_threshold}:")
            for employee in high_performers:
                print(f"Employee ID: {employee[0]}, Name: {employee[1]}, Salary: {employee[3]}")
        else:
            print("No high performers found.")
    
    except ValueError:
        print("Invalid input. Please enter a numeric value for the performance threshold.")
    except mysql.connector.Error as err:
        print(f"Error accessing the database: {err}")

# Salary Section
def adjust_salary(cursor):
    print("Adjusting Salary:")
    emp_no = int(input("Enter Employee Number to adjust salary: "))
    new_salary = int(input("Enter New Salary: "))
    cursor.execute("UPDATE employees SET SALARY = %s WHERE EMPNO = %s", (new_salary, emp_no))
    if cursor.rowcount > 0:
        print(f"Salary for Employee with EMPNO {emp_no} has been adjusted to {new_salary}.")
    else:
        print(f"Employee with EMPNO {emp_no} not found.")

def give_bonus(cursor):
    print("Giving Bonus:")
    emp_no = int(input("Enter Employee Number to give a bonus: "))
    bonus_amount = int(input("Enter Bonus Amount: "))
    cursor.execute("UPDATE employees SET SALARY = SALARY + %s WHERE EMPNO = %s", (bonus_amount, emp_no))
    if cursor.rowcount > 0:
        print(f"Bonus of {bonus_amount} given to Employee with EMPNO {emp_no}.")
    else:
        print(f"Employee with EMPNO {emp_no} not found.")

# Main function
def main():
    connection, cursor = connect_to_mysql()
    if connection and cursor:
        create_tables(cursor)

        while True:
            print("===============================================")
            print("            EMPLOYEE MANAGEMENT SYSTEM         ")
            print("===============================================")
            print("1. Hire Employee\n2. Fire Employee\n3. Promote Employee\n4. Give Raise\n5. Transfer Employee")

            print("\nReporting Section:")
            print("6. List Employees \n7.List Employees by Department\n8. Hierarchical Department View\n9. Search Employee")

            print("\nPerformance Evaluation Section:")
            print("10. Evaluate Performance")

            print("\nSalary Section:")
            print("11. Adjust Salary\n12. Give Bonus")

            print("\n13. Quit")
            choice = input("Enter your choice (1-12): ")
            print("===============================================")

            if choice == '01':
                add_employee(cursor)
                connection.commit()
            elif choice == '02':
                fire_employee(cursor)
                connection.commit()
            elif choice == '03':
                promote_employee(cursor)
                connection.commit()
            elif choice == '04':
                give_raise(cursor)
                connection.commit()
            elif choice == '05':
                transfer_employee(cursor)
                connection.commit()
            elif choice == '06':
                list_all_employees(cursor)
            elif choice == '07':
                list_employees_by_department(cursor)
            elif choice == '08':
                hierarchical_department_view(cursor)
            elif choice == '09':
                search_employee(cursor)
            elif choice == '10':
                evaluate_performance(cursor)
            elif choice == '11':
                adjust_salary(cursor)
                connection.commit()
            elif choice == '12':
                give_bonus(cursor)
                connection.commit()
            elif choice == '13':
                break
            else:
                print("Invalid choice")

        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()
