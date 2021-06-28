
def search(cur, id, location):
    result = []
    for row in cur.execute(f'SELECT * FROM {location} WHERE guild_id={id}'):
        result.append(list(row)[0])

    return result
    

def create(con, cur, name, value, guild_id):
    cur.execute(f'''CREATE TABLE {name}
               ({value} text, {guild_id} text)''')
    con.commit()
    print(f'Sucessfully created {name} table')


def insert(cur, name, value, guild_id):
    cur.execute(f"INSERT INTO {name} VALUES (?, ?)", (value, guild_id))
    print(f'Inserted values: [{value}, {guild_id}] into {name}.')