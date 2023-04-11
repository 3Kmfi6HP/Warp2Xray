import ipaddress

# 定义 IP 段列表
ip_ranges = [
  "162.159.192.0/24", "162.159.193.0/24", "162.159.195.0/24",
  "188.114.96.0/24", "188.114.97.0/24", "188.114.98.0/24", "188.114.99.0/24"
]

# 定义 IP 地址列表
ip_list = []

# 循环遍历 IP 段列表，将每个 IP 段转换成 IP 地址，并添加到 IP 地址列表中
for ip_range in ip_ranges:
  ip_network = ipaddress.ip_network(ip_range)
  for ip_address in ip_network:
    ip_list.append(str(ip_address))

# 将 IP 地址列表写入文件 ip.txt
with open("ip.txt", "w") as f:
  f.write("\n".join(ip_list))
