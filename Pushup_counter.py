import cv2  # Import library OpenCV untuk tugas penglihatan komputer
import mediapipe as mp  # Import library Mediapipe untuk estimasi pose
import numpy as np  # Import library NumPy untuk operasi numerik
import PoseModule as pm  # Import PoseModule untuk fungsi deteksi pose kustom

# Buka kamera
cap = cv2.VideoCapture(0)

# Buat objek detektor pose
detector = pm.poseDetector()

# Inisialisasi variabel untuk menghitung push-up
count = 0
direction = 0
form = 0
feedback = "Perbaiki Posisi"

# Loop utama untuk menangkap bingkai video dari kamera
while cap.isOpened():
    # Baca bingkai dari kamera
    ret, img = cap.read()  # 640 x 480
    
    # Tentukan dimensi video
    width = cap.get(3)  # lebar
    height = cap.get(4)  # tinggi

    # Temukan pose dalam bingkai
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    
    # Periksa apakah landmark terdeteksi
    if len(lmList) != 0:
        # Hitung sudut untuk evaluasi push-up
        siku = detector.findAngle(img, 11, 13, 15)
        bahu = detector.findAngle(img, 13, 11, 23)
        pinggul = detector.findAngle(img, 11, 23, 25)
        
        # Hitung persentase keberhasilan push-up
        per = np.interp(siku, (90, 160), (0, 100))
        
        # Hitung batang untuk menampilkan kemajuan push-up
        batang = np.interp(siku, (90, 160), (380, 50))

        # Periksa posisi yang benar sebelum memulai program push-up
        if siku > 160 and bahu > 40 and pinggul > 160:
            form = 1
    
        # Periksa untuk rentang gerak penuh push-up
        if form == 1:
            if per == 0:
                if siku <= 90 and pinggul > 160:
                    feedback = "Up"
                    if direction == 0:
                        count += 0.5
                        direction = 1
                else:
                    feedback = "Perbaiki Posisi"
                    
            if per == 100:
                if siku > 160 and bahu > 40 and pinggul > 160:
                    feedback = "Down"
                    if direction == 1:
                        count += 0.5
                        direction = 0
                else:
                    feedback = "Perbaiki Posisi"
    
        print(count)
        
        # Gambar progress bar
        if form == 1:
            cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
            cv2.rectangle(img, (580, int(batang)), (600, 380), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        # Gambar hitungan push-up
        cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
        
        # Gambar umpan balik
        cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    # Tampilkan bingkai dengan anotasi
    cv2.imshow('Hitungan Push-Up', img)
    
    # Keluar dari loop jika tombol 'q' ditekan
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Bebaskan kamera dan tutup semua jendela OpenCV
cap.release()

cv2.destroyAllWindows()