import logging
import os
import numpy as np
import sounddevice as sd
import soundfile as sf
from settings import (
    DURATION,
    DEFAULT_SAMPLE_RATE,
    MAX_INPUT_CHANNELS,
    WAVE_OUTPUT_FILE,
)

logger = logging.getLogger("src.sound")

class Sound:
    def __init__(self):
        self.sample_rate = DEFAULT_SAMPLE_RATE
        self.channels = MAX_INPUT_CHANNELS
        self.duration = DURATION
        self.path = WAVE_OUTPUT_FILE
        self.recording = None

    def record(self):
        logger.info(f"Recording started for {self.duration} seconds")
        self.recording = sd.rec(
            int(self.duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="float32"
        )
        sd.wait()
        logger.info("Recording completed")
        self.save()

    def save(self):
        # Ensure parent directory exists
        dirname = os.path.dirname(self.path)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)
            
        if self.recording is not None:
            sf.write(self.path, self.recording, self.sample_rate)
            logger.info(f"Recording saved to {self.path}")
        else:
            logger.error("No recording data to save")

    def play(self):
        if os.path.exists(self.path):
            logger.info(f"Playing the recorded sound {self.path}")
            data, fs = sf.read(self.path, dtype="float32")
            sd.play(data, fs)
            sd.wait()
        else:
            logger.warning("No recording file found to play.")

# Global instance of Sound
sound = Sound()
