#!/usr/bin/env python3
"""
Example script to generate both the double pendulum and Lorenz attractor animations.
This script imports the simulation modules from the src package and runs them
to generate animations in the output directory.
"""

import os
import sys

# Add the parent directory to the path so we can import the src package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.simulations.double_pendulum import create_double_pendulum_animation
from src.simulations.lorenz_attractor import create_lorenz_animation

def main():
    """Generate both animations"""
    
    print("=== Science in Motion Animation Generator ===")
    print("\nGenerating Double Pendulum animation...")
    create_double_pendulum_animation()
    
    print("\nGenerating Lorenz Attractor animation...")
    create_lorenz_animation()
    
    print("\nDone! Check the 'output' directory for the generated MP4 files.")

if __name__ == "__main__":
    main() 