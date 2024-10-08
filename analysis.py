import pandas as pd
import re
import spacy
import matplotlib.pyplot as plt

nlp = spacy.load('fr_core_news_lg')
nlp.Defaults.stop_words -= {"pas", "sais", "rien","non"}

file_path = r'perrine.xlsx'

a=0

def remove_anormal_punctuation(raw_sentence):
    res_sentence = raw_sentence.replace('’','\'')
    res_sentence = res_sentence.replace('/',' ')
    res_sentence = raw_sentence.replace('‘','\'')
    res_sentence = raw_sentence.replace('(','')
    res_sentence = raw_sentence.replace(')','')
    res_sentence = raw_sentence.replace('ʼ','\'')
    return res_sentence

def remove_stopwords(token_list):
    res_list = []
    for token in token_list:
        if token.lemma_ not in nlp.Defaults.stop_words:
            res_list.append(token)
    return token

def count_lemme_by_answer(set):
    dict_of_known_lemma = {}
    for answer in set:
        for token in answer :
            lemma = token.lemma_
            if lemma not in dict_of_known_lemma.keys() :
                dict_of_known_lemma[lemma]=1
            else:
                dict_of_known_lemma[lemma]+=1
    return dict_of_known_lemma

def find_position_empty_lists(set):
    res_positions = []
    i=0
    while i in range(len(set)):
        element = set[i]
        if len(element) == 0:
            res_positions.append(i)
        i+=1
    return res_positions

def correction_lemma(dict):
    problematic_lemma = ['crou','cnou','cnous','etat',',','état/','cultur\'','?','ecole','(',')','/','.','jsp','l','asso','idee','education',
                        'etudiant','region','...',' ','ministere','nsp','universite','…','superieur','univ','etablissement','assos','academie',
                        '-','etude','reverse','etudiante','!','surement','\'','d','u','>','ingé','étudiant.e.','..','assoc','ministére','know',
                        'idk','superieure','universités/','idéee','inge','/universite',':','/état','l!université','universitzire','universitè',
                        'étudiant•e','crous\\','academi','l‘école','administation','*','independant','ratacher','éduction','françai','french','government',
                        'x','partenair','l´ecole','ministrère','administrafif',';','répartisse','etc.','chaqué','....','concernée//le','mèr','academiqu',
                        'associtation','univeristé','universtaire','entiereté','deplorabl','crous/','eleve','dingenieur','amicales/','crous+écoles','jcp',
                        '́en','selectionner','cnous/','assosiation','impot','largent','éudiant','reférente','organne','don\'','t','letat','plublic','universitét',
                        'l´université','bibliothèqu','commisison','ministair','létat','univeristair','ceou','l"état','grupe','fonctionnair','la.e','trésoreri',
                        'etudiant.gouv.fr','regional','admin','oeuvre','éleve','finacement','événement','accadémie','ø','associations/','écoke','leducation',
                        'asssociation','scolaire/','l"etat','écoles/','/la','éducation/','luniversit','specifiqu','universiataire','rataché','orgnisme',
                        'minsitère','universiter','50','typ','100','50/50','francai','cotisation','15','99','25','1','2','100000000','180','😂','53','110',
                        'c','150','vaaaa','ae']
    keys = [key for key in dict.keys()]
    dict['culture']=0
    for key in keys:
        if key in problematic_lemma:
            if key=='crou' or key=='cnou' or key=='cnous' or key=='crous\\' or key=='crous/' or key=='cnous/' or key=='ceou':
                if 'crous' not in keys:
                    dict['crous']=0
                dict['crous']+=dict[key]
            elif key=='etat' or key=='état/' or key=='/état' or key=='letat' or key=='létat' or key=='l"état' or key=='l"etat':
                if 'état' not in keys:
                    dict['état']=0
                dict['état']+=dict[key]
            elif key=='cultur\'':
                if 'culture' not in keys:
                    dict['culture']=0
                dict['culture']+=dict[key]
            elif key=='ecole' or key=='l‘école' or key=='l´ecole' or key=='écoke' or key=='écoles/':
                if 'école' not in keys:
                    dict['école']=0
                dict['école']+=dict[key]
            elif key=='scolaire/':
                if 'scolaire' not in keys:
                    dict['scolaire']=0
                dict['scolaire']+=dict[key]
            elif key=='jsp' or key=='nsp' or key=='idk' or key=='jcp':
                if 'sais' not in keys:
                    dict['sais']=0
                if 'pas' not in keys:
                    dict['pas']=0
                dict['sais']+=dict[key]
                dict['pas']+=dict[key]
            elif key=='know':
                if 'sais' not in keys:
                    dict['sais']=0
                dict['sais']+=dict[key]
            elif key=='don\'':
                if 'pas' not in keys:
                    dict['pas']=0
                dict['pas']+=dict[key]
            elif key=='universite' or key=='univ' or key=='universités/' or key=='/universite' or key=='l!université' or key=='universitè' or key=='univeristé' or key=='universitét' or key=='l´université' or key=='luniversit' or key=='universiataire' or key=='universiter':
                if 'université' not in keys:
                    dict['université']=0
                dict['université']+=dict[key]
            elif key=='universitzire' or key=='universtaire' or key=='univeristair':
                if 'universitaire' not in keys:
                    dict['universitaire']=0
                dict['universitaire']+=dict[key]
            elif key=='asso' or key=='assos' or key=='assoc' or key=='associtation' or key=='assosiation' or key=='associations/' or key=='asssociation':
                if 'association' not in keys:
                    dict['association']=0
                dict['association']+=dict[key]
            elif key=='idee' or key=='idéee':
                if 'idée' not in keys:
                    dict['idée']=0
                dict['idée']+=dict[key]
            elif key=='education' or key=='éduction' or key=='leducation' or key=='éducation/':
                if 'éducation' not in keys:
                    dict['éducation']=0
                dict['éducation']+=dict[key]
            elif key=='etudiant' or key=='etudiante' or key=='étudiant.e.' or key=='étudiant•e' or key=='éudiant':
                if 'étudiant' not in keys:
                    dict['étudiant']=0
                dict['étudiant']+=dict[key]
            elif key=='eleve' or key=='éleve':
                if 'élève' not in keys:
                    dict['élève']=0
                dict['élève']+=dict[key]
            elif key=='region':
                if 'région' not in keys:
                    dict['région']=0
                dict['région']+=dict[key]
            elif key=='regional':
                if 'régional' not in keys:
                    dict['régional']=0
                dict['régional']+=dict[key]
            elif key=='ministere' or key=='ministére' or key=='ministrère' or key=='ministair' or key=='minsitère':
                if 'ministère' not in keys:
                    dict['ministère']=0
                dict['ministère']+=dict[key]
            elif key=='superieur' or key=='superieure':
                if 'supérieur' not in keys:
                    dict['supérieur']=0
                dict['supérieur']+=dict[key]
            elif key=='etablissement':
                if 'établissement' not in keys:
                    dict['établissement']=0
                dict['établissement']+=dict[key]
            elif key=='academie' or key=='academi' or key=='accadémie':
                if 'académie' not in keys:
                    dict['académie']=0
                dict['académie']+=dict[key]
            elif key=='academiqu':
                if 'académique' not in keys:
                    dict['académique']=0
                dict['académique']+=dict[key]
            elif key=='etude':
                if 'étude' not in keys:
                    dict['étude']=0
                dict['étude']+=dict[key]
            elif key=='reverse':
                if 'reverser' not in keys:
                    dict['reverser']=0
                dict['reverser']+=dict[key]
            elif key=='surement':
                if 'sûrement' not in keys:
                    dict['sûrement']=0
                dict['sûrement']+=dict[key]
            elif key=='ingé' or key=='inge' or key=='dingenieur':
                if 'ingénieur' not in keys:
                    dict['ingénieur']=0
                dict['ingénieur']+=dict[key]
            elif key=='administation' or key=='admin':
                if 'administration' not in keys:
                    dict['administration']=0
                dict['administration']+=dict[key]
            elif key=='administrafif':
                if 'administratif' not in keys:
                    dict['administratif']=0
                dict['administratif']+=dict[key]
            elif key=='independant':
                if 'indépendant' not in keys:
                    dict['indépendant']=0
                dict['indépendant']+=dict[key]
            elif key=='ratacher' or key=='rataché':
                if 'rattacher' not in keys:
                    dict['rattacher']=0
                dict['rattacher']+=dict[key]
            elif key=='françai' or key=='french' or key=='francai':
                if 'français' not in keys:
                    dict['français']=0
                dict['français']+=dict[key]
            elif key=='government':
                if 'gouvernement' not in keys:
                    dict['gouvernement']=0
                dict['gouvernement']+=dict[key]
            elif key=='partenair':
                if 'partenaire' not in keys:
                    dict['partenaire']=0
                dict['partenaire']+=dict[key]
            elif key=='répartisse':
                if 'répartir' not in keys:
                    dict['répartir']=0
                dict['répartir']+=dict[key]
            elif key=='concernée//le':
                if 'concerné' not in keys:
                    dict['concerné']=0
                dict['concerné']+=dict[key]
            elif key=='entiereté':
                if 'entièreté' not in keys:
                    dict['entièreté']=0
                dict['entièreté']+=dict[key]
            elif key=='deplorabl':
                if 'déplorable' not in keys:
                    dict['déplorable']=0
                dict['déplorable']+=dict[key]
            elif key=='crous+écoles':
                if 'crous' not in keys:
                    dict['crous']=0
                dict['crous']+=dict[key]
                if 'école' not in keys:
                    dict['école']=0
                dict['école']+=dict[key]
            elif key=='selectionner':
                if 'sélectionner' not in keys:
                    dict['sélectionner']=0
                dict['sélectionner']+=dict[key]
            elif key=='impot':
                if 'impôt' not in keys:
                    dict['impôt']=0
                dict['impôt']+=dict[key]
            elif key=='largent':
                if 'argent' not in keys:
                    dict['argent']=0
                dict['argent']+=dict[key]
            elif key=='reférente':
                if 'référent' not in keys:
                    dict['référent']=0
                dict['référent']+=dict[key]
            elif key=='organne':
                if 'organe' not in keys:
                    dict['organe']=0
                dict['organe']+=dict[key]
            elif key=='orgnisme':
                if 'organisme' not in keys:
                    dict['organisme']=0
                dict['organisme']+=dict[key]
            elif key=='plublic':
                if 'public' not in keys:
                    dict['public']=0
                dict['public']+=dict[key]
            elif key=='bibliothèqu':
                if 'bibliothèque' not in keys:
                    dict['bibliothèque']=0
                dict['bibliothèque']+=dict[key]
            elif key=='commisison':
                if 'commission' not in keys:
                    dict['commisison']=0
                dict['commisison']+=dict[key]
            elif key=='grupe':
                if 'groupe' not in keys:
                    dict['groupe']=0
                dict['groupe']+=dict[key]
            elif key=='fonctionnair':
                if 'fonctionnaire' not in keys:
                    dict['fonctionnaire']=0
                dict['fonctionnaire']+=dict[key]
            elif key=='trésoreri':
                if 'trésorerie' not in keys:
                    dict['trésorerie']=0
                dict['trésorerie']+=dict[key]
            elif key=='etudiant.gouv.fr':
                if '.gouv' not in keys:
                    dict['.gouv']=0
                dict['.gouv']+=dict[key]
            elif key=='oeuvre':
                if 'œuvre' not in keys:
                    dict['œuvre']=0
                dict['œuvre']+=dict[key]
            elif key=='finacement':
                if 'financement' not in key:
                    dict['finacement']=0
                dict['financement']+=dict[key]
            elif key=='événement':
                if 'évènement' not in keys:
                    dict['événement']=0
                dict['événement']+=dict[key]
            elif key=='specifiqu':
                if 'spécifique' not in keys:
                    dict['spécifique']=0
                dict['spécifique']+=dict[key]
            elif key=='typ':
                if 'type' not in keys:
                    dict['type']=0
                dict['type']+=dict[key]
            elif key=='cotisation':
                if 'côtisation' not in keys:
                    dict['côtisation']=0
                dict['côtisation']+=dict[key]
            elif key=='ae':
                if 'association' not in keys:
                    dict['association']=0
                dict['association']+=dict[key]
                if 'étudiant' not in keys:
                    dict['étudiant']=0
                dict['étudiant']+=dict[key]
    for lemma in problematic_lemma:
        if lemma in keys:
            del dict[lemma]

data = pd.read_excel(file_path)
data['Answer']=data["D'après vous, qui récolte la CVEC ?"]
del data["D'après vous, qui récolte la CVEC ?"]
answers_list = [nlp(remove_anormal_punctuation(data['Answer'].iloc[i].lower())) for i in range(len(data.index))]
dict_res = count_lemme_by_answer(answers_list)

keys_stop_words = []
for key in dict_res.keys():
    if key in nlp.Defaults.stop_words:
        keys_stop_words.append(key)

for key in keys_stop_words:
    del dict_res[key]

correction_lemma(dict_res)
dict_pertinent_res = {key:value for key, value in dict_res.items() if value>30}
dict_pertinent_res['Ne sais pas/Aucune idée']=min(dict_pertinent_res['savoir'],dict_pertinent_res['pas'])+min(dict_pertinent_res['idée'],dict_pertinent_res['aucun'])
del dict_pertinent_res['savoir']
del dict_pertinent_res['pas']
del dict_pertinent_res['idée']
del dict_pertinent_res['aucun']
dict_pertinent_res = {key:value for key, value in sorted(dict_pertinent_res.items(), key=lambda item: -item[1])}

# for element in dict_res.keys():
#     print(element)
#     input()
# print(dict_res)


fig, ax = plt.subplots(layout='constrained')
names = [key for key in dict_pertinent_res.keys()]
values = [100*value/len(answers_list) for value in dict_pertinent_res.values()]

bars_container=ax.bar(names, values)
ax.bar_label(bars_container,[str(round(value,2))+'%' for value in values])

ax.set_title('D\'après vous, qui récolte la CVEC ?')
ax.set_ylabel('Pourcentage de réponses comprenant le mot (%)')
ax.set_xlabel('Mots les plus fréquemment observés dans les réponses')

fig.autofmt_xdate()

plt.show()