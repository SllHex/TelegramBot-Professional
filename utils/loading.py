"""Helper functions for loading animations and progress bars"""

def get_progress_bar(progress: float, total_bars: int = 10) -> str:
    """
    Create a green progress bar
    Args:
        progress: Progress from 0.0 to 1.0
        total_bars: Total number of bars to show
    Returns:
        Progress bar string
    """
    filled = int(progress * total_bars)
    empty = total_bars - filled
    
    # Use green and gray squares
    bar = "🟩" * filled + "⬜" * empty
    percentage = int(progress * 100)
    
    return f"{bar} {percentage}%"

def get_loading_animation(step: int, total_steps: int = 3) -> str:
    """
    Get loading animation for current step
    Args:
        step: Current step (0-based)
        total_steps: Total number of steps
    Returns:
        Progress bar for the current step
    """
    progress = (step + 1) / total_steps
    return get_progress_bar(progress)

# Simple loading spinner
LOADING_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

def get_spinner(frame: int) -> str:
    """Get spinner character for animation"""
    return LOADING_FRAMES[frame % len(LOADING_FRAMES)]
