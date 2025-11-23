import veicolo
class Auto(veicolo.Veicolo):
    def __init__(self,n_ruote, marca,n_portiere):
        super().__init__(n_ruote, marca)
        self.n_portiere = n_portiere
        