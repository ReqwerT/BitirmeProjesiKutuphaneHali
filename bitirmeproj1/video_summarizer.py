import cv2  # OpenCV kütüphanesini içe aktarıyoruz, görüntü işleme işlemleri için kullanacağız.
import numpy as np  # NumPy kütüphanesini içe aktarıyoruz, matematiksel işlemler ve dizi yönetimi için kullanacağız.
from moviepy.editor import VideoFileClip  # Video dosyalarını düzenlemek ve işlemek için MoviePy kütüphanesini kullanıyoruz.

def initialize_video_capture(video_path):
    return cv2.VideoCapture(video_path)  # Video dosyasını okumak için VideoCapture nesnesi oluşturuyoruz.

def summarize_video(video_path, output_path):
    video_capture = initialize_video_capture(video_path)  # Video yakalamayı başlatıyoruz.
    fps = video_capture.get(cv2.CAP_PROP_FPS)  # Videonun FPS (saniyedeki kare sayısı) değerini alıyoruz.
    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))  # Videonun genişliğini alıyoruz.
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Videonun yüksekliğini alıyoruz.
    frame_size = (width, height)  # Kare boyutunu belirliyoruz (genişlik x yükseklik).
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Video dosyasını MP4 formatında kaydetmek için dört karakterlik kod belirliyoruz.
    out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)  # Video yazıcıyı oluşturuyoruz.

    back_sub = cv2.createBackgroundSubtractorMOG2(history=700, varThreshold=10, detectShadows=True)  # Arka plan çıkarma için MOG2 algoritmasını kullanıyoruz.

    frame_count = 0  # İşlenen kare sayacını başlatıyoruz.
    sampling_rate = 2  # Karelerin örnekleme oranını belirliyoruz (her iki karede bir işlem yapacağız).

    while True:
        ret, frame = video_capture.read()  # Her kareyi videodan okuyoruz.
        if not ret:  # Eğer video sonuna gelinirse, döngüden çıkıyoruz.
            break

        frame_count += 1  # Kare sayacını artırıyoruz.
        if frame_count % sampling_rate != 0:  # Eğer kare sayısı örnekleme oranına uymuyorsa, bu kareyi atlıyoruz.
            continue

        fg_mask = back_sub.apply(frame)  # Arka plan çıkarma işlemi uygulayarak hareketli nesneleri tespit ediyoruz.
        _, thresh = cv2.threshold(fg_mask, 15, 255, cv2.THRESH_BINARY)  # İkili eşikleme işlemi uygulayarak maske oluşturuyoruz.
        movement_ratio = np.sum(thresh) / (width * height)  # Hareket oranını hesaplıyoruz (beyaz piksel sayısı/ toplam piksel sayısı).

        if movement_ratio > 0.002:  # Eğer hareket oranı belirli bir eşik değerini aşıyorsa, bu kareyi kaydediyoruz.
            out.write(frame)

        key = cv2.waitKey(1) & 0xFF  # Klavye girişini 1 ms bekliyoruz.
        if key == ord('q') or cv2.getWindowProperty('Video Özeti', cv2.WND_PROP_VISIBLE) < 1:  # 'q' tuşuna basılırsa veya pencere kapatılırsa döngüyü sonlandırıyoruz.
            break

    video_capture.release()  # Video dosyasıyla ilişkili kaynakları serbest bırakıyoruz.
    out.release()  # Video yazıcıyı serbest bırakıyoruz.
    cv2.destroyAllWindows()  # Tüm OpenCV pencerelerini kapatıyoruz.
