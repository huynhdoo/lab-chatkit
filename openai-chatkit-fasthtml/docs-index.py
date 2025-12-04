#!/usr/bin/env python3
"""
Documentation index for ChatKit FastHTML project.
"""

DOCUMENTATION = {
    "Getting Started": [
        {
            "file": "README.md",
            "description": "Installation, setup, and basic usage",
            "audience": "New users",
            "read_time": "5 min",
        },
        {
            "file": "quickstart.sh",
            "description": "Automated setup script",
            "audience": "Quick setup",
            "read_time": "1 min",
        },
    ],
    "Understanding the Project": [
        {
            "file": "PROJECT_SUMMARY.md",
            "description": "High-level overview and statistics",
            "audience": "Decision makers",
            "read_time": "5 min",
        },
        {
            "file": "ARCHITECTURE.md",
            "description": "Detailed architecture, modules, and design",
            "audience": "Developers",
            "read_time": "15 min",
        },
    ],
    "Code & Implementation": [
        {
            "file": "CODE_COMPARISON.md",
            "description": "Detailed comparison with Next.js original",
            "audience": "Migrating developers",
            "read_time": "10 min",
        },
        {
            "file": "MIGRATION_GUIDE.md",
            "description": "How to migrate from Next.js to FastHTML",
            "audience": "Upgrading users",
            "read_time": "20 min",
        },
        {
            "file": "ADVANCED_EXAMPLES.md",
            "description": "12 advanced usage examples and extensions",
            "audience": "Advanced developers",
            "read_time": "30 min",
        },
    ],
    "Deployment & Operations": [
        {
            "file": "DEPLOYMENT.md",
            "description": "8 deployment platforms and guides",
            "audience": "DevOps/Operators",
            "read_time": "25 min",
        },
        {
            "file": "Makefile",
            "description": "Development commands (test, lint, format, etc)",
            "audience": "Developers",
            "read_time": "5 min",
        },
    ],
    "Configuration Files": [
        {
            "file": ".env.example",
            "description": "Environment variables template",
            "audience": "Configuration",
            "read_time": "2 min",
        },
        {
            "file": "pyproject.toml",
            "description": "Project configuration and dependencies",
            "audience": "Configuration",
            "read_time": "3 min",
        },
        {
            "file": "requirements.txt",
            "description": "Python dependencies",
            "audience": "Setup",
            "read_time": "1 min",
        },
        {
            "file": "Dockerfile",
            "description": "Docker container configuration",
            "audience": "DevOps",
            "read_time": "3 min",
        },
        {
            "file": "docker-compose.yml",
            "description": "Docker Compose for local development",
            "audience": "DevOps",
            "read_time": "3 min",
        },
        {
            "file": "Procfile",
            "description": "Heroku deployment configuration",
            "audience": "Heroku users",
            "read_time": "1 min",
        },
    ],
}

SOURCE_CODE = {
    "app/main.py": {
        "purpose": "FastHTML app definition and HTML routes",
        "lines": "~150",
        "key_functions": ["home()", "create_session()", "health()", "config()"],
    },
    "app/routes.py": {
        "purpose": "HTTP request handlers and business logic",
        "lines": "~140",
        "key_functions": ["handle_create_session()", "handle_health_check()", "handle_config()"],
    },
    "app/config.py": {
        "purpose": "Configuration management and validation",
        "lines": "~120",
        "key_classes": ["ChatKitConfig", "AppConfig", "ThemeConfig"],
    },
    "app/session.py": {
        "purpose": "Session management and API interactions",
        "lines": "~160",
        "key_functions": ["create_chatkit_session()", "create_or_get_session_cookie()"],
    },
    "app/static/styles.css": {
        "purpose": "Application styling",
        "lines": "~250",
        "features": ["Dark mode", "Responsive layout", "Error overlay"],
    },
    "app/static/chatkit.js": {
        "purpose": "Client-side ChatKit initialization",
        "lines": "~100",
        "key_functions": ["initChatKit()", "toggleTheme()"],
    },
}

if __name__ == "__main__":
    print("=" * 80)
    print("ChatKit FastHTML - Documentation Index".center(80))
    print("=" * 80)
    print()
    
    for section, docs in DOCUMENTATION.items():
        print(f"\n📚 {section}")
        print("-" * 80)
        
        for doc in docs:
            print(f"\n  📄 {doc['file']}")
            print(f"     {doc['description']}")
            print(f"     👥 Audience: {doc['audience']}")
            print(f"     ⏱️  Read time: {doc['read_time']}")
    
    print("\n\n")
    print("=" * 80)
    print("Source Code Overview".center(80))
    print("=" * 80)
    
    for file, info in SOURCE_CODE.items():
        print(f"\n📝 {file}")
        print(f"   Purpose: {info['purpose']}")
        print(f"   Size: ~{info['lines']} lines")
        
        if "key_functions" in info:
            print(f"   Key functions: {', '.join(info['key_functions'])}")
        
        if "key_classes" in info:
            print(f"   Key classes: {', '.join(info['key_classes'])}")
        
        if "features" in info:
            print(f"   Features: {', '.join(info['features'])}")
    
    print("\n\n")
    print("=" * 80)
    print("Quick Navigation".center(80))
    print("=" * 80)
    print("""
👉 First time? Start with:
   1. README.md - Get it running
   2. PROJECT_SUMMARY.md - Understand what you have
   3. ARCHITECTURE.md - Learn how it works

🔄 Migrating from Next.js?
   1. MIGRATION_GUIDE.md - Overview of changes
   2. CODE_COMPARISON.md - Side-by-side code comparison
   3. ADVANCED_EXAMPLES.md - Extend functionality

🚀 Ready to deploy?
   1. DEPLOYMENT.md - Choose your platform
   2. Dockerfile - For containerization
   3. README.md "Getting Started" section

💻 Want to extend it?
   1. ARCHITECTURE.md - Understand the structure
   2. ADVANCED_EXAMPLES.md - Real-world examples
   3. Source files in app/ directory

❓ Got issues?
   1. Check ARCHITECTURE.md "Troubleshooting"
   2. Run: make lint, make test
   3. Check logs: make dev (DEBUG=True)
    """)
    
    print("=" * 80)
    print(f"Total documentation: {sum(len(docs) for docs in DOCUMENTATION.values())} guides")
    print(f"Total source files: {len(SOURCE_CODE)} files")
    print("=" * 80)
