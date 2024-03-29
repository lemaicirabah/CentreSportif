class Moniteur:
    def __init__(self, matricule, nom, prenom, adresse, email, mot_de_passe):
        self.matricule = matricule
        self.nom = nom
        self.prenom = prenom
        self.adresse = adresse
        self.email = email
        self.mot_de_passe = mot_de_passe

    def entrer_disponibilites(self, disponibilites):
        # Méthode pour entrer les disponibilités de travail du moniteur
        pass

    def consulter_horaire(self):
        # Méthode pour consulter l'horaire personnel de travail du moniteur
        pass

    def deposer_message(self, destinataire, message):
        # Méthode pour déposer un message à un destinataire spécifique (gestionnaire, administrateur, etc.)
        pass
