import pandas as pd
import os
from openai import OpenAI

# Define the sheet name to read (adjustable as needed)
sheet_name = 2 # Modify this to handle sheets 0-2 if necessary
ground_truth = "washingtontimes"
save_path = f"{ground_truth}_day{int(sheet_name) + 1}"
def clean_data_from_sheet(file_path):
    """
    Reads data from a specified sheet in an Excel file, renames columns to standard names.
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    df.columns = ['headlines', 'Cosine_Similarity']
    return df

def topk_with_min(df, k, min_value):
    """
    Filters the DataFrame to select the top k rows based on Cosine Similarity above a minimum value.
    """
    df["Cosine_Similarity"] = pd.to_numeric(df["Cosine_Similarity"], errors="coerce")
    filtered = df[df["Cosine_Similarity"] >= min_value]
    return filtered.nlargest(k, "Cosine_Similarity")

def evaluate_headlines(client, ground_truth_headlines, test_headline):
    """
    Uses the OpenAI API to score the similarity of a test headline with the ground truth headlines.
    """
    ground_truth_combined = " ".join(ground_truth_headlines)
    prompt = (
    """Let's call the dataset of texts provided 'F.' 
    Assume that all the information in 'F' is true for the purpose of this judgment. 
    Do not use any prior knowledge or information about the subject. 
    Evaluate the given article headline based solely on 'F,' and provide a score 
    between 0 and 1, where 1 indicates that the article is fully aligned with the facts in 'F' 
    (no contradictions), and 0 indicates that it contradicts the information in 'F.' 
    In 10 words or less for each headline, explain the score. 
    The format: "<score>: <explanation>"
    """
    f"Ground Truth (F): '{ground_truth_combined}' "
    f"\nHeadline: '{test_headline}'"
    )
    
    response = client.chat.completions.create(
        model="gpt-4",  # Update as appropriate
        messages=[{"role": "user", "content": prompt}]
    )
    result = response.choices[0].message.content
    try:
        score, explanation = result.split(": ", 1)
        return float(score.strip()), explanation.strip()
    except ValueError:
        return None, "Parsing error in response."

# API key setup
API_KEY = "..."

# Initialize the OpenAI client
client = OpenAI(api_key=API_KEY)

# Define ground truth file (e.g., CNN)
ground_truth_file = f"{ground_truth}.xlsx"
ground_truth_data = clean_data_from_sheet(ground_truth_file)
topk_ground_truth = topk_with_min(ground_truth_data, k=30, min_value=0.05)
ground_truth_headlines = topk_ground_truth['headlines'].tolist()

# Define the output directory based on the ground truth file and sheet number
save_path = f"{ground_truth_file.split('.')[0]}_day{int(sheet_name) + 1}"
os.makedirs(save_path, exist_ok=True)  # Create the directory if it doesn't exist

# Loop through all files in the directory and evaluate each against the ground truth
for file in os.listdir():
    if file.endswith(".xlsx") and file != ground_truth_file:
        print(f"Evaluating file: {file}")
        
        # Load and process test file data
        test_data = clean_data_from_sheet(file)
        topk_test = topk_with_min(test_data, k=30, min_value=0.05)
        test_headlines = topk_test['headlines'].tolist()
        
        # Evaluate each headline in the test file
        results = []
        for headline in test_headlines:
            score, explanation = evaluate_headlines(client, ground_truth_headlines, headline)
            results.append({
                "Test Headline": headline,
                "Score": score,
                "Explanation": explanation
            })

        # Save the results for this test file to a CSV
        results_df = pd.DataFrame(results)
        output_filename = f"{save_path}/{file.split('.')[0]}_evaluation_results.csv"
        results_df.to_csv(output_filename, index=False)
        print(f"Evaluation completed for {file} and results saved to '{output_filename}'.")

# day3_files = ["latimes, nytimes, theepochtimes, washingtontimes"]

# Read the evaluation files and calculate average scores
edges = []
for file in os.listdir(save_path):
    if file.endswith(".csv"):
        print(f"Processing evaluation results for: {file}")
        
        # Read the CSV and calculate the average score
        # results_df = pd.read_csv(f"{save_path}/{file}")
        try:
            results_df = pd.read_csv(f"{save_path}/{file}")
            if results_df.empty:
                print(f"Skipping {file} because it is empty.")
                continue
        except pd.errors.EmptyDataError:
            print(f"Skipping {file} because it is empty.")
            continue
        avg_score = results_df["Score"].mean()
        print(f"Average score for {file}: {avg_score}")
        
        # Append the tuple for weighted edges: (ground_truth_node, test_file, avg_score)
        test_file_node = file.split('_evaluation_results.csv')[0]
        edges.append((ground_truth, test_file_node, avg_score))

save_path1 = f"day{int(sheet_name) + 1}_network"
os.makedirs(save_path1, exist_ok=True)
edges_df = pd.DataFrame(edges, columns=["source", "target", "weight"])
edges_df.to_csv(f"{save_path1}/{ground_truth}_network_edges.csv", index=False)
print("Network edges saved to CSV.")
# Create the graph and add weighted edges
# G = nx.Graph()
# G.add_weighted_edges_from(edges)

# # Draw the network graph
# plt.figure(figsize=(12, 12))
# pos = nx.spring_layout(G, seed=42)  # Position nodes for better visualization

# # Draw nodes, edges, and labels with weights
# nx.draw_networkx_nodes(G, pos, node_size=700, node_color='skyblue', edgecolors='black')
# nx.draw_networkx_edges(G, pos, width=2, edge_color='gray', alpha=0.7)
# nx.draw_networkx_labels(G, pos, font_size=10, font_color="black", font_weight="bold")

# # Draw edge labels (average scores as weights)
# edge_labels = {(u, v): f"{d['weight']:.2f}" for u, v, d in G.edges(data=True)}
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

# plt.title("Network Graph with Average Score as Edge Weights")
# plt.show()
