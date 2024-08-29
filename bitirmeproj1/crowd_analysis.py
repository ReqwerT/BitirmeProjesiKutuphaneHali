import cv2  # OpenCV kütüphanesini içe aktarıyoruz, görüntü işleme işlemleri için kullanacağız.
import numpy as np  # NumPy kütüphanesini içe aktarıyoruz, matematiksel işlemler ve dizi yönetimi için kullanacağız.

def initialize_video_capture(video_path):
    return cv2.VideoCapture(video_path)  # Video dosyasını okumak için VideoCapture nesnesi oluşturuyoruz.

def crowd_analysis(video_path):
    video_capture = initialize_video_capture(video_path)  # Video yakalamayı başlatıyoruz.
    
    ret, first_frame = video_capture.read()  # İlk kareyi videodan okuyoruz.
    if not ret:  # Eğer video okunamazsa, hata mesajı veriyoruz ve fonksiyondan çıkıyoruz.
        print("Video okunamadı!")
        return
    
    prev_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)  # İlk kareyi gri tonlamalı (grayscale) bir görüntüye çeviriyoruz.
    mask = np.zeros_like(first_frame)  # İlk kare ile aynı boyutta sıfırlanmış bir maske oluşturuyoruz.
    mask[..., 1] = 255  # Maskenin doygunluk kanalını (HSV formatında) maksimum yapıyoruz, böylece renkler belirgin olacak.

    while True:
        ret, frame = video_capture.read()  # Her kareyi videodan okuyoruz.
        if not ret:  # Eğer video sonuna gelinirse, döngüden çıkıyoruz.
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Mevcut kareyi gri tonlamalı bir görüntüye çeviriyoruz.
        # Optical Flow Farneback algoritmasını kullanarak optik akışı hesaplıyoruz.
        flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])  # Akışın büyüklük ve açı bileşenlerini hesaplıyoruz.
        mask[..., 0] = angle * 180 / np.pi / 2  # Açıyı maskenin hue kanalına atıyoruz (HSV formatında).
        mask[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)  # Büyüklüğü normalize edip maske üzerine atıyoruz.
        rgb = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)  # Maskeyi BGR formatına çeviriyoruz.
        dense_flow = cv2.addWeighted(frame, 1, rgb, 2, 0)  # RGB akışı orijinal kare ile birleştirerek yoğun bir optik akış görüntüsü elde ediyoruz.

        mean_movement = np.mean(magnitude)  # Optik akış büyüklüğünün ortalamasını hesaplayarak genel hareket yoğunluğunu ölçüyoruz.
        # Kalabalık yoğunluğunu görüntü üzerine yazıyoruz.
        cv2.putText(dense_flow, f"Kalabalik Yogunlugu: {mean_movement:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Kalabalik Analizi', dense_flow)  # Optik akış analizi sonucunu görüntülüyoruz.
        prev_gray = gray  # Bir sonraki kare için mevcut kareyi önceki kare olarak kaydediyoruz.

        key = cv2.waitKey(30) & 0xFF  # Klavye girişini 30 ms bekliyoruz.
        if key == ord('q') or cv2.getWindowProperty('Kalabalik Analizi', cv2.WND_PROP_VISIBLE) < 1:  # 'q' tuşuna basılırsa veya pencere kapatılırsa döngüyü sonlandırıyoruz.
            break

    video_capture.release()  # Video dosyasıyla ilişkili kaynakları serbest bırakıyoruz.
    cv2.destroyAllWindows()  # Tüm OpenCV pencerelerini kapatıyoruz.
