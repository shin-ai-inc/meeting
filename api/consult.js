const https = require('https');
const http = require('http');

function escapeHtml(str) {
  if (!str) return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;');
}

function sanitize(str, maxLen) {
  if (!str || typeof str !== 'string') return '';
  return str.replace(/[\x00-\x08\x0b\x0c\x0e-\x1f]/g, '').slice(0, maxLen).trim();
}

function buildMailBody(data) {
  const now = new Date().toLocaleString('ja-JP', {
    timeZone: 'Asia/Tokyo',
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit'
  });

  return [
    '30分相談のお申し込みがありました。',
    '',
    'お名前：',
    data.name,
    '',
    '会社名：',
    data.company || '未入力',
    '',
    '直近ご都合の良いお日にち（2～3日）：',
    data.dates || '未入力',
    '',
    'ご相談内容：',
    data.message || '未入力',
    '',
    '受付日時：',
    now,
    '',
    '送信元ページ：',
    'https://shinai.life/consult'
  ].join('\n');
}

function sendEmail(to, subject, body) {
  return new Promise((resolve, reject) => {
    const SENDGRID_API_KEY = process.env.SENDGRID_API_KEY;
    const FROM_EMAIL = process.env.FROM_EMAIL || 'noreply@shinai.life';
    const FROM_NAME = process.env.FROM_NAME || 'ShinAI';

    if (!SENDGRID_API_KEY) {
      console.error('SENDGRID_API_KEY is not set');
      reject(new Error('Mail service not configured'));
      return;
    }

    const payload = JSON.stringify({
      personalizations: [{ to: [{ email: to }] }],
      from: { email: FROM_EMAIL, name: FROM_NAME },
      subject: subject,
      content: [{ type: 'text/plain', value: body }]
    });

    const options = {
      hostname: 'api.sendgrid.com',
      path: '/v3/mail/send',
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + SENDGRID_API_KEY,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload)
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve();
        } else {
          console.error('SendGrid error:', res.statusCode, data);
          reject(new Error('Mail send failed: ' + res.statusCode));
        }
      });
    });

    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', 'https://shinai.life');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(204).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const body = req.body;

  if (!body || typeof body !== 'object') {
    return res.status(400).json({ error: 'Invalid request' });
  }

  // Honeypot
  if (body.website) {
    return res.status(200).json({ ok: true });
  }

  const name = sanitize(body.name, 100);
  const company = sanitize(body.company, 200);
  const dates = sanitize(body.dates, 500);
  const message = sanitize(body.message, 2000);

  if (!name) {
    return res.status(400).json({ error: 'お名前は必須です' });
  }

  const subjectLabel = company || name;
  const subject = `30分相談のお申し込み｜${subjectLabel}`;
  const mailBody = buildMailBody({ name, company, dates, message });
  const to = 'shinai.life@gmail.com';

  try {
    await sendEmail(to, subject, mailBody);
    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('Email send error:', err);
    return res.status(500).json({ error: '送信に失敗しました' });
  }
};
