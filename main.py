import time
import os
from config.arguments import parse_arguments
from core.sniffer_manager import SnifferManager
from utils.logger import setup_logger

logger = setup_logger(__name__)

def main():
    # Parse arguments
    config = parse_arguments()
    
    logger.info("Starting Maruja...")
    logger.info(f"Configuration: Output='{config.output_prefix}', Dir='{config.output_dir}', Limit={config.packet_limit}")

    # Ensure output directory exists
    if not os.path.exists(config.output_dir):
        try:
            os.makedirs(config.output_dir)
            logger.info(f"Created output directory: {config.output_dir}")
        except OSError as e:
            logger.error(f"Failed to create directory {config.output_dir}: {e}")
            return

    # Initialize and start sniffer manager
    manager = SnifferManager(config)
    
    try:
        manager.start()
        
        # Keep main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Stopping Tanuki Sniffer...")
        # In a real scenario, we would signal threads to stop here
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

if __name__ == '__main__':
    main()
