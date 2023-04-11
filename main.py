import csv
import hashlib
import json

MAX_IPS = 2000
BALANCER_TYPE = "leastPing"
BALANCER_TAG = "balancer"
CONFIG_FILE = "config.json"
RESULT_FILE = "result.csv"

# Read IPs from the CSV file
ips = []
with open(RESULT_FILE, newline="") as csvfile:
  reader = csv.reader(csvfile)
  next(reader)  # Skip header row
  for row in reader:
    if "100.00%" in row:
      # print(row)
      continue
    ip = row[0]  # Extract IP address
    loss = row[1]
    delay = row[2]
    print(ip, loss, delay)
    ips.append(ip)
    if len(ips) >= MAX_IPS:
      break

# Generate outbound configurations for each IP
outbounds = []
for ip in ips:
  tag = hashlib.md5(ip.encode("utf-8")).hexdigest()
  endpoint = f"{ip}"
  outbounds.append({
    "_flag_tag": tag,
    "_flag_proxy": 0,
    "_flag_proxy_tag": "nil",
    "settings": {
      "address":
      ["172.16.0.2/32", "2606:4700:110:87cb:8c72:f6ae:b7b8:90a7/128"],
      "secretKey":
      "2FjQ/hjZVg7pgG13QiTW7JebLJuntYCQ0poCehCQ9G4=",
      "mtu":
      1280,
      "peers": [{
        "publicKey": "bmXOC+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=",
        "endpoint": endpoint
      }]
    },
    "mux": {
      "enabled": False,
      "concurrency": 8
    },
    "protocol": "wireguard",
    "tag": tag
  })

# Generate balancer configuration
selector = [outbound["_flag_tag"] for outbound in outbounds]
balancer_config = {
  "strategy": {
    "type": BALANCER_TYPE
  },
  "selector": selector,
  "tag": BALANCER_TAG
}
balancer_random_config = {
  "strategy": {
    "type": "random"
  },
  "selector": selector,
  "tag": BALANCER_TAG + "2"
}
balancers = [balancer_config, balancer_random_config]
adds_dns = [{
  "settings": {
    "port": 53,
    "network": "tcp",
    "address": "1.1.1.2"
  },
  "protocol": "dns",
  "tag": "dns-out"
}, {
  "protocol": "freedom",
  "tag": "direct"
}, {
  "protocol": "blackhole",
  "tag": "blackhole"
}]
# Generate complete configuration
config = {
  "outbounds":
  outbounds + adds_dns,
  "log": {
    "loglevel": "debug",
  },
  "dns": {
    "servers": [{
      "port": 53,
      "address": "tcp://1.1.1.2:53"
    }],
    "disableCache": False,
    "tag": "dns-in1"
  },
  "policy": {
    "levels": {
      "0": {
        "statsUserUplink": False,
        "statsUserDownlink": False
      }
    }
  },
  "routing": {
    "rules": [{
      "type": "field",
      "inboundTag": ["dns-in"],
      "outboundTag": "dns-out"
    }, {
      "balancerTag": "balancer",
      "type": "field",
      "inboundTag": "socks-1080",
      "network": "tcp,udp"
    }, {
      "balancerTag": "balancer2",
      "inboundTag": "socks-1082",
      "type": "field",
      "network": "tcp,udp"
    }],
    "domainStrategy":
    "IPIfNonMatch",
    "balancers":
    balancers,
    "domainMatcher":
    "hybrid"
  },
  "observatory": {
    "probeInterval": "1m",
    "enableConcurrency": True,
    "probeUrl": "https://www.google.com/generate_204"
  },
  "inbounds": [{
    "port": 1080,
    "tag": "socks-1080",
    "protocol": "socks",
    "sniffing": {
      "enabled": True,
      "destOverride": ["http", "tls"]
    },
    "settings": {
      "udp": True,
      "auth": "noauth"
    },
    "listen": "0.0.0.0"
  }, {
    "port": 1082,
    "tag": "socks-1082",
    "protocol": "socks",
    "sniffing": {
      "enabled": True,
      "destOverride": ["http", "tls"]
    },
    "settings": {
      "udp": True,
      "auth": "noauth"
    },
    "listen": "0.0.0.0"
  }]
}

# Write configuration to file
with open(CONFIG_FILE, "w") as f:
  json.dump(config, f, indent=4)
