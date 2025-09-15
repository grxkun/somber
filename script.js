// Todo List Application
class TodoApp {
    constructor() {
        this.tasks = [];
        this.currentEditingId = null;
        this.initializeElements();
        this.loadTasks();
        this.bindEvents();
        this.updateUI();
    }

    // Initialize DOM elements
    initializeElements() {
        this.taskInput = document.getElementById('task-input');
        this.addBtn = document.getElementById('add-btn');
        this.clearCompletedBtn = document.getElementById('clear-completed-btn');
        this.incompleteTasksList = document.getElementById('incomplete-tasks');
        this.completedTasksList = document.getElementById('completed-tasks');
        this.incompleteCount = document.getElementById('incomplete-count');
    }

    // Bind event listeners
    bindEvents() {
        this.addBtn.addEventListener('click', () => this.addTask());
        this.taskInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.addTask();
        });
        this.clearCompletedBtn.addEventListener('click', () => this.clearCompletedTasks());
        
        // Auto-save on input
        this.taskInput.addEventListener('input', () => {
            this.addBtn.disabled = this.taskInput.value.trim() === '';
        });
    }

    // Generate unique ID for tasks
    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }

    // Add new task
    addTask() {
        const text = this.taskInput.value.trim();
        if (!text) return;

        const task = {
            id: this.generateId(),
            text: text,
            completed: false,
            createdAt: new Date().toISOString()
        };

        this.tasks.push(task);
        this.taskInput.value = '';
        this.addBtn.disabled = true;
        this.saveTasks();
        this.updateUI();
    }

    // Toggle task completion status
    toggleTask(id) {
        const task = this.tasks.find(t => t.id === id);
        if (task) {
            task.completed = !task.completed;
            this.saveTasks();
            this.updateUI();
        }
    }

    // Delete task
    deleteTask(id) {
        if (confirm('Are you sure you want to delete this task?')) {
            this.tasks = this.tasks.filter(t => t.id !== id);
            this.saveTasks();
            this.updateUI();
        }
    }

    // Start editing task
    startEdit(id) {
        if (this.currentEditingId) {
            this.cancelEdit(this.currentEditingId);
        }
        
        this.currentEditingId = id;
        const taskElement = document.querySelector(`[data-id="${id}"]`);
        const textElement = taskElement.querySelector('.task-text');
        const actionsElement = taskElement.querySelector('.task-actions');
        
        const currentText = textElement.textContent;
        textElement.innerHTML = `<input type="text" class="edit-input" value="${this.escapeHtml(currentText)}" maxlength="200">`;
        
        actionsElement.innerHTML = `
            <button class="task-btn save-btn" onclick="todoApp.saveEdit('${id}')">Save</button>
            <button class="task-btn cancel-btn" onclick="todoApp.cancelEdit('${id}')">Cancel</button>
        `;
        
        const input = textElement.querySelector('.edit-input');
        input.focus();
        input.select();
        
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.saveEdit(id);
            if (e.key === 'Escape') this.cancelEdit(id);
        });
    }

    // Save edited task
    saveEdit(id) {
        const taskElement = document.querySelector(`[data-id="${id}"]`);
        const input = taskElement.querySelector('.edit-input');
        const newText = input.value.trim();
        
        if (!newText) {
            alert('Task text cannot be empty');
            input.focus();
            return;
        }

        const task = this.tasks.find(t => t.id === id);
        if (task) {
            task.text = newText;
            this.saveTasks();
        }
        
        this.currentEditingId = null;
        this.updateUI();
    }

    // Cancel editing
    cancelEdit(id) {
        this.currentEditingId = null;
        this.updateUI();
    }

    // Clear all completed tasks
    clearCompletedTasks() {
        const completedCount = this.tasks.filter(t => t.completed).length;
        if (completedCount === 0) {
            alert('No completed tasks to clear');
            return;
        }
        
        if (confirm(`Are you sure you want to delete ${completedCount} completed task${completedCount > 1 ? 's' : ''}?`)) {
            this.tasks = this.tasks.filter(t => !t.completed);
            this.saveTasks();
            this.updateUI();
        }
    }

    // Create task element HTML
    createTaskElement(task) {
        const isCompleted = task.completed ? 'completed' : '';
        return `
            <li class="task-item ${isCompleted}" data-id="${task.id}">
                <input type="checkbox" class="task-checkbox" ${task.completed ? 'checked' : ''} 
                       onchange="todoApp.toggleTask('${task.id}')">
                <span class="task-text">${this.escapeHtml(task.text)}</span>
                <div class="task-actions">
                    <button class="task-btn edit-btn" onclick="todoApp.startEdit('${task.id}')" 
                            ${task.completed ? 'disabled' : ''}>Edit</button>
                    <button class="task-btn delete-btn" onclick="todoApp.deleteTask('${task.id}')">Delete</button>
                </div>
            </li>
        `;
    }

    // Update the UI
    updateUI() {
        const incompleteTasks = this.tasks.filter(t => !t.completed);
        const completedTasks = this.tasks.filter(t => t.completed);

        // Update incomplete tasks
        if (incompleteTasks.length === 0) {
            this.incompleteTasksList.innerHTML = '<div class="empty-state">No incomplete tasks</div>';
        } else {
            this.incompleteTasksList.innerHTML = incompleteTasks
                .map(task => this.createTaskElement(task))
                .join('');
        }

        // Update completed tasks
        if (completedTasks.length === 0) {
            this.completedTasksList.innerHTML = '<div class="empty-state">No completed tasks</div>';
        } else {
            this.completedTasksList.innerHTML = completedTasks
                .map(task => this.createTaskElement(task))
                .join('');
        }

        // Update counter
        this.incompleteCount.textContent = incompleteTasks.length;

        // Update button states
        this.addBtn.disabled = this.taskInput.value.trim() === '';
        this.clearCompletedBtn.disabled = completedTasks.length === 0;
    }

    // Save tasks to localStorage
    saveTasks() {
        try {
            localStorage.setItem('todoTasks', JSON.stringify(this.tasks));
        } catch (error) {
            console.error('Failed to save tasks to localStorage:', error);
            alert('Failed to save tasks. Please check if localStorage is available.');
        }
    }

    // Load tasks from localStorage
    loadTasks() {
        try {
            const saved = localStorage.getItem('todoTasks');
            if (saved) {
                this.tasks = JSON.parse(saved);
                // Validate loaded data
                this.tasks = this.tasks.filter(task => 
                    task && typeof task.text === 'string' && typeof task.completed === 'boolean'
                );
            }
        } catch (error) {
            console.error('Failed to load tasks from localStorage:', error);
            this.tasks = [];
        }
    }

    // Utility function to escape HTML
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Get statistics
    getStats() {
        return {
            total: this.tasks.length,
            completed: this.tasks.filter(t => t.completed).length,
            incomplete: this.tasks.filter(t => !t.completed).length
        };
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.todoApp = new TodoApp();
});

// Export for potential testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TodoApp;
}