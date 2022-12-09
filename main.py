import sqlite3
from tkinter import *
from tkinter import messagebox

root = Tk()
root.title = "Ziamah"
root.geometry("350x450")

global first_name_update
global last_name_update
global address_update
global city_update
global editor
global connection
global connector

# Databases
# Create a database or connect to one
# Open connection
connection = sqlite3.connect("address_book.db")
# Create cursor
connector = connection.cursor()


# Creation of tables in database. Code below should be uncommented when running code for the first time.

# connector.execute("""CREATE TABLE addresses (
#     first_name text,
#     last_name text,
#     address,
#     city
#     )""")


def update_btn_func():
	global connection
	global connector

	# Open connection
	connection = sqlite3.connect("address_book.db")
	# Create cursor
	connector = connection.cursor()

	record_id = delete_box.get()
	connector.execute(
		"""UPDATE addresses SET
		first_name = :first,
		last_name = :last,
		address = :address,
		city = :city

		WHERE oid = :oid""",
		{
			"first": first_name_update.get(),
			"last": last_name_update.get(),
			"address": address_update.get(),
			"city": city_update.get(),

			"oid": record_id
		}
	)

	# Commit changes to database
	connection.commit()
	# Close connection
	connection.close()

	editor.destroy()


# Function to update record
def update():
	global first_name_update
	global last_name_update
	global address_update
	global city_update
	global editor
	global connection
	global connector

	record_id = delete_box.get()

	if record_id != "":

		editor = Tk()
		editor.title = "Update Record"
		editor.geometry("350x250")

		# Open connection
		connection = sqlite3.connect("address_book.db")
		# Create cursor
		connector = connection.cursor()

		# Query the database
		connector.execute("SELECT * FROM addresses WHERE oid=" + record_id)
		records = connector.fetchall()
		print(records)

		# Creation of text boxes and the labels
		f_name_update = Label(editor, text="First Name: ")
		f_name_update.grid(row=0, column=0)
		first_name_update = Entry(editor, width=30)
		first_name_update.grid(row=0, column=1, padx=5)

		l_name_update = Label(editor, text="Last Name: ")
		l_name_update.grid(row=1, column=0)
		last_name_update = Entry(editor, width=30)
		last_name_update.grid(row=1, column=1, padx=5)

		add_label_update = Label(editor, text="Address: ")
		add_label_update.grid(row=2, column=0)
		address_update = Entry(editor, width=30)
		address_update.grid(row=2, column=1, padx=5)

		city_label_update = Label(editor, text="City: ")
		city_label_update.grid(row=3, column=0)
		city_update = Entry(editor, width=30)
		city_update.grid(row=3, column=1, padx=5)

		# Creation of update button
		submit_btn_update = Button(editor, text="Update contact", command=update_btn_func)
		submit_btn_update.grid(row=4, column=1, columnspan=2, padx=10, pady=10, ipadx=50)

		for record in records:
			first_name_update.insert(0, record[0])
			last_name_update.insert(0, record[1])
			address_update.insert(0, record[2])
			city_update.insert(0, record[3])

		# Commit changes to database
		connection.commit()
		# Close connection
		connection.close()
	else:
		messagebox.showerror("Invalid input", "Please enter an ID.")


# print_records = ""
# for record in records:
#     print_records += f"Name: {record[0]} {record[1]}, \t OID: {record[4]} \n\n"


# Create function to delete a record
def delete():
	global connection
	global connector

	if delete_box.get() != "":
		# Open connection
		connection = sqlite3.connect("address_book.db")
		# Create cursor
		connector = connection.cursor()

		# Delete a record
		connector.execute("DELETE from addresses WHERE oid= " + delete_box.get())

		# Commit changes to database
		connection.commit()
		# Close connection
		connection.close()
	else:
		messagebox.showerror("Invalid input", "Please enter an ID.")


# Creation of submit
def submit():
	global connection
	global connector

	# Open connection
	connection = sqlite3.connect("address_book.db")
	# Create cursor
	connector = connection.cursor()

	# Insert into table
	if (first_name.get() or last_name.get() or address.get() or city.get()) != "":
		connector.execute("INSERT INTO addresses VALUES (:first_name, :last_name, :address, :city)",
						  {
							  "first_name": first_name.get(),
							  "last_name": last_name.get(),
							  "address": address.get(),
							  "city": city.get(),
						  }
						  )
	else:
		messagebox.showerror("Error", "Please fill the form.")

	# Commit changes to database
	connection.commit()
	# Close connection
	connection.close()

	# Clear fields after submission
	first_name.delete(0, END)
	last_name.delete(0, END)
	address.delete(0, END)
	city.delete(0, END)


def query():
	global connection
	global connector

	# Open connection
	connection = sqlite3.connect("address_book.db")
	# Create cursor
	connector = connection.cursor()

	# Query the database
	connector.execute("SELECT *, oid FROM addresses")
	records = connector.fetchall()
	print(records)

	print_records = ""
	for record in records:
		print_records += f"Name: {record[0]} {record[1]}, \t OID: {record[4]} \n\n"

	query_label = Label(root, text=print_records)
	query_label.grid(row=9, column=0, columnspan=2)

	# Commit changes to database
	connection.commit()
	# Close connection
	connection.close()


# Creation of text boxes and the labels
f_name = Label(root, text="First Name: ")
f_name.grid(row=0, column=0)
first_name = Entry(root, width=30)
first_name.grid(row=0, column=1, padx=5)

l_name = Label(root, text="Last Name: ")
l_name.grid(row=1, column=0)
last_name = Entry(root, width=30)
last_name.grid(row=1, column=1, padx=5)

add_label = Label(root, text="Address: ")
add_label.grid(row=2, column=0)
address = Entry(root, width=30)
address.grid(row=2, column=1, padx=5)

city_label = Label(root, text="City: ")
city_label.grid(row=3, column=0)
city = Entry(root, width=30)
city.grid(row=3, column=1, padx=5)

delete_label = Label(root, text="Select ID: ")
delete_label.grid(row=6, column=0, pady=(20, 0))
delete_box = Entry(root, width=30)
delete_box.grid(row=6, column=1, padx=5, pady=(20, 0))

# Creation of submit button
submit_btn = Button(root, text="Save contact", command=submit)
submit_btn.grid(row=4, column=1, columnspan=2, padx=10, pady=10, ipadx=50)

# Creation of query button
query_btn = Button(root, text="Show records", command=query)
query_btn.grid(row=5, column=1, columnspan=2, padx=10, pady=10, ipadx=50)

# Creation of delete button
delete_btn = Button(root, text="Delete record", command=delete)
delete_btn.grid(row=8, column=1, padx=0, pady=10, ipadx=10)

# Creation of update button
update_btn = Button(root, text="Update record", command=update)
update_btn.grid(row=7, column=1, padx=0, pady=10, ipadx=10)

# Commit changes to database
connection.commit()

# Close connection
connection.close()

root.mainloop()
