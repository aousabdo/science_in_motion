import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import os
from matplotlib import rcParams

# Set high DPI value for better quality
rcParams['figure.dpi'] = 150

def create_sine_circle_trace_animation(output_dir="output"):
    """
    Creates an animation showing how a sine wave is generated from circular motion.
    The animation shows a point moving around a circle and traces the sine wave
    as the y-coordinate of the point is plotted against the angle.
    """
    print("Creating Sine Circle Trace Animation...")
    
    # Animation parameters
    fps = 30
    duration = 15  # 15 seconds total
    frames = fps * duration
    
    # Set up figure (9:16 aspect ratio for TikTok)
    fig = plt.figure(figsize=(6, 10.67), facecolor='black')
    ax = fig.add_subplot(111)
    
    # Configure axes
    ax.set_facecolor('black')
    ax.set_xlim(-6, 6)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Create circle
    circle = Circle((0, 0), 1, fill=False, color='white', lw=1.5)
    ax.add_patch(circle)
    
    # Create horizontal and vertical axes
    ax.axhline(y=0, color='gray', linestyle='-', alpha=0.7, lw=1)
    ax.axvline(x=0, color='gray', linestyle='-', alpha=0.7, lw=1)
    
    # X-axis markings (π, 2π, 3π, 4π)
    for i, label in enumerate(['π', '2π', '3π', '4π']):
        x = (i + 1) * np.pi
        ax.plot([x, x], [-0.1, 0.1], 'gray', lw=1)
        ax.text(x, -0.3, label, color='white', ha='center', fontsize=12)
    
    # Create point on circle
    point_on_circle, = ax.plot([], [], 'o', color='cyan', ms=8)
    
    # Create horizontal line from point to axis
    horizontal_line, = ax.plot([], [], '--', color='cyan', alpha=0.5, lw=1)
    
    # Create line connecting point to right side
    connecting_line, = ax.plot([], [], '--', color='cyan', alpha=0.5, lw=1)
    
    # Create sine wave
    sine_wave, = ax.plot([], [], '-', color='cyan', lw=2)
    
    # Create point on sine wave
    point_on_sine, = ax.plot([], [], 'o', color='#FF00FF', ms=8)
    
    # Add title
    title = ax.text(0, 2.7, "How a Sine Wave is Generated", 
                    fontsize=18, color='white', ha='center', fontname='DejaVu Serif')
    
    # Add subtitle
    subtitle = ax.text(0, 2.3, "From Circular Motion", 
                      fontsize=14, color='white', ha='center', fontname='DejaVu Serif')
    
    # Add watermark
    watermark = ax.text(0, -2.7, "@ScienceInMotion", 
                       fontsize=14, color='#FF00FF', ha='center', alpha=0.7)
    
    # Create data arrays
    t_points = np.linspace(0, 0, 1000)
    sine_points = np.sin(t_points)
    
    def init():
        """Initialize animation"""
        point_on_circle.set_data([], [])
        horizontal_line.set_data([], [])
        sine_wave.set_data([], [])
        connecting_line.set_data([], [])
        point_on_sine.set_data([], [])
        return (point_on_circle, horizontal_line, sine_wave, 
                connecting_line, point_on_sine, title, subtitle, watermark)
    
    def update(frame):
        """Update animation for each frame"""
        t = 2 * np.pi * frame / frames
        
        # Calculate position on circle
        x = np.cos(t)
        y = np.sin(t)
        
        # Update point on circle
        point_on_circle.set_data([x], [y])
        
        # Update horizontal line
        horizontal_line.set_data([x, 0], [y, y])
        
        # Update connecting line to right side
        connecting_line.set_data([0, t], [y, y])
        
        # Update sine wave
        max_t = max(2 * np.pi, t)
        t_points = np.linspace(0, max_t, 1000)
        mask = t_points <= t
        sine_points = np.sin(t_points)
        sine_wave.set_data(t_points[mask], sine_points[mask])
        
        # Update point on sine wave
        point_on_sine.set_data([t], [y])
        
        return (point_on_circle, horizontal_line, sine_wave, 
                connecting_line, point_on_sine, title, subtitle, watermark)
    
    # Create animation
    ani = animation.FuncAnimation(
        fig,
        update,
        frames=frames,
        init_func=init,
        blit=True,
        interval=1000/fps
    )
    
    # Save animation
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'sine_circle_trace.mp4')
    print(f"Saving animation to {output_file}...")
    
    try:
        writer = animation.FFMpegWriter(fps=fps, metadata=dict(artist='Me'),
                                      bitrate=1800, codec="h264",
                                      extra_args=['-pix_fmt', 'yuv420p'])
        ani.save(output_file, writer=writer)
        print(f"Sine circle trace animation saved to '{output_file}'")
    except (RuntimeError, FileNotFoundError) as e:
        print("ffmpeg not found. Saving as GIF instead...")
        gif_file = os.path.join(output_dir, 'sine_circle_trace.gif')
        ani.save(gif_file, writer='pillow', fps=fps)
        print(f"Sine circle trace animation saved as GIF to '{gif_file}'")
        
        file_size_bytes = os.path.getsize(gif_file)
        file_size_mb = file_size_bytes / (1024 * 1024)
        print(f"File size: {file_size_mb:.2f} MB")
    
    plt.close(fig)

if __name__ == "__main__":
    create_sine_circle_trace_animation() 