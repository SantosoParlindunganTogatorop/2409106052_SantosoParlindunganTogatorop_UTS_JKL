#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
netconf_modul.py
Tujuan  : Membangun (bukan menulis manual) pesan NETCONF <rpc><edit-config>
          untuk membuat VLAN dengan ID dari kode_cabang, memakai
          xml.etree.ElementTree, lalu mengembalikannya sebagai string XML.
Pembuat : Santoso Parlindungan Togatorop (NIM 2409106052)

Empat layer NETCONF:
  - Transport  : SSH (port 830). Tidak tampil di XML karena ditangani oleh
                 sesi SSH yang membawa pesan ini.
  - Messages   : elemen <rpc> beserta atribut message-id.
  - Operations : elemen <edit-config> beserta parameter <target>.
  - Content    : data konfigurasi VLAN di dalam elemen <config>.
"""

import xml.etree.ElementTree as ET

from identitas import kode_cabang

PORT_NETCONF = 830                 
NS_NETCONF = "urn:ietf:params:xml:ns:netconf:base:1.0"
NS_NATIVE = "http://cisco.com/ns/yang/Cisco-IOS-XE-native"
NS_VLAN = "http://cisco.com/ns/yang/Cisco-IOS-XE-vlan"

VLAN_ID = int(kode_cabang)             
VLAN_NAME = f"VLAN_{kode_cabang}"        
MESSAGE_ID = "101"


def buat_pesan_netconf(vlan_id=VLAN_ID, vlan_name=VLAN_NAME, message_id=MESSAGE_ID):
    """Membangun pesan <rpc><edit-config> pembuat VLAN dan mengembalikan string XML."""

    # ===== MESSAGES LAYER: pembungkus RPC dan identitas pesan =====
    rpc = ET.Element("rpc", {"message-id": message_id, "xmlns": NS_NETCONF})

    # ===== OPERATIONS LAYER: operasi <edit-config> pada datastore running =====
    edit_config = ET.SubElement(rpc, "edit-config")
    target = ET.SubElement(edit_config, "target")
    ET.SubElement(target, "running")
    ET.SubElement(edit_config, "default-operation").text = "merge"

    # ===== CONTENT LAYER: data konfigurasi VLAN (berdasarkan model YANG) =====
    config = ET.SubElement(edit_config, "config")
    native = ET.SubElement(config, "native", {"xmlns": NS_NATIVE})
    vlan = ET.SubElement(native, "vlan")
    vlan_list = ET.SubElement(vlan, "vlan-list", {"xmlns": NS_VLAN})
    ET.SubElement(vlan_list, "id").text = str(vlan_id)
    ET.SubElement(vlan_list, "name").text = vlan_name

    ET.indent(rpc, space="  ")            
    return ET.tostring(rpc, encoding="unicode")


if __name__ == "__main__":
    print(f"[NETCONF] Transport: SSH, port {PORT_NETCONF}")
    print(f"[NETCONF] Pesan <rpc><edit-config> pembuat VLAN {VLAN_ID} ({VLAN_NAME}):\n")
    print(buat_pesan_netconf())