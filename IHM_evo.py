#---------------------- Projet CPI2-02 ----------------------#
#---------------------- Jilian Jouault / Maxime Bacq / Antone Bograt / Hamel Nino ----------------------#
#---------------------- Réalisation : Décembre 2020 / Janvier 2021 ----------------------#

#---------------------- Import des plugins ----------------------#
from turtle import *
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import json, sys, os, random

#---------------------- Gestion des erreurs ----------------------#

def affiche_erreur (str_error):
    global error_Label

    error_Label.configure(text=str_error)

#---------------------- Gestion des fichiers ----------------------#

def ouverture_fichier(nom_entree):
    global errno
    global entree

    if not(entree):
        nom_entree = nom_entree

    try:
        with open(nom_entree): pass
    except IOError:
        errno = -1
        print("Le fichier " + nom_entree + " n'existe pas.")
        affiche_erreur("Le fichier " + nom_entree + " n'existe pas.")
        nom_entree = ""
        entree = False
        errno = -1
        #sys.exit()
    return nom_entree

def test_fichier(p):
    global errno
    try:
        axiome = p['axiome']
    except KeyError:
        print("Il n'y a pas d'axiome dans le fichier.")
        affiche_erreur("Il n'y a pas d'axiome dans le fichier.")
        errno = -1
        #sys.exit()
    try:
        niveau = int(p['niveau'])
    except KeyError or ValueError:
        print("Il n'y a pas de niveau dans le fichier ou est écrit incorrectement.")
        affiche_erreur("Il n'y a pas de niveau dans le fichier ou est écrit incorrectement.")
        errno = -1
        #sys.exit()
    try:
        taille = int(p['taille'])
    except KeyError or ValueError:
        print("Il n'y a pas de taille dans le fichier ou est écrit incorrectement.")
        affiche_erreur("Il n'y a pas de taille dans le fichier ou est écrit incorrectement.")
        errno = -1
        #sys.exit()
    try:
        angle = float(p['angle'])
    except KeyError or ValueError:
        print("Il n'y a pas d'angle dans le fichier ou est écrit incorrectement.")
        affiche_erreur("Il n'y a pas d'angle dans le fichier ou est écrit incorrectement.")
        errno = -1
        #sys.exit()
    return axiome, niveau, taille, angle

def lire_fichier(nom_entree):
    global errno

    #paramètres de base
    variable = []
    regle = []
    retour = False
    axiome = ""
    niveau = 0
    taille = 0
    angle = 0

    if (nom_entree!="") and (errno == 0):
        with open(nom_entree) as lsystem:
            data = json.load(lsystem)
            for p in data:
                retour = test_fichier(p)
                axiome = retour[0]
                niveau = retour[1]
                taille = retour[2]
                angle = retour[3]

        for i in range(len(p['regle'])):
            compteur = 0
            for j, c in enumerate(p['regle'][i]):
                if c == "=":
                    compteur = compteur+1
                    index = j+1

            if compteur != 1:
                print("Erreur, nombre de = incorrect")
                affiche_erreur("Erreur, nombre de = incorrect")
                errno = -1
                #sys.exit()
            else:
                variable.append(p['regle'][i][0:index-1])
                regle.append(p['regle'][i][index:len(p['regle'][i])])
                #print(variable)
                #print(regle)

    return axiome, variable, regle, niveau, taille, angle

#---------------------- Traçage de la fractale ----------------------#

def traite_a(taille):
    print('pd()\nfd(' + str(taille) + ')\n')
    text.insert(INSERT, 'pd()\nfd(' + str(taille) + ')\n')
    text.see(END)
    if sortie == True:
        with open(nom_sortie, "a") as fichier_sortie:
            fichier_sortie.write('pd()\nfd(' + str(taille) + ')\n')

    if execution == True :
        tortue.pd()
        tortue.fd(taille)

def traite_b(taille):
    print('pu()\nfd(' + str(taille) + ')\n')
    text.insert(INSERT, 'pu()\nfd(' + str(taille) + ')\n')
    text.see(END)
    if sortie == True:
        with open(nom_sortie, "a") as fichier_sortie:
            fichier_sortie.write('pu()\nfd(' + str(taille) + ')\n')
    
    if execution == True :
        tortue.pu()
        tortue.fd(taille)

def traite_c(taille):
    print('pd()\nfd(' + str(taille) + ')\n')
    text.insert(INSERT, 'pd()\nfd(' + str(taille) + ')\n')
    text.see(END)
    if sortie == True:
        with open(nom_sortie, "a") as fichier_sortie:
            fichier_sortie.write('pd()\nfd(' + str(taille) + ')\n')

    if execution == True :
        tortue.pd()
        tortue.fd(taille)

def traite_plus(angle):
    print('right('+ str(angle) + ')\n')
    text.insert(INSERT, 'right('+ str(angle) + ')\n')
    text.see(END)
    if sortie == True:
        with open(nom_sortie, "a") as fichier_sortie:
            fichier_sortie.write('right('+ str(angle) + ')\n')

    if execution == True :
        tortue.right(angle)

def traite_moins(angle):
    print('left(' + str(angle) + ')\n')
    text.insert(INSERT, 'left(' + str(angle) + ')\n')
    text.see(END)
    if sortie == True:
        with open(nom_sortie, "a") as fichier_sortie:
            fichier_sortie.write('left(' + str(angle) + ')\n')
    if execution == True :
        tortue.left(angle)

def traite_sauve(saved_state, case):
    saved_state.append(get_turtle_state(tortue))
    return case + 1

def traite_restaure(saved_state, case):

    if execution == True :
        tortue.pu()
    restore_turtle_state(tortue, saved_state[case])
    print('pu()\nseth(' + str(saved_state[case][0]) + ')\nsetpos(' + str(saved_state[case][1][0]) + ',' + str(saved_state[case][1][1]) + ')\npd()\n')
    text.insert(INSERT, 'pu()\nseth(' + str(saved_state[case][0]) + ')\nsetpos(' + str(saved_state[case][1][0]) + ',' + str(saved_state[case][1][1]) + ')\npd()\n')
    text.see(END)
    if sortie == True:
        with open(nom_sortie, "a") as fichier_sortie:
            fichier_sortie.write('pu()\nseth(' + str(saved_state[case][0]) + ')\nsetpos(' + str(saved_state[case][1][0]) + ',' + str(saved_state[case][1][1]) + ')\npd()\n')
    saved_state.remove(saved_state[case])

    if execution == True :
        tortue.pd()
    return case - 1

def traite_etoile():
    print('right(''180'')\n')
    text.insert(INSERT, 'right(''180'')\n')
    if sortie == True:
        with open(nom_sortie, "a") as fichier_sortie:
            fichier_sortie.write('right(''180'')\n')

    if execution == True :
        tortue.right(180)

def traite_accolade(task, axiome):
    alea = random.randrange(1, 100, 1)
    acco = task
    if alea > 50:
        compte_acc = 0
        for task in range(acco, len(axiome)):
            if axiome[task] == "{":
                compte_acc = compte_acc + 1
            elif axiome[task] == "}":
                compte_acc = compte_acc - 1
                if compte_acc <= 0:
                    return task
    else:
        return task

#---------------------- Informations sur turtle ----------------------#

#récupère la postion et l'orientation de la tortue en un point x
def get_turtle_state(turtle):
    """ Return turtle's current heading and position. """
    return tortue.heading(), tortue.position()

#renvoie la tortue au point x avec la bonne orientation
def restore_turtle_state(turtle, state):
    """ Set the turtle's heading and position to the given values. """
    tortue.setheading(state[0])
    tortue.setposition(state[1][0], state[1][1])

#---------------------- Gestion fractale ----------------------#

def cree_fractale(axiome, variable, regle, niveau):
    #crée la fractale
    for i in range(niveau):
        nvlaxiome = ""
        for j in range(len(axiome)):
            if axiome[j] in variable:
                nvlaxiome = nvlaxiome + regle[variable.index(axiome[j])]
            else:
                nvlaxiome = nvlaxiome + axiome[j]
        axiome = nvlaxiome
            #print(axiome)
    #affiche cheminement finale de fractale
    #print(axiome)
    return axiome

def genere_fractale(axiome,taille,angle):
    global errno
    tortue.speed(0)
    #paramètres pour "[" et "]"
    saved_state = []
    case = -1
    task = 0
    while task < len(axiome) and errno == 0:
        if axiome[task] == "a":
            traite_a(taille)
        elif axiome[task] == "b":
            traite_b(taille)
        elif axiome[task] == "c":
            traite_c(taille)
        elif axiome[task] == "+":
            traite_plus(angle)
        elif axiome[task] == "-":
            traite_moins(angle)
        elif axiome[task] == "[":
            case = traite_sauve(saved_state, case)
        elif axiome[task] == "]":
            case = traite_restaure(saved_state, case)
        elif axiome[task] == "*":
            traite_etoile()
        elif axiome[task] == "{":
            task = traite_accolade(task, axiome)
        elif axiome[task] == "}":
            task = task
        else:
            print('Erreur : Caractère '+ axiome[task] +' invalide')
            affiche_erreur("Erreur : Caractère "+ axiome[task] +" invalide")
            errno = -1
            #sys.exit()
        task += 1

def dessine_fractale(axiome, taille, angle):
    global errno
    print('from turtle import *')
    print('color("black")')
    print('speed(10)')
    text.insert(INSERT, 'from turtle import *')
    text.insert(INSERT, 'color("black")')
    text.insert(INSERT, 'speed(10)')
    

    if sortie == True:
        with open(nom_sortie, "a") as fichier_sortie:
                fichier_sortie.write('from turtle import *\ncolor("black")\nspeed(10)\ntitle("' + nom_sortie + '")\n')
    genere_fractale(axiome,taille,angle)
    if errno == 0:
        print('hideturtle()\nexitonclick()')
        text.insert(INSERT,'hideturtle()\nexitonclick()')
        if sortie == True:
            with open(nom_sortie, "a") as fichier_sortie:
                    fichier_sortie.write('hideturtle()\nexitonclick()\n')
        #quitter uniquement quand l'utilisateur le désire
        tortue.hideturtle()

#---------------------- Bonus arguments ----------------------#

def traite_args():  
    args = []
    nom_entree = ''
    nom_sortie = ''
    fichier_sortie = ''
    entree = False
    sortie = False
    execution = False
    for arg in sys.argv:
        args.append(arg)
    i = len(args)
    if i > 1:
        j = 1
        while j < i:
            if args[j] == "-i" and i > j + 1:
                nom_entree = args[j+1]
                try:
                    with open(args[j+1]): pass
                except IOError:
                    print("Le fichier " + args[j+1] + " n'existe pas.")
                    sys.exit()
                entree = True
                j = j + 2
            elif args[j] == "-o":
                temp = nom_entree[::-1]
                temp1 = temp.replace("nosj.","yp.",1)
                nom_sortie = temp1[::-1]
                try:
                    with open(nom_sortie, "w") as fichier_sortie: pass
                except OSError:
                    print("Le nom du fichier " + nom_sortie + " est incorrect.")
                    sys.exit()
                sortie = True
                j = j + 1
            elif args[j] == "-r":
                execution = True
                j = j + 1
            else:
                print("Erreur, mauvais arguments spécifiés en entrée : Saisir 'python test_arg.py -i nom_du_fichier_en_entrée -o -r'")
                sys.exit()
    return nom_sortie, fichier_sortie, sortie, nom_entree, entree, execution

#---------------------- Partie graphique ----------------------#

#clique sur "générer"
def click_generer() :

    global retour, en_cours, generer_Button, axiome_Button

    if en_cours == False :

        en_cours = True

        generer_Button.configure(state=DISABLED)
        axiome_Button.configure(state=DISABLED)

        tortue.clear()
        tortue.pu()
        tortue.home()
        tortue.st()
        dessine_fractale(cree_fractale(retour[0], retour[1], retour[2], retour[3]), retour[4], retour[5])

        axiome_Button.configure(state=ACTIVE)
        generer_Button.configure(state=ACTIVE)
        en_cours = False

#clique sur "nouvel_axiome"
def click_choisir_axiome() :
    global errno, generer_Button, input_Label, output_Label, sauve, dessine, nom_entree, nom_sortie, sortie, retour

    nom_entree = askopenfilename(title="Ouvrir un axiome",filetypes=[('json files','.json'),('Tous types','.*')])
    
    if nom_entree !="":
        retour = lire_fichier(ouverture_fichier(nom_entree))
        if errno==0:
            entree = True

            input_Label.config(text=nom_entree)
            sortie = (sauve.get() == 1)
            if sortie:
                temp = nom_entree[::-1]
                temp1 = temp.replace("nosj.","yp.",1)
                nom_sortie = temp1[::-1]
                output_Label.config(text=nom_sortie)
            execution = (dessine.get() == 1)
            generer_Button.configure(state=ACTIVE,bg="grey",fg="black")
    else:
        nom_sortie = ""
        generer_Button.configure(state=DISABLED,bg="grey",fg="black")
        input_Label.config(text="LSystem non sélectionné")
        sortie = (sauve.get() == 1)
        if sortie:
            output_Label.config(text="LSystem non sélectionné")
        else:
            output_Label.config(text="Pas de sauvegarde")

#clique sur "Sauvegarde prg"
def click_sauver() :
    global output_Label, sauve, nom_entree, nom_sortie, sortie

    sortie = (sauve.get() == 1)
    if sortie:
        if nom_entree !="":
            temp = nom_entree[::-1]
            temp1 = temp.replace("nosj.","yp.",1)
            nom_sortie = temp1[::-1]
            output_Label.config(text=nom_sortie)
        else:
            output_Label.config(text="LSystem non sélectionné")
    else:
        output_Label.config(text="Pas de sauvegarde")

#clique sur "Dessiner la fractale"
def click_dessiner() :
    
    global dessine, execution

    execution = dessine.get() == 1

#clique sur "effacer"
def click_effacer() :
    tortue.clear()
    text.delete("1.0", "end")

#clique sur "quitter"
def click_quitter() :
    canvas.destroy()
    canvas.quit()  

#la plupart des objets IHM
def IHM():
    global generer_Button, error_Label, input_Label, output_Label, sortie, axiome_Button

    #affiche la zone de dessin
    canvas.grid(padx=2, pady=2, row=0, column=0, rowspan=10, columnspan=10)

    #choisis un nouvel axiome
    axiome_Button = Button(master = window, text ="Choisir un LSystem", command = click_choisir_axiome, state=ACTIVE)
    axiome_Button.config(bg="grey",fg="black")
    axiome_Button.grid(padx=2, pady=2, row=0, column=10)

    #efface l'écran
    effacer_Button = Button(master = window, text ="Effacer", command = click_effacer)
    effacer_Button.config(bg="grey",fg="black")
    effacer_Button.grid(padx=2, pady=2, row=0, column=14)

    #affiche le chemin et le nom de fichier LSystem sélectionné
    input_Label = Label(master = window, text = "LSystem non sélectionné", height=1)
    input_Label.grid(padx=2, pady=2, row=1, column=10, columnspan=10)
    if nom_entree != "":
        input_Label.config(text=nom_entree)
    
    #affiche le chemin et le nom de fichier de sauvegarde
    output_Label = Label(master = window, text = "Pas de sauvegarde", height=1)
    output_Label.grid(padx=2, pady=2, row=2, column=10, columnspan=10)
    
    #affiche le terminal
    canvas_text.grid(padx=2, pady=2, row=3, column=10, rowspan=8, columnspan=10)
    text.pack(side="left")

    #barre de défilement à côté du terminal graphique
    scroll_y = Scrollbar(master= canvas_text, orient="vertical", command=text.yview)
    scroll_y.pack(side="left", expand=True, fill="y")

    text.configure(yscrollcommand=scroll_y.set)

    #affiche les messages d'erreur
    error_Label = Label(master = window, text = "", height=1, fg="red")
    error_Label.grid(padx=2, pady=2, row=9, column=10, columnspan=8)
    
   #quitte le programme
    quitter_Button = Button(master = window, text ="Quitter", command = click_quitter)
    quitter_Button.config(bg="grey",fg="black")
    quitter_Button.grid(padx=2, pady=2, row=9, column=14)

    if sortie == True:
        fichier_sortie.close()
        click_sauver()

    if execution == True:
        click_generer()

    canvas_text.mainloop()

#les variables de l'IHM --> les boutons grisés / les cases à cocher
def IHM_Var():

    global sauve, dessine, generer_Button, retour

    sauve = IntVar()
    Sauve_Coche = Checkbutton(master = window, text="Sauvegarder le programme PYTHON", variable=sauve, justify='left', command=click_sauver)
    Sauve_Coche.grid(padx=2, pady=2, row=0, column=11)

    dessine = IntVar()
    Dessine_Coche = Checkbutton(master = window, text="Dessiner la fractal", variable=dessine, justify='left', command = click_dessiner)
    Dessine_Coche.grid(padx=2, pady=2, row=0, column=12)

    #génère un nouvel l-system
    generer_Button = Button(master = window, text ="Générer", command = click_generer, state=DISABLED)
    generer_Button.config(bg="grey",fg="black")
    generer_Button.grid(padx=2, pady=2, row=0, column=13)

    if entree == True :
        generer_Button.configure(state=ACTIVE,bg="grey",fg="black")
        retour = lire_fichier(ouverture_fichier(nom_entree))

    if sortie == True :
        Sauve_Coche.select()

    if execution == True :
        Dessine_Coche.select()

#Effacement de la fenêtre du terminal
os.system("cls")

#---------------------- Début programme ----------------------#

#detection des arguments et initialisation de ceux-ci
en_cours = False
errno = 0
retour = traite_args()
nom_sortie = retour[0]
fichier_sortie = retour[1]
sortie = retour[2]
nom_entree = retour[3]
entree = retour[4]
execution = retour[5]

#on créer la fenêtre Tkinter
window = Tk()
canvas = Canvas(master = window, width = 800, height = 800)

#permet de placer turtle sur notre fenêtre tk 
tortue = RawTurtle(canvas)

#créer le terminal
canvas_text = Canvas(master = window, width = 800, height = 800)
text = Text(canvas_text)

#les parties qui vont varier dans l'IHM
IHM_Var()

#lance l'IHM
IHM()
