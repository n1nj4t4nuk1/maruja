import threading
import os
from datetime import datetime
from scapy.all import PcapWriter
from utils.logger import setup_logger

logger = setup_logger(__name__)

class GlobalPacketWriter:
    def __init__(self, directory: str, file_prefix: str):
        self.lock = threading.Lock()
        timestamp = datetime.now().timestamp()
        # Filename no longer includes interface since it's global
        filename = f'{file_prefix}@{timestamp}.pcap'
        self.filepath = os.path.join(directory, filename)
        
        os.makedirs(directory, exist_ok=True)
        
        # append=True allows appending to the file. 
        # Scapy handles the PCAP header automatically (writes it if file is empty/new).
        self.writer = PcapWriter(self.filepath, append=True)
        logger.info(f"Created global capture file: {self.filepath}")

    def write(self, packet):
        with self.lock:
            try:
                self.writer.write(packet)
                # Optional: self.writer.flush() if real-time updates are needed, 
                # but it impacts performance.
            except Exception as e:
                logger.error(f"Error writing packet to pcap: {e}")

    def close(self):
        with self.lock:
            if self.writer:
                self.writer.close()
                logger.info(f"Closed global capture file: {self.filepath}")
