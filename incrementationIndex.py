#!/usr/bin/env python
# coding: utf-8
# Projet du groupe : Siyu Wang et Natia Davitashvili

# ------------------------------------------------------------------------------------------------------
#   script d'incrémentation des indexations
#   Usage : python3 incrementationIndex.py <chemin de dossier>
# ------------------------------------------------------------------------------------------------------
import traitementCommun as trc
import glob
import json
import re
import sys
from langdetect import detect

# -------- à paramétrer ---------------
# chemin du dossier saisi par l'utilisatuer
chemin = sys.argv[1]

# corpus à incrémenter pour l'indexation
extra_corpus = chemin + "/*.txt"

# ----------------- incrémentation ---------------------

# OBTENIR UNE LISTE DES FICHIERS DÉJÀ INDEXÉS POUR ÉVITER DES DOUBLONS D'INDEXATION
def get_list_fichiersIdex(fichier_js):
    data = trc.lireJson(fichier_js)
    list_fichiers = list()
    for t in data:
        for x in data[t]:
            fi = list(x.values())[0]
            list_fichiers.append(fi)
    return list_fichiers


# LIRE LE FICHIER INDEXDOCS EXISTANT ET AJOUTER LES NOUVEAUX INDEX
def get_indexDocs_increm(nb_docs):
    index_sup = dict()
    index_docs = dict()
    x = 31
    while (x<31+nb_docs):
        for doc in list_docs:
            print("Traitement du fichier : "+doc)
            text = trc.lireFichier(doc)
            titre = text[1]
            titre = re.sub (r'<[^>]+>', '', titre)
            titre = re.sub (r'\n', '', titre)
            index_docs[x]={"Fichier":doc, "Titre":titre}
            x+=1
    index_sup['indexDocs_complémentaires'] = index_docs
    return index_sup


# TRAITEMENT POUR OBTENIR UN DICTIONNAIRE AVEC L'ID D'ARTICLE COMME CLÉ ET LE DICT DES FRÉQUENCES COMME VALEUR
def traitement_terme_per_doc(doc,texte,langue,dict_doc_termes):
    print("--- Langue : "+langue)
    texte = trc.supprimPonct(texte)
    tags = trc.treetagger_tag(texte,'fr')
    dict_terme_par_doc = trc.get_terme_per_doc(tags)
    dict_doc_termes[doc]=dict_terme_par_doc
    nom_f = './documentsIndexes/index_par_document_'+langue+'.json'
    increment_Json(nom_f,dict_doc_termes)


# INCREMENTER LE FICHIER INDEXDOCS.JSON
def increment_indexDocs(list_docs,list_fichiers_fr,list_fichiers_en):
    for f in list_docs:
        # vérifier si l'articles est bien dedans
        print("--- Vérification du fichier " + f + " ---")

        if f in list_fichiers_fr or f in list_fichiers_en:
            print('--- ATTENTION : Le fichier '+f+' est déjà indexé au processus précédent ! ---')

        else:
            print('--- Nouveau document à incrémenter --- ')
            
            # IndexDocs
            index_docs = get_indexDocs_increm(nb_docs)
            increment_Json("./documentsIndexes/IndexDocs.json",index_docs)
            print('--- Incrémentation du corpus complémentaire dans IndexDocs.json réussite ! ---')

# INCREMENTER L'INDEX DES TERMES, METTRE À JOURS LE DICIONNAIRE D'INDEX
def increment_terme(dict_doc_termes,data_termes):
    for a,d in dict_doc_termes.items():
        for t in d.keys():
            if t in data_termes.keys():
                data_termes[t].append({"doc_id":a,"fréquence":d[t]})
                #print("-- Fréquence du terme '"+t+"' mis à jours ! --")
            else:
                data_termes.update( {t:[{"doc_id":a,"fréquence":d[t]}]} )
                #print("-- Nouveau terme '"+ t + "' ajouté ! --")


# ----------------------------- json ----------------------------------

# INCRÉMENTATION DU FICHIER INDEXDOCS.JSON
def increment_Json(js_file,index_docs):
    with open(js_file, "r+") as file:
            data = json.load(file)
            data.update(index_docs)
            file.seek(0)
            json.dump(data, file, indent=4, ensure_ascii=False)


# ---------------------------- main -----------------------------------------
print('*'*50)
print('*****    Partie incrémentation du projet    ******')
print('*'*50)

# liste de tous les fichiers txt du dossier complémentaire
list_docs = glob.glob(extra_corpus)

nb_docs = len(list_docs)

# Incrémentation 

print("--- Incrémentation des fichiers d'indexation avec le corpus complémentaire ---")

# lire les fichiers d'indexation json
list_fichiers_fr = get_list_fichiersIdex("./documentsIndexes/IndexTermesFR.json")
list_fichiers_en = get_list_fichiersIdex("./documentsIndexes/IndexTermesEN.json")

# incrémenter le fichier indexDocs.json
increment_indexDocs(list_docs,list_fichiers_fr,list_fichiers_en)

    
# ----- Incrémentation IndexTermes -------
dict_doc_termes_fr = dict()
dict_doc_termes_en = dict()

# parcourir les fichiers complémentaires
for doc in list_docs:

    # si ce fichier est déjà indexé, on ne fait rien
    if doc in list_fichiers_fr or doc in list_fichiers_en:
        pass

    # si ce fichier est un nouveau fichier, donc à incrémenter
    else:
        print("--- Indexation des termes du fichier: "+doc)
        texte = trc.extraitTexteFichier(doc)

        if detect(texte)=="fr":
            traitement_terme_per_doc(doc,texte,'fr',dict_doc_termes_fr)
            
        if detect(texte)=='en':
            traitement_terme_per_doc(doc,texte,'en',dict_doc_termes_en)

# lire le fichiers d'index des termes français IndexTermesFR.json
data_termes_fr = trc.lireJson("./documentsIndexes/IndexTermesFR.json")
# lire le fichiers d'index des termes anglais IndexTermesEN.json
data_termes_en = trc.lireJson("./documentsIndexes/IndexTermesEN.json")

# mettre à jour le dictionnaire contenant les indexs de termes
increment_terme(dict_doc_termes_fr,data_termes_fr)
increment_terme(dict_doc_termes_en,data_termes_en)

# écrire les contenus mis à jour (incrémentés) dans le fichier json
trc.ecrireJson("./documentsIndexes/IndexTermesFR.json",data_termes_fr)
print("--- Fichier IndexTermesFR.json mis à jour avec succès ! ---")
trc.ecrireJson("./documentsIndexes/IndexTermesEN.json",data_termes_en)
print("--- Fichier IndexTermesEN.json mis à jour avec succès ! ---")




