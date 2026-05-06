# Healthcare Data Warehouse & BI

Projet de Business Intelligence applique au domaine de la sante.
L'objectif est de concevoir un entrepot de donnees hospitalier, produire des KPI decisionnels et ajouter une couche de machine learning pour predire la duree de sejour des patients.

## Objectifs
- analyser l'activite hospitaliere : sejours, couts, duree de sejour
- concevoir un schema en etoile pour un Data Warehouse sante
- creer des vues SQL pour alimenter la BI
- visualiser les KPI dans Power BI
- predire la duree de sejour avec Python et le machine learning

## Stack technique
- modelisation : MCD / schema en etoile
- Data Warehouse : MySQL
- SQL : creation des tables et vues KPI
- BI : Power BI
- Python : pandas, scikit-learn, joblib, SQLAlchemy, mysql-connector-python

## Structure du projet
- `sql/` : scripts SQL du Data Warehouse
- `docs/` : schemas et apercu du dashboard
- `ml/` : dataset, preparation, entrainement et prediction ML
- `requirements.txt` : dependances Python

## Partie SQL
Les scripts SQL disponibles :
- `sql/create_tables.sql`
- `sql/create_views.sql`

Les KPI actuels couvrent :
- nombre de sejours par service
- duree moyenne de sejour par service
- cout total et cout moyen par service
- evolution mensuelle des sejours
- activite par medecin

## Partie Machine Learning
La partie ML est construite autour de la prediction de `duree_sejour` et utilise uniquement vos donnees hospitalieres reelles.

Fichiers principaux :
- `ml/build_dataset.py` : construction du dataset ML depuis MySQL et `v_ml_dataset`
- `ml/dataset.csv` : dataset d'entrainement genere depuis la base
- `ml/data_preparation.py` : chargement, validation et pretraitement
- `ml/model_training.py` : entrainement et sauvegarde du modele
- `ml/prediction.py` : prediction sur de nouvelles observations et publication optionnelle dans MySQL
- `ml/sample_prediction_input.csv` : entree de prediction generee depuis vos donnees reelles
- `sql/create_ml_objects.sql` : table et vue pour stocker et exposer les predictions

Variables utilisees :
- `service`
- `type_service`
- `capacite_lits`
- `specialite_medecin`
- `ancienete_medecin`
- `sexe`
- `age`
- `ville`
- `mois`
- `trimestre`
- `nombre_examens`
- `cout_total`

Variable cible :
- `duree_sejour`

## Execution
Installer les dependances :

```bash
pip install -r requirements.txt
```

Configurer MySQL une seule fois :

1. copier `.env.example` en `.env`
2. remplacer les valeurs par vos vrais acces MySQL

Exemple de contenu :

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=hopital_dw
MYSQL_USER=votre_user
MYSQL_PASSWORD=votre_mot_de_passe
```

Generer le dataset depuis MySQL :

```bash
python ml/build_dataset.py
```

Lancer l'entrainement :

```bash
python ml/model_training.py
```

Lancer une prediction :

```bash
python ml/prediction.py
```

Ecrire aussi les predictions dans MySQL :

```bash
python ml/prediction.py --write-mysql
```

Sorties generees :
- `ml/artifacts/length_of_stay_model.joblib`
- `ml/artifacts/training_metrics.json`
- `ml/predictions.csv`
- table MySQL `ml_predictions`
- vue MySQL `v_ml_predictions_latest`

Par defaut, `ml/build_dataset.py` lit directement :
- la base MySQL `hopital_dw`
- la vue `v_ml_dataset`
- le fichier `.env` a la racine du projet si present

Les variables attendues sont :
- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`

## Power BI
Pour integrer les resultats dans Power BI :

1. executer `sql/create_ml_objects.sql` dans MySQL
2. lancer `python ml/prediction.py --write-mysql`
3. dans Power BI, se connecter a la base `hopital_dw`
4. importer la vue `v_ml_predictions_latest`

La vue `v_ml_predictions_latest` permet d'afficher :
- la prediction de duree de sejour par sejour
- la comparaison prediction vs duree reelle
- les erreurs moyennes par service, specialite ou trimestre
- des cartes KPI de qualite du modele dans le dashboard

## Perspectives
Pour aller encore plus loin, vous pourrez ensuite :
- comparer plusieurs modeles de regression
- ajouter des visualisations de performance du modele
- integrer les predictions dans Power BI
