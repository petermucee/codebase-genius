#!/usr/bin/env python3
"""
Code Analyzer for building Code Context Graph
"""
import ast
from pathlib import Path

class CodeAnalyzer:
    def __init__(self):
        pass
    
    def analyze_python_file(self, file_path: Path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            analysis = {
                'file_path': str(file_path),
                'functions': [],
                'classes': []
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis['functions'].append(node.name)
                elif isinstance(node, ast.ClassDef):
                    analysis['classes'].append(node.name)
            
            return analysis
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_directory(self, directory_path: Path):
        directory_path = Path(directory_path)
        all_analysis = {}
        
        python_files = list(directory_path.rglob("*.py"))
        print(f"Found {len(python_files)} Python files")
        
        # Analyze more files and skip setup.py
        analyzed_count = 0
        for py_file in python_files:
            if 'test' in str(py_file).lower() or '__pycache__' in str(py_file) or 'setup.py' in str(py_file):
                continue
            if analyzed_count >= 5:  # Analyze first 5 meaningful files
                break
            print(f"Analyzing: {py_file.name}")
            analysis = self.analyze_python_file(py_file)
            if analysis.get('functions') or analysis.get('classes'):
                all_analysis[str(py_file.relative_to(directory_path))] = analysis
                analyzed_count += 1
        
        return all_analysis
    
    def generate_code_context_graph(self, analysis_results):
        ccg = {
            'nodes': [],
            'edges': [],
            'statistics': {
                'total_files': len(analysis_results),
                'total_functions': 0,
                'total_classes': 0
            }
        }
        
        for file_path, analysis in analysis_results.items():
            file_node = {
                'id': f"file_{file_path}",
                'type': 'file',
                'label': file_path
            }
            ccg['nodes'].append(file_node)
            
            for func in analysis.get('functions', []):
                ccg['statistics']['total_functions'] += 1
            
            for cls in analysis.get('classes', []):
                ccg['statistics']['total_classes'] += 1
        
        return ccg

def main():
    analyzer = CodeAnalyzer()
    test_dir = Path("../temp_repos/requests")
    
    if test_dir.exists():
        print("Testing Code Analyzer")
        analysis_results = analyzer.analyze_directory(test_dir)
        ccg = analyzer.generate_code_context_graph(analysis_results)
        print(f"Files analyzed: {ccg['statistics']['total_files']}")
        print(f"Functions found: {ccg['statistics']['total_functions']}")
        print(f"Classes found: {ccg['statistics']['total_classes']}")
    else:
        print("Test directory not found")

if __name__ == "__main__":
    main()
