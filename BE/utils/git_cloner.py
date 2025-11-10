import os
import subprocess
import shutil
from pathlib import Path

class GitCloner:
    def __init__(self, temp_dir="temp_repos"):
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(exist_ok=True)
        print(f"GitCloner initialized with temp_dir: {self.temp_dir.absolute()}")
    
    def clone_repository(self, repo_url: str) -> dict:
        """Clone a GitHub repository and return basic info"""
        try:
            repo_name = repo_url.rstrip('/').split('/')[-1]
            if repo_name.endswith('.git'):
                repo_name = repo_name[:-4]
            
            clone_path = self.temp_dir / repo_name
            
            print(f"🔄 Cloning {repo_url} to {clone_path}...")
            
            # Remove existing directory if it exists
            if clone_path.exists():
                print(f"Removing existing directory: {clone_path}")
                shutil.rmtree(clone_path)
            
            result = subprocess.run(
                ['git', 'clone', '--depth', '1', repo_url, str(clone_path)],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                file_tree = self.get_file_tree(clone_path)
                readme_content = self.extract_readme(clone_path)
                
                return {
                    "success": True,
                    "repo_name": repo_name,
                    "local_path": str(clone_path),
                    "file_count": len(file_tree),
                    "file_tree": file_tree[:10],
                    "readme_found": bool(readme_content),
                    "readme_preview": readme_content[:200] + "..." if readme_content else None
                }
            else:
                return {"success": False, "error": result.stderr}
                
        except Exception as e:
            print(f"Exception during cloning: {e}")
            return {"success": False, "error": str(e)}
    
    def get_file_tree(self, repo_path: Path) -> list:
        """Generate file tree structure"""
        file_tree = []
        if not repo_path.exists():
            return file_tree
            
        for file_path in repo_path.rglob('*'):
            if file_path.is_file():
                if any(part.startswith('.') for part in file_path.parts):
                    continue
                excluded_dirs = {'.git', '__pycache__', 'node_modules', 'venv'}
                if any(excluded in file_path.parts for excluded in excluded_dirs):
                    continue
                relative_path = file_path.relative_to(repo_path)
                file_tree.append({
                    'path': str(relative_path),
                    'size': file_path.stat().st_size,
                    'language': self._detect_language(file_path)
                })
        return sorted(file_tree, key=lambda x: x['path'])
    
    def extract_readme(self, repo_path: Path) -> str:
        """Extract README content"""
        if not repo_path.exists():
            return ""
        readme_files = ['README.md', 'README.txt', 'README']
        for readme_file in readme_files:
            readme_path = repo_path / readme_file
            if readme_path.exists():
                return readme_path.read_text(encoding='utf-8', errors='ignore')
        return ""
    
    def _detect_language(self, file_path: Path) -> str:
        """Detect programming language from file extension"""
        extensions = {
            '.py': 'python', '.jac': 'jac', '.md': 'markdown',
            '.txt': 'text', '.json': 'json', '.yaml': 'yaml',
            '.yml': 'yaml', '.js': 'javascript', '.html': 'html',
            '.css': 'css', '.java': 'java'
        }
        return extensions.get(file_path.suffix.lower(), 'unknown')

if __name__ == "__main__":
    cloner = GitCloner()
    result = cloner.clone_repository("https://github.com/psf/requests")
    print("Test result:", result["success"])
    if result["success"]:
        print("Files:", result["file_count"])
        print("README:", result["readme_found"])
