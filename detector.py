from scapy.all import TCP

def detect_attack(packet):

    if packet.haslayer(TCP):

        flags = packet[TCP].flags

        if flags == "S":
            return "High - SYN Scan"

        elif flags == "F":
            return "Medium - FIN Scan"

        elif flags == "R":
            return "Low - RST Attack"

    return None