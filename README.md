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
3. Open the `.env` file and replace the placeholder with your API key:

For ClickUp specifically, you'll need to create an app and generate a client_id and client_secret. Follow the guide here: [ClickUp Authentication Guide](https://developer.clickup.com/docs/authentication#oauth-flow)

### Testing
Run `adk web` and access the ADK dev UI.

