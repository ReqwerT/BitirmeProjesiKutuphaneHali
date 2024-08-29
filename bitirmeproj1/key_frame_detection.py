import cv2  # OpenCV kütüphanesini içe aktarıyoruz, görüntü işleme işlemleri için kullanacağız.
import numpy as np  # NumPy kütüphanesini içe aktarıyoruz, matematiksel işlemler ve dizi yönetimi için kullanacağız.
import os  # Dosya ve dizin işlemleri için os kütüphanesini içe aktarıyoruz.

def initialize_video_capture(video_path):
    return cv2.VideoCapture(video_path)  # Video dosyasını okumak için VideoCapture nesnesi oluşturuyoruz.

def detect_key_frames(video_path, output_dir, threshold=13):
    video_capture = initialize_video_capture(video_path)  # Video yakalamayı başlatıyoruz.
    
    ret, prev_frame = video_capture.read()  # İlk kareyi videodan okuyoruz.
    if not ret:  # Eğer video okunamazsa, hata mesajı veriyoruz ve fonksiyondan çıkıyoruz.
        print("Video okunamadı!")
        return
    
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)  # İlk kareyi gri tonlamalı (grayscale) bir görüntüye çeviriyoruz.
    frame_counter = 0  # İşlenen kare sayacını başlatıyoruz.
    key_frame_counter = 0  # Tespit edilen anahtar kare sayacını başlatıyoruz.

    key_frames = []  # Anahtar kareleri saklamak için bir liste oluşturuyoruz.

    if not os.path.exists(output_dir):  # Çıkış dizini yoksa oluşturuyoruz.
        os.makedirs(output_dir)

    while True:
        ret, frame = video_capture.read()  # Her kareyi videodan okuyoruz.
        if not ret:  # Eğer video sonuna gelinirse, döngüden çıkıyoruz.
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Mevcut kareyi gri tonlamalı bir görüntüye çeviriyoruz.
        frame_diff = cv2.absdiff(prev_gray, gray)  # Önceki kare ile mevcut kare arasındaki farkı hesaplıyoruz.
        diff_score = np.sum(frame_diff) / (gray.shape[0] * gray.shape[1])  # Fark skorunu hesaplıyoruz.

        if diff_score > threshold:  # Fark skoru eşik değerini aşıyorsa, anahtar kare olarak kaydediyoruz.
            key_frame_counter += 1
            key_frame_name = f"key_frame_{key_frame_counter}.jpg"  # Anahtar kare ismini oluşturuyoruz.
            save_path = os.path.join(output_dir, key_frame_name)  # Kaydedilecek dosya yolunu oluşturuyoruz.
            cv2.imwrite(save_path, frame)  # Anahtar kareyi dosyaya kaydediyoruz.
            key_frames.append((frame_counter, save_path))  # Anahtar kareyi listeye ekliyoruz.
            print(f"Anahtar kare tespit edildi: {save_path}, Fark Skoru: {diff_score:.2f}")
        
        prev_gray = gray  # Mevcut kareyi bir sonraki döngü için önceki kare olarak saklıyoruz.
        frame_counter += 1  # İşlenen kare sayısını artırıyoruz.

        cv2.imshow('Video', frame)  # Mevcut kareyi gösteriyoruz.
        key = cv2.waitKey(30) & 0xFF  # Klavye girişini 30 ms bekliyoruz.
        if key == ord('q') or cv2.getWindowProperty('Video', cv2.WND_PROP_VISIBLE) < 1:  # 'q' tuşuna basılırsa veya pencere kapatılırsa döngüyü sonlandırıyoruz.
            break

    video_capture.release()  # Video dosyasıyla ilişkili kaynakları serbest bırakıyoruz.
    cv2.destroyAllWindows()  # Tüm OpenCV pencerelerini kapatıyoruz.

    print(f"Toplam {key_frame_counter} anahtar kare tespit edildi.")  # Toplam tespit edilen anahtar kare sayısını yazdırıyoruz.
    return key_frames  # Anahtar karelerin listesini döndürüyoruz.
