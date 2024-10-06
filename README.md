![Dreamscape Symphony](logo.png)
# Dreamscape Symphony 🎶

Dreamscape Symphony is an AI-powered web app that transforms your dreams into personalized song lyrics and generates text-to-speech (TTS) audio. Using advanced natural language processing techniques, the app analyzes dream descriptions to extract key themes, named entities, and emotions, creating unique songs from your subconscious thoughts.

## 🚀 Features

- **Dream Analysis**: Extracts named entities, sentiments, keywords, and themes from your dream descriptions.
- **Lyrics Generation**: Produces personalized song lyrics in genres like Pop, Rock, Carnatic, Samba, and Hip-Hop.
- **Text-to-Speech (TTS)**: Converts the generated lyrics into speech so you can listen to the song based on your dream.
- **Image Upload**: Option to upload images that relate to your dream and display them alongside the lyrics.
- **PDF Export**: Download the generated lyrics and images as a well-formatted PDF, making it a great keepsake.
- **Downloadable TTS Audio**: Allows users to download the generated TTS audio file of the lyrics.
- **Custom Themes**: Supports light and dark mode for personalized user experience.

## 🖥️ Demo

You can try out the live version of Dreamscape Symphony here:

[Live Demo on Streamlit Cloud](#https://dreamscape-symphony.streamlit.app/)

## 📖 Usage

1. **Describe your dream**: Enter a brief description of your dream in the input box.
2. **Optional Image**: Upload an image related to your dream to enhance the visualization.
3. **Analyze Dream**: Click the "Analyze Dream" button to extract named entities, keywords, and emotional tone from the dream.
4. **Generate Song Lyrics**: Choose a genre, then click "Generate Lyrics" to create a personalized song based on your dream.
5. **Listen to the Song**: Click "Listen to the Lyrics" to hear the generated lyrics using TTS.
6. **Download PDF & Audio**: You can download the lyrics and the album cover as a PDF, as well as the TTS audio file of the song.


## 🛠️ Installation

To run Dreamscape Symphony locally, follow these steps:

### Prerequisites

- Python 3.8 or higher
- `pip` (Python package manager)

### Clone the Repository

```bash
git clone https://github.com/your-username/dreamscape-symphony.git
cd dreamscape-symphony
```

### Install Dependencies

Create a virtual environment and install the required dependencies listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

### Add Your API Keys

Create a `secrets.toml` file in the .streamlit folder of the project and add your API key for the Hugging Face models.

```
[huggingface]
HUGGINGFACE_API_TOKEN=your_huggingface_api_token
```

### Run the App

```bash
streamlit run app.py
```

## 🧑‍💻 Contributing

We welcome contributions! Follow these steps to contribute to Dreamscape Symphony:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push the changes to your fork: `git push origin feature/your-feature-name`.
5. Create a pull request.

Please ensure that your code follows the project's style guidelines and is well-documented.

## 💬 Acknowledgments

- Thanks to the **Streamlit** community for providing an amazing framework to build and deploy web apps.
- Thanks the **Hugging Face** team for their powerful NLP models.
