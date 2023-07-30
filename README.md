# Athena
To clone: 
1. clone repo
2. create new python virtual environment
3. Install requirements: 'pip install -r requirements.txt'
4. Install PGVector using homebrew or other
5. In postgres database to be used to run application enable PGVector extension : 'CREATE EXTENSION vector;'

Create .env file in top level directory with following content: 
OPENAI_API_KEY="" #your own OpenAI api key 

PGVECTOR_DRIVER="" #connection to postgres database with PGVector installed 
PGVECTOR_HOST=""
PGVECTOR_PORT=""
PGVECTOR_DATABASE=""
PGVECTOR_USER=""
PGVECTOR_PASSWORD=""
