import cv2  # OpenCV kütüphanesini içe aktarıyoruz, görüntü işleme işlemleri için kullanacağız.
import numpy as np  # NumPy kütüphanesini içe aktarıyoruz, matematiksel işlemler ve dizi yönetimi için kullanacağız.

def initialize_video_capture(video_path):
    return cv2.VideoCapture(video_path)  # Video dosyasını okumak için VideoCapture nesnesi oluşturuyoruz.

def update_heatmap(heatmap, frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Mevcut kareyi gri tonlamalı (grayscale) bir görüntüye çeviriyoruz.
    heatmap += gray  # Gri tonlamalı kareyi mevcut ısı haritasına ekleyerek güncelliyoruz.

def display_heatmap(heatmap):
    heatmap_normalized = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)  # Isı haritasını 0-255 aralığında normalize ediyoruz.
    heatmap_colored = cv2.applyColorMap(heatmap_normalized.astype(np.uint8), cv2.COLORMAP_JET)  # Normalize edilmiş ısı haritasını renkli bir ısı haritasına dönüştürüyoruz.
    cv2.imshow('Heatmap', heatmap_colored)  # Renkli ısı haritasını ekranda gösteriyoruz.

def release_resources(video_capture):
    video_capture.release()  # Video dosyasıyla ilişkili kaynakları serbest bırakıyoruz.
    cv2.destroyAllWindows()  # Tüm OpenCV pencerelerini kapatıyoruz.

def run_heatmap_generation(video_path):
    video_capture = initialize_video_capture(video_path)  # Video yakalamayı başlatıyoruz.
    ret, frame = video_capture.read()  # İlk kareyi videodan okuyoruz.
    if not ret:  # Eğer video okunamazsa, hata mesajı veriyoruz ve fonksiyondan çıkıyoruz.
        print("Video okunamadı!")
        return
    
    # Isı haritasını başlatmak için gri tonlamalı bir görüntü boyutunda sıfırlanmış bir matris oluşturuyoruz.
    heatmap = np.zeros_like(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), dtype=np.float32)

    while True:
        ret, frame = video_capture.read()  # Her kareyi videodan okuyoruz.
        if not ret:  # Eğer video sonuna gelinirse, döngüden çıkıyoruz.
            break
        
        update_heatmap(heatmap, frame)  # Isı haritasını mevcut kareyle güncelliyoruz.
        display_heatmap(heatmap)  # Güncellenen ısı haritasını ekranda gösteriyoruz.
        
        key = cv2.waitKey(30) & 0xFF  # Klavye girişini 30 ms bekliyoruz.
        if key == ord('q') or cv2.getWindowProperty('Heatmap', cv2.WND_PROP_VISIBLE) < 1:  # 'q' tuşuna basılırsa veya pencere kapatılırsa döngüyü sonlandırıyoruz.
            break

    release_resources(video_capture)  # Kaynakları serbest bırakıp pencereleri kapatıyoruz.
