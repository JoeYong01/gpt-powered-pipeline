# LLM Call Log Transcription & classification
This Python project seeks to automate the transcription & analysis of audio call logs on disputes between customer support agents & customers using OpenAI `Whisper` for transcription & `GPT-3.5` for text analysis.

`GPT-3.5` here is used to evaluate whether the dispute has been resolved, a long with the identification of other features (for example in this case whether or not a discount/gift card was offered)

### Directory Structure
```
/project_root
|-- /call_logs       # Contains the call log audio files
|-- /db              # Contains the SQLite database file
|-- /logs            # Contains logging information
|-- /scripts         # Python script to initialize the database
|-- /src             # Source files for the project
|-- /tests           # Contains the pytest tests
```

### Usage
1. Activate the virtual environment & install the neccesary modules via:
   - `python -m venv venv`
   - `source venv\Scripts\activate`
   - `pip install -r requirements.txt`
2. Initialize the sqlite database:
   - `python scripts/initialize_db.py` 
3. Assuming a source system exists, the audio files can be uploaded into `/call_logs`.
4. Run the main script:
   - `python main.py`
5. Query the database:
   - `python scripts/query_db.py`

# Notes
As Threading is superior in performance compared to asyncio in this use-case, the main branch will focus development on threading

# Todo
- Productionize the script:
    - calculate processed token count against limit

# Done
- Processed files should be deleted/archived (& compressed)
- add tests for main functions
- Implement Logging
- Implement Threading
- Implement asyncio