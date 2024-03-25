from Client import Client


class Inscription:
    @staticmethod
    def creer_nouveau_client(matricule, nom, prenom, adresse, email, mot_de_passe):
        # Cette méthode statique permet de créer un nouveau compte client
        nouveau_client = Client(matricule, nom, prenom, adresse, email, mot_de_passe)
        # Vous pouvez ajouter ici la logique pour sauvegarder le nouveau client dans la base de données ou le système de gestion des comptes
        return nouveau_client
