import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.integrate import odeint

# Uncomment the next import if you want to add audio at the end:
# from moviepy.editor import VideoFileClip, AudioFileClip

def double_pendulum_equations(y, t, L1, L2, m1, m2, g):
    """
    Defines the differential equations for a double pendulum system.
    y  : [theta1, omega1, theta2, omega2]
    t  : time
    L1, L2, m1, m2, g : lengths, masses, gravity
    """
    theta1, omega1, theta2, omega2 = y
    delta = theta2 - theta1

    # Pre-calculate denominators
    den1 = (m1 + m2)*L1 - m2*L1*(np.cos(delta))**2
    den2 = (L2 / L1) * den1

    dydt = np.zeros_like(y)

    # dtheta1/dt
    dydt[0] = omega1
    # domega1/dt
    dydt[1] = (
        m2*L1*omega1**2*np.sin(delta)*np.cos(delta)
        + m2*g*np.sin(theta2)*np.cos(delta)
        + m2*L2*omega2**2*np.sin(delta)
        - (m1+m2)*g*np.sin(theta1)
    ) / den1
    # dtheta2/dt
    dydt[2] = omega2
    # domega2/dt
    dydt[3] = (
        -m2*L2*omega2**2*np.sin(delta)*np.cos(delta)
        + (m1+m2)*g*np.sin(theta1)*np.cos(delta)
        - (m1+m2)*L1*omega1**2*np.sin(delta)
        - (m1+m2)*g*np.sin(theta2)
    ) / den2

    return dydt

def create_double_pendulum_animation():
    """
    Simulates a double pendulum with a visually striking style suitable for TikTok.
    It saves the animation as 'double_pendulum_tiktok.mp4' (portrait ratio, dark background).
    No audio is added here by default, but instructions to add audio are included.
    """

    # ----------------------------
    # 1. Physical & Initial Setup
    # ----------------------------
    L1, L2 = 1.0, 1.0   # rod lengths
    m1, m2 = 1.0, 1.0   # bob masses
    g = 9.81            # gravity

    # Initial angles (in radians)
    theta1_0 = np.radians(120)  # a large initial angle
    omega1_0 = 0.0
    theta2_0 = np.radians(60)
    omega2_0 = 0.0
    y0 = [theta1_0, omega1_0, theta2_0, omega2_0]

    # ----------------------------
    # 2. Simulation Time
    # ----------------------------
    t_max = 30.0        # total simulation time (sec)
    fps = 30            # frames per second
    frames = int(t_max * fps)
    t = np.linspace(0, t_max, frames)

    # ----------------------------
    # 3. Numerical Integration
    # ----------------------------
    sol = odeint(double_pendulum_equations, y0, t, args=(L1, L2, m1, m2, g))
    theta1, theta2 = sol[:, 0], sol[:, 2]

    # Convert to Cartesian coordinates
    x1 = L1 * np.sin(theta1)
    y1 = -L1 * np.cos(theta1)
    x2 = x1 + L2 * np.sin(theta2)
    y2 = y1 - L2 * np.cos(theta2)

    # ----------------------------
    # 4. Figure & Axes (Portrait)
    # ----------------------------
    # 9:16 aspect ratio suitable for TikTok (e.g., 4.5 by 8)
    fig, ax = plt.subplots(figsize=(4.5, 8), facecolor="black")
    ax.set_facecolor("black")
    ax.set_xlim(-L1 - L2 - 0.2, L1 + L2 + 0.2)
    ax.set_ylim(-L1 - L2 - 0.2, L1 + L2 + 0.2)
    ax.set_aspect("equal", "box")
    
    # Hide axes lines/ticks to emphasize the pendulum
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # We’ll draw the rods and bobs as a single line with marker
    line, = ax.plot([], [], marker='o', lw=3, markersize=10)
    # Add a trace for the second bob
    trace, = ax.plot([], [], lw=1)

    # Customize colors for better contrast
    line.set_color("white")   # rods and bobs
    trace.set_color("cyan")   # bob trace

    # Lists to keep track of second bob's path
    x2_history, y2_history = [], []

    # ----------------------------
    # 5. Animation Functions
    # ----------------------------
    def init():
        line.set_data([], [])
        trace.set_data([], [])
        x2_history.clear()
        y2_history.clear()
        return line, trace,

    def update(frame):
        x1f, y1f = x1[frame], y1[frame]
        x2f, y2f = x2[frame], y2[frame]

        # Rod 1: pivot(0,0) -> (x1f, y1f)
        # Rod 2: (x1f, y1f) -> (x2f, y2f)
        # Marker for both bobs
        line.set_data([0, x1f, x2f], [0, y1f, y2f])

        # Trace for the second bob
        x2_history.append(x2f)
        y2_history.append(y2f)
        trace.set_data(x2_history, y2_history)

        return line, trace,

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=frames,
        init_func=init,
        interval=1000/fps,
        blit=True
    )

    # ----------------------------
    # 6. Save Animation (No Audio)
    # ----------------------------
    output_file = "double_pendulum_tiktok.mp4"
    print("Generating animation... Please wait.")
    ani.save(output_file, writer="ffmpeg", fps=fps, dpi=100)
    print(f"Animation saved to '{output_file}'")

    # ----------------------------
    # 7. (Optional) Add Audio with MoviePy
    # ----------------------------
    """
    # Example code to add an audio track (e.g., background_music.mp3)
    # after the main video is created:
    
    from moviepy.editor import VideoFileClip, AudioFileClip
    
    final_video = "double_pendulum_tiktok_with_audio.mp4"
    audio_clip = AudioFileClip("background_music.mp3")
    
    # Load the silent video, set audio, and write a new file
    video_clip = VideoFileClip(output_file)
    video_duration = video_clip.duration

    # Optionally shorten or loop audio to match video_duration
    # e.g., trimmed_audio = audio_clip.subclip(0, video_duration)

    # Combine them
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(final_video, codec="libx264", audio_codec="aac")
    print(f"Video with audio saved to '{final_video}'")
    """

def main():
    create_double_pendulum_animation()

if __name__ == "__main__":
    main()
