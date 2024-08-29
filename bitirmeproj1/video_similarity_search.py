import cv2  # OpenCV kütüphanesini içe aktarıyoruz, görüntü işleme işlemleri için kullanacağız.
import numpy as np  # NumPy kütüphanesini içe aktarıyoruz, matematiksel işlemler ve dizi yönetimi için kullanacağız.
import os  # Dosya ve dizin işlemleri için os kütüphanesini içe aktarıyoruz.
import traceback  # Hata yönetimi ve hata izleme için traceback modülünü içe aktarıyoruz.

def initialize_video_capture(video_path):
    return cv2.VideoCapture(video_path)  # Video dosyasını okumak için VideoCapture nesnesi oluşturuyoruz.

def find_similarity_in_video(video_path, template_paths, output_dir):
    video_capture = initialize_video_capture(video_path)  # Video yakalamayı başlatıyoruz.
    templates = [cv2.imread(template_path) for template_path in template_paths]  # Her bir şablon dosyasını okuyoruz.

    for template_path, template in zip(template_paths, templates):
        if template is None:  # Eğer bir şablon dosyası açılamazsa, hata mesajı veriyoruz ve fonksiyondan çıkıyoruz.
            print(f"Şablon dosyası açılamadı: {template_path}")
            return

    if not os.path.exists(output_dir):  # Çıkış dizini yoksa oluşturuyoruz.
        os.makedirs(output_dir)

    similarity_found = [False] * len(templates)  # Her bir şablon için benzerlik bulunup bulunmadığını takip etmek için bir liste oluşturuyoruz.
    frame_counter = 0  # İşlenen kare sayacını başlatıyoruz.

    while True:
        ret, frame = video_capture.read()  # Her kareyi videodan okuyoruz.
        if not ret:  # Eğer video sonuna gelinirse, döngüden çıkıyoruz.
            break

        frame_counter += 1  # Kare sayacını artırıyoruz.

        for idx, template in enumerate(templates):  # Her bir şablon için benzerlik araması yapıyoruz.
            template_height, template_width = template.shape[:2]  # Şablonun boyutlarını alıyoruz.
            result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)  # Karede şablonun yerini bulmak için şablon eşleme tekniğini kullanıyoruz.
            _, max_val, _, max_loc = cv2.minMaxLoc(result)  # Maksimum benzerlik değerini ve konumunu alıyoruz.

            if max_val > 0.6:  # Eğer benzerlik değeri 0.6'nın üzerindeyse, bir eşleşme bulunduğunu kabul ediyoruz.
                top_left = max_loc  # Eşleşmenin sol üst köşesini alıyoruz.
                bottom_right = (top_left[0] + template_width, top_left[1] + template_height)  # Eşleşmenin sağ alt köşesini hesaplıyoruz.
                cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)  # Kare üzerinde eşleşmenin yerini göstermek için bir dikdörtgen çiziyoruz.
                cv2.putText(frame, f"Benzerlik {idx+1}: {max_val:.2f}", (10, 30 + 40 * idx), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)  # Ekrana benzerlik skorunu yazdırıyoruz.
                print(f"Şablon {idx+1} için benzerlik bulundu! Skor: {max_val:.2f}")
                
                if not similarity_found[idx]:  # Eğer bu şablon için daha önce benzerlik bulunmadıysa, durumu güncelliyoruz.
                    similarity_found[idx] = True

                save_path = os.path.join(output_dir, f"match_{idx+1}_frame_{frame_counter}.png")  # Kaydedilecek dosya yolunu oluşturuyoruz.
                
                try:
                    if cv2.imwrite(save_path, frame):  # Kareyi dosyaya kaydediyoruz.
                        print(f"Kare kaydedildi: {save_path}")
                    else:
                        print(f"Kare kaydedilemedi: {save_path}. Dosya yazma işlemi başarısız.")
                except Exception as e:  # Eğer dosya kaydedilemezse, hatayı yakalayıp bildiriyoruz.
                    print(f"Kare kaydedilemedi: {save_path}. Hata: {str(e)}")
                    traceback.print_exc()  # Hatanın izini ayrıntılı olarak çıktılıyoruz.
        
        cv2.imshow('Benzerlik Araması', frame)  # Mevcut kareyi ekranda gösteriyoruz.

        key = cv2.waitKey(1) & 0xFF  # Klavye girişini 1 ms bekliyoruz.
        if key == ord('q') or cv2.getWindowProperty('Benzerlik Araması', cv2.WND_PROP_VISIBLE) < 1:  # 'q' tuşuna basılırsa veya pencere kapatılırsa döngüyü sonlandırıyoruz.
            break

    video_capture.release()  # Video dosyasıyla ilişkili kaynakları serbest bırakıyoruz.
    cv2.destroyAllWindows()  # Tüm OpenCV pencerelerini kapatıyoruz.
