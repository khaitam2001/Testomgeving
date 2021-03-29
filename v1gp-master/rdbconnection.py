import psycopg2

# DIT IS HETZELFDE ALS VAN GAYNORA, DIT KOMT UIT ONS GROUP PROJECT
def conrdb():
    try:
        connectionRDB = psycopg2.connect(
            user='postgres',
            password='Nguyen1996',
            host='localhost',
            database='postgres'
        )
        cursor = connectionRDB.cursor()
        return connectionRDB, cursor
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
