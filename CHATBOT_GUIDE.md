# AI Style Assistant - User Guide

## Overview
The AI Style Assistant is powered by **Groq API** using the LLaMA 3 70B language model, providing lightning-fast, intelligent responses about nail services, style suggestions, and care tips.

## Features

### 1. Interactive Chat
- Ask any question about nail services, pricing, or care
- Get instant, context-aware responses
- Natural conversation flow with typing indicators
- Beautiful, user-friendly interface

### 2. Quick Suggestions
Pre-loaded question buttons for common queries:
- "What nail services do you offer?"
- "Suggest a design for a wedding"
- "What are trendy summer nail colors?"
- "How do I care for gel nails?"
- "What is the difference between gel and acrylic?"

### 3. AI Style Suggester Tool
Get personalized nail design suggestions based on:
- **Occasion**: Wedding, Holiday, Everyday, Party, Professional
- **Season**: Spring, Summer, Fall, Winter
- **Color Preference**: Pink, Red, Nude, Black, White, Pastel

The AI will generate 3 creative, detailed design suggestions tailored to your criteria.

## How It Works

### Context-Aware Intelligence
The chatbot has access to your live business data:
- All active services with prices and descriptions
- Popular nail styles and trending tags
- Service categories and options

This means responses are always accurate and up-to-date with your actual offerings.

### Example Conversations

**Customer**: "I have a wedding next month. What do you recommend?"

**AI Assistant**: "Congratulations on your upcoming wedding! For a wedding, I'd recommend our Gel Manicure ($40) with elegant nail art. Here are some beautiful options:

1. **Classic French with Subtle Shimmer**: Timeless French tips with a delicate shimmer overlay - perfect for photos
2. **Soft Pink Ombre**: Gentle gradient from nude to blush pink with tiny crystal accents
3. **White Floral Design**: Pure white nails with hand-painted delicate flowers

All of these can last 2-3 weeks, so they'll be perfect through your honeymoon!"

---

**Customer**: "What's the difference between gel and acrylic?"

**AI Assistant**: "Great question! Here's the breakdown:

**Gel Nails** ($40):
- More natural, flexible finish
- Cured under UV light
- Better for natural nail health
- Lasts 2-3 weeks
- Easier removal process

**Acrylic Full Set** ($55):
- Harder, more durable
- Air-dried (no UV needed)
- Great for length and strength
- Lasts 3-4 weeks
- More dramatic looks possible

For everyday wear and nail health, I'd suggest gel. For durability and length, acrylic is your best bet!"

## Technical Details

### API Configuration
- **Provider**: Groq (https://groq.com)
- **Model**: llama3-70b-8192 (enhanced reasoning)
- **Temperature**: 0.7 (balanced creativity)
- **Max Tokens**: 500 (detailed responses)

### Response Speed
Groq's LPU (Language Processing Unit) technology delivers responses in **under 1 second**, creating a seamless conversational experience.

### Data Privacy
- No chat history is stored in the database
- Each conversation is independent
- API calls are encrypted via HTTPS
- Groq API key is securely stored in environment variables

## Best Practices

### For Customers
1. **Be specific**: "I need summer nails for a beach vacation" gets better results than "suggest something"
2. **Ask follow-ups**: The AI can refine suggestions based on your feedback
3. **Mention constraints**: "I work in healthcare" or "I type a lot" helps tailor recommendations

### For Admin
1. Keep your Services table updated - AI uses this data
2. Add descriptive information to services
3. Use relevant tags in your portfolio - AI references popular trends
4. Monitor conversations to understand customer needs

## Customization Options

You can customize the chatbot by editing `app/blueprints/chatbot.py`:

### Change AI Model
```python
model="llama3-70b-8192"  # Current (best quality)
# OR
model="llama3-8b-8192"   # Faster, good for simple queries
# OR
model="mixtral-8x7b-32768"  # Balanced option
```

### Adjust Response Style
```python
temperature=0.7  # Current (balanced)
# Range: 0.0 (very focused) to 1.0 (very creative)
```

### Modify Context
Edit the `get_business_context()` function to add:
- Seasonal promotions
- Special policies
- Booking information
- Care instructions

## Troubleshooting

### "Error processing request"
- Check that GROQ_API_KEY is set in .env
- Verify API key is valid at console.groq.com
- Check internet connection

### Slow Responses
- Groq is typically very fast (<1 second)
- If slow, check your internet connection
- Consider using llama3-8b-8192 for faster responses

### Inaccurate Service Information
- Update your Services table in the database
- AI pulls data from your actual services
- Restart the app after database changes

## Future Enhancements

Possible additions:
- **Chat History**: Save conversations for client reference
- **Appointment Booking**: Direct booking from chat
- **Image Analysis**: Upload nail photos for AI feedback
- **Multi-language**: Support for Spanish, French, etc.
- **Voice Input**: Speak your questions instead of typing

## Support

For Groq API issues: https://console.groq.com/docs
For app-specific questions: Check the main README.md

---

**Enjoy your AI-powered nail salon experience!** 💅✨
