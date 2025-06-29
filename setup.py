#!/usr/bin/env python3
"""
Setup script for ASL Recognition App
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"✗ Python {version.major}.{version.minor} detected")
        print("This app requires Python 3.8 or higher")
        return False
    else:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
        return True

def install_dependencies():
    """Install required dependencies"""
    print("\nInstalling dependencies...")
    
    # Upgrade pip first
    if not run_command("python -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing requirements"):
        return False
    
    return True

def create_directories():
    """Create necessary directories"""
    print("\nCreating directories...")
    
    directories = ['templates', 'static', 'models', 'data']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Created directory: {directory}")
        else:
            print(f"✓ Directory already exists: {directory}")
    
    return True

def main():
    """Main setup function"""
    print("ASL Recognition App - Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        print("\n❌ Setup failed: Incompatible Python version")
        return
    
    # Create directories
    if not create_directories():
        print("\n❌ Setup failed: Could not create directories")
        return
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed: Could not install dependencies")
        print("Please try installing manually:")
        print("pip install -r requirements.txt")
        return
    
    print("\n✅ Setup completed successfully!")
    print("\nNext steps:")
    print("1. Test the installation:")
    print("   python test_installation.py")
    print("\n2. Run the simple version (command line):")
    print("   python simple_asl.py")
    print("\n3. Run the full web app:")
    print("   python app.py")
    print("   Then open: http://localhost:5000")
    print("\n4. For help, see README.md")

if __name__ == "__main__":
    main() 