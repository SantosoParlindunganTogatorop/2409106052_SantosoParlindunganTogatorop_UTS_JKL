#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
identitas.py
Tujuan  : Menyimpan identitas cabang (NIM, nama, kode cabang) dan menyediakan
          function pembuat ID perangkat yang konsisten untuk seluruh project
          UTS Jaringan Komputer Lanjut.
Pembuat : Santoso Parlindungan Togatorop (NIM 2409106052)
"""

nim = "2409106052"
nama = "Santoso Parlindungan Togatorop"
kode_cabang = nim[-3:]  # 3 digit terakhir NIM -> "052"


def buat_id_perangkat(jenis, nomor):
    """Membuat ID perangkat dengan format JENIS-KODECABANG-NOMOR.

    Contoh: buat_id_perangkat("router", 1) -> "ROUTER-052-01"
    """
    jenis = str(jenis).strip().upper()
    if not jenis:
        raise ValueError("Jenis perangkat tidak boleh kosong.")
    return f"{jenis}-{kode_cabang}-{int(nomor):02d}"


if __name__ == "__main__":
    print("=" * 45)
    print("IDENTITAS CABANG")
    print("=" * 45)
    print(f"Nama         : {nama}")
    print(f"NIM          : {nim}")
    print(f"Kode cabang  : {kode_cabang}")
    print("-" * 45)
    print(f"ID Router    : {buat_id_perangkat('router', 1)}")
    print(f"ID Switch    : {buat_id_perangkat('switch', 2)}")
    print(f"ID Server    : {buat_id_perangkat('server', 3)}")