#!/usr/bin/env python
"""
Generate animations for Science in Motion TikTok channel
This script allows generating one or more physics visualizations
with command line arguments.
"""

import os
import argparse
import sys

# Add the parent directory to the path so we can import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import simulation functions
from src.simulations.double_pendulum import create_double_pendulum_animation
from src.simulations.lorenz_attractor import create_lorenz_attractor_animation
from src.simulations.mandelbrot_zoom import create_mandelbrot_zoom_animation
from src.simulations.wave_function_collapse import create_wave_function_collapse_animation

def main():
    """
    Generate animations for the Science in Motion TikTok channel.
    Use command line arguments to specify which animations to create.
    Example: python generate_animations.py --double_pendulum --lorenz
    """
    parser = argparse.ArgumentParser(description='Generate animations for Science in Motion')
    
    # Add arguments for each animation type
    parser.add_argument('--double_pendulum', action='store_true', help='Generate double pendulum animation')
    parser.add_argument('--lorenz', action='store_true', help='Generate Lorenz attractor animation')
    parser.add_argument('--mandelbrot', action='store_true', help='Generate Mandelbrot zoom animation')
    parser.add_argument('--quantum', action='store_true', help='Generate quantum wave function collapse animation')
    parser.add_argument('--all', action='store_true', help='Generate all animations')
    
    # Add output directory argument
    parser.add_argument('--output_dir', type=str, default='output', help='Directory to save animations')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Generate animations based on arguments
    if args.all or args.double_pendulum:
        create_double_pendulum_animation(args.output_dir)
    
    if args.all or args.lorenz:
        create_lorenz_attractor_animation(args.output_dir)
    
    if args.all or args.mandelbrot:
        create_mandelbrot_zoom_animation(args.output_dir)
    
    if args.all or args.quantum:
        create_wave_function_collapse_animation(args.output_dir)
    
    # If no specific animations were requested, display help
    if not (args.all or args.double_pendulum or args.lorenz or args.mandelbrot or args.quantum):
        parser.print_help()

if __name__ == "__main__":
    main()