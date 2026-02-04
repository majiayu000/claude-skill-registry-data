---
name: data-ai-ml-skill
description: Master machine learning, data engineering, AI engineering, MLOps, and prompt engineering. Build intelligent systems from data pipelines to production AI applications with LLMs, agents, and modern frameworks.
---

# Data, AI & ML Skill

Complete guide to building intelligent systems using data science, machine learning, and artificial intelligence.

## Quick Start

### Choose Your Path

```
Data → ML → Production
  ↓      ↓      ↓
Pandas SQL  Models
NumPy  ETL  Deployment
```

### Get Started in 5 Steps

1. **Python Fundamentals** (2-3 weeks)
   - NumPy, Pandas basics
   - Data manipulation

2. **Statistics & Math** (4-6 weeks)
   - Probability, distributions
   - Hypothesis testing
   - Linear algebra basics

3. **Machine Learning Algorithms** (6-8 weeks)
   - Supervised learning
   - Unsupervised learning
   - Scikit-learn library

4. **Deep Learning** (8-12 weeks)
   - Neural networks
   - PyTorch or TensorFlow

5. **Production & Deployment** (ongoing)
   - MLOps practices
   - Model serving
   - Monitoring

---

## Data Fundamentals

### **NumPy for Numerical Computing**

```python
import numpy as np

# Array creation
arr = np.array([1, 2, 3, 4, 5])
matrix = np.array([[1, 2], [3, 4]])
zeros = np.zeros((3, 3))
ones = np.ones(5)
range_arr = np.arange(0, 10, 2)

# Basic operations
arr + 5  # [6, 7, 8, 9, 10]
arr * 2  # [2, 4, 6, 8, 10]
np.sum(arr)  # 15
np.mean(arr)  # 3.0
np.std(arr)   # Standard deviation

# Indexing and slicing
arr[0]  # 1
arr[1:4]  # [2, 3, 4]
matrix[0, 1]  # 2

# Linear algebra
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
np.dot(A, B)  # Matrix multiplication
np.linalg.inv(A)  # Matrix inverse
```

### **Pandas for Data Analysis**

```python
import pandas as pd

# Create DataFrame
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'salary': [50000, 60000, 70000]
})

# Selecting data
df['name']  # Column
df.loc[0]  # Row by label
df.iloc[0]  # Row by position

# Filtering
df[df['age'] > 25]  # Age greater than 25
df[(df['age'] > 25) & (df['salary'] > 55000)]

# Aggregation
df.groupby('age')['salary'].mean()
df.describe()  # Summary statistics

# Missing data
df.isnull()  # Check for nulls
df.fillna(0)  # Fill nulls
df.dropna()  # Remove nulls

# Data transformation
df['age_group'] = pd.cut(df['age'], bins=[0, 30, 60])
df['name_upper'] = df['name'].str.upper()

# Merging
merged = pd.merge(df1, df2, on='id')
combined = pd.concat([df1, df2])
```

### **Data Visualization**

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Line plot
plt.plot(df['year'], df['sales'])
plt.xlabel('Year')
plt.ylabel('Sales')
plt.show()

# Scatter plot
plt.scatter(df['age'], df['salary'])

# Bar chart
df['category'].value_counts().plot(kind='bar')

# Histogram
plt.hist(df['age'], bins=10)

# Seaborn (higher level)
sns.scatterplot(x='age', y='salary', data=df, hue='department')
sns.heatmap(correlation_matrix, annot=True)

# Plotly (interactive)
import plotly.express as px
fig = px.scatter(df, x='age', y='salary', color='department')
fig.show()
```

---

## Machine Learning

### **Supervised Learning**

**Classification:**
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

# Load data
X = df[['feature1', 'feature2', 'feature3']]
y = df['target']  # 0 or 1

# Split: 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
```

**Regression:**
```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Metrics
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)
```

### **Unsupervised Learning**

**Clustering:**
```python
from sklearn.cluster import KMeans

# Determine optimal clusters
inertias = []
for k in range(1, 10):
    model = KMeans(n_clusters=k, random_state=42)
    model.fit(X)
    inertias.append(model.inertia_)

# Elbow method (plot and find elbow)
plt.plot(range(1, 10), inertias)
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia')
plt.show()

# Train final model
model = KMeans(n_clusters=3, random_state=42)
clusters = model.fit_predict(X)
```

**Dimensionality Reduction:**
```python
from sklearn.decomposition import PCA

# Reduce to 2 dimensions
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

print(f"Explained variance: {pca.explained_variance_ratio_}")
```

### **Feature Engineering**

```python
# Scaling
from sklearn.preprocessing import StandardScaler, MinMaxScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)

# Encoding categorical variables
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# Label encoding (ordinal)
le = LabelEncoder()
df['category_encoded'] = le.fit_transform(df['category'])

# One-hot encoding (nominal)
df_encoded = pd.get_dummies(df, columns=['category'])

# Feature selection
from sklearn.feature_selection import SelectKBest, f_classif

selector = SelectKBest(k=5)
X_selected = selector.fit_transform(X, y)
```

---

## Deep Learning

### **Neural Networks with PyTorch**

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# Define model
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(10, 64)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.sigmoid(self.fc3(x))
        return x

# Initialize
model = SimpleNN()
optimizer = optim.Adam(model.parameters(), lr=0.001)
loss_fn = nn.BCELoss()

# Training loop
for epoch in range(100):
    for X_batch, y_batch in train_loader:
        # Forward pass
        predictions = model(X_batch)
        loss = loss_fn(predictions, y_batch.unsqueeze(1))

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch + 1) % 10 == 0:
        print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")
```

### **Convolutional Neural Networks (CNN)**

```python
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(64 * 56 * 56, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 64 * 56 * 56)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x
```

---

## AI Engineering & LLMs

### **Working with Large Language Models**

**OpenAI API:**
```python
import openai

openai.api_key = "your-api-key"

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain machine learning in simple terms."}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)
```

**LangChain (LLM Framework):**
```python
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

llm = OpenAI(temperature=0.7)

template = """
You are an expert {expertise}.
{question}
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["expertise", "question"]
)

chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run(expertise="data scientist", question="What is feature engineering?")
```

### **Prompt Engineering**

**Few-Shot Learning:**
```python
prompt = """
Classify the sentiment: positive, negative, or neutral.

Examples:
"I love this product!" → positive
"This is terrible." → negative
"It's okay." → neutral

Classify: "Best purchase ever!"
"""
```

**Chain of Thought:**
```python
prompt = """
Let's think step by step.

Question: If a train leaves at 2 PM going 60 mph, and another at 3 PM at 80 mph, when does the second catch up?

Step 1: Set up equations
Step 2: Solve for time
Step 3: Verify answer
"""
```

### **Building AI Agents**

```python
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.llms import OpenAI

# Define tools
tools = [
    Tool(
        name="Calculator",
        func=lambda x: str(eval(x)),
        description="Useful for math"
    ),
    Tool(
        name="Search",
        func=google_search,
        description="Search the internet"
    )
]

agent = initialize_agent(
    tools,
    OpenAI(temperature=0),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

result = agent.run("What is 45 * 3? Then search for the capital of France.")
```

---

## MLOps (Production)

### **Model Versioning with MLflow**

```python
import mlflow
import mlflow.sklearn

mlflow.set_experiment("iris-classification")

with mlflow.start_run():
    # Log parameters
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 5)

    # Train model
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    # Log metrics
    accuracy = model.score(X_test, y_test)
    mlflow.log_metric("accuracy", accuracy)

    # Log model
    mlflow.sklearn.log_model(model, "random_forest_model")

# Later, load model
model = mlflow.sklearn.load_model("runs:/model_id/random_forest_model")
```

### **Model Serving with FastAPI**

```python
from fastapi import FastAPI
import joblib

app = FastAPI()
model = joblib.load('model.pkl')

@app.post("/predict")
async def predict(data: dict):
    features = [data['feature1'], data['feature2'], data['feature3']]
    prediction = model.predict([features])
    return {"prediction": prediction[0]}

# Run: uvicorn app:app --reload
```

### **Monitoring Models**

```python
# Detect data drift
from evidentlyai.dashboard import Dashboard
from evidentlyai.tabs import DataDriftTab

dashboard = Dashboard(tabs=[DataDriftTab()])
dashboard.calculate(reference_data, current_data)
dashboard.save("data_drift_report.html")
```

---

## Learning Roadmap

- [ ] Python fundamentals (NumPy, Pandas)
- [ ] Statistics and probability
- [ ] Data visualization
- [ ] Machine learning basics (Scikit-learn)
- [ ] Supervised learning (classification, regression)
- [ ] Unsupervised learning (clustering, dimensionality reduction)
- [ ] Deep learning (PyTorch or TensorFlow)
- [ ] Build 2-3 ML projects
- [ ] Learn MLOps basics
- [ ] LLMs and prompt engineering
- [ ] Deploy a model to production
- [ ] Ready for ML engineer role!

---

**Source**: https://roadmap.sh/machine-learning, https://roadmap.sh/ai-engineer, https://roadmap.sh/data-engineer
