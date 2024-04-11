#!/bin/sh

trap 'sudo networksetup -setsocksfirewallproxystate Wi-fi off' 2

sudo networksetup -setsocksfirewallproxy Wi-fi localhost 9050
sudo networksetup -setsocksfirewallproxystate Wi-fi on

pproxy -l http://:8118 -r socks5://127.0.0.1:9050 & tor
