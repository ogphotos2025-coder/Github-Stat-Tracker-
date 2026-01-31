#!/usr/bin/env python3
import requests
import json
from datetime import datetime
from collections import defaultdict
import os

class GitHubAnalytics:
    def __init__(self, username, token=None):
        self.username = username
        self.headers = {}
        if token:
            self.headers['Authorization'] = f'token {token}'
        self.base_url = 'https://api.github.com'
    
    def fetch_user_info(self):
        url = f'{self.base_url}/users/{self.username}'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching user info: {response.status_code}")
            return None
    
    def fetch_repos(self):
        repos = []
        page = 1
        while True:
            url = f'{self.base_url}/users/{self.username}/repos?page={page}&per_page=100'
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                break
            data = response.json()
            if not data:
                break
            repos.extend(data)
            page += 1
        return repos
    
    def fetch_events(self, pages=3):
        events = []
        for page in range(1, pages + 1):
            url = f'{self.base_url}/users/{self.username}/events?page={page}&per_page=100'
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                events.extend(response.json())
            else:
                break
        return events
    
    def analyze_languages(self, repos):
        language_stats = defaultdict(int)
        for repo in repos:
            if repo['language']:
                language_stats[repo['language']] += 1
        return dict(language_stats)
    
    def analyze_commit_times(self, events):
        commit_hours = defaultdict(int)
        commit_days = defaultdict(int)
        for event in events:
            if event['type'] == 'PushEvent':
                created_at = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                hour = created_at.hour
                day = created_at.strftime('%A')
                commit_hours[hour] += 1
                commit_days[day] += 1
        return dict(commit_hours), dict(commit_days)
    
    def analyze_activity_types(self, events):
        activity_types = defaultdict(int)
        for event in events:
            activity_types[event['type']] += 1
        return dict(activity_types)

    def analyze_monthly_commits(self, events, months=12):
        counts = defaultdict(int)
        for event in events:
            if event['type'] == 'PushEvent':
                created_at = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                key = created_at.strftime('%Y-%m')
                commits = len(event.get('payload', {}).get('commits', []))
                counts[key] += commits or 1

        now = datetime.utcnow()
        for i in range(months):
            m = (now.replace(day=1) - timedelta(days=30 * i)).strftime('%Y-%m')
            counts.setdefault(m, 0)
        return dict(sorted(counts.items()))

    def analyze_pr_stats(self, events):
        total_prs = 0
        merged_prs = 0
        merge_durations = []
        for event in events:
            if event['type'] == 'PullRequestEvent':
                pr = event.get('payload', {}).get('pull_request') or {}
                total_prs += 1
                if event.get('payload', {}).get('action') in ('closed',) and pr.get('merged'):
                    merged_prs += 1
                    try:
                        created = datetime.strptime(pr['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                        closed = datetime.strptime(pr['closed_at'], '%Y-%m-%dT%H:%M:%SZ')
                        merge_durations.append((closed - created).total_seconds() / 3600.0)
                    except Exception:
                        pass
        merge_rate = (merged_prs / total_prs) if total_prs else None
        avg_time = (sum(merge_durations) / len(merge_durations)) if merge_durations else None
        return {
            'total_prs': total_prs,
            'merged_prs': merged_prs,
            'merge_rate': merge_rate,
            'avg_time_to_merge_hours': round(avg_time, 1) if avg_time else None
        }

    def analyze_repo_health(self, repos):
        owner = None
        has_readme = 0
        has_ci = 0
        has_tests = 0
        has_license = 0
        for repo in repos:
            if not owner:
                owner = repo.get('owner', {}).get('login')
            if repo.get('license'):
                has_license += 1
            repo_name = repo['name']
            base = f"{self.base_url}/repos/{repo.get('owner', {}).get('login')}/{repo_name}/contents"
            try:
                r = requests.get(f"{base}/README.md", headers=self.headers)
                if r.status_code == 200:
                    has_readme += 1
            except Exception:
                pass
            try:
                r = requests.get(f"{base}/.github/workflows", headers=self.headers)
                if r.status_code == 200:
                    has_ci += 1
            except Exception:
                pass
            try:
                r = requests.get(f"{base}/tests", headers=self.headers)
                if r.status_code == 200:
                    has_tests += 1
                else:
                    r2 = requests.get(f"{base}/test", headers=self.headers)
                    if r2.status_code == 200:
                        has_tests += 1
            except Exception:
                pass
        return {
            'has_readme': has_readme,
            'has_ci': has_ci,
            'has_tests': has_tests,
            'has_license': has_license,
            'total_repos_checked': len(repos)
        }

    def get_repo_stats(self, repos):
        total_stars = sum(repo['stargazers_count'] for repo in repos)
        total_forks = sum(repo['forks_count'] for repo in repos)
        top_repos = sorted(repos, key=lambda x: x['stargazers_count'], reverse=True)[:5]
        top_repos_data = [
            {
                'name': repo['name'],
                'stars': repo['stargazers_count'],
                'forks': repo['forks_count'],
                'language': repo['language']
            }
            for repo in top_repos
        ]
        return {
            'total_stars': total_stars,
            'total_forks': total_forks,
            'total_repos': len(repos),
            'top_repos': top_repos_data
        }
    
    def generate_analytics(self):
        print(f"Fetching data for {self.username}...")
        user_info = self.fetch_user_info()
        if not user_info:
            return None
        print("Fetching repositories...")
        repos = self.fetch_repos()
        print("Fetching recent events...")
        events = self.fetch_events(pages=3)
        print("Analyzing data...")
        languages = self.analyze_languages(repos)
        commit_hours, commit_days = self.analyze_commit_times(events)
        activity_types = self.analyze_activity_types(events)
        repo_stats = self.get_repo_stats(repos)

        # MVP additional analytics
        monthly_commits = self.analyze_monthly_commits(events, months=12)
        pr_stats = self.analyze_pr_stats(events)
        repo_health = self.analyze_repo_health(repos)
        monthly_vals = list(monthly_commits.values())
        monthly_avg = (sum(monthly_vals) / len(monthly_vals)) if monthly_vals else 0
        hireability_breakdown = {
            'public_repos': user_info['public_repos'],
            'stars': repo_stats['total_stars'],
            'followers': user_info['followers'],
            'consistency': round(monthly_avg, 1),
            'collaboration': round((pr_stats.get('merge_rate') or 0) * 100, 1)
        }

        analytics = {
            'user': {
                'username': user_info['login'],
                'name': user_info['name'],
                'bio': user_info['bio'],
                'public_repos': user_info['public_repos'],
                'followers': user_info['followers'],
                'following': user_info['following'],
                'created_at': user_info['created_at']
            },
            'languages': languages,
            'commit_hours': commit_hours,
            'commit_days': commit_days,
            'activity_types': activity_types,
            'repo_stats': repo_stats,
            'monthly_commits': monthly_commits,
            'monthly_commits_avg': round(monthly_avg, 1),
            'pr_stats': pr_stats,
            'repo_health': repo_health,
            'hireability_breakdown': hireability_breakdown,
            'last_updated': datetime.now().isoformat()
        }
        return analytics
    
    def save_to_file(self, data, filename='data/analytics.json'):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Data saved to {filename}")

def main():
    print("=" * 50)
    print("GitHub Analytics Dashboard - Data Fetcher")
    print("=" * 50)
    print()
    username = input("Enter your GitHub username: ").strip()
    print("\nOptional: Enter your GitHub Personal Access Token")
    print("(Increases API rate limit from 60 to 5000 requests/hour)")
    print("Leave empty to skip: ")
    token = input().strip() or None
    analytics = GitHubAnalytics(username, token)
    data = analytics.generate_analytics()
    if data:
        analytics.save_to_file(data)
        print("\n✓ Success! Your analytics data has been generated.")
        print("  Open index.html in your browser to view the dashboard.")
    else:
        print("\n✗ Failed to fetch data. Please check your username and try again.")

if __name__ == '__main__':
    main()
