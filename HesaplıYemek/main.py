import logging
from GUI import run_gui

# Loglama yapılandırması: main.log dosyasına INFO seviyesinde loglama yap
logging.basicConfig(
    filename='main.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("GUI baslatiliyor.")
run_gui()
logging.info("GUI calismasi tamamlandi.")
