import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Arc, Circle
import os
from matplotlib import rcParams

# Set high DPI value for better quality
rcParams['figure.dpi'] = 150

def create_trig_challenge_animation(output_dir="output"):
    """
    Creates an engaging trigonometry challenge animation optimized for TikTok.
    The animation shows a rotating triangle with dynamic measurements and asks
    viewers to solve for a missing value.
    """
    print("Creating Trigonometry Challenge Animation...")
    
    # Animation parameters
    fps = 30
    duration = 30  # 30 seconds total
    frames = fps * duration
    
    # Set up figure (9:16 aspect ratio for TikTok)
    fig = plt.figure(figsize=(6, 10.67), facecolor='black')
    ax = fig.add_subplot(111)
    
    # Configure axes
    ax.set_facecolor('black')
    ax.set_xlim(-6, 6)
    ax.set_ylim(-8, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Define the base triangle points
    base_length = 4
    height = 3
    A = np.array([-base_length/2, -height/2])
    B = np.array([base_length/2, -height/2])
    C = np.array([0, height/2])
    
    # Create triangle elements
    triangle, = ax.plot([], [], 'w-', lw=2)
    point_A = Circle(A, 0.1, color='cyan', zorder=3)
    point_B = Circle(B, 0.1, color='magenta', zorder=3)
    point_C = Circle(C, 0.1, color='yellow', zorder=3)
    ax.add_patch(point_A)
    ax.add_patch(point_B)
    ax.add_patch(point_C)
    
    # Create angle arcs
    angle_A = Arc(A, 1, 1, angle=0, theta1=0, theta2=0, color='cyan', lw=2)
    angle_B = Arc(B, 1, 1, angle=0, theta1=0, theta2=0, color='magenta', lw=2)
    angle_C = Arc(C, 1, 1, angle=0, theta1=0, theta2=0, color='yellow', lw=2)
    ax.add_patch(angle_A)
    ax.add_patch(angle_B)
    ax.add_patch(angle_C)
    
    # Text elements with mathematical styling
    title = ax.text(0, 7, "Trigonometry Challenge", 
                   fontsize=18, color='white', ha='center', 
                   fontname='DejaVu Serif')
    
    subtitle = ax.text(0, 6, "Can you find x?", 
                      fontsize=14, color='white', ha='center', 
                      fontname='DejaVu Serif', alpha=0)
    
    # Side labels
    side_a = ax.text(0, 0, "", color='white', ha='right', va='bottom', fontsize=12)
    side_b = ax.text(0, 0, "", color='white', ha='left', va='bottom', fontsize=12)
    side_c = ax.text(0, 0, "x", color='red', ha='center', va='center', fontsize=14, fontweight='bold')
    
    # Angle labels
    angle_label_A = ax.text(0, 0, "", color='cyan', ha='right', va='top', fontsize=12)
    angle_label_B = ax.text(0, 0, "", color='magenta', ha='left', va='top', fontsize=12)
    angle_label_C = ax.text(0, 0, "", color='yellow', ha='center', va='bottom', fontsize=12)
    
    # Watermark
    watermark = ax.text(0, -7, "@ScienceInMotion", 
                       fontsize=14, color='#FF00FF', ha='center', alpha=0.7)
    
    def rotate_point(point, angle, center=np.array([0, 0])):
        """Rotate a point around a center by given angle in radians"""
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)
        px, py = point - center
        rx = px * cos_a - py * sin_a
        ry = px * sin_a + py * cos_a
        return np.array([rx, ry]) + center
    
    def get_angle(p1, p2, p3):
        """Calculate angle between three points in degrees"""
        v1 = p1 - p2
        v2 = p3 - p2
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
        return np.degrees(angle)
    
    def init():
        """Initialize animation"""
        triangle.set_data([], [])
        return (triangle, point_A, point_B, point_C, angle_A, angle_B, angle_C,
                title, subtitle, side_a, side_b, side_c, angle_label_A, 
                angle_label_B, angle_label_C, watermark)
    
    def update(frame):
        """Update animation for each frame"""
        frame_norm = frame / frames  # Normalized frame (0 to 1)
        
        # Rotation angle for the entire triangle
        rotation = frame_norm * 2 * np.pi
        
        # Calculate current triangle points with rotation
        center = np.array([0, 0])
        current_A = rotate_point(A, rotation)
        current_B = rotate_point(B, rotation)
        current_C = rotate_point(C, rotation)
        
        # Update triangle
        triangle.set_data([current_A[0], current_B[0], current_C[0], current_A[0]],
                         [current_A[1], current_B[1], current_C[1], current_A[1]])
        
        # Update points
        point_A.center = current_A
        point_B.center = current_B
        point_C.center = current_C
        
        # Calculate and update angles
        angle_A_val = get_angle(current_B, current_A, current_C)
        angle_B_val = get_angle(current_A, current_B, current_C)
        angle_C_val = get_angle(current_A, current_C, current_B)
        
        # Update angle arcs
        for point, angle_patch, angle_val, offset in [
            (current_A, angle_A, angle_A_val, 180),
            (current_B, angle_B, angle_B_val, -60),
            (current_C, angle_C, angle_C_val, 60)
        ]:
            angle_patch.center = point
            angle_patch.theta1 = offset - angle_val/2
            angle_patch.theta2 = offset + angle_val/2
        
        # Calculate side lengths
        side_a_len = np.linalg.norm(current_B - current_C)
        side_b_len = np.linalg.norm(current_A - current_C)
        side_c_len = np.linalg.norm(current_A - current_B)
        
        # Text fade-in based on animation phase
        if frame_norm < 0.1:  # Initial fade in
            alpha = frame_norm / 0.1
            title.set_alpha(alpha)
            watermark.set_alpha(alpha * 0.7)
        elif 0.2 < frame_norm < 0.3:  # Fade in measurements
            alpha = (frame_norm - 0.2) / 0.1
            subtitle.set_alpha(alpha)
        elif frame_norm > 0.9:  # Fade out
            alpha = (1 - (frame_norm - 0.9) / 0.1)
            title.set_alpha(alpha)
            subtitle.set_alpha(alpha)
            watermark.set_alpha(alpha * 0.7)
        
        # Update angle labels with rounded values
        angle_label_A.set_text(f"{angle_A_val:.0f}°")
        angle_label_B.set_text(f"{angle_B_val:.0f}°")
        angle_label_C.set_text(f"{angle_C_val:.0f}°")
        
        # Position labels
        for label, point in [
            (angle_label_A, current_A),
            (angle_label_B, current_B),
            (angle_label_C, current_C)
        ]:
            label.set_position((point[0], point[1]))
        
        # Update side labels
        side_a.set_text(f"{side_a_len:.1f}")
        side_b.set_text(f"{side_b_len:.1f}")
        
        # Position side labels at midpoints
        side_a.set_position(((current_B[0] + current_C[0])/2, (current_B[1] + current_C[1])/2))
        side_b.set_position(((current_A[0] + current_C[0])/2, (current_A[1] + current_C[1])/2))
        side_c.set_position(((current_A[0] + current_B[0])/2, (current_A[1] + current_B[1])/2))
        
        return (triangle, point_A, point_B, point_C, angle_A, angle_B, angle_C,
                title, subtitle, side_a, side_b, side_c, angle_label_A, 
                angle_label_B, angle_label_C, watermark)
    
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
    output_file = os.path.join(output_dir, 'trig_challenge.mp4')
    print(f"Saving animation to {output_file}...")
    
    try:
        writer = animation.FFMpegWriter(fps=fps, metadata=dict(artist='Me'),
                                      bitrate=1800, codec="h264",
                                      extra_args=['-pix_fmt', 'yuv420p'])
        ani.save(output_file, writer=writer)
        print(f"Trigonometry challenge animation saved to '{output_file}'")
    except (RuntimeError, FileNotFoundError) as e:
        print("ffmpeg not found. Saving as GIF instead...")
        gif_file = os.path.join(output_dir, 'trig_challenge.gif')
        ani.save(gif_file, writer='pillow', fps=fps)
        print(f"Trigonometry challenge animation saved as GIF to '{gif_file}'")
        
        file_size_bytes = os.path.getsize(gif_file)
        file_size_mb = file_size_bytes / (1024 * 1024)
        print(f"File size: {file_size_mb:.2f} MB")
    
    plt.close(fig)

if __name__ == "__main__":
    create_trig_challenge_animation() 