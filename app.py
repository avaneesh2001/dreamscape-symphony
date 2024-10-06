# app.py

import streamlit as st
import time
import os
from PIL import Image
from gtts import gTTS

from modules.dream_analysis.dream_analysis import DreamAnalyzer
from modules.lyric_generation.lyric_generation import LyricGenerator
from modules.pdf_generator.pdf_generator import PDFGenerator

# Initialize the DreamAnalyzer
dream_analyzer = DreamAnalyzer()
lyrics_generator = LyricGenerator()
pdf_generator = PDFGenerator()

# Set the page configuration
st.set_page_config(
    page_title="Dreamscape Symphony",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "dream_analysis_done" not in st.session_state:
    st.session_state.dream_analysis_done = False
if "lyrics_generation_done" not in st.session_state:
    st.session_state.lyrics_generation_done = False
if "dream_analysis_results" not in st.session_state:
    st.session_state.dream_analysis_results = {}

# Title and Description
st.title("Dreamscape Symphony")
st.write(
    """
Transform your dreams into personalized music lyrics and visual representations using advanced AI technologies.
"""
)

# Layout: Two Columns
col1, col2 = st.columns(2)

with col1:
    # Dream Input Section
    st.header("1. Enter Your Dream")
    dream_text = st.text_area(
        "Describe your dream in about 500 charecters:", height=200
    )
    st.session_state.dream_text = dream_text

    if len(dream_text) > 515:
        st.warning("Your dream description exceeds 500 characters. Please shorten it.")

    # Optional Image Upload
    st.header("2. Upload an Image (Optional)")
    uploaded_image = st.file_uploader(
        "Choose an image related to your dream", type=["jpg", "jpeg", "png"]
    )

    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)
    else:
        image = None
    st.session_state.image = image


with col2:
    # Analyze Dream Button
    st.header("3. Analyze Your Dream")
    analyze_button = st.button("Analyze Dream")

    if analyze_button:
        if dream_text.strip() == "":
            st.warning("Please enter a dream description to proceed.")
        else:
            with st.spinner("Analyzing your dream..."):
                named_entities, sentiment, keywords, themes = (
                    dream_analyzer.analyze_dream(dream_text)
                )

                # Store results in session state
                st.session_state.dream_analysis_done = True
                st.session_state.dream_analysis_results = {
                    "named_entities": named_entities,
                    "sentiment": sentiment,
                    "keywords": keywords,
                    "themes": themes,
                }

            st.subheader("Dream Analysis Results")

            named_entities = st.session_state.dream_analysis_results["named_entities"]
            emotion, score = st.session_state.dream_analysis_results["sentiment"]
            keywords = st.session_state.dream_analysis_results["keywords"]
            themes = st.session_state.dream_analysis_results["themes"]

            st.markdown("**Named Entities:**")
            if named_entities:
                for entity in named_entities:
                    st.write(f"- **{entity}**")
            else:
                st.write("No named entities identified.")

            st.markdown(f"**Emotional Tone:** {emotion} (Confidence: {score:.2f})")

            st.markdown(
                "**Keywords:** "
                + (", ".join(keywords) if keywords else "No keywords identified.")
            )

            if themes:
                st.markdown("**Themes:**")
                for theme_group in themes:
                    st.markdown(f""" - {", ".join(theme_group)}""")
            else:
                st.markdown("**Themes:** No themes identified.")

# Generate Lyrics
st.header("4. Generate Song Lyrics")
genere = st.selectbox(
    "Choose a genre:", ["Pop", "Rock", "Carnatic", "Samba", "Hip-Hop"]
)
lyrics_generator_button = st.button("Generate Lyrics")

if lyrics_generator_button:
    if not st.session_state.dream_analysis_done:
        st.warning("Please analyze the dream to proceed.")
    else:
        keywords = st.session_state.dream_analysis_results["keywords"]
        emotion = st.session_state.dream_analysis_results["sentiment"][0]
        named_entities = st.session_state.dream_analysis_results["named_entities"]
        themes = st.session_state.dream_analysis_results["themes"]
        dream = st.session_state.dream_text

        if themes:
            with st.spinner("Generating lyrics..."):
                lyrics = lyrics_generator.generate_lyrics(
                    keywords=keywords,
                    sentiment=emotion,
                    named_entity=named_entities,
                    topics=themes[0],
                    genere=genere.lower(),
                    dream=dream,
                )
                st.subheader("Generated Lyrics")
                placeholder = st.empty()
                st.session_state.lyrics_generation_done = True
                st.session_state.lyrics = lyrics
                displayed_text = ""

                for char in lyrics:
                    displayed_text += char
                    placeholder.text(displayed_text)
                    time.sleep(0.01)
        else:
            st.warning("No themes were identified, unable to generate lyrics.")

if st.session_state.lyrics_generation_done:
    lyrics_audio_button = st.button("Listen to the lyrics")
    if lyrics_audio_button:
        audio_file = None
        with st.spinner("Generating audio file..."):
            tts = gTTS(text=st.session_state.lyrics, lang="en")
            audio_file = "lyrics_audio.mp3"
            tts.save(audio_file)
            st.audio(audio_file)

            if audio_file is not None:
                with open(audio_file, "rb") as file:
                    audio_data = file.read()

                st.download_button(
                    label="Download Lyrics Audio",
                    data=audio_data,
                    file_name="lyrics_audio.mp3",
                    mime="audio/mpeg",
                )

# Generate PDF

st.header("5. Generate Album Cover and Lyrics as PDF")
pdf_button = st.button("Generate PDF")

if pdf_button:
    if not st.session_state.lyrics_generation_done:
        st.warning("Please generate lyrics to proceed.")
    else:
        pdf_data = pdf_generator.create_pdf(st.session_state.lyrics, image)
        st.download_button(
            label="Download Album Cover + Lyrics as PDF",
            data=pdf_data,
            file_name="album_and_lyrics.pdf",
            mime="application/pdf",
        )
