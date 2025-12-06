#!/usr/bin/env python3
"""
Setup script for Telegram Bot Showcase
Automates the installation and configuration process
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


class Colors:
    """Terminal colors"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print colored header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.END}\n")


def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")


def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")


def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")


def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")


def check_python_version():
    """Check if Python version is 3.9 or higher"""
    print_info("Checking Python version...")
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print_error(f"Python 3.9+ required, you have {version.major}.{version.minor}")
        print_info("Please upgrade Python: https://www.python.org/downloads/")
        return False
    
    print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def create_virtual_environment():
    """Create a virtual environment"""
    print_info("Creating virtual environment...")
    
    venv_path = Path("venv")
    if venv_path.exists():
        print_warning("Virtual environment already exists, skipping...")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print_success("Virtual environment created")
        return True
    except subprocess.CalledProcessError:
        print_error("Failed to create virtual environment")
        return False


def get_pip_command():
    """Get the pip command based on OS"""
    if platform.system() == "Windows":
        return "venv\\Scripts\\pip.exe"
    else:
        return "venv/bin/pip"


def install_dependencies():
    """Install required dependencies"""
    print_info("Installing dependencies...")
    
    pip_cmd = get_pip_command()
    
    try:
        # Upgrade pip
        subprocess.run([pip_cmd, "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        
        # Install requirements
        result = subprocess.run(
            [pip_cmd, "install", "-r", "requirements.txt"],
            check=True,
            capture_output=True,
            text=True
        )
        
        print_success("Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print_error("Failed to install dependencies")
        print(e.stderr)
        return False


def create_env_file():
    """Create .env file from template"""
    print_info("Setting up environment configuration...")
    
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if env_path.exists():
        overwrite = input(f"{Colors.YELLOW}.env file already exists. Overwrite? (y/N): {Colors.END}")
        if overwrite.lower() != 'y':
            print_info("Keeping existing .env file")
            return True
    
    # Get user input
    print(f"\n{Colors.BOLD}Please provide the following information:{Colors.END}\n")
    
    print_info("Get your bot token from @BotFather on Telegram")
    bot_token = input("Bot Token: ").strip()
    
    print_info("Get your user ID from @userinfobot on Telegram")
    admin_id = input("Your Telegram User ID: ").strip()
    
    print_info("(Optional) Get free Gemini API key from https://makersuite.google.com/app/apikey")
    gemini_key = input("Gemini API Key (press Enter to skip): ").strip()
    
    # Create .env content
    env_content = f"""# Required Configuration
BOT_TOKEN={bot_token}
ADMIN_USER_IDS={admin_id}

# Optional: AI Features (Google Gemini - FREE)
# Get your free API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY={gemini_key}

# Optional: Payment Demo
PAYMENT_PROVIDER_TOKEN=

# Bot Settings
DEBUG_MODE=False
MAX_FILE_SIZE_MB=10
RATE_LIMIT_MESSAGES=30
RATE_LIMIT_SECONDS=60
"""
    
    # Write .env file
    try:
        with open(env_path, 'w') as f:
            f.write(env_content)
        print_success("Configuration file created")
        return True
    except Exception as e:
        print_error(f"Failed to create .env file: {e}")
        return False


def test_bot_import():
    """Test if bot can be imported"""
    print_info("Testing bot configuration...")
    
    # Get Python command
    if platform.system() == "Windows":
        python_cmd = "venv\\Scripts\\python.exe"
    else:
        python_cmd = "venv/bin/python"
    
    try:
        result = subprocess.run(
            [python_cmd, "-c", "from config import BOT_TOKEN; print('OK' if BOT_TOKEN else 'MISSING')"],
            check=True,
            capture_output=True,
            text=True
        )
        
        if "OK" in result.stdout:
            print_success("Bot configuration is valid")
            return True
        else:
            print_error("BOT_TOKEN is missing in .env file")
            return False
    except subprocess.CalledProcessError as e:
        print_error("Failed to validate configuration")
        print(e.stderr)
        return False


def print_next_steps():
    """Print next steps for the user"""
    print_header("Setup Complete! 🎉")
    
    if platform.system() == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
        python_cmd = "python"
    else:
        activate_cmd = "source venv/bin/activate"
        python_cmd = "python3"
    
    print(f"{Colors.BOLD}To start your bot:{Colors.END}\n")
    print(f"  1. Activate virtual environment:")
    print(f"     {Colors.GREEN}{activate_cmd}{Colors.END}\n")
    print(f"  2. Run the bot:")
    print(f"     {Colors.GREEN}{python_cmd} main.py{Colors.END}\n")
    
    print(f"{Colors.BOLD}Quick start:{Colors.END}")
    print(f"  {Colors.GREEN}{activate_cmd} && {python_cmd} main.py{Colors.END}\n")
    
    print(f"{Colors.BOLD}Next steps:{Colors.END}")
    print(f"  • Open Telegram and search for your bot")
    print(f"  • Send /start to begin")
    print(f"  • Explore all features!")
    
    print(f"\n{Colors.BOLD}Documentation:{Colors.END}")
    print(f"  • README.md - Full documentation")
    print(f"  • QUICKSTART.md - Quick start guide")
    print(f"  • docs/API.md - API integration guide")
    print(f"  • docs/DEPLOYMENT.md - Deployment guide")
    
    print(f"\n{Colors.BOLD}Need help?{Colors.END}")
    print(f"  • GitHub Issues: https://github.com/yourusername/telegram-bot-showcase/issues")
    print(f"  • Documentation: https://github.com/yourusername/telegram-bot-showcase")
    
    print(f"\n{Colors.GREEN}Happy botting! 🤖{Colors.END}\n")


def main():
    """Main setup function"""
    print_header("Telegram Bot Showcase - Setup")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        print_error("Setup failed: Could not create virtual environment")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print_error("Setup failed: Could not install dependencies")
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        print_error("Setup failed: Could not create configuration file")
        sys.exit(1)
    
    # Test configuration
    if not test_bot_import():
        print_warning("Setup completed with warnings. Please check your configuration.")
    
    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Setup cancelled by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
