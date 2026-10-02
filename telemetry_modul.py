#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
telemetry_modul.py
Tujuan  : Menyediakan data sampel telemetry cpuUsage (menyerupai hasil decode GPB
          yang diterima collector) dan mengklasifikasikan tiap sampel menjadi
          KRITIS, WASPADA, atau NORMAL.
Pembuat : Santoso Parlindungan Togatorop (NIM 2409106052)

Aturan penurunan nilai dari NIM:
  Setiap pasangan digit berurutan pada NIM dijadikan satu sampel cpuUsage (%).
  Contoh NIM 2409106052 -> 24, 40, 09, 91, 10, 06, 60, 05, 52.
"""

from identitas import buat_id_perangkat, nim

SENSOR_PATH = "huawei-devm:devm/cpuInfos/cpuInfo"
BATAS_KRITIS = 80      # di atas 80            -> KRITIS
BATAS_WASPADA = 50     # 50 sampai 80          -> WASPADA, di bawah 50 -> NORMAL


def turunkan_sampel(nim_str):
    """Mengubah NIM menjadi daftar nilai cpuUsage dari pasangan digit berurutan."""
    return [int(nim_str[i:i + 2]) for i in range(len(nim_str) - 1)]


# Data sampel menyerupai hasil decode GPB: node, sensor path, lalu nilai per sampel.
DATA_TELEMETRY = {
    "node": buat_id_perangkat("router", 1),
    "sensor_path": SENSOR_PATH,
    "sampel": {
        f"sampel_{urutan:02d}": {"cpuUsage": nilai}
        for urutan, nilai in enumerate(turunkan_sampel(nim), start=1)
    },
}


def tentukan_status(cpu_usage):
    """Menentukan status berdasarkan nilai cpuUsage."""
    if cpu_usage > BATAS_KRITIS:
        return "KRITIS"
    if cpu_usage >= BATAS_WASPADA:
        return "WASPADA"
    return "NORMAL"


def klasifikasi_telemetry(data=DATA_TELEMETRY):
    """Meng-iterasi semua sampel, mencetak klasifikasinya, dan mengembalikan hasilnya."""
    detail = {}
    ringkasan = {"KRITIS": 0, "WASPADA": 0, "NORMAL": 0}

    print(f"[TELEMETRY] Node   : {data['node']}")
    print(f"[TELEMETRY] Sensor : {data['sensor_path']}")
    print(f"[TELEMETRY] Jumlah sampel: {len(data['sampel'])}")

    for nama_sampel, isi in data["sampel"].items():
        cpu = isi["cpuUsage"]
        status = tentukan_status(cpu)
        detail[nama_sampel] = {"cpuUsage": cpu, "status": status}
        ringkasan[status] += 1
        print(f"  {nama_sampel:<10} cpuUsage = {cpu:>3}% -> {status}")

    print(
        "[TELEMETRY] Ringkasan : "
        + " | ".join(f"{status}: {jumlah}" for status, jumlah in ringkasan.items())
    )

    return {"node": data["node"], "detail": detail, "ringkasan": ringkasan}


if __name__ == "__main__":
    klasifikasi_telemetry()