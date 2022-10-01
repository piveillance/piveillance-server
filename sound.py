from queue import Queue
import asyncio
from typing import Dict
from os import walk, path, listdir
import json

import speech_recognition as sr
from googleapiclient import discovery

# stored as plaintext, please don't steal (:
API_KEY = "AIzaSyDs9Ppmwz4TQF6iCKixIKjNEjnb9VAaypE"
PWD = path.dirname(path.realpath(__file__))

# Type to represent the files that have been read and associated toxicity
# In the format [name, score(0-1)]
read_files = Dict[str, float]


class Sound:
    def __init__(self, dirname: str = "audio"):
        self.r = sr.Recognizer()
        self.audio_queue = Queue()
        self.read: read_files = {}
        self.dir = path.join(PWD, dirname)

        self.client = discovery.build(
            "commentanalyzer",
            "v1alpha1",
            developerKey=API_KEY,
            discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
            static_discovery=False,
        )

    """
    Read the audio files in the directory and process them
    """
    async def read_dir(self):
        tasks = []

        for filename in listdir(self.dir):
            new_task = self.read_file(filename)
            tasks.append(new_task)

        await asyncio.gather(*tasks)

    """
    Process a single file
    """
    async def read_file(self, filename: str):
        print("start!")
        with sr.AudioFile(path.join(self.dir, filename)) as file:
            data = self.r.record(file)
            phrase = await self.speech_to_text(data)
            sentiment = await self.text_to_sentiment(phrase)
            self.read[filename] = sentiment
        print("done!")

    async def speech_to_text(self, data: sr.AudioData) -> str:
        return self.r.recognize_google(data)

    async def text_to_sentiment(self, phrase: str) -> float:
        req = {
            'comment': {'text': phrase},
            'requestedAttributes': {'TOXICITY': {}}
        }

        res = self.client.comments().analyze(body=req).execute()
        return float(res["attributeScores"]["TOXICITY"]["summaryScore"]["value"])

    """
    Return the data of all files that have been read and clear them out of the buffer
    """
    def get_read_data(self) -> read_files:
        buffer = self.read
        self.read = {}
        return buffer


if __name__ == "__main__":
    soundQ = SoundQueue()
    asyncio.run(soundQ.read_dir())
    print(soundQ.read)
