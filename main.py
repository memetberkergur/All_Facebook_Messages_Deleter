import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class FacebookMessageDeleter:
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.driver = None
        

    def login(self, username, password):
        # Web sürücüsünü başlatın
        self.driver = webdriver.Chrome(self.driver_path)

        # Web sürücüsünü tam ekran yapın
        self.driver.maximize_window()

        # Facebook'a gidin
        self.driver.get("https://www.facebook.com")


        # Facebook girişi yapın (kullanıcı adı ve şifrenizi girin)
        email_input = self.driver.find_element("id", "email")
        email_input.send_keys(username)

        password_input = self.driver.find_element("id", "pass")
        password_input.send_keys(password)

        password_input.send_keys(Keys.ENTER)

    def delete_messages(self):
        # Mesajlar sayfasına gidin
        self.driver.get("https://www.facebook.com/messages")
        time.sleep(5)

        # Tüm mesajları silin
        while True:
            delete_buttons = self.driver.find_elements("xpath", "//a[@aria-label='Sil']")
            if len(delete_buttons) == 0:
                break

            for delete_button in delete_buttons:
                delete_button.click()
                time.sleep(1)  # Silme işlemi için biraz bekleyin

                # Silme işlemini onaylayın
                confirm_button = self.driver.find_element("xpath", "//button[contains(., 'Sil')]")
                confirm_button.click()
                time.sleep(2)  # Silme işlemi için biraz daha uzun süre bekleyin

    def close(self):
        # Web sürücüsünü kapatın
        if self.driver:
            self.driver.quit()

class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Facebook Toplu Mesaj Silme")
        # Pencerenin boyutunu ve konumunu hesaplayın
        window_width = 350
        window_height = 120
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))

        # Pencerenin ortalanmış konumunu ayarlayın
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Kullanıcı adı etiketi ve giriş alanı
        username_label = tk.Label(self.window, text="Kullanıcı Adı:")
        username_label.pack()

        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack()

        # Şifre etiketi ve giriş alanı
        password_label = tk.Label(self.window, text="Şifre:")
        password_label.pack()

        self.password_entry = tk.Entry(self.window)
        #self.password_entry = tk.Entry(self.window,show="*") # Eğer şifrenin yıldız ile gizlenmesini istiyorsanız bu satırı uncomment ediniz.
        self.password_entry.pack()

        # Giriş düğmesi
        login_button = tk.Button(self.window, text="Giriş", command=self.login_and_delete)
        login_button.pack()

        # Enter tuşuna basıldığında pencerenin kapanmasını sağlayın
        self.window.bind("<Return>", self.login_and_delete)

    def login_and_delete(self, event=None):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # FacebookMessageDeleter sınıfından bir örnek oluşturun
        message_deleter = FacebookMessageDeleter("path/to/chromedriver")
        message_deleter.login(username, password)
        message_deleter.delete_messages()
        message_deleter.close()

        # Pencereyi kapatın
        self.window.destroy()

    def start(self):
        # Ana döngüyü başlatın
        self.window.mainloop()

# GUI'yi başlatın

gui = GUI()
gui.start()
