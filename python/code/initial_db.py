from sqlalchemy import create_engine

db_name = 'db'
db_user = 'user'
db_pass = 'secret'
db_host = 'db'
db_port = '5432'

db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)

def init_tables():
    query = """
        INSERT INTO organization
            (id, name, created) VALUES
            ('123', 'Super1', '2018-01-24 17:28:09.000000'),
            ('1234', 'Super2', '2017-01-24 17:28:09.000000'),
            ('1235', 'Super3', '2016-01-24 17:28:09.000000')
        RETURNING *;
    """
    results = db.execute(query)
    print_results(results)

def init():
    is_table_result = db.execute("SELECT name FROM organization WHERE id = '123';")
    if is_table_result.first():
        return

    init_tables()

def print_results(results):
    for r in results:
        print(r)

if __name__ == '__main__':
    print('Python application started!')

    init()
