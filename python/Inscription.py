from client import Client


class Inscription:
    @staticmethod
    def creer_nouveau_client(matricule, nom, prenom, adresse, email, mot_de_passe):
        nouveau_client = Client(matricule, nom, prenom, adresse, email, mot_de_passe)
        return nouveau_client
