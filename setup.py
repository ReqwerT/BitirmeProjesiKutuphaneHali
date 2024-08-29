from setuptools import setup, find_packages

setup(
    name="bitirmeproj1",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "moviepy",
    ],
    author="Adınız",
    author_email="email@example.com",
    description="Video işleme araçları kütüphanesi",
    keywords="video processing analysis segmentation",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
