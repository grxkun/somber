# Simple To-Do List Application

A clean, responsive web-based To-Do list application built with vanilla HTML, CSS, and JavaScript. Manage your tasks efficiently with features like adding, editing, deleting, and marking tasks as complete, all with persistent storage using browser localStorage.

## Features

### Core Functionality
- ✅ **Add Tasks**: Create new tasks with a simple input field
- ✅ **Edit Tasks**: Click edit to modify existing task text inline
- ✅ **Remove Tasks**: Delete individual tasks with confirmation prompts
- ✅ **Mark Complete/Incomplete**: Toggle task completion status with checkboxes
- ✅ **Persistent Storage**: All tasks are saved in browser localStorage and restored on page reload
- ✅ **Visual Separation**: Completed and incomplete tasks are displayed in separate, clearly labeled sections

### Bonus Features
- 🧹 **Clear Completed Tasks**: Remove all completed tasks at once with confirmation
- 📊 **Task Counter**: Live count of remaining incomplete tasks displayed at the top
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices
- 🎨 **Modern UI/UX**: Clean, intuitive interface with hover effects and smooth transitions

### User Experience
- **Smart Button States**: Add button is disabled when input is empty, Clear Completed is disabled when no completed tasks exist
- **Confirmation Dialogs**: Prompts before deleting tasks or clearing completed tasks
- **Keyboard Support**: Press Enter in the input field to add tasks quickly
- **Edit Mode**: Save/Cancel buttons appear when editing, with keyboard shortcuts (Enter to save, Escape to cancel)
- **Visual Feedback**: Completed tasks are visually distinguished with strikethrough text and reduced opacity

## Screenshots

### Initial State
![Initial State](https://github.com/user-attachments/assets/7ee0348c-fa1e-4e6d-b10e-9ce0582f82ab)

### Application in Use
![Application with Tasks](https://github.com/user-attachments/assets/47972797-689b-4af0-a10c-b210ec7cbc47)

## Getting Started

### Prerequisites
- A modern web browser (Chrome, Firefox, Safari, Edge)
- No additional dependencies or installations required

### Installation & Usage

1. **Clone or download** this repository to your local machine
2. **Open `index.html`** in your web browser
3. **Start managing your tasks!**

#### Alternative: Local Server
For the best experience, serve the files through a local web server:

```bash
# Using Python 3
python3 -m http.server 8000

# Using Node.js (if you have http-server installed)
npx http-server

# Using PHP
php -S localhost:8000
```

Then navigate to `http://localhost:8000` in your browser.

## How to Use

### Adding Tasks
1. Type your task in the "Add a new task..." input field
2. Press **Enter** or click the **"Add Task"** button
3. Your task appears in the "Incomplete Tasks" section

### Managing Tasks
- **Mark as Complete**: Click the checkbox next to any task
- **Edit Task**: Click the **"Edit"** button, modify the text, then click **"Save"** or press Enter
- **Delete Task**: Click the **"Delete"** button and confirm the deletion
- **Cancel Edit**: Click **"Cancel"** or press Escape while editing

### Bulk Operations
- **Clear Completed**: Click the **"Clear Completed"** button to remove all finished tasks
- **Task Counter**: Monitor your progress with the live count at the top

## File Structure

```
├── index.html          # Main HTML structure
├── styles.css          # CSS styling and responsive design
├── script.js           # JavaScript functionality and logic
└── README.md          # This documentation
```

## Technical Details

### Technologies Used
- **HTML5**: Semantic markup and accessibility features
- **CSS3**: Modern styling with Flexbox/Grid layouts, animations, and responsive design
- **Vanilla JavaScript**: ES6+ features, localStorage API, DOM manipulation

### Browser Compatibility
- ✅ Chrome 60+
- ✅ Firefox 55+
- ✅ Safari 12+
- ✅ Edge 79+

### Key JavaScript Features
- **Class-based Architecture**: Organized code structure with TodoApp class
- **Event Delegation**: Efficient event handling for dynamic content
- **LocalStorage Integration**: Automatic save/load with error handling
- **Input Validation**: Prevents empty tasks and handles edge cases
- **XSS Protection**: HTML escaping for user input security

### Responsive Design
- **Mobile-first Approach**: Optimized for touch devices
- **Flexible Layout**: Adapts from mobile (single column) to desktop (two columns)
- **Touch-friendly**: Larger buttons and touch targets on mobile devices

## Code Structure

### HTML Structure
- Semantic HTML5 elements for accessibility
- Clear separation of incomplete and completed task sections
- Form controls with proper labels and ARIA attributes

### CSS Organization
- CSS Reset for cross-browser consistency
- Responsive design with mobile-first approach
- CSS transitions for smooth user interactions
- Color-coded sections (orange for incomplete, green for completed)

### JavaScript Architecture
```javascript
class TodoApp {
    // Core methods
    addTask()           // Add new tasks
    toggleTask()        // Mark complete/incomplete
    editTask()          // Inline editing functionality
    deleteTask()        // Remove individual tasks
    clearCompleted()    // Bulk delete completed tasks
    
    // Storage methods
    saveTasks()         // Save to localStorage
    loadTasks()         // Load from localStorage
    
    // UI methods
    updateUI()          // Refresh display
    createTaskElement() // Generate task HTML
}
```

## Local Storage

Tasks are automatically saved to your browser's localStorage as JSON data. The storage format:

```json
[
  {
    "id": "unique_id_string",
    "text": "Task description",
    "completed": false,
    "createdAt": "2025-01-01T12:00:00.000Z"
  }
]
```

## Customization

### Styling
Modify `styles.css` to customize:
- Colors and themes
- Typography and fonts
- Layout and spacing
- Animation timing

### Functionality
Extend `script.js` to add:
- Task priorities or categories
- Due dates
- Task search/filtering
- Export/import features

## Contributing

This is a simple educational project, but improvements are welcome! Consider:
- Additional features (due dates, priorities, categories)
- Enhanced accessibility features
- Performance optimizations
- Additional themes or customization options

## License

This project is open source and available under the MIT License.

---

**Enjoy organizing your tasks!** 📝✨
