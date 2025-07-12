import csv
from datetime import datetime
from collections import deque

menu_makanan = {
    "Sop Iga": 15000,
    "Dimsum Mentai": 28000,
    "Mie Goreng": 13000,
    "Gepuk": 15000
}

antrean = deque()
pesanan = []
riwayat_pesanan = []
struk_dicetak = []
pelanggan_aktif = None

def tambah_pelanggan():
    nama = input("Masukkan nama pelanggan: ")
    antrean.append(nama)
    print(f"Pelanggan '{nama}' masuk antrean.")

def proses_pelanggan():
    global pelanggan_aktif
    if not antrean:
        print("Tidak ada pelanggan di antrean.")
        return
    pelanggan_aktif = antrean.popleft()
    print(f"\n Sekarang melayani: {pelanggan_aktif}")

def lihat_menu():
    print("\n=== MENU MAKANAN RUMAHAN ===")
    for i, (nama, harga) in enumerate(menu_makanan.items(), start=1):
        print(f"{i}. {nama} - Rp{harga}")

def tampilkan_pesanan():
    if not pesanan:
        print("Belum ada pesanan.")
        return
    print("\n=== PESANAN SAAT INI ===")
    total = 0
    for i, item in enumerate(pesanan, start=1):
        print(f"{i}. {item[0]} x{item[1]} = Rp{item[3]}")
        total += item[3]
    print(f"\nTOTAL HARGA SEMUA PESANAN: Rp{total}")

def tambah_pesanan():
    if not pelanggan_aktif:
        print("Belum ada pelanggan yang sedang dilayani.")
        return
    nama = input("Masukkan nama makanan: ").strip().title()
    if nama in menu_makanan:
        try:
            jumlah = int(input(f"Berapa porsi {nama}? "))
            harga = menu_makanan[nama]
            total = jumlah * harga
            pesanan.append([nama, jumlah, harga, total])
            print(f"{jumlah} porsi {nama} berhasil ditambahkan.")
        except ValueError:
            print("Jumlah harus angka.")
    else:
        print("Menu tidak ditemukan.")

def edit_pesanan():
    tampilkan_pesanan()
    if pesanan:
        try:
            index = int(input("Masukkan nomor pesanan yang ingin diedit: ")) - 1
            if 0 <= index < len(pesanan):
                jumlah_baru = int(input(f"Jumlah baru untuk {pesanan[index][0]}: "))
                pesanan[index][1] = jumlah_baru
                pesanan[index][3] = jumlah_baru * pesanan[index][2]
                print("Pesanan berhasil diperbarui.")
            else:
                print("Nomor tidak valid.")
        except ValueError:
            print("Input harus angka.")

def hapus_pesanan():
    tampilkan_pesanan()
    if pesanan:
        try:
            index = int(input("Masukkan nomor pesanan yang ingin dihapus: ")) - 1
            if 0 <= index < len(pesanan):
                item = pesanan.pop(index)
                print(f"{item[0]} berhasil dihapus.")
            else:
                print("Nomor tidak valid.")
        except ValueError:
            print("Input harus angka.")

def simpan_ke_csv():
    if not pesanan:
        print("Tidak ada pesanan untuk disimpan.")
        return
    tanggal_hari_ini = datetime.today().strftime("%Y-%m-%d")
    with open("pesanan.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["tanggal", "menu", "jumlah", "harga", "total"])
        for item in pesanan:
            writer.writerow([tanggal_hari_ini, item[0], item[1], item[2], item[3]])
    riwayat_pesanan.append(pesanan.copy())
    struk_dicetak.append(pesanan.copy())
    print(f"\nStruk atas nama '{pelanggan_aktif}' disimpan ke 'pesanan.csv'.")
    pesanan.clear()

def main():
    while True:
        print("\n===== SISTEM PEMESANAN MAKANAN RUMAHAN =====")
        print("0. Tambah Pelanggan ke Antrean")
        print("1. Layani Pelanggan (Ambil dari antrean)")
        print("2. Tambah Pesanan")
        print("3. Edit Pesanan")
        print("4. Hapus Pesanan")
        print("5. Selesai & Cetak Struk")
        pilihan = input("Pilih menu (0-5): ")

        if pilihan == "0":
            tambah_pelanggan()
        elif pilihan == "1":
            proses_pelanggan()
            if pelanggan_aktif:
                lihat_menu()
        elif pilihan == "2":
            tambah_pesanan()
        elif pilihan == "3":
            edit_pesanan()
        elif pilihan == "4":
            hapus_pesanan()
        elif pilihan == "5":
            tampilkan_pesanan()
            simpan_ke_csv()
            print("Terima kasih. Struk telah disimpan.")
            break
        else:
            print("Pilihan tidak valid.")

main()