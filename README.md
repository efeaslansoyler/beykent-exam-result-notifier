# Beykent Sınav Sonuç Bildirici

[![English](https://img.shields.io/badge/English-EN-blue)](README.en.md)
[![Türkçe](https://img.shields.io/badge/Türkçe-TR-red)](README.md)

Bu Python scripti, Beykent Üniversitesi öğrencilerinin sınav sonuçlarını otomatik olarak kontrol eder ve sonuçlar açıklandığında ntfy.sh üzerinden bildirim gönderir.

## Özellikler

- Otomatik sınav sonucu kontrolü
- ntfy.sh üzerinden anlık bildirimler
- Özelleştirilebilir kontrol aralığı
- Güvenli kimlik bilgisi yönetimi
- %100 yerel çalışma - verileriniz cihazınızda kalır

## Kurulum

1. Python sanal ortamı oluşturun ve aktifleştirin:

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

2. Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

3. Ortam değişkenlerini yapılandırın:

```bash
# Windows
copy .env.example .env

# Linux/MacOS
cp .env.example .env
```

4. `.env` dosyasını düzenleyin ve aşağıdaki bilgileri girin:
   - `USERNAME`: Öğrenci numaranız
   - `PASSWORD`: Öğrenci portalı şifreniz
   - `HEADLESS`: Tarayıcı görünürlüğü (varsayılan: false)
   - `NTFY_TOPIC`: ntfy.sh bildirim konusu

> **Not**: `.env.example` dosyasını `.env` olarak yeniden adlandırdıktan sonra düzenlemeyi unutmayın.

## Kullanım

> **Öneri**: Otomatik çalıştırma için uzak sunucu (VPS/VDS) kullanmanız önerilir.

### Windows'ta Otomatik Çalıştırma

1. Görev Zamanlayıcıyı açın (Task Scheduler)
2. "Create Basic Task" seçeneğini tıklayın
3. Görev adı ve açıklaması girin
4. Tetikleyici olarak "Daily" seçin
5. Başlangıç zamanını ayarlayın
6. Eylem olarak "Start a program" seçin
7. Program/script kısmına aşağıdaki komutu girin:
   ```
   C:\Path\To\Your\venv\Scripts\python.exe C:\Path\To\Your\main.py
   ```
8. "Finish" düğmesine tıklayın

### Linux'ta Otomatik Çalıştırma

1. crontab'ı düzenleyin:
   ```bash
   crontab -e
   ```

2. Aşağıdaki satırı ekleyin (her saat başı çalışacak şekilde):
   ```
   0 * * * * cd /path/to/your/project && source /path/to/your/project/venv/bin/activate && python main.py
   ```

> **Not**: Yukarıdaki komutta `/path/to/your/project` kısmını kendi proje dizininizin tam yolu ile değiştirmeyi unutmayın.

> **Özel Çalıştırma Aralığı**: Scripti farklı aralıklarla çalıştırmak için crontab satırındaki `0 * * * *` kısmını değiştirebilirsiniz. Örnekler:
> - Her 2 saatte bir: `0 */2 * * *`
> - Her 3 saatte bir: `0 */3 * * *`
> - Her 30 dakikada bir: `*/30 * * * *`
> - Her 15 dakikada bir: `*/15 * * * *`

## Manuel Çalıştırma

Scripti çalıştırmadan önce sanal ortamı aktifleştirmeyi unutmayın:

```bash
# Windows
.\venv\Scripts\activate

# Linux/MacOS
source venv/bin/activate

# Scripti çalıştır
python main.py
```

> **Not**: Script her çalıştırılmadan önce sanal ortamın aktif olması gerekmektedir. Sanal ortam aktif değilse, yukarıdaki komutlardan uygun olanı kullanarak aktifleştirin.

## Gereksinimler

- Python 3.8 veya üzeri
- İnternet bağlantısı
- ntfy.sh bildirim konusu (hesap oluşturmaya gerek yok)

## Güvenlik ve Gizlilik

- Tüm işlemler %100 yerel olarak gerçekleştirilir
- Kimlik bilgileriniz sadece sizin cihazınızda `.env` dosyasında saklanır
- Hiçbir veri sunuculara gönderilmez veya üçüncü taraflarla paylaşılmaz
- Kod açık kaynaklıdır, güvenliği kendiniz kontrol edebilirsiniz
- ntfy.sh bildirimleri şifrelidir ve sadece sizin belirlediğiniz konuya gönderilir

## Hata Ayıklama

- Script çalışmazsa, sanal ortamın aktif olduğundan emin olun
- İnternet bağlantınızı kontrol edin
- `.env` dosyasındaki bilgilerin doğru olduğunu kontrol edin
- Logs klasöründeki log dosyalarını inceleyin

## Teşekkürler

- Captcha çözme modülü [AmireNoori/MathCaptchaSolver](https://github.com/AmireNoori/MathCaptchaSolver) projesinden uyarlanmıştır. Orijinal kod temel aritmetik işlemleri ve işaret tespitini desteklerken, aşağıdaki geliştirmeler yapılmıştır:
  - Loglama sistemi entegrasyonu ile hata ayıklama
  - Hata yönetimi ve doğrulama sistemi
  - Dinamik veri klasörü yönetimi
  - İşlenmiş görüntülerin özel klasörde saklanması
  - Sabit kodlanmış dosya yollarının kaldırılması
  - Optimize edilmiş görüntü kırpma pozisyonları ve boyutları
  - Geliştirilmiş sayı temizleme ve doğrulama

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.
