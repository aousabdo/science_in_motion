import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import os
from matplotlib import rcParams

# Set high DPI value for better quality
rcParams['figure.dpi'] = 150

def create_sine_cosine_circle_animation(output_dir="output"):
    """
    Creates an animation showing how sine and cosine waves are generated from circular motion.
    The animation shows a point moving around a circle and traces both waves simultaneously.
    """
    print("Creating Sine/Cosine Circle Animation...")
    
    # Animation parameters
    fps = 60
    duration = 15  # 15 seconds total
    frames = fps * duration
    
    # Set up figure (9:16 aspect ratio for TikTok)
    fig = plt.figure(figsize=(6, 10.67), facecolor='black')
    ax = fig.add_subplot(111)
    
    # Configure axes
    ax.set_facecolor('black')
    ax.set_xlim(-2.3, 4*np.pi)
    ax.set_ylim(-3, 3)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Create circle - position it near the left side of the plot
    circle = Circle((-1, 0), 1, fill=False, color='#00AAFF', lw=2)
    ax.add_patch(circle)
    
    # Create horizontal and vertical axes
    ax.axhline(y=0, color='gray', linestyle='-', alpha=0.4, lw=1)
    ax.axvline(x=0, color='gray', linestyle='-', alpha=0.4, lw=1)
    
    # X-axis markings (π, 2π, 3π, 4π)
    for i, label in enumerate(['π', '2π', '3π', '4π']):
        x = (i + 1) * np.pi
        ax.plot([x, x], [-0.1, 0.1], 'gray', lw=1)
        ax.text(x, -0.5, label, color='white', ha='center', fontsize=10)
    
    # Create point on circle
    point_on_circle, = ax.plot([], [], 'o', color='white', ms=10)
    
    # Create horizontal and vertical lines from point to axes
    horizontal_line, = ax.plot([], [], '--', color='#00FFFF', alpha=0.6, lw=1.5)
    vertical_line, = ax.plot([], [], '--', color='#FF9500', alpha=0.6, lw=1.5)
    
    # Create lines connecting point to right side for sine and cosine
    sine_connecting_line, = ax.plot([], [], '--', color='#00FFFF', alpha=0.6, lw=1.5)
    cosine_connecting_line, = ax.plot([], [], '--', color='#FF9500', alpha=0.6, lw=1.5)
    
    # Create sine and cosine waves
    sine_wave, = ax.plot([], [], '-', color='#00FFFF', lw=3)
    cosine_wave, = ax.plot([], [], '-', color='#FF9500', lw=3)
    
    # Create points on sine and cosine waves
    point_on_sine, = ax.plot([], [], 'o', color='#00FFFF', ms=10)
    point_on_cosine, = ax.plot([], [], 'o', color='#FF9500', ms=10)
    
    # Labels for sine and cosine with arrows
    sine_label = ax.text(0.8, 1.8, "SINE", color='#00FFFF', fontsize=18, 
                         weight='bold', ha='center')
    cosine_label = ax.text(0.8, -1.8, "COSINE", color='#FF9500', fontsize=18, 
                           weight='bold', ha='center')
    
    # Add title - more eye-catching with glow effect
    for offset in [(0.03, 0.03), (-0.03, -0.03), (0.03, -0.03), (-0.03, 0.03)]:
        glow = ax.text(2*np.pi+offset[0], 4.8+offset[1], "SIN & COS", 
                       fontsize=28, color='#333333', ha='center', 
                       weight='bold', alpha=0.3)
    
    title = ax.text(2*np.pi, 4.8, "SIN & COS", 
                    fontsize=28, color='white', ha='center', 
                    weight='bold')
    
    # Add small subtitle
    subtitle = ax.text(2*np.pi, 4., "FROM CIRCLES", 
                      fontsize=18, color='white', ha='center', alpha=0.9,
                      weight='bold')
    
    # Add equations
    eq_sine = ax.text(3*np.pi, 1.5, "y = sin(θ)", color='#00FFFF', fontsize=14, 
                     ha='center', style='italic')
    eq_cosine = ax.text(3*np.pi, -1.7, "y = cos(θ)", color='#FF9500', fontsize=14, 
                       ha='center', style='italic')
                       
    # Add watermark
    watermark = ax.text(2*np.pi, -3.8, "@Science_In_Motion", 
                       fontsize=14, color='#FF00FF', ha='center', alpha=0.9,
                       style='italic', weight='bold')
    
    # Create data arrays
    t_points = np.linspace(0, 0, 1000)
    sine_points = np.sin(t_points)
    cosine_points = np.cos(t_points)
    
    def init():
        """Initialize animation"""
        point_on_circle.set_data([], [])
        horizontal_line.set_data([], [])
        vertical_line.set_data([], [])
        sine_connecting_line.set_data([], [])
        cosine_connecting_line.set_data([], [])
        sine_wave.set_data([], [])
        cosine_wave.set_data([], [])
        point_on_sine.set_data([], [])
        point_on_cosine.set_data([], [])
        return (point_on_circle, horizontal_line, vertical_line, 
                sine_connecting_line, cosine_connecting_line,
                sine_wave, cosine_wave, point_on_sine, point_on_cosine,
                title, subtitle, sine_label, cosine_label, eq_sine, eq_cosine, watermark)
    
    def update(frame):
        """Update animation for each frame"""
        t = 4 * np.pi * frame / frames
        
        # Calculate position on circle
        x = -1 + np.cos(t)  # -1 is the x-center of circle
        y = np.sin(t)
        
        # Update point on circle
        point_on_circle.set_data([x], [y])
        
        # Update horizontal line (for sine wave projection)
        horizontal_line.set_data([x, 0], [y, y])
        
        # Update vertical line (for cosine wave projection)
        vertical_line.set_data([x, x], [y, 0])
        
        # Update connecting lines to right side
        sine_connecting_line.set_data([0, t], [y, y])    # Sine uses y-coordinate
        cosine_connecting_line.set_data([0, t], [x+1, x+1])  # Cosine uses x-coordinate (shifted)
        
        # Update sine and cosine waves
        max_t = max(4 * np.pi, t)
        t_points = np.linspace(0, max_t, 1000)
        mask = t_points <= t
        sine_points = np.sin(t_points)
        cosine_points = np.cos(t_points)
        sine_wave.set_data(t_points[mask], sine_points[mask])
        cosine_wave.set_data(t_points[mask], cosine_points[mask])
        
        # Update points on waves
        point_on_sine.set_data([t], [y])             # y = sin(t)
        point_on_cosine.set_data([t], [x+1])         # x+1 = cos(t)
        
        return (point_on_circle, horizontal_line, vertical_line, 
                sine_connecting_line, cosine_connecting_line,
                sine_wave, cosine_wave, point_on_sine, point_on_cosine,
                title, subtitle, sine_label, cosine_label, eq_sine, eq_cosine, watermark)
    
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
    output_file = os.path.join(output_dir, 'sine_cosine_circle.mp4')
    print(f"Saving animation to {output_file}...")
    
    try:
        writer = animation.FFMpegWriter(fps=fps, metadata=dict(artist='Me'),
                                      bitrate=1800, codec="h264",
                                      extra_args=['-pix_fmt', 'yuv420p'])
        ani.save(output_file, writer=writer)
        print(f"Sine cosine animation saved to '{output_file}'")
    except (RuntimeError, FileNotFoundError) as e:
        print("ffmpeg not found. Saving as GIF instead...")
        gif_file = os.path.join(output_dir, 'sine_cosine_circle.gif')
        ani.save(gif_file, writer='pillow', fps=fps)
        print(f"Sine cosine animation saved as GIF to '{gif_file}'")
        
        file_size_bytes = os.path.getsize(gif_file)
        file_size_mb = file_size_bytes / (1024 * 1024)
        print(f"File size: {file_size_mb:.2f} MB")
    
    plt.close(fig)

if __name__ == "__main__":
    create_sine_cosine_circle_animation() 