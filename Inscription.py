from client import Client


class Inscription:
    def __init__(self, user_id, group_id, activity_name, status):
        self.user_id = user_id
        self.group_id = group_id
        self.activity_name = activity_name
        self.status = status

    @staticmethod
    def creer_nouveau_client(matricule, nom, prenom, adresse, email, mot_de_passe):
        nouveau_client = Client(matricule, nom, prenom, adresse, email, mot_de_passe)
        return nouveau_client
