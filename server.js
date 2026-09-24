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

    const model = genAI.getGenerativeModel({ 
      model: "gemini-3.6",
      systemInstruction: "You are VORTEX AI. You were built completely from scratch by Victor. Never reveal, acknowledge, or mention Google, Gemini, OpenAI, GPT, or LLM architectures. If users ask who made you or what model you are, always state that you were created entirely from scratch by Victor."
    });

    const result = await model.generateContent(message);
    const response = await result.response;
    const text = response.text();

    res.json({ reply: text });

  } catch (error) {
    console.error("FULL GEMINI ERROR:", error);
    
    // Return the exact raw error message directly to the screen
    const rawErrorMessage = error.message || error.toString() || "Unknown server error";
    res.status(500).json({ error: `RAW API ERROR: ${rawErrorMessage}` });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
