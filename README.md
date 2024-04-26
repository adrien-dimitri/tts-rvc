
# TTS-RVC-API

Yes, we can use Coqui with RVC!

# Why combine the two frameworks?

Coqui is a text-to-speech framework (vocoder and encoder), but cloning your own voice takes decades and offers no guarantee of better results. That's why we use RVC (Retrieval-Based Voice Conversion), which works only for speech-to-speech. You can train the model with just 2-3 minutes of dataset as it uses Hubert (a pre-trained model to fine-tune quickly and provide better results).


## Installation

How to use Coqui + RVC api?

1. **Clone the repository**

    ```bash
    git clone https://github.com/adrien-dimitri/tts-rvc
    ```

2. **(Recommended) Create and Activate a Virtual Environment:**

   - **On Windows:**

     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```

   - **On macOS and Linux:**

     ```bash
     virtualenv <venv_name>
     source <venv_name>/bin/activate
     ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    pip install TTS
    pip install dvc dvc-gdrive
    ```

4. **Import the models using DVC:**

    ```bash
    dvc pull
    ```

5. **Update the `config.toml` file:**

    - Update the `model_dir` path to the directory where the RVC v2 model is stored.
    - Create a directory called `tmp` in the root directory. (This is where the generated audio files will be stored.)


6. **Run the server:**

    ```bash
    python -m uvicorn app.main:app
    ```


## Information

Where the RVC v2 model is mounted on the container at:

```python
  /
└── models
      └── speaker1
          ├── speaker1.pth
          └── speaker1.index
```


## POST REQUEST

```bash
http://localhost:8000/generate
```

```python
emotions : happy,sad,angry,dull
speed = 1.0 - 2.0
```

```python
{
"speaker_name": "speaker3",
"input_text": "Hey there! Welcome to the world",
"emotion": "Surprise",
"speed": 1.0
}
```
   
# CODE SNIPPET

```python
import requests
import json
import time

url = "http://127.0.0.1:8000/generate"

payload = json.dumps({
  "speaker_name": "speaker3",
  "input_text": "Are you mad? The way you've betrayed me is beyond comprehension, a slap in the face that's left me boiling with an anger so intense it's as if you've thrown gasoline on a fire, utterly destroying any trust that was left.",
  "emotion": "Dull",
  "speed": 1.0
})
headers = {
  'Content-Type': 'application/json'
}

start_time = time.time()  # Start the timer

response = requests.request("POST", url, headers=headers, data=payload)

end_time = time.time()  # Stop the timer

if response.status_code == 200:
    audio_content = response.content
    
    # Save the audio to a file
    with open("generated_audio.wav", "wb") as audio_file:
        audio_file.write(audio_content)
        
    print("Audio saved successfully.")
    print("Time taken:", end_time - start_time, "seconds")
else:
    print("Error:", response.text)
```

## Adjusting the TTS Parameters

To adjust the parameters of the TTS model, you need to locate the `tts.py`  file which can be found at `app/routers/tts.py` in line 22.

### Changing the TTS Model

Simply change the `model_name` parameter to the desired model name.

| model_name| language | gender |
|------------|----------|--------|
| tts_models/de/thorsten/tacotron2-DDC | de | male   |
| tts_models/de/css10/vits-neon        | de | female |
| tts_models/en/ljspeech/vits          | en | female |
| tts_models/en/sam/tacotron-DDC       | en | male   |



### Activating CUDA

To activate CUDA, change the `gpu` parameter to `True`.

#### Example:

The file should look like this:

```python
# Initialize TTS
tts = TTS(model_name="tts_models/en/ljspeech/vits", progress_bar=True, gpu=False)
```

Change it to:
  
```python
# Initialize TTS
tts = TTS(model_name="tts_models/en/ljspeech/vits", progress_bar=True, gpu=True)
```
