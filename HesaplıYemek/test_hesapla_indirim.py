import logging
import pytest
from indirimhesabi import hesapla_indirim


logger = logging.getLogger("testLogger")
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("test.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

@pytest.mark.parametrize("toplam_fiyat, joker, site, sonuc", [
    (300, 0, 1, (300, 0, 300)),   # Yemeksepeti indirimsiz
    (260, 0, 1, (260, 0, 260)),   # Yemeksepeti indirimsiz
    (90, 1, 1, (90, 0, 90)),      # Yemeksepeti indirimli
    (500, 1, 1, (500, 150, 350)),  # Yemeksepeti indirimli

    (100, 0, 2, (100, 0, 100)),   # Getir indirimsiz
    (200, 0, 2, (200, 0, 200)),   # Getir indirimsiz
    (300, 1, 2, (300, 100, 200)),  # Getir indirimli
    (450, 1, 2, (450, 150, 300)),  # Getir indirimli

    (450, 0, 3, (450, 0, 450)),    # Migros indirimsiz
    (140, 0, 3, (140, 0, 140)),    # Migros indirimsiz
    (100, 1, 3, (100, 0, 100)),    # Migros indirimli
    (370, 1, 3, (370, 120, 250)),  # Migros indirimli
])
def test_hesapla_indirim(toplam_fiyat, joker, site, sonuc):
    result = hesapla_indirim(toplam_fiyat, joker, site)
    if result == sonuc:
        logger.info(
            f"PASS: Test Case: Toplam Fiyat={toplam_fiyat}, Joker={joker}, Site={site} => Expected: {sonuc}, Obtained: {result}"
        )
    else:
        logger.error(
            f"FAIL: Test Case: Toplam Fiyat={toplam_fiyat}, Joker={joker}, Site={site} => Expected: {sonuc}, Obtained: {result}"
        )
    assert result == sonuc
