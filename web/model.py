import tensorflow as tf
import numpy as np
import cv2
import random
import tempfile

class CFG:
    n_frames = 10
    output_size = (224, 224)
    frame_step = 15
    classes = ["Orginal", "Watermark"]  


def format_frames(frame, output_size):
    frame = tf.image.convert_image_dtype(frame, tf.float32)
    frame = tf.image.resize_with_pad(frame, *output_size)
    return frame


def frames_from_video_file(video_path, n_frames=10, output_size=(224,224), frame_step=15):
    result = []
    src = cv2.VideoCapture(video_path)
    video_length = src.get(cv2.CAP_PROP_FRAME_COUNT)

    need_length = 1 + (n_frames - 1) * frame_step
    start = 0 if need_length > video_length else random.randint(0, int(video_length - need_length) + 1)

    src.set(cv2.CAP_PROP_POS_FRAMES, start)
    ret, frame = src.read()
    result.append(format_frames(frame, output_size))

    for _ in range(n_frames - 1):
        for _ in range(frame_step):
            ret, frame = src.read()
        if ret:
            frame = format_frames(frame, output_size)
            result.append(frame)
        else:
            result.append(np.zeros_like(result[0]))

    src.release()
    result = np.array(result)[..., [2, 1, 0]]  
    return result


def build_model(input_shape=(10, 224, 224, 3)):
    model = tf.keras.Sequential([
        tf.keras.Input(shape=input_shape),
        tf.keras.layers.Conv3D(32, kernel_size=3, padding="same", activation="relu"),
        tf.keras.layers.MaxPooling3D(),
        tf.keras.layers.Conv3D(64, kernel_size=3, padding="same", activation="relu"),
        tf.keras.layers.MaxPooling3D(),
        tf.keras.layers.Conv3D(128, kernel_size=3, padding="same", activation="relu"),
        tf.keras.layers.MaxPooling3D(),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.GlobalAveragePooling3D(),
        tf.keras.layers.Dense(1, activation="sigmoid")  
    ])
    return model



def predict_video_class(uploaded_file, model):
    # Save uploaded file to a temp file so OpenCV can read it
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    
    frames = frames_from_video_file(tmp_path, n_frames=CFG.n_frames,
                                    output_size=CFG.output_size,
                                    frame_step=CFG.frame_step)
    frames = np.expand_dims(frames, axis=0)
    pred_prob = model.predict(frames)[0][0]
    pred_class = CFG.classes[int(pred_prob >= 0.9)]
    return pred_class, pred_prob



