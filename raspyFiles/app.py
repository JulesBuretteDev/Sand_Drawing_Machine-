from flask import Flask, render_template, request

app = Flask(__name__)

class Imprimante3DIHM:
    def __init__(self):
        self.position_extrudeur = (0, 0, 0)
        self.nom_imprimante = "Imprimante 3D"
        self.reglages = ["Réglage 1", "Réglage 2", "Réglage 3"]
        


@app.route('/')
def index():
    return render_template('index.html', position=imprimante.position_extrudeur, nom_imprimante=imprimante.nom_imprimante, reglages=imprimante.reglages)

@app.route('/envoyer_commande', methods=['POST'])
def envoyer_commande(self):
    commande = request.form['commande']
    print("Commande envoyée:", commande)
    # Ajoutez ici le code pour traiter la commande envoyée
    
    return render_template('index.html', position=imprimante.position_extrudeur, nom_imprimante=imprimante.nom_imprimante, reglages=imprimante.reglages)

imprimante = Imprimante3DIHM()

if __name__ == '__main__':
    app.run()
