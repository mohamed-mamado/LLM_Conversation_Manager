# LLM Conversation Manager
This repository contains a project aimed at managing user conversation histories for language model interactions. It supports the efficient storage of conversations in a database and provides features like token counting, user history management, and conversation summaries. The code currently supports tokenization for GPT-based models and Hugging Face models.

## Features:
- **Database Management**: Using PostgreSQL, the system stores user information, conversations, and tokenized messages.
- **Token Counting**: Support for counting tokens using GPT (tiktoken) and Hugging Face models.
- **Conversation Summaries**: Generates summaries of conversations based on token counts or number of messages.
- **User History**: Fetches historical conversations for each user.
- **Optimized History Creation**: The conversation history is stored and retrieved using highly optimized database queries, ensuring fast access and management even for large-scale data.
## Project Structure:
- `DatabaseManager.py`: Manages PostgreSQL database operations, including creating, deleting, and fetching user and conversation data.
- `TokenizerHelper.py`: Helper class for counting tokens in conversations, supporting both GPT and Hugging Face models.
## Future Improvements:
- **Add Support for More Databases:**
  - In addition to PostgreSQL, the system could be extended to support other databases such as MySQL, MongoDB, or SQLite.
- **Incorporate More Algorithms:**
  - Add algorithms to optimize the tokenization process, summarization methods, or conversation analysis.
  - **Examples:**
    - Use **TF-IDF (Term Frequency-Inverse Document Frequency)** to enhance the conversation summary generation process.
    - Implement **Sentence Transformers** for more advanced semantic analysis of conversations.
    - Apply **Clustering Algorithms (e.g., K-Means, DBSCAN)** to group similar conversations for improved organization and retrieval.
- **Framework Compatibility:**
  - Ensure the system is compatible with popular frameworks like **LangChain**, **CrewAI**, and **LlamaIndex**, making it easy to integrate with existing workflows for language model pipelines.
    - **LangChain:** Enables the chaining of different components (models, databases, etc.) to handle complex conversation tasks.
    - **CrewAI:** Aids in conversational AI projects by managing different components, offering flexibility and control over the pipeline.
    - **LlamaIndex:** A framework to index and query large-scale documents, which could be integrated for efficient conversation history search and summaries.
## Optimized Settings for History Creation:
- **Highly Efficient Query Execution:** The system uses optimized queries for creating and managing conversation histories, ensuring minimal lag even when dealing with large datasets.
- **Data Indexing and Partitioning:** To improve retrieval times, the database can be indexed based on user and conversation IDs, and partitioned for large-scale operations.
- **Token and Conversation Tracking:** Tokens and conversation data are carefully tracked and managed, ensuring that conversations are efficiently summarized and stored.
