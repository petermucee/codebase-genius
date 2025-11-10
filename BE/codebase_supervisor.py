#!/usr/bin/env python3
"""
Simple Python-based supervisor for Codebase Genius
"""
from utils.git_cloner import GitCloner
from pathlib import Path
from datetime import datetime

class CodebaseSupervisor:
    def __init__(self):
        self.cloner = GitCloner()
    
    def analyze_repository(self, repo_url: str) -> dict:
        """Main analysis pipeline"""
        print(f"🔍 Analyzing repository: {repo_url}")
        
        clone_result = self.cloner.clone_repository(repo_url)
        
        if not clone_result['success']:
            return clone_result
        
        documentation = self.generate_documentation(clone_result)
        output_path = self.save_results(clone_result['repo_name'], documentation)
        
        return {
            "success": True,
            "repo_name": clone_result['repo_name'],
            "output_path": str(output_path),
            "file_count": clone_result['file_count']
        }
    
    def generate_documentation(self, clone_result: dict) -> str:
        """Generate markdown documentation"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        doc = f"# {clone_result['repo_name']} - Codebase Documentation\n\n"
        doc += f"*Generated on {timestamp}*\n\n"
        doc += "## Overview\n"
        doc += f"- **Files**: {clone_result['file_count']}\n"
        doc += f"- **README**: {clone_result['readme_found']}\n\n"
        doc += "## File Structure\n```\n"
        
        for file in clone_result['file_tree'][:10]:
            doc += f"{file['path']} ({file['language']})\n"
        
        doc += "```\n"
        
        if clone_result['readme_found']:
            doc += f"\n## README\n{clone_result['readme_preview']}\n"
        
        return doc
    
    def save_results(self, repo_name: str, documentation: str) -> Path:
        """Save documentation to file"""
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / f"{repo_name}_docs.md"
        output_file.write_text(documentation)
        return output_file

def main():
    supervisor = CodebaseSupervisor()
    test_repo = "https://github.com/psf/requests"
    
    print("🚀 Codebase Genius - Python Supervisor")
    result = supervisor.analyze_repository(test_repo)
    
    if result['success']:
        print(f"✅ Success: {result['repo_name']}")
        print(f"📄 Output: {result['output_path']}")
    else:
        print(f"❌ Failed")

if __name__ == "__main__":
    main()
