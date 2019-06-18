
sudo apt-get update

# install chrome
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt-get update 
sudo apt-get install google-chrome-stable

# install chrome driver
wget -N https://chromedriver.storage.googleapis.com/75.0.3770.90/chromedriver_linux64.zip
sudo apt install unzip
unzip chromedriver_linux64.zip
chmod +x chromedriver

# set permissions for chrome driver
sudo mv -f chromedriver /usr/local/share/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver -f
sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver -f

sudo apt-get -y install python3-pip
sudo python3 -m pip install -r requirements.txt