#!/usr/bin/env python
# coding: utf-8
# Projet du groupe : Siyu Wang et Natia Davitashvili
import json
import re
import treetaggerwrapper

# ----------------- gestion de fichiers ----------------------------

# LIRE DES FICHIERS
def lireFichier (fichier) :

    with open (fichier , "r") as FI :
        texte = FI.readlines()
    return texte    


# ECRITURE DU TEXTE DANS UN FICHIER 
def ecritTexteDansFichier (texte, fichier) :

    with open (fichier, "w") as FI :
        FI.write (texte)

# ----------------------- Traitements TAL communs ---------------------------

# EXTRAIRE LES CONTENUS TEXTUELS DU FICHIER
def extraitTexteFichier (fichier) :
    texte = lireFichier (fichier)
    texte = "".join(texte)
        
    # suppression des balises xml  et des lignes vierges
    texte = re.sub (r'<[^>]+>', '', texte)
    texte = re.sub (r'\n+', '\n', texte)
    texte = re.sub(r"’","'",texte)

    return texte

# SUPPRIMER LES SIGNES DE PONCTUATIONS
def supprimPonct(texte):
    texte = "".join(c for c in texte if c not in ('!','.',':',',','«','?','»','(',')','-','\",','°'))
    return texte

# UTILISER TREETAGGER ET RENVOYER UNE LISTE DES MOTS TAGGÉS
def treetagger_tag(texte,langue):
    tagger=treetaggerwrapper.TreeTagger(TAGLANG=langue)
    tags=tagger.tag_text(texte)
    tags2=treetaggerwrapper.make_tags(tags)
    return tags2

# RÉCUPÉRER LES LEMMES DEPUIS LISTE DES TAGS ET RENVOYER UN DICTIONNAIRE DE FRÉQUENCE DES LEMMES
def get_terme_per_doc(tags):
    dict_terme_par_doc = dict()

    for tag in tags:
        t = tag[2].lower()
        if t != "\ufeff":
            if t not in dict_terme_par_doc.keys():
                dict_terme_par_doc[t] = 1
            elif t in dict_terme_par_doc.keys():
                dict_terme_par_doc[t] = dict_terme_par_doc[t]+1
    return dict_terme_par_doc

# ------------------------ json -----------------------------------------

# ÉCRIRE UN FICHIER JSON
def ecrireJson(fichier_js,dict_index):
    with open (fichier_js, "w") as js:
        json.dump(dict_index, js, indent=4, ensure_ascii=False)


# LIRE UN FICHIER JSON
def lireJson(fichier_js):
    with open(fichier_js) as json_file:
        data = json.load(json_file)
    return data
