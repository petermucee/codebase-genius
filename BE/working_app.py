import streamlit as st
import subprocess
import sys
import os
from pathlib import Path

st.set_page_config(page_title="Codebase Genius", page_icon="📚", layout="wide")

def run_analysis(repo_url):
    """Run backend analysis and return results"""
    try:
        # Run the backend supervisor
        result = subprocess.run([
            sys.executable, "integrated_supervisor.py"
        ], capture_output=True, text=True, cwd="BE")
        
        if result.returncode == 0:
            # Find the generated documentation
            repo_name = repo_url.split("/")[-1]
            docs_file = Path(f"../outputs/{repo_name}_complete_analysis.md")
            
            if docs_file.exists():
                return {
                    "success": True,
                    "output": result.stdout,
                    "documentation": docs_file.read_text(),
                    "docs_path": str(docs_file)
                }
        
        return {
            "success": False,
            "error": result.stderr or "Unknown error",
            "output": result.stdout
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    st.title("📚 Codebase Genius")
    st.markdown("### Full-Stack Documentation System")
    
    # Sidebar
    with st.sidebar:
        st.header("Quick Start")
        if st.button("Test with Requests"):
            st.session_state.repo_url = "https://github.com/psf/requests"
        if st.button("Test with Flask"):
            st.session_state.repo_url = "https://github.com/pallets/flask"
    
    # Main content
    repo_url = st.text_input(
        "GitHub Repository URL:",
        value="https://github.com/psf/requests",
        placeholder="https://github.com/username/repository"
    )
    
    if st.session_state.get("repo_url"):
        repo_url = st.session_state.repo_url
        st.text_input("GitHub URL:", value=repo_url, key="url_input")
    
    if st.button("🚀 Generate Documentation", type="primary"):
        if not repo_url:
            st.error("Please enter a repository URL")
            return
        
        with st.spinner("🔄 Running full analysis pipeline..."):
            result = run_analysis(repo_url)
            
            if result["success"]:
                st.success("✅ Analysis Complete!")
                
                # Show metrics from output
                st.subheader("Analysis Results")
                st.text_area("Backend Output:", result["output"], height=100)
                
                # Show generated documentation
                st.subheader("Generated Documentation")
                st.markdown(result["documentation"])
                
                # Download button
                st.download_button(
                    "📥 Download Documentation",
                    result["documentation"],
                    f"{repo_url.split('/')[-1]}_documentation.md",
                    "text/markdown"
                )
                
                st.info(f"📄 Saved to: {result['docs_path']}")
            else:
                st.error("❌ Analysis Failed")
                st.text_area("Error Details:", result.get("error", "Unknown error"), height=200)

if __name__ == "__main__":
    main()
