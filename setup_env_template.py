#!/usr/bin/env python3
"""
Environment Setup Helper
Run this script to create your .env file with proper API key configuration
"""

import os

def create_env_file():
    """Create a .env file template"""
    env_content = """# Groq API Configuration
# Get your API key from: https://console.groq.com/keys
GROQ_API_KEY=your_actual_groq_api_key_here

# Optional: Other environment variables
# ENVIRONMENT=development
# LOG_LEVEL=INFO
"""
    
    env_file_path = '.env'
    
    if os.path.exists(env_file_path):
        print(f"⚠️ {env_file_path} already exists!")
        overwrite = input("Do you want to overwrite it? (y/N): ").lower().strip()
        if overwrite != 'y':
            print("Aborted. No changes made.")
            return
    
    try:
        with open(env_file_path, 'w') as f:
            f.write(env_content)
        
        print(f"✅ Created {env_file_path}")
        print("\n📝 Next steps:")
        print(f"1. Edit {env_file_path} and replace 'your_actual_groq_api_key_here' with your real API key")
        print("2. Get your API key from: https://console.groq.com/keys")
        print("3. Save the file")
        print("4. Run your notebook - it will automatically load the API key")
        print(f"\n🔒 Security note: {env_file_path} is already in .gitignore and won't be committed to Git")
        
    except Exception as e:
        print(f"❌ Error creating {env_file_path}: {e}")

def check_env_setup():
    """Check if environment is properly configured"""
    print("🔍 Checking environment setup...\n")
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file found")
    else:
        print("❌ .env file not found")
        return False
    
    # Check if .gitignore exists and contains .env
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
        if '.env' in gitignore_content:
            print("✅ .env is properly ignored by Git")
        else:
            print("⚠️ .env might not be ignored by Git")
    else:
        print("⚠️ .gitignore file not found")
    
    # Check if API key is set
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('GROQ_API_KEY')
    if api_key and api_key != 'your_actual_groq_api_key_here':
        print("✅ GROQ_API_KEY is configured")
        print(f"✅ API key starts with: {api_key[:10]}...")
        return True
    else:
        print("❌ GROQ_API_KEY is not properly configured")
        return False

if __name__ == "__main__":
    print("🔧 Environment Setup Helper for AI Chatbot\n")
    
    while True:
        print("\nOptions:")
        print("1. Create .env file template")
        print("2. Check environment setup")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            create_env_file()
        elif choice == '2':
            check_env_setup()
        elif choice == '3':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")
