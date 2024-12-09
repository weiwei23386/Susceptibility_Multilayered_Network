import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Example claim
# doc1 = "Trump incited the Capitol riot by urging supporters to resist Biden's certification, leading to his impeachment. He falsely claimed victory after the election, calling absentee ballot counting a fraud. This narrative made it harder for some Democrats to vote and increased partisan control over elections."
doc1 = "On January 6, 2021, the United States Capitol Building in Washington, D.C., was attacked by a mob of supporters of then–U.S. President Donald Trump in an attempted self-coup d'état two months after his defeat in the 2020 presidential election. They sought to keep him in power by occupying the Capitol and preventing a joint session of Congress from counting the Electoral College votes to formalize the victory of President-elect Joe Biden. The attack was ultimately unsuccessful in preventing the certification of the election results. According to the bipartisan House select committee that investigated the incident, the attack was the culmination of a seven-part plan by Trump to overturn the election. Within 36 hours, five people died: one was shot by Capitol Police, another died of a drug overdose, three died of natural causes, and a police officer died after being assaulted by rioters. Many people were injured, including 174 police officers. Four officers who responded to the attack died by suicide within seven months. Damage caused by attackers exceeded $2.7 million."

# List of CSV filenames
# filenames = ['cnn.csv', 'foxnews.csv', 'latimes.csv', 'nytimes.csv', 'reuters.csv', 'theepochtimes.csv', 'thefederalist.csv', 'washingtonpost.csv', 'washingtontimes.csv']
# filenames = ['latimes.csv', 'nytimes.csv', 'reuters.csv', 'theepochtimes.csv', 'thefederalist.csv', 'washingtonpost.csv', 'washingtontimes.csv']
# filenames = ['cnn.xlsx', 'foxnews.xlsx', 'latimes.xlsx', 'nytimes.xlsx', 'reuters.xlsx', 'theepochtimes.xlsx', 'thefederalist.xlsx', 'washingtonpost.xlsx', 'washingtontimes.xlsx']
filenames = ['thefederalist.xlsx', 'washingtonpost.xlsx']
# Initialize the TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# cnn = pd.read_csv('cnn.csv', encoding='ISO-8859-1')
# print(cnn.head())
# Process each file one by one
for file in filenames:
    # Load the CSV file into a DataFrame
    # df = pd.read_csv(file, encoding='ISO-8859-1', header=0, delimiter=',')
    df = pd.read_excel(file, header=0)
    print(df.head())
    # Extract the first column (assumed to be the text column)
    text_data = df.iloc[:, 0].dropna().tolist()  # Drop any NaN values
    text_data1 = df.iloc[:,1].dropna().tolist()
    # text_data2 = df.iloc[:,2].dropna().tolist()

    # Add the claim to the text data for similarity calculation
    documents = [doc1] + text_data  # First element is the claim, rest are the statements
    documents1 = [doc1] + text_data1
    # documents2 = [doc1] + text_data2

    # Convert the documents into TF-IDF vectors
    tfidf_matrix = vectorizer.fit_transform(documents)
    tfidf_matrix1 = vectorizer.fit_transform(documents1)
    # tfidf_matrix2 = vectorizer.fit_transform(documents2)

    # Compute cosine similarity of the claim (doc1) with all the other documents
    cos_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()  # Flatten to get a 1D array
    cos_sim1 = cosine_similarity(tfidf_matrix1[0:1], tfidf_matrix1[1:]).flatten()
    # cos_sim2 = cosine_similarity(tfidf_matrix2[0:1], tfidf_matrix2[1:]).flatten()

    # Reorder columns to make sure new columns are at the end
    # df = df[[col for col in df.columns if col not in ['Cosine_Similarity', 'Cosine_Similarity1', 'Cosine_Similarity2']] + 
        # ['Cosine_Similarity', 'Cosine_Similarity1', 'Cosine_Similarity2']]
    # Check the lengths
    # print(len(df))  # Number of rows in the DataFrame
    # print(len(cos_sim))  # Length of cosine similarity values
    # print(len(cos_sim1))
    # print(len(cos_sim2))

    # # Add the cosine similarity values as a new column to the DataFrame
    # df['Cosine_Similarity'] = cos_sim
    # df['Cosine_Similarity1'] = cos_sim1
    # df['Cosine_Similarity2'] = cos_sim2
    # Align the indices if using Series
    df['Cosine_Similarity'] = pd.Series(cos_sim).reset_index(drop=True)
    df['Cosine_Similarity1'] = pd.Series(cos_sim1).reset_index(drop=True)
    # df['Cosine_Similarity2'] = pd.Series(cos_sim2).reset_index(drop=True)


    # Save the updated DataFrame back to the same CSV file (you can change to a new file if preferred)
    df.to_excel(file, index=False)
    print(f"Cosine similarity values have been added to {file}")
