import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib

# Set backend to TkAgg for better compatibility
matplotlib.use('TkAgg')

def create_lorenz_animation():
    """
    Creates a visually striking animation of the Lorenz attractor
    optimized for TikTok (30 seconds long). This version fixes the
    color array issue and is more robust.
    """
    
    # -----------------------------
    # 1. Lorenz System Parameters
    # -----------------------------
    sigma = 10.0
    rho = 28.0
    beta = 8.0 / 3.0
    
    # -----------------------------
    # 2. Simulation Setup
    # -----------------------------
    dt = 0.01  # Time step
    num_steps = 8000  # More points for smoother animation
    
    # Arrays for storing points
    xs = np.zeros(num_steps)
    ys = np.zeros(num_steps)
    zs = np.zeros(num_steps)
    
    # Set initial point
    xs[0], ys[0], zs[0] = 0.1, 0.0, 0.0
    
    # Integrate using Euler method
    print("Generating Lorenz attractor points...")
    for i in range(1, num_steps):
        x, y, z = xs[i-1], ys[i-1], zs[i-1]
        
        # The Lorenz equations
        dx = sigma * (y - x) * dt
        dy = (x * (rho - z) - y) * dt
        dz = (x * y - beta * z) * dt
        
        # Update the position
        xs[i] = x + dx
        ys[i] = y + dy
        zs[i] = z + dz
    
    print(f"Generated {num_steps} points.")
    
    # -----------------------------
    # 3. Prepare Figure (9:16 ratio)
    # -----------------------------
    fig = plt.figure(figsize=(4.5, 8), facecolor='black')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    
    # Set axis limits
    x_min, x_max = np.min(xs), np.max(xs)
    y_min, y_max = np.min(ys), np.max(ys)
    z_min, z_max = np.min(zs), np.max(zs)
    
    padding = 2
    ax.set_xlim(x_min - padding, x_max + padding)
    ax.set_ylim(y_min - padding, y_max + padding)
    ax.set_zlim(z_min - padding, z_max + padding)
    
    # Remove axis labels and ticks
    ax.set_axis_off()
    
    # -----------------------------
    # 4. Prepare Animation Elements
    # -----------------------------
    # Line for attractor path - using blue to magenta gradient
    line, = ax.plot([], [], [], lw=2, color='cyan')
    
    # Current point marker
    point, = ax.plot([], [], [], 'o', markersize=6, color='white')
    
    # Define our beautiful colors - array of fixed colors to avoid the dynamic coloring issue
    colors = [
        (0.6, 0, 0.6, 1),     # Purple 
        (0.4, 0, 0.8, 1),     # Deep purple
        (0, 0.5, 1, 1),       # Blue
        (0, 0.8, 1, 1),       # Cyan
        (0, 1, 1, 1)          # Bright cyan
    ]
    
    # Title
    title_text = ax.text2D(0.5, 0.95, 
                          "Lorenz Attractor", 
                          transform=ax.transAxes,
                          color='white', fontsize=14, ha='center')
    
    # Subtitle - appears after a few seconds
    subtitle_text = ax.text2D(0.5, 0.85,
                             "Chaos Theory Visualization",
                             transform=ax.transAxes,
                             color='white', fontsize=10, ha='center', alpha=0)
    
    # Equations
    eq_text = ax.text2D(0.5, 0.05,
                       r"$\dot{x} = 10(y-x)$"
                       "\n"
                       r"$\dot{y} = x(28-z)-y$"
                       "\n"
                       r"$\dot{z} = xy-\frac{8}{3}z$",
                       transform=ax.transAxes,
                       color='white', fontsize=10, ha='center')
    
    # ScienceInMotion branding
    watermark = ax.text2D(0.95, 0.05, 
                         "ScienceInMotion", 
                         transform=ax.transAxes,
                         color='white', fontsize=8, ha='right', alpha=0.7)
    
    # -----------------------------
    # 5. Animation Functions
    # -----------------------------
    def init():
        """Initialize animation"""
        line.set_data([], [])
        line.set_3d_properties([])
        point.set_data([], [])
        point.set_3d_properties([])
        return line, point, title_text, subtitle_text, eq_text, watermark
    
    def update(frame):
        """Update function for each frame"""
        # Parameters for a 30-second animation
        fps = 30
        total_seconds = 30
        total_frames = fps * total_seconds
        
        # Calculate normalized progress (0.0 to 1.0)
        progress = frame / total_frames
        
        # Calculate the number of points to show based on progress
        if progress < 0.05:  # First 5% - intro
            # Just show the starting point
            point.set_data([xs[0]], [ys[0]])
            point.set_3d_properties([zs[0]])
            
            # Fade in title and equation
            alpha = progress / 0.05
            title_text.set_alpha(alpha)
            eq_text.set_alpha(alpha)
            watermark.set_alpha(alpha * 0.7)
            
            # No line yet
            line.set_data([], [])
            line.set_3d_properties([])
            
        elif progress < 0.95:  # Main animation (90% of time)
            # Scale the animation progress from 0-1 over the main phase
            main_progress = (progress - 0.05) / 0.9
            
            # Calculate which segment of the path to show
            i = int(main_progress * num_steps)
            i = max(1, min(i, num_steps - 1))  # Ensure i is between 1 and num_steps-1
            
            # Show subtitle during middle part of animation
            if 0.3 < main_progress < 0.7:
                subtitle_alpha = min(1.0, (main_progress - 0.3) * 5)
                if main_progress > 0.6:
                    subtitle_alpha = max(0, (0.7 - main_progress) * 10)
                subtitle_text.set_alpha(subtitle_alpha)
            else:
                subtitle_text.set_alpha(0)
            
            # Make text fully visible
            title_text.set_alpha(1.0)
            eq_text.set_alpha(1.0)
            watermark.set_alpha(0.7)
            
            # Update line data - simple approach that always works
            line.set_data(xs[:i], ys[:i])
            line.set_3d_properties(zs[:i])
            
            # Use one of our fixed colors based on progress
            color_idx = int(main_progress * (len(colors) - 1))
            color_idx = min(color_idx, len(colors) - 1)
            line.set_color(colors[color_idx])
            
            # Update point position
            point.set_data([xs[i-1]], [ys[i-1]])
            point.set_3d_properties([zs[i-1]])
            
            # Rotate view for 3D effect
            elevation = 20 + 10 * np.sin(main_progress * 6)
            azimuth = 30 + 180 * main_progress
            ax.view_init(elev=elevation, azim=azimuth)
            
        else:  # Final 5% - outro
            # Fade out everything
            fade = max(0, 1.0 - (progress - 0.95) / 0.05)
            
            # Keep showing the full path
            line.set_data(xs, ys)
            line.set_3d_properties(zs)
            line.set_alpha(fade)
            line.set_color(colors[-1])  # Use the final color
            
            # Keep point at the end
            point.set_data([xs[-1]], [ys[-1]])
            point.set_3d_properties([zs[-1]])
            point.set_alpha(fade)
            
            # Fade out text
            title_text.set_alpha(fade)
            eq_text.set_alpha(fade)
            watermark.set_alpha(fade * 0.7)
            subtitle_text.set_alpha(0)  # Already faded out
            
            # Keep camera position steady
            ax.view_init(elev=30, azim=210)
        
        return line, point, title_text, subtitle_text, eq_text, watermark
    
    # -----------------------------
    # 6. Create Animation
    # -----------------------------
    fps = 30
    duration = 30  # seconds
    frames = fps * duration
    
    print(f"Creating animation with {frames} frames at {fps} fps...")
    ani = animation.FuncAnimation(
        fig, 
        update, 
        frames=frames,
        init_func=init,
        interval=1000/fps,
        blit=True
    )
    
    # -----------------------------
    # 7. Save Animation
    # -----------------------------
    output_file = "lorenz_attractor_tiktok.mp4"
    print(f"Saving animation to {output_file}...")
    
    writer = animation.FFMpegWriter(
        fps=fps, 
        metadata=dict(artist='ScienceInMotion'),
        bitrate=2000
    )
    
    ani.save(output_file, writer=writer)
    print(f"Animation saved to '{output_file}'")
    
    # Print file size for verification
    import os
    file_size = os.path.getsize(output_file) / 1024  # Size in KB
    print(f"File size: {file_size:.2f} KB")

def main():
    create_lorenz_animation()

if __name__ == "__main__":
    main()