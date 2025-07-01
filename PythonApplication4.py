


#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      yigit
#
# Created:     01.07.2025
# Copyright:   (c) yigit 2025
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import random
import sys

def kurallar():                                                                                     #Kuralları yazma
    print(" BLACKJACK \n Kurallar:\n Kartlarin toplami 21'i gecmeden 21'e en yakin olan o turu kazanir\nKiz, Papaz ve Vale 10 puan değerindedir.\nAs lar 1 yada 11 puandir.\n2'den 10'a kadar olan kartlar normal degerdedir.\n(A)tusu kart almak icindir.\n(K)tusu kalmak icindir.\n(D)tusu bahsi 2 ye katlamak icindir ama 2 ye katladiktan sonra en az 1 kere kart alinmasi zorunludur\nBeraberlik durumunda bahis iade edilir.")

def bahis_alma(max_bahis):                                                                          #Oyun başladıgında kullanıcıdan alınan bahis miktarı
    while True:
        print('Ne kadar bahis koyucaksiniz ? (1-{}, yada Cikis)'.format(max_bahis))
        bahis = input('> ').upper().strip()
        if bahis == 'CIKIS':
            print('Oynadiginiz icin tesekkurler!')
            sys.exit()
        if not bahis.isdecimal():
            print('Lutfen sayi giriniz.\n')
            continue

        bahis = int(bahis)
        if 1 <= bahis <= max_bahis:
            return bahis

def Deste_Alma():                                                                                   #Iskambil kartlarini tanimlama ve kariştirma
    KUPA = chr(9829)  # 9829. Karakter '♥'.
    KARO = chr(9830)  # 9830. Karakter '♦'.
    MACA = chr(9824)  # 9824. Karakter '♠'.
    SINEK = chr(9827)  # 9827. Karakter '♣'.

    deste = []
    for tur in (KUPA, KARO, MACA, SINEK):
        for sayi in range(2, 11):
            deste.append((str(sayi), tur))
        for sayi in ('J', 'Q', 'K', 'A'):
            deste.append((sayi, tur))
    random.shuffle(deste)
    return deste

def Elleri_Gosterme(oyuncunun_eli, kurpiyerin_eli, kurpiyerin_acik_eli):                            #Oyudaki kartlari ekrana yazdırma
    print()
    if kurpiyerin_acik_eli:
        print('Kurpiyer:', Deste_Degeri_Alma(kurpiyerin_eli))
        Kart_Gosterme(kurpiyerin_eli)
    else:
        print('Kurpiyer: ???')
        Kart_Gosterme([ARKATARAF] + kurpiyerin_eli[1:])

    print('Oyuncu:', Deste_Degeri_Alma(oyuncunun_eli))
    Kart_Gosterme(oyuncunun_eli)

def Deste_Degeri_Alma(kartlar):                                                                     #Oyuncu ve kurpiyerin kart degerlerini hesaplama
    deger = 0
    as_sayisi = 0

    for kart in kartlar:
        sayi = kart[0]
        if sayi == 'A':
            as_sayisi += 1
        elif sayi in ('K', 'Q', 'J'):
            deger += 10
        else:
            deger += int(sayi)

    deger += as_sayisi
    for i in range(as_sayisi):
        if deger + 10 <= 21:
            deger += 10

    return deger

def Kart_Gosterme(kartlar):                                                                         #Ekrandaki kartlarin gozukmesi
    satirlar = ['', '', '', '', '']

    for i, kart in enumerate(kartlar):
        satirlar[0] += ' ___  '
        if kart == ARKATARAF:
            satirlar[1] += '|## | '
            satirlar[2] += '|###| '
            satirlar[3] += '|_##| '
        else:
            sayi, tur = kart
            satirlar[1] += '|{} | '.format(sayi.ljust(2))
            satirlar[2] += '| {} | '.format(tur)
            satirlar[3] += '|{}| '.format(sayi.rjust(2, ''))

    for satir in satirlar:
        print(satir)

def Hamle_yapma(oyuncunun_eli, para):                                                               #Oyuncu tarafindan yazdilan input ile oyunun devami saglanmasi

    while True:
        hamleler = ['(A)Kart al', '(K)Kalmak']

        if len(oyuncunun_eli) == 2 and para > 0:
            hamleler.append('(D)2x bahis')

        yapilan_hamle = ', '.join(hamleler) + ' > '
        hamle = input(yapilan_hamle).upper()
        if hamle in ('A', 'K'):
            return hamle
        if hamle == 'D' and '(D)2x bahis' in hamleler:
            return hamle

def para_miktari_kaydet(para):                                                                      #Oyun bitince oyuncunun parasini kaydetme
    with open("para_miktari.txt", "w") as dosya:
        dosya.write(str(para))

def para_miktari_oku():                                                                             #Oyun basladıginda oyuncunun eski parasi ile devam etmesi
    try:
        with open("para_miktari.txt", "r") as dosya:
            para = int(dosya.readline().strip())
        return para
    except FileNotFoundError:
        return None
#########################################

KUPA = chr(9829)  # 9829. Karakter '♥'.
KARO = chr(9830)  # 9830. Karakter '♦'.
MACA = chr(9824)  # 9824. Karakter '♠'.
SINEK = chr(9827)  # 9827. Karakter '♣'.
ARKATARAF = 'arkataraf'

para = para_miktari_oku()

if para is None:
    para = 5000

kurallar()
while True:
    if para <= 0:
        print('Kumarda kaybettin.')
        print('Belki ask\'ta kazanirsin.')
        print('Oynadigin icin tesekkurler.')
        sys.exit()

    para_miktari_kaydet(para)
    print('Para: ', para)
    bahis = bahis_alma(para)

    deste = Deste_Alma()
    kurpiyerin_eli = [deste.pop(), deste.pop()]
    oyuncunun_eli = [deste.pop(), deste.pop()]

    print('Bahis: ', bahis)
    while True:
        Elleri_Gosterme(oyuncunun_eli, kurpiyerin_eli, False)
        print()

        if Deste_Degeri_Alma(oyuncunun_eli) > 21:
            break

        hamle = Hamle_yapma(oyuncunun_eli, para - bahis)

        if hamle == 'D':
            Ek_Bahis = bahis_alma(min(bahis, (para - bahis)))
            bahis += Ek_Bahis
            print('Bahsiniz {} yükseldi.'.format(bahis))
            print('bahis: ', bahis)

        if hamle in ('A', 'D'):
            yeni_kart = deste.pop()
            sayi, tur = yeni_kart
            print('{} nin {} sayili kartini cektiniz.'.format(tur, sayi))
            oyuncunun_eli.append(yeni_kart)

            if Deste_Degeri_Alma(oyuncunun_eli) > 21:
                continue

        if hamle in ('K', 'D'):
            break

    if Deste_Degeri_Alma(oyuncunun_eli) <= 21:
        while Deste_Degeri_Alma(kurpiyerin_eli) < 17:
            print('Kurpiyer kart aldi...')
            kurpiyerin_eli.append(deste.pop())
            Elleri_Gosterme(oyuncunun_eli, kurpiyerin_eli, False)

            if Deste_Degeri_Alma(oyuncunun_eli) > 21:
                break

            input('Devam etmek icin ENTER a basiniz...')
            print('\n\n')

    Elleri_Gosterme(oyuncunun_eli, kurpiyerin_eli, True)

    oyuncunun_puani = Deste_Degeri_Alma(oyuncunun_eli)
    kurpiyerin_puani = Deste_Degeri_Alma(kurpiyerin_eli)

    if kurpiyerin_puani > 21:
        print('Kurpier 21 i asti {}TL kazandin!😎'.format(bahis))
        para += bahis
    elif (oyuncunun_puani > 21) or (oyuncunun_puani < kurpiyerin_puani):
        print('Kaybettin😥')
        para -= bahis
    elif oyuncunun_puani > kurpiyerin_puani:
        print('{}TL kazandin!🤯'.format(bahis))
        para += bahis
    elif oyuncunun_puani == kurpiyerin_puani:
        print('Berabere bitti, bahis geri verildi.')

    input('Devam etmek icin ENTER a basiniz...')
    print('\n\n')




