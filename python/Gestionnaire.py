class Gestionnaire:
    def __init__(self, matricule, nom, prenom, adresse, email, mot_de_passe):
        self.matricule = matricule
        self.nom = nom
        self.prenom = prenom
        self.adresse = adresse
        self.email = email
        self.mot_de_passe = mot_de_passe

    def gerer_activites(self, activites):
        # Méthode pour gérer les activités du centre sportif (ajout, modification, annulation, consultation)
        pass

    def gerer_groupes(self, groupes):
        # Méthode pour gérer les groupes d'activités offertes (ajout, modification, annulation, consultation)
        pass

    def consulter_disponibilites_moniteur(self, moniteur):
        # Méthode pour consulter les disponibilités d'un moniteur spécifique
        pass

    def deposer_message_moniteur(self, moniteur, message):
        # Méthode pour déposer un message à un moniteur spécifique
        pass
