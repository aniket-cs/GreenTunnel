from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.core.window import Window

import dns.resolver
import requests
import threading
import os

Window.clearcolor = (0.8, 1, 0.8, 1)  # green background

class DNSApp(BoxLayout):
    def __init__(self, **kwargs):
        super(DNSApp, self).__init__(orientation='vertical', padding=10, spacing=10, **kwargs)

        self.add_widget(Label(text='GreenTunnel - DNS & Subdomain Enumeration Tool', font_size=35, bold=True, color=(0, 0.5, 0, 1), size_hint=(1, None), height=150))
        self.domain_input = TextInput(hint_text='Enter domain (e.g. youtube.com)', size_hint_y=None, height=50)

        file_chooser_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        self.file_path_label = Label(text='Please select subdomain file ---->', size_hint_x=0.8, color=(0, 0, 0, 1))
        file_btn = Button(text='Choose File', size_hint_x=0.3)
        file_btn.bind(on_press=self.open_file_chooser)
        file_chooser_layout.add_widget(self.file_path_label)
        file_chooser_layout.add_widget(file_btn)

        button_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        dns_btn = Button(text='Run DNS Enumeration')
        dns_btn.bind(on_press=self.run_dns)
        subdomain_btn = Button(text='Run Subdomain Enumeration')
        subdomain_btn.bind(on_press=self.run_subdomains)
        button_layout.add_widget(dns_btn)
        button_layout.add_widget(subdomain_btn)

        self.output_label = Label(size_hint_y=None, height=500, text='', color=(0, 0, 0, 1), halign='left', valign='top')
        self.output_label.bind(size=self.update_text_size)

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.output_label)

        self.add_widget(self.domain_input)
        self.add_widget(file_chooser_layout)
        self.add_widget(button_layout)
        self.add_widget(scroll)

        self.subdomain_file_path = ''

    def update_text_size(self, instance, value):
        self.output_label.text_size = (self.output_label.width, None)
        self.output_label.texture_update()
        self.output_label.height = self.output_label.texture_size[1]

    def update_output(self, text):
        self.output_label.text += text + '\n'

    def open_file_chooser(self, instance):
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView()
        popup = Popup(title="Select Subdomain File", content=content, size_hint=(0.9, 0.9))

        def select_file(instance):
            if filechooser.selection:
                self.subdomain_file_path = filechooser.selection[0]
                self.file_path_label.text = os.path.basename(self.subdomain_file_path)
                popup.dismiss()

        select_btn = Button(text="Select", size_hint_y=None, height=40)
        select_btn.bind(on_press=select_file)

        content.add_widget(filechooser)
        content.add_widget(select_btn)

        popup.open()

    def run_dns(self, instance):
        domain = self.domain_input.text.strip()
        records_type = ['A', 'AAAA', 'CNAME', 'MX', 'TXT', 'SOA']

        if not domain:
            self.show_popup("Error", "Please enter a domain.")
            return

        resolver = dns.resolver.Resolver()
        self.output_label.text = ""
        self.update_output("[+] DNS Enumeration\n")

        for record_type in records_type:
            try:
                answer = resolver.resolve(domain, record_type)
            except dns.resolver.NoAnswer:
                continue
            except dns.resolver.NXDOMAIN:
                self.update_output(f"[-] No such domain: {domain}")
                break
            except Exception as e:
                self.update_output(f"[-] Error resolving {record_type}: {e}")
                continue

            self.update_output(f'\n{record_type} records for {domain}')
            for data in answer:
                self.update_output(f' {data}')

    def run_subdomains(self, instance):
        domain = self.domain_input.text.strip()
        file_path = self.subdomain_file_path

        if not domain or not file_path:
            self.show_popup("Error", "Please enter domain and select subdomain file.")
            return

        if not os.path.exists(file_path):
            self.show_popup("Error", "Subdomain file not found.")
            return

        self.output_label.text = ""
        self.update_output("[+] Subdomain Enumeration\n")

        with open(file_path) as file:
            subdomains = file.read().splitlines()

        discovered = []
        lock = threading.Lock()

        def check_sub(subdomain):
            url = f'http://{subdomain}.{domain}'
            try:
                requests.get(url, timeout=3)
            except requests.ConnectionError:
                pass
            else:
                with lock:
                    discovered.append(url)
                    self.update_output(f"[+] Discovered subdomain: {url}")

        threads = []
        for subdomain in subdomains:
            t = threading.Thread(target=check_sub, args=(subdomain,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        with open("discovered_subdomains.txt", 'w') as f:
            for d in discovered:
                f.write(d + '\n')

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.6, 0.3))
        popup.open()

class GreenTunnelApp(App):
    def build(self):
        return DNSApp()

if __name__ == '__main__':
    GreenTunnelApp().run()
