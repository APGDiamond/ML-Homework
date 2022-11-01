import pandas as pd

symptoms_df = pd.read_csv('symptom.csv', sep=';')
disease_df = pd.read_csv('disease.csv', sep=';')


def get_probability(symptom_number, disease_number):
    total_symptoms_by_disease_prob = 1
    for symptom in symptom_number:
        symptom_by_disease_prob = symptoms_df.iloc[symptom, disease_number+1]
        total_symptoms_by_disease_prob *= symptom_by_disease_prob
    disease_probability = disease_df.iloc[disease_number, 1]/disease_df.iloc[disease_df.shape[0]-1, 1]
    total_symptoms_by_disease_prob *= disease_probability
    return total_symptoms_by_disease_prob


def get_all_probability_by_symptoms(symptoms_list):
    symptoms = list(symptoms_df.iloc[:, 0])
    count = len(symptoms)    #кол-во симптомов
    diseases = disease_df.iloc[:-1, 0]

    if len(symptoms_list) != count:
        print('Wrong arguments! You need to put ' + str(count) + ' values 0 or 1.')
        return

    selected_symptoms = []
    for i in range(len(symptoms)):
        if symptoms_list[i] == 1:
            selected_symptoms.append(i)

    diseases_probabilities = []
    for disease_number in range(len(diseases)):
        diseases_probabilities.append(get_probability(selected_symptoms, disease_number))

    max_probability = -1
    print('Diseases probability: ')
    for i in range(len(diseases_probabilities)):
        print(str(disease_df.iloc[i, 0]) + ': ' + str(diseases_probabilities[i]))
        if diseases_probabilities[i] > max_probability:
            max_probability = diseases_probabilities[i]

    print('\nMost probable diseases:')
    for i in range(len(diseases_probabilities)):
        if diseases_probabilities[i] == max_probability:
            print(str(disease_df.iloc[i, 0]))


get_all_probability_by_symptoms([1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0])
