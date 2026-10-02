#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
snmp_modul.py
Tujuan  : Mengambil nilai sysName (OID 1.3.6.1.2.1.1.5.0) dari perangkat memakai
          SNMPv2c dan PySNMP. Kegagalan ditangani dengan try/except agar program
          tidak berhenti.
Pembuat : Santoso Parlindungan Togatorop (NIM 2409106052)
"""

import asyncio

from pysnmp.hlapi.v3arch.asyncio import (
    CommunityData,
    ContextData,
    ObjectIdentity,
    ObjectType,
    SnmpEngine,
    UdpTransportTarget,
    get_cmd,
)

from identitas import kode_cabang

HOST = "127.0.0.1"
PORT = 161
COMMUNITY = f"comm_{kode_cabang}"        
OID_SYSNAME = "1.3.6.1.2.1.1.5.0"
TIMEOUT = 3                              
RETRIES = 1


async def _get_sysname(host, port):
    """Mengirim SNMP GET untuk sysName (SNMPv2c) dan mengembalikan hasil mentahnya."""
    engine = SnmpEngine()
    try:
        target = await UdpTransportTarget.create(
            (host, port), timeout=TIMEOUT, retries=RETRIES
        )
        return await get_cmd(
            engine,
            CommunityData(COMMUNITY, mpModel=1),  # mpModel=1 -> SNMPv2c
            target,
            ContextData(),
            ObjectType(ObjectIdentity(OID_SYSNAME)),
        )
    finally:
        engine.close_dispatcher()


def cek_snmp(host=HOST, port=PORT):
    """Ambil sysName lewat SNMPv2c, cetak hasil, dan kembalikan dict hasil."""
    hasil = {
        "host": host,
        "oid": OID_SYSNAME,
        "status": "GAGAL",
        "sysname": "-",
        "pesan": "",
    }

    print(f"[SNMP] GET sysName ({OID_SYSNAME}) ke {host}:{port} (SNMPv2c) ...")
    try:
        error_indication, error_status, error_index, var_binds = asyncio.run(
            _get_sysname(host, port)
        )
        if error_indication:
            hasil["pesan"] = f"Tidak ada respons: {error_indication}"
        elif error_status:
            hasil["pesan"] = (
                f"Error SNMP: {error_status.prettyPrint()} (indeks {error_index})"
            )
        else:
            _, nilai = var_binds[0]
            hasil["sysname"] = nilai.prettyPrint()
            hasil["status"] = "BERHASIL"
            hasil["pesan"] = "sysName berhasil diambil."
    except Exception as err:  # pengaman agar program tidak berhenti
        hasil["pesan"] = f"Terjadi kesalahan: {err}"

    print(f"[SNMP] Status  : {hasil['status']}")
    print(f"[SNMP] Pesan   : {hasil['pesan']}")
    print(f"[SNMP] sysName : {hasil['sysname']}")

    return hasil


if __name__ == "__main__":
    cek_snmp()