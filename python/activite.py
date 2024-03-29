from database import execute_query

class Activite:
    @staticmethod
    def get_activities():
            query = "SELECT activity_id, name FROM activities"
            activities = execute_query(query).fetchall()
            return activities

    @staticmethod
    def insert_activities(activities_to_insert):
            query = "INSERT INTO activities (name, description, min_participants, max_participants) VALUES (?, ?, ?, ?)"
            execute_query(query, activities_to_insert)