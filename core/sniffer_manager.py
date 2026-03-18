import threading
import traceback
from typing import List
from scapy.all import sniff
from scapy.config import conf
from scapy.interfaces import get_if_list

from core.packet_processor import PacketProcessor
from core.writer import GlobalPacketWriter
from config.arguments import MarujaConfig
from utils.logger import setup_logger

logger = setup_logger(__name__)

class SnifferThread(threading.Thread):
    def __init__(self, interface: str, writer: GlobalPacketWriter):
        super().__init__()
        self.interface = interface
        self.processor = PacketProcessor(
            interface=interface,
            writer=writer
        )
        self._stop_event = threading.Event()
        self.daemon = True

    def run(self):
        logger.info(f"Starting sniffer thread for interface: {self.interface}")
        try:
            sniff(
                prn=self.processor.process_packet,
                iface=self.interface,
                store=False,
            )
        except Exception as e:
            logger.error(f"Critical error in sniffer thread {self.interface}: {e}")
            logger.debug(traceback.format_exc())
        finally:
            self.processor.close()

    def stop(self):
        self._stop_event.set()

class SnifferManager:
    def __init__(self, config: MarujaConfig):
        self.config = config
        self.threads: List[SnifferThread] = []
        # Initialize the global writer
        self.writer = GlobalPacketWriter(
            directory=config.output_dir,
            file_prefix=config.output_prefix
        )

    def discover_interfaces(self) -> List[str]:
        conf.ifaces.reload()
        interfaces = get_if_list()
        logger.info(f"Detected interfaces: {interfaces}")
        return interfaces

    def start(self):
        interfaces = self.discover_interfaces()
        
        for interface in interfaces:
            if interface == 'lo': 
                continue
                
            # Pass the shared writer to each thread
            thread = SnifferThread(interface, self.writer)
            self.threads.append(thread)
            thread.start()
            
        logger.info(f"Started {len(self.threads)} sniffer threads.")

    def join(self):
        for thread in self.threads:
            thread.join()
        
        # Close the writer when all threads are done (or when manager is stopped)
        # Note: In the current main loop, join() might not be reached easily, 
        # but it's good practice.
        self.writer.close()
