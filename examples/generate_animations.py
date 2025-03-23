#!/usr/bin/env python3
"""
Example script to generate animations for the Science in Motion TikTok channel.
This script imports the simulation modules from the src package and runs them
to generate animations in the output directory.
"""

import os
import sys
import argparse

# Add the parent directory to the path so we can import the src package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.simulations.double_pendulum import create_double_pendulum_animation
from src.simulations.lorenz_attractor import create_lorenz_animation
from src.simulations.mandelbrot_zoom import create_mandelbrot_animation

def main():
    """Generate animations based on command line arguments"""
    
    parser = argparse.ArgumentParser(description="Generate animations for Science in Motion")
    parser.add_argument("--all", action="store_true", help="Generate all animations")
    parser.add_argument("--pendulum", action="store_true", help="Generate double pendulum animation")
    parser.add_argument("--lorenz", action="store_true", help="Generate Lorenz attractor animation")
    parser.add_argument("--mandelbrot", action="store_true", help="Generate Mandelbrot zoom animation")
    parser.add_argument("--output", default="output", help="Output directory for animations")
    
    args = parser.parse_args()
    
    # If no specific animations are selected, generate all
    if not (args.pendulum or args.lorenz or args.mandelbrot or args.all):
        args.all = True
    
    print("=== Science in Motion Animation Generator ===")
    
    if args.all or args.pendulum:
        print("\nGenerating Double Pendulum animation...")
        create_double_pendulum_animation(output_dir=args.output)
    
    if args.all or args.lorenz:
        print("\nGenerating Lorenz Attractor animation...")
        create_lorenz_animation(output_dir=args.output)
    
    if args.all or args.mandelbrot:
        print("\nGenerating Mandelbrot Zoom animation...")
        create_mandelbrot_animation(output_dir=args.output)
    
    print("\nDone! Check the '{}' directory for the generated MP4 files.".format(args.output))

if __name__ == "__main__":
    main() 