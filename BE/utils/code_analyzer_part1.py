#!/usr/bin/env python3
"""
Code Analyzer for building Code Context Graph
"""
import ast
import os
from pathlib import Path
from typing import Dict, List, Set

class CodeAnalyzer:
    def __init__(self):
        self.functions = {}
        self.classes = {}
        self.imports = {}
        self.function_calls = {}
    
    def analyze_python_file(self, file_path: Path) -> Dict:
        """Analyze a Python file and extract structure"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            analysis = {
                'file_path': str(file_path),
                'functions': [],
                'classes': [],
                'imports': [],
                'function_calls': []
            }
            
            # Extract imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis['imports'].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    for alias in node.names:
                        analysis['imports'].append(f"{module}.{alias.name}")
            
            # Extract functions and classes
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_info = {
                        'name': node.name,
                        'line': node.lineno,
                        'args': [arg.arg for arg in node.args.args],
                        'docstring': ast.get_docstring(node)
                    }
                    analysis['functions'].append(func_info)
                
                elif isinstance(node, ast.ClassDef):
                    class_info = {
                        'name': node.name,
                        'line': node.lineno,
                        'methods': [],
                        'docstring': ast.get_docstring(node)
                    }
                    
                    # Extract methods
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            class_info['methods'].append(item.name)
                    
                    analysis['classes'].append(class_info)
            
            # Extract function calls (basic)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    analysis['function_calls'].append(node.func.id)
            
            return analysis
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return {
                'file_path': str(file_path),
                'functions': [],
                'classes': [],
                'imports': [],
                'function_calls': [],
                'error': str(e)
            }
