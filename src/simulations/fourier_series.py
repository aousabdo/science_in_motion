import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import os
from matplotlib import rcParams

# Set high DPI value for better quality
rcParams['figure.dpi'] = 150

def create_fourier_visualization(output_dir="output", n_terms=8):
    """
    Creates a visualization of Fourier series approximating a square wave,
    optimized for TikTok's portrait format.
    
    This visualization shows how circles of different radii rotating at
    different frequencies can be combined to create a square wave.
    
    Parameters:
    -----------
    output_dir : str
        Directory where output files will be saved
    n_terms : int
        Number of terms in the Fourier series
    """
    print("Creating Fourier Series Visualization...")
    
    # Animation parameters
    fps = 30
    duration = 30  # 30 seconds total
    frames = fps * duration
    
    # Set up figure (9:16 aspect ratio for TikTok)
    fig = plt.figure(figsize=(6, 10.67), facecolor='black')
    
    # Create axes for vector representation and function plot
    ax_vectors = fig.add_axes([0, 0.45, 1, 0.55])  # Top half for vectors
    ax_func = fig.add_axes([0, 0, 1, 0.45])  # Bottom half for function
    
    # Configure axes
    for ax in [ax_vectors, ax_func]:
        ax.set_facecolor('black')
        ax.grid(color='gray', alpha=0.3)
        ax.set_xlim(-5, 5)
        ax.set_ylim(-3, 3)
        ax.xaxis.set_visible(True)
        ax.yaxis.set_visible(True)
        ax.tick_params(colors='white', which='both')
        
        # Make coordinate arrows more visible
        ax.spines['left'].set_color('white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_linewidth(1.2)
        ax.spines['bottom'].set_linewidth(1.2)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        
        # Add arrows to the axes
        ax.plot(1.05*ax.get_xlim()[1], 0, '>k', transform=ax.transData, color='white', markersize=8)
        ax.plot(0, 1.05*ax.get_ylim()[1], '^k', transform=ax.transData, color='white', markersize=8)

    # For the function plot, configure x-axis with π marks
    ax_func.set_xlim(0, 4*np.pi)
    ax_func.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi, 5*np.pi/2, 3*np.pi, 7*np.pi/2, 4*np.pi])
    ax_func.set_xticklabels(['0', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$', 
                             r'$\frac{5\pi}{2}$', r'$3\pi$', r'$\frac{7\pi}{2}$', r'$4\pi$'])
    ax_func.set_yticks([-1, 0, 1])
    
    # Add a red horizontal line at y=0 in the function plot
    ax_func.axhline(y=0, color='red', alpha=0.7, lw=1.5)
    
    # Calculate coefficients for square wave Fourier series
    # f(x) = 4/π * Σ 1/(2n-1) * sin((2n-1)x) for n from 1 to ∞
    def fourier_term(n, x):
        return 4/(np.pi * (2*n-1)) * np.sin((2*n-1) * x)
    
    # Function to compute the square wave approximation with n terms
    def fourier_approx(x, n_terms):
        result = np.zeros_like(x)
        for n in range(1, n_terms+1):
            result += fourier_term(n, x)
        return result
    
    # Function to compute the exact square wave
    def square_wave(x):
        result = np.zeros_like(x)
        for i, val in enumerate(x):
            if val % (2*np.pi) < np.pi:
                result[i] = 1
            else:
                result[i] = -1
        return result
    
    # Create vibrant colors for each term
    colors = [
        'cyan',      # 1st term (large circle)
        'yellow',    # 2nd term
        'magenta',   # 3rd term
        'lime',      # 4th term
        'orange',    # 5th term
        'pink',      # 6th term
        'white',     # 7th term
        'aqua',      # 8th term
        'gold',      # 9th term (if needed)
        'violet',    # 10th term (if needed)
        'greenyellow', # 11th term (if needed)
        'coral'      # 12th term (if needed)
    ]
    
    # Initialize circles for visualization
    circles = []
    lines = []
    dots = []
    
    for i in range(n_terms):
        # Create circle
        circle = Circle((0, 0), 0, fill=False, color=colors[i], lw=1.5, alpha=0.8)
        ax_vectors.add_patch(circle)
        circles.append(circle)
        
        # Create line for vector inside the circle
        line, = ax_vectors.plot([], [], color=colors[i], lw=1.5)
        lines.append(line)
        
        # Create dot for the tip of the vector
        dot, = ax_vectors.plot([], [], 'o', color=colors[i], markersize=6)
        dots.append(dot)
    
    # Line to connect all vector tips
    connector, = ax_vectors.plot([], [], 'w-', lw=1, alpha=0.5)
    
    # Path traced by the final dot
    path, = ax_func.plot([], [], 'w-', lw=2)
    
    # Dot tracing the function
    trace_dot, = ax_func.plot([], [], 'o', color='white', markersize=6)
    
    # Text equations
    eq1 = fig.text(0.5, 0.27, r"$f(x) = \frac{4}{\pi}\sum_{n=1}^{\infty}\frac{1}{(2n-1)}\sin((2n-1)x)$", 
                  color='white', fontsize=12, ha='center')
    
    eq2 = fig.text(0.5, 0.22, r"$f(x) = \begin{cases} -1, & -\pi < x < 0; \\ 0, & x = 0, -\pi, \pi \\ 1, & 0 < x < \pi. \end{cases}$", 
                  color='white', fontsize=12, ha='center')
    
    # Watermark
    watermark = fig.text(0.5, 0.17, "@ScienceInMotion", 
                        color='magenta', fontsize=14, ha='center', alpha=0.7)
    
    # Animation variables
    x_data = np.linspace(0, 0, 1000)  # Initialize with zeros, will be updated
    y_data = np.zeros_like(x_data)
    time_stretch = 8.0  # How many cycles to go through during animation
    
    # For Fourier animation
    def init():
        """Initialize animation"""
        for circle in circles:
            circle.center = (0, 0)
            circle.radius = 0
        
        for line in lines:
            line.set_data([], [])
        
        for dot in dots:
            dot.set_data([], [])
        
        connector.set_data([], [])
        path.set_data([], [])
        trace_dot.set_data([], [])
        
        return circles + lines + dots + [connector, path, trace_dot]
    
    def update(frame):
        """Update animation for each frame"""
        frame_norm = frame / frames  # Normalized frame (0 to 1)
        
        # Text opacity based on animation phase
        if frame_norm < 0.05:  # Fade in
            alpha = frame_norm / 0.05
            eq1.set_alpha(alpha)
            eq2.set_alpha(alpha)
            watermark.set_alpha(alpha * 0.7)
        elif frame_norm > 0.95:  # Fade out
            alpha = (1 - (frame_norm - 0.95) / 0.05)
            eq1.set_alpha(alpha)
            eq2.set_alpha(alpha)
            watermark.set_alpha(alpha * 0.7)
        else:
            eq1.set_alpha(1.0)
            eq2.set_alpha(1.0)
            watermark.set_alpha(0.7)
        
        # Calculate the current time for this frame
        t = frame_norm * time_stretch * 2 * np.pi
        
        # Calculate positions for each vector (circle)
        prev_x, prev_y = 0, 0  # Starting position
        connector_x, connector_y = [prev_x], [prev_y]  # For the connector line
        
        # Phase-in for the circles
        visible_terms = min(n_terms, int(n_terms * min(1.0, frame_norm * 2.5)) + 1)
        
        for i in range(visible_terms):
            n = i + 1
            
            # Calculate radius and frequency for this term
            radius = 4 / (np.pi * (2*n-1))
            freq = 2*n-1
            
            # Set the circle properties
            circles[i].center = (prev_x, prev_y)
            circles[i].radius = radius
            
            # Calculate tip of the vector for this frequency
            x = prev_x + radius * np.cos(freq * t)
            y = prev_y + radius * np.sin(freq * t)
            
            # Update the line showing the vector
            lines[i].set_data([prev_x, x], [prev_y, y])
            
            # Update the dot at the tip of the vector
            dots[i].set_data([x], [y])
            
            # Save for the next circle's starting point
            prev_x, prev_y = x, y
            
            # Add to connector line
            connector_x.append(x)
            connector_y.append(y)
        
        # Set invisible circles and vectors for terms not yet shown
        for i in range(visible_terms, n_terms):
            circles[i].center = (0, 0)
            circles[i].radius = 0
            lines[i].set_data([], [])
            dots[i].set_data([], [])
        
        # Update the connector line
        connector.set_data(connector_x, connector_y)
        
        # Update the function trace
        # Calculate the x positions for the trace (representing time)
        x_data = np.linspace(0, t, 1000)
        
        # Only keep points within our x-axis range
        mask = x_data <= 4*np.pi
        x_plot = x_data[mask]
        
        # Calculate the y values using our Fourier approximation with visible_terms
        y_plot = fourier_approx(x_plot, visible_terms)
        
        # Update the path
        path.set_data(x_plot, y_plot)
        
        # Update the trace dot
        trace_dot.set_data([t % (4*np.pi)], [prev_y])
        
        # Return all updated elements
        return circles + lines + dots + [connector, path, trace_dot, eq1, eq2, watermark]
    
    # Create animation
    ani = animation.FuncAnimation(
        fig,
        update,
        frames=frames,
        init_func=init,
        blit=True,
        interval=1000/fps
    )
    
    # 7. Save Animation
    # -----------------------------
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'fourier_series.mp4')
    print(f"Saving animation to {output_file}...")
    
    try:
        # Try to use ffmpeg for MP4
        writer = animation.FFMpegWriter(fps=fps, metadata=dict(artist='Me'), 
                                       bitrate=1800, codec="h264", 
                                       extra_args=['-pix_fmt', 'yuv420p'])
        ani.save(output_file, writer=writer)
        print(f"Fourier series animation saved to '{output_file}'")
    except (RuntimeError, FileNotFoundError) as e:
        # Fallback to GIF if ffmpeg is not available
        print("ffmpeg not found. Saving as GIF instead...")
        gif_file = os.path.join(output_dir, 'fourier_series.gif')
        ani.save(gif_file, writer='pillow', fps=fps)
        print(f"Fourier series animation saved as GIF to '{gif_file}'")
        
        # Get file size information
        file_size_bytes = os.path.getsize(gif_file)
        file_size_mb = file_size_bytes / (1024 * 1024)
        print(f"File size: {file_size_mb:.2f} MB")
    
    plt.close(fig)

def main():
    create_fourier_visualization()

if __name__ == "__main__":
    main()