import psycopg2
import psycopg2.extras

class DatabaseManager:
    def __init__(self, hostname, database, username, password, port_id):
        self.hostname = hostname
        self.database = database
        self.username = username
        self.password = password
        self.port_id = port_id
        self.conn = None
        self.cur = None
    ## connect to database
    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.hostname,
                dbname=self.database,
                user=self.username,
                password=self.password,
                port=self.port_id
            )
            self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except Exception as error:
            print(f"Error connecting to the database: {error}")
    ## close Database
    def close(self):
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()
    ## create tables
    def create_tables_if_not_exists(self):
        create_main_history_table = '''
        CREATE TABLE IF NOT EXISTS user_history (
            id_user SERIAL PRIMARY KEY,
            name TEXT,
            converstion_ids INTEGER [],
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        '''
        create_converstion_table = '''
        CREATE TABLE IF NOT EXISTS converstion (
            converstion_id SERIAL PRIMARY KEY,
            history_arry TEXT [],
            last_summary TEXT,
            id_user INTEGER REFERENCES user_history(id_user)
        );
        '''
        create_masseges_table = '''
        CREATE TABLE IF NOT EXISTS masseges (
            chat_id SERIAL PRIMARY KEY,
            converstion_id INTEGER,
            human_chat TEXT,
            human_chat_token INTEGER,
            date_human DEFAULT CURRENT_TIMESTAMP,
            ai_chat TEXT,
            ai_chat_token INTEGER,
            date_ai DEFAULT CURRENT_TIMESTAMP,
            summary TEXT,
            summary_token INTEGER,
            data JSONB,
            id_user INTEGER REFERENCES user_history(id_user),
            id_converstion INTEGER REFERENCES converstion(converstion_id)
        );
        '''

        # Execute the table creation queries
        self.execute_query(create_main_history_table)
        self.execute_query(create_converstion_table)
        self.execute_query(create_masseges_table)
    ## delete Tables
    def delete_tables_if_exists(self):
        drop_masseges_table = '''
        DROP TABLE IF EXISTS masseges;
        '''
        
        create_converstion_table = '''
        DROP TABLE IF EXISTS converstion;
        '''

        create_user_history_table = '''
        DROP TABLE IF EXISTS user_history;
        '''

        # Execute the table deletion queries
        self.execute_query(drop_masseges_table)
        self.execute_query(create_converstion_table)
        self.execute_query(create_user_history_table)

    ## Execute querys
    def execute_query(self, query, values=None):
        try:
            if values:
                self.cur.execute(query, values)
            else:
                self.cur.execute(query)
            self.conn.commit()
        except Exception as error:
            print(f"Error executing query: {error}")
            self.conn.rollback()

    ## Fetch ONE for database
    def fetch_one(self):
        return self.cur.fetchone()
    ## Fetch all for database
    def fetch_all(self):
        return self.cur.fetchall()
    
    ## Check_id
    def check_id(self, id_user, converstion_id):
        self.execute_query('''SELECT 
                                id_user,
                                CASE
                                    WHEN %s = ANY(converstion_ids) THEN %s
                                    ELSE NULL
                                END AS converstion_id
                            FROM 
                                user_history
                            WHERE 
                                id_user = %s;
               ''',(converstion_id, id_user))
        result = self.fetch_all()
        return result
        # if result == []:
        #     return False 
        # elif isinstance(result, list) and result:
        #     return result[0]
        # else:
        #     return False
    ## Create New User
    def create_user(self, id_user, name, converstion_ids):
        self.execute_query('INSERT INTO user_history (id_user, name, converstion_ids) VALUES (%s, %s, %s)',
                           (id_user, name, converstion_ids))
    ## Insert Human
    def human_chat(self, human_chat, human_chat_token, id_user, id_conversation, summary=None, summary_token=None):
        if summary: 
            self.execute_query(
                '''
                INSERT INTO messages (human_chat, human_chat_token, summary, summary_token, id_user, id_conversation) 
                VALUES (%s, %s, %s, %s, %s, %s)
                ''',
                (human_chat, human_chat_token, summary, summary_token, id_user, id_conversation)
            )
        else:
            self.execute_query(
                '''
                INSERT INTO messages (human_chat, human_chat_token, id_user, id_conversation) 
                VALUES (%s, %s, %s, %s)
                ''',
                (human_chat, human_chat_token, id_user, id_conversation)
            )
    ## Fetch chat for summary
    def summary_by(self, summary_mode, number_chat=None, token_number=1500, id_conversation=None):
        """Generates a summary based on the provided mode."""
        if summary_mode not in ['default', 'token', 'chat']:
            raise ValueError("Invalid summary mode provided. Choose 'default', 'token', or 'chat'.")

        query = """
            SELECT chat_id, human_chat, ai_chat, human_chat_token, ai_chat_token
            FROM messages
            WHERE id_conversation = %s
            ORDER BY chat_id DESC
        """
        self.execute_query(query, (id_conversation,))
        rows = self.fetch_all()

        if summary_mode == 'default':
            # Limit by tokens (default 1500 tokens)
            total_tokens = 0
            selected_rows = []
            for row in rows:
                total_tokens += row['human_chat_token'] + row['ai_chat_token']
                if total_tokens <= token_number:
                    selected_rows.append(row)
                else:
                    break
            return selected_rows

        elif summary_mode == 'token':
            # Similar to default, limit by a given token number
            total_tokens = 0
            selected_rows = []
            for row in rows:
                total_tokens += row['human_chat_token'] + row['ai_chat_token']
                if total_tokens <= token_number:
                    selected_rows.append(row)
                else:
                    break
            return selected_rows

        elif summary_mode == 'chat':
            # Limit by the number of chats
            return rows[:number_chat]


    ## Insert AI
    def ai_chat(self, id_conversation, ai_chat, ai_chat_token, data=None):
        if data:
            self.execute_query('''
                UPDATE messages
                SET ai_chat = %s, ai_chat_token = %s, data = %s
                WHERE id_conversation = %s
                ORDER BY date_ai DESC
                LIMIT 1
            ''', (ai_chat, ai_chat_token, data, id_conversation))
        else:
            self.execute_query('''
                UPDATE messages
                SET ai_chat = %s, ai_chat_token = %s
                WHERE id_conversation = %s
                ORDER BY date_ai DESC
                LIMIT 1
            ''', (ai_chat, ai_chat_token, id_conversation))

    ## check_and_insert_human_chat      
    def check_and_insert_human_chat(self, main_history_id, human, human_token, name=None, summary=None, summary_token=None):
        # Check if the ID exists
        id_exists = self.check_id(main_history_id)
        
        # If the ID doesn't exist, create a new user
        if id_exists is None:
            # Ensure a name is provided for creating a new user
            if name is None:
                raise ValueError("Name must be provided to create a new user if main_history_id does not exist.")
            
            # Create a new user
            self.create_user(main_history_id, name)
            id_exists = -1
        
        # Insert the human chat
        self.human_chat(main_history_id, id_exists+1, human, human_token, summary, summary_token)
    ## Insert Ai now
    def add_ai(self, main_history_id, ai, ai_token, data=None):

        id_exists = self.check_id(main_history_id)

        if id_exists is None:
            raise ValueError("Error NO user Exist With This ID")
        
        self.ai_chat(main_history_id, id_exists, ai, ai_token, data)
    ## fetch history
    def fetch_user_history(self, main_history_id, num_rows, include_summary=False):
        # Construct the query based on whether to include the summary
        if include_summary:
            self.execute_query('''
                SELECT human, ai, summary
                FROM user_history
                WHERE main_history_id = %s
                ORDER BY chat_id
                LIMIT %s
            ''', (main_history_id,num_rows))
        else:
            self.execute_query('''
                SELECT human, ai
                FROM user_history
                WHERE main_history_id = %s
                ORDER BY chat_id
                LIMIT %s
            ''', (main_history_id,num_rows))

        # Fetch all results
        results = self.fetch_all()

        # Initialize an empty string to build the formatted result
        formatted_output = ""

        # Iterate over the results to build the string
        for row in results:
            formatted_output += f"human: {row['human']}\n"
            formatted_output += f"ai: {row['ai']}\n"
            if include_summary and 'summary' in row:
                formatted_output += f"summary: {row['summary']}\n"
        
        return formatted_output


# Example usage
if __name__ == "__main__":
    db_manager = DatabaseManager(
        hostname='localhost',
        database='llm_history',
        username='postgres',
        password='1612',
        port_id=5433
    )

    db_manager.connect()

    db_manager.delete_tables_if_exists()

    db_manager.create_tables_if_not_exists()

    db_manager.check_and_insert_human_chat(1, 'human', 123, 'mohamed',summary='summ',summary_token=33)

    db_manager.add_ai(1, 'AI', 11)

    db_manager.check_and_insert_human_chat(1, 'human_1', 124)

    db_manager.add_ai(1, 'AI_1', 12)

    output_with_summary = db_manager.fetch_user_history(1, num_rows=5,include_summary=True)
    print(output_with_summary)

    db_manager.check_and_insert_human_chat(2, 'human_3', 126, 'Atrozy')

    db_manager.add_ai(2, 'AI_3', 14)

    db_manager.check_and_insert_human_chat(3, 'human_4', 126, 'Hassan')

    db_manager.add_ai(3, 'AI_4', 17)
  

    db_manager.close()
