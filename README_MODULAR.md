# CPU Scheduler - Modüler Yapı

Bu proje modüler bir yapıya sahiptir. Kodlar mantıksal olarak ayrılmış modüllere bölünmüştür.

## Proje Yapısı

```
Cpu-Scheduler3/
├── main.py                 # Ana giriş noktası
├── scheduler_fixed.py      # Scheduling algoritmaları
├── ui/                     # UI modülleri
│   ├── __init__.py
│   ├── main_window.py      # Ana pencere
│   ├── header.py           # Header component
│   ├── components/         # UI componentleri
│   │   ├── __init__.py
│   │   ├── cards.py        # ModernCard, MetricCard
│   │   └── gantt_chart.py  # GanttChart, ScrollFriendlyCanvas
│   └── tabs/               # Tab modülleri (gelecekte kullanılabilir)
│       └── __init__.py
├── themes/                 # Tema yönetimi
│   ├── __init__.py
│   └── theme_manager.py    # ThemeManager sınıfı
└── utils/                  # Yardımcı modüller
    ├── __init__.py
    └── constants.py        # Sabitler ve konfigürasyon
```

## Modül Açıklamaları

### 1. `main.py`
- Uygulamanın ana giriş noktası
- QApplication oluşturur ve pencereyi başlatır

### 2. `ui/main_window.py`
- Ana pencere sınıfı (`CPUSchedulerApp`)
- Tüm tab'ları ve işlevleri yönetir
- Process yönetimi, simülasyon çalıştırma, sonuçları gösterme

### 3. `ui/header.py`
- Header widget component
- Başlık, alt başlık, export ve dark mode butonları

### 4. `ui/components/`
- **cards.py**: ModernCard ve MetricCard componentleri
- **gantt_chart.py**: GanttChart ve ScrollFriendlyCanvas componentleri

### 5. `themes/theme_manager.py`
- Tema yönetimi (Light/Dark mode)
- Stylesheet'leri merkezi olarak yönetir
- Text renkleri ve messagebox stilleri

### 6. `utils/constants.py`
- Tüm sabitler (renkler, boyutlar, ayarlar)
- Kolay konfigürasyon için merkezi yer

## Kullanım

### Çalıştırma
```bash
python main.py
```

### Eski Yöntem (Hala Çalışır)
```bash
python pyqt_app.py
```

## Modüler Yapının Avantajları

1. **Bakım Kolaylığı**: Her modül kendi sorumluluğuna sahip
2. **Yeniden Kullanılabilirlik**: Componentler başka projelerde kullanılabilir
3. **Test Edilebilirlik**: Her modül bağımsız test edilebilir
4. **Okunabilirlik**: Kod daha organize ve anlaşılır
5. **Genişletilebilirlik**: Yeni özellikler kolayca eklenebilir

## Gelecek Geliştirmeler

- Tab içeriklerini ayrı widget sınıflarına dönüştürme
- Daha fazla component modülerleştirme
- Unit testler ekleme

