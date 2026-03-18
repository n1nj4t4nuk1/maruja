import argparse
from dataclasses import dataclass

@dataclass
class MarujaConfig:
    output_prefix: str
    output_dir: str
    packet_limit: int

def parse_arguments() -> MarujaConfig:
    parser = argparse.ArgumentParser(description="Maruja - Network Packet Capture Tool")
    parser.add_argument('--output', type=str, nargs='?', default='capture', help='PCAP file output name prefix.')
    parser.add_argument('--dir', type=str, nargs='?', default='/records', help='Directory to save PCAP files.')
    parser.add_argument('--limit', type=int, nargs='?', default=10000, help='Number of packets per file.')
    
    args = parser.parse_args()
    
    return MarujaConfig(
        output_prefix=args.output,
        output_dir=args.dir,
        packet_limit=args.limit
    )
