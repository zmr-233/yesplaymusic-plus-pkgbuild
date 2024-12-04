import requests
import json

# AUR RPC API 基础 URL
AUR_RPC_URL = "https://aur.archlinux.org/rpc/v5/search/"

# 定义包的基础名称
BASE_PKGNAME = "yesplaymusic"

# 定义自身包名称
SELF_PKGNAME = BASE_PKGNAME + "-plus"

# PKGBUILD 文件路径
PKGBUILD_PATH = "PKGBUILD"

def fetch_aur_packages(base_pkgname):
    """从 AUR 获取与 base_pkgname 相关的所有包信息"""
    response = requests.get(AUR_RPC_URL + base_pkgname)
    if response.status_code == 200:
        data = response.json()
        if data.get("resultcount", 0) > 0:
            return [result["Name"] for result in data["results"]]
    return []

def generate_conflicts_list(base_pkgname):
    """生成 conflicts 数组列表"""
    packages = fetch_aur_packages(base_pkgname)
    # 排除自身
    filtered_packages = [pkg for pkg in packages if pkg != SELF_PKGNAME]
    return filtered_packages

def update_pkgbuild_conflicts(conflicts_list):
    """将 conflicts 列表写入 PKGBUILD"""
    with open("pre-" + PKGBUILD_PATH, "r") as f:
        lines = f.readlines()

    # 找到 @conflicts_list@ 标记
    with open(PKGBUILD_PATH, "w") as f:
        for line in lines:
            if "# @conflicts_list@" in line:
                # 替换标记为 conflicts 数组
                conflicts_str = 'conflicts=(\n' + '\n'.join(f'    "{pkg}"' for pkg in conflicts_list) + '\n)'
                f.write(conflicts_str + "\n")
            else:
                f.write(line)

def main():
    print("Fetching AUR packages...")
    conflicts_list = generate_conflicts_list(BASE_PKGNAME)
    if not conflicts_list:
        print("No conflicts found or error fetching data.")
        return

    print("Updating PKGBUILD with the following conflicts:")
    print(conflicts_list)
    update_pkgbuild_conflicts(conflicts_list)
    print("PKGBUILD updated successfully.")

if __name__ == "__main__":
    main()
