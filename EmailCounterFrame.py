import tkinter as tk
from tkinter import ttk, filedialog
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class EmailCounterFrame(tk.Frame):
    """Frame for the Email Counter functionality."""

    def __init__(self, container):
        super().__init__(container)
        self.create_widgets()
        self.place_widgets()

    def fetch_subpages(self, domain):
        try:
            response = requests.get(domain, verify=False)
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            subpages = []
            for link in soup.find_all('a', href=True):
                subpage_url = link['href']
                full_url = urljoin(domain, subpage_url)
                subpages.append(full_url)
            return subpages
        except requests.exceptions.RequestException as e:
            return []

    def count_email_occurrences(self, subpage_url, email_to_search):
        try:
            response = requests.get(subpage_url, verify=False)
            html_content = response.text
            return html_content.count(email_to_search)
        except requests.exceptions.RequestException as e:
            return 0

    def search_and_update_status(self):
        domain = self.entry.get()
        email_to_search = self.email_entry.get()
        subpages = self.fetch_subpages(domain)
        
        for subpage in subpages:
            self.update_status(f"Searching subpage: {subpage}")
            self.update()  # Update GUI
            email_count = self.count_email_occurrences(subpage, email_to_search)
            self.result_table.insert("", tk.END, values=(subpage, email_count))
        
        self.update_status("Search done")

    def export_to_html(self, filename, data):
        with open(filename, 'w') as f:
            f.write('<html><head><title>Results</title></head><body>')
            f.write('<table border="1"><tr><th>Subpage</th><th>Email Count</th></tr>')
            for subpage, count in data:
                f.write(f'<tr><td><a href="{subpage}">{subpage}</a></td><td>{count}</td></tr>')
            f.write('</table></body></html>')

    def export_to_csv(self, filename, data):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Subpage', 'Email Count'])
            for row in data:
                writer.writerow(row)

    def export_results(self):
        file_type = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("HTML file", "*.html"), ("CSV file", "*.csv")])
        if file_type:
            data = [(self.result_table.set(item, 'Subpage'), self.result_table.set(item, 'Email Count')) for item in self.result_table.get_children()]
            if file_type.endswith('.html'):
                self.export_to_html(file_type, data)
            else:
                self.export_to_csv(file_type, data)

    def update_status(self, status):
        self.status_label.config(text=status)

    def create_widgets(self):
        self.top_frame = tk.Frame(self)
        self.entry = tk.Entry(self.top_frame)
        self.entry.insert(0, "Enter domain here (https://www.domain.com)")
        self.email_entry = tk.Entry(self.top_frame)
        self.email_entry.insert(0, "Enter email here (my@mail.com)")
        self.search_button = tk.Button(self.top_frame, text="Search", command=self.search_and_update_status)
        
        self.table_frame = tk.Frame(self)
        columns = ('Subpage', 'Email Count')
        self.result_table = ttk.Treeview(self.table_frame, columns=columns, show='headings')
        self.result_table.heading('Subpage', text='Subpage', anchor='w')
        self.result_table.heading('Email Count', text='Email Count', anchor='w')
        self.result_table.column('Subpage', width=600)
        self.result_table.column('Email Count', width=100)

        self.status_label = tk.Label(self, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W, width=100)
        self.export_button = tk.Button(self, text="Export", command=self.export_results)
    
    def place_widgets(self):
        # Place widgets in the frame
        self.top_frame.pack(fill=tk.X)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.email_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_button.pack(side=tk.RIGHT, padx=5)
        self.table_frame.pack(fill=tk.BOTH, expand=True)
        self.result_table.pack(fill=tk.BOTH, expand=True)
        self.status_label.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X)
        self.export_button.pack(pady=5)
