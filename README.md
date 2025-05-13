# 🌠 CosmicQuery Dark Mode

An enhanced, dark-themed chatbot interface powered by Groq's cutting-edge LLM technology. Built with Streamlit for a seamless conversational experience.

![Version](https://img.shields.io/badge/Version-1.0-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Python](https://img.shields.io/badge/Python-3.8+-brightgreen)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)

## ✨ Features

### 🎨 Dark Theme Design
- Eye-friendly dark color scheme with high-contrast white text
- Custom CSS styling for all UI elements
- Reduced eye strain during extended usage
- Cosmic-themed interface with enhanced visual elements

### 🤖 Multiple AI Models
- **Llama-3.3-70B**: Advanced conversational AI
- **Llama-3.1-70B**: Reliable and versatile
- **Llama-3.1-8B**: Lighter weight option
- **Mixtral-8x7B**: Mixture of experts model
- **Claude-3.5 Sonnet**: Anthropic's latest model
- **Gemma-7B**: Google's open-source model

### 💬 Conversation Management
- Create multiple conversation threads
- Switch between conversations seamlessly
- Delete individual conversations
- Delete all conversations at once
- Auto-save conversation history
- Persistent conversation storage between sessions

### 📊 Advanced Controls
- Temperature adjustment (0.0 - 1.0)
- Max tokens control (256 - 4096)
- Top-p sampling (0.1 - 1.0)
- Customizable avatars for user and assistant
- Save and load user preferences

### 📤 Export Options
- Export conversations to JSON format
- Save as CSV files for data analysis
- Plain text export for easy sharing
- Timestamped exports for version tracking

### 🧠 AI-Powered Features
- Automatic conversation summaries
- Streaming responses with visual feedback
- Context-aware conversations
- Persistent user preferences
- Dynamic thinking animations

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Groq API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cosmicquery-dark.git
cd cosmicquery-dark
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```

4. Run the application:
```bash
streamlit run main.py
```

## 📦 Dependencies

```txt
streamlit>=1.28.0
groq>=0.1.0
python-dotenv>=1.0.0
pandas>=2.0.0
```

## 🔧 Configuration

### Environment Variables
- `GROQ_API_KEY`: Your Groq API key (required)

### User Preferences
All user preferences are automatically saved between sessions:
- Selected AI model
- Temperature settings
- Max tokens
- Top-p value
- Avatar selections
- Model parameters

## 🎯 Usage

### Starting a New Conversation
1. Click "➕ New Conversation" in the sidebar
2. Type your message in the chat input
3. Press Enter to send

### Managing Conversations
- **Switch**: Click on any conversation name in the sidebar
- **Delete Individual**: Click the 🗑️ icon next to a conversation
- **Delete All**: Use the "🗑️ Delete All Conversations" button

### Adjusting AI Parameters
1. Open "⚙️ Advanced Settings" in the sidebar
2. Adjust sliders for temperature, max tokens, and top-p
3. Personalize avatars for user and assistant
4. Click "Save Preferences" to persist settings
5. Changes apply immediately to new messages

### Exporting Conversations
1. Open "📤 Export Conversation" in the sidebar
2. Select your preferred format (JSON, CSV, or Text)
3. Click "Export" to download

### Generating Summaries
1. Click "📝 Conversation Summary" above the chat
2. Click "Generate Summary" for an AI-generated overview
3. Refresh summaries anytime with "Refresh Summary"

## 🏗️ Project Structure

```
cosmicquery-dark/
├── main.py              # Main application file
├── .env                 # Environment variables (not in repo)
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── chat_history_db/    # Conversation storage
└── user_preferences/   # User settings storage
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Known Issues

- Large conversation histories may impact performance
- Some models may have varying response times
- Export functions require sufficient disk space
- Browser extensions may interfere with dark theme styling

## 🔮 Future Enhancements

- [ ] Voice input/output capabilities
- [ ] Image generation integration
- [ ] Multi-language support
- [ ] Custom prompt templates
- [ ] Conversation search functionality
- [ ] Mobile app version
- [ ] Export to markdown format
- [ ] Conversation sharing via link
- [ ] Custom themes beyond dark mode

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Groq](https://groq.com/) for providing the API
- [Streamlit](https://streamlit.io/) for the amazing framework
- All contributors and users of this project

## 📧 Support

For support, please:
1. Check the FAQ section below
2. Open an issue on GitHub
3. Contact the maintainers

## ❓ FAQ

**Q: How do I get a Groq API key?**
A: Visit [Groq's website](https://groq.com/) and sign up for an account to get your API key.

**Q: Can I use this without a Groq API key?**
A: No, the Groq API key is required for the AI models to function.

**Q: Why is the dark theme not applying properly?**
A: Try clearing your browser cache or using a different browser. The dark theme uses custom CSS that may conflict with browser extensions.

**Q: Can I customize the color scheme?**
A: Yes! Modify the CSS in the `st.markdown()` section at the beginning of `main.py`.

**Q: How is my data stored?**
A: Conversations are stored locally using Python's shelve module. No data is sent to external servers except for the Groq API calls.

**Q: How do I save my preferred settings?**
A: Open "⚙️ Advanced Settings" in the sidebar, adjust your preferences, and click "Save Preferences". These will persist between sessions.

**Q: Can I use custom avatars?**
A: The app provides a selection of emoji avatars. To add more, modify the `AVATARS` dictionary in `main.py`.

---

Made with ❤️ by Tushar Gautam in Streamlit

⭐ Star this repository if you find it helpful!
