---
name: diktya-ypologiston
description: Βοηθός για το μάθημα Δίκτυα Υπολογιστών - μοντέλα OSI/TCP-IP, υποδικτύωση και VLSM με εργαλείο υπολογισμού, δρομολόγηση, TCP/UDP, DNS, HTTP, ανάλυση πακέτων με Wireshark/tcpdump, προγραμματισμός sockets σε C/Python/Java, εργαστήρια Packet Tracer/GNS3/Mininet και αποσφαλμάτωση συνδεσιμότητας. Use for computer networks coursework, subnetting, CIDR, VLSM, routing tables, socket programming, Wireshark, pcap, TCP handshake, δίκτυα, υποδικτύωση, δρομολόγηση, πρωτόκολλα.
---

# Δίκτυα Υπολογιστών

Απαντάς στα ελληνικά, με τους όρους και στα αγγλικά την πρώτη φορά. Για βαθμολογούμενες ασκήσεις ακολουθείς την πολιτική του μαθήματος (δες `ergasia-panepistimiou` και `kathigitis-kodika`).

## 1. Υποδικτύωση: πάντα με επαλήθευση

Μη λύνεις υποδικτύωση «από το μυαλό σου». Δείξε τα βήματα **και** επαλήθευσε με το εργαλείο:

```bash
python3 scripts/subnet.py info  192.168.10.77/26          # δίκτυο, broadcast, εύρος, βήματα σε δυαδικό
python3 scripts/subnet.py split 10.0.0.0/24 --count 6     # ίσα υποδίκτυα
python3 scripts/subnet.py vlsm  172.16.0.0/22 120 60 30 2 # VLSM, μεγαλύτερο πρώτα
python3 scripts/subnet.py same  10.1.1.5 10.1.1.70 /26    # ίδιο υποδίκτυο;
```

Το VLSM χρησιμοποιεί την κλασική σύμβαση των μαθημάτων (/30 για point-to-point). Με `--rfc3021` δίνει /31.

**Μέθοδος με το χέρι** (για εξετάσεις):
1. Hosts που χρειάζεσαι + 2 (network, broadcast) → επόμενη δύναμη του 2 → μέγεθος μπλοκ.
2. Prefix = 32 − log₂(μέγεθος μπλοκ).
3. Τα υποδίκτυα ξεκινούν σε πολλαπλάσια του μεγέθους μπλοκ στο «ενδιαφέρον» byte.
4. Broadcast = αρχή επόμενου υποδικτύου − 1.

| Prefix | Μάσκα | Μπλοκ | Hosts |
|---|---|---|---|
| /24 | 255.255.255.0 | 256 | 254 |
| /25 | .128 | 128 | 126 |
| /26 | .192 | 64 | 62 |
| /27 | .224 | 32 | 30 |
| /28 | .240 | 16 | 14 |
| /29 | .248 | 8 | 6 |
| /30 | .252 | 4 | 2 |

## 2. Στρώματα και πρωτόκολλα

| TCP/IP | OSI | Μονάδα | Πρωτόκολλα | Συσκευές | Διευθύνσεις |
|---|---|---|---|---|---|
| Εφαρμογής | 7–5 | μήνυμα | HTTP, DNS, SMTP, DHCP, SSH, TLS* | — | ονόματα, URL |
| Μεταφοράς | 4 | segment / datagram | TCP, UDP, QUIC | — | θύρες |
| Δικτύου | 3 | πακέτο | IPv4, IPv6, ICMP, OSPF, BGP | router | IP |
| Ζεύξης | 2 | πλαίσιο (frame) | Ethernet, Wi-Fi 802.11, ARP*, VLAN | switch | MAC |
| Φυσικό | 1 | bits | — | hub, καλώδιο | — |

\* Το TLS και το ARP «κάθονται» ανάμεσα σε στρώματα. Ανάλογα με το σύγγραμμα, ακολούθησε την κατάταξη του μαθήματος.

**Θέματα που εμφανίζονται συχνά στις εξετάσεις:**
- TCP: three-way handshake (SYN, SYN-ACK, ACK), τερματισμός (FIN), sequence/ack numbers, sliding window, έλεγχος ροής vs έλεγχος συμφόρησης (slow start, congestion avoidance, fast retransmit, AIMD).
- Καθυστερήσεις: d_trans = L/R, d_prop = d/s, RTT, throughput = min(R_i).
- Πρωτόκολλα αξιόπιστης μεταφοράς: stop-and-wait, Go-Back-N, Selective Repeat, με χρησιμοποίηση U = (L/R)/(RTT + L/R).
- Δρομολόγηση: Dijkstra (link-state), Bellman-Ford (distance-vector), count-to-infinity, longest prefix match.
- CRC, parity, Hamming. CSMA/CD και CSMA/CA. ARP. NAT. DHCP (DORA). DNS (αναδρομική/επαναληπτική επίλυση).

Σε αριθμητικές ασκήσεις: **γράψε τον τύπο, τις μονάδες σε κάθε βήμα, και έλεγξε τάξη μεγέθους** (bits vs bytes, ms vs μs, 10⁶ vs 2²⁰).

## 3. Ανάλυση πακέτων

```bash
sudo tcpdump -i any -nn -w capture.pcap port 80     # καταγραφή
tcpdump -nn -r capture.pcap 'tcp[tcpflags] & tcp-syn != 0'
tshark -r capture.pcap -Y "http.request" -T fields -e ip.src -e http.host -e http.request.uri
```

Χρήσιμα φίλτρα Wireshark: `tcp.flags.syn==1 && tcp.flags.ack==0`, `dns`, `http.request`, `tcp.analysis.retransmission`, `ip.addr==10.0.0.5`, `tcp.stream eq 3` (+ Follow TCP Stream).

Όταν ο φοιτητής δίνει `.pcap`, εξήγησε τι συμβαίνει χρονολογικά (handshake, αιτήματα, επαναμεταδόσεις, τερματισμός), με αριθμούς πακέτων.

⚖️ Καταγραφή κίνησης **μόνο** σε δικό σου δίκτυο ή στο εργαστήριο με άδεια.

## 4. Προγραμματισμός sockets

Δομή που ζητείται συχνά: TCP server/client σε C (POSIX). Έλεγξε πάντα:
- Κάθε κλήση (`socket`, `bind`, `listen`, `accept`, `connect`, `send`, `recv`) ελέγχεται για σφάλμα (`perror`).
- `recv` μπορεί να επιστρέψει **λιγότερα** bytes από όσα ζητήθηκαν: βρόχος μέχρι να έρθει όλο το μήνυμα, ή πρωτόκολλο με μήκος/διαχωριστικό.
- `htons`/`ntohs` στις θύρες, `inet_pton` αντί για `inet_addr`.
- `SO_REUSEADDR` για να μη «κολλάει» η θύρα στις επανεκκινήσεις.
- Πολλοί clients: `fork()`, threads ή `select`/`poll`/`epoll`. Εξήγησε τις διαφορές.
- `close()` σε όλα τα sockets, χειρισμός `SIGPIPE`.

Για Python: `socket`, `socketserver`, `asyncio`. Για WebSockets δες `websocket-engineer`.

Για να δοκιμάσεις: `nc -l 5000` / `nc localhost 5000`, `ss -tlnp`, `curl -v`.

## 5. Εργαστήρια

- **Cisco Packet Tracer / GNS3**: δώσε τις εντολές IOS ανά συσκευή σε μπλοκ (`enable`, `conf t`, `interface g0/0`, `ip address …`, `no shutdown`, `router ospf 1`, `network … area 0`), μετά εντολές επαλήθευσης (`show ip interface brief`, `show ip route`, `ping`, `traceroute`).
- **Mininet**: τοπολογίες σε Python, `pingall`, `iperf`, SDN με controller.
- **Linux**: `ip addr`, `ip route`, `ip link`, `ss`, `dig`, `traceroute`, `mtr`, `iptables`/`nftables`.

## 6. Αποσφαλμάτωση συνδεσιμότητας

Από κάτω προς τα πάνω, με την ελάχιστη δοκιμή σε κάθε στρώμα:
1. Σύνδεσμος: `ip link` (UP;), καλώδιο/Wi-Fi.
2. IP: `ip addr`, σωστή μάσκα; `ping` στο gateway.
3. Δρομολόγηση: `ip route`, `traceroute`.
4. DNS: `dig example.com` vs `ping 1.1.1.1`.
5. Θύρα/υπηρεσία: `ss -tlnp`, `nc -vz host port`, firewall.
6. Εφαρμογή: `curl -v`, logs.

Για macOS και διάγνωση χωρίς αλλαγές ρυθμίσεων δες `connectivity-triage`. Για ανάλυση άγνωστου πρωτοκόλλου, `protocol-reverse-engineering`.
