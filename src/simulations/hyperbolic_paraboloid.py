import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import os

def create_hyperbolic_paraboloid(output_dir="output"):
    """
    Creates a rotating 3D animation of a hyperbolic paraboloid (Pringle shape)
    with custom styling to match the reference.
    """
    # Create figure and 3D axis
    fig = plt.figure(figsize=(10, 12), facecolor='black')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    
    # Remove ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    
    # Set axis limits
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    
    # Set axis lines color to white
    ax.xaxis.line.set_color('white')
    ax.yaxis.line.set_color('white')
    ax.zaxis.line.set_color('white')
    
    # Display coordinate axes with white color and ticks
    ax.xaxis.set_pane_color((0, 0, 0, 0))
    ax.yaxis.set_pane_color((0, 0, 0, 0))
    ax.zaxis.set_pane_color((0, 0, 0, 0))
    
    # Draw 3D coordinate axes through the shape
    # X-axis
    ax.plot([-1, 1], [0, 0], [0, 0], color='white', linewidth=1.0)
    # Y-axis
    ax.plot([0, 0], [-1, 1], [0, 0], color='white', linewidth=1.0)
    # Z-axis
    ax.plot([0, 0], [0, 0], [-1, 1], color='white', linewidth=1.0)
    
    # Add small tick marks along the axes
    for tick in np.linspace(-0.8, 0.8, 5):
        if tick != 0:  # Skip the origin
            # Tick on x-axis
            ax.plot([tick, tick], [0, 0], [0, -0.03], color='white', linewidth=0.8)
            # Tick on y-axis
            ax.plot([0, 0], [tick, tick], [0, -0.03], color='white', linewidth=0.8)
            # Tick on z-axis
            ax.plot([0, 0.03], [0, 0], [tick, tick], color='white', linewidth=0.8)
    
    # Add grid on the bottom reference plane
    for tick in np.linspace(-1, 1, 5):
        if tick != 0:  # Skip the center to avoid overlapping with axes
            ax.plot([-1, 1], [tick, tick], [-0.9, -0.9], color='white', alpha=0.2, linestyle='-', linewidth=0.5)
            ax.plot([tick, tick], [-1, 1], [-0.9, -0.9], color='white', alpha=0.2, linestyle='-', linewidth=0.5)
    
    # Make axis scale equal for proportional shape
    ax.set_box_aspect([1, 1, 1])
    
    # Generate hyperbolic paraboloid data
    a, b = 1, 1
    u = np.linspace(-0.8, 0.8, 40)  # Increased resolution
    v = np.linspace(-0.8, 0.8, 40)
    u, v = np.meshgrid(u, v)
    
    # Using the equation from the image: z = x²/a² - y²/b²
    x = u
    y = v
    z = (x**2/a**2) - (y**2/b**2)
    
    # Create the surface
    surface = ax.plot_surface(
        x, y, z,
        cmap=cm.YlOrBr_r,  # Yellow to brown colormap
        linewidth=0.5,
        edgecolor='#444444',
        alpha=0.9,
        rstride=1,
        cstride=1
    )
    
    # Add title
    title = fig.text(0.5, 0.92, 'Pringle', fontsize=36, color='yellow', 
                    horizontalalignment='center', weight='bold')
    
    # Draw a line under the title
    fig.text(0.5, 0.89, '_____________', fontsize=24, color='yellow', 
            horizontalalignment='center')
    
    # Add equations with proper LaTeX formatting
    fig.text(0.5, 0.17, 'x = u', fontsize=22, color='yellow', 
            horizontalalignment='center')
    fig.text(0.5, 0.13, 'y = v', fontsize=22, color='yellow', 
            horizontalalignment='center')
    
    # Use proper LaTeX formatting for the fraction
    equation = r'$z = \frac{x^2}{a^2} - \frac{y^2}{b^2}$'
    fig.text(0.5, 0.09, equation, fontsize=22, color='yellow', 
            horizontalalignment='center')
    
    # Add signature
    fig.text(0.5, 0.03, '@maths.1089', fontsize=16, color='#777777', 
            horizontalalignment='center')
    
    # Initial view angle
    elev = 28
    azim = 0
    
    # Animation function for rotation
    def update(frame):
        nonlocal azim
        # Update viewing angle - rotate around z-axis (change azimuth)
        azim = frame * 2  # Speed of rotation
        ax.view_init(elev, azim)
        return [surface]
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Number of frames - 180 for a full 360° rotation (each frame = 2°)
    frames = 180
    
    # Create animation
    ani = animation.FuncAnimation(
        fig, 
        update, 
        frames=frames, 
        interval=50,
        blit=False
    )
    
    # Save animation as MP4
    output_file = os.path.join(output_dir, 'hyperbolic_paraboloid.mp4')
    writer = animation.FFMpegWriter(fps=30, metadata=dict(artist='Science_In_Motion'),
                                  bitrate=2400, codec="h264",
                                  extra_args=['-pix_fmt', 'yuv420p'])
    ani.save(output_file, writer=writer)
    print(f"Hyperbolic paraboloid animation saved to '{output_file}'")
    
    plt.close(fig)

if __name__ == "__main__":
    create_hyperbolic_paraboloid() 