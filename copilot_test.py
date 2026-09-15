#!/usr/bin/env python3
"""
Script to print system uptime with improved security and reliability.
"""

import os
import platform
import subprocess
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Tuple


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class UptimeReader:
    """Safe and reliable system uptime reader with security and error handling."""
    
    def __init__(self):
        """Initialize the uptime reader."""
        self.system = platform.system()
        self.uptime_seconds: Optional[int] = None
    
    def get_uptime(self) -> Optional[Tuple[int, int, int, int]]:
        """
        Get system uptime safely and return as (days, hours, minutes, seconds).
        
        Returns:
            Tuple of (days, hours, minutes, seconds) or None if retrieval fails.
        """
        try:
            if self.system == "Linux":
                return self._get_uptime_linux()
            elif self.system == "Darwin":  # macOS
                return self._get_uptime_macos()
            elif self.system == "Windows":
                return self._get_uptime_windows()
            else:
                logger.error(f"Unsupported operating system: {self.system}")
                return None
        except Exception as e:
            logger.error(f"Error retrieving system uptime: {e}")
            return None
    
    def _get_uptime_linux(self) -> Optional[Tuple[int, int, int, int]]:
        """
        Get uptime on Linux systems safely.
        
        Returns:
            Tuple of (days, hours, minutes, seconds) or None if failed.
        """
        try:
            uptime_file = Path("/proc/uptime")
            
            if not uptime_file.exists():
                logger.warning("/proc/uptime not found, attempting fallback method")
                return self._get_uptime_fallback()
            
            # Read uptime file safely with permission checks
            if not os.access(uptime_file, os.R_OK):
                logger.error("Permission denied reading /proc/uptime")
                return None
            
            with open(uptime_file, "r") as f:
                content = f.read().strip()
            
            if not content:
                logger.error("Empty /proc/uptime file")
                return None
            
            # Parse uptime safely
            parts = content.split()
            if len(parts) < 1:
                logger.error("Invalid /proc/uptime format")
                return None
            
            uptime_seconds = int(float(parts[0]))
            return self._convert_seconds_to_tuple(uptime_seconds)
        
        except (ValueError, OSError) as e:
            logger.error(f"Failed to read Linux uptime: {e}")
            return None
    
    def _get_uptime_macos(self) -> Optional[Tuple[int, int, int, int]]:
        """
        Get uptime on macOS systems safely.
        
        Returns:
            Tuple of (days, hours, minutes, seconds) or None if failed.
        """
        try:
            # Use subprocess with timeout and security flags
            result = subprocess.run(
                ["uptime", "-p"],
                capture_output=True,
                text=True,
                timeout=5,
                check=False
            )
            
            if result.returncode != 0:
                logger.warning("uptime command failed, attempting fallback")
                return self._get_uptime_fallback()
            
            output = result.stdout.strip()
            if not output:
                logger.error("Empty uptime output")
                return None
            
            logger.info(f"System Uptime: {output}")
            return None  # Fallback - uptime -p already prints formatted output
        
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            logger.error(f"Failed to execute uptime command on macOS: {e}")
            return self._get_uptime_fallback()
    
    def _get_uptime_windows(self) -> Optional[Tuple[int, int, int, int]]:
        """
        Get uptime on Windows systems safely.
        
        Returns:
            Tuple of (days, hours, minutes, seconds) or None if failed.
        """
        try:
            # Use subprocess with timeout and proper error handling
            result = subprocess.run(
                ["wmic", "os", "get", "lastbootuptime"],
                capture_output=True,
                text=True,
                timeout=10,
                check=False
            )
            
            if result.returncode != 0:
                logger.warning("wmic command failed, attempting fallback")
                return self._get_uptime_fallback()
            
            lines = result.stdout.strip().split("\n")
            if len(lines) < 2:
                logger.error("Invalid wmic output format")
                return None
            
            boot_time_str = lines[1][:14]  # Extract YYYYMMDDHHMMSS
            
            # Validate format
            if not boot_time_str.isdigit() or len(boot_time_str) != 14:
                logger.error("Invalid boot time format from wmic")
                return None
            
            boot_time = datetime.strptime(boot_time_str, "%Y%m%d%H%M%S")
            uptime_delta = datetime.now() - boot_time
            uptime_seconds = int(uptime_delta.total_seconds())
            
            if uptime_seconds < 0:
                logger.error("Negative uptime calculated - system clock may be incorrect")
                return None
            
            return self._convert_seconds_to_tuple(uptime_seconds)
        
        except (subprocess.TimeoutExpired, FileNotFoundError, ValueError) as e:
            logger.error(f"Failed to get Windows uptime: {e}")
            return self._get_uptime_fallback()
    
    def _get_uptime_fallback(self) -> Optional[Tuple[int, int, int, int]]:
        """
        Fallback method to get uptime (platform-agnostic).
        
        Returns:
            Tuple of (days, hours, minutes, seconds) or None if failed.
        """
        try:
            result = subprocess.run(
                ["uptime"],
                capture_output=True,
                text=True,
                timeout=5,
                check=False
            )
            
            if result.returncode == 0 and result.stdout.strip():
                logger.info(f"System Uptime (fallback): {result.stdout.strip()}")
                return None
            
            logger.warning("All uptime retrieval methods failed")
            return None
        
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            logger.error(f"Fallback method also failed: {e}")
            return None
    
    @staticmethod
    def _convert_seconds_to_tuple(uptime_seconds: int) -> Tuple[int, int, int, int]:
        """
        Convert uptime in seconds to (days, hours, minutes, seconds).
        
        Args:
            uptime_seconds: Uptime in seconds
            
        Returns:
            Tuple of (days, hours, minutes, seconds)
        """
        uptime_delta = timedelta(seconds=uptime_seconds)
        days = uptime_delta.days
        hours, remainder = divmod(uptime_delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return (days, hours, minutes, seconds)
    
    def print_uptime(self) -> None:
        """Print system uptime in a formatted way."""
        uptime = self.get_uptime()
        
        if uptime is None:
            logger.warning("Could not retrieve system uptime")
            return
        
        days, hours, minutes, seconds = uptime
        
        print(f"\n{'='*50}")
        print(f"System: {self.system}")
        print(f"Uptime: {days} day(s), {hours} hour(s), {minutes} minute(s), {seconds} second(s)")
        print(f"Total Uptime: {days * 86400 + hours * 3600 + minutes * 60 + seconds} seconds")
        print(f"{'='*50}\n")


def main():
    """Main entry point."""
    try:
        reader = UptimeReader()
        reader.print_uptime()
    except KeyboardInterrupt:
        logger.info("Uptime script interrupted by user")
    except Exception as e:
        logger.critical(f"Unexpected error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
