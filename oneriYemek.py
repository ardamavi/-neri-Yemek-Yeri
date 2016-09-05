import sqlite3
from copy import deepcopy
import platform # for Check what OS you running on
import os # for clearing screan

def clear_screan():
    if platform.system() == "Windows":
        os.system('cls')  # on windows
    else:
        os.system('clear') # on linux / os x

def set_sql_connect(database_name):
    return sqlite3.connect(database_name)

def set_sql_cursor(database_connect):
    return database_connect.cursor()

def set_connect_and_cursor():
    vt = set_sql_connect('database.sqlite')
    db = set_sql_cursor(vt)

    return vt, db

def close_connect(vt):
    if vt:
        vt.commit()
        vt.close

def create_table(table_name, columns):
    vt, db = set_connect_and_cursor()
    db.execute("CREATE TABLE IF NOT EXISTS {0} ({1})".format(table_name, columns))
    close_connect(vt)

def verileri_al(table, column):
    vt, db = set_connect_and_cursor()
    db.execute("SELECT {0} FROM {1}".format(column, table))
    tum_veriler = db.fetchall()
    close_connect(vt)
    return tum_veriler

def data_ekle(table, eklenecek):
    vt, db = set_connect_and_cursor()
    db.execute("INSERT INTO {0} VALUES ('{1}')".format(table, eklenecek))
    close_connect(vt)

def yeni_kullanici():
    tum_kullanicilar = verileri_al("kullanicilar", "*")
    inpt = input("Kullanıcı Adı: ")
    tmp_kullanicilar = []
    for bir_veri in tum_kullanicilar:
        if bir_veri[0] not in tmp_kullanicilar:
            tmp_kullanicilar.append(bir_veri[0])
    tum_kullanicilar = deepcopy(tmp_kullanicilar)
    if inpt not in tum_kullanicilar:
        data_ekle("kullanicilar", inpt)
        print("Kullanıcı Eklendi !")
        giris_yapildi(inpt)
    else:
        print("Hatalı Giriş !\nBu Kullanıcı Zaten Var\n")

def yer_puan_ekle(kullanici, yer, puan):
    vt, db = set_connect_and_cursor()
    db.execute("INSERT INTO puanlar VALUES ('{0}', '{1}', {2})".format(kullanici, yer, puan))
    close_connect(vt)

def puani_guncellencek_mi(kullanici, yer, puan):
    vt, db = set_connect_and_cursor()
    db.execute("SELECT yer FROM puanlar WHERE kisi='{0}'".format(kullanici))
    kisinin_yerleri = db.fetchall()
    kisinin_yerleri_list = []
    for bir_kullanici in kisinin_yerleri:
        kisinin_yerleri_list.append(bir_kullanici[0])
    if yer in kisinin_yerleri_list:
        db.execute("UPDATE puanlar SET puan='{0}' WHERE kisi='{1}' and yer='{2}'".format(puan, kullanici, yer))
        close_connect(vt)
        return True
    close_connect(vt)
    return False

def puanla(kullanici, tum_kullanicilar):
    tmp_kullanicilar = []
    for bir_kullanici in tum_kullanicilar:
        if bir_kullanici not in tmp_kullanicilar:
            tmp_kullanicilar.append(bir_kullanici)
    tum_kullanicilar = deepcopy(tmp_kullanicilar)

    if tum_kullanicilar != []:
        print("Yerler: ")
        for bir_kullanici in tum_kullanicilar:
            print("- "+bir_kullanici)
        print("Çıkış: 0")
    yer = input("Puanlama Yapacağınız Yer: ")
    if yer == "0" or yer == "":
        print("Puanlama menüsünden çıkış yapıldı.")
        return "cik"
    if yer not in tum_kullanicilar:
        print("Bu yer ile ilgili ilk puanı siz ekleyin !")
    puan = ""
    hata_mesaji = "Hatalı Giriş !\nLütfen 0 ile 10 arasında bir sayı giriniz."
    while True:
        puan = input("Puanınız: ")
        try:
            if 0 > int(puan) or int(puan) > 10:
                print(hata_mesaji)
            else:
                break
        except:
            print(hata_mesaji)
    if puani_guncellencek_mi(kullanici, yer, puan) == False:
        yer_puan_ekle(kullanici, yer, puan)
    print("Puan Eklendi !")
    clear_screan()
    return "cikma"

def yerler_dondur():
    create_table("puanlar", "kisi, yer, puan")
    db_yerler = verileri_al("puanlar", "yer")
    tum_kullanicilar = []
    for bir_kullanici in db_yerler:
        tum_kullanicilar.append(bir_kullanici[0])
    return tum_kullanicilar

def oneri_al(kullanici):
    vt, db = set_connect_and_cursor()
    tum_kullanicilar = verileri_al("kullanicilar", "*")
    tmp_kullanicilar = []
    for bir_kullanici in tum_kullanicilar:
            tmp_kullanicilar.append(bir_kullanici[0])
    tum_kullanicilar = deepcopy(tmp_kullanicilar)
    tum_kullanicilar.remove(kullanici)
    db.execute("SELECT * FROM puanlar WHERE kisi='{0}'".format(kullanici))
    benim_verilerim = db.fetchall()
    baskalarinin_verileri = []
    for kişi in tum_kullanicilar:
        db.execute("SELECT * FROM puanlar WHERE kisi='{0}'".format(kişi))
        baskalarinin_verileri.append(db.fetchall())
    benzer_kisi = ""
    benzer_kisiler = []
    for kisilerin_verileri in baskalarinin_verileri:
        kac_benzer = 0
        kac_puan_yakin = 0
        for bir_kisi_verileri in kisilerin_verileri:
            for benim_bir_verim in benim_verilerim:
                if bir_kisi_verileri[1] == benim_bir_verim[1]:
                    kac_benzer += 1
                    if abs(int(bir_kisi_verileri[2]) - int(benim_bir_verim[2])) <= 3:
                        kac_puan_yakin += 1
                        if bir_kisi_verileri[0] not in benzer_kisiler:
                            benzer_kisi = bir_kisi_verileri[0]
        if (kac_puan_yakin/kac_benzer) > (3/4):
            benzer_kisiler.append(benzer_kisi)
    oneri_yerler = []
    for bir_kisi_verileri in kisilerin_verileri:
        if bir_kisi_verileri[0] in benzer_kisiler:
            if int(bir_kisi_verileri[2]) > 5:
                if bir_kisi_verileri[1] not in oneri_yerler:
                    oneri_yerler.append([bir_kisi_verileri[1], bir_kisi_verileri[2]])
    puana_gore_oneriler = []
    benim_yerlerim = []
    for bir_verim in benim_verilerim:
        if bir_verim[1] not in benim_yerlerim:
            benim_yerlerim.append(bir_verim[1])
    for yer_puan in oneri_yerler:
        if int(yer_puan[1]) > 5:
            if (yer_puan[1] not in puana_gore_oneriler) and (yer_puan[0] not in benim_yerlerim):
                puana_gore_oneriler.append(yer_puan[0])
    close_connect(vt)
    clear_screan()
    if puana_gore_oneriler == []:
        print("Size özel bir öneri bulunamadı !")
    else:
        print("Sizin için önerilerim: ")
        for bir_yer in puana_gore_oneriler:
            print("- "+bir_yer)

    inpt = input("\nMenüye Dönmek İçin: Enter")

def giris_yapildi(kullanici):
    clear_screan()

    print("Giriş Yapıldı !\nHoş Geldiniz "+kullanici+"\n")
    while True:
        print("1. Önerileri Al\n2. Puanla\nRastgele -> Çıkış")
        inpt = input("\nSecim: ")
        if inpt == "1":
            if yerler_dondur() == []:
                clear_screan()
                print("Database boş !\nÖneri alamazsınız.")
            else:
                clear_screan()
                oneri_al(kullanici)
        elif inpt == "2":
            cikis_yapilsin_mi = "cikma"
            clear_screan()
            while cikis_yapilsin_mi == "cikma":
                cikis_yapilsin_mi = puanla(kullanici, yerler_dondur())
            clear_screan()
        else:
            clear_screan()
            break

def kullanici_giris():
    tum_kullanicilar = verileri_al("kullanicilar", "*")
    if tum_kullanicilar == []:
        print("Hiç Kullanıcı Yok !\nYeni Kullanıcı Eklemeniz Gerekmekte !")
        yeni_kullanici()
        return
    print("Tüm Kullanıcılar:")
    for i in tum_kullanicilar:
        print("-",i[0])
    inpt = input("\nKullanıcı Adı: ")
    for bir_kullanici in tum_kullanicilar:
        if inpt == bir_kullanici[0]:
            giris_yapildi(inpt)
            return
    clear_screan()
    print("Hatalı Giriş !\nBöyle Bir Kullanıcı Bulunmamakta\n")
    kullanici_giris()

def main():
        create_table("kullanicilar", "kullaniciAdi")
        clear_screan()
        print("Yemek Yeri Öneri Programı - Arda Mavi\n")
        while True:
            print("1. Kullanıcı Girişi\n2. Yeni Kullanıcı\nRastgele -> Çıkış")
            inpt = input("\nSecim: ")
            clear_screan()
            if inpt == "1":
                kullanici_giris()
            elif inpt == "2":
                yeni_kullanici()
            else:
                break
        print("Çıkış Yapıldı !\nArda Mavi - ardamavi.com")

if __name__ == "__main__":
    main()
