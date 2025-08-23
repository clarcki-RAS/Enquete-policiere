import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import tempfile
import os

class PrologInvestigationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 Système d'Enquête Policière")
        self.root.geometry("700x600")
        self.root.configure(bg='#2c3e50')
        
        # Style moderne
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configuration des styles
        self.style.configure('TFrame', background='#2c3e50')
        self.style.configure('TLabel', background='#2c3e50', foreground='white', font=('Arial', 10))
        self.style.configure('Title.TLabel', font=('Arial', 18, 'bold'), foreground='#3498db')
        self.style.configure('TButton', font=('Arial', 10, 'bold'), padding=10)
        self.style.configure('TCombobox', padding=5)
        self.style.configure('Result.TText', font=('Consolas', 9))
        
        # Couleurs personnalisées
        self.style.map('TButton',
                      background=[('active', '#2980b9'), ('pressed', '#1c638e')],
                      foreground=[('active', 'white'), ('pressed', 'white')])
        
        # Cadre principal
        main_frame = ttk.Frame(root, padding="20", style='TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # En-tête
        header_frame = ttk.Frame(main_frame, style='TFrame')
        header_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky=(tk.W, tk.E))
        
        # Titre avec icône
        title_label = ttk.Label(header_frame, text="🔍 Système d'Enquête Policière", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0)
        
        # Sous-titre
        subtitle_label = ttk.Label(header_frame, text="Vérifiez la culpabilité des suspects", 
                                  font=('Arial', 12), foreground='#bdc3c7')
        subtitle_label.grid(row=1, column=0, pady=(5, 0))
        
        # Cadre de sélection
        selection_frame = ttk.LabelFrame(main_frame, text=" Sélection ", padding="15")
        selection_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Sélection du suspect
        ttk.Label(selection_frame, text="Suspect:", font=('Arial', 11, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.suspect_var = tk.StringVar()
        suspects = ["john", "mary", "alice", "bruno", "sophie"]
        self.suspect_combo = ttk.Combobox(selection_frame, textvariable=self.suspect_var, 
                                         values=suspects, width=20, font=('Arial', 10))
        self.suspect_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        self.suspect_combo.current(0)
        
        # Sélection du type de crime
        ttk.Label(selection_frame, text="Type de crime:", font=('Arial', 11, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=10)
        self.crime_var = tk.StringVar()
        crimes = ["vol", "assassinat", "escroquerie"]
        self.crime_combo = ttk.Combobox(selection_frame, textvariable=self.crime_var, 
                                       values=crimes, width=20, font=('Arial', 10))
        self.crime_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=10, padx=(10, 0))
        self.crime_combo.current(0)
        
        # Boutons
        button_frame = ttk.Frame(main_frame, style='TFrame')
        button_frame.grid(row=2, column=0, columnspan=2, pady=15)
        
        self.check_button = ttk.Button(button_frame, text="🔎 Vérifier la culpabilité", 
                                      command=self.check_guilt, style='TButton')
        self.check_button.grid(row=0, column=0, padx=10)
        
        self.clear_button = ttk.Button(button_frame, text="🗑️ Effacer les résultats", 
                                      command=self.clear_results, style='TButton')
        self.clear_button.grid(row=0, column=1, padx=10)
        
        # Cadre des résultats
        result_frame = ttk.LabelFrame(main_frame, text=" Résultats ", padding="10")
        result_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Zone de texte pour les résultats avec style
        self.result_text = tk.Text(result_frame, height=12, width=60, font=('Consolas', 9),
                                  bg='#ecf0f1', fg='#2c3e50', relief=tk.FLAT, 
                                  borderwidth=1, padx=10, pady=10)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Barre de défilement pour le texte
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        # Statut en bas de la fenêtre
        self.status_var = tk.StringVar()
        self.status_var.set("Prêt")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              foreground='#7f8c8d', font=('Arial', 9))
        status_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Configuration des poids pour le redimensionnement
        selection_frame.columnconfigure(1, weight=1)
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        # Charger le fichier Prolog
        self.prolog_file = "logique.pl"
        
        # Centrer la fenêtre
        self.center_window()
        
        # Configurer les styles de texte
        self.result_text.tag_configure('guilty', foreground='#e74c3c', font=('Consolas', 9, 'bold'))  # Rouge pour coupable
        self.result_text.tag_configure('not_guilty', foreground='#27ae60', font=('Consolas', 9, 'bold'))  # Vert pour non coupable
        self.result_text.tag_configure('error', foreground='#c0392b', font=('Consolas', 9, 'bold'))
        self.result_text.tag_configure('unknown', foreground='#f39c12', font=('Consolas', 9, 'bold'))
        self.result_text.tag_configure('normal', foreground='#2c3e50', font=('Consolas', 9))
        
    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def check_guilt(self):
        suspect = self.suspect_var.get()
        crime_type = self.crime_var.get()
        
        if not suspect or not crime_type:
            messagebox.showerror("Erreur", "Veuillez sélectionner un suspect et un type de crime.")
            return
        
        self.status_var.set("Vérification en cours...")
        self.root.update()
        
        try:
            # Exécuter la requête avec SWI-Prolog
            cmd = ['swipl', '-q', '-s', self.prolog_file, '-g', f'crime({suspect}, {crime_type})', '-t', 'halt']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            # Afficher le résultat
            output = result.stdout.strip()
            error_output = result.stderr.strip()
            
            # Appliquer un style différent selon le résultat
            self.result_text.insert(tk.END, f"🔍 Enquête: {suspect} - {crime_type}\n", 'normal')
            
            if "coupable" in output:
                self.result_text.insert(tk.END, f"🔴 {output}\n", 'guilty')  # Rouge pour coupable
            elif "non coupable" in output:
                self.result_text.insert(tk.END, f"🟢 {output}\n", 'not_guilty')  # Vert pour non coupable
            elif error_output:
                self.result_text.insert(tk.END, f"⚠️  Erreur: {error_output}\n", 'error')
            else:
                self.result_text.insert(tk.END, "❓ Aucun résultat retourné.\n", 'unknown')
                
            self.result_text.insert(tk.END, "―" * 50 + "\n\n", 'normal')
            
            self.status_var.set("Vérification terminée")
                
        except subprocess.TimeoutExpired:
            self.result_text.insert(tk.END, f"⏰ {suspect} - {crime_type}: Timeout\n", 'error')
            self.result_text.insert(tk.END, "―" * 50 + "\n\n", 'normal')
            self.status_var.set("Timeout - La requête a pris trop de temps")
        except Exception as e:
            self.result_text.insert(tk.END, f"💥 {suspect} - {crime_type}: Erreur - {str(e)}\n", 'error')
            self.result_text.insert(tk.END, "―" * 50 + "\n\n", 'normal')
            self.status_var.set("Erreur d'exécution")
    
    def clear_results(self):
        self.result_text.delete(1.0, tk.END)
        self.status_var.set("Résultats effacés")

if __name__ == "__main__":
    root = tk.Tk()
    app = PrologInvestigationSystem(root)
    root.mainloop()