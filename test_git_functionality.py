#!/usr/bin/env python3
"""Test script to verify git functionality."""

import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from yx_cc.integrations.git_handler import GitHandler

def test_git_handler():
    """Test the GitHandler functionality."""
    handler = GitHandler()
    
    print("Testing GitHandler functionality...")
    
    try:
        # Test getting current branch
        current_branch = handler._get_current_branch_from_git()
        print(f"✓ Current branch: {current_branch}")
        
        # Test fetch origin
        print("Fetching from origin...")
        fetch_success = handler.fetch_origin()
        print(f"✓ Fetch successful: {fetch_success}")
        
        # Test branch diff (using master as base and current branch)
        base_branch = "master"
        target_branch = current_branch
        
        if target_branch != base_branch:
            print(f"Getting diff between {base_branch} and {target_branch}...")
            diff_summary = handler.get_branch_diff_summary(base_branch, target_branch)
            print(f"✓ Diff summary: {len(diff_summary['changed_files'])} files changed")
            
            if diff_summary['changed_files']:
                print("Changed files:")
                for file_info in diff_summary['changed_files'][:5]:  # Show first 5 files
                    print(f"  {file_info['status']}: {file_info['filename']}")
                
                if len(diff_summary['changed_files']) > 5:
                    print(f"  ... and {len(diff_summary['changed_files']) - 5} more files")
        else:
            print(f"Current branch is {base_branch}, cannot compare with itself")
        
        print("\n✓ All tests completed successfully!")
        
    except Exception as e:
        print(f"✗ Error during testing: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_git_handler()