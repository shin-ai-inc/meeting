// ===========================================================
// ShinAI 30分相談フォーム — Google Apps Script
// ===========================================================
// 設置手順:
//   1. https://script.google.com で新しいプロジェクトを作成
//   2. このコードを貼り付けて保存
//   3. 「デプロイ」→「新しいデプロイ」→ 種類「ウェブアプリ」
//      - 実行するユーザー: 自分
//      - アクセスできるユーザー: 全員
//   4. 表示されたウェブアプリURLをコピー
//   5. public/consult/index.html の GAS_URL を置き換え
// ===========================================================

var TO_EMAIL = 'shinai.life@gmail.com';

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);

    // Honeypot
    if (data.website) {
      return _json({ ok: true });
    }

    var name    = _sanitize(data.name, 100);
    var email   = _sanitize(data.email, 254);
    var company = _sanitize(data.company, 200);
    var dates   = _sanitize(data.dates, 500);
    var message = _sanitize(data.message, 2000);

    if (!name) {
      return _json({ error: 'お名前は必須です' });
    }

    if (!email) {
      return _json({ error: 'メールアドレスは必須です' });
    }

    var subjectLabel = company || name;
    var subject = '30分相談のお申し込み｜' + subjectLabel;

    var now = Utilities.formatDate(
      new Date(),
      'Asia/Tokyo',
      'yyyy/MM/dd HH:mm'
    );

    var body = [
      '30分相談のお申し込みがありました。',
      '',
      'お名前：',
      name,
      '',
      'メールアドレス：',
      email,
      '',
      '会社名：',
      company || '未入力',
      '',
      '直近ご都合の良いお日にち（2～3日）：',
      dates || '未入力',
      '',
      'ご相談内容：',
      message || '未入力',
      '',
      '受付日時：',
      now,
      '',
      '送信元ページ：',
      'https://shinai.vercel.app/consult'
    ].join('\n');

    GmailApp.sendEmail(TO_EMAIL, subject, body, {
      name: 'ShinAI 相談フォーム',
      replyTo: email
    });

    return _json({ ok: true });

  } catch (err) {
    Logger.log('Error: ' + err);
    return _json({ error: '送信に失敗しました' });
  }
}

function _sanitize(str, maxLen) {
  if (!str || typeof str !== 'string') return '';
  return str
    .replace(/[\x00-\x08\x0b\x0c\x0e-\x1f]/g, '')
    .replace(/<[^>]*>/g, '')
    .substring(0, maxLen)
    .trim();
}

function _json(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
