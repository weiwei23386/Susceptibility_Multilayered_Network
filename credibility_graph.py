import os
import glob
import pandas as pd
import networkx as nx

dir_path = "./day3_network/"
out_put_path = os.path.join(dir_path, "day1_network_graph.gexf")
all_files = glob.glob(os.path.join(dir_path, "*.csv"))


# Check if files are found
if not all_files:
    print("No CSV files found in the specified directory. Check the directory path and file names.")
else:
    print(f"Found {len(all_files)} CSV files: {all_files}")

    # Combine data from all CSV files
    edge_list = []
    for filename in all_files:
        df = pd.read_csv(filename)
        edge_list.append(df)

    # Concatenate data if edge_list is not empty
    if edge_list:
        combined_df = pd.concat(edge_list, ignore_index=True)
        
        # Create the NetworkX graph
        G = nx.from_pandas_edgelist(combined_df, 'source', 'target', 'weight', create_using=nx.Graph())
        
        # Save the graph
        nx.write_gexf(G, out_put_path)
        print("Network graph saved to:", out_put_path)
    else:
        print("No data to combine.")


# edge_list = []
# for filename in all_files:
#     df = pd.read_csv(filename)
#     edge_list.append(df)

# combined_df = pd.concat(edge_list, ignore_index=True)

# G = nx.from_pandas_edgelist(combined_df, 'source', 'target', 'weight', create_using=nx.Graph())
# nx.write_gexf(G, out_put_path)

# print("Network graph saved to:", out_put_path)