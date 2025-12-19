import os
import subprocess
import sys
import shutil

def build_executable():
    """Build .exe file for CPU Scheduler"""
    
    print("🚀 CPU Scheduler EXE Builder")
    print("=" * 40)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("❌ PyInstaller not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Define paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    main_file = os.path.join(current_dir, "main.py")
    dist_dir = os.path.join(current_dir, "dist")
    
    # Clean previous builds
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
        print("🧹 Cleaned previous builds")
    
    # Build command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=CPU_Scheduler",
        "--clean",
        "--noconfirm",
        f"--workpath={os.path.join(current_dir, 'build')}",
        f"--specpath={current_dir}",
        f"--distpath={dist_dir}",
        f"--add-data={os.path.join(current_dir, 'themes')}{os.pathsep}themes",
        f"--add-data={os.path.join(current_dir, 'ui')}{os.pathsep}ui",
        f"--add-data={os.path.join(current_dir, 'services')}{os.pathsep}services",
        f"--add-data={os.path.join(current_dir, 'utils')}{os.pathsep}utils",
        f"--add-data={os.path.join(current_dir, 'models')}{os.pathsep}models",
        f"--add-data={os.path.join(current_dir, 'algorithms')}{os.pathsep}algorithms",
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=matplotlib",
        "--hidden-import=matplotlib.backends.backend_qtagg",
        "--hidden-import=numpy",
        main_file
    ]
    
    print(f"📦 Building executable...")
    print(f"📁 Source: {main_file}")
    
    # Run PyInstaller
    try:
        subprocess.run(cmd, check=True)
        print("✅ Build completed successfully!")
        
        exe_path = os.path.join(dist_dir, "CPU_Scheduler.exe")
        if os.path.exists(exe_path):
            print(f"📁 Executable location: {exe_path}")
            print(f"📏 File size: {os.path.getsize(exe_path) / (1024*1024):.2f} MB")
        else:
            print("⚠️ Executable not found in expected location")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed with error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    build_executable()
    input("\nPress Enter to exit...")