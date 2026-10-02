# UTS Jaringan Komputer Lanjut - Integration Network with Python

- Nama: Santoso Parlindungan Togatorop
- NIM: 2409106052
- Mata kuliah: Jaringan Komputer Lanjut (Kelas B 2024, Informatika)
- Dosen pengampu: Reza Wardhana, M.Eng.

Project Python yang mengotomatisasi identitas cabang, akses SSH, monitoring SNMP,
pembuatan pesan NETCONF, dan analisis data telemetry, lalu menggabungkannya dalam
satu laporan akhir.

## Struktur Project

```
2409106052_SantosoParlindunganTogatorop_UTS_JKL/
├── .gitignore
├── README.md
├── main.py              # integrasi semua modul + laporan akhir (class LaporanCabang)
├── identitas.py         # identitas cabang dan buat_id_perangkat()
├── ssh_modul.py         # cek_ssh()  - SSH dengan Paramiko
├── snmp_modul.py        # cek_snmp() - SNMPv2c dengan PySNMP
├── netconf_modul.py     # buat_pesan_netconf() - XML <rpc><edit-config>
└── telemetry_modul.py   # klasifikasi_telemetry() - KRITIS/WASPADA/NORMAL
```

## Cara Menjalankan

1. Clone repository dan masuk ke foldernya:

```
   git clone https://github.com/SantosoParlindunganTogatorop/2409106052_SantosoParlindunganTogatorop_UTS_JKL.git
   cd 2409106052_SantosoParlindunganTogatorop_UTS_JKL
```

2. Buat dan aktifkan virtual environment (Windows PowerShell):

```
   python -m venv venv
   venv\Scripts\activate
```

3. Pasang library (PySNMP versi 7 ke atas):

```
   pip install paramiko "pysnmp>=7"
```

4. Jalankan program utama:

```
   python main.py
```

Prasyarat: target SSH dan SNMP agent aktif di perangkat tujuan. Password SSH diminta
saat program berjalan (atau dibaca dari environment variable `SSH_PASSWORD`).
Jika target tidak tersedia, program tetap berjalan dan melaporkan status GAGAL.

## Ringkasan Personalisasi

| Komponen              | Aturan yang dipakai                             |
| --------------------- | ----------------------------------------------- |
| kode_cabang           | 3 digit terakhir NIM                            |
| Username SSH          | `admin_<kode_cabang>`                           |
| Community string SNMP | `comm_<kode_cabang>`                            |
| VLAN ID (NETCONF)     | angka dari kode_cabang                          |
| Sampel telemetry      | pasangan digit berurutan pada NIM (cpuUsage, %) |

Klasifikasi telemetry: di atas 80 = KRITIS, 50-80 = WASPADA, di bawah 50 = NORMAL.
