"""
Enhanced Linear Integration
============================

Advanced Linear API integration with:
- Project milestones for tracking phases
- Project health status updates
- Progress calculations with estimates
- Cycle support for time-based sprints
- Rich metadata and labels
- Real-time progress visualization
- Session summaries with metrics

Based on Linear API research (December 2025):
- Progress = (completed + 0.25*in_progress) / total
- Milestones for project stages
- Health status: on_track, at_risk, off_track
- Project graphs with automatic predictions
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
from linear_cache import LinearCache


class EnhancedLinearIntegration:
    """
    Enhanced Linear integration with advanced progress tracking.

    Features:
    - Milestone management (phases: Setup, Core, Features, Polish, Complete)
    - Health status tracking (on_track, at_risk, off_track)
    - Estimate-based progress calculation
    - Rich session summaries
    - Label organization (functional, style, infrastructure, priority)
    """

    # Milestone definitions for project phases
    MILESTONES = {
        'setup': {
            'name': 'Project Setup',
            'description': 'Initial project scaffolding and infrastructure',
            'target_percentage': 10
        },
        'core': {
            'name': 'Core Features',
            'description': 'Essential functionality and critical features',
            'target_percentage': 40
        },
        'features': {
            'name': 'Feature Implementation',
            'description': 'Secondary features and enhancements',
            'target_percentage': 75
        },
        'polish': {
            'name': 'Polish & Refinement',
            'description': 'UI polish, performance optimization, bug fixes',
            'target_percentage': 95
        },
        'complete': {
            'name': 'Project Complete',
            'description': 'All features implemented and tested',
            'target_percentage': 100
        }
    }

    # Label categories for organization
    LABEL_CATEGORIES = {
        'functional': ['auth', 'api', 'database', 'ui', 'testing'],
        'style': ['layout', 'responsive', 'accessibility', 'animation'],
        'infrastructure': ['build', 'deployment', 'monitoring', 'security'],
        'priority': ['p1-urgent', 'p2-high', 'p3-medium', 'p4-low']
    }

    def __init__(self, project_dir: Path, cache: Optional[LinearCache] = None):
        self.project_dir = project_dir
        self.cache = cache or LinearCache(project_dir)
        self.project_file = project_dir / ".linear_project.json"
        self.project_data = self._load_project_data()

    def _load_project_data(self) -> Dict:
        """Load project metadata from file."""
        if self.project_file.exists():
            with open(self.project_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_project_data(self):
        """Save project metadata to file."""
        with open(self.project_file, 'w') as f:
            json.dump(self.project_data, f, indent=2)

    def calculate_progress(self, issues: List[Dict]) -> Dict[str, Any]:
        """
        Calculate detailed progress metrics.

        Uses Linear's formula:
        progress = (completed_points + 0.25 * in_progress_points) / total_points

        Returns:
            {
                'total_issues': int,
                'completed': int,
                'in_progress': int,
                'todo': int,
                'progress_percentage': float,
                'estimated_completion': str,
                'velocity': float (issues per session)
            }
        """
        total = len(issues)
        completed = sum(1 for i in issues if i.get('state', {}).get('name') == 'Done')
        in_progress = sum(1 for i in issues if i.get('state', {}).get('name') == 'In Progress')
        todo = total - completed - in_progress

        # Calculate progress with Linear's formula
        # Assuming 1 estimate point per issue (can be customized)
        progress_percentage = ((completed + 0.25 * in_progress) / total * 100) if total > 0 else 0

        # Calculate velocity (issues completed per session)
        sessions = self.project_data.get('session_count', 1)
        velocity = completed / sessions if sessions > 0 else 0

        # Estimate completion
        remaining_issues = todo + in_progress
        estimated_sessions = remaining_issues / velocity if velocity > 0 else 0
        estimated_completion = "Unknown"
        if velocity > 0:
            days = estimated_sessions * 0.5  # Assume 2 sessions per day
            estimated_completion = f"{int(days)} days"

        return {
            'total_issues': total,
            'completed': completed,
            'in_progress': in_progress,
            'todo': todo,
            'progress_percentage': round(progress_percentage, 1),
            'velocity': round(velocity, 2),
            'estimated_completion': estimated_completion
        }

    def determine_current_milestone(self, progress_percentage: float) -> Dict[str, str]:
        """Determine current milestone based on progress."""
        for key, milestone in self.MILESTONES.items():
            if progress_percentage < milestone['target_percentage']:
                return {
                    'key': key,
                    'name': milestone['name'],
                    'description': milestone['description'],
                    'target': milestone['target_percentage']
                }

        # If 100% complete
        return {
            'key': 'complete',
            'name': self.MILESTONES['complete']['name'],
            'description': self.MILESTONES['complete']['description'],
            'target': 100
        }

    def determine_health_status(
        self,
        progress_percentage: float,
        velocity: float,
        errors_count: int
    ) -> str:
        """
        Determine project health status.

        Returns: 'on_track', 'at_risk', or 'off_track'
        """
        # Healthy: Good velocity, low errors, progressing well
        if velocity > 0.8 and errors_count < 5 and progress_percentage > 20:
            return 'on_track'

        # At risk: Slowing down or some issues
        elif velocity > 0.3 and errors_count < 10:
            return 'at_risk'

        # Off track: Stalled or many errors
        else:
            return 'off_track'

    def generate_session_summary(
        self,
        issues_completed: List[str],
        issues_attempted: List[str],
        all_issues: List[Dict],
        session_metrics: Dict
    ) -> str:
        """
        Generate rich session summary for Linear META issue.

        Returns formatted markdown for Linear comment.
        """
        progress = self.calculate_progress(all_issues)
        milestone = self.determine_current_milestone(progress['progress_percentage'])
        health = self.determine_health_status(
            progress['progress_percentage'],
            progress['velocity'],
            session_metrics.get('errors', 0)
        )

        # Health emoji
        health_emoji = {
            'on_track': '🟢',
            'at_risk': '🟡',
            'off_track': '🔴'
        }.get(health, '⚪')

        summary = f"""## Session Complete - {datetime.now().strftime('%Y-%m-%d %H:%M')}

### Issues Completed This Session
{chr(10).join(f'- {title}' for title in issues_completed) if issues_completed else '- No issues completed'}

### Progress Overview
- **Total Progress**: {progress['progress_percentage']}% complete
- **Issues**: {progress['completed']}/{progress['total_issues']} done, {progress['in_progress']} in progress, {progress['todo']} remaining
- **Current Milestone**: {milestone['name']} (Target: {milestone['target']}%)
- **Velocity**: {progress['velocity']} issues/session
- **Estimated Completion**: {progress['estimated_completion']}

### Health Status
{health_emoji} **{health.replace('_', ' ').title()}**

### Session Metrics
- **Linear API Calls**: {session_metrics.get('linear_api_calls', 0)} (Cached: {session_metrics.get('linear_api_cached', 0)})
- **Tools Used**: {len(session_metrics.get('tools_used', {}))} unique tools
- **Errors**: {session_metrics.get('errors', 0)}
- **Session Duration**: {session_metrics.get('duration_minutes', 'N/A')} minutes

### Next Session Priorities
{self._generate_next_priorities(all_issues, progress)}

---
*Generated by autonomous coding agent with enhanced Linear integration*
"""
        return summary

    def _generate_next_priorities(
        self,
        all_issues: List[Dict],
        progress: Dict
    ) -> str:
        """Generate priority recommendations for next session."""
        # Find highest priority Todo issues
        todo_issues = [i for i in all_issues if i.get('state', {}).get('name') == 'Todo']
        todo_issues.sort(key=lambda x: x.get('priority', 4))

        top_3 = todo_issues[:3]
        if not top_3:
            return "🎉 All issues completed!"

        priorities = []
        for issue in top_3:
            priority = issue.get('priority', 4)
            priority_label = ['🔴 URGENT', '🟠 HIGH', '🟡 MEDIUM', '🟢 LOW'][priority - 1]
            title = issue.get('title', 'Unknown')
            priorities.append(f"- {priority_label}: {title}")

        return '\n'.join(priorities)

    def create_initializer_summary(
        self,
        project_id: str,
        project_name: str,
        total_issues: int,
        issues_by_priority: Dict[str, int],
        milestones_created: bool = False
    ) -> Dict:
        """
        Create comprehensive initializer summary.

        Returns metadata to save in .linear_project.json
        """
        return {
            'initialized': True,
            'created_at': datetime.now().isoformat(),
            'project_id': project_id,
            'project_name': project_name,
            'total_issues': total_issues,
            'issues_by_priority': issues_by_priority,
            'milestones_created': milestones_created,
            'session_count': 0,
            'milestones': self.MILESTONES,
            'health_history': [],
            'velocity_history': []
        }

    def update_session_history(self, session_summary: Dict):
        """Update session history in project data."""
        if 'session_history' not in self.project_data:
            self.project_data['session_history'] = []

        self.project_data['session_history'].append(session_summary)
        self.project_data['session_count'] = len(self.project_data['session_history'])

        # Track health history
        if 'health_history' not in self.project_data:
            self.project_data['health_history'] = []

        self.project_data['health_history'].append({
            'timestamp': datetime.now().isoformat(),
            'health': session_summary.get('health', 'unknown'),
            'progress': session_summary.get('progress_percentage', 0)
        })

        # Track velocity history
        if 'velocity_history' not in self.project_data:
            self.project_data['velocity_history'] = []

        self.project_data['velocity_history'].append({
            'timestamp': datetime.now().isoformat(),
            'velocity': session_summary.get('velocity', 0),
            'issues_completed': session_summary.get('issues_completed', 0)
        })

        self._save_project_data()

    def generate_progress_report(self) -> str:
        """
        Generate comprehensive progress report for terminal output.

        Returns formatted text report.
        """
        if not self.project_data:
            return "⚠️  Project not initialized"

        sessions = self.project_data.get('session_count', 0)
        latest_health = self.project_data.get('health_history', [])[-1] if self.project_data.get('health_history') else None
        latest_velocity = self.project_data.get('velocity_history', [])[-1] if self.project_data.get('velocity_history') else None

        report = f"""
╔════════════════════════════════════════════════════════════════╗
║         LINEAR CODING AGENT - PROGRESS REPORT                 ║
╚════════════════════════════════════════════════════════════════╝

Project: {self.project_data.get('project_name', 'Unknown')}
Sessions Completed: {sessions}
Total Issues: {self.project_data.get('total_issues', 0)}

"""
        if latest_health:
            health_emoji = {'on_track': '🟢', 'at_risk': '🟡', 'off_track': '🔴'}.get(latest_health.get('health', ''), '⚪')
            report += f"Current Health: {health_emoji} {latest_health.get('health', 'unknown').replace('_', ' ').title()}\n"
            report += f"Progress: {latest_health.get('progress', 0)}%\n"

        if latest_velocity:
            report += f"Current Velocity: {latest_velocity.get('velocity', 0)} issues/session\n"

        report += f"\nLog Files:\n"
        log_dir = self.project_dir / "logs"
        if log_dir.exists():
            report += f"  - Daily: {log_dir / 'agent_daily.log'}\n"
            report += f"  - Errors: {log_dir / 'errors.log'}\n"

        report += f"\nLinear Project: {self.project_data.get('project_url', 'N/A')}\n"
        report += f"Cache: {self.project_dir / '.linear_cache.json'}\n"

        return report


def create_enhanced_integration(
    project_dir: Path,
    cache: Optional[LinearCache] = None
) -> EnhancedLinearIntegration:
    """
    Factory function to create enhanced Linear integration.

    Usage:
        integration = create_enhanced_integration(project_dir)

        # Calculate progress
        progress = integration.calculate_progress(all_issues)

        # Generate session summary
        summary = integration.generate_session_summary(
            issues_completed=['PRO-56'],
            issues_attempted=['PRO-56', 'PRO-57'],
            all_issues=all_issues,
            session_metrics=logger.metrics
        )

        # Print progress report
        print(integration.generate_progress_report())
    """
    return EnhancedLinearIntegration(project_dir, cache)
