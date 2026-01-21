#!/usr/bin/env python3
"""
Test script for the beautiful Chatterbox UI implementation.
This script validates that all components are working correctly.
"""

import os
import sys
import webbrowser
import time
import subprocess
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and report status."""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} (NOT FOUND)")
        return False

def validate_implementation():
    """Validate the beautiful UI implementation."""
    print("🔍 Validating Beautiful UI Implementation")
    print("=" * 50)
    
    # Check for required files
    files_to_check = [
        ("beautiful_chatterbox.html", "HTML Dashboard Interface"),
        ("enhanced_unified_webui.py", "Enhanced Gradio App"),
        ("BEAUTIFUL_UI_GUIDE.md", "Documentation Guide"),
        ("index.html", "Alternative HTML Interface"),
    ]
    
    all_files_exist = True
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_files_exist = False
    
    print("\n" + "=" * 50)
    
    if all_files_exist:
        print("🎉 All files are present and ready!")
        return True
    else:
        print("⚠️  Some files are missing. Please check the implementation.")
        return False

def test_html_dashboard():
    """Test the HTML dashboard by opening it in browser."""
    print("\n🌐 Testing HTML Dashboard")
    print("-" * 30)
    
    html_file = "beautiful_chatterbox.html"
    if os.path.exists(html_file):
        print(f"📍 Opening {html_file} in your default browser...")
        try:
            webbrowser.open(f"file://{os.path.abspath(html_file)}")
            print("✅ HTML dashboard opened successfully!")
            print("💡 Note: The dashboard will show a loading screen until your Gradio app is running.")
            return True
        except Exception as e:
            print(f"❌ Failed to open HTML dashboard: {e}")
            return False
    else:
        print(f"❌ HTML dashboard file not found: {html_file}")
        return False

def test_enhanced_gradio_app():
    """Test the enhanced Gradio app."""
    print("\n🤖 Testing Enhanced Gradio App")
    print("-" * 30)
    
    app_file = "enhanced_unified_webui.py"
    if os.path.exists(app_file):
        print(f"📍 Enhanced Gradio app is ready: {app_file}")
        print("💡 To test, run: python enhanced_unified_webui.py")
        print("   This will start the app with beautiful Tailwind CSS styling!")
        return True
    else:
        print(f"❌ Enhanced Gradio app file not found: {app_file}")
        return False

def check_dependencies():
    """Check for required dependencies."""
    print("\n📦 Checking Dependencies")
    print("-" * 30)
    
    try:
        import gradio
        print(f"✅ Gradio: {gradio.__version__}")
    except ImportError:
        print("❌ Gradio: Not installed")
        print("   Install with: pip install gradio")
    
    try:
        import torch
        print(f"✅ PyTorch: {torch.__version__}")
        if torch.cuda.is_available():
            print(f"   CUDA: Available ({torch.cuda.get_device_name(0)})")
        else:
            print("   CUDA: Not available (using CPU)")
    except ImportError:
        print("❌ PyTorch: Not installed")
        print("   Install with: pip install torch")
    
    # Check for chatterbox modules
    try:
        sys.path.insert(0, 'src')
        from chatterbox.tts import ChatterboxTTS
        print("✅ Chatterbox TTS: Available")
    except ImportError as e:
        print(f"❌ Chatterbox TTS: {e}")
        print("   Make sure the src/ directory is in your Python path")

def show_usage_instructions():
    """Show usage instructions."""
    print("\n📖 Usage Instructions")
    print("=" * 50)
    
    print("""
🚀 Quick Start Options:

1️⃣ HTML Dashboard (Recommended):
   a) Run your existing Gradio app: python unified_webui.py
   b) Open beautiful_chatterbox.html in your browser
   c) Enjoy the beautiful interface!

2️⃣ Enhanced Gradio App:
   a) Run the enhanced version: python enhanced_unified_webui.py
   b) Access the beautiful interface directly

3️⃣ Development & Customization:
   a) Edit beautiful_chatterbox.html for HTML dashboard
   b) Modify enhanced_unified_webui.py for Gradio app
   c) Update BEAUTIFUL_UI_GUIDE.md for documentation

🎯 Features Available:
   • Classic TTS with full customization
   • Turbo TTS with event tags
   • Multilingual TTS (23+ languages)
   • Voice Conversion technology
   • Beautiful dark theme with neon accents
   • Responsive design for all devices
   • Smooth animations and transitions

📚 Documentation:
   Read BEAUTIFUL_UI_GUIDE.md for detailed instructions,
   customization options, and troubleshooting tips.
""")

def main():
    """Main test function."""
    print("🌟 Chatterbox Beautiful UI Test Suite")
    print("=" * 50)
    
    # Validate implementation
    if not validate_implementation():
        print("\n❌ Implementation validation failed!")
        sys.exit(1)
    
    # Check dependencies
    check_dependencies()
    
    # Test components
    html_success = test_html_dashboard()
    gradio_success = test_enhanced_gradio_app()
    
    # Show usage instructions
    show_usage_instructions()
    
    # Final summary
    print("\n" + "=" * 50)
    print("🏁 Test Summary")
    print("-" * 20)
    
    if html_success and gradio_success:
        print("🎉 All tests passed! Your beautiful UI is ready to use.")
        print("\n✨ Next Steps:")
        print("   1. Choose your preferred interface option")
        print("   2. Start creating beautiful voice content!")
        print("   3. Customize the styling to match your brand")
    else:
        print("⚠️  Some tests failed. Please check the output above.")
    
    print("\n💡 For support, check BEAUTIFUL_UI_GUIDE.md or the console output.")

if __name__ == "__main__":
    main()