import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Polygon, Arc, RegularPolygon, Circle
import matplotlib.patheffects as path_effects
import os

def create_triangle_angle_challenge(output_dir="output"):
    """
    Creates an animation showing geometric angle challenge problems
    where students need to find missing angles in triangles.
    """
    # Animation parameters
    fps = 30
    duration = 15
    frames = fps * duration
    
    # Setup figure
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
    ax.set_facecolor('#000000')
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Draw grid lines
    for x in range(-10, 11, 1):
        ax.axvline(x, color='#333333', linestyle='-', linewidth=0.5, alpha=0.5)
    for y in range(-10, 11, 1):
        ax.axhline(y, color='#333333', linestyle='-', linewidth=0.5, alpha=0.5)
    
    # Challenge parameters
    problems = [
        {
            'points': [(-5, -5), (5, -5), (0, 5)],  # Triangle vertices
            'known_angles': [40, 60, None],         # Known angles (None for unknown)
            'label_positions': [(0, -6), (5.5, -4), (-0.5, 5.5)],  # Angle label positions
            'text': "Find angle x",
            'x_value': 80  # The actual value of x that students should calculate
        },
        {
            'points': [(-6, -3), (6, -3), (0, 6)],
            'known_angles': [35, None, 55],
            'label_positions': [(-6.5, -4), (6.5, -4), (0, 6.5)],
            'text': "Find angle x",
            'x_value': 90
        },
        {
            'points': [(-4, -4), (7, -4), (2, 5)],
            'known_angles': [None, 28, 47],
            'label_positions': [(-4.5, -5), (7.5, -3), (2.5, 5.5)],
            'text': "Find angle x",
            'x_value': 105
        }
    ]
    
    # Current problem index
    problem_idx = 0
    
    # Initialize elements
    triangle = Polygon(problems[0]['points'], closed=True, fill=False, 
                     edgecolor='white', linewidth=2)
    ax.add_patch(triangle)
    
    # Create angle arcs
    angle_arcs = []
    angle_labels = []
    
    for i in range(3):
        arc = Arc((0, 0), 0, 0, theta1=0, theta2=0, color='white', linewidth=2)
        angle_arcs.append(arc)
        ax.add_patch(arc)
        
        label = ax.text(0, 0, "", fontsize=14, color='white', ha='center', va='center')
        angle_labels.append(label)
    
    # Create text elements
    title = ax.text(0, 9, "GEOMETRY CHALLENGE", fontsize=24, color='white', 
                  ha='center', weight='bold')
    title.set_path_effects([path_effects.withStroke(linewidth=3, foreground='black')])
    
    instruction = ax.text(0, 7, problems[0]['text'], fontsize=20, color='#AAAAFF', 
                        ha='center')
    instruction.set_path_effects([path_effects.withStroke(linewidth=3, foreground='black')])
    
    # Solution box
    solution_box = Polygon([(-3, -8), (3, -8), (3, -7), (-3, -7)], 
                         facecolor='#222222', edgecolor='white', linewidth=1)
    ax.add_patch(solution_box)
    
    solution_text = ax.text(0, -7.5, "x = ?", fontsize=16, color='white', ha='center')
    
    # Markers showing right angles
    right_angle_markers = []
    for _ in range(3):
        marker = RegularPolygon((0, 0), 4, radius=0.3, orientation=np.pi/4, 
                             fill=False, color='#44AAFF', linewidth=1.5)
        marker.set_visible(False)  # Hide initially
        right_angle_markers.append(marker)
        ax.add_patch(marker)
    
    # Helper points
    point_markers = []
    for _ in range(3):
        point = Circle((0, 0), radius=0.1, fill=True, color='#FF4444')
        point_markers.append(point)
        ax.add_patch(point)
    
    # Function to set up angles
    def setup_angles(vertices):
        angles = []
        for i in range(3):
            # Get angle vertices in correct order
            prev_i = (i - 1) % 3
            next_i = (i + 1) % 3
            
            # Calculate vectors
            v1 = np.array(vertices[prev_i]) - np.array(vertices[i])
            v2 = np.array(vertices[next_i]) - np.array(vertices[i])
            
            # Calculate angle
            dot_product = np.dot(v1, v2)
            norm_product = np.linalg.norm(v1) * np.linalg.norm(v2)
            cos_angle = dot_product / norm_product
            angle_rad = np.arccos(np.clip(cos_angle, -1.0, 1.0))
            angle_deg = np.degrees(angle_rad)
            
            # Calculate start angle for arc
            start_angle = np.degrees(np.arctan2(v1[1], v1[0]))
            
            # Adjust for Matplotlib's angle convention
            start_angle = (start_angle + 180) % 360
            
            angles.append({
                'center': vertices[i],
                'angle': angle_deg,
                'start_angle': start_angle,
                'end_angle': (start_angle - angle_deg) % 360
            })
            
        return angles
    
    def init():
        # Initialize function for animation
        return (triangle, *angle_arcs, *angle_labels, *point_markers)
    
    def update(frame):
        nonlocal problem_idx
        
        # Change problem every 5 seconds
        if frame % (fps * 5) == 0:
            problem_idx = (frame // (fps * 5)) % len(problems)
            
        # Get current problem
        problem = problems[problem_idx]
        vertices = problem['points']
        known_angles = problem['known_angles']
        
        # Setup angle information
        angle_info = setup_angles(vertices)
        
        # Update triangle
        triangle.set_xy(vertices)
        
        # Update instruction
        instruction.set_text(problem['text'])
        
        # Update points
        for i, (point, vertex) in enumerate(zip(point_markers, vertices)):
            point.set_center(vertex)
        
        # Create animation effect - reveal solution gradually
        progress = (frame % (fps * 5)) / (fps * 5)
        
        # Update angle arcs and labels
        for i in range(3):
            # Set arc parameters
            center = angle_info[i]['center']
            angle = angle_info[i]['angle']
            start = angle_info[i]['start_angle']
            end = start - angle * min(1.0, 2 * progress)
            
            # Size of arc depends on position in triangle
            size = 1.5
            
            # Create a new arc with updated parameters
            arc = angle_arcs[i]
            # Remove old arc
            arc.remove()
            # Create new arc with updated parameters
            new_arc = Arc(xy=center, width=size, height=size, 
                        angle=0, theta1=start, theta2=end, 
                        color='white', linewidth=2)
            ax.add_patch(new_arc)
            angle_arcs[i] = new_arc
            
            # Set angle label
            label_pos = problem['label_positions'][i]
            label = angle_labels[i]
            label.set_position(label_pos)
            
            # Check if this is a right angle
            is_right = abs(angle - 90) < 0.5
            if is_right:
                right_angle_markers[i].set_visible(True)
                right_angle_markers[i].set_xy(center)
            else:
                right_angle_markers[i].set_visible(False)
            
            # Set angle label text
            if known_angles[i] is not None:
                label.set_text(f"{known_angles[i]}°")
            else:
                label.set_text("x")
                # On last second of the problem, reveal the answer
                if progress > 0.8:
                    solution_text.set_text(f"x = {problem['x_value']}°")
                else:
                    solution_text.set_text("x = ?")
        
        return (triangle, *angle_arcs, *angle_labels, instruction, 
                solution_text, *right_angle_markers, *point_markers)
    
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
    output_file = os.path.join(output_dir, 'triangle_angle_challenge.mp4')
    
    try:
        writer = animation.FFMpegWriter(fps=fps, metadata=dict(artist='Science_In_Motion'),
                                      bitrate=2400, codec="h264",
                                      extra_args=['-pix_fmt', 'yuv420p'])
        ani.save(output_file, writer=writer)
        print(f"Triangle angle challenge animation saved to '{output_file}'")
    except Exception as e:
        print(f"Error saving MP4: {e}")
        print("Trying GIF...")
        gif_file = os.path.join(output_dir, 'triangle_angle_challenge.gif')
        try:
            ani.save(gif_file, writer='pillow', fps=fps)
            print(f"Saved as GIF to '{gif_file}'")
        except Exception as e:
            print(f"Error saving GIF: {e}")
            plt.savefig(os.path.join(output_dir, 'triangle_angle_challenge_static.png'))
            print("Saved static image instead")
    
    plt.close(fig)

if __name__ == "__main__":
    create_triangle_angle_challenge() 