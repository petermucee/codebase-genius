import re
from pathlib import Path
from utils.git_cloner import GitCloner

class EnhancedAnalyzer:
    def __init__(self):
        self.cloner = GitCloner()
    
    def analyze_repository(self, repo_url):
        try:
            clone_result = self.cloner.clone_repository(repo_url)
            if not clone_result['success']:
                return clone_result
            
            repo_path = Path(clone_result['local_path'])
            
            analysis = {
                'success': True,
                'repo_name': clone_result['repo_name'],
                'file_count': clone_result['file_count'],
                'readme_found': clone_result['readme_found'],
                'readme_preview': clone_result.get('readme_preview', ''),
                'file_tree': clone_result['file_tree'][:15]
            }
            return analysis
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

def main():
    analyzer = EnhancedAnalyzer()
    result = analyzer.analyze_repository('https://github.com/psf/requests')
    if result['success']:
        print('Analysis successful')
    else:
        print('Analysis failed')

if __name__ == '__main__':
    main()
