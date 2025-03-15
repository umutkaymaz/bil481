# indirimhesabı.py

def hesapla_indirim(toplam_fiyat, joker, site):
    """
    Verilen toplam fiyata göre (varsayılan %10 indirim) indirim miktarı ve 
    indirimli fiyatı hesaplar.
    
    Args:
        toplam_fiyat (float): Ürünlerin toplam fiyatı.
        oran (float): İndirim oranı (örn. 0.1 -> %10).

    Returns:
        tuple: (toplam_fiyat, indirim_miktari, indirimli_fiyat)
    """
    indirim_miktari=0
    
    if(site==1 and joker==1):
        if(150<=toplam_fiyat<300):
            indirim_miktari=60
        elif(300<=toplam_fiyat<450):
            indirim_miktari=100
        elif(450<=toplam_fiyat):
            indirim_miktari=150
        else:
            indirim_miktari=0
    elif(site==2 and joker==1):
        if(200<=toplam_fiyat<300):
            indirim_miktari=75
        elif(300<=toplam_fiyat<450):
            indirim_miktari=100
        elif(450<=toplam_fiyat):
            indirim_miktari=150
        else:
            indirim_miktari=0
    elif(site==3 and joker==1):
        if(150<=toplam_fiyat<250):
            indirim_miktari=60
        elif(250<=toplam_fiyat<350):
            indirim_miktari=90
        elif(350<=toplam_fiyat<450):
            indirim_miktari=120
        elif(450<=toplam_fiyat):
            indirim_miktari=150
        else:
            indirim_miktari=0
    else:
        indirim_miktari=0
      
    indirimli_fiyat = toplam_fiyat - indirim_miktari
    
    return toplam_fiyat, indirim_miktari, indirimli_fiyat
