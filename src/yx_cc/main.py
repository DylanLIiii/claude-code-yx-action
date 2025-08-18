"""Main CLI entry point for YX-CC PR review tool."""

import os
import sys
import asyncio
from typing import Optional

from .core.pr_reviewer import PRReviewer
from dotenv import load_dotenv

def main():
    """Main CLI entry point."""
    # Load environment variables from .env file
    # Try to load from current directory first, then home directory
    import pathlib
    
    current_dir_env = pathlib.Path.cwd() / '.env'
    home_dir_env = pathlib.Path.home() / '.yx-cc.env'
    
    if current_dir_env.exists():
        load_dotenv(current_dir_env)
    elif home_dir_env.exists():
        load_dotenv(home_dir_env)
    else:
        load_dotenv()  # Try default behavior
    
    import argparse
    
    parser = argparse.ArgumentParser(description='YX-CC PR Review Tool')
    parser.add_argument('--target-branch', default='master', help='Target branch to compare against')
    parser.add_argument('--pr-id', type=int, help='Specific PR local ID to review')
    
    args = parser.parse_args()
    
    try:
        # PR review using YunXiao + Claude Code SDK
        result = asyncio.run(run_pr_review(args))
        print_pr_result(result)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


async def run_pr_review(args):
    """Run PR review asynchronously."""
    pr_reviewer = PRReviewer()
    
    if args.pr_id:
        return await pr_reviewer.review_specific_pr(args.pr_id)
    else:
        return await pr_reviewer.review_current_pr(args.target_branch)


def print_pr_result(result: dict):
    """Print PR review result in a formatted way."""
    print(f"PR Review Status: {result['status']}")
    
    if result['status'] == 'no_changes':
        print(result['message'])
        return
    
    print(f"PR ID: {result['pr_id']}")
    print(f"PR Title: {result['pr_title']}")
    print(f"Comments Posted: {result['comments_posted']}")
    
    if result.get('analysis'):
        print(f"\nAnalysis Summary:")
        print(result['analysis'])
    
    if result.get('comments'):
        print(f"\nComments Posted:")
        for i, comment in enumerate(result['comments'], 1):
            if comment['type'] == 'inline':
                print(f"{i}. [INLINE] {comment['file']}:{comment['line']}")
                print(f"   {comment['content'][:100]}...")
            else:
                print(f"{i}. [GLOBAL] {comment['content'][:100]}...")


if __name__ == "__main__":
    main()