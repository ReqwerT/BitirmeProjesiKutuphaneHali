import os
from bitirmeproj1.video_similarity_search import find_similarity_in_video

def main():
    # Video dosyasının yolu
    video_path = "video1.mp4"  # Test etmek için mevcut bir video dosyasını belirtin

    # Şablonların bulunduğu klasörün yolu
    current_directory = os.getcwd()
    template_dir = os.path.join(current_directory, "benzerlik")

    # Eğer şablon klasörü yoksa hata ver
    if not os.path.exists(template_dir):
        print(f"Şablon klasörü bulunamadı: {template_dir}")
        return

    # Şablon dosyalarının yollarını al
    template_paths = [os.path.join(template_dir, f) for f in os.listdir(template_dir) if os.path.isfile(os.path.join(template_dir, f))]

    # Sonuçları kaydetmek için kullanılacak klasörün yolu
    output_dir = os.path.join(current_directory, "similarity_results")

    # Eğer sonuç klasörü yoksa oluştur
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Benzerlik araması başlat
    find_similarity_in_video(video_path, template_paths, output_dir)

if __name__ == "__main__":
    main()
