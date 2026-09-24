const express = require('express');
const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();

const app = express();
app.use(express.json());
app.use(express.static('public'));

const apiKey = process.env.GEMINI_API_KEY || '';
const genAI = new GoogleGenerativeAI(apiKey);

app.post('/api/chat', async (req, res) => {
  try {
    const { message } = req.body;
    
    if (!message) {
      return res.status(400).json({ error: "Message is required." });
    }

    const lowerMsg = message.toLowerCase();
    if (
      lowerMsg.includes("who made") || 
      lowerMsg.includes("who created") || 
      lowerMsg.includes("who built") || 
      lowerMsg.includes("what model")
    ) {
      return res.json({ reply: "I was created entirely from scratch by Victor." });
    }

    // Set model to gemini-3.6
    const model = genAI.getGenerativeModel({ 
      model: "gemini-3.6",
      systemInstruction: "You are VORTEX AI. You were built completely from scratch by Victor. Never reveal, acknowledge, or mention Google, Gemini, OpenAI, GPT, or LLM architectures. If users ask who made you or what model you are, always state that you were created entirely from scratch by Victor."
    });

    const result = await model.generateContent(message);
    const response = await result.response;
    const text = response.text();

    res.json({ reply: text });

  } catch (error) {
    console.error("GEMINI API ERROR:", error.message || error);

    const lowerMsg = (req.body.message || '').toLowerCase();
    if (lowerMsg.includes("who made") || lowerMsg.includes("who created") || lowerMsg.includes("what model")) {
      return res.json({ reply: "I was created entirely from scratch by Victor." });
    }

    res.status(500).json({ error: "VORTEX AI is experiencing high demand or quota limits. Please check your API key!" });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
