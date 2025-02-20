# Create subdirectories
mkdir -p data models src notebooks frontend

# Create necessary files
touch data/mlflow_docs.json
touch data/mlflow_chunks.json
touch data/mlflow_embeddings.json

touch models/README.md  # Placeholder for model storage

touch src/retriever.py
touch src/embeddings.py
touch src/chatbot.py
touch src/evaluator.py
touch src/database.py
touch src/app.py

touch notebooks/scraping.ipynb
touch notebooks/chatbot_testing.ipynb

mkdir -p frontend
touch frontend/index.html
touch frontend/chatbot.js

# Create config and requirements files
touch config.yaml
touch requirements.txt
touch README.md

# Initialize Git repository
git init

# Create .gitignore
cat <<EOL > .gitignore
# Ignore data and model files
data/
models/
*.json
*.pkl
*.log
*.db
__pycache__/
*.ipynb_checkpoints/
EOL

# First Git commit
git add .
git commit -m "Initial project setup"