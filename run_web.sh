#!/bin/bash

# Start FastAPI (main.py) in the background
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit (chat_ui.py) in the foreground
streamlit run chat_ui.py --server.port 8501 --server.address 0.0.0.0
```

#### 3. Update `requirements.txt`

Ensure your `requirements.txt` file has the following web server dependencies for Docker:

```text
streamlit
requests
fastapi
uvicorn
python-dotenv
google-generativeai
qdrant-client
sentence-transformers
beautifulsoup4
```

#### 4. Deploy using Google Cloud Run

1.  **Commit and Push:** Upload all your files (including the new `Dockerfile` and `run_web.sh`) to your GitHub repository.
2.  **Go to Google Cloud Run:** Use the Google Cloud platform to deploy the container. (This requires setting up a Google Cloud account and using the `gcloud CLI` from your terminal).
3.  **Deployment Command:** You would run a command like:
    ```bash
    gcloud run deploy zebo-chatbot --source .
    
