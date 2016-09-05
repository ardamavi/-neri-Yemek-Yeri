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
    for bir_yer in kisinin_yerleri:
        kisinin_yerleri_list.append(bir_yer[0])
    if yer in kisinin_yerleri_list:
        db.execute("UPDATE puanlar SET puan='{0}' WHERE kisi='{1}' and yer='{2}'".format(puan, kullanici, yer))
        close_connect(vt)
        return True
    close_connect(vt)
    return False

def puanla(kullanici, db_yerler_list):
    tmp_db_yerler = []
    for bir_yer in db_yerler_list:
        if bir_yer not in tmp_db_yerler:
            tmp_db_yerler.append(bir_yer)
    db_yerler_list = deepcopy(tmp_db_yerler)

    if db_yerler_list != []:
        print("Yerler: ")
        for bir_yer in db_yerler_list:
            print("- "+bir_yer)
        print("Çıkış: 0")
    yer = input("Puanlama Yapacağınız Yer: ")
    if yer == "0":
        print("Puanlama menüsünden çıkış yapıldı.")
        return "cik"
    if yer not in db_yerler_list:
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
    db_yerler_list = []
    for bir_yer in db_yerler:
        db_yerler_list.append(bir_yer[0])
    return db_yerler_list

def oneri_al():
    inpt = input("Yapım Aşamasında !")

def giris_yapildi(kullanici):
    clear_screan()

    print("Giriş Yapıldı !\nHoş Geldiniz "+kullanici)
    while True:
        print("\n1. Önerileri Al\n2. Puanla\nRastgele -> Çıkış")
        inpt = input("Secim: ")
        if inpt == "1":
            if yerler_dondur() == []:
                print("Database boş !\nÖneri alamazsınız.")
            else:
                oneri_al()
        elif inpt == "2":
            cikis_yapilsin_mi = "cikma"
            clear_screan()
            while cikis_yapilsin_mi == "cikma":
                cikis_yapilsin_mi = puanla(kullanici, yerler_dondur())
        else:
            break
        clear_screan()

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

def menu():
    clear_screan()
    print("1. Kullanıcı Girişi\n2. Yeni Kullanıcı\nRastgele -> Çıkış")
    inpt = input("Secim: ")
    clear_screan()
    if inpt == "1":
        kullanici_giris()
    elif inpt == "2":
        yeni_kullanici()

def main():
        create_table("kullanicilar", "kullaniciAdi")
        menu()
        print("Çıkış Yapıldı !\nArda Mavi - ardamavi.com")

if __name__ == "__main__":
    main()
