# 🎯 Real-Time Object Detection System

Professional object detection system menggunakan **YOLOv8** dan **OpenCV** untuk mendeteksi objek secara real-time dari kamera.

## ✨ Fitur Utama

- ✅ **Real-time Object Detection** - Deteksi objek secara langsung dari kamera
- ✅ **YOLOv8 Integration** - Menggunakan model YOLO terbaru dan tercepat
- ✅ **Multi-Camera Support** - Mendukung multiple kamera
- ✅ **FPS Counter** - Menampilkan frame rate real-time
- ✅ **Confidence Threshold** - Konfigurasi tingkat kepercayaan deteksi
- ✅ **Video Recording** - Merekam hasil deteksi ke file video
- ✅ **Frame Capture** - Menyimpan screenshot hasil deteksi
- ✅ **GPU Acceleration** - Dukungan CUDA untuk performa maksimal
- ✅ **Professional Code** - Clean code dengan error handling lengkap

## 📋 Requirements

- Python 3.8 atau lebih tinggi
- Webcam atau kamera eksternal
- (Opsional) NVIDIA GPU dengan CUDA untuk akselerasi

## 🚀 Instalasi

### 1. Clone atau Download Project

```bash
cd C:\Users\Lenovo\tes
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Catatan:** Model YOLOv8 akan otomatis terdownload saat pertama kali dijalankan (~6MB untuk yolov8n).

### 3. (Opsional) Install PyTorch dengan CUDA

Untuk performa maksimal dengan GPU:

```bash
# CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# CUDA 12.1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

## 💻 Cara Penggunaan

### Menjalankan Program

```bash
python main.py
```

### Menggunakan Kamera Spesifik

```bash
python main.py --camera 1
```

### Melihat Daftar Kamera yang Tersedia

```bash
python main.py --list-cameras
```

## ⌨️ Keyboard Controls

Saat program berjalan, gunakan tombol berikut:

| Tombol | Fungsi |
|--------|--------|
| `Q` atau `ESC` | Keluar dari program |
| `S` | Simpan frame saat ini |
| `R` | Toggle recording video |
| `I` | Tampilkan info deteksi di console |

## ⚙️ Konfigurasi

Edit file `config.py` untuk mengubah pengaturan:

```python
# Model Configuration
MODEL_NAME = "yolov8n.pt"  # yolov8n, yolov8s, yolov8m, yolov8l, yolov8x

# Detection Parameters
CONFIDENCE_THRESHOLD = 0.5  # 0.0 - 1.0

# Camera Configuration
CAMERA_ID = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# Display
SHOW_FPS = True
SHOW_CONFIDENCE = True
```

### Model Options

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| yolov8n | ~6MB | Fastest | Good |
| yolov8s | ~22MB | Fast | Better |
| yolov8m | ~52MB | Medium | Great |
| yolov8l | ~87MB | Slow | Excellent |
| yolov8x | ~136MB | Slowest | Best |

## 📁 Struktur Project

```
tes/
├── main.py              # Main application
├── detector.py          # Object detection module
├── camera_handler.py    # Camera interface
├── config.py            # Configuration
├── requirements.txt     # Dependencies
├── README.md           # Documentation
├── models/             # YOLO models (auto-created)
└── outputs/            # Saved frames & videos (auto-created)
```

## 🎯 Objek yang Dapat Dideteksi

YOLOv8 dapat mendeteksi **80 jenis objek** dari COCO dataset, termasuk:

- 👤 **Manusia** (person)
- 🚗 **Kendaraan** (car, motorcycle, bus, truck, bicycle)
- 🐕 **Hewan** (dog, cat, bird, horse, dll)
- 📱 **Elektronik** (cell phone, laptop, tv, keyboard, mouse)
- 🪑 **Furniture** (chair, couch, bed, table)
- 🍎 **Makanan** (apple, banana, pizza, cake, dll)
- Dan 60+ objek lainnya

## 🔧 Troubleshooting

### Kamera Tidak Terdeteksi

```bash
# Cek kamera yang tersedia
python main.py --list-cameras

# Coba kamera lain
python main.py --camera 1
```

### Error: Module Not Found

```bash
# Install ulang dependencies
pip install -r requirements.txt --upgrade
```

### Performa Lambat

1. Gunakan model lebih kecil: `yolov8n.pt`
2. Kurangi resolusi kamera di `config.py`
3. Install PyTorch dengan CUDA support

### Model Tidak Terdownload

Download manual dari [Ultralytics](https://github.com/ultralytics/assets/releases):
- Simpan di folder `models/`
- Rename sesuai `MODEL_NAME` di config

## 📊 Performance Tips

1. **GPU Acceleration**: Install PyTorch dengan CUDA
2. **Model Selection**: Gunakan yolov8n untuk real-time, yolov8m untuk akurasi
3. **Resolution**: 640x480 optimal untuk real-time
4. **Confidence Threshold**: 0.5 - 0.7 untuk hasil terbaik

## 🛠️ Advanced Usage

### Custom Confidence Threshold

```python
# Edit config.py
CONFIDENCE_THRESHOLD = 0.7  # Lebih strict
```

### Change Detection Colors

```python
# Edit config.py
BOX_COLOR = (0, 0, 255)  # Red boxes
TEXT_COLOR = (255, 255, 0)  # Cyan text
```

### Enable Auto-Recording

```python
# Edit config.py
ENABLE_RECORDING = True
```

## 📝 License

Project ini dibuat untuk tujuan edukasi dan profesional.

## 👨‍💻 Developer Notes

- Code mengikuti best practices Python
- Comprehensive error handling
- Modular architecture untuk maintainability
- Type hints untuk better IDE support
- Detailed documentation

## 🆘 Support

Jika mengalami masalah:
1. Pastikan semua dependencies terinstall
2. Cek versi Python (3.8+)
3. Pastikan kamera tidak digunakan aplikasi lain
4. Cek permission kamera di Windows

---

**Dibuat dengan ❤️ menggunakan YOLOv8 & OpenCV**
