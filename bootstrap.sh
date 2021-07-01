# Update Packages
apt-get -y update

# Upgrade Packages
apt-get -y upgrade

# DPKG
apt-get install -y dpkg

# GIT
apt-get install -y git

# GCC
apt install -y build-essential
apt-get install -y manpages-dev

# JDK
#apt-get install -y default-jdk
apt install -y openjdk-11-jdk

# CURL
apt-get install -y curl

# BAZEL
apt install -y curl gnupg
curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor > bazel.gpg
mv bazel.gpg /etc/apt/trusted.gpg.d/
echo "deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8" | tee /etc/apt/sources.list.d/bazel.list
apt update 
apt install -y bazel
apt update 
apt full-upgrade
apt install -y bazel-1.0.0

# VERIBLE
git clone https://github.com/google/verible.git
cd verible
bazel build -c opt //...
bazel run -c opt :install -- ~/bin
bazel test -c opt //...