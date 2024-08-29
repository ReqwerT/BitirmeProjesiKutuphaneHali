import cv2  # OpenCV kütüphanesini içe aktarıyoruz, görüntü işleme işlemlerini gerçekleştirmek için kullanacağız.

def initialize_video_capture(video_path):
    return cv2.VideoCapture(video_path)  # Video dosyasını okumak için VideoCapture nesnesi oluşturuyoruz.

def create_background_subtractor():
    return cv2.createBackgroundSubtractorMOG2()  # MOG2 algoritmasını kullanarak arka plan çıkarıcı oluşturuyoruz.

def process_frame(video_capture, back_sub):
    ret, frame = video_capture.read()  # Videodan bir kare okuyoruz.
    if not ret:  # Kare okunamazsa, None döndürerek döngüyü sonlandırıyoruz.
        return None, None
    fg_mask = back_sub.apply(frame)  # Arka plan çıkarıcıyı kullanarak hareketli nesneleri tespit ediyoruz.
    return frame, fg_mask  # Orijinal kare ve ön plan maskesini döndürüyoruz.

def display_frame(window_name, frame):
    cv2.imshow(window_name, frame)  # Belirtilen pencerede görüntüyü gösteriyoruz.

def release_resources(video_capture):
    video_capture.release()  # Video dosyasıyla ilişkili kaynakları serbest bırakıyoruz.
    cv2.destroyAllWindows()  # Tüm OpenCV pencerelerini kapatıyoruz.

def run_video_segmentation(video_path):
    video_capture = initialize_video_capture(video_path)  # Video yakalamayı başlatıyoruz.
    back_sub = create_background_subtractor()  # Arka plan çıkarıcıyı oluşturuyoruz.

    while True:
        frame, fg_mask = process_frame(video_capture, back_sub)  # Her kare için segmentasyon işlemi yapıyoruz.
        if frame is None:  # Video sonuna geldiğimizde döngüyü sonlandırıyoruz.
            break
        display_frame('Segmented Frame', fg_mask)  # Segmentasyon sonucunu ekranda gösteriyoruz.
        
        key = cv2.waitKey(30) & 0xFF  # Klavye girişini 30 ms bekliyoruz.
        if key == ord('q') or cv2.getWindowProperty('Segmented Frame', cv2.WND_PROP_VISIBLE) < 1:  # 'q' tuşuna basılırsa veya pencere kapatılırsa döngüyü sonlandırıyoruz.
            break

    release_resources(video_capture)  # Kaynakları serbest bırakıp pencereleri kapatıyoruz.




