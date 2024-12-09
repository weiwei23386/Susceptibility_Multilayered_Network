# Susceptibility_Multilayered_Network

## Experiment Workflow and Guidelines

This repository contains the code and methodology for analyzing media credibility and subreddit interactions using a multilayered network approach. The workflow is divided into several steps, each implemented through dedicated scripts.

---

## **Overview**

The experiment involves:
1. Extracting news headlines related to specific political events.
2. Analyzing headline relevance using sentence embeddings.
3. Evaluating headline credibility using a large language model (LLM) such as ChatGPT.
4. Constructing a credibility network from the evaluated headlines.
5. Analyzing subreddit posts to refine the credibility network.
6. Incorporating temporal dynamics into a multilayer network.
7. DEtecting the anomaly community by computing ACE score.

---

## **Workflow**

### **1. Data Collection and Query Design**

**Script**: `gdelt_news_extractor.py`  
**Description**: Customize parameters to extract relevant news headlines.  

**Steps**:
- Modify the **date range**, **keywords**, **news sources**, and whether to include article content.
- Example Keywords: “Trump,” “Capitol,” “riot.”

**Methodology**:
- A neutral query text guides the analysis, focusing on the background, intent, and outcomes of events like the January 6 Capitol attack.
- Use `sentence_similarity.py` to input the query (`doc1` variable) and calculate similarity scores using TFIDF.

---

### **2. Headline Selection and Evaluation**

**Script**: `headlines_evaluation.py`  
**Description**: 
- Configure ChatGPT API access.
- Modify the prompt for LLM evaluation.  

**Steps**:
1. **Top \(k\) Selection**:
   - Identify the top \(k\) headlines from each source using cosine similarity (threshold: 0.6–0.7).
   - Select up to 20 headlines per source.
2. **Credibility Evaluation**:
   - Evaluate headlines using an LLM with the following prompt:  
     > "Assume the information is correct and factual. Judge the credibility of other sources. Score 0 (fake) to 1 (true) and explain in 10 words or less."
3. **Output**:
   - LLM-generated credibility scores and brief explanations.

---

### **3. Credibility Network Construction**

**Script**: `credibility_graph.py`  
**Description**: Use LLM scores to create a credibility network.  

**Methodology**:
- **Nodes**: Represent media sources.
- **Edges**: Weighted by the average credibility scores between sources.

---

### **4. Subreddit Post Analysis**

**Script**: `reddit_multilayered.ipynb`  
**Description**: Analyze subreddit discussions related to selected news headlines.  

**Steps**:
1. Search for subreddit posts referencing the selected headlines.
2. Identify interactions between subreddit communities and media sources.
3. Integrate these insights into the credibility network.

---

### **5. Heterogeneous Multilayer Network Construction and Temporal Analysis (ACE score)**

**Script**: `anomaly_detection.ipynb`  
**Description**: Incorporate temporal dynamics into a multilayer network.  

**Steps**:
1. Analyze daily shifts in credibility scores for each news source.
2. Track community interactions and their evolution over time.
3. Construct a multilayer network to visualize and understand temporal changes.

---

## **Setup Instructions**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/wc23386/Susceptibility_Multilayered_Network.git
   cd Susceptibility_Multilayered_Network```

## **Install Dependencies**:

```bash
   pip install -r requirements.txt
```

## **Modify Parameters**:

Update configuration files or variables in scripts as needed.
Ensure API keys (e.g., ChatGPT) are properly set up.

## **Outputs**
1. Credibility Network: Nodes: Media sources. Edges: Weighted by credibility alignment.
2. Subreddit Analysis: Mapping of subreddit interactions to media sources.
3. Temporal Analysis: Dynamic credibility and interaction shifts.

## **Contributing**
Contributions are welcome! Feel free to submit issues or pull requests.

Contact
Author: WeiChun Chang, Jennifer Rozenblit
Email: weichun.chang@utexas.edu, jrozenblit@utexas.edu
Date: Dec 09 2024
