# Athena Knowledge Resource Manager

## Problem/Motivation
Everywhere there are useful pieces of information scattered across the internet that could be used to increase productivity for individuals or entities. These bits of knowledge can be in forms like social media posts, websites, documents, and more. However, there's no unified tool to consolidate these resources for easy retrieval based on context or bits of remembered information.

## Proposed Solutions & Decisions
An optimal solution would offer:
- Saving data from diverse platforms.
- A lookup feature querying items based on keywords or ideas.

Thanks to recent advances in LLM (large language model) technology, we can transform textual data into vectors and execute similarity searches for the closest vector matches.

### Why this approach?
Packages like **LangChain** offer robust utilities to work with LLMs. By allowing users to input any URL into our system, we can scrape the data, convert it to a vector with LangChain, and then store it. **PGVector**, an extension to PostgreSQL, is chosen for its vector comparison capabilities like KNN to pinpoint the most suitable matches. Plus, using PGVector eliminates the need for a separate vector database alongside PostgreSQL.

## Experiment & Solutions
The system lets users input resources and later search them based on partial memories of the content. However, gauging the search result's correctness is subjective.

### Addressing the Subjectivity Challenge:
A "needle in a haystack" testing framework was crafted. Here, a collection ("haystack") of assorted documents is added to the database. Specific queries ("needles") anticipated to match specific items in the haystack are then tested. By evaluating accuracy, we can monitor performance over time, focusing on consistency and adaptability rather than raw accuracy.

Throughout the project, I found this solution effectively managed resources and heightened my productivity, simplifying the save-and-retrieve process for intriguing finds.

## Highlights & Technologies Used:

- 🚀 Developed a web application to store diverse resources and employ large language models for querying.
- 💾 Utilized **Django** for backend development.
- 🔗 Integrated **LangChain** for interactions with Large Language Models.
- 🗃️ Chose **PGVector** for storing LLM text vectors, enabling similarity searches.
- 🛠️ Created a testing infrastructure to subjectively evaluate performance, ensuring trackable progress over time.
- 📋 Managed the project and collaborated using **Trello**.


To clone: 
1. clone repo
2. create new python virtual environment
3. Install requirements: 'pip install -r requirements.txt'
4. Install PGVector using homebrew or other
5. In postgres database to be used to run application enable PGVector extension : 'CREATE EXTENSION vector;'

Create .env file in top level directory with following content: \
OPENAI_API_KEY="" #your own OpenAI api key \

PGVECTOR_DRIVER="" #connection to postgres database with PGVector installed \
PGVECTOR_HOST=""\
PGVECTOR_PORT=""\
PGVECTOR_DATABASE=""\
PGVECTOR_USER=""\
PGVECTOR_PASSWORD=""
