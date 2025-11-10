#!/usr/bin/env python3
"""
Enhanced Supervisor for Codebase Genius
"""
from utils.git_cloner import GitCloner
from pathlib import Path
from datetime import datetime
import json

class EnhancedSupervisor:
    def __init__(self):
        self.cloner = GitCloner()
    
    def analyze_repository(self, repo_url: str) -> dict:
        print(f"Analyzing repository: {repo_url}")
        
        clone_result = self.cloner.clone_repository(repo_url)
        
        if not clone_result['success']:
            return clone_result
        
        analysis = self.enhanced_analysis(clone_result)
        documentation = self.generate_comprehensive_docs(clone_result, analysis)
        output_path = self.save_results(clone_result['repo_name'], documentation, analysis)
        
        return {
            "success": True,
            "repo_name": clone_result['repo_name'],
            "output_path": str(output_path),
            "file_count": clone_result['file_count'],
            "analysis": analysis
        }
    
    def enhanced_analysis(self, clone_result: dict) -> dict:
        analysis = {
            "languages": {},
            "total_size": 0,
            "has_tests": False,
            "has_docs": False
        }
        
        for file in clone_result['file_tree']:
            lang = file['language']
            analysis["languages"][lang] = analysis["languages"].get(lang, 0) + 1
            analysis["total_size"] += file['size']
            
            if 'test' in file['path'].lower():
                analysis["has_tests"] = True
            if 'docs' in file['path'].lower():
                analysis["has_docs"] = True
        
        return analysis
    
    def generate_comprehensive_docs(self, clone_result: dict, analysis: dict) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        doc = f"# {clone_result['repo_name']} - Comprehensive Documentation\n\n"
        doc += f"*Generated on {timestamp}*\n\n"
        
        doc += "## Repository Overview\n\n"
        doc += f"- **Files**: {clone_result['file_count']}\n"
        doc += f"- **Size**: {analysis['total_size'] / 1024:.1f} KB\n"
        doc += f"- **README**: {clone_result['readme_found']}\n"
        
        doc += "\n## Languages Used:\n"
        for lang, count in analysis['languages'].items():
            doc += f"- **{lang}**: {count} files\n"
        
        doc += "\n## File Structure\n```\n"
        for file in clone_result['file_tree'][:15]:
            doc += f"{file['path']} ({file['language']})\n"
        doc += "```\n"
        
        if clone_result['readme_found']:
            doc += f"\n## README Preview\n{clone_result['readme_preview']}\n"
        
        return doc
    
    def save_results(self, repo_name: str, documentation: str, analysis: dict) -> Path:
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)
        
        docs_file = output_dir / f"{repo_name}_enhanced_docs.md"
        docs_file.write_text(documentation)
        
        analysis_file = output_dir / f"{repo_name}_analysis.json"
        analysis_file.write_text(json.dumps(analysis, indent=2))
        
        return docs_file

def main():
    supervisor = EnhancedSupervisor()
    test_repo = "https://github.com/psf/requests"
    
    print("Enhanced Supervisor")
    result = supervisor.analyze_repository(test_repo)
    
    if result['success']:
        print(f"Success: {result['repo_name']}")
        print(f"Output: {result['output_path']}")
        print(f"Files: {result['file_count']}")

if __name__ == "__main__":
    main()
