// api/chat.js
// 這裡已經徹底拔除別人的模型，完全預留給你們團隊自研的 AI 大腦！

export default async function handler(req, res) {
  // 1. 處理跨網域限制（CORS），確保你們的前端網頁滑起來不卡頓
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: '請使用 POST 方法傳送訊息' });
  }

  try {
    const { message } = req.body; // 接收使用者在 iOS 26 畫面輸入的對話

    // 2. 這裡直接對接你們團隊未來「自己架設的模型伺服器網址」
    // 等你們的後端同學把模型跑起來後，把下面這個網址換成你們自己的 IP 或雲端網址即可！
    const YOUR_AI_SERVER_URL = 'https://your-team-model.com'; 

    const response = await fetch(YOUR_AI_SERVER_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // 這裡用你們自己模型專屬的安全密鑰，完全不透過別人
        'Authorization': `Bearer ${process.env.MY_OWN_MODEL_KEY}` 
      },
      body: JSON.stringify({
        model: 'omnicore-ai-model', // ← 這裡直接寫上你們自己研發、自己命名的 AI 模型名稱！
        messages: [
          { role: 'developer', content: '你是我們團隊百分之百自主研發的頂級 AI 聊天機器人。' },
          { role: 'user', content: message }
        ],
        temperature: 0.7
      })
    });

    const data = await response.json();

    // 3. 乾乾淨淨地把你們自己 AI 的思考結果吐回給 iOS 26 前端畫面
    if (data.choices && data.choices[0]) {
      const aiReply = data.choices[0].message.content;
      return res.status(200).json({ reply: aiReply });
    } else {
      return res.status(500).json({ error: '自研模型伺服器回應異常' });
    }

  } catch (error) {
    return res.status(500).json({ error: '連線到自研模型失敗: ' + error.message });
  }
}
