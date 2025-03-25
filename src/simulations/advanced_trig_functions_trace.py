import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import os
from matplotlib import rcParams

# Set high DPI value for better quality
rcParams['figure.dpi'] = 150

def create_advanced_trig_functions_animation(output_dir="output"):
    """
    Creates an animation showing how secant, cosecant, and cotangent waves are generated from circular motion.
    The animation shows a point moving around a circle and traces all three waves in separate subplots.
    """
    print("Creating Advanced Trigonometric Functions Animation...")
    
    # Animation parameters
    fps = 60
    duration = 15  # 15 seconds total
    frames = fps * duration
    
    # Set up figure with 3 vertically stacked subplots (16:9 aspect ratio)
    fig = plt.figure(figsize=(12, 20), facecolor='black')
    
    # Create gridspec for custom layout
    gs = fig.add_gridspec(4, 1, height_ratios=[1, 1, 1, 0.2])
    
    # Create subplots
    ax_secant = fig.add_subplot(gs[0])
    ax_cosecant = fig.add_subplot(gs[1])
    ax_cotangent = fig.add_subplot(gs[2])
    ax_info = fig.add_subplot(gs[3])
    
    axes = [ax_secant, ax_cosecant, ax_cotangent, ax_info]
    for ax in axes:
        ax.set_facecolor('black')
        ax.set_xlim(-2.3, 4*np.pi)
        
    # Set y-limits for each plot (these reciprocal functions have wider ranges)
    ax_secant.set_ylim(-5, 5)
    ax_cosecant.set_ylim(-5, 5)
    ax_cotangent.set_ylim(-5, 5)
    ax_info.set_ylim(-1, 1)
    
    # Set equal aspect ratio to ensure circles appear as circles
    ax_secant.set_aspect('equal', adjustable='box')
    ax_cosecant.set_aspect('equal', adjustable='box')
    ax_cotangent.set_aspect('equal', adjustable='box')
    
    # Turn off all axes
    for ax in axes:
        ax.axis('off')
    
    # Create circle in each subplot
    circle_secant = Circle((-1, 0), 1, fill=False, color='#22FFAA', lw=2)
    circle_cosecant = Circle((-1, 0), 1, fill=False, color='#FF22AA', lw=2)
    circle_cotangent = Circle((-1, 0), 1, fill=False, color='#AAFF22', lw=2)
    
    ax_secant.add_patch(circle_secant)
    ax_cosecant.add_patch(circle_cosecant)
    ax_cotangent.add_patch(circle_cotangent)
    
    # Create horizontal and vertical axes in each subplot
    for ax in [ax_secant, ax_cosecant, ax_cotangent]:
        ax.axhline(y=0, color='gray', linestyle='-', alpha=0.4, lw=1)
        ax.axvline(x=0, color='gray', linestyle='-', alpha=0.4, lw=1)
    
    # X-axis markings (π, 2π, 3π, 4π) for each subplot
    for ax in [ax_secant, ax_cosecant, ax_cotangent]:
        for i, label in enumerate(['π', '2π', '3π', '4π']):
            x = (i + 1) * np.pi
            ax.plot([x, x], [-0.1, 0.1], 'gray', lw=1)
            ax.text(x, -0.3, label, color='white', ha='center', fontsize=10)
    
    # Create points on circles
    point_on_circle_secant, = ax_secant.plot([], [], 'o', color='white', ms=10)
    point_on_circle_cosecant, = ax_cosecant.plot([], [], 'o', color='white', ms=10)
    point_on_circle_cotangent, = ax_cotangent.plot([], [], 'o', color='white', ms=10)
    
    # Create projection and connection lines for each function
    # SECANT
    secant_x_line, = ax_secant.plot([], [], '--', color='#22FFAA', alpha=0.6, lw=1.5)
    secant_extension, = ax_secant.plot([], [], '--', color='#22FFAA', alpha=0.6, lw=1.5)
    secant_connecting_line, = ax_secant.plot([], [], '--', color='#22FFAA', alpha=0.6, lw=1.5)
    secant_wave, = ax_secant.plot([], [], '-', color='#22FFAA', lw=3)
    point_on_secant, = ax_secant.plot([], [], 'o', color='#22FFAA', ms=10)
    
    # COSECANT
    cosecant_y_line, = ax_cosecant.plot([], [], '--', color='#FF22AA', alpha=0.6, lw=1.5)
    cosecant_extension, = ax_cosecant.plot([], [], '--', color='#FF22AA', alpha=0.6, lw=1.5)
    cosecant_connecting_line, = ax_cosecant.plot([], [], '--', color='#FF22AA', alpha=0.6, lw=1.5)
    cosecant_wave, = ax_cosecant.plot([], [], '-', color='#FF22AA', lw=3)
    point_on_cosecant, = ax_cosecant.plot([], [], 'o', color='#FF22AA', ms=10)
    
    # COTANGENT
    cotangent_tangent_line, = ax_cotangent.plot([], [], '--', color='#AAFF22', alpha=0.6, lw=1.5)
    cotangent_extension, = ax_cotangent.plot([], [], '--', color='#AAFF22', alpha=0.6, lw=1.5)
    cotangent_connecting_line, = ax_cotangent.plot([], [], '--', color='#AAFF22', alpha=0.6, lw=1.5)
    cotangent_wave, = ax_cotangent.plot([], [], '-', color='#AAFF22', lw=3)
    point_on_cotangent, = ax_cotangent.plot([], [], 'o', color='#AAFF22', ms=10)
    
    # Add unit circle radius lines to help visualize the relationships
    secant_radius, = ax_secant.plot([], [], '-', color='white', alpha=0.3, lw=1)
    cosecant_radius, = ax_cosecant.plot([], [], '-', color='white', alpha=0.3, lw=1)
    cotangent_radius, = ax_cotangent.plot([], [], '-', color='white', alpha=0.3, lw=1)
    
    # Labels for each wave
    secant_label = ax_secant.text(4*np.pi-0.5, 4.2, "SECANT", color='#22FFAA', fontsize=18, 
                                 weight='bold', ha='right')
    cosecant_label = ax_cosecant.text(4*np.pi-0.5, 4.2, "COSECANT", color='#FF22AA', fontsize=18, 
                                    weight='bold', ha='right')
    cotangent_label = ax_cotangent.text(4*np.pi-0.5, 4.2, "COTANGENT", color='#AAFF22', fontsize=18, 
                                      weight='bold', ha='right')
    
    # Equations for each function
    eq_secant = ax_secant.text(3*np.pi, -4.5, "y = sec(θ) = 1/cos(θ)", color='#22FFAA', fontsize=14, 
                             ha='center', style='italic')
    eq_cosecant = ax_cosecant.text(3*np.pi, -4.5, "y = csc(θ) = 1/sin(θ)", color='#FF22AA', fontsize=14, 
                                ha='center', style='italic')
    eq_cotangent = ax_cotangent.text(3*np.pi, -4.5, "y = cot(θ) = 1/tan(θ)", color='#AAFF22', fontsize=14, 
                                   ha='center', style='italic')
    
    # Add main title
    title = ax_info.text(2*np.pi, 0.6, "ADVANCED TRIGONOMETRIC FUNCTIONS", 
                        fontsize=24, color='white', ha='center', 
                        weight='bold')
    
    subtitle = ax_info.text(2*np.pi, 0, "FROM CIRCULAR MOTION", 
                          fontsize=18, color='white', ha='center', alpha=0.9,
                          weight='bold')
    
    # Add watermark
    watermark = ax_info.text(2*np.pi, -0.6, "@Science_In_Motion", 
                           fontsize=14, color='#00FFFF', ha='center', alpha=0.9,
                           style='italic', weight='bold')
    
    # Create data arrays with initial values
    t_points = np.linspace(0, 0, 1000)
    
    # Initialize empty arrays to avoid runtime errors
    secant_points = np.ones_like(t_points)
    cosecant_points = np.ones_like(t_points)
    cotangent_points = np.ones_like(t_points)
    
    def init():
        """Initialize animation"""
        # Initialize all plot elements
        point_on_circle_secant.set_data([], [])
        point_on_circle_cosecant.set_data([], [])
        point_on_circle_cotangent.set_data([], [])
        
        secant_x_line.set_data([], [])
        secant_extension.set_data([], [])
        secant_connecting_line.set_data([], [])
        secant_wave.set_data([], [])
        point_on_secant.set_data([], [])
        secant_radius.set_data([], [])
        
        cosecant_y_line.set_data([], [])
        cosecant_extension.set_data([], [])
        cosecant_connecting_line.set_data([], [])
        cosecant_wave.set_data([], [])
        point_on_cosecant.set_data([], [])
        cosecant_radius.set_data([], [])
        
        cotangent_tangent_line.set_data([], [])
        cotangent_extension.set_data([], [])
        cotangent_connecting_line.set_data([], [])
        cotangent_wave.set_data([], [])
        point_on_cotangent.set_data([], [])
        cotangent_radius.set_data([], [])
        
        return (point_on_circle_secant, secant_x_line, secant_extension, secant_connecting_line, 
                secant_wave, point_on_secant, secant_radius,
                point_on_circle_cosecant, cosecant_y_line, cosecant_extension, cosecant_connecting_line, 
                cosecant_wave, point_on_cosecant, cosecant_radius,
                point_on_circle_cotangent, cotangent_tangent_line, cotangent_extension, 
                cotangent_connecting_line, cotangent_wave, point_on_cotangent, cotangent_radius)
    
    def update(frame):
        """Update animation for each frame"""
        t = 4 * np.pi * frame / frames
        
        # Calculate position on circle
        x = -1 + np.cos(t)  # -1 is the x-center of circle
        y = np.sin(t)
        
        # Update points on circles
        point_on_circle_secant.set_data([x], [y])
        point_on_circle_cosecant.set_data([x], [y])
        point_on_circle_cotangent.set_data([x], [y])
        
        # Draw radius lines
        secant_radius.set_data([-1, x], [0, y])
        cosecant_radius.set_data([-1, x], [0, y])
        cotangent_radius.set_data([-1, x], [0, y])
        
        # Calculate values for each function (with safeguards for discontinuities)
        # For secant (1/cos(t))
        if abs(np.cos(t)) > 0.01:
            secant_val = 1 / np.cos(t)
        else:
            # Near discontinuity points
            secant_val = np.sign(np.cos(t)) * 100
            
        # For cosecant (1/sin(t))
        if abs(np.sin(t)) > 0.01:
            cosecant_val = 1 / np.sin(t)
        else:
            # Near discontinuity points
            cosecant_val = np.sign(np.sin(t)) * 100
            
        # For cotangent (1/tan(t) or cos(t)/sin(t))
        if abs(np.sin(t)) > 0.01:
            cotangent_val = np.cos(t) / np.sin(t)
        else:
            # Near discontinuity points
            cotangent_val = np.sign(np.cos(t)) * 100
            
        # Limit display values for better visualization
        display_secant = np.clip(secant_val, -5, 5)
        display_cosecant = np.clip(cosecant_val, -5, 5)
        display_cotangent = np.clip(cotangent_val, -5, 5)
        
        # SECANT visualization
        # Drawing x-axis projection and extension to secant value
        secant_x_line.set_data([x, x], [y, 0])  # Vertical line to x-axis
        
        # Extension to secant value (handle display):
        # For normal values
        if abs(secant_val) < 10:
            # Extension along x-axis to the secant value
            secant_extension.set_data([x, -1 + secant_val], [0, 0])
            secant_connecting_line.set_data([0, t], [display_secant, display_secant])
        else:
            # For near discontinuities, don't draw the line
            secant_extension.set_data([], [])
            secant_connecting_line.set_data([], [])
        
        # COSECANT visualization
        # Drawing y-axis projection and extension
        cosecant_y_line.set_data([x, 0], [y, y])  # Horizontal line to y-axis
        
        # Extension to cosecant value (handle display):
        if abs(cosecant_val) < 10:
            # Extension along y-axis to the cosecant value
            cosecant_extension.set_data([0, 0], [y, cosecant_val])
            cosecant_connecting_line.set_data([0, t], [display_cosecant, display_cosecant])
        else:
            # For near discontinuities, don't draw the line
            cosecant_extension.set_data([], [])
            cosecant_connecting_line.set_data([], [])
        
        # COTANGENT visualization
        # We need to draw a line from the circle point to the y-axis that has slope = cotangent
        
        # First draw the tangent line at the point on circle
        if abs(cotangent_val) < 10:
            # For normal values, draw the cotangent line and extensions
            # Drawing a cotangent line through the point on circle
            
            # Extend a line with cotangent slope
            dx = 0.5  # Small offset
            dy = dx * cotangent_val
            
            cotangent_tangent_line.set_data([x - dx, x + dx], [y - dy, y + dy])
            
            # Extension from origin at angle t to where it meets the x-axis
            if abs(np.sin(t)) > 0.01:
                # Find where the line from origin at angle t meets the y-axis
                # This is the cotangent value on the y-axis
                cotangent_extension.set_data([0, 0], [0, cotangent_val])
                cotangent_connecting_line.set_data([0, t], [display_cotangent, display_cotangent])
            else:
                cotangent_extension.set_data([], [])
                cotangent_connecting_line.set_data([], [])
        else:
            # For near discontinuities, don't draw the lines
            cotangent_tangent_line.set_data([], [])
            cotangent_extension.set_data([], [])
            cotangent_connecting_line.set_data([], [])
        
        # Update waves
        max_t = max(4 * np.pi, t)
        t_points = np.linspace(0, max_t, 1000)
        mask = t_points <= t
        
        # Compute trig values with protection against discontinuities
        secant_points = np.zeros_like(t_points)
        cosecant_points = np.zeros_like(t_points)
        cotangent_points = np.zeros_like(t_points)
        
        # Compute values carefully to avoid divide-by-zero issues
        for i, angle in enumerate(t_points):
            # Secant
            if abs(np.cos(angle)) > 0.01:
                secant_points[i] = 1 / np.cos(angle)
            else:
                secant_points[i] = np.sign(np.cos(angle)) * 100 if np.cos(angle) != 0 else 100
                
            # Cosecant
            if abs(np.sin(angle)) > 0.01:
                cosecant_points[i] = 1 / np.sin(angle)
            else:
                cosecant_points[i] = np.sign(np.sin(angle)) * 100 if np.sin(angle) != 0 else 100
                
            # Cotangent
            if abs(np.sin(angle)) > 0.01:
                cotangent_points[i] = np.cos(angle) / np.sin(angle)
            else:
                cotangent_points[i] = np.sign(np.cos(angle)) * 100 if np.cos(angle) != 0 else 100
        
        # Create masks for discontinuities
        secant_mask = np.abs(secant_points) < 10
        cosecant_mask = np.abs(cosecant_points) < 10
        cotangent_mask = np.abs(cotangent_points) < 10
        
        # Clip values for display
        secant_points = np.clip(secant_points, -5, 5)
        cosecant_points = np.clip(cosecant_points, -5, 5)
        cotangent_points = np.clip(cotangent_points, -5, 5)
        
        # Apply masks to handle discontinuities in the plots
        masked_secant = np.ma.masked_array(secant_points, ~secant_mask)
        masked_cosecant = np.ma.masked_array(cosecant_points, ~cosecant_mask)
        masked_cotangent = np.ma.masked_array(cotangent_points, ~cotangent_mask)
        
        # Update the wave plots
        secant_wave.set_data(t_points[mask & secant_mask], masked_secant[mask & secant_mask])
        cosecant_wave.set_data(t_points[mask & cosecant_mask], masked_cosecant[mask & cosecant_mask])
        cotangent_wave.set_data(t_points[mask & cotangent_mask], masked_cotangent[mask & cotangent_mask])
        
        # Update points on waves
        point_on_secant.set_data([t], [display_secant])
        point_on_cosecant.set_data([t], [display_cosecant])
        point_on_cotangent.set_data([t], [display_cotangent])
        
        return (point_on_circle_secant, secant_x_line, secant_extension, secant_connecting_line, 
                secant_wave, point_on_secant, secant_radius,
                point_on_circle_cosecant, cosecant_y_line, cosecant_extension, cosecant_connecting_line, 
                cosecant_wave, point_on_cosecant, cosecant_radius,
                point_on_circle_cotangent, cotangent_tangent_line, cotangent_extension, 
                cotangent_connecting_line, cotangent_wave, point_on_cotangent, cotangent_radius)
    
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
    output_file = os.path.join(output_dir, 'advanced_trig_functions.mp4')
    print(f"Saving animation to {output_file}...")
    
    try:
        writer = animation.FFMpegWriter(fps=fps, metadata=dict(artist='Science_In_Motion'),
                                      bitrate=2400, codec="h264",
                                      extra_args=['-pix_fmt', 'yuv420p'])
        ani.save(output_file, writer=writer)
        print(f"Advanced trig functions animation saved to '{output_file}'")
    except (RuntimeError, FileNotFoundError) as e:
        print("ffmpeg not found. Saving as GIF instead...")
        gif_file = os.path.join(output_dir, 'advanced_trig_functions.gif')
        ani.save(gif_file, writer='pillow', fps=fps)
        print(f"Advanced trig functions animation saved as GIF to '{gif_file}'")
        
        file_size_bytes = os.path.getsize(gif_file)
        file_size_mb = file_size_bytes / (1024 * 1024)
        print(f"File size: {file_size_mb:.2f} MB")
    
    plt.close(fig)

if __name__ == "__main__":
    create_advanced_trig_functions_animation() 