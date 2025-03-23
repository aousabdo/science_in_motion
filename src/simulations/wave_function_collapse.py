import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
import os
from scipy.special import hermite
from scipy.stats import norm
import math  # Import standard math module for factorial

def create_wave_function_collapse_animation(output_dir="output"):
    """
    Creates a mesmerizing visualization of quantum wave function collapse
    with vibrant colors and particle effects, optimized for TikTok's portrait format.
    The simulation shows a probability cloud that gradually collapses to definite states.
    
    Parameters:
    -----------
    output_dir : str
        Directory where output files will be saved
    """
    print("Creating Wave Function Collapse animation...")
    
    # Animation parameters
    fps = 30
    duration = 30  # 30 seconds total
    frames = fps * duration
    
    # Quantum system parameters
    x_min, x_max = -6, 6
    n_points = 500  # resolution
    x = np.linspace(x_min, x_max, n_points)
    
    # Create quantum states (superpositions of harmonic oscillator eigenstates)
    def psi_n(n, x):
        """nth eigenstate of quantum harmonic oscillator"""
        prefactor = 1.0 / np.sqrt(2**n * math.factorial(n) * np.sqrt(np.pi))
        h_n = hermite(n)(x)  # Hermite polynomial
        return prefactor * h_n * np.exp(-x**2 / 2)
    
    # Create a superposition of states (n=0 to n=6)
    max_n = 6
    states = []
    for n in range(max_n+1):
        states.append(psi_n(n, x))
    
    # Setup figure for 9:16 aspect ratio (portrait mode for TikTok)
    fig = plt.figure(figsize=(4.5, 8), facecolor='black')
    
    # Create two subplots: one for wave function, one for probability density
    ax1 = fig.add_subplot(211)  # Wave function
    ax2 = fig.add_subplot(212)  # Probability density
    
    # Configure axes
    for ax in [ax1, ax2]:
        ax.set_facecolor('black')
        ax.set_xlim(x_min, x_max)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
    
    # Set y-limits
    ax1.set_ylim(-0.8, 0.8)  # For wave function
    ax2.set_ylim(0, 0.5)     # For probability density
    
    # Create a vibrant colormap for the visualization
    colors = [
        (0.1, 0, 0.2),     # Deep purple
        (0.3, 0, 0.6),     # Purple
        (0.5, 0, 1.0),     # Bright purple
        (0, 0.5, 1.0),     # Bright blue
        (0, 0.8, 1.0),     # Cyan
        (0, 1.0, 0.8),     # Turquoise
        (0, 1.0, 0.4),     # Light green
        (0.5, 1.0, 0),     # Lime
        (1.0, 1.0, 0),     # Yellow
        (1.0, 0.6, 0),     # Orange
        (1.0, 0.4, 0),     # Orange-red
        (1.0, 0, 0),       # Red
        (1.0, 0, 0.6)      # Pink
    ]
    cmap = LinearSegmentedColormap.from_list('quantum', colors, N=512)
    
    # Initialize the animation elements
    wave_line, = ax1.plot([], [], lw=2, color='cyan')
    prob_fill = ax2.fill_between(x, 0, 0, alpha=0.7, color='cyan')
    
    # Particle effects - will represent "measurements"
    # Initialize with an empty array in the correct format for scatter
    particles = ax2.scatter([], [], s=20, c=[], cmap=cmap, alpha=0.8)
    
    # Text elements
    title = fig.text(0.5, 0.97, "Quantum Wave Function Collapse", 
                    fontsize=14, color='white', ha='center')
    
    subtitle = fig.text(0.5, 0.93, "", 
                       fontsize=10, color='white', ha='center', alpha=0)
    
    measurement_text = fig.text(0.5, 0.1, "", 
                               fontsize=12, color='white', ha='center', alpha=0)
    
    equation = fig.text(0.5, 0.05, r"$\hat{H}\Psi = i\hbar\frac{\partial\Psi}{\partial t}$", 
                       fontsize=12, color='white', ha='center', alpha=0)
    
    # ScienceInMotion branding
    watermark = fig.text(0.95, 0.97, "ScienceInMotion", 
                        fontsize=8, color='white', ha='right', alpha=0.7)
    
    # Store particle data for animation
    particle_data = {'x': [], 'y': [], 'colors': [], 'sizes': [], 'alpha': []}
    
    def generate_superposition(t, collapse_start=None, collapse_target=None, collapse_progress=0):
        """
        Generate a superposition state for time t.
        If collapse parameters are provided, gradually collapse to target state.
        """
        # Start with a superposition of states with time-dependent phases
        psi = np.zeros(n_points, dtype=complex)
        
        # Different weights for a more interesting initial superposition
        weights = [0.5, 0.5, 0.4, 0.3, 0.2, 0.1, 0.05]
        energies = [n + 0.5 for n in range(max_n+1)]  # E_n = (n + 1/2)ħω
        
        for n in range(max_n+1):
            # Time-dependent phase factor
            phase = np.exp(-1j * energies[n] * t)
            
            if collapse_start is not None and collapse_target == n:
                # Increase this state's weight during collapse
                weight = weights[n] * (1 - collapse_progress) + collapse_progress
            elif collapse_start is not None:
                # Decrease other states' weights during collapse
                weight = weights[n] * (1 - collapse_progress)
            else:
                weight = weights[n]
                
            psi += weight * phase * states[n]
        
        # Normalize
        norm = np.sqrt(np.sum(np.abs(psi)**2) * (x_max - x_min) / n_points)
        psi = psi / norm
        
        return psi
    
    def init():
        """Initialize animation"""
        wave_line.set_data([], [])
        
        # Remove existing collection and create a new one
        if len(ax2.collections) > 0:
            for collection in ax2.collections[:]:
                collection.remove()
        
        # Initialize the fill between
        prob_fill = ax2.fill_between(x, 0, 0, alpha=0.7, color='cyan')
        
        # Initialize particles with empty arrays
        particles.set_offsets(np.empty((0, 2)))
        particles.set_array(np.array([]))
        
        return wave_line, prob_fill, particles, title, subtitle, measurement_text, equation, watermark
    
    def update(frame):
        """Update function for each frame"""
        # Progress through the animation (0 to 1)
        progress = frame / frames
        
        # Parameters for the animation
        time_factor = 5.0  # Controls how fast the wave function oscillates
        t = frame * time_factor / frames
        
        # Initialize collapse parameters
        collapse_start = None
        collapse_target = None
        collapse_progress = 0
        collapsed = False
        
        # Stage 1: Introduce the wave function (0% - 10%)
        if progress < 0.1:
            # Fade in title and equation
            alpha = min(1.0, progress / 0.05)
            title.set_alpha(alpha)
            equation.set_alpha(alpha * 0.8)
            watermark.set_alpha(alpha * 0.7)
            
            subtitle_text = "Superposition of Quantum States"
            subtitle.set_text(subtitle_text)
            subtitle.set_alpha(alpha if progress > 0.05 else 0)
            
            # Wave function in superposition
            psi = generate_superposition(t)
            
        # Stage 2: Explain superposition (10% - 25%)
        elif progress < 0.25:
            subtitle_text = "Many Possible States Exist Simultaneously"
            subtitle.set_text(subtitle_text)
            subtitle.set_alpha(1.0)
            
            # Wave function continues to evolve
            psi = generate_superposition(t)
            
        # Stage 3: Measurement is about to happen (25% - 30%)
        elif progress < 0.3:
            # Show measurement text
            measurement_progress = (progress - 0.25) / 0.05
            measurement_text.set_text("Preparing to Measure...")
            measurement_text.set_alpha(measurement_progress)
            
            # Wave function still in superposition but "vibrating" more
            psi = generate_superposition(t * (1 + 2 * measurement_progress))
            
        # Stage 4: First collapse (30% - 40%)
        elif progress < 0.4:
            # Collapse parameters
            collapse_start = 0.3
            collapse_target = 2  # Collapse to n=2 state
            collapse_progress = min(1.0, (progress - 0.3) / 0.05)
            
            # Update text
            if collapse_progress >= 1.0:
                measurement_text.set_text("Measured: Energy Level 2")
                subtitle.set_text("Wave Function Collapsed!")
                collapsed = True
            else:
                measurement_text.set_text("Measuring...")
                
            measurement_text.set_alpha(1.0)
            
            # Generate collapsed wave function
            psi = generate_superposition(t, collapse_start, collapse_target, collapse_progress)
            
        # Stage 5: Show collapsed state (40% - 50%)
        elif progress < 0.5:
            # Already collapsed to state n=2
            collapse_target = 2
            collapse_progress = 1.0
            collapsed = True
            
            # Fade out measurement text
            fade_out = min(1.0, max(0.0, 1.0 - min(1.0, (progress - 0.45) / 0.05)))
            measurement_text.set_text("Measured: Energy Level 2")
            measurement_text.set_alpha(fade_out)
            
            subtitle.set_text("System in Definite Energy State")
            
            # Generate collapsed wave function
            psi = generate_superposition(t, 0.3, collapse_target, collapse_progress)
            
        # Stage 6: Return to superposition (50% - 60%)
        elif progress < 0.6:
            # Gradually return to superposition
            uncollapse_progress = min(1.0, (progress - 0.5) / 0.05)
            collapse_progress = 1.0 - uncollapse_progress
            collapse_target = 2
            
            subtitle.set_text("Returning to Superposition")
            subtitle.set_alpha(1.0)
            
            if uncollapse_progress >= 1.0:
                collapse_start = None
                collapse_target = None
                collapse_progress = 0
            else:
                collapse_start = 0.3
            
            # Generate wave function that's returning to superposition
            psi = generate_superposition(t, collapse_start, collapse_target, collapse_progress)
            
        # Stage 7: Second measurement preparation (60% - 65%)
        elif progress < 0.65:
            measurement_progress = (progress - 0.6) / 0.05
            measurement_text.set_text("Preparing Another Measurement...")
            measurement_text.set_alpha(measurement_progress)
            
            subtitle.set_text("Quantum States Interfering")
            
            # Wave function in superposition
            psi = generate_superposition(t)
            
        # Stage 8: Second collapse (65% - 75%)
        elif progress < 0.75:
            # Collapse parameters - different target this time
            collapse_start = 0.65
            collapse_target = 4  # Collapse to n=4 state
            collapse_progress = min(1.0, (progress - 0.65) / 0.05)
            
            # Update text
            if collapse_progress >= 1.0:
                measurement_text.set_text("Measured: Energy Level 4")
                subtitle.set_text("Different Result This Time!")
                collapsed = True
            else:
                measurement_text.set_text("Measuring...")
                
            measurement_text.set_alpha(1.0)
            
            # Generate collapsed wave function
            psi = generate_superposition(t, collapse_start, collapse_target, collapse_progress)
            
        # Stage 9: Final explanations (75% - 90%)
        elif progress < 0.9:
            # Keep collapsed state for explanation
            collapse_start = 0.65
            collapse_target = 4
            collapse_progress = 1.0
            collapsed = True
            
            # Different messages during this phase
            if progress < 0.8:
                subtitle.set_text("Quantum Measurement Is Probabilistic")
            elif progress < 0.85:
                subtitle.set_text("Each Measurement May Give Different Results")
            else:
                # Begin fading out measurement text
                fade_out = min(1.0, max(0.0, 1.0 - min(1.0, (progress - 0.85) / 0.05)))
                measurement_text.set_alpha(fade_out)
                subtitle.set_text("The Heart of Quantum Mechanics")
            
            # Generate collapsed wave function
            psi = generate_superposition(t, collapse_start, collapse_target, collapse_progress)
            
        # Stage 10: Outro (90% - 100%)
        else:
            # Fade everything out
            fade_out = min(1.0, max(0.0, 1.0 - min(1.0, (progress - 0.9) / 0.1)))
            
            title.set_alpha(fade_out)
            subtitle.set_alpha(fade_out)
            equation.set_alpha(fade_out * 0.8)
            watermark.set_alpha(fade_out * 0.7)
            measurement_text.set_alpha(0)
            
            # Gradually uncollapse and slow down
            uncollapse_progress = min(1.0, (progress - 0.9) / 0.05)
            if uncollapse_progress >= 1.0:
                # Full superposition again for outro
                psi = generate_superposition(t * (1.0 - (progress - 0.95) / 0.05))
            else:
                # Gradually return to superposition
                collapse_progress = 1.0 - uncollapse_progress
                psi = generate_superposition(t, 0.65, 4, collapse_progress)
        
        # Extract real part and probability density
        psi_real = np.real(psi)
        probability = np.abs(psi)**2
        
        # Update the wave function plot
        wave_line.set_data(x, psi_real)
        
        # Remove previous fill_between
        if len(ax2.collections) > 0:
            for collection in ax2.collections[:]:
                collection.remove()
        
        # Add new fill_between
        prob_fill = ax2.fill_between(x, 0, probability, alpha=0.7, 
                                   color=('cyan' if not collapsed else 'magenta'))
        
        # Handle particle effects for measurement visualization
        
        # Add new particles at certain frames during collapse
        if ((0.3 < progress < 0.4) or (0.65 < progress < 0.75)) and frame % 2 == 0:
            # Only add particles during collapse transitions
            
            # Determine collapsed state
            if 0.3 < progress < 0.4:
                target = 2
            else:
                target = 4
                
            # Add particles near the peaks of the target state's probability
            peak_indices = []
            target_prob = np.abs(states[target])**2
            
            # Find peaks by looking for points higher than neighbors
            for i in range(1, len(target_prob)-1):
                if target_prob[i] > target_prob[i-1] and target_prob[i] > target_prob[i+1]:
                    if target_prob[i] > 0.1 * np.max(target_prob):  # Only significant peaks
                        peak_indices.append(i)
            
            # Add particles near these peaks
            for peak_idx in peak_indices:
                peak_x = x[peak_idx]
                for _ in range(np.random.randint(1, 4)):  # 1-3 particles per peak
                    # Position with some random noise
                    particle_x = peak_x + np.random.normal(0, 0.1)
                    particle_y = np.random.uniform(0.05, probability[peak_idx])
                    
                    # Add to particle data lists
                    particle_data['x'].append(particle_x)
                    particle_data['y'].append(particle_y)
                    particle_data['colors'].append(np.random.random())  # Random color
                    particle_data['sizes'].append(np.random.randint(10, 50))  # Random size
                    particle_data['alpha'].append(1.0)  # Start fully visible
        
        # Update existing particles (fade out and move)
        if particle_data['x']:
            # Filter out particles that have faded
            indices_to_keep = []
            for i in range(len(particle_data['x'])):
                # Decrease alpha (fade out)
                particle_data['alpha'][i] -= 0.05
                
                if particle_data['alpha'][i] > 0:
                    indices_to_keep.append(i)
            
            # Keep only non-faded particles
            for key in particle_data:
                particle_data[key] = [particle_data[key][i] for i in indices_to_keep]
        
        # Update particle scatter plot
        if particle_data['x']:
            # Create the data for scatter
            offsets = np.column_stack((particle_data['x'], particle_data['y']))
            particles.set_offsets(offsets)
            
            # Update colors, sizes, and alpha
            particles.set_array(np.array(particle_data['colors']))
            particles.set_sizes(particle_data['sizes'])
            particles.set_alpha(particle_data['alpha'])
        else:
            # No particles - set empty arrays
            particles.set_offsets(np.empty((0, 2)))
            particles.set_array(np.array([]))
        
        # Return updated artists
        return wave_line, prob_fill, particles, title, subtitle, measurement_text, equation, watermark
    
    # Create the animation
    print(f"Creating animation with {frames} frames at {fps} fps...")
    ani = animation.FuncAnimation(
        fig, 
        update, 
        frames=frames,
        init_func=init,
        interval=1000/fps,
        blit=True
    )
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the animation
    output_file = os.path.join(output_dir, "wave_function_collapse.mp4")
    print(f"Saving animation to {output_file}...")
    
    try:
        # Try using ffmpeg if available
        writer = animation.FFMpegWriter(fps=fps, metadata=dict(artist='ScienceInMotion'), bitrate=3500)
        ani.save(output_file, writer=writer)
        print(f"Quantum wave function animation saved to '{output_file}'")
    except FileNotFoundError:
        # If ffmpeg is not available, save as a GIF instead
        print("ffmpeg not found. Saving as GIF instead...")
        gif_file = os.path.join(output_dir, "wave_function_collapse.gif")
        writer = animation.PillowWriter(fps=fps)
        ani.save(gif_file, writer=writer)
        print(f"Quantum wave function animation saved as GIF to '{gif_file}'")
    
    plt.close(fig)
    
    # Print file size for verification
    if os.path.exists(output_file):
        file_size = os.path.getsize(output_file) / (1024 * 1024)  # Size in MB
        print(f"File size: {file_size:.2f} MB")
    elif os.path.exists(gif_file):
        file_size = os.path.getsize(gif_file) / (1024 * 1024)  # Size in MB
        print(f"File size: {file_size:.2f} MB")

def main():
    create_wave_function_collapse_animation()

if __name__ == "__main__":
    main()