# Crawlab + CapSolver Integration Guide

[![GitHub license](https://img.shields.io/github/license/capsolver/crawlab-capsolver-integration)](https://github.com/capsolver/crawlab-capsolver-integration/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/capsolver/crawlab-capsolver-integration)](https://github.com/capsolver/crawlab-capsolver-integration/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/capsolver/crawlab-capsolver-integration)](https://github.com/capsolver/crawlab-capsolver-integration/issues)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Node.js Version](https://img.shields.io/badge/node-16%2B-green)](https://nodejs.org/)

> **Automated CAPTCHA Solving for Distributed Crawling.** Integrate [CapSolver](https://www.capsolver.com/?utm_source=github&utm_medium=blog&utm_campaign=crawlab-capsolver) with [Crawlab](https://github.com/crawlab-team/crawlab) to build enterprise-grade crawling systems that bypass reCAPTCHA, Cloudflare Turnstile, and more.

---

## 📖 Table of Contents

- [Introduction](#-introduction)
- [Key Features](#-key-features)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Integration Examples](#-integration-examples)
  - [Selenium + reCAPTCHA v2](#selenium--recaptcha-v2)
  - [Cloudflare Turnstile](#cloudflare-turnstile)
  - [Scrapy Middleware](#scrapy-middleware)
  - [Node.js + Puppeteer](#nodejs--puppeteer)
- [Best Practices](#-best-practices)
- [Troubleshooting](#-troubleshooting)
- [Bonus Code](#-bonus-code)
- [License](#-license)

---

## 🚀 Introduction

Managing web crawlers at scale requires robust infrastructure. **Crawlab** is a powerful distributed web crawler management platform, while **CapSolver** provides AI-powered CAPTCHA solving services. This repository provides ready-to-use templates to integrate these two powerhouses.

### What is Crawlab?
[Crawlab](https://github.com/crawlab-team/crawlab) is a language-agnostic distributed crawler management platform. It supports Python, Node.js, Go, and more, allowing you to manage spiders across multiple nodes with a beautiful UI.

### What is CapSolver?
 [CapSolver](https://www.capsolver.com/?utm_source=github&utm_medium=blog&utm_campaign=crawlab-capsolver) is an AI-driven service that solves various CAPTCHAs including reCAPTCHA (v2/v3/Enterprise), Cloudflare Turnstile, and AWS WAF.

---

## ✨ Key Features

- 🌐 **Distributed Support**: Works seamlessly with Crawlab's master/worker architecture.
- 🛠️ **Multi-Framework**: Examples for Selenium, Scrapy, and Puppeteer.
- 🤖 **AI-Powered**: High success rates for modern anti-bot challenges.
- 📈 **Scalable**: Handle thousands of CAPTCHAs per minute.

---

## 📋 Prerequisites

- **Crawlab Instance**: [Installation Guide](https://docs.crawlab.cn/en/guide/installation/)
- **CapSolver API Key**: [Get it here](https://dashboard.capsolver.com/dashboard/overview/?utm_source=github&utm_medium=blog&utm_campaign=crawlab-capsolver)    
- **Environment**: Python 3.8+ or Node.js 16+

```bash
# Install Python dependencies
pip install selenium requests scrapy

# Install Node.js dependencies
npm install puppeteer
```

---

## ⚡ Quick Start

1. **Clone this repo**:
   ```bash
   git clone https://github.com/your-username/crawlab-capsolver-integration.git
   cd crawlab-capsolver-integration
   ```

2. **Set your API Key**:
   ```bash
   export CAPSOLVER_API_KEY="your-api-key-here"
   ```

3. **Run an example**:
   ```bash
   python examples/selenium_recaptcha_v2.py
   ```

---

## 🛠 Integration Examples

Detailed code examples are located in the [`examples/`](./examples) directory.

### Selenium + reCAPTCHA v2
Automate browser interactions and solve reCAPTCHA v2 challenges.
👉 [View Python Script](./examples/selenium_recaptcha_v2.py)

### Cloudflare Turnstile
Bypass Cloudflare's modern Turnstile challenges with ease.
👉 [View Python Script](./examples/selenium_turnstile.py)

### Scrapy Middleware
Integrate CAPTCHA solving directly into your Scrapy pipelines.
👉 [View Scrapy Spider](./examples/scrapy_spider.py)

### Node.js + Puppeteer
Full support for JavaScript-based crawling environments.
👉 [View Node.js Script](./examples/puppeteer_spider.js)

---

## 💡 Best Practices

| Category | Recommendation |
| :--- | :--- |
| **Error Handling** | Implement exponential backoff for API retries. |
| **Cost Control** | Only trigger the solver when a CAPTCHA is detected. |
| **Performance** | Cache reCAPTCHA tokens (valid for ~2 mins). |
| **Security** | Use environment variables for API keys. |

---

## 🔍 Troubleshooting

| Error Code | Potential Cause | Solution |
| :--- | :--- | :--- |
| `ERROR_ZERO_BALANCE` | Insufficient credits. | Top up your [CapSolver Dashboard](https://dashboard.capsolver.com/dashboard/overview/?utm_source=github). |
| `ERROR_CAPTCHA_UNSOLVABLE` | Incorrect site key or URL. | Verify the parameters extracted from the page. |
| `TimeoutError` | Network latency. | Increase the polling timeout in your script. |

---

## 🎁 Bonus Code

To celebrate this integration, use the code **Crawlab** during your next recharge to receive an **extra 6% credit**!

[**Register on CapSolver Now**](https://dashboard.capsolver.com/dashboard/overview/?utm_source=github&utm_medium=blog&utm_campaign=crawlab-capsolver)

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<p align="center">
  Made with ❤️ by the community
</p>
