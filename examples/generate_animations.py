#!/usr/bin/env python
"""
Generate animations for Science in Motion TikTok channel
This script allows generating one or more physics visualizations
with command line arguments.
"""

import os
import argparse
import sys

# Add the repository root to the path to allow imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import simulation functions
from src.simulations.double_pendulum import create_double_pendulum_animation
from src.simulations.lorenz_attractor import create_lorenz_attractor_animation
from src.simulations.mandelbrot_zoom import create_mandelbrot_zoom_animation
from src.simulations.wave_function_collapse import create_wave_function_collapse_animation
from src.simulations.fourier_series import create_fourier_visualization
from src.simulations.trig_challenge import create_trig_challenge_animation

def main():
    parser = argparse.ArgumentParser(description='Generate animations for Science in Motion TikTok channel')
    
    # Add arguments for each animation type
    parser.add_argument('--pendulum', action='store_true', help='Generate double pendulum animation')
    parser.add_argument('--lorenz', action='store_true', help='Generate Lorenz attractor animation')
    parser.add_argument('--mandelbrot', action='store_true', help='Generate Mandelbrot zoom animation')
    parser.add_argument('--quantum', action='store_true', help='Generate wave function collapse animation')
    parser.add_argument('--fourier', action='store_true', help='Generate Fourier series visualization')
    parser.add_argument('--trig', action='store_true', help='Generate trigonometry challenge animation')
    parser.add_argument('--all', action='store_true', help='Generate all animations')
    
    # Output directory
    parser.add_argument('--output', type=str, default='output', help='Output directory for animations')
    
    # Number of terms for Fourier series (optional)
    parser.add_argument('--terms', type=int, default=8, help='Number of terms for Fourier series visualization')
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if not any([args.pendulum, args.lorenz, args.mandelbrot, args.quantum, args.fourier, args.trig, args.all]):
        parser.print_help()
        return
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    # Generate animations based on arguments
    if args.all or args.pendulum:
        print("\n=== Generating Double Pendulum Animation ===")
        create_double_pendulum_animation(args.output)
        
    if args.all or args.lorenz:
        print("\n=== Generating Lorenz Attractor Animation ===")
        create_lorenz_attractor_animation(args.output)
        
    if args.all or args.mandelbrot:
        print("\n=== Generating Mandelbrot Zoom Animation ===")
        create_mandelbrot_zoom_animation(args.output)
        
    if args.all or args.quantum:
        print("\n=== Generating Wave Function Collapse Animation ===")
        create_wave_function_collapse_animation(args.output)
    
    if args.all or args.fourier:
        print("\n=== Generating Fourier Series Visualization ===")
        create_fourier_visualization(args.output, args.terms)
        
    if args.all or args.trig:
        print("\n=== Generating Trigonometry Challenge Animation ===")
        create_trig_challenge_animation(args.output)
        
    print("\nAll requested animations have been generated in the", args.output, "directory.")

if __name__ == '__main__':
    main()