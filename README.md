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
    source .venv\Scripts\activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file and add the following environment variables:
    ```env
    OUTPUT_FILE="utils/output.txt"
    WEB_FILE="utils/web.txt"
    LLM_CONTEXT="<your context>"
    ```

5. Install additional dependencies:
    ```sh
    pip install python-ffmpeg
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    ```

6. Configure the repository and install NVIDIA tools:
    ```sh
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
    curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    sudo apt-get update
    sudo apt-get install -y nvidia-container-toolkit
    ```

7. Pull the Docker container from Docker Hub:
    ```sh
    docker pull ollama/container
    ```

8. Allow GPU access and start the container:
    ```sh
    sudo nvidia-ctk runtime configure --runtime=docker
    sudo systemctl restart docker
    ```

9. Start the container with gpu access and volume mapping:
    ```sh
    docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
    ```

10. Run a model:
    ```sh
    docker exec -it ollama ollama run llama3
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
