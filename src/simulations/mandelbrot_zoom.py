import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
import os
from numba import jit  # For just-in-time compilation

@jit(nopython=True)
def mandelbrot_numpy(h, w, max_iters, center_x, center_y, zoom_width):
    """
    Calculate the Mandelbrot set using Numba for acceleration.
    
    This is a faster implementation using Numba's just-in-time compilation.
    """
    zoom_height = zoom_width * h / w
    
    y_min = -center_y 
    y_max = zoom_height - center_y
    x_min = -center_x
    x_max = zoom_width - center_x
    
    x = np.linspace(x_min, x_max, w)
    y = np.linspace(y_min, y_max, h)
    
    result = np.zeros((h, w), dtype=np.int32)
    
    for i in range(h):
        for j in range(w):
            c = complex(x[j], y[i])
            z = 0.0
            for k in range(max_iters):
                z = z*z + c
                if (z.real*z.real + z.imag*z.imag) >= 4.0:
                    result[i, j] = k
                    break
    
    return result

def create_color_palette():
    """Create a vibrant color palette suited for the Mandelbrot visualization."""
    colors = [
        (0, 0, 0),       # Black
        (0, 0, 0.5),     # Dark blue
        (0, 0, 1),       # Blue
        (0, 0.5, 1),     # Sky blue
        (0, 1, 1),       # Cyan
        (0, 1, 0.5),     # Teal
        (0, 1, 0),       # Green
        (0.5, 1, 0),     # Lime
        (1, 1, 0),       # Yellow
        (1, 0.5, 0),     # Orange
        (1, 0, 0),       # Red
        (1, 0, 0.5),     # Pink
        (1, 0, 1),       # Magenta
        (0.5, 0, 1),     # Purple
        (0, 0, 0.5),     # Dark blue (cycle back)
    ]
    
    return LinearSegmentedColormap.from_list('mandelbrot', colors, N=2048)

def smooth_color(iterations, max_iters):
    """Apply smooth coloring to the Mandelbrot set for better visuals."""
    # Normalized iterations for smooth coloring
    return iterations / max_iters

def create_mandelbrot_animation(output_dir="output"):
    """
    Creates a visually stunning animation of zooming into the Mandelbrot set,
    optimized for TikTok with the portrait aspect ratio.
    
    Parameters:
    -----------
    output_dir : str
        Directory where output files will be saved
    """
    print("Creating Mandelbrot Zoom animation...")
    
    # Animation parameters - reduced for faster processing
    fps = 30
    duration = 20  # reduced from 30 seconds to 20 for faster generation
    frames = fps * duration
    
    # Mandelbrot calculation parameters - reduced resolution for faster processing
    width, height = 360, 640  # reduced from 540x960 for faster processing
    max_iterations = 80       # reduced from 100 for faster processing
    
    # Interesting zoom target coordinates
    # This is a beautiful spiral pattern in the Mandelbrot set
    target_x = -0.743643887037158704752191506114774
    target_y = 0.131825904205311970493132056385139
    
    # Zoom parameters - made less extreme for faster processing
    start_width = 3.0
    end_width = 0.00001  # reduced from 0.000000001 for faster processing
    
    # Precalculate zoom values to avoid repeated calculations
    zoom_values = []
    for frame in range(frames):
        # Calculate zoom factor and current width
        zoom_factor = (end_width / start_width) ** (1 / frames)
        current_width = start_width * (zoom_factor ** frame)
        zoom_ratio = start_width / current_width
        zoom_values.append((current_width, zoom_ratio))
    
    # Create figure and add a subplot with no frame
    plt.rcParams['figure.dpi'] = 100  # Explicit DPI setting
    fig = plt.figure(figsize=(3.6, 6.4), facecolor='black')  # Reduced figsize for faster processing
    ax = fig.add_subplot(111, frameon=False)
    ax.set_facecolor('black')
    
    # Remove ticks and labels
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Create color palette
    cmap = create_color_palette()
    
    # Initial image placeholder
    img = ax.imshow(np.zeros((height, width)), cmap=cmap, 
                   interpolation='nearest', extent=[-1, 1, -1, 1])
    
    # Text elements
    title = plt.text(0.5, 0.95, "Mandelbrot Set", color='white', 
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax.transAxes, fontsize=14)
    
    equation = plt.text(0.5, 0.05, r"$z_{n+1} = z_n^2 + c$", color='white',
                       horizontalalignment='center', verticalalignment='center',
                       transform=ax.transAxes, fontsize=12)
    
    depth_counter = plt.text(0.95, 0.05, "Zoom: 1x", color='white',
                            horizontalalignment='right', verticalalignment='center',
                            transform=ax.transAxes, fontsize=10)
    
    info_text = plt.text(0.5, 0.88, "Infinite Complexity from Simple Rules", 
                        color='white', alpha=0, horizontalalignment='center',
                        verticalalignment='center', transform=ax.transAxes, fontsize=10)
    
    coordinates = plt.text(0.5, 0.10, f"Coordinates: ({target_x:.6f}, {target_y:.6f})", 
                          color='white', alpha=0, horizontalalignment='center',
                          verticalalignment='center', transform=ax.transAxes, fontsize=8)
    
    # ScienceInMotion branding
    watermark = plt.text(0.95, 0.95, "ScienceInMotion", color='white', alpha=0.7,
                         horizontalalignment='right', verticalalignment='center',
                         transform=ax.transAxes, fontsize=8)
    
    def update(frame):
        """Update function for each frame of the animation."""
        nonlocal img
        
        # Calculate normalized progress
        progress = frame / frames
        
        # Get precalculated zoom values
        current_width, zoom_ratio = zoom_values[frame]
        
        # Generate the Mandelbrot set for the current zoom level
        mandelbrot_data = mandelbrot_numpy(height, width, max_iterations, 
                                         target_x, target_y, current_width)
        
        # Update the image data
        img.set_data(smooth_color(mandelbrot_data, max_iterations))
        
        # Update the zoom counter text
        depth_counter.set_text(f"Zoom: {zoom_ratio:.1f}x")
        
        # Handle text animations based on progress
        if progress < 0.1:  # Intro
            # Fade in title and equation
            alpha = min(1.0, progress / 0.05)
            title.set_alpha(alpha)
            equation.set_alpha(alpha)
            watermark.set_alpha(alpha * 0.7)
            info_text.set_alpha(0)
            coordinates.set_alpha(0)
        
        elif 0.3 < progress < 0.5:  # Show info text
            info_alpha = min(1.0, (progress - 0.3) * 5)
            info_text.set_alpha(info_alpha)
            coordinates.set_alpha(0)
        
        elif 0.5 < progress < 0.7:  # Fade out info text, show coordinates
            info_alpha = max(0, 1.0 - (progress - 0.5) * 5)
            coord_alpha = min(1.0, (progress - 0.5) * 5)
            info_text.set_alpha(info_alpha)
            coordinates.set_alpha(coord_alpha)
        
        elif 0.7 < progress < 0.9:  # Show coordinates
            info_text.set_alpha(0)
            coordinates.set_alpha(1.0)
        
        elif progress > 0.9:  # Outro - fade out coordinates
            coord_alpha = max(0, 1.0 - (progress - 0.9) * 10)
            coordinates.set_alpha(coord_alpha)
        
        return img, title, equation, depth_counter, info_text, coordinates, watermark
    
    # Create the animation
    print(f"Creating animation with {frames} frames at {fps} fps...")
    anim = animation.FuncAnimation(fig, update, frames=frames, interval=1000/fps, blit=True)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the animation
    output_file = os.path.join(output_dir, "mandelbrot_zoom.mp4")
    print(f"Saving animation to {output_file}...")
    
    # Lower bitrate for faster encoding
    writer = animation.FFMpegWriter(fps=fps, metadata=dict(artist='ScienceInMotion'), bitrate=2000)
    anim.save(output_file, writer=writer)
    
    print(f"Mandelbrot zoom animation saved to '{output_file}'")
    
    # Print file size for verification
    file_size = os.path.getsize(output_file) / (1024 * 1024)  # Size in MB
    print(f"File size: {file_size:.2f} MB")

def main():
    create_mandelbrot_animation()

if __name__ == "__main__":
    main() 