from utils.logger import setup_logger
from core.writer import GlobalPacketWriter

logger = setup_logger(__name__)

class PacketProcessor:
    def __init__(self, interface: str, writer: GlobalPacketWriter):
        self.interface = interface
        self.writer = writer
        self._detected_packets = 0

    def process_packet(self, packet):
        """Callback function for processing a single packet."""
        try:
            self._detected_packets += 1
            
            # Delegate writing to the global writer
            self.writer.write(packet)
            
            # Log progress
            if self._detected_packets % 100 == 0:
                logger.debug(f"Interface {self.interface}: Captured {self._detected_packets} packets.")
                
        except Exception as e:
            logger.error(f"Error processing packet on {self.interface}: {e}")

    def close(self):
        """Clean up resources."""
        # Nothing to close here as the writer is shared and managed externally
        pass
