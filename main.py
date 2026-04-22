import os
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import google.generativeai as genai

# 1. Fetch News (Using NewsData.io as a free source)
def get_news():
    api_key = os.getenv("NEWSDATA_API_KEY")
    url = f"https://newsdata.io/api/1/news?apikey={api_key}&language=en&category=top"
    response = requests.get(url).json()
    articles = response.get('results', [])
    return [{"title": a['title'], "link": a['link']} for a in articles[:10]]

# 2. Summarize with Gemini
def summarize_news(articles):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = "Summarize the following news headlines into a daily digest with 1-2 sentences each, keeping the original links: " + str(articles)
    response = model.generate_content(prompt)
    return response.text

# 3. Send Email via Gmail
def send_email(content):
    sender = os.getenv("GMAIL_ADDRESS")
    password = os.getenv("GMAIL_APP_PASSWORD")
    
    msg = MIMEMultipart()
    msg['Subject'] = "Your Daily AI News Summary"
    msg['From'] = sender
    msg['To'] = sender
    msg.attach(MIMEText(content, 'plain'))
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, sender, msg.as_string())

if __name__ == "__main__":
    news = get_news()
    summary = summarize_news(news)
    send_email(summary)
