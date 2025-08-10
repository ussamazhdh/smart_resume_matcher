# Smart Resume Matcher - AI-Powered Job Matching Platform

A professional and creative web application that uses AI to match resumes with job opportunities. Built with modern HTML, CSS, and JavaScript, featuring a beautiful user interface and intelligent matching algorithms.

## 🚀 Features

### ✨ Professional Design
- **Modern UI/UX**: Clean, professional design with smooth animations
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile devices
- **Interactive Elements**: Hover effects, smooth transitions, and engaging visuals
- **Beautiful Gradients**: Eye-catching color schemes and visual appeal

### 🧠 Smart Matching Algorithm
- **AI-Powered Analysis**: Advanced skill extraction and matching
- **Real Job Data**: Uses actual job postings from leading platforms
- **Comprehensive Scoring**: Calculates match percentages based on required and nice-to-have skills
- **Visual Indicators**: Color-coded skill tags showing matched vs. missing skills

### 📊 Rich Results Display
- **Match Scoring**: Percentage-based compatibility scores
- **Filtering Options**: Filter results by match level (High, Medium, Low)
- **Detailed Insights**: View job descriptions, requirements, and skill analysis
- **Apply Integration**: Direct links to job application pages

### 🔧 User-Friendly Interface
- **Multiple Input Methods**: Paste resume text or upload files
- **Drag & Drop**: Easy file upload with drag and drop support
- **Real-time Feedback**: Loading animations and success notifications
- **Sample Data**: Built-in sample resume for demonstration

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Custom CSS with Flexbox and Grid layouts
- **Icons**: Font Awesome 6.0
- **Fonts**: Inter (Google Fonts)
- **Data**: JSON-based job and resume datasets

## 📁 Project Structure

```
smart_resume_matcher/
├── index.html          # Main HTML file
├── styles.css          # CSS styling and animations
├── script.js           # JavaScript functionality
├── README.md           # Project documentation
└── data/               # Data directory
    ├── job_descriptions.json    # Job postings data
    ├── resumes_clean.json       # Sample resumes
    ├── resumes_user_raw.txt     # User resume data
    └── README_ADDENDUM.md       # Data documentation
```

## 🚀 How to Run

### Option 1: Simple HTTP Server (Recommended)

1. **Open Terminal/Command Prompt**
2. **Navigate to project directory**:
   ```bash
   cd smart_resume_matcher
   ```

3. **Start a local server**:

   **Using Python 3:**
   ```bash
   python -m http.server 8000
   ```

   **Using Python 2:**
   ```bash
   python -m SimpleHTTPServer 8000
   ```

   **Using Node.js (if you have it installed):**
   ```bash
   npx http-server
   ```

4. **Open your browser** and go to:
   ```
   http://localhost:8000
   ```

### Option 2: Direct File Opening

Simply double-click the `index.html` file to open it in your default browser. However, some features (like file upload) may not work due to browser security restrictions.

## 🎯 How to Use

### 1. **Upload Your Resume**
   - **Paste Method**: Click "Paste Resume" and paste your resume content
   - **File Upload**: Click "Upload File" and select a text file (.txt)
   - **Drag & Drop**: Drag a text file directly onto the upload area

### 2. **Get Matches**
   - Click "Find My Matches" to analyze your resume
   - Wait for the AI to process your information
   - View your personalized job matches

### 3. **Explore Results**
   - **Match Scores**: See percentage compatibility with each job
   - **Skill Analysis**: View which skills match and which are missing
   - **Filter Results**: Use filters to focus on high, medium, or low matches
   - **Apply**: Click "Apply Now" to go to the job application page

### 4. **Sample Data**
   - Click "Load Sample Resume" to see the system in action with example data

## 📊 Matching Algorithm

The application uses a sophisticated matching algorithm that:

1. **Extracts Skills**: Identifies technical skills from resume content
2. **Compares Requirements**: Matches skills against job requirements
3. **Calculates Scores**: 
   - 80% weight for required skills
   - 20% weight for nice-to-have skills
4. **Ranks Results**: Sorts jobs by match percentage

### Skill Recognition
The system recognizes over 50+ technical skills including:
- Programming Languages: Python, JavaScript, Java, C++, etc.
- Frameworks: React, Angular, Django, FastAPI, etc.
- Databases: PostgreSQL, MongoDB, Redis, etc.
- Cloud Platforms: AWS, Azure, GCP
- Tools: Docker, Kubernetes, Git, CI/CD

## 🎨 Design Features

### Visual Elements
- **Gradient Backgrounds**: Beautiful color transitions
- **Floating Animations**: Subtle card animations in hero section
- **Smooth Transitions**: Hover effects and state changes
- **Professional Typography**: Clean, readable fonts

### User Experience
- **Intuitive Navigation**: Clear sections and smooth scrolling
- **Loading States**: Professional loading animations
- **Notifications**: Success, error, and info messages
- **Responsive Design**: Adapts to all screen sizes

## 📱 Mobile Responsiveness

The application is fully responsive and optimized for:
- **Desktop**: Full feature set with optimal layout
- **Tablet**: Adapted layout for medium screens
- **Mobile**: Touch-friendly interface with simplified navigation

## 🔧 Customization

### Adding New Jobs
Edit `data/job_descriptions.json` to add new job postings:

```json
{
  "title": "Job Title",
  "company": "Company Name",
  "location": "Location",
  "requirements": ["Skill 1", "Skill 2"],
  "nice_to_have": ["Bonus Skill 1"],
  "description": "Job description"
}
```

### Modifying Skills
Update the `commonSkills` array in `script.js` to recognize additional skills.

### Styling Changes
Modify `styles.css` to customize colors, fonts, and layout.

## 🚀 Performance Features

- **Fast Loading**: Optimized assets and efficient code
- **Smooth Animations**: 60fps animations using CSS transforms
- **Efficient Matching**: Optimized algorithm for quick results
- **Minimal Dependencies**: Only external fonts and icons

## 📈 Future Enhancements

Potential improvements for the project:
- **PDF Support**: Direct PDF resume parsing
- **Advanced NLP**: More sophisticated text analysis
- **User Accounts**: Save and manage multiple resumes
- **Email Integration**: Send match results via email
- **Analytics Dashboard**: Detailed matching insights

## 🤝 Contributing

This is a demonstration project for academic purposes. Feel free to:
- Fork the repository
- Submit issues and suggestions
- Create pull requests for improvements

## 📄 License

This project is created for educational and demonstration purposes.

## 👨‍💻 Author

Created as a professional project demonstration showcasing modern web development techniques and AI-powered matching algorithms.

---

**Ready to find your perfect job match?** 🚀

Open the application and start your job matching journey today! 