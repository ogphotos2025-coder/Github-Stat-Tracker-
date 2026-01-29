# 🚀 Quick Start Guide

## Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or simply:
```bash
pip install requests
```

## Step 2: Preview the Dashboard (Optional)

Open `index.html` in your browser to see the demo dashboard with sample data.

## Step 3: Generate Your Real Data

Run the data fetcher:
```bash
python fetch_data.py
```

When prompted:
1. Enter your GitHub username
2. (Optional) Enter a Personal Access Token for higher rate limits
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - No special permissions needed (you can leave all checkboxes unchecked)
   - Copy the token and paste it when prompted

## Step 4: View Your Dashboard

Refresh `index.html` in your browser - your real data will now be displayed!

## 🔄 Updating Your Data

Simply run the script again:
```bash
python fetch_data.py
```

Then refresh your browser.

## 📌 Tips for First-Time Users

1. **No Token Needed**: You can start without a token, but you're limited to 60 API requests per hour
2. **Token Benefits**: With a token, you get 5000 requests per hour
3. **Data Storage**: All data is stored locally in `data/analytics.json`
4. **Privacy**: Your data never leaves your computer

## 🎯 What's Next?

After getting your dashboard running, try:

1. **Customize the colors** in `index.html` (look for backgroundColor values)
2. **Add new metrics** to `fetch_data.py` (explore the GitHub API)
3. **Schedule automatic updates** (use cron on Linux/Mac or Task Scheduler on Windows)
4. **Deploy to GitHub Pages** (see README.md for instructions)

## ❓ Common Issues

**"Module not found: requests"**
```bash
pip install requests
```

**"Error 404 - User not found"**
- Double-check your GitHub username
- Make sure it's spelled correctly

**"Rate limit exceeded"**
- Wait 1 hour, or
- Use a Personal Access Token

## 🎓 Learning Resources

- GitHub API: https://docs.github.com/en/rest
- Python Requests: https://requests.readthedocs.io/
- Chart.js: https://www.chartjs.org/

---

**Need help?** Check the troubleshooting section in README.md
