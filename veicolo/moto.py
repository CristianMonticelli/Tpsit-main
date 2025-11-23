import veicolo
class Moto(veicolo.Veicolo):
    def __init__(self,n_ruote, marca, cilindrata):
        super().__init__(n_ruote, marca)
        self.cilindrata = cilindrata
        