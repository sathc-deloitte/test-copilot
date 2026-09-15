#!/usr/bin/env python3
"""
Script to print system uptime
"""

import os
import platform
from datetime import datetime, timedelta


def get_system_uptime():
    """
    Get and print the system uptime based on the operating system.
    """
    system = platform.system()
    
    try:
        if system == "Linux" or system == "Darwin":  # Linux or macOS
            # Get uptime from /proc/uptime (Linux) or use uptime command
            if os.path.exists("/proc/uptime"):
                with open("/proc/uptime", "r") as f:
                    uptime_seconds = float(f.read().split()[0])
            else:
                # Fallback for macOS or other Unix-like systems
                uptime_output = os.popen("uptime -p").read().strip()
                print(f"System Uptime: {uptime_output}")
                return
        
        elif system == "Windows":
            # Get uptime using wmic on Windows
            uptime_output = os.popen("wmic os get lastbootuptime").read()
            lines = uptime_output.strip().split("\n")
            if len(lines) > 1:
                boot_time_str = lines[1][:14]  # Extract YYYYMMDDHHMMSS
                boot_time = datetime.strptime(boot_time_str, "%Y%m%d%H%M%S")
                uptime_delta = datetime.now() - boot_time
                uptime_seconds = uptime_delta.total_seconds()
            else:
                print("Could not determine uptime on Windows")
                return
        else:
            print(f"Unsupported operating system: {system}")
            return
        
        # Convert seconds to readable format
        uptime_delta = timedelta(seconds=int(uptime_seconds))
        days = uptime_delta.days
        hours, remainder = divmod(uptime_delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        print(f"System: {system}")
        print(f"Total Uptime (seconds): {int(uptime_seconds)}")
        print(f"Uptime: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds")
        
    except Exception as e:
        print(f"Error getting system uptime: {e}")


if __name__ == "__main__":
    get_system_uptime()
