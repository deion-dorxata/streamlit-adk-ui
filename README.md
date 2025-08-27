# adk-auth-tests

## Getting Started

### Setup Environment

You'll need to set up a virtual environment to run each agent.

```bash
# Create virtual environment in the root directory
python -m venv .venv

# Activate (each new terminal)
# macOS/Linux:
source .venv/bin/activate
# Windows CMD:
.venv\Scripts\activate.bat
# Windows PowerShell:
.venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt
```

Once set up, this single environment will work for all examples in the repository.

### Setting Up API Keys

Each example folder contains a `.env.example` file. For each project you want to run:

1. Navigate to the example folder
2. Rename `.env.example` to `.env` 
3. Open the `.env` file and replace the placeholder with your Google API key:


### Testing

Replace the sample_agent directory with your own agent.

Run `python main.py` to start the Fast API server. 

Next, open another terminal and run `streamlit run app.py` to access the Streamlit chat interface.

For now, the app uses a dummy sign-in screen to simulate user authentication. 

Initial session state is retrieved by using logged-in user's credentials to access a mock database implemeneted in json.



