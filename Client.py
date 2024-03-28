from database import execute_query

class Client:
    def __init__(self, user_id=None):
        self.user_id = user_id

    @staticmethod
    def verify_user(username, password):
        query = "SELECT user_id FROM users WHERE username=? AND password=?"
        user = execute_query(query, (username, password)).fetchone()
        return user[0] if user else None

    def register_activity(self, activity_id):
        if not self.user_id:
            raise Exception("Client not logged in.")
        query = "INSERT INTO registrations (user_id, activity_id, status) VALUES (?, ?, 'registered')"
        execute_query(query, (self.user_id, activity_id))