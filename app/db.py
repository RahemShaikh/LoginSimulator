import config
import pyodbc

def get_connection_to_db() -> pyodbc.Connection:
    """
    Establishes a connection to the SQL Server database using ODBC and Windows Authentication.

    Returns:
        pyodbc.Connection: A connection object to the specified database.

    Raises:
        pyodbc.Error: If the connection fails.
    """

    server = config.DB_SERVER
    database = config.DB_DATABASE

    conn_str = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={server};'
        f'DATABASE={database};'
        'Trusted_Connection=yes;'  # Enables Windows Authentication
    )

    return pyodbc.connect(conn_str)


def close_connection(connection) -> None:
    """
    Closes the provided database connection.

    Args:
        connection (pyodbc.Connection): The active database connection to close.
    """
    
    connection.close()
