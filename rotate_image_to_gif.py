"""
rotate_ease_in_out.py

Loads a square icon (e.g. icon.png), rotates it through 360° in N_FRAMES steps
but uses an “ease‐in‐out” (sinusoidal) timing so it starts from rest, speeds up
in the middle, then slows down to a stop at 360°. Every frame stays at the same
dimensions as the original icon (corners will be clipped after ~45° and near 315°).

- INPUT_ICON    : your original square image (e.g. icon.png)
- OUTPUT_GIF     : where to write the resulting GIF
- N_FRAMES       : how many intermediate steps from 0 → 360 (more → smoother but bigger file)
- DURATION_MS    : duration (in milliseconds) each frame stays on screen
- LOOP_FOREVER   : if True, the GIF loops forever; if False, it plays “once” (actually 2 passes, see note)
"""

from PIL import Image
import math

def ease_in_out_sine(t: float) -> float:
    """
    Sinusoidal ease‐in‐out function. Input t ∈ [0,1], output ∈ [0,1].
    
    f(0)=0, f'(0)=0; f(1)=1, f'(1)=0. Monotonic.
    
    f(t) = (1 - cos(π t)) / 2
    """
    return 0.5 * (1 - math.cos(math.pi * t))


def create_eased_rotating_gif(
    input_path: str,
    output_path: str,
    n_frames: int = 36,
    frame_duration_ms: int = 100,
    loop_forever: bool = True
):
    """
    - input_path:       Path to your original icon (must exist), e.g. "icon.png".
    - output_path:      Where to write the resulting GIF, e.g. "rotating_icon.gif".
    - n_frames:         Number of discrete steps between 0° and 360°. (More → smoother.)
    - frame_duration_ms:Duration in milliseconds for each frame.
    - loop_forever:     If True → `loop=0` (infinite). If False → `loop=1` (plays twice).
    """
    # 1) Load the original image as RGBA
    original = Image.open(input_path).convert("RGBA")
    w, h = original.size

    # 2) Build a list of “eased” angles: θ_i = 360° * f(t_i), where t_i = i/(n_frames-1).
    angles = []
    for i in range(n_frames):
        t = i / float(n_frames - 1)       # t goes from 0.0 to 1.0 inclusive
        eased_t = ease_in_out_sine(t)     # eased fraction ∈ [0,1]
        theta = 360.0 * eased_t           # final angle in degrees
        angles.append(theta)

    # 3) Rotate each frame _without_ expanding. This keeps the canvas at (w,h).
    #    Because expand=False, corners get clipped (become transparent) once they rotate out of the square.
    frames = []
    for theta in angles:
        frame = original.rotate(
            theta,
            resample=Image.BICUBIC,
            expand=False,
            fillcolor=(0, 0, 0, 0)  # newly exposed pixels → fully transparent
        )
        frames.append(frame)

    # 4) Save them out as an animated GIF
    loop_param = 0 if loop_forever else 1
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        optimize=True,
        format="GIF",
        duration=frame_duration_ms,
        loop=loop_param
    )
    print(
        f"✅ Saved eased‐in‐out GIF to '{output_path}'. "
        f"Size = {w}×{h}, Frames = {n_frames}, "
        f"Duration per frame = {frame_duration_ms}ms, "
        f"{'∞ loop' if loop_forever else 'play twice'}."
    )


if __name__ == "__main__":
    # You can change these variables as you like:
    INPUT_ICON = "C:\\Users\\kanva\\Downloads\\k4.png"            # <-- your original square icon
    OUTPUT_GIF  = "C:\\Users\\kanva\\Downloads\\rotating_icon.gif"  # <-- where the GIF will be written
    N_FRAMES       = 24                   # ← 24 → 15° increments (but eased speed)
    DURATION_MS    = 100                  # ← 100ms per frame → total ~2.4s per cycle
    LOOP_FOREVER   = True                 # ← True = infinite looping, False ≈ “play once”
    # ───────────────────────────────────────────────────────────────

    create_eased_rotating_gif(
        INPUT_ICON,
        OUTPUT_GIF,
        n_frames=N_FRAMES,
        frame_duration_ms=DURATION_MS,
        loop_forever=LOOP_FOREVER
    )
