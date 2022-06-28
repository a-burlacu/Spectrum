import sqlite3
from employee import Employee

#conn = connection object that represents our database
#creates a file to store data, keeps adding to file each run
# conn = sqlite3.connect('employee.db')

# uses RAM to store data, rewrites database each run, good for testing
conn = sqlite3.connect(':memory:')

#cursor allows us to execute SQL commands
c = conn.cursor()

#create Employee table
#holds firstname, lastname, pay (case-INsensitive)
c.execute("""CREATE TABLE EMPLOYEES (
            FIRST TEXT,
            LAST TEXT,
            PAY INTEGER
            )""")



#### create fxs to insert,search,update,and delete ####

def insert_emp(emp):
    with conn:    # using 'with conn' means we don't need a conn.commit() later
        c.execute("INSERT INTO EMPLOYEES VALUES(:first, :last, :pay)", {'first': emp.first, 'last': emp.last, 'pay': emp.pay})

def get_emp_by_name(lastname):

    c.execute("SELECT * FROM EMPLOYEES WHERE LAST=:last", {'last': lastname})
    return c.fetchall()

def update_pay(emp, pay):
    with conn:
        c.execute("""UPDATE EMPLOYEES SET PAY = :pay 
                    WHERE FIRST = :first AND LAST = :last""",
                  {'first': emp.first, 'last': emp.last, 'pay': emp.pay})

def remove_emp(emp):
    with conn:
        c.execute("DELETE FROM EMPLOYEES WHERE FIRST = :first AND LAST = :last",
                  {'first': emp.first, 'last': emp.last})





# #### ways to insert data ####
#
emp_1 = Employee('John','Doe', 80000)
emp_2 = Employee('Jane','Smith', 90000)

#using  our new fx def #
insert_emp(emp_1)
insert_emp(emp_2)

emp = get_emp_by_name('Doe')
print(emp)

update_pay(emp_2, 95000)

remove_emp(emp_1)

emp = get_emp_by_name('Doe')
print(emp)



# c.execute("INSERT INTO EMPLOYEES VALUES('Mary', 'Schafer', 70000)")
#
#
# # # use ? as placeholder for values
# c.execute("INSERT INTO EMPLOYEES VALUES(?, ?, ?)",(emp_1.first, emp_1.last, emp_1.pay))
#
#
# # #OR use a dictionary to populate table using {'key': value} pairs (keys set by VALUES)
# c.execute("INSERT INTO EMPLOYEES VALUES(:first, :last, :pay)",{'first': emp_2.first,'last': emp_2.last,'pay': emp_2.pay})
#
#
#
#
#
#
#
# #### ways to search for items ####
#
# # finds one instance in database, returns only one Employee object
# # c.execute("SELECT * FROM EMPLOYEES WHERE FIRST= 'Mary'")
# # print(c.fetchone())
#
# # finds all instances, returns list with Employee objects
# # qmark ? method of search
# c.execute("SELECT * FROM EMPLOYEES WHERE LAST=?", ('Doe',))
# print(c.fetchall())
#
# # dictionary method
# c.execute("SELECT * FROM EMPLOYEES WHERE LAST=:last", {'last': 'Smith'})
# print(c.fetchall())
#
#
# #commits current transaction to database file (all edits made since last run)
# conn.commit()
#
# #deletes table
# # c.execute("DROP TABLE EMPLOYEES")


#good practice: closes connection to database
conn.close()