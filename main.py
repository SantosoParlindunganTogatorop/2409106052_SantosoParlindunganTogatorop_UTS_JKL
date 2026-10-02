#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py
Tujuan  : Mengintegrasikan modul identitas, SSH, SNMP, NETCONF, dan telemetry,
          menjalankan seluruh function secara berurutan, lalu mencetak satu
          laporan akhir gabungan untuk cabang.
Pembuat : Santoso Parlindungan Togatorop (NIM 2409106052)
"""

from datetime import datetime

import identitas
import netconf_modul
import snmp_modul
import ssh_modul
import telemetry_modul

LEBAR = 64


class LaporanCabang:
    """Menyusun dan menampilkan laporan akhir gabungan satu cabang."""

    def __init__(self, nama, nim, kode_cabang, id_router):
        self.nama = nama
        self.nim = nim
        self.kode_cabang = kode_cabang
        self.id_router = id_router

    @staticmethod
    def _bagian(judul):
        print("\n" + "-" * LEBAR)
        print(judul)
        print("-" * LEBAR)

    def tampilkan_laporan(self, hasil_ssh, hasil_snmp, pesan_netconf, hasil_telemetry):
        """Mencetak satu laporan gabungan dari hasil SSH, SNMP, NETCONF, dan telemetry."""
        print("\n" + "=" * LEBAR)
        print("LAPORAN AKHIR CABANG".center(LEBAR))
        print("=" * LEBAR)
        print(f"Nama         : {self.nama}")
        print(f"NIM          : {self.nim}")
        print(f"Kode cabang  : {self.kode_cabang}")
        print(f"ID Router    : {self.id_router}")
        print(f"Waktu        : {datetime.now():%Y-%m-%d %H:%M:%S}")

        # --- Bagian B: SSH ---
        self._bagian("1. SSH (Paramiko)")
        print(f"Target       : {hasil_ssh['username']}@{hasil_ssh['host']}")
        print(f"Status       : {hasil_ssh['status']}")
        print(f"Pesan        : {hasil_ssh['pesan']}")
        for perintah, keluaran in hasil_ssh["perintah"].items():
            print(f"  $ {perintah:<9}: {keluaran}")

        # --- Bagian C: SNMP ---
        self._bagian("2. SNMP (PySNMP, SNMPv2c)")
        print(f"Target       : {hasil_snmp['host']}")
        print(f"OID          : {hasil_snmp['oid']}")
        print(f"Status       : {hasil_snmp['status']}")
        print(f"Pesan        : {hasil_snmp['pesan']}")
        print(f"sysName      : {hasil_snmp['sysname']}")

        # --- Bagian D: NETCONF ---
        self._bagian("3. Pesan NETCONF (<rpc><edit-config>)")
        print(pesan_netconf)

        # --- Bagian E: Telemetry ---
        self._bagian("4. Klasifikasi Telemetry (cpuUsage)")
        print(f"Node         : {hasil_telemetry['node']}")
        for nama_sampel, isi in hasil_telemetry["detail"].items():
            print(f"  {nama_sampel:<10} cpuUsage = {isi['cpuUsage']:>3}% -> {isi['status']}")
        ringkasan = " | ".join(
            f"{status}: {jumlah}" for status, jumlah in hasil_telemetry["ringkasan"].items()
        )
        print(f"Ringkasan    : {ringkasan}")

        print("\n" + "=" * LEBAR)
        print("SELESAI".center(LEBAR))
        print("=" * LEBAR)


def main():
    print("=" * LEBAR)
    print("MENJALANKAN SELURUH MODUL".center(LEBAR))
    print("=" * LEBAR)

    id_router = identitas.buat_id_perangkat("router", 1)

    hasil_ssh = ssh_modul.cek_ssh()
    print()
    hasil_snmp = snmp_modul.cek_snmp()
    print()
    print("[NETCONF] Membangun pesan <rpc><edit-config> ...")
    pesan_netconf = netconf_modul.buat_pesan_netconf()
    print()
    hasil_telemetry = telemetry_modul.klasifikasi_telemetry()

    laporan = LaporanCabang(
        identitas.nama, identitas.nim, identitas.kode_cabang, id_router
    )
    laporan.tampilkan_laporan(hasil_ssh, hasil_snmp, pesan_netconf, hasil_telemetry)


if __name__ == "__main__":
    main()