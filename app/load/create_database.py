from app.logging.load_logger import load_logger

def create_database(database_name, connection):

    # Connect to the master database
    cursor = connection.cursor()
    sql = f"""
                IF EXISTS(SELECT * FROM master.sys.databases WHERE name='EsureDb')
                    BEGIN
                        PRINT 'Database Exists'
                    END
                ELSE
                    BEGIN
                        CREATE DATABASE EsureDb;
                        PRINT 'Database Created'
                    END;
        """

    cursor.execute(sql)

    for message in cursor.messages:
        prefix = "[Microsoft][ODBC SQL Server Driver][SQL Server]"
        msg = message[1]
        run_message = msg[len(prefix):].strip()
        load_logger.info(run_message)

    print(run_message)
