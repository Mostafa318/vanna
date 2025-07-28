// Vanna Farsi Frontend JavaScript

class VannaFarsiApp {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.loadSuggestions();
        this.isProcessing = false;
    }

    initializeElements() {
        this.questionInput = document.getElementById('question-input');
        this.sendBtn = document.getElementById('send-btn');
        this.chatMessages = document.getElementById('chat-messages');
        this.resultsArea = document.getElementById('results-area');
        this.sqlQuery = document.getElementById('sql-query');
        this.dataTable = document.getElementById('data-table');
        this.chartContainer = document.getElementById('chart-container');
        this.suggestionsContainer = document.getElementById('suggestions');
        this.loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
    }

    bindEvents() {
        // Send button click
        this.sendBtn.addEventListener('click', () => this.sendQuestion());
        
        // Enter key press
        this.questionInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendQuestion();
            }
        });

        // Input focus for better UX
        this.questionInput.addEventListener('focus', () => {
            this.questionInput.style.borderColor = '#007bff';
        });

        this.questionInput.addEventListener('blur', () => {
            this.questionInput.style.borderColor = '#e9ecef';
        });
    }

    async loadSuggestions() {
        try {
            const response = await fetch('/api/suggestions');
            const data = await response.json();
            this.displaySuggestions(data.suggestions);
        } catch (error) {
            console.error('Error loading suggestions:', error);
        }
    }

    displaySuggestions(suggestions) {
        this.suggestionsContainer.innerHTML = '';
        suggestions.forEach(suggestion => {
            const suggestionElement = document.createElement('div');
            suggestionElement.className = 'suggestion-item';
            suggestionElement.textContent = suggestion;
            suggestionElement.addEventListener('click', () => {
                this.questionInput.value = suggestion;
                this.questionInput.focus();
            });
            this.suggestionsContainer.appendChild(suggestionElement);
        });
    }

    async sendQuestion() {
        if (this.isProcessing) return;

        const question = this.questionInput.value.trim();
        if (!question) {
            this.showError('لطفاً سوالی بنویسید');
            return;
        }

        this.isProcessing = true;
        this.setLoadingState(true);
        this.loadingModal.show();

        try {
            // Add user message to chat
            this.addMessage(question, 'user');

            // Send question to API
            const response = await fetch('/api/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question })
            });

            const data = await response.json();

            if (response.ok) {
                // Add bot response
                this.addMessage('کوئری SQL تولید شد و نتایج آماده است.', 'bot');
                
                // Display results
                this.displayResults(data);
                
                // Clear input
                this.questionInput.value = '';
                
            } else {
                this.showError(data.error || 'خطا در پردازش سوال');
            }

        } catch (error) {
            console.error('Error sending question:', error);
            this.showError('خطا در ارتباط با سرور');
        } finally {
            this.isProcessing = false;
            this.setLoadingState(false);
            this.loadingModal.hide();
        }
    }

    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const icon = sender === 'bot' ? 'fas fa-robot text-primary' : 'fas fa-user text-success';
        const name = sender === 'bot' ? 'وانا' : 'شما';
        
        messageDiv.innerHTML = `
            <div class="message-content">
                <div class="message-header">
                    <i class="${icon}"></i>
                    <span class="ms-2">${name}</span>
                </div>
                <div class="message-text">
                    ${text}
                </div>
            </div>
        `;

        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    displayResults(data) {
        // Show results area
        this.resultsArea.style.display = 'block';
        
        // Display SQL query
        this.sqlQuery.textContent = data.sql;
        
        // Display data table
        this.displayDataTable(data.data, data.columns);
        
        // Display chart if available
        if (data.chart) {
            this.displayChart(data.chart);
        } else {
            this.chartContainer.innerHTML = '<p class="text-muted text-center">نمودار برای این داده‌ها در دسترس نیست</p>';
        }
        
        // Scroll to results
        this.resultsArea.scrollIntoView({ behavior: 'smooth' });
    }

    displayDataTable(data, columns) {
        if (!data || data.length === 0) {
            this.dataTable.innerHTML = '<p class="text-muted text-center">داده‌ای برای نمایش وجود ندارد</p>';
            return;
        }

        let tableHTML = '<table class="table table-striped table-hover">';
        
        // Header
        tableHTML += '<thead><tr>';
        columns.forEach(column => {
            tableHTML += `<th>${this.formatColumnName(column)}</th>`;
        });
        tableHTML += '</tr></thead>';
        
        // Body
        tableHTML += '<tbody>';
        data.forEach(row => {
            tableHTML += '<tr>';
            columns.forEach(column => {
                const value = row[column];
                tableHTML += `<td>${this.formatCellValue(value)}</td>`;
            });
            tableHTML += '</tr>';
        });
        tableHTML += '</tbody></table>';
        
        this.dataTable.innerHTML = tableHTML;
    }

    displayChart(chartData) {
        try {
            const chartConfig = JSON.parse(chartData);
            
            // Update chart layout for RTL
            if (chartConfig.layout) {
                chartConfig.layout.direction = 'rtl';
                chartConfig.layout.font = {
                    family: 'Vazirmatn, Tahoma, Arial, sans-serif'
                };
            }
            
            Plotly.newPlot(this.chartContainer, chartConfig.data, chartConfig.layout, {
                responsive: true,
                displayModeBar: true,
                modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d']
            });
        } catch (error) {
            console.error('Error displaying chart:', error);
            this.chartContainer.innerHTML = '<p class="text-muted text-center">خطا در نمایش نمودار</p>';
        }
    }

    formatColumnName(column) {
        // Convert column names to Persian if possible
        const columnMappings = {
            'name': 'نام',
            'city': 'شهر',
            'email': 'ایمیل',
            'registration_date': 'تاریخ ثبت‌نام',
            'product_name': 'نام محصول',
            'quantity': 'تعداد',
            'price': 'قیمت',
            'order_date': 'تاریخ سفارش',
            'department': 'بخش',
            'salary': 'حقوق',
            'hire_date': 'تاریخ استخدام',
            'total_quantity': 'مجموع تعداد',
            'avg_salary': 'میانگین حقوق',
            'order_count': 'تعداد سفارشات'
        };
        
        return columnMappings[column] || column;
    }

    formatCellValue(value) {
        if (value === null || value === undefined) {
            return '-';
        }
        
        // Format numbers with Persian separators
        if (typeof value === 'number') {
            if (value >= 1000000) {
                return (value / 1000000).toLocaleString('fa-IR') + ' میلیون';
            } else if (value >= 1000) {
                return value.toLocaleString('fa-IR');
            }
            return value.toString();
        }
        
        // Format dates
        if (typeof value === 'string' && value.match(/^\d{4}-\d{2}-\d{2}$/)) {
            const date = new Date(value);
            return date.toLocaleDateString('fa-IR');
        }
        
        return value.toString();
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.innerHTML = `
            <i class="fas fa-exclamation-triangle me-2"></i>
            ${message}
        `;
        
        this.chatMessages.appendChild(errorDiv);
        this.scrollToBottom();
        
        // Remove error message after 5 seconds
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }

    setLoadingState(loading) {
        this.sendBtn.disabled = loading;
        this.questionInput.disabled = loading;
        
        if (loading) {
            this.sendBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> در حال پردازش...';
        } else {
            this.sendBtn.innerHTML = '<i class="fas fa-paper-plane"></i> ارسال';
        }
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    // Utility method to check if Ollama is running
    async checkOllamaStatus() {
        try {
            const response = await fetch('http://localhost:11434/api/tags');
            return response.ok;
        } catch (error) {
            return false;
        }
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.vannaApp = new VannaFarsiApp();
    
    // Check Ollama status on startup
    window.vannaApp.checkOllamaStatus().then(isRunning => {
        if (!isRunning) {
            console.warn('Ollama is not running. Please start Ollama to use the application.');
            // You could show a notification to the user here
        }
    });
});

// Add some utility functions for better UX
window.addEventListener('beforeunload', () => {
    // Clean up any resources if needed
});

// Handle window resize for responsive design
window.addEventListener('resize', () => {
    // Adjust chart size if needed
    if (window.vannaApp && window.vannaApp.chartContainer) {
        const charts = document.querySelectorAll('.js-plotly-plot');
        charts.forEach(chart => {
            Plotly.Plots.resize(chart);
        });
    }
});