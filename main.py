import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random
import unicodedata

# ------------------ NUEVA FUNCIÓN ------------------
def normalize(text):
    text = text.lower().strip()
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
# --------------------------------------------------

duration = 5  # segundos de grabación
sample_rate = 44100
max_errors = 3
score = 0
errors = 0


words = {
    "easy": ["gato", "perro", "manzana", "leche", "sol"],
    "medium": ["banano", "escuela", "amigo", "ventana", "amarillo"],
    "hard": ["tecnologia", "universidad", "informacion", "pronunciacion", "imaginacion"]
}

idioms = {
    "inglés": "en",
    "ruso": "ru",
    "portugués": "pt",
    "indonesio": "in",
    "polaco": "pl",
    "italiano": "it",
    "turco": "tr"
}

idiom = input("Choose the language you want to learn today: Inglés, Ruso, Portugués, Indonesio, Polaco, Italiano, Turco. ").strip().lower()

level = input("Choose a difficulty level: Easy, Medium or Hard. ").strip().lower()

# ------------------ MEJORAS ------------------

if level not in words:
    print("Nivel inválido, se usará 'easy' por defecto")
    level = "easy"

if idiom not in idioms:
    print("Idioma inválido, se usará inglés por defecto")
    idiom = "inglés"

selected_language = idioms[idiom]

print("\n🎮 INICIANDO JUEGO...")
print(f"Idioma seleccionado: {idiom}")
print(f"Dificultad: {level}")
print("Tienes 3 vidas ❤️❤️❤️\n")

# ------------------------------------------------------

word_list = words[level]
random.shuffle(word_list)

translator = Translator()
recognizer = sr.Recognizer()

# ❗ TU LÍNEA ORIGINAL (se respeta)
# for word in word_list():

# ✅ CORRECCIÓN FUNCIONAL
for word in word_list:

    print(f"Palabra: {word}")
    print("Habla ahora...")

    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    wav.write("output.wav", sample_rate, recording)
    print("Grabación completa, ahora reconociendo...")

    try:
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language="es").lower()
            print("Dijiste:", text)

            # ❗ TU LÍNEA ORIGINAL (controlada)
            try:
                translated = translator.translate(text, dest=idioms).text.lower()
            except:
                translated = translator.translate(text, dest=selected_language).text.lower()

            # ------------------ MEJORA CLAVE ------------------

            # Traducción correcta (forzando español → idioma objetivo)
            correct_translation = translator.translate(word, src="es", dest=selected_language).text.lower()
            print(f"Traducción correcta esperada: {correct_translation}")

            # NORMALIZACIÓN
            normalized_text = normalize(text)
            normalized_correct = normalize(correct_translation)

            # CONTROL DE RESPUESTA
            is_correct = False

            # ❗ TU LÓGICA ORIGINAL (se mantiene)
            if text == translated:
                print("¡CORRECTO!")
                is_correct = True
            else:
                print("MUY MAL... INTENTA DE NUEVO")

            # ✅ NUEVA LÓGICA CORRECTA
            if normalized_correct in normalized_text:
                print("✅ ¡CORRECTO!")
                is_correct = True
            else:
                print("❌ Incorrecto")

            # ✅ SOLO SE SUMA UNA VEZ
            if is_correct:
                score += 1
            else:
                errors += 1

            # -------------------------------------------------

            if errors >= max_errors:
                print("💀 GAME OVER")
                break

    except sr.UnknownValueError:
        print("No se pudo reconocer el habla.")
        errors += 1
        print("MUY MAL... INTENTA DE NUEVO")

        if errors >= max_errors:
            print("💀 GAME OVER")
            break

    except sr.RequestError as e:
        print(f"Error del servicio: {e}")
        break

    # FEEDBACK
    print(f"❤️ Vidas restantes: {max_errors - errors}")
    print(f"⭐ Puntaje actual: {score}\n")

print(f"🏁 YOUR SCORE: {score}")
