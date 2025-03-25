import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, Path, PathPatch
import os

def create_projectile_challenge(output_dir="output"):
    """
    Creates a simulation challenge where students need to determine the correct angle
    to launch a projectile to hit a target on a hill.
    """
    # Animation parameters
    fps = 30
    duration = 10
    frames = fps * duration
    
    # Physics parameters - use these in the challenge
    g = 9.8  # gravity (m/s²)
    initial_velocity = 20  # m/s
    start_height = 5  # m
    target_x = 30  # m
    target_y = 12  # m
    target_size = 2  # m
    
    # Slope calculation
    slope = 0.3
    slope_angle = np.degrees(np.arctan(slope))
    
    # Setup figure
    fig, ax = plt.subplots(figsize=(12, 8), facecolor='black')
    ax.set_facecolor('#001122')
    ax.set_xlim(0, 40)
    ax.set_ylim(0, 25)
    
    # Draw ground with hill
    x_ground = np.linspace(0, 40, 100)
    y_ground = 3 + x_ground * slope
    ground = ax.fill_between(x_ground, 0, y_ground, color='#355522')
    
    # Draw launch platform
    platform = Rectangle((2, y_ground[5]), 4, start_height, color='#555555')
    ax.add_patch(platform)
    
    # Draw target
    target = Rectangle((target_x-target_size/2, target_y-target_size/2), target_size, target_size, color='#FF3333')
    ax.add_patch(target)
    
    # Trajectory path
    trajectory = Path([(0, 0)], [Path.MOVETO])
    path_patch = PathPatch(trajectory, color='#FFFF00', lw=2, fill=False)
    ax.add_patch(path_patch)
    
    # Projectile point
    projectile, = ax.plot([], [], 'o', color='white', ms=8)
    
    # Add info text
    title = ax.text(20, 23, "PROJECTILE CHALLENGE", fontsize=24, color='white', ha='center', weight='bold')
    instruction = ax.text(20, 20, "Find the launch angle to hit the target!", fontsize=16, color='#AAAAFF', ha='center')
    physics_info = ax.text(5, 18, f"Initial velocity: {initial_velocity} m/s\nGravity: {g} m/s²\nSlope angle: {slope_angle:.1f}°", 
                         fontsize=12, color='#CCCCCC', ha='left')
    
    # Target info
    target_info = ax.text(target_x, target_y+2, f"Target", fontsize=10, color='#FF5555', ha='center')
    
    # Angle indicator
    angle_text = ax.text(6, start_height + y_ground[5] + 2, "?°", color='#FFFF00', fontsize=16)
    angle_line, = ax.plot([], [], '-', color='#FFFF00', lw=2, alpha=0.7)
    
    # Function to calculate trajectory
    def trajectory_path(angle_deg, steps=100):
        angle_rad = np.radians(angle_deg)
        vx = initial_velocity * np.cos(angle_rad)
        vy = initial_velocity * np.sin(angle_rad)
        
        # Calculate time of flight (with solution checking)
        # This deliberately avoids giving away the answer
        max_t = 2 * vy / g * 2  # Extended time to show misses
        
        t = np.linspace(0, max_t, steps)
        x = 4 + vx * t  # Start from platform x position
        y = y_ground[5] + start_height + vy * t - 0.5 * g * t**2
        
        # Cut off when projectile hits ground
        above_ground = []
        for i, (xi, yi) in enumerate(zip(x, y)):
            # Find corresponding ground height at this x position
            if xi >= 40:
                break
                
            idx = int(xi / 40 * 100)
            if idx >= len(y_ground):
                idx = len(y_ground) - 1
                
            ground_height = y_ground[idx]
            if yi < ground_height:
                break
            above_ground.append(i)
            
        if above_ground:
            return x[:above_ground[-1]+1], y[:above_ground[-1]+1]
        return [4], [y_ground[5] + start_height]  # Return initial position if no valid trajectory
    
    def init():
        projectile.set_data([], [])
        return projectile, path_patch, angle_line
    
    def update(frame):
        # Different angles in each portion of the animation
        if frame < frames // 5:
            angle = 30
        elif frame < 2 * frames // 5:
            angle = 45
        elif frame < 3 * frames // 5:
            angle = 20
        elif frame < 4 * frames // 5:
            angle = 60
        else:
            angle = 37  # Not the solution!
            
        angle_text.set_text(f"{angle}°")
        
        # Update angle indicator line
        start_x = 4  # Platform center
        start_y = y_ground[5] + start_height
        end_x = start_x + 3 * np.cos(np.radians(angle))
        end_y = start_y + 3 * np.sin(np.radians(angle))
        angle_line.set_data([start_x, end_x], [start_y, end_y])
        
        # Calculate current trajectory
        x, y = trajectory_path(angle)
        
        # Check if we have a valid trajectory with at least one point
        if len(x) > 0:
            # Frame progress along the trajectory
            progress = min(1.0, (frame % (frames // 5)) / (frames // 10))
            idx = min(int(progress * (len(x) - 1)), len(x) - 1)  # Make sure idx is valid
            
            # Update projectile position
            projectile.set_data([x[idx]], [y[idx]])  # Use lists instead of scalars
            
            # Update trajectory path
            if len(x) > 1:  # Only create a path if we have multiple points
                vertices = [np.array([xi, yi]) for xi, yi in zip(x[:idx+1], y[:idx+1])]
                codes = [Path.MOVETO] + [Path.LINETO] * (len(vertices)-1)
                trajectory = Path(vertices, codes)
                path_patch.set_path(trajectory)
            else:
                # Just a single point, draw nothing
                path_patch.set_path(Path([(0, 0)], [Path.MOVETO]))
        else:
            # No valid trajectory, hide projectile and path
            projectile.set_data([], [])
            path_patch.set_path(Path([(0, 0)], [Path.MOVETO]))
            
        return projectile, path_patch, angle_line
    
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
    output_file = os.path.join(output_dir, 'projectile_challenge.mp4')
    
    # Print solution (for instructor reference)
    print("--------------------------------------")
    print("SOLUTION (Do not share with students)")
    print("--------------------------------------")
    print(f"Initial velocity: {initial_velocity} m/s")
    print(f"Target position: ({target_x}, {target_y}) m")
    print(f"Slope angle: {slope_angle:.1f}°")
    
    # Calculate the actual solution for reference
    # Using projectile motion equations
    # This is approximate and won't be shown to students
    dx = target_x - 4  # Horizontal distance
    dy = target_y - (y_ground[5] + start_height)  # Vertical distance
    
    # Quadratic formula coefficients for angle calculation
    a = initial_velocity**2
    b = -g * dx**2 / (2 * initial_velocity**2)
    c = -dx**2 / (2 * initial_velocity**2) * g - dy
    
    # Discriminant
    discriminant = b**2 - 4 * a * c
    
    if discriminant >= 0:
        t1 = np.arctan((-b + np.sqrt(discriminant)) / (2 * a) / dx) * 180 / np.pi
        t2 = np.arctan((-b - np.sqrt(discriminant)) / (2 * a) / dx) * 180 / np.pi
        print(f"Possible launch angles: {t1:.1f}° or {t2:.1f}°")
        print(f"Best launch angle: {max(t1, t2):.1f}°")
    else:
        print("Target is not reachable with given parameters.")
    print("--------------------------------------")
    
    try:
        writer = animation.FFMpegWriter(fps=fps, metadata=dict(artist='Science_In_Motion'),
                                      bitrate=2400, codec="h264",
                                      extra_args=['-pix_fmt', 'yuv420p'])
        ani.save(output_file, writer=writer)
        print(f"Projectile challenge animation saved to '{output_file}'")
    except Exception as e:
        print(f"Error saving MP4: {e}")
        print("Trying GIF...")
        gif_file = os.path.join(output_dir, 'projectile_challenge.gif')
        try:
            ani.save(gif_file, writer='pillow', fps=fps)
            print(f"Saved as GIF to '{gif_file}'")
        except Exception as e:
            print(f"Error saving GIF: {e}")
            plt.savefig(os.path.join(output_dir, 'projectile_challenge_static.png'))
            print("Saved static image instead")
    
    plt.close(fig)

if __name__ == "__main__":
    create_projectile_challenge()