#!/usr/bin/env python3
"""
Quick navigation for ChatKit FastHTML project.
Run: python3 nav.py
"""

import os
import sys

def display_menu():
    """Display main navigation menu."""
    print("\n" + "="*80)
    print("ChatKit FastHTML - Quick Navigation".center(80))
    print("="*80 + "\n")
    
    menu = {
        "1": {
            "title": "📖 Getting Started",
            "items": [
                ("a", "README.md", "Installation & setup guide"),
                ("b", "quickstart.sh", "Automatic setup script"),
                ("c", "FINAL_SUMMARY.txt", "Visual summary"),
            ]
        },
        "2": {
            "title": "🏗️  Architecture & Design",
            "items": [
                ("a", "ARCHITECTURE.md", "Technical architecture"),
                ("b", "CODE_COMPARISON.md", "Next.js vs FastHTML"),
                ("c", "MIGRATION_GUIDE.md", "Migration from Next.js"),
            ]
        },
        "3": {
            "title": "🚀 Deployment & Ops",
            "items": [
                ("a", "DEPLOYMENT.md", "8 deployment platforms"),
                ("b", "Dockerfile", "Docker configuration"),
                ("c", "docker-compose.yml", "Local development"),
            ]
        },
        "4": {
            "title": "💻 Code & Development",
            "items": [
                ("a", "app/main.py", "FastHTML app (150 LOC)"),
                ("b", "app/routes.py", "API handlers (140 LOC)"),
                ("c", "app/config.py", "Configuration (120 LOC)"),
                ("d", "app/session.py", "Session management (160 LOC)"),
            ]
        },
        "5": {
            "title": "🔧 Tools & Scripts",
            "items": [
                ("a", "Makefile", "Development commands"),
                ("b", "docs-index.py", "Documentation index"),
                ("c", "pyproject.toml", "Project configuration"),
            ]
        },
        "6": {
            "title": "📊 Statistics & Summaries",
            "items": [
                ("a", "PROJECT_SUMMARY.md", "Project overview"),
                ("b", "STATISTICS.md", "Detailed metrics"),
                ("c", "REFACTORING_SUMMARY.md", "Refactoring summary"),
            ]
        },
        "7": {
            "title": "🎓 Advanced",
            "items": [
                ("a", "ADVANCED_EXAMPLES.md", "12 extension examples"),
                ("b", "PROJECT_LOCATION.md", "File locations"),
                ("c", ".env.example", "Environment template"),
            ]
        },
    }
    
    for key, section in menu.items():
        print(f"{key}. {section['title']}")
        for subkey, filename, description in section['items']:
            print(f"   {subkey}. {filename:25} - {description}")
        print()
    
    print("Q. Quit")
    print("="*80 + "\n")

def open_file(filename):
    """Open a file for viewing."""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filename}")
        return False
    
    # Use system viewer
    if sys.platform == "linux" or sys.platform == "darwin":
        os.system(f"less -R '{filepath}'")
    else:
        print(f"Opening: {filepath}\n")
        with open(filepath) as f:
            print(f.read())
    
    return True

def main():
    """Main navigation loop."""
    while True:
        display_menu()
        
        choice = input("Select an option: ").strip().upper()
        
        if choice == "Q":
            print("Goodbye! 👋")
            break
        
        # Handle main menu choices
        menu_items = {
            "1": {
                "a": "README.md",
                "b": "quickstart.sh",
                "c": "FINAL_SUMMARY.txt",
            },
            "2": {
                "a": "ARCHITECTURE.md",
                "b": "CODE_COMPARISON.md",
                "c": "MIGRATION_GUIDE.md",
            },
            "3": {
                "a": "DEPLOYMENT.md",
                "b": "Dockerfile",
                "c": "docker-compose.yml",
            },
            "4": {
                "a": "app/main.py",
                "b": "app/routes.py",
                "c": "app/config.py",
                "d": "app/session.py",
            },
            "5": {
                "a": "Makefile",
                "b": "docs-index.py",
                "c": "pyproject.toml",
            },
            "6": {
                "a": "PROJECT_SUMMARY.md",
                "b": "STATISTICS.md",
                "c": "REFACTORING_SUMMARY.md",
            },
            "7": {
                "a": "ADVANCED_EXAMPLES.md",
                "b": "PROJECT_LOCATION.md",
                "c": ".env.example",
            },
        }
        
        if choice in menu_items:
            subchoice = input("Select file: ").strip().lower()
            
            if subchoice in menu_items[choice]:
                filename = menu_items[choice][subchoice]
                print(f"\nOpening: {filename}...\n")
                open_file(filename)
        
        input("\n[Press Enter to continue...]")

if __name__ == "__main__":
    main()
