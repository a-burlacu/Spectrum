# Databases

## SQLite

> Provides lightweight disk-based database 
>
> **sqlite3** is a module included with Python
>
> Used to prototype application and then use a bigger database like PostgreSQL or Oracle 
>
> Used for small applications
>
> Uses **SQL** language 
>
> **[SQL KEYWORDS](https://www.sqlite.org/lang.html)**

#### ---Use:

- import **sqlite3** into a Python file

- Create a **connection object** **`con`** that represents the database 
- name the database that will be created as a **`.db`** file 
- to create a database stored on RAM (temporary database) use **`:memory:`**

```python
import sqlite3

con = sqlite3.connect('example.db')  # create a database file

con = sqlite3.connect(':memory:')  # OR create temporary database in RAM
```

- Create a **cursor object** **`cur`** and use **`.execute()`** method to perform commands on database

```python
import sqlite3
con = sqlite3.connect('example.db')

cur = con.cursor()

cur.execute(*something*)
```

---

#### ---Creating a Table:

```python
import sqlite3
con = sqlite3.connect('stocks.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE STOCKS
               (DATE TEXT,
               TRANS TEXT, 
               SYMBOL TEXT,
               QTY REAL, 
               PRICE REAL)''')

# Insert a row of data
cur.execute("INSERT INTO STOCKS VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()
```

- The saved data is persistent: it can be reloaded in a subsequent session even after restarting the Python interpreter

  ---

#### ---Retrieving Data:

- syntax: **SELECT *  FROM ....**

- **DO NOT** use %string operations to assemble queries 

  **`symbol = 'RHAT'`**

  **`cur.execute("SELECT * FROM STOCKS WHERE SYMBOL = '%s'" %SYMBOL)`**

The **`%s`** allows the program to be vulnerable to **SQL injection attacks** 

##### ----SQL Injection Attacks:

- This can be huge security issue, for example:

- ```python
  @app.route("/login")
  def login():
      username = request.values.get('username')
      password = request.values.get('password')
      
  	db = sqlite3.connect("localhost")
  	cur = db.cursor()
  
  	cur.execute("SELECT * FROM users WHERE username = '%s' AND password = '%s'" %  		(username, password))
  
      record = cur.fetchone()
  
  	if record:
      	session['logged_user'] = username
  		db.close()
  ```

- if the user injects **`john' OR 'a'='a';-- `**  in the 'username' field, then this command is submitted:

- **`SELECT * FROM users WHERE username = 'john' OR 'a'='a';-- AND password = '';`**

- **`'a' = 'a'`**statement is always true, the expression allows the attacker to login with the username 'john' if it exists, or with the first entry in the user table. 

- The characters **`;--`** comment out the rest of the SQL query, causing the application to ignore the password field.

##### **----Correct SELECT Example**:

```python
import sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("CREATE TABLE LANG (NAME TEXT, FIRST_APPEARED INTEGER)")



# This is the qmark style:
cur.execute("insert into lang values (?, ?)", ("C", 1972))

# The qmark style used with executemany():
lang_list = [
    ("Fortran", 1957),
    ("Python", 1991),
    ("Go", 2009),
]
cur.executemany("insert into lang values (?, ?)", lang_list)



# And this is the named style:
cur.execute("select * from lang where first_appeared=:year", {"year": 1972})
print(cur.fetchall())

con.close()
```









