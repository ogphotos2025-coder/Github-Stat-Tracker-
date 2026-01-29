# 📊 GitHub Analytics Dashboard

A beautiful, data-driven dashboard that visualizes your GitHub activity and statistics. Perfect for learning about data MVPs and the GitHub API!

![Dashboard Preview](https://img.shields.io/badge/Status-Ready-green)

## ✨ Features

- **User Statistics**: Repos, followers, stars, and more
- **Language Analysis**: Visual breakdown of your programming languages
- **Commit Patterns**: See when you code most (by hour and day)
- **Activity Types**: Track your different GitHub activities
- **Top Repositories**: Showcase your most starred projects

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- A GitHub account

### Installation

1. **Clone or download this repository**

2. **Install required Python packages**:
```bash
pip install requests
```

3. **Run the data fetcher**:
```bash
python fetch_data.py
```

4. **Enter your GitHub username** when prompted

5. **(Optional) Enter a GitHub Personal Access Token** for higher API rate limits
   - Without token: 60 requests/hour
   - With token: 5000 requests/hour
   - [Create a token here](https://github.com/settings/tokens) (no special permissions needed)

6. **Open `index.html` in your browser** to view your dashboard!

## 📁 Project Structure

```
github-analytics-dashboard/
├── fetch_data.py          # Python script to fetch GitHub data
├── index.html             # Dashboard webpage
├── data/
│   └── analytics.json     # Your generated analytics data
└── README.md             # This file
```

## 🔄 Updating Your Dashboard

To refresh your data with the latest GitHub activity:

```bash
python fetch_data.py
```

Then reload `index.html` in your browser.

## 🎨 Customization Ideas

Want to make this project your own? Here are some ideas:

1. **Add more charts**: 
   - Repository size analysis
   - Issue/PR trends over time
   - Contribution streak tracking

2. **Store historical data**:
   - Save snapshots over time
   - Track growth trends
   - Compare month-over-month

3. **Add filters**:
   - Filter by date range
   - Filter by repository
   - Filter by language

4. **Enhance the UI**:
   - Dark mode toggle
   - Export data as PDF
   - Share card images

## 🛠️ Technologies Used

- **Python**: Data fetching and processing
- **GitHub API**: Data source
- **Chart.js**: Data visualization
- **HTML/CSS/JavaScript**: Frontend dashboard

## 📚 Learning Resources

- [GitHub API Documentation](https://docs.github.com/en/rest)
- [Chart.js Documentation](https://www.chartjs.org/docs/)
- [Python Requests Library](https://requests.readthedocs.io/)

## 🐛 Troubleshooting

**"Error fetching user info"**: 
- Check your username is correct
- Verify your internet connection

**"Rate limit exceeded"**:
- Wait an hour, or
- Use a Personal Access Token

**"No data found in dashboard"**:
- Make sure you've run `fetch_data.py` first
- Check that `data/analytics.json` exists

## 🚀 Deployment

### Deploy to GitHub Pages

1. Create a new GitHub repository
2. Push your code to the repository
3. Run `fetch_data.py` locally and commit the `data/` folder
4. Go to Settings → Pages → Deploy from branch (main)
5. Your dashboard will be live at `https://yourusername.github.io/repo-name`

**Note**: You'll need to manually run `fetch_data.py` and push updates to refresh your data.

## 📝 Next Steps

Ready to level up? Try these challenges:

1. **Automate data updates**: Use GitHub Actions to run the script daily
2. **Add authentication**: Store your token securely in environment variables
3. **Build a backend**: Create an API endpoint to serve fresh data
4. **Multi-user support**: Compare stats with friends
5. **Mobile responsive**: Optimize for phone screens

## 📄 License

MIT License - Feel free to use this project for learning and building!

## 🤝 Contributing

This is a learning project, but if you have ideas or improvements, feel free to:
- Open an issue
- Submit a pull request
- Fork and make it your own

---

**Happy coding!** 🎉

Built as a beginner-friendly data MVP project.
