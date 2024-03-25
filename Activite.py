class Activite:
    def __init__(self, nom, description, horaires, capacite_max):
        self.nom = nom
        self.description = description
        self.horaires = horaires
        self.capacite_max = capacite_max
        self.inscrits = []

    def ajouter_inscription(self, client):
        if len(self.inscrits) < self.capacite_max:
            self.inscrits.append(client)
            return True
        else:
            return False

    def supprimer_inscription(self, client):
        if client in self.inscrits:
            self.inscrits.remove(client)
            return True
        else:
            return False
