import sqlite3 as sql

con = sql.connect("base_de_datos.db")
cur = con.cursor()

cur.execute("PRAGMA foreign_keys = ON;") 

cur.execute("DROP TABLE operaciones")
cur.execute("DROP TABLE balance")
cur.execute("DROP TABLE usuarios")

cur.execute("CREATE TABLE usuarios (usuario TEXT, contraseña TEXT, PRIMARY KEY(usuario))")
cur.execute("CREATE TABLE balance (usuario TEXT, balance NUMBER, PRIMARY KEY(usuario), FOREIGN KEY (usuario) references usuarios(usuario))")
cur.execute("CREATE TABLE operaciones (usuario TEXT, id NUMBER, dinero NUMBER, tipo TEXT, fecha DATE, concepto TEXT, PRIMARY KEY(usuario, id), FOREIGN KEY (usuario) references usuarios(usuario))")


cur.execute("INSERT INTO usuarios Values('a', 1)")
cur.execute("INSERT INTO balance Values('a', 200)")
cur.execute("INSERT INTO operaciones Values ('a', 1, 100, 'R', '10/09/2023', 'Cena')")
cur.execute("INSERT INTO operaciones Values ('a', 2, 200, 'R', '10/09/2023', 'Cena')")
con.commit()

res = cur.execute("SELECT * from usuarios")
print("Usuarios: " + str(res.fetchall()))
res = cur.execute("SELECT * from balance")
print("Balance: " + str(res.fetchall()))
res = cur.execute("Select * from operaciones")
print("Operaciones: " + str(res.fetchall()))
