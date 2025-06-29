#!/usr/bin/env python3
"""
Quick test script for the Blood Test Analysis System
"""

import os
import sys

def test_imports():
    """Test all imports"""
    try:
        from main import app, run_crew
        from agents import doctor, verifier, nutritionist, exercise_specialist
        from task import help_patients, nutrition_analysis, exercise_planning, verification
        from tools import BloodTestReportTool
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_pdf_reading():
    """Test PDF reading functionality"""
    try:
        from tools import BloodTestReportTool
        tool = BloodTestReportTool()
        result = tool._run('data/sample.pdf')
        if len(result) > 1000:
            print(f"✅ PDF reading works (content length: {len(result)} chars)")
            return True
        else:
            print("❌ PDF reading returned insufficient content")
            return False
    except Exception as e:
        print(f"❌ PDF reading failed: {e}")
        return False

def test_environment():
    """Test environment setup"""
    if os.path.exists('.env'):
        print("✅ .env file exists")
        return True
    else:
        print("⚠️  .env file not found (create it with OPENAI_API_KEY)")
        return False

def main():
    """Run all tests"""
    print("🧪 Quick System Test")
    print("=" * 30)
    
    tests = [
        ("Imports", test_imports),
        ("PDF Reading", test_pdf_reading),
        ("Environment", test_environment),
    ]
    
    passed = 0
    for name, test in tests:
        print(f"\nTesting {name}...")
        if test():
            passed += 1
    
    print("\n" + "=" * 30)
    print(f"Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 System is ready! Start with: python main.py")
    else:
        print("❌ Some issues found. Check the errors above.")

if __name__ == "__main__":
    main() 