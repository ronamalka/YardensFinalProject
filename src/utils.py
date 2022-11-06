import soundfile
import numpy as np
import librosa
import glob
import os

from sklearn.model_selection import train_test_split


# all emotions on RAVDESS dataset
int2emotion = {
    "01": "neutral",
    "02": "calm",
    "03": "happy",
    "04": "sad",
    "05": "angry",
    "06": "fearful",
    "07": "disgust",
    "08": "surprised"
}

# # we allow these emotions
# AVAILABLE_EMOTIONS = {
#     "neutral",
#     "calm",
#     "happy",
#     "sad",
#     "angry",
#     "fearful",
#     "disgust",
#     "surprised",
#     "boredom"
# }

# we allow these emotions
AVAILABLE_EMOTIONS = {
    "fearful",
    "angry",
    "sad",
    "neutral",
    "happy"
}


def extract_feature(file_name, **kwargs):
    """
    Extract feature from audio file `file_name`
        Features supported:
            - MFCC (mfcc)
            - Chroma (chroma)
            - MEL Spectrogram Frequency (mel)
            - Contrast (contrast)
            - Tonnetz (tonnetz)
    """
    mfcc = kwargs.get("mfcc")
    chroma = kwargs.get("chroma")
    mel = kwargs.get("mel")
    contrast = kwargs.get("contrast")
    tonnetz = kwargs.get("tonnetz")
    with soundfile.SoundFile(file_name) as sound_file:
        X = sound_file.read(dtype="float32")
        sample_rate = sound_file.samplerate
        if chroma or contrast:
            stft = np.abs(librosa.stft(X))
        result = np.array([])
        if mfcc:
            mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
            result = np.hstack((result, mfccs))
        if chroma:
            chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
            result = np.hstack((result, chroma))
        if mel:
            mel = np.mean(librosa.feature.melspectrogram(y=X, sr=sample_rate).T, axis=0)
            result = np.hstack((result, mel))
        if contrast:
            contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0)
            result = np.hstack((result, contrast))
        if tonnetz:
            tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T, axis=0)
            result = np.hstack((result, tonnetz))
    return result


def load_data(test_size=0.25):
    X, y = [], []
    # ----------------------------------RAVDESS---------------------------------------------------------------------------
    for file in glob.glob("data\\RAVDESS\\Actor_*\\*.wav"):
        # get the base name of the audio file
        basename = os.path.basename(file)
        # get the emotion label
        emotion = int2emotion[basename.split("-")[2]]
        # we allow only AVAILABLE_EMOTIONS we set
        if emotion not in AVAILABLE_EMOTIONS:
            continue
        # extract speech features
        features = extract_feature(file, mfcc=True, chroma=True, mel=True)
        # add to data
        X.append(features)
        y.append(emotion)
    # ----------------------------arabic-----------------------------------------------------------------------------
    for file in glob.glob("data\\arabic\\*.wav"):
        # get the base name of the audio file
        basename = os.path.basename(file)
        # get the emotion label
        emotion = (((basename.split("_")[1:])[0]).split(".")[:1])[0]
        if emotion not in AVAILABLE_EMOTIONS:
            continue
        # extract speech features
        features = extract_feature(file, mfcc=True, chroma=True, mel=True)
        # add to data
        X.append(features)
        y.append(emotion)
    # ------------------------------emodb------------------------------------------------------------------------------
    for file in glob.glob("data\\emodb\\*.wav"):
        # get the base name of the audio file
        basename = os.path.basename(file)
        # get the emotion label
        label = (basename[5:6])
        if label == "W":
            emotion = 'angry'
        elif label == "L":
            emotion = 'boredom'
        elif label == "E":
            emotion = 'disgusted'
        elif label == "A":
            emotion = 'angry'
        elif label == "F":
            emotion = 'happy'
        elif label == "T":
            emotion = 'sad'
        elif label == "N":
            emotion = 'neutral'
        else:
            continue
        if emotion not in AVAILABLE_EMOTIONS:
            continue
        # extract speech features
        features = extract_feature(file, mfcc=True, chroma=True, mel=True)
        # add to data
        X.append(features)
        y.append(emotion)
    # -------------------------------SAVEE----------------------------------------------------------------------------
    for file in glob.glob("data\\SAVEE\\*.wav"):
        # get the base name of the audio file
        basename = os.path.basename(file)
        part = basename.split('_')[1]
        ele = part[:-6]
        if ele == 'a':
            emotion = 'angry'
        elif ele == 'd':
            emotion = 'disgust'
        elif ele == 'f':
            emotion = 'fearful'
        elif ele == 'h':
            emotion = 'happy'
        elif ele == 'n':
            emotion = 'neutral'
        elif ele == 'sa':
            emotion = 'sad'
        else:
            emotion = 'surprise'
        if emotion not in AVAILABLE_EMOTIONS:
            continue
        # extract speech features
        features = extract_feature(file, mfcc=True, chroma=True, mel=True)
        # add to data
        X.append(features)
        y.append(emotion)
    # -------------------------------CREMAD----------------------------------------------------------------------------
    # for file in glob.glob("data\\CREMAD\\*.wav"):
    #     # get the base name of the audio file
    #     basename = os.path.basename(file)
    #     part = basename.split('_')
    #     if part[2] == 'SAD':
    #         emotion = 'sad'
    #     elif part[2] == 'ANG':
    #         emotion = 'angry'
    #     elif part[2] == 'DIS':
    #         emotion = 'disgust'
    #     elif part[2] == 'FEA':
    #         emotion = 'fearful'
    #     elif part[2] == 'HAP':
    #         emotion = 'happy'
    #     elif part[2] == 'NEU':
    #         emotion = 'neutral'
    #     else:
    #         emotion = 'Unknown'
    #     if emotion not in AVAILABLE_EMOTIONS:
    #         continue
    #     # extract speech features
    #     features = extract_feature(file, mfcc=True, chroma=True, mel=True)
    #     # add to data
    #     X.append(features)
    #     y.append(emotion)
    # -------------------------------TESS-----------------------------------------------------------------------------
    for fi in glob.glob("data\\TESS\\OAF_*"):
        # get the base name of the audio file
        basename = os.listdir(fi)
        for file in basename:
            part = file.split('.')[0]
            part = part.split('_')[2]
            if part == "fear":
                emotion = 'fearful'
            elif part == 'ps':
                emotion = 'surprise'
            else:
                emotion = part
            if emotion not in AVAILABLE_EMOTIONS:
                continue
            # extract speech features
            features = extract_feature(fi + "\\" + file, mfcc=True, chroma=True, mel=True)
            # add to data
            X.append(features)
            y.append(emotion)
    for fi in glob.glob("data\\TESS\\YAF_*"):
        # get the base name of the audio file
        basename = os.listdir(fi)
        for file in basename:
            part = file.split('.')[0]
            part = part.split('_')[2]
            if part == "fear":
                emotion = 'fearful'
            elif part == 'ps':
                emotion = 'surprise'
            else:
                emotion = part
            if emotion not in AVAILABLE_EMOTIONS:
                continue
            # extract speech features
            features = extract_feature(fi + "\\" + file, mfcc=True, chroma=True, mel=True)
            # add to data
            X.append(features)
            y.append(emotion)
    # ----------------------------------------emovo---------------------------------------------------------------------------
    # for file in glob.glob("data\\emovo\\*.wav"):
    #     # get the base name of the audio file
    #     basename = os.path.basename(file)
    #     # get the emotion label
    #     label = (basename[:3])
    #     if label == "rab":
    #         emotion = 'angry'
    #     elif label == "dis":
    #         emotion = 'disgust'
    #     elif label == "pau":
    #         emotion = 'fearful'
    #     elif label == "gio":
    #         emotion = 'happy'
    #     elif label == "tri":
    #         emotion = 'sad'
    #     elif label == "neu":
    #         emotion = 'neutral'
    #     elif label == "sor":
    #         emotion = 'surprise'
    #     else:
    #         continue
    #     if emotion not in AVAILABLE_EMOTIONS:
    #         continue
    #     # extract speech features
    #     features = extract_feature(file, mfcc=False, chroma=True, mel=True)
    #     # add to data
    #     X.append(features)
    #     y.append(emotion)

    # split the data to training and testing and return it
    return train_test_split(np.array(X), y, test_size=test_size, random_state=7)

