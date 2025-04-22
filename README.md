# Agno Chainlit

## Setup Instructions

1. Install dependencies using uv and node version:
```bash
uv sync
```

use node version 18 from .nvmrc
```
nvm use
```

2. Set up environment variables:
   - Copy the `.env.example` file to create a new `.env` file:
   ```bash
   cp .env.example .env
   ```
   - Edit the `.env` file with your configuration values

3. Run the project:
```bash
uv run run.py
```

4. visit browser

```

localhost:8000/chainlit

```