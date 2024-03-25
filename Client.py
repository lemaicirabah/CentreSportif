class Client:
    def __init__(self, matricule, nom, prenom, adresse, email, mot_de_passe):
        self.matricule = matricule
        self.nom = nom
        self.prenom = prenom
        self.adresse = adresse
        self.email = email
        self.mot_de_passe = mot_de_passe
    def inscrire_activite(self, activite):
        # Méthode pour inscrire le client à une activité
        pass

    def annuler_inscription(self, activite):
        # Méthode pour annuler l'inscription du client à une activité
        pass

    def consulter_facture(self):
        # Méthode pour consulter la facture personnelle du client
        pass

    def consulter_horaire(self):
        # Méthode pour consulter l'horaire personnel des activités du client
        pass

    def modifier_profil(self, nouveau_nom, nouvelle_adresse, nouvel_email, nouveau_mot_de_passe):
        # Méthode pour modifier le profil du client
        self.nom = nouveau_nom
        self.adresse = nouvelle_adresse
        self.email = nouvel_email
        self.mot_de_passe = nouveau_mot_de_passe

    def consulter_infos_activites(self):
        # Méthode pour consulter les informations relatives aux activités du centre
        pass