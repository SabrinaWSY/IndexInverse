-------------------------------------------------
        Instruction d'exécution du projet
         Siyu Wang et Natia Davitashvili
-------------------------------------------------
# Pour installer les outils requis : (modules: langdetect, six, et treetaggerwrapper)
pip3 install -r requirements.txt

# Pour indexer un dossier :
python3 indexerDocuments.py <chemin de dossier>
Ex: python3 incrementationIndex.py ./corpusExamenCorrige/initiaux/

# Pour incrémentation d'indexation d'un autre dossier :
python3 incrementationIndex.py <chemin de dossier>
Ex: python3 incrementationIndex.py ./corpusExamenCorrige/complémentaires/

# Pour faire la requête :
python3 requetesCorpus.py 