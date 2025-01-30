import cv2
import pytesseract
from datetime import timedelta

# Path ke video
video_path = "video.mp4"
cap = cv2.VideoCapture(video_path)

# Konfigurasi OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Sesuaikan jika di Linux/Mac

# Ambil FPS video
fps = cap.get(cv2.CAP_PROP_FPS)
frame_interval = int(fps * 2)  # Ambil setiap 2 detik

transcripts = []
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Hanya proses setiap frame_interval
    if frame_count % frame_interval == 0:
        timestamp = str(timedelta(seconds=int(frame_count / fps)))
        
        # Konversi frame ke grayscale untuk OCR
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray, lang='jpn')  # Gunakan bahasa Jepang
        
        if text.strip():
            transcripts.append(f"{timestamp}: {text.strip()}")
    
    frame_count += 1

cap.release()

# Simpan hasil ke file
with open("transcript.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(transcripts))

print("Transkripsi selesai! Lihat transcript.txt")
