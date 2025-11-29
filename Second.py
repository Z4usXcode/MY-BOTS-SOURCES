

from datetime import datetime
import sys

# Bitiş tarihini buradan değiştir
BITIS_TARIHI = datetime(2025, 12, 4, 23, 59, 0)

# Modül import edildiğinde otomatik kontrol
if datetime.now() >= BITIS_TARIHI:
    print("⏳ API durduruldu! Satın alım için @Z4usXcode")
    sys.exit(0)
