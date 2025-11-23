import veicolo
class Camion(veicolo.Veicolo):
    def __init__(self,n_ruote, marca, portatta_di_traino):
        super().__init__(n_ruote, marca)
        self.portatta_di_traino = portatta_di_traino
        