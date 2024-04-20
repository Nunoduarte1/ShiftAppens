import csv
import emotions
import logistic_inference

def average_emotion(filepath):   
    # open csv file and read the column 'abstract' and 'company'
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        abstracts = [row['Abstract'] for row in reader]
        company = [row['Company'] for row in reader]
        # logistic inference
        total = 0
        sum = 0
        for abstract in abstracts:
            total += 1
            parts = abstract.split('.')
            sum += logistic_inference.compute_positivity(parts)
        print(sum / total, '% of acceptance')
        for i in range(len(company)):
            emotions.add_element_to_file('./emotion.json', company[i], round(sum / total, 1)) # TODO - check if it is needed to divide by 10 or 20
        
