import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import os
from matplotlib import rcParams

# Set high DPI value for better quality
rcParams['figure.dpi'] = 150

def create_trig_functions_animation(output_dir="output"):
    """
    Creates an animation showing how sine, cosine, and tangent waves are generated from circular motion.
    The animation shows a point moving around a circle and traces all three waves in separate subplots.
    """
    print("Creating Trigonometric Functions Animation...")
    
    # Animation parameters
    fps = 60
    duration = 15  # 15 seconds total
    frames = fps * duration
    
    # Set up figure with 3 vertically stacked subplots (16:9 aspect ratio)
    fig = plt.figure(figsize=(12, 20), facecolor='black')
    
    # Create gridspec for custom layout
    gs = fig.add_gridspec(4, 1, height_ratios=[1, 1, 1, 0.2])
    
    # Create subplots
    ax_sine = fig.add_subplot(gs[0])
    ax_cosine = fig.add_subplot(gs[1])
    ax_tangent = fig.add_subplot(gs[2])
    ax_info = fig.add_subplot(gs[3])
    
    axes = [ax_sine, ax_cosine, ax_tangent, ax_info]
    for ax in axes:
        ax.set_facecolor('black')
        ax.set_xlim(-2.3, 4*np.pi)
        
    # Set y-limits for each plot
    ax_sine.set_ylim(-1.5, 1.5)
    ax_cosine.set_ylim(-1.5, 1.5)
    ax_tangent.set_ylim(-3, 3)  # Tangent has wider range
    ax_info.set_ylim(-1, 1)
    
    # Set equal aspect ratio to ensure circles appear as circles
    ax_sine.set_aspect('equal', adjustable='box')
    ax_cosine.set_aspect('equal', adjustable='box')
    ax_tangent.set_aspect('equal', adjustable='box')
    
    # Turn off all axes
    for ax in axes:
        ax.axis('off')
    
    # Create circle in each subplot
    circle_sine = Circle((-1, 0), 1, fill=False, color='#00AAFF', lw=2)
    circle_cosine = Circle((-1, 0), 1, fill=False, color='#FF9500', lw=2)
    circle_tangent = Circle((-1, 0), 1, fill=False, color='#FF00FF', lw=2)
    
    ax_sine.add_patch(circle_sine)
    ax_cosine.add_patch(circle_cosine)
    ax_tangent.add_patch(circle_tangent)
    
    # Create horizontal and vertical axes in each subplot
    for ax in [ax_sine, ax_cosine, ax_tangent]:
        ax.axhline(y=0, color='gray', linestyle='-', alpha=0.4, lw=1)
        ax.axvline(x=0, color='gray', linestyle='-', alpha=0.4, lw=1)
    
    # X-axis markings (π, 2π, 3π, 4π) for each subplot
    for ax in [ax_sine, ax_cosine, ax_tangent]:
        for i, label in enumerate(['π', '2π', '3π', '4π']):
            x = (i + 1) * np.pi
            ax.plot([x, x], [-0.1, 0.1], 'gray', lw=1)
            ax.text(x, -0.3, label, color='white', ha='center', fontsize=10)
    
    # Create points on circles
    point_on_circle_sine, = ax_sine.plot([], [], 'o', color='white', ms=10)
    point_on_circle_cosine, = ax_cosine.plot([], [], 'o', color='white', ms=10)
    point_on_circle_tangent, = ax_tangent.plot([], [], 'o', color='white', ms=10)
    
    # Create projection lines
    # Sine
    sine_projection, = ax_sine.plot([], [], '--', color='#00AAFF', alpha=0.6, lw=1.5)
    sine_connecting_line, = ax_sine.plot([], [], '--', color='#00AAFF', alpha=0.6, lw=1.5)
    sine_wave, = ax_sine.plot([], [], '-', color='#00AAFF', lw=3)
    point_on_sine, = ax_sine.plot([], [], 'o', color='#00AAFF', ms=10)
    
    # Cosine
    cosine_projection, = ax_cosine.plot([], [], '--', color='#FF9500', alpha=0.6, lw=1.5)
    cosine_connecting_line, = ax_cosine.plot([], [], '--', color='#FF9500', alpha=0.6, lw=1.5)
    cosine_wave, = ax_cosine.plot([], [], '-', color='#FF9500', lw=3)
    point_on_cosine, = ax_cosine.plot([], [], 'o', color='#FF9500', ms=10)
    
    # Tangent
    tangent_projection1, = ax_tangent.plot([], [], '--', color='#FF00FF', alpha=0.6, lw=1.5)
    tangent_projection2, = ax_tangent.plot([], [], '--', color='#FF00FF', alpha=0.6, lw=1.5)
    tangent_connecting_line, = ax_tangent.plot([], [], '--', color='#FF00FF', alpha=0.6, lw=1.5)
    tangent_wave, = ax_tangent.plot([], [], '-', color='#FF00FF', lw=3)
    point_on_tangent, = ax_tangent.plot([], [], 'o', color='#FF00FF', ms=10)
    
    # Create tangent line on the circle
    tangent_line, = ax_tangent.plot([], [], '-', color='#FF00FF', lw=1.5, alpha=0.7)
    
    # Labels for each wave
    sine_label = ax_sine.text(4*np.pi-0.5, 1.2, "SINE", color='#00AAFF', fontsize=18, 
                             weight='bold', ha='right')
    cosine_label = ax_cosine.text(4*np.pi-0.5, 1.2, "COSINE", color='#FF9500', fontsize=18, 
                                weight='bold', ha='right')
    tangent_label = ax_tangent.text(4*np.pi-0.5, 2.7, "TANGENT", color='#FF00FF', fontsize=18, 
                                   weight='bold', ha='right')
    
    # Equations for each function
    eq_sine = ax_sine.text(3*np.pi, -1.2, "y = sin(θ)", color='#00AAFF', fontsize=14, 
                         ha='center', style='italic')
    eq_cosine = ax_cosine.text(3*np.pi, -1.2, "y = cos(θ)", color='#FF9500', fontsize=14, 
                            ha='center', style='italic')
    eq_tangent = ax_tangent.text(3*np.pi, -2.7, "y = tan(θ)", color='#FF00FF', fontsize=14, 
                               ha='center', style='italic')
    
    # Add main title
    title = ax_info.text(2*np.pi, 0.6, "TRIGONOMETRIC FUNCTIONS", 
                        fontsize=28, color='white', ha='center', 
                        weight='bold')
    
    subtitle = ax_info.text(2*np.pi, 0, "FROM CIRCULAR MOTION", 
                          fontsize=18, color='white', ha='center', alpha=0.9,
                          weight='bold')
    
    # Add watermark
    watermark = ax_info.text(2*np.pi, -0.6, "@Science_In_Motion", 
                           fontsize=14, color='#00FFFF', ha='center', alpha=0.9,
                           style='italic', weight='bold')
    
    # Create data arrays
    t_points = np.linspace(0, 0, 1000)
    sine_points = np.sin(t_points)
    cosine_points = np.cos(t_points)
    tangent_points = np.tan(t_points)
    
    # To avoid plotting tangent at discontinuities
    tangent_mask = np.abs(tangent_points) < 10
    
    def init():
        """Initialize animation"""
        # Initialize all plot elements
        point_on_circle_sine.set_data([], [])
        point_on_circle_cosine.set_data([], [])
        point_on_circle_tangent.set_data([], [])
        
        sine_projection.set_data([], [])
        sine_connecting_line.set_data([], [])
        sine_wave.set_data([], [])
        point_on_sine.set_data([], [])
        
        cosine_projection.set_data([], [])
        cosine_connecting_line.set_data([], [])
        cosine_wave.set_data([], [])
        point_on_cosine.set_data([], [])
        
        tangent_projection1.set_data([], [])
        tangent_projection2.set_data([], [])
        tangent_connecting_line.set_data([], [])
        tangent_wave.set_data([], [])
        point_on_tangent.set_data([], [])
        tangent_line.set_data([], [])
        
        return (point_on_circle_sine, sine_projection, sine_connecting_line, sine_wave, point_on_sine,
                point_on_circle_cosine, cosine_projection, cosine_connecting_line, cosine_wave, point_on_cosine,
                point_on_circle_tangent, tangent_projection1, tangent_projection2, tangent_connecting_line, 
                tangent_wave, point_on_tangent, tangent_line)
    
    def update(frame):
        """Update animation for each frame"""
        t = 4 * np.pi * frame / frames
        
        # Calculate position on circle
        x = -1 + np.cos(t)  # -1 is the x-center of circle
        y = np.sin(t)
        
        # Calculate tangent value and tangent line
        tangent_val = np.tan(t)
        
        # Limit tangent value for display (prevent extreme values)
        display_tangent = np.clip(tangent_val, -3, 3)
        
        # Update points on circles
        point_on_circle_sine.set_data([x], [y])
        point_on_circle_cosine.set_data([x], [y])
        point_on_circle_tangent.set_data([x], [y])
        
        # Update SINE projection and wave
        sine_projection.set_data([x, 0], [y, y])
        sine_connecting_line.set_data([0, t], [y, y])
        
        # Update COSINE projection and wave
        cosine_projection.set_data([x, x], [y, 0])
        cosine_connecting_line.set_data([0, t], [x+1, x+1])
        
        # Create tangent line on the circle (tangent to the point)
        radius = 1
        # Tangent line extends from the point on circle
        if abs(tangent_val) < 100:  # Avoid extreme cases
            tangent_length = 0.5
            tangent_dx = tangent_length / np.sqrt(1 + tangent_val**2)
            tangent_dy = tangent_val * tangent_dx
            tangent_line.set_data([x - tangent_dx, x + tangent_dx], [y - tangent_dy, y + tangent_dy])
        else:
            tangent_line.set_data([], [])
        
        # Update TANGENT projection and wave
        # Tangent point is where a line from origin meets the tangent line to the circle
        tangent_x = -1 + radius / np.cos(t) if abs(np.cos(t)) > 0.01 else -1 + 100*radius
        tangent_projection1.set_data([x, -1], [y, 0])  # Line from point to origin
        tangent_projection2.set_data([-1, tangent_x], [0, 0])  # Line from origin along x axis
        tangent_connecting_line.set_data([0, t], [display_tangent, display_tangent])
        
        # Update waves
        max_t = max(4 * np.pi, t)
        t_points = np.linspace(0, max_t, 1000)
        mask = t_points <= t
        
        sine_points = np.sin(t_points)
        cosine_points = np.cos(t_points)
        tangent_points = np.tan(t_points)
        
        # Mask out tangent discontinuities
        tangent_mask = np.abs(tangent_points) < 10
        masked_tangent = np.ma.masked_array(tangent_points, ~tangent_mask)
        
        sine_wave.set_data(t_points[mask], sine_points[mask])
        cosine_wave.set_data(t_points[mask], cosine_points[mask])
        tangent_wave.set_data(t_points[mask & tangent_mask], masked_tangent[mask & tangent_mask])
        
        # Update points on waves
        point_on_sine.set_data([t], [y])           # y = sin(t)
        point_on_cosine.set_data([t], [x+1])       # y = cos(t)
        point_on_tangent.set_data([t], [display_tangent])  # y = tan(t) (clipped)
        
        return (point_on_circle_sine, sine_projection, sine_connecting_line, sine_wave, point_on_sine,
                point_on_circle_cosine, cosine_projection, cosine_connecting_line, cosine_wave, point_on_cosine,
                point_on_circle_tangent, tangent_projection1, tangent_projection2, tangent_connecting_line, 
                tangent_wave, point_on_tangent, tangent_line)
    
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
    output_file = os.path.join(output_dir, 'trig_functions_circle.mp4')
    print(f"Saving animation to {output_file}...")
    
    try:
        writer = animation.FFMpegWriter(fps=fps, metadata=dict(artist='Science_In_Motion'),
                                      bitrate=2400, codec="h264",
                                      extra_args=['-pix_fmt', 'yuv420p'])
        ani.save(output_file, writer=writer)
        print(f"Trig functions animation saved to '{output_file}'")
    except (RuntimeError, FileNotFoundError) as e:
        print("ffmpeg not found. Saving as GIF instead...")
        gif_file = os.path.join(output_dir, 'trig_functions_circle.gif')
        ani.save(gif_file, writer='pillow', fps=fps)
        print(f"Trig functions animation saved as GIF to '{gif_file}'")
        
        file_size_bytes = os.path.getsize(gif_file)
        file_size_mb = file_size_bytes / (1024 * 1024)
        print(f"File size: {file_size_mb:.2f} MB")
    
    plt.close(fig)

if __name__ == "__main__":
    create_trig_functions_animation() 