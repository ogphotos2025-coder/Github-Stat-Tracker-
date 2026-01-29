#!/usr/bin/env python3
"""
GitHub Analytics Dashboard - Data Fetcher
Fetches your GitHub activity data and saves it for visualization
"""

import requests
import json
from datetime import datetime, timedelta
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
        """Fetch basic user information"""
        url = f'{self.base_url}/users/{self.username}'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching user info: {response.status_code}")
            return None
    
    def fetch_repos(self):
        """Fetch all user repositories"""
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
        """Fetch recent events (commits, PRs, issues, etc.)"""
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
        """Analyze programming language usage across repositories"""
        language_stats = defaultdict(int)
        for repo in repos:
            if repo['language']:
                language_stats[repo['language']] += 1
        return dict(language_stats)
    
    def analyze_commit_times(self, events):
        """Analyze when commits are made (hour of day)"""
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
        """Count different types of GitHub activities"""
        activity_types = defaultdict(int)
        for event in events:
            activity_types[event['type']] += 1
        return dict(activity_types)
    
    def get_repo_stats(self, repos):
        """Get repository statistics"""
        total_stars = sum(repo['stargazers_count'] for repo in repos)
        total_forks = sum(repo['forks_count'] for repo in repos)
        
        # Top repos by stars
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
        """Generate complete analytics data"""
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
            'last_updated': datetime.now().isoformat()
        }
        
        return analytics
    
    def save_to_file(self, data, filename='data/analytics.json'):
        """Save analytics data to JSON file"""
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
