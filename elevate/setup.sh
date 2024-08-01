# #!/bin/bash

# # Function to install MySQL development libraries
# install_mysql_dev() {
#   if [ "$(uname)" == "Darwin" ]; then
#     # macOS
#     echo "Installing MySQL development libraries on macOS..."
#     brew install mysql-client
#   elif [ -f /etc/debian_version ]; then
#     # Debian-based Linux
#     echo "Installing MySQL development libraries on Debian-based Linux..."
#     sudo apt-get update
#     sudo apt-get install -y libmysqlclient-dev
#   elif [ -f /etc/redhat-release ]; then
#     # Red Hat-based Linux
#     echo "Installing MySQL development libraries on Red Hat-based Linux..."
#     sudo yum install -y mysql-devel
#   else
#     echo "Unsupported operating system"
#     exit 1
#   fi
# }

# # Install MySQL development libraries
# install_mysql_dev



# # Set environment variables (if needed)
# export MYSQLCLIENT_CFLAGS=$(mysql_config --cflags)
# export MYSQLCLIENT_LDFLAGS=$(mysql_config --libs)

# # python3.9 manage.py collectstatic --noinput --clear

#!/bin/bash

# Function to install MySQL development libraries
# install_mysql_dev() {
#   if [ "$(uname)" == "Darwin" ]; then
#     # macOS
#     echo "Installing MySQL development libraries on macOS..."
#     brew install mysql-client
#     echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc
#     export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"
#     export LDFLAGS="-L/opt/homebrew/opt/mysql-client/lib"
#     export CPPFLAGS="-I/opt/homebrew/opt/mysql-client/include"
#     export PKG_CONFIG_PATH="/opt/homebrew/opt/mysql-client/lib/pkgconfig"
#   elif [ -f /etc/debian_version ]; then
#     # Debian-based Linux
#     echo "Installing MySQL development libraries on Debian-based Linux..."
#     sudo apt-get update
#     sudo apt-get install -y libmysqlclient-dev
#   elif [ -f /etc/redhat-release ]; then
#     # Red Hat-based Linux
#     echo "Installing MySQL development libraries on Red Hat-based Linux..."
#     sudo yum install -y mysql-devel
#   else
#     echo "Unsupported operating system"
#     exit 1
#   fi
# }

# # Install MySQL development libraries
# install_mysql_dev

# # Ensure Python is available
# if ! command -v python3 &> /dev/null
# then
#     echo "Python3 could not be found, please install it."
#     exit 1
# fi

# # Set environment variables (if needed)
# export MYSQLCLIENT_CFLAGS=$(mysql_config --cflags)
# export MYSQLCLIENT_LDFLAGS=$(mysql_config --libs)

# # Install Python dependencies
# pip3 install -r requirements.txt

#!/bin/bash

# Function to install MySQL development libraries
# install_mysql_dev() {
#   if [ "$(uname)" == "Darwin" ]; then
#     # macOS
#     echo "Installing MySQL development libraries on macOS..."
#     brew install mysql-client || { echo "Failed to install mysql-client via brew"; exit 1; }
#     echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc
#     export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"
#     export LDFLAGS="-L/opt/homebrew/opt/mysql-client/lib"
#     export CPPFLAGS="-I/opt/homebrew/opt/mysql-client/include"
#     export PKG_CONFIG_PATH="/opt/homebrew/opt/mysql-client/lib/pkgconfig"
#   elif [ -f /etc/debian_version ]; then
#     # Debian-based Linux
#     echo "Installing MySQL development libraries on Debian-based Linux..."
#     sudo apt-get update || { echo "Failed to update apt-get"; exit 1; }
#     sudo apt-get install -y libmysqlclient-dev || { echo "Failed to install libmysqlclient-dev"; exit 1; }
#   elif [ -f /etc/redhat-release ]; then
#     # Red Hat-based Linux
#     echo "Installing MySQL development libraries on Red Hat-based Linux..."
#     sudo yum install -y mysql-devel || { echo "Failed to install mysql-devel"; exit 1; }
#   else
#     echo "Unsupported operating system"
#     exit 1
#   fi
# }

# # Install MySQL development libraries
# install_mysql_dev

# # Ensure Python is available
# if ! command -v python3 &> /dev/null; then
#   echo "Python3 could not be found, please install it."
#   exit 1
# fi

# # Set environment variables (if needed)
# export MYSQLCLIENT_CFLAGS=$(mysql_config --cflags) || { echo "Failed to set MYSQLCLIENT_CFLAGS"; exit 1; }
# export MYSQLCLIENT_LDFLAGS=$(mysql_config --libs) || { echo "Failed to set MYSQLCLIENT_LDFLAGS"; exit 1; }

# # Install Python dependencies
# pip3 install -r requirements.txt || { echo "Failed to install Python dependencies"; exit 1; }

# echo "Setup script completed successfully"


#!/bin/bash

# Function to install MySQL development libraries
install_mysql_dev() {
  if [ "$(uname)" == "Darwin" ]; then
    # macOS
    echo "Installing MySQL development libraries on macOS..."
    brew install mysql-client || { echo "Failed to install mysql-client via brew"; exit 1; }
    echo 'export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"' >> ~/.zshrc
    export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"
    export LDFLAGS="-L/opt/homebrew/opt/mysql-client/lib"
    export CPPFLAGS="-I/opt/homebrew/opt/mysql-client/include"
    export PKG_CONFIG_PATH="/opt/homebrew/opt/mysql-client/lib/pkgconfig"
  elif [ -f /etc/debian_version ]; then
    # Debian-based Linux
    echo "Installing MySQL development libraries on Debian-based Linux..."
    sudo apt-get update || { echo "Failed to update apt-get"; exit 1; }
    sudo apt-get install -y libmysqlclient-dev || { echo "Failed to install libmysqlclient-dev"; exit 1; }
  elif [ -f /etc/redhat-release ]; then
    # Red Hat-based Linux
    echo "Installing MySQL development libraries on Red Hat-based Linux..."
    sudo yum install -y mysql-devel || { echo "Failed to install mysql-devel"; exit 1; }
  else
    echo "Unsupported operating system"
    exit 1
  fi
}

# Install MySQL development libraries
install_mysql_dev

# Ensure Python is available
if ! command -v python3 &> /dev/null; then
  echo "Python3 could not be found, please install it."
  exit 1
fi

# Set environment variables (if needed)
export MYSQLCLIENT_CFLAGS=$(mysql_config --cflags) || { echo "Failed to set MYSQLCLIENT_CFLAGS"; exit 1; }
export MYSQLCLIENT_LDFLAGS=$(mysql_config --libs) || { echo "Failed to set MYSQLCLIENT_LDFLAGS"; exit 1; }

# Install Python dependencies
pip3 install -r requirements.txt || { echo "Failed to install Python dependencies"; exit 1; }

echo "Setup script completed successfully"
