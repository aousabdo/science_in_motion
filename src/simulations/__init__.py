"""
Simulation modules for Science in Motion animations.

These modules provide functions to create various scientific and mathematical animations
optimized for sharing on social media platforms like TikTok.
"""

from src.simulations.double_pendulum import create_double_pendulum_animation
from src.simulations.lorenz_attractor import create_lorenz_attractor_animation
from src.simulations.mandelbrot_zoom import create_mandelbrot_zoom_animation
from src.simulations.wave_function_collapse import create_wave_function_collapse_animation
from src.simulations.fourier_series import create_fourier_visualization
from src.simulations.trig_challenge import create_trig_challenge_animation
from src.simulations.sine_circle_trace import create_sine_circle_trace_animation

__all__ = [
    'create_double_pendulum_animation',
    'create_lorenz_attractor_animation',
    'create_mandelbrot_zoom_animation',
    'create_wave_function_collapse_animation',
    'create_fourier_visualization',
    'create_trig_challenge_animation',
    'create_sine_circle_trace_animation'
] 