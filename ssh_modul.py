#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ssh_modul.py
Tujuan  : Login ke perangkat (VM/laptop) lewat SSH memakai Paramiko, menjalankan
          perintah diagnostik, lalu mencetak hasilnya. Kegagalan koneksi
          ditangani dengan try/except agar program tidak berhenti.
Pembuat : Santoso Parlindungan Togatorop (NIM 2409106052)
"""

import os
import socket
from getpass import getpass

import paramiko

from identitas import kode_cabang

HOST = "127.0.0.1"                      
PORT = 22
USERNAME = f"admin_{kode_cabang}"        
TIMEOUT = 5                             
PERINTAH_DIAGNOSTIK = ["hostname", "whoami"]  


def jalankan_perintah(client, perintah):
    """Menjalankan satu perintah di perangkat remote dan mengembalikan outputnya."""
    _, stdout, stderr = client.exec_command(perintah, timeout=TIMEOUT)
    keluaran = stdout.read().decode(errors="replace").strip()
    galat = stderr.read().decode(errors="replace").strip()
    return keluaran or galat or "(tidak ada output)"


def cek_ssh(host=HOST, port=PORT):
    """Login SSH, jalankan perintah diagnostik, cetak hasil, dan kembalikan dict hasil."""
    hasil = {
        "host": host,
        "username": USERNAME,
        "status": "GAGAL",
        "perintah": {},
        "pesan": "",
    }

    # Password TIDAK ditulis di kode karena repository bersifat publik.
    password = os.environ.get("SSH_PASSWORD") or getpass(
        f"Password SSH untuk {USERNAME}@{host}: "
    )

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # cukup untuk lab

    print(f"[SSH] Menghubungkan ke {USERNAME}@{host}:{port} ...")
    try:
        client.connect(
            hostname=host,
            port=port,
            username=USERNAME,
            password=password,
            timeout=TIMEOUT,
            look_for_keys=False,
            allow_agent=False,
        )
        for perintah in PERINTAH_DIAGNOSTIK:
            hasil["perintah"][perintah] = jalankan_perintah(client, perintah)
        hasil["status"] = "BERHASIL"
        hasil["pesan"] = "Login dan eksekusi perintah berhasil."
    except paramiko.AuthenticationException:
        hasil["pesan"] = "Autentikasi gagal (username/password salah)."
    except (paramiko.SSHException, OSError, socket.timeout) as err:
        hasil["pesan"] = f"Koneksi gagal: {err}"
    except Exception as err:  # pengaman terakhir agar program tidak berhenti
        hasil["pesan"] = f"Terjadi kesalahan tak terduga: {err}"
    finally:
        client.close()

    print(f"[SSH] Status : {hasil['status']}")
    print(f"[SSH] Pesan  : {hasil['pesan']}")
    for perintah, keluaran in hasil["perintah"].items():
        print(f"[SSH] $ {perintah}\n      {keluaran}")

    return hasil


if __name__ == "__main__":
    cek_ssh()