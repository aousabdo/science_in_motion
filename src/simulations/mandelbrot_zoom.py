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
    # Calculate the height based on the width and aspect ratio
    zoom_height = zoom_width * h / w
    
    # Calculate the boundaries of the view
    x_min = center_x - zoom_width/2
    x_max = center_x + zoom_width/2
    y_min = center_y - zoom_height/2
    y_max = center_y + zoom_height/2
    
    # Create coordinate arrays
    x = np.linspace(x_min, x_max, w)
    y = np.linspace(y_min, y_max, h)
    
    # Result array - initialized to max_iters (will be black)
    result = np.zeros((h, w), dtype=np.float32)
    
    # For each pixel
    for i in range(h):
        for j in range(w):
            c = complex(x[j], y[i])
            z = 0.0
            for k in range(max_iters):
                z = z*z + c
                if (z.real*z.real + z.imag*z.imag) >= 4.0:
                    # Apply smooth coloring formula
                    result[i, j] = k + 1 - np.log(np.log(abs(z))) / np.log(2)
                    break
    
    return result

def create_color_palette():
    """Create a vibrant color palette suited for the Mandelbrot visualization."""
    colors = [
        (0, 0, 0.2),     # Start with dark blue instead of black
        (0.1, 0.1, 0.3),  # Dark purple
        (0.2, 0, 0.5),   # Purple
        (0.3, 0, 0.8),   # Deep purple
        (0, 0.2, 1),     # Blue
        (0, 0.5, 1),     # Sky blue
        (0, 0.8, 1),     # Light blue
        (0, 1, 0.8),     # Teal
        (0, 1, 0.5),     # Sea green
        (0, 1, 0),       # Green
        (0.5, 1, 0),     # Lime
        (0.8, 1, 0),     # Yellow-green
        (1, 1, 0),       # Yellow
        (1, 0.8, 0),     # Gold
        (1, 0.5, 0),     # Orange
        (1, 0.2, 0),     # Red-orange
        (1, 0, 0),       # Red
        (1, 0, 0.5),     # Pink
        (1, 0, 0.8),     # Magenta
        (0.8, 0, 1),     # Purple
        (0.5, 0, 0.8),   # Violet
        (0.3, 0, 0.5),   # Dark purple
        (0, 0, 0.2)      # Back to dark blue (cycle)
    ]
    
    return LinearSegmentedColormap.from_list('mandelbrot', colors, N=512)

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
    
    # Animation parameters
    fps = 30
    duration = 30  # extended to 30 seconds as requested
    frames = fps * duration
    
    # Mandelbrot calculation parameters - reduced resolution for faster processing
    width, height = 360, 640  # reduced resolution for faster processing
    max_iterations = 200  # increased for more detail during deep zoom
    
    # Interesting zoom target coordinates - changed to mini-brot with spirals
    # This location shows intricate details throughout the zoom
    target_x = -0.743643887037151
    target_y = 0.131825904205330
    
    # Zoom parameters
    start_zoom = 3.5  # start further out to see the whole set
    end_zoom = 0.000005  # adjusted to see interesting patterns throughout
    
    # Calculate zoom sequence
    zoom_values = []
    zoom_widths = np.geomspace(start_zoom, end_zoom, frames)
    
    for frame in range(frames):
        zoom_width = zoom_widths[frame]
        zoom_ratio = start_zoom / zoom_width
        zoom_values.append((zoom_width, zoom_ratio))
    
    # Set up figure and axis
    plt.rcParams['figure.dpi'] = 100
    fig = plt.figure(figsize=(3.6, 6.4), facecolor='black')
    ax = fig.add_subplot(111)
    ax.set_position([0, 0, 1, 1])  # Fill the entire figure
    ax.set_facecolor('black')
    
    # Remove ticks and labels
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Create color palette
    cmap = create_color_palette()
    
    # Generate an initial Mandelbrot set for the starting frame
    print("Generating initial frame...")
    initial_data = mandelbrot_numpy(height, width, max_iterations, 
                                  target_x, target_y, start_zoom)
    
    # Initial image - use a logarithmic normalization to enhance color contrast
    img = ax.imshow(initial_data, cmap=cmap, 
                   interpolation='bilinear',
                   norm=plt.Normalize(0, max_iterations))
    
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
    
    # Progress information
    print("Ready to generate animation frames")
    
    def update(frame):
        """Update function for each frame of the animation."""
        nonlocal img
        
        if frame % 10 == 0:
            print(f"Processing frame {frame+1}/{frames}...")
        
        # Calculate normalized progress
        progress = frame / frames
        
        # Get precalculated zoom values
        zoom_width, zoom_ratio = zoom_values[frame]
        
        # Generate the Mandelbrot set for the current zoom level
        mandelbrot_data = mandelbrot_numpy(height, width, max_iterations, 
                                         target_x, target_y, zoom_width)
        
        # Update the image data
        img.set_data(mandelbrot_data)
        
        # Update the zoom counter text
        depth_counter.set_text(f"Zoom: {zoom_ratio:.1f}x")
        
        # Handle text animations based on progress
        if progress < 0.05:  # Intro - shorter to allow more zoom time
            # Fade in title and equation
            alpha = min(1.0, progress / 0.025)
            title.set_alpha(alpha)
            equation.set_alpha(alpha)
            watermark.set_alpha(alpha * 0.7)
            info_text.set_alpha(0)
            coordinates.set_alpha(0)
        
        elif 0.15 < progress < 0.25:  # Show info text
            info_alpha = min(1.0, (progress - 0.15) * 10)
            info_text.set_alpha(info_alpha)
            coordinates.set_alpha(0)
        
        elif 0.25 < progress < 0.35:  # Fade out info text, show coordinates
            info_alpha = max(0, 1.0 - (progress - 0.25) * 10)
            coord_alpha = min(1.0, (progress - 0.25) * 10)
            info_text.set_alpha(info_alpha)
            coordinates.set_alpha(coord_alpha)
        
        elif 0.35 < progress < 0.9:  # Show coordinates for longer during zoom
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
    
    # Higher bitrate for better quality
    writer = animation.FFMpegWriter(fps=fps, metadata=dict(artist='ScienceInMotion'), bitrate=3500)
    anim.save(output_file, writer=writer)
    
    print(f"Mandelbrot zoom animation saved to '{output_file}'")
    
    # Print file size for verification
    file_size = os.path.getsize(output_file) / (1024 * 1024)  # Size in MB
    print(f"File size: {file_size:.2f} MB")

def main():
    create_mandelbrot_animation()

if __name__ == "__main__":
    main() 