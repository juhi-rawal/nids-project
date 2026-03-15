from scapy.all import sniff, IP
import sqlite3
from detector import detect_attack
import threading


def process_packet(packet):

    if packet.haslayer(IP):

        attack = detect_attack(packet)

        if attack:

            src = packet[IP].src
            dst = packet[IP].dst

            conn = sqlite3.connect("nids.db")
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO attacks (source_ip, destination_ip, attack) VALUES (?,?,?)",
                (src, dst, attack)
            )

            conn.commit()
            conn.close()


def start_sniffer():

    thread = threading.Thread(
        target=lambda: sniff(prn=process_packet, store=0)
    )

    thread.daemon = True
    thread.start()