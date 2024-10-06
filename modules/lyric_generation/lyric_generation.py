from typing import List, Tuple
import streamlit as st

import requests
from dotenv import load_dotenv
import os
import re


class LyricGenerator:
    """
    A class for generating lyrics based on specified genre and topic.

    Attributes:
        api_url (str): The API URL for the AI model.
        api_token (str | None): The HuggingFace API token.
        prompt_genere (dict): A dictionary containing genre-specific prompts for generating lyrics.

    Methods:
        __init__(self): Initializes the LyricGenerator class.
        get_api_token(self)->None: Retrieves the HuggingFace API token from the environment variables.
        generate_prompt(self, topics:List[str], named_entity:List[str], keywords:List[str], sentiment:str, genre:str)->str: Generates a prompt for the AI model to generate catchy and upbeat lyrics based on the specified genre and topic.
    """

    def __init__(self):
        """
        Initialize the LyricGenerator class.

        :return: None
        """
        self.api_url = "https://api-inference.huggingface.co/models/microsoft/Phi-3.5-mini-instruct"
        self.api_token = None
        self.prompt_genere = {
            "pop": "Ensure the genre is **Pop**, and make the lyrics upbeat and catchy, celebrating simple joys like eating ice cream. Structure the lyrics with verses and a repetitive chorus that invites listeners to sing along.",
            "rock": "Ensure the genre is **Rock**, and create energetic and powerful lyrics that celebrate adventure and spontaneity. Incorporate driving rhythms and a memorable chorus that inspires excitement and movement.",
            "carnatic": "Ensure the genre is **Classical Indian (Carnatic)**, and compose intricate and melodic lyrics that highlight the beauty of nature and everyday experiences. Structure the lyrics with verses that flow seamlessly into a captivating refrain.",
            "samba": "Ensure the genre is **Samba**, and create vibrant and fun lyrics that capture the excitement of street parties and summer celebrations. Structure the lyrics with upbeat verses and a repetitive chorus that embodies the spirit of dance and community.",
            "hip-hop": "Ensure the genre is **Hip-Hop**, and write clever and rhythmic lyrics that playfully describe the fun of enjoying ice cream and having a good time with friends. Structure the lyrics with engaging verses and a catchy hook that encourages listeners to vibe along.",
        }
        self.get_api_token()

    def get_api_token(self) -> None:
        """
        Retrieve the HuggingFace API token from the environment variables.

        :return: None
        """
        self.api_token = st.secrets("HUGGINGFACE_API_TOKEN")

    def generate_prompt(
        self,
        topics: List[str],
        named_entity: List[str],
        keywords: List[str],
        sentiment: str,
        genere: str,
        dream: str,
    ) -> str:
        """
        Generate a prompt for the AI model to generate catchy and upbeat lyrics based on the specified genre and topic.

        :param topics: A list of topics that should be included in the lyrics.
        :type topics: List[str]

        :param named_entity: A list of named entities that must be mentioned in the lyrics.
        :type named_entity: List[str]

        :param keywords: A list of keywords that should be included in the lyrics.
        :type keywords: List[str]

        :param sentiment: The sentiment that should be conveyed in the lyrics.
        :type sentiment: str

        :param genre: The genre of the lyrics.
        :type genre: str

        :return: A prompt for the AI model to generate lyrics based on the specified parameters.
        :rtype: str
        """

        prompt = f"""## Lyric Generation based on Topic:

**Objective:** Generate catchy and upbeat lyrics based on genre and topic.

**Topics:** 
{",".join(topics)}

The named entities "{",".join(named_entity)}" must be mentioned.

Use the following keywords in the lyrics: 
{",".join(keywords)}

**Sentiment:** The sentiment must be {sentiment}.

Use the following text to guide you:  
"{dream}" 

{self.prompt_genere[genere]} 

Give a *minimum of  4 verses.* 

Give the output Lyrics in the following format:
```md
<LYRICS>
GIVE THE LYRICS HERE
</LYRICS>
```

Five the complete Output. **Do not leave any blank lines or placeholders**.
"""
        return prompt

    def clean_output(self, generated_text: str) -> str:
        """
        Clean and extract the generated lyrics from the API response.

        This function processes the  response from the API, extracts the generated text,
        and cleans it to retrieve only the content within the <LYRICS> tags.

        :param generated_text: The text response from the API containing the generated text.
        :type generated_text: str

        :return: The cleaned and extracted lyrics.
        :rtype: str
        """
        print(generated_text)
        pattern = r"<LYRICS>(.*?)</LYRICS>"
        matchs = re.findall(pattern, generated_text, re.DOTALL)
        generated_lyrics = "".join(matchs[-1])
        return generated_lyrics.strip()

    def generate_lyrics(
        self,
        topics: List[str],
        named_entity: List[str],
        keywords: List[str],
        sentiment: str,
        genere: str,
        dream: str,
    ):
        """
        Generate catchy and upbeat lyrics based on the specified genre and topic using an AI model.

        :param topics: A list of topics that should be included in the lyrics.
        :type topics: List[str]

        :param named_entity: A list of named entities that must be mentioned in the lyrics.
        :type named_entity: List[str]

        :param keywords: A list of keywords that should be included in the lyrics.
        :type keywords: List[str]

        :param sentiment: The sentiment that should be conveyed in the lyrics.
        :type sentiment: str

        :param genre: The genre of the lyrics.
        :type genre: str

        :param dream: A text that should guide the AI model in generating the lyrics.
        :type dream: str

        :return: The generated lyrics in a string format.
        :rtype: str
        """
        
        prompt = self.generate_prompt(
            keywords=keywords,
            sentiment=sentiment,
            named_entity=named_entity,
            topics=topics,
            genere=genere.lower(),
            dream=dream,
        )
        headers = {"Authorization": f"Bearer {self.api_token}"}
        payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 15000,
            "temperature": 0.7,
            "top_p": 0.9,
        },
    }

        response = requests.post(self.api_url, headers=headers, json=payload)
        try:
            if response.json().get("error", None) is not None:
                return f"Error occurred :{response.json().get("error", None)}"
        except:
            pass
        generated_text = response.json()[0]["generated_text"].replace(prompt,"")
        generated_lyrics = self.clean_output(generated_text)
        return generated_lyrics
