from .config_parse import Config

import wave
import sounddevice as sd
from sounddevice import DeviceList
import pyaudio


CHUNK = 1024


def find_output():
    output_devs: DeviceList | dict = sd.query_devices()
    if isinstance(output_devs, dict):
        raise NotImplementedError("Query device was not supposed to return a dict...")

    config = Config.config

    for i in output_devs:
        name = i["name"].lower()
        if (
            # speaker name has all terms required
            (all([(term.lower() in name) for term in config.speaker_has]))
            # speaker name doesn't have banned terms
            and (all([term.lower() not in name for term in config.speaker_not_have]))
            # speaker can actually output audio
            and (i["max_output_channels"] > 0)
        ):
            return i["index"]

    raise Exception("Output not found")


def play_ringtone():
    with wave.open("GeometryRingtone.wav", "rb") as wf:
        p = pyaudio.PyAudio()

        out_dev = find_output()

        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True,
            output_device_index=out_dev,
        )

        try:
            while len(data := wf.readframes(CHUNK)):
                stream.write(data)
        except KeyboardInterrupt:
            print("Closing Stream...")

        stream.close()

        p.terminate()


if __name__ == "__main__":
    play_ringtone()
