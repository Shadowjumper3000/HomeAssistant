# Home Assistant Project

I wanna make Friday from Iron Man.
This is that project.

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

4. Create a [.env](http://_vscodecontentref_/3) file and add the following environment variables:
    ```env
    OUTPUT_FILE=".data/output.txt"
    WEB_FILE=".data/web.txt"
    LLM_FILE=".data/llm.txt"
    LLM_MODEL="deepseek-r1"
    LLM_API_URL="http://localhost:11434/api/generate"
    LLM_CONTEXT="You are Friday, an AI Assistant.
    You are designed to help people with their daily tasks.
    You keep your answers short and to the point."
    ELEVENLABS_APIKEY="<your elevenlabs api key>" # Optional/Required if TTS_ENGINE="elevenlabs"
    FFMPEG_PATH="<your ffmpeg path>"
    DEBUG="True"
    TTS_ENGINE="pyttsx3"  # Options: "pyttsx3", "elevenlabs" (requires API key)
    ```

5. Install additional dependencies:
    ```sh
    pip install python-ffmpeg
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    ```

6. Configure the repository and install NVIDIA tools (if using GPU):
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

8. Allow GPU access and restart docker:
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
    docker exec -it ollama ollama run <deepseek-r1>
    ```

## Usage

To start the assistant, run the following command (or run main.py in your IDE):
```sh
python main.py
```

The assistant will listen for voice commands and respond accordingly.

## Project Structure

```
├─] .audio_data/ (ignored)
├─] .data/ (ignored)
├─] .env (ignored)
├── .gitignore
├─] .venv/ (ignored)
├── audio_recording/
│   ├── recording.py
│   ├── __init__.py
├── llm/
│   ├── llm_interaction.py
│   ├── __init__.py
└── tts/
    ├── tts.py
    ├── __init__.py
├── main.py
├── README.md
├── requirements.txt

```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
