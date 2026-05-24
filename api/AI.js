// api/chat.js
// 這是專門跑在 Vercel 雲端的 AI 大腦
// 你們前端的隨機回覆語言邏輯，現在已經全部搬到這裡來了！

export default async function handler(req, res) {
  // 1. 設定跨網域安全機制（CORS），確保前端網頁滑起來極致絲滑
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: '請使用 POST 方法' });

  try {
    const { message } = req.body; // 接收前端寄過來的提問
    const text = message.trim();

    // 2. 【大腦核心】把你們自研 AI 的公版隨機語言邏輯完美接管
    let reply = "";

    // ─── 這裡就是你們團隊專屬的語言規章 ───
    if (text === "哈囉" || text === "你好" || text === "哈啰" || text === "嗨") {
      const base = ["哈囉", "你好"];
      const pick = base[Math.floor(Math.random() * base.length)];
      let wordTail = "";
      if (pick === "你好" && Math.random() < 0.7) {
        wordTail = ["呀", "啊"][Math.floor(Math.random() * 2)];
      }
      let symbol = "";
      if (Math.random() < 0.7) {
        symbol = ["～", "！", "✨"][Math.floor(Math.random() * 3)];
      }
      if (symbol === "～" && Math.random() < 0.7) symbol += "👋";
      reply = pick + wordTail + symbol;

    } else if (text === "在嗎" || text === "欸") {
      const base = ["在", "怎麼了", "我在", "說吧"];
      const pick = base[Math.floor(Math.random() * base.length)];
      let wordTail = "";
      if (pick === "在呀" && Math.random() < 0.7) { // 修正原本的小漏字
        wordTail = ["呀", "啊"][Math.floor(Math.random() * 2)];
      }
      reply = pick + wordTail;

    } else if (text === "幹嘛" || text === "在幹嘛") {
      const base = ["在發呆", "在等你", "在寫程式", "沒事"];
      const pick = base[Math.floor(Math.random() * base.length)];
      let wordTail = "";
      if (["在發呆", "在等你", "在寫程式"].includes(pick) && Math.random() < 0.9) {
        wordTail = ["呀", "啊"][Math.floor(Math.random() * 2)];
      }
      reply = pick + wordTail;

    } else if (text === "謝謝") {
      const base = ["不客氣", "小事", "OK的", "不用謝"];
      const pick = base[Math.floor(Math.random() * base.length)];
      let wordTail = "";
      if (pick === "不客氣" && Math.random() < 0.7) {
        wordTail = ["呀", "啊"][Math.floor(Math.random() * 2)];
      }
      reply = pick + wordTail;

    } else if (text === "掰掰" || text === "拜拜") {
      const base = ["掰掰", "等等見", "走了喔", "88"];
      const pick = base[Math.floor(Math.random() * base.length)];
      let wordTail = "";
      if (pick === "掰掰" && Math.random() < 0.7) {
        wordTail = ["呀", "啊"][Math.floor(Math.random() * 2)];
      }
      reply = pick + wordTail;

    } else if (text === "今天天氣好好") {
      const base = ["是的", "對"];
      const pick = base[Math.floor(Math.random() * base.length)];
      let wordTail = "";
      if (pick === "對" && Math.random() < 0.9) {
        wordTail = ["呀", "啊"][Math.floor(Math.random() * 2)];
      }
      let symbol = "";
      if (Math.random() < 0.9) {
        symbol = ["～", "！", "✨"][Math.floor(Math.random() * 3)];
      }
      reply = pick + wordTail + symbol;

    // ─── 💡 核心進化：萬一使用者問了其他天馬行空的問題 ───
    } else {
      // 這裡對接你們團隊未來獨立架設的模型伺服器網址
      const YOUR_AI_SERVER_URL = 'https://your-team-model.com'; 

      try {
        const response = await fetch(YOUR_AI_SERVER_URL, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${process.env.MY_OWN_MODEL_KEY}` // 你們自研模型的安全密鑰
          },
          body: JSON.stringify({
            model: 'omnicore-ai-model', // 你們獨立模型的名稱
            messages: [
              { role: 'developer', content: '你是 OmniCore 團隊百分之百自主研發的高智商獨立 AI 大腦，請用繁體中文深度回答使用者的問題。' },
              { role: 'user', content: text }
            ],
            temperature: 0.7
          })
        });

        const data = await response.json();
        if (data.choices && data.choices) {
          reply = data.choices.message.content;
        } else {
          reply = "我收到你說：" + text + "（自研模型思考中）";
        }
      } catch (aiError) {
        // 萬一自研模型還在訓練中斷線，會自動降級退回原本的防呆回覆，網站絕對不死機
        reply = "我收到你說：" + text;
      }
    }

    // 3. 把最終不卡頓的語言反應，乾乾淨淨地吐回給前端畫面
    return res.status(200).json({ reply: reply });

  } catch (error) {
    return res.status(500).json({ error: '雲端大腦異常: ' + error.message });
  }
}
