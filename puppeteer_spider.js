const puppeteer = require('puppeteer');

const CAPSOLVER_API_KEY = process.env.CAPSOLVER_API_KEY || 'YOUR_CAPSOLVER_API_KEY';
const CAPSOLVER_API = 'https://api.capsolver.com';

class Capsolver {
    constructor(apiKey) {
        this.apiKey = apiKey;
    }

    async createTask(task) {
        const response = await fetch(`${CAPSOLVER_API}/createTask`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                clientKey: this.apiKey,
                task: task
            })
        });
        const result = await response.json();
        if (result.errorId !== 0) throw new Error(result.errorDescription);
        return result.taskId;
    }

    async getTaskResult(taskId, timeout = 120) {
        for (let i = 0; i < timeout; i++) {
            const response = await fetch(`${CAPSOLVER_API}/getTaskResult`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    clientKey: this.apiKey,
                    taskId: taskId
                })
            });
            const result = await response.json();
            if (result.status === 'ready') return result.solution;
            if (result.status === 'failed') throw new Error('Task failed');
            await new Promise(r => setTimeout(r, 1000));
        }
        throw new Error('Timeout');
    }

    async solveRecaptchaV2(url, siteKey) {
        const taskId = await this.createTask({
            type: 'ReCaptchaV2TaskProxyLess',
            websiteURL: url,
            websiteKey: siteKey
        });
        const solution = await this.getTaskResult(taskId);
        return solution.gRecaptchaResponse;
    }

    async solveTurnstile(url, siteKey) {
        const taskId = await this.createTask({
            type: 'AntiTurnstileTaskProxyLess',
            websiteURL: url,
            websiteKey: siteKey
        });
        const solution = await this.getTaskResult(taskId);
        return solution.token;
    }
}

async function crawlWithCaptcha(url) {
    const capsolver = new Capsolver(CAPSOLVER_API_KEY);
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();

    try {
        await page.goto(url, { waitUntil: 'networkidle2' });
        const captchaInfo = await page.evaluate(() => {
            const recaptcha = document.querySelector('.g-recaptcha');
            if (recaptcha) return { type: 'recaptcha', siteKey: recaptcha.dataset.sitekey };
            const turnstile = document.querySelector('.cf-turnstile');
            if (turnstile) return { type: 'turnstile', siteKey: turnstile.dataset.sitekey };
            return null;
        });

        if (captchaInfo) {
            let token;
            if (captchaInfo.type === 'recaptcha') {
                token = await capsolver.solveRecaptchaV2(url, captchaInfo.siteKey);
                await page.evaluate((t) => {
                    const field = document.getElementById('g-recaptcha-response');
                    if (field) field.value = t;
                    document.querySelectorAll('textarea[name="g-recaptcha-response"]').forEach(el => el.value = t);
                }, token);
            } else if (captchaInfo.type === 'turnstile') {
                token = await capsolver.solveTurnstile(url, captchaInfo.siteKey);
                await page.evaluate((t) => {
                    const field = document.querySelector('[name="cf-turnstile-response"]');
                    if (field) field.value = t;
                }, token);
            }
        }
        return await page.evaluate(() => ({ title: document.title, url: window.location.href }));
    } finally {
        await browser.close();
    }
}

const targetUrl = process.argv[2] || 'https://example.com';
crawlWithCaptcha(targetUrl).then(result => console.log(JSON.stringify(result, null, 2))).catch(console.error);
