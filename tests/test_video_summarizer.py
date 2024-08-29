import os
from bitirmeproj1.video_summarizer import summarize_video

def main():
    # Video dosyasının yolu
    video_path = "video1.mp4"  # Test etmek için mevcut bir video dosyasını belirtin

    # Kayıt edilecek klasörün yolu
    current_directory = os.getcwd()
    output_dir = os.path.join(current_directory, "video_ozeti")

    # Eğer klasör yoksa oluştur
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Çıktı dosyasının yolu
    output_video_path = os.path.join(output_dir, "summary_video.mp4")

    # Video özetleme işlemini başlat
    summarize_video(video_path, output_video_path)

if __name__ == "__main__":
    main()
