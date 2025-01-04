# Home Assistant Project

Welcome to the Home Assistant Project! This project aims to create a voice-activated assistant using various Python libraries and APIs.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/home-assistant.git
    cd home-assistant
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file and add the following environment variables:
    ```env
    OUTPUT_FILE="utils/output.txt"
    WEB_FILE="utils/web.txt"
    LLM_CONTEXT="You are Friday, an AI assistant. You will provide short funny answers"
    ```

## Usage

To start the assistant, run the following command:
```sh
python recog.py
```

The assistant will listen for voice commands and respond accordingly.

## Project Structure

```
home-assistant/
├── data/
│   ├── llm_queries.txt
│   └── output.txt
├── utils/
│   ├── __init__.py
│   ├── audio.py
│   ├── llm.py
│   ├── text_to_speech.py
│   └── web_search.py
├── .env
├── .gitignore
├── Dockerfile
├── README.md
├── recog.py
└── requirements.txt
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.