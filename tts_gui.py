import tkinter as tk
from tkinter import filedialog, messagebox
from gtts import gTTS
from pydub import AudioSegment
from pathlib import Path

def convert_text_to_speech():
    text = text_entry.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Advertencia", "El campo de texto está vacío.")
        return
    
    try:
        # Convertir texto a voz
        tts = gTTS(text, lang='es', slow=False)
        speech_file_path = Path("speech.mp3")
        tts.save(speech_file_path)

        # Ajustar la velocidad del audio
        speed_factor = speed_scale.get()
        audio = AudioSegment.from_file(speech_file_path)
        faster_audio = audio._spawn(audio.raw_data, overrides={
            "frame_rate": int(audio.frame_rate * speed_factor)
        }).set_frame_rate(audio.frame_rate)

        # Guardar el archivo de audio ajustado
        faster_speech_file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        if faster_speech_file_path:
            faster_audio.export(faster_speech_file_path, format="mp3")
            messagebox.showinfo("Éxito", f"Archivo de audio guardado en: {faster_speech_file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al convertir el texto a voz: {e}")

# Crear la ventana principal
root = tk.Tk()
root.title("Convertidor de Texto a Voz")

# Crear el campo de entrada de texto
text_label = tk.Label(root, text="Ingrese el texto:")
text_label.pack(pady=5)

text_entry = tk.Text(root, wrap=tk.WORD, width=50, height=10)
text_entry.pack(pady=5)

# Crear la escala para ajustar la velocidad
speed_label = tk.Label(root, text="Ajustar velocidad:")
speed_label.pack(pady=5)

speed_scale = tk.Scale(root, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL)
speed_scale.set(1.0)
speed_scale.pack(pady=5)

# Crear el botón para convertir el texto a voz
convert_button = tk.Button(root, text="Convertir", command=convert_text_to_speech)
convert_button.pack(pady=20)

# Iniciar el bucle principal de la aplicación
root.mainloop()

