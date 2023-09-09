import sqlite3 as sql

con = sql.connect("base_de_datos.db")
cur = con.cursor()

cur.execute("DROP TABLE usuario")
cur.execute("CREATE TABLE usuario (usuario TEXT, contraseña TEXT, PRIMARY KEY(usuario))")

cur.execute("INSERT INTO usuario Values('a', '1')")
con.commit()
res = cur.execute("SELECT * from usuario")
print(res.fetchall())