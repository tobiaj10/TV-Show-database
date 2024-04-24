import psycopg2
from psycopg2 import OperationalError, sql


table_info = {
    'status': ['statusid', 'statuslabel'],
    'types': ['typeid', 'categoryname'],
    'genre_types': ['genretypeid', 'genrelabel'],
    'language_types': ['languagetypeid', 'languagelabel'],
    'link_types': ['linktypeid', 'linkcategoryname'],
    'network_types': ['networktypeid', 'networkname'],
    'production_company_types': ['productioncompanytypeid', 'producername'],
    'production_country_types': ['productioncountrytypeid', 'countryofproduction'],
    'origin_country_types': ['origincountrytypeid', 'originalcountryname'],
    'spoken_language_types': ['spokenlanguagetypeid', 'languagespoken'],
    'created_by_types': ['createdbyid', 'creatorname'],
    'shows': [
        'showid', 'name', 'numberofseasons', 'numberofepisodes', 'overview',
        'adult', 'inproduction', 'originalname', 'popularity', 'tagline',
        'episoderuntime', 'statusid', 'typeid'
    ],
    'genres': ['showid', 'genretypeid'],
    'languages': ['showid', 'languagetypeid'],
    'links': ['linktypeid', 'showid', 'linkname'],
    'networks': ['showid', 'networktypeid'],
    'production_companies': ['showid', 'productioncompanytypeid'],
    'production_countries': ['showid', 'productioncountrytypeid', 'origincountrytypeid'],
    'spoken_languages': ['showid', 'spokenlanguagetypeid'],
    'show_votes': ['votecount', 'voteaverage', 'showid'],
    'created_bys': ['showid', 'createdbyid'],
    'air_dates': ['isfirst', 'showid', 'date']
}



def create_connection():
    dbconnection = None
    try:
        dbconnection = psycopg2.connect(
            dbname="Tobi Ajayi",
            user="Tobi Ajayi",  
            password="12345", 
            host="localhost"
        )
    except OperationalError as e:
        print(f"An error occurred: {e}")
    return dbconnection


def insert_data(dbconnection):
    print("Which table would you like to insert into?")
    for idx, table in enumerate(table_info.keys(), start=1):  
        print(f"{idx}. {table}")
    table_choice = int(input("Enter the number of the table: "))
    
    table_name = list(table_info.keys())[table_choice - 1]
    columns = table_info[table_name]
    
    print(f"Inserting into {table_name}.")
    values = []
    for col in columns:
        value = input(f"Enter {col}: ")
        values.append(value)

    sql_query = sql.SQL('INSERT INTO {table} ({fields}) VALUES ({values})').format(
        table=sql.Identifier(table_name),
        fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
        values=sql.SQL(', ').join(sql.Placeholder() * len(columns)) 
    )

    cur = dbconnection.cursor()
    try:
        cur.execute(sql_query, values)
        dbconnection.commit()
        print(f"Data inserted into {table_name} successfully.")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        dbconnection.rollback() 
        reset_connection(dbconnection)
    finally:
        cur.close()





def delete_data(dbconnection):
    print("Which table would you like to delete from?")
    for idx, table in enumerate(table_info.keys(), 1):
        print(f"{idx}. {table}")
    table_choice = int(input("Enter the number of the table: "))
    
    table_name = list(table_info.keys())[table_choice - 1]
    
    print(f"Delete from {table_name}.")
    condition = input("Enter the condition (e.g., 'column_name = value'): ")
    condition_value = input("Enter the value for the condition: ")

    sql = f'DELETE FROM {table_name} WHERE {condition} = %s'
    cur = dbconnection.cursor()

    try:
        cur.execute(sql, (condition_value,))
        dbconnection.commit()
        print(f"Record(s) deleted successfully from {table_name}.")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        dbconnection.rollback() 
        reset_connection(dbconnection)
    finally:
        cur.close()


def update_data(dbconnection):
    print("Which table would you like to update?")
    for idx, table in enumerate(table_info.keys(), 1):
        print(f"{idx}. {table}")
    table_choice = int(input("Enter the number of the table: "))
    
    table_name = list(table_info.keys())[table_choice - 1]
    
    set_clause = input("Enter the SET clause (e.g., 'column1 = new_value'): ")
    set_value = input("Enter the new value for the set clause: ")
    condition = input("Enter the condition for the update (e.g., 'id = 4'): ")
    condition_value = input("Enter the value for the condition: ")

    sql = f'UPDATE {table_name} SET {set_clause} = %s WHERE {condition} = %s'
    cur = dbconnection.cursor()

    try:
        cur.execute(sql, (set_value, condition_value))
        dbconnection.commit()
        if cur.rowcount > 0:
            print("Record(s) updated successfully.")
        else:
            print("No records were updated. Please check your condition.")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        dbconnection.rollback() 
        reset_connection(dbconnection)
    finally:
        cur.close()

def search_data(dbconnection):
    print("Which table would you like to search in?")
    for idx, table in enumerate(table_info.keys(), start=1):
        print(f"{idx}. {table}")
    table_choice = int(input("Enter the number of the table: "))
    
    table_name = list(table_info.keys())[table_choice - 1]
    
    print(f"Enter the search criteria for the {table_name} table.")
    column_name = input("Enter the column name to search (e.g., 'statuslabel'): ")
    search_value = input("Enter the search value (will automatically be wrapped with %): ")

    sql = f'SELECT * FROM {table_name} WHERE {column_name} LIKE %s'
    search_pattern = f'%{search_value}%' 
    
    cur = dbconnection.cursor()

    try:
        cur.execute(sql, (search_pattern,))  
        rows = cur.fetchall()
        print(f"Found {len(rows)} record(s):")
        for row in rows:
            print(row)
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        dbconnection.rollback() 
        reset_connection(dbconnection)
    finally:
        cur.close()




def perform_aggregation(dbconnection):
    print("Which table would you like to perform aggregation on?")
    for idx, table in enumerate(table_info.keys(), 1):
        print(f"{idx}. {table}")
    table_choice = int(input("Enter the number of the table: "))

    table_name = list(table_info.keys())[table_choice - 1]
    
    column = input(f"Enter the column to aggregate: ")
    print("Which aggregate function would you like to perform?")
    print("1. SUM")
    print("2. AVG")
    print("3. COUNT")
    print("4. MIN")
    print("5. MAX")
    agg_choice = input("Enter your choice (1-5): ")

    agg_functions = {
        '1': 'SUM',
        '2': 'AVG',
        '3': 'COUNT',
        '4': 'MIN',
        '5': 'MAX'
    }
    
    agg_function = agg_functions[agg_choice]

    sql = f'SELECT {agg_function}({column}) FROM {table_name}'
    cur = dbconnection.cursor()

    try:
        cur.execute(sql)
        result = cur.fetchone()
        print(f"{agg_function} of {column} in {table_name} is: {result[0]}")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        dbconnection.rollback() 
        reset_connection(dbconnection)
    finally:
        cur.close()



def sort_data(dbconnection):
    print("Which table would you like to sort data in?")
    for idx, table in enumerate(table_info.keys(), 1):
        print(f"{idx}. {table}")
    table_choice = int(input("Enter the number of the table: "))

    table_name = list(table_info.keys())[table_choice - 1]
    
    column = input("Enter the column to sort by: ")
    print("Choose sort direction:")
    print("1. Ascending (ASC)")
    print("2. Descending (DESC)")
    direction_choice = input("Enter your choice (1-2): ")

    direction = "ASC" if direction_choice == "1" else "DESC"

    sql = f'SELECT * FROM {table_name} ORDER BY {column} {direction}'
    cur = dbconnection.cursor()

    try:
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        dbconnection.rollback() 
        reset_connection(dbconnection)
    finally:
        cur.close()


def perform_join(dbconnection):
    print("Available tables for JOIN operation:")
    for idx, table in enumerate(table_info.keys(), start=1):
        print(f"{idx}. {table}")
    
    table1_choice = int(input("Enter the number of the first table: "))
    table2_choice = int(input("Enter the number of the second table: "))
    
    table1_name = list(table_info.keys())[table1_choice - 1]
    table2_name = list(table_info.keys())[table2_choice - 1]
    
    join_column = input("Enter the column name to join on (assumed same in both tables): ")
    
    sql = f'''SELECT *
              FROM {table1_name}
              INNER JOIN {table2_name}
              ON {table1_name}.{join_column} = {table2_name}.{join_column}
              LIMIT 6''' 
    cur = dbconnection.cursor()

    try:
        cur.execute(sql)
        rows = cur.fetchall()
        print(f"Joined data ({len(rows)} records):")
        for row in rows:
            print(row)
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        dbconnection.rollback() 
        reset_connection(dbconnection)
    finally:
        cur.close()


def group_data(dbconnection):
    print("Available tables for GROUP BY operation:")
    for idx, table in enumerate(table_info.keys(), 1):
        print(f"{idx}. {table}")
    
    table_choice = int(input("Enter the number of the table: "))
    table_name = list(table_info.keys())[table_choice - 1]
    
    group_column = input("Enter the column name to group by: ")
    print("Choose the aggregate function to apply:")
    print("1. COUNT")
    print("2. SUM")
    print("3. AVG")
    print("4. MIN")
    print("5. MAX")
    agg_choice = input("Enter your choice (1-5): ")

    agg_function = ['COUNT', 'SUM', 'AVG', 'MIN', 'MAX'][int(agg_choice) - 1]

    sql = f'SELECT {group_column}, {agg_function}({group_column}) FROM {table_name} GROUP BY {group_column}'
    cur = dbconnection.cursor()

    try:
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        dbconnection.rollback() 
        reset_connection(dbconnection)
    finally:
        cur.close()



def perform_subqueries(dbconnection):
    print("Available tables for performing subqueries:")
    for idx, table in enumerate(table_info.keys(), 1):
        print(f"{idx}. {table}")

    main_table_choice = int(input("Enter the number of the main table: "))
    sub_table_choice = int(input("Enter the number of the table for the subquery: "))

    main_table_name = list(table_info.keys())[main_table_choice - 1]
    sub_table_name = list(table_info.keys())[sub_table_choice - 1]

    subquery_column = input("Enter the column used in the subquery condition: ")

    sql = f'''SELECT * FROM {main_table_name}
              WHERE {subquery_column} IN
              (SELECT {subquery_column} FROM {sub_table_name})
              LIMIT 6'''
    cur = dbconnection.cursor()

    try:
        cur.execute(sql)
        rows = cur.fetchall()
        if rows:
            print(f"Found {len(rows)} record(s) based on the subquery condition:")
            for row in rows:
                print(row)
        else:
            print("No records found based on the subquery condition.")
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        dbconnection.rollback() 
        reset_connection(dbconnection)
    finally:
        cur.close()

def perform_transactions(dbconnection):
    while True:
        print("""
        Transaction Menu:
        1. Begin Transaction
        2. Commit Transaction
        3. Rollback Transaction
        4. Return to Main Menu
        """)
        choice = input("Enter your choice: ")
        if choice == "1":
            begin_transaction(dbconnection)
        elif choice == "2":
            commit_transaction(dbconnection)
        elif choice == "3":
            rollback_transaction(dbconnection)
        elif choice == "4":
            print("Returning to main menu...")
            break
        else:
            print("Invalid choice. Please try again.")

def begin_transaction(dbconnection):
    try:
        dbconnection.commit() 
        dbconnection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
        print("Transaction started. You can now perform operations before committing.")
    except psycopg2.Error as e:
        print(f"Failed to start transaction: {e}")

def commit_transaction(dbconnection):
    try:
        dbconnection.commit()
        print("Transaction committed successfully.")
    except psycopg2.Error as e:
        print(f"Failed to commit transaction: {e}")

def rollback_transaction(dbconnection):
    try:
        dbconnection.rollback()
        print("Transaction rolled back.")
    except psycopg2.Error as e:
        print(f"Failed to roll back transaction: {e}")

def reset_connection(dbconnection):
    try:
        dbconnection.reset() 
    except psycopg2.Error as e:
        print(f"Failed to reset the database connection: {e}")



def handle_error(dbconnection):
    pass

def main():
    dbconnection = create_connection()

    menu_options = {
        1: insert_data,
        2: delete_data,
        3: update_data,
        4: search_data,
        5: perform_aggregation,
        6: sort_data,
        7: perform_join,
        8: group_data,
        9: perform_subqueries,
        10: perform_transactions,
        11: handle_error,
        12: exit
    }

    if dbconnection:
        try:
            while True:
                print("""
                Welcome to the Database CLI Interface!

                Please select an option:
                1. Insert Data
                2. Delete Data
                3. Update Data
                4. Search Data
                5. Aggregate Functions
                6. Sorting
                7. Joins
                8. Grouping
                9. Subqueries
                10. Transactions
                11. Error Handling
                12. Exit
                """)

                choice = int(input("Enter your choice (1-12): "))
                
                if choice in menu_options:
                    if choice == 12:
                        print("Exiting the application...")
                        break
                    else:
                        menu_options[choice](dbconnection)
                else:
                    print("Invalid choice. Please try again.")
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            dbconnection.close()
            print("Database connection closed.")
    else:
        print("Failed to connect to the database. Please check the connection settings.")

if __name__ == '__main__':
    main()

