// Codebase Genius - Main Entry Point
// Multi-agent system for automated code documentation

import { Walker } from "std.jac";
import { repo_mapper, get_file_tree } from "./agents/repo_mapper.jac";

graph codebase_genius {
    has anchor supervisor;
}

node repository {
    has name;
    has url;
    has local_path;
}

walker supervisor {
    has repo_url;
    has temp_dir = "BE/temp_repos";
    
    with entry {
        std.out("Codebase Genius Supervisor initialized");
        std.out("Target repository: " + repo_url);
        
        // Spawn repository node
        repo_node = spawn here --> node::repository(
            name=repo_url.split("/")[-1],
            url=repo_url,
            local_path=temp_dir + "/" + repo_url.split("/")[-1]
        );
        
        // Delegate to Repo Mapper
        spawn repo_node walker::repo_mapper(
            repo_url=repo_url,
            local_path=repo_node.local_path
        );
        
        report "Supervisor delegated to Repo Mapper";
    }
}

walker generate_docs {
    has input repo_url;
    
    with entry {
        spawn here walker::supervisor(repo_url=repo_url);
    }
}

walker test_repo_mapper {
    has repo_url = "https://github.com/jaseci-labs/jac-sample-apps";
    
    with entry {
        spawn here walker::supervisor(repo_url=repo_url);
    }
}
