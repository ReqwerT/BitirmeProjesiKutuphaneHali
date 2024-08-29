import os
import bitirmeproj1


def main():
    # Video dosyasının yolu
    video_path = "video1.mp4"  

    # Kayıt edilecek klasörün yolu
    current_directory = os.getcwd()
    output_dir = os.path.join(current_directory, "keyframe")

    # Eğer klasör yoksa oluştur
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Anahtar kareleri tespit et ve kaydet
    bitirmeproj1.detect_key_frames(video_path, output_dir)

if __name__ == "__main__":
    main()
