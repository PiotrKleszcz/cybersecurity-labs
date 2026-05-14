from collections import Counter
from tabulate import tabulate

def generate_report(records: list):
    if not records:
        print("[!] No packets captured.")
        return

    protos = Counter(r["proto"] for r in records if r)
    src_ips = Counter(r["src"] for r in records if r and "src" in r)
    dst_ips = Counter(r["dst"] for r in records if r and "dst" in r)

    print("\n" + "="*50)
    print("  NETSNIFF — CAPTURE REPORT")
    print("="*50)
    print(f"\nTotal packets: {len(records)}")

    print("\n[Protocol distribution]")
    print(tabulate(protos.most_common(), headers=["Protocol", "Count"], tablefmt="simple"))

    print("\n[Top 5 source IPs]")
    print(tabulate(src_ips.most_common(5), headers=["Source IP", "Count"], tablefmt="simple"))

    print("\n[Top 5 destination IPs]")
    print(tabulate(dst_ips.most_common(5), headers=["Destination IP", "Count"], tablefmt="simple"))

    tcp_records = [r for r in records if r and r.get("proto") == "TCP"]
    scanners = Counter(r["src"] for r in tcp_records)
    suspects = [(ip, c) for ip, c in scanners.items() if c > 30]
    if suspects:
        print("\n[!] Possible port scan detected:")
        print(tabulate(suspects, headers=["Source IP", "TCP packets"], tablefmt="simple"))
    print("="*50 + "\n")
