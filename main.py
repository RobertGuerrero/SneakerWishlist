import tkinter as tk
import sqlite3

database = r"database.db"
conn = sqlite3.connect(database)
c = conn.cursor()

def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    conn.close()
    print("Connection Created.")

def remove(key):
    try:
        remove_sql = "DELETE FROM Sneakers WHERE id = {};".format(key)
        c.execute(remove_sql)
        conn.commit()
    except:
        print("Key does not exist.")

def user_input():
    snkr_name = input("Enter sneaker name: ")
    snkr_size = float(input("Enter size: "))
    snkr_price = int(input("Enter price: "))

    insert_sql = "INSERT INTO Sneakers (name, size, price) VALUES ('{}', {}, {});".format(snkr_name, snkr_size, snkr_price)

    c.execute(insert_sql)
    conn.commit()

def add_snkr_db(snkr_name, snkr_size, snkr_price, window, list_frame):

    insert_sql = "INSERT INTO Sneakers (name, size, price) VALUES ('{}', {}, {});".format(snkr_name, snkr_size, snkr_price)

    c.execute(insert_sql)
    conn.commit()
    update_window(list_frame)
    window.destroy()

def add_snkr(frame, name, size, price, id):
    row = tk.Frame(frame, width=300)
    snkr_id = tk.Label(row, text = str(id))
    snkr = tk.Label(row, text = name)
    snkr_size = tk.Label(row, text = str(size))
    snkr_price = tk.Label(row, text = str(price))

    snkr_id.pack(side=tk.LEFT)
    snkr.pack(side=tk.LEFT)
    snkr_price.pack(side=tk.RIGHT)
    snkr_size.pack(side=tk.RIGHT)
    row.pack(fill=tk.X, anchor=tk.N)

def add_action(list_frame):
    add_window = tk.Toplevel()
    add_window.title("Add Sneaker")

    name_var = tk.StringVar()
    size_var = tk.DoubleVar()
    price_var = tk.IntVar()

    name_entry = tk.Entry(add_window, width=30, textvariable=name_var)
    size_entry = tk.Entry(add_window, width=30, textvariable=size_var)
    price_entry = tk.Entry(add_window, width=30, textvariable=price_var)

    name_label = tk.Label(add_window, text="Name: ")
    size_label = tk.Label(add_window, text="Size: ")
    price_label = tk.Label(add_window, text="Price: ")

    add_button = tk.Button(add_window, text="Add Sneaker", command=lambda: add_snkr_db(name_var.get(), size_var.get(), price_var.get(), add_window, list_frame))

    name_label.grid(row=1, column=0)
    size_label.grid(row=2, column=0)
    price_label.grid(row=3, column=0)

    name_entry.grid(row=1, column=1)
    size_entry.grid(row=2, column=1)
    price_entry.grid(row=3, column=1)
    add_button.grid(row=4, column=0, columnspan=2)

def update_window(list_frame):
    for i in list_frame.winfo_children():
        i.destroy()

    add_snkr(list_frame, "Sneaker Name", "Size", "Price", "ID")

    select_query = """SELECT *
                            FROM Sneakers;"""
    c.execute(select_query)
    results = c.fetchall()

    for i in results:
        add_snkr(list_frame, i[1], i[2], i[3], i[0])

def delete_snkr_db(id_var, list_frame, window):
    delete_sql = """DELETE FROM Sneakers WHERE id = {}""".format(id_var)
    print(delete_sql)
    c.execute(delete_sql)
    conn.commit()
    update_window(list_frame)
    window.destroy()

def delete_action(list_frame):
    delete_window = tk.Toplevel()
    delete_window.title("Delete Sneaker")

    id_var = tk.IntVar()

    id_entry = tk.Entry(delete_window, width=30, textvariable=id_var)

    id_label = tk.Label(delete_window, text="ID: ")

    delete_button = tk.Button(delete_window, text="Delete Sneaker",
                           command=lambda: delete_snkr_db(id_var.get(), list_frame, delete_window))

    id_label.grid(row=1, column=0)

    id_entry.grid(row=1, column=1)
    delete_button.grid(row=4, column=0, columnspan=2)


if __name__ == '__main__':
    #create_connection(r"database.db")
    #database = r"database.db"
    #conn = sqlite3.connect(database)
    #c = conn.cursor()

    table1 = """CREATE TABLE IF NOT EXISTS Sneakers (
                    id integer PRIMARY KEY,
                    name text NOT NULL,
                    size float NOT NULL,
                    price integer NOT NULL
    );"""

    insert_sql = """INSERT INTO Sneakers (name, size, price)
                        VALUES ('Jordan 1 Mocha', 8, 450);"""

    select_query = """SELECT *
                        FROM Sneakers;"""
    #c.execute(insert_sql)
    #conn.commit()

    #user_input()

    #remove(1)

    c.execute(select_query)
    results = c.fetchall()

    for i in results:
        print(i)


    window = tk.Tk()

    window.title("Sneaker Wishlist")
    window.geometry("300x400")
    list_frame = tk.Frame(window)
    list_frame.pack(fill=tk.BOTH)
    button_frame = tk.Frame(window)
    button_frame.pack(fill=tk.BOTH, side=tk.BOTTOM)
    update_window(list_frame)

    add_button = tk.Button(button_frame, text="Add Sneaker", command=lambda: add_action(list_frame))
    add_button.pack(side=tk.LEFT)
    delete_button = tk.Button(button_frame, text="Delete Sneaker", command=lambda: delete_action(list_frame))
    delete_button.pack(side=tk.RIGHT)

    window.mainloop()

