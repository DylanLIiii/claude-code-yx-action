"""Main CLI entry point for YX-CC PR review tool."""

import sys
import asyncio

from .core.pr_reviewer import PRReviewer
from .core.output_formatter import OutputFormatter
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
    parser.add_argument('--modes', nargs='+', choices=['summary', 'analysis', 'comments'],
                       default=['summary', 'analysis', 'comments'],
                       help='Review modes to run (default: all phases)')
    parser.add_argument('--force-regenerate', action='store_true',
                       help='Force regeneration of phases even if existing results found')
    parser.add_argument('--update-description', type=str, help='Update the description of a specific PR and exit. Requires --pr-id.')

    args = parser.parse_args()
    
    try:
        pr_reviewer = PRReviewer(modes=args.modes)

        if args.update_description:
            if not args.pr_id:
                print("Error: --update-description requires --pr-id.", file=sys.stderr)
                sys.exit(1)

            result = pr_reviewer.update_pr_description_only(args.pr_id, args.update_description)
            print(result.get('message', 'Operation completed.'))
            sys.exit(0)

        # PR review using YunXiao + Claude Code SDK
        result = asyncio.run(run_pr_review(args, pr_reviewer))
        print_pr_result(result)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


async def run_pr_review(args, pr_reviewer):
    """Run PR review asynchronously."""
    if args.pr_id:
        return await pr_reviewer.review_specific_pr(args.pr_id, args.force_regenerate)
    else:
        return await pr_reviewer.review_current_pr(args.target_branch, args.force_regenerate)


def print_pr_result(result: dict):
    """Print PR review result in a formatted way."""
    print(f"🔍 PR Review Status: {result['status']}")

    if result['status'] == 'no_changes':
        print(f"ℹ️  {result['message']}")
        return

    print(f"📋 PR ID: {result['pr_id']}")
    print(f"📝 PR Title: {result['pr_title']}")

    # Print enabled phases
    if result.get('enabled_phases'):
        print(f"🔧 Enabled Phases: {', '.join(result['enabled_phases'])}")

    print(f"💬 Comments Posted: {result['comments_posted']}")

    # Initialize output formatter for proper markdown formatting
    formatter = OutputFormatter(format_type='markdown')

    # Print summary if available (properly formatted)
    if result.get('summary'):
        print("\n" + "=" * 60)
        try:
            formatted_summary = formatter.format_summary_result(result['summary'])
            print(formatted_summary)
        except Exception as e:
            print("📊 Summary (Raw - formatting failed):")
            print("-" * 50)
            summary_preview = result['summary'][:500] + "..." if len(result['summary']) > 500 else result['summary']
            print(summary_preview)
            print(f"\n_Note: Formatting error: {e}_")

    # Print analysis if available (properly formatted)
    if result.get('analysis'):
        print("\n" + "=" * 60)
        try:
            formatted_analysis = formatter.format_analysis_result(result['analysis'])
            print(formatted_analysis)
        except Exception as e:
            print("🔬 Analysis (Raw - formatting failed):")
            print("-" * 50)
            analysis_preview = result['analysis'][:500] + "..." if len(result['analysis']) > 500 else result['analysis']
            print(analysis_preview)
            print(f"\n_Note: Formatting error: {e}_")

    # Print comments if available (properly formatted)
    if result.get('comments_json'):
        print("\n" + "=" * 60)
        try:
            formatted_comments = formatter.format_comment_result(result['comments_json'])
            print(formatted_comments)
        except Exception as e:
            print("💭 Comments (Raw - formatting failed):")
            print("-" * 50)
            print(str(result.get('comments_json', 'No comments data'))[:500])
            print(f"\n_Note: Formatting error: {e}_")
    elif result.get('comments'):
        # Fallback to old format for backward compatibility
        print("\n💭 Specific Comments Generated:")
        print("-" * 50)
        for i, comment in enumerate(result['comments'], 1):
            if comment.get('file') and comment.get('line'):
                comment_type = comment.get('type', 'COMMENT')
                print(f"{i}. [{comment_type}] {comment['file']}:{comment['line']}")
                content_preview = comment['content'][:100] + "..." if len(comment['content']) > 100 else comment['content']
                print(f"   {content_preview}")
            else:
                print(f"{i}. [GENERAL] {comment.get('content', 'No content')[:100]}...")

    print("\n✅ Review completed! Check the PR comments in YunXiao for full details.")


if __name__ == "__main__":
    main()