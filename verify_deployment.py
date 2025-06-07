#!/usr/bin/env python3
"""
Deployment Verification Script
Run this script before deploying to ensure all dependencies work correctly
"""

import sys
import os
from typing import List, Tuple

def test_langchain_imports():
    """Test all LangChain related imports"""
    try:
        from langchain_groq import ChatGroq
        from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
        from langchain_community.chat_message_histories import ChatMessageHistory
        from langchain_core.chat_history import BaseChatMessageHistory
        from langchain_core.runnables.history import RunnableWithMessageHistory
        from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
        from langchain_core.messages import trim_messages
        from langchain_core.runnables import RunnablePassthrough
        print("✅ All LangChain imports successful")
        return True
    except ImportError as e:
        print(f"❌ LangChain import failed: {e}")
        return False

def test_web_framework_imports():
    """Test web framework imports"""
    streamlit_ok = flask_ok = True
    
    try:
        import streamlit as st
        print("✅ Streamlit import successful")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        streamlit_ok = False
    
    try:
        from flask import Flask, request, jsonify
        from flask_cors import CORS
        print("✅ Flask imports successful")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        flask_ok = False
    
    return streamlit_ok and flask_ok

def test_utility_imports():
    """Test utility imports"""
    try:
        import requests
        import httpx
        from dotenv import load_dotenv
        import pydantic
        print("✅ All utility imports successful")
        return True
    except ImportError as e:
        print(f"❌ Utility import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic chatbot functionality without API key"""
    try:
        from langchain_core.messages import HumanMessage
        from langchain_community.chat_message_histories import ChatMessageHistory
        
        # Test message history
        history = ChatMessageHistory()
        history.add_user_message("Test message")
        messages = history.messages
        assert len(messages) == 1
        assert messages[0].content == "Test message"
        
        print("✅ Basic functionality test passed")
        return True
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def check_environment_setup():
    """Check environment setup for deployment"""
    issues = []
    
    # Check Python version
    if sys.version_info < (3, 8):
        issues.append("Python 3.8+ required for deployment")
    else:
        print(f"✅ Python version: {sys.version}")
    
    # Check for common deployment files
    deployment_files = ['requirements.txt', 'streamlit_chatbot.py']
    for file in deployment_files:
        if os.path.exists(file):
            print(f"✅ Found {file}")
        else:
            issues.append(f"Missing {file}")
    
    return len(issues) == 0, issues

def main():
    """Run all deployment checks"""
    print("🚀 DEPLOYMENT VERIFICATION STARTING...
")
    print("=" * 50)
    
    tests = [
        ("LangChain Imports", test_langchain_imports),
        ("Web Framework Imports", test_web_framework_imports),
        ("Utility Imports", test_utility_imports),
        ("Basic Functionality", test_basic_functionality),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"
🔍 Testing {test_name}:")
        result = test_func()
        results.append(result)
    
    print(f"
🔍 Checking Environment Setup:")
    env_ok, env_issues = check_environment_setup()
    results.append(env_ok)
    
    if env_issues:
        for issue in env_issues:
            print(f"❌ {issue}")
    
    print("
" + "=" * 50)
    print("📋 VERIFICATION SUMMARY:")
    
    all_passed = all(results)
    if all_passed:
        print("🎉 ALL TESTS PASSED - READY FOR DEPLOYMENT!")
        print("
📝 Next steps:")
        print("1. Set your GROQ_API_KEY environment variable")
        print("2. Test locally: streamlit run streamlit_chatbot.py")
        print("3. Deploy to your chosen platform")
    else:
        print("❌ SOME TESTS FAILED - FIX ISSUES BEFORE DEPLOYMENT")
        print("
🔧 Recommended actions:")
        print("1. pip install -r requirements-production.txt")
        print("2. Check for any error messages above")
        print("3. Re-run this verification script")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
