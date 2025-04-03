"""
comme on insère 10 000 mots dans une filtre de taille 100 à 1000 , la filtre serait 
saturée de 1 et donne un taux de faux positif de 100%


"""

import random

# matplolib.pyplot pour les courbes 
import matplotlib.pyplot as plt

def creerTeta(nombreFonction):
    #création d'une liste de tetas  afin de le pouvoir varier 
    # teta ne sera pas proche de 1 ni de 0 , donc j'estime que si teta est entre 0.3 et 0.7
    tetas = [random.uniform(0.3, 0.7) for _ in range(nombreFonction)]
    return tetas


#on a notre classe filtre de bloom qui prend en parametre la taille du filtre, le nombre de mot, le nombre de mot test et le nombre de fonction de hachage
class FiltreBloom:
    def __init__(self, taille, nombreMot,nombreMotTest,nombreFonction,tetas):
        #notre mot ne sera composé que de lettre minuscule
        self.lettre = "abcdefghijklmnopqrstuvwxyz"
        
        self.nombreMot = nombreMot
        self.nombreMotTest = nombreMotTest
        self.nombreFonction = nombreFonction
        
        #la taille du mot aléatoire sera de 5 afin d'obtenir des résultats plus concrètes
        self.motAleatoire = self.motAleatoire(5)
        self.motTest = self.motAleatoireTest(5)
        
        self.tetas = tetas


        #initialisation du filtre à partir de la taille
        self.filtre = [0] * taille

        #ajout des éléments dans le filtre
        for mot in self.motAleatoire:
            self.ajouter_mot(mot)

    def motAleatoire(self, taille):
        #création d'une liste de mot aleatoire a partir de la taille du mot et le nombre de mot
        L = []
        for i in range(self.nombreMot):
            mot = ''.join(random.choice(self.lettre) for i in range(taille))
            L.append(mot)
        return L

    def motAleatoireTest(self, taille):
        #meme principe que motAleatoire mais pour les mots qu'on va tester
        L = []
        #tant que la taille de la liste est inférieur au nombre de mot test
        while len(L) < self.nombreMotTest:
            mot = ''.join(random.choice(self.lettre) for i in range(taille))
            #on vérifie que le mot à ajouter n'est pas dans la liste de mot aléatoire
            if mot not in self.motAleatoire:
                L.append(mot)
        return L
    def transformerEnEntier(self, mot):
        #on transforme le mot en entier
        #on encode le mot puis on le transforme en entier afin de bien distribuer les valeurs
        
        mot = mot.encode()
        mot = int.from_bytes(mot, byteorder='little')
        
        return mot
      

    def hachage(self, mot,teta):
        #on hache le mot en utilisant la fonction de hachage par multiplication
        mot = self.transformerEnEntier(mot)
        #recuperation de la partie decimale
        h = (mot * teta) % 1
        # recuperation de la partie entiere
        h = int(h * len(self.filtre))
        return h

    def ajouter_mot(self, mot):
        #ajout du mot dans le filtre à partir du nombre de fonction de hachage
        
        for i in range(self.nombreFonction):
            indices = self.hachage(mot,self.tetas[i])
            self.filtre[indices] = 1


    def verifier_mot(self, mot):
        # pour verifier si le mot est dans le filtre on verifie
        # si les valeurs des indices des fonctions de hachage sont égales à 1
        vrai = True;
        for teta in self.tetas:
            indices = self.hachage(mot,teta)
            vrai = vrai and (self.filtre[indices] == 1)
        return vrai

    def calculer_faux_positifs(self):
        # pour calculer le taux de faux positifs on verifie si les mots testés sont dans le filtre
        faux_positifs = 0
        for mot in self.motTest:
            if self.verifier_mot(mot):
                faux_positifs += 1
        return faux_positifs



def main():
    #initialisation
    nombreMots = int(input("saisissez le nombre de mots : "))
    nombreMotsTest = 1000
    taillesFiltre = range(1000, 10001, 1000)
    #10001 pour que 10000 soit inclus dans la boucle
    nombreFonctions = range(2, 9)


    #faire le test
    for nombreFonction in nombreFonctions:
        tauxFauxPositifs = []
        for tailleFiltre in taillesFiltre:
            #on initialise un objet FiltreBloom puis on calcule son nombre de faux positif 
            #et on ajoute dans la liste son pourcentage
            tetas = creerTeta(nombreFonction)
            filtre = FiltreBloom(tailleFiltre, nombreMots, nombreMotsTest, nombreFonction, tetas)
            fauxPositifs = filtre.calculer_faux_positifs()
            tauxFauxPositifs.append(fauxPositifs / nombreMotsTest * 100)
            print(f'pour {nombreFonction} fonctions de hachage et la taille du filtre {tailleFiltre},le taux de faux positifs est de {fauxPositifs / nombreMotsTest * 100}%')

    plt.xlabel('Taille du filtre')
    plt.ylabel('Taux de faux positifs (%)')
    plt.title(f'Taux de faux positifs en fonction de la taille du filtre pour différentes fonctions de hachage pour {nombreMots} mots')
    plt.legend()
    plt.show()

main()



