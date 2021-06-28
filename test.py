import sqlite3
from ticket_system.sqlCommands import search, create, insert
con = sqlite3.connect(":memory:")
cur = con.cursor()
# cur.execute('''CREATE TABLE roles_allow_to_config
#                (role_name text, guild_id text)''')
# cur.execute("INSERT INTO roles_allow_to_config VALUES ('test1', '69')")
# cur.execute("INSERT INTO roles_allow_to_config VALUES ('test2', '69')")
# cur.execute("INSERT INTO roles_allow_to_config VALUES ('test3', '69')")
con.commit()


create(con, cur, 'roles_allow_to_config', 'role_name', 'guild_id')
# insert(cur, 'roles_allow_to_config', 'test1', '69')
# cur.execute("INSERT INTO roles_allow_to_config VALUES ('test3', '69')")
print(search(cur, '69', 'roles_allow_to_config'))
con.close()
