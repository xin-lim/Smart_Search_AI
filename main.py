# main.py
import datetime
import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import json
import os
from openai import OpenAI

client = OpenAI(api_key = "sk-18396a4dac4b4b4a856fdc3d313a21f3",
                base_url= "https://api.deepseek.com")

class DeepSeekAssistant:
    def __init__(self, root):
        self.root = root
        self.history = []

        # Configure window
        root.title("DeepSeek Assistant")
        root.geometry("700x500")

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Input Section
        self.query_label = tk.Label(self.root, text="Ask DeepSeek:")
        self.query_entry = tk.Entry(self.root, width=70)
        self.ask_button = tk.Button(self.root, text="Search", command=self.ask_question)

        # Response Display
        self.response_area = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            width=80,
            height=20
        )

        # Report Generation
        self.report_button = tk.Button(
            self.root,
            text="Generate HTML Report",
            command=self.generate_html_report
        )

        # Layout using grid
        self.query_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.query_entry.grid(row=1, column=0, padx=10, pady=5)
        self.ask_button.grid(row=1, column=1, padx=5, pady=5)
        self.response_area.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.report_button.grid(row=3, column=0, columnspan=2, pady=5)
        
    # Add to DeepSeekAssistant class

    def ask_question(self):
        question = self.query_entry.get().strip()
        if not question:
            messagebox.showwarning("Empty Input", "Please enter a question")
            return

        try:
            # Use the existing client instance instead of making direct requests
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": question}],
                temperature=0.7,
                max_tokens=1000
            )

            # Correct response parsing (using message.content instead of text)
            answer = response.choices[0].message.content.strip()
            self.show_response(question, answer)
            self.query_entry.delete(0, tk.END)

        except requests.exceptions.RequestException as e:
            messagebox.showerror("API Error", f"Request failed: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    # Add to DeepSeekAssistant class
    def show_response(self, question, answer):
        # Display in text area
        formatted_response = f"Q: {question}\\nA: {answer}\\n{'='*50}\\n\\n"
        self.response_area.insert(tk.END, formatted_response)

        # Store in history
        self.history.append({
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "question": question,
            "answer": answer
        })

        # Auto-scroll to bottom
        self.response_area.see(tk.END)

    # Add to DeepSeekAssistant class
    def generate_html_report(self):
        if not self.history:
            messagebox.showinfo("Empty Report", "No queries to report")
            return

        try:
            # Create reports directory if not exists
            if not os.path.exists("reports"):
                os.makedirs("reports")

            # Generate filename with timestamp
            filename = f"reports/report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

            # Build HTML content
            html_content = f"""<html>
            <head>
                <title>DeepSeek Report</title>
                <style>
                    body {{
                        font-family: 'Segoe UI', Arial, sans-serif;
                        margin: 0;
                        background: #f8f9fa;
                    }}
                    .container {{
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 30px;
                    }}
                    .report-header {{
                        text-align: center;
                        margin-bottom: 40px;
                        padding-bottom: 25px;
                        border-bottom: 2px solid #e9ecef;
                    }}
                    .main-title {{
                        color: #2c3e50;
                        font-size: 2.4em;
                        margin-bottom: 8px;
                    }}
                    .report-subtitle {{
                        color: #7f8c8d;
                        font-size: 1.1em;
                        margin-bottom: 15px;
                    }}
                    .metadata {{
                        display: flex;
                        justify-content: center;
                        gap: 25px;
                        color: #95a5a6;
                        font-size: 0.95em;
                        margin-bottom: 20px;
                    }}
                    .section-title {{
                        color: #2c3e50;
                        font-size: 1.4em;
                        margin: 25px 0 15px;
                        padding-left: 15px;
                        border-left: 4px solid #3498db;
                        position: relative;
                    }}
                    .section-title::before {{
                        content: "•";
                        color: #3498db;
                        position: absolute;
                        left: -10px;
                        top: -2px;
                        font-size: 1.8em;
                    }}
                    .subsection {{
                        margin-left: 25px;
                        margin-bottom: 20px;
                    }}
                    .subsection-title {{
                        color: #3498db;
                        font-weight: 600;
                        margin: 15px 0 10px;
                        display: flex;
                        align-items: center;
                        gap: 8px;
                    }}
                    .subsection-title i {{
                        color: #7f8c8d;
                        font-size: 0.9em;
                    }}
                    .qa-card {{
                        background: white;
                        border-radius: 8px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                        margin-bottom: 25px;
                        padding: 25px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="report-header">
                        <h1 class="main-title">📑 DeepSeek Assistant Report</h1>
                        <div class="metadata">
                            <span>Total Queries: {len(self.history)}</span>
                            <span>|</span>
                            <span>First Query: {self.history[0]['timestamp']}</span>
                            <span>|</span>
                            <span>Last Query: {self.history[-1]['timestamp']}</span>
                        </div>
                        <h2 class="report-subtitle">Analysis Report • {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</h2>
                    </div>

                    <h2 class="section-title">Conversation History</h2>
                    <div class="subsection">
                        <p class="subsection-title">
                            <i class="fas fa-comment-dots"></i>
                            Session Summary
                        </p>
                        <div class="summary-content">
                            <p>Total interactions: {len(self.history)}</p>
                            <p>Date range: {self.history[0]['timestamp']} to {self.history[-1]['timestamp']}</p>
                        </div>
                    </div>"""

            for idx, item in enumerate(self.history, 1):
                html_content += f"""
                    <div class="qa-card">
                        <div class="subsection">
                            <p class="subsection-title">
                                <i class="fas fa-question-circle"></i>
                                Interaction #{idx} • {item['timestamp']}
                            </p>
                            <div class="subsection">
                                <p class="subsection-title" style="color: #27ae60;">
                                    <i class="fas fa-question"></i>
                                    Question
                                </p>
                                <ul class="bullet-list">
                                    <li>{item['question']}</li>
                                </ul>
                            </div>
                            <div class="subsection">
                                <p class="subsection-title" style="color: #e67e22;">
                                    <i class="fas fa-lightbulb"></i>
                                    Answer
                                </p>
                                <ul class="bullet-list">"""
                
                for line in item['answer'].split('\n'):
                    if line.strip():
                        html_content += f"<li>{line.strip()}</li>"
                
                html_content += """</ul>
                            </div>
                        </div>
                    </div>"""

            html_content += """</div>
            </body>
            </html>"""

            # Write to file
            with open(filename, "w") as f:
                f.write(html_content)

            messagebox.showinfo("Success", f"Report generated:\\n{filename}")

        except Exception as e:
            messagebox.showerror("Report Error", f"Failed to generate report: {str(e)}")

# Add to bottom of main.py
if __name__ == "__main__":
    root = tk.Tk()
    app = DeepSeekAssistant(root)
    root.mainloop()
